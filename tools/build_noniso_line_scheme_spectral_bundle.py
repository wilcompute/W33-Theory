#!/usr/bin/env python3
"""
Compute the spectral / primitive-idempotent decomposition of the Aut(W33)-invariant
association scheme on the 90 non-isotropic lines of PG(3,3).

Input:
  - W33_nonisotropic_line_association_scheme_bundle.zip
      * scheme_matrices.npz  (B0..B4, Ameet, S)

Output:
  - W33_nonisotropic_line_scheme_spectral_bundle.zip
      * P_eigenmatrix.csv, Q_dual_eigenmatrix.csv
      * primitive_idempotents_coeffs.json (exact rationals in the B-basis)
      * primitive_idempotents_float.npz   (E0..E4 as float64 matrices)
      * generator_identities.json         (B0 = Ameet*S, B3 as a polynomial in Ameet and S)
      * sanity_checks.json
      * README.txt

Optional (if provided):
  - project two 90-vectors (z,m) into scheme eigenspaces and fit an Aut-invariant operator
    D = sum_i alpha_i B_i mapping z -> m (mod 3 and over R).
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MOD3 = 3


def _read_bytes_from_zip(zip_path: Path, inner_path: str) -> bytes:
    with zipfile.ZipFile(zip_path) as zf:
        return zf.read(inner_path)


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _fraction_to_str(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def _invert_matrix_fraction(A: list[list[int]]) -> list[list[Fraction]]:
    n = len(A)
    aug: list[list[Fraction]] = []
    for i in range(n):
        row = [Fraction(int(x), 1) for x in A[i]]
        row.extend(Fraction(int(i == j), 1) for j in range(n))
        aug.append(row)

    for col in range(n):
        pivot = None
        for r in range(col, n):
            if aug[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]

        pv = aug[col][col]
        for c in range(2 * n):
            aug[col][c] /= pv

        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor == 0:
                continue
            for c in range(2 * n):
                aug[r][c] -= factor * aug[col][c]

    return [row[n:] for row in aug]


def _read_90_vector_csv(path: Path) -> np.ndarray:
    """
    Accepts CSV with headers like:
      - line_id,weight
      - line_id,value
      - line_id,x
    Any second column is accepted; values are interpreted as ints mod 3.
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        if not r.fieldnames or "line_id" not in r.fieldnames:
            raise ValueError(f"{path}: expected a 'line_id' column")
        value_cols = [c for c in r.fieldnames if c != "line_id"]
        if not value_cols:
            raise ValueError(f"{path}: expected a second value column besides 'line_id'")
        value_col = value_cols[0]
        out = np.zeros(90, dtype=np.int16)
        seen = set()
        for row in r:
            lid = int(row["line_id"])
            if lid < 0 or lid >= 90:
                raise ValueError(f"{path}: line_id out of range: {lid}")
            if lid in seen:
                raise ValueError(f"{path}: duplicate line_id: {lid}")
            seen.add(lid)
            out[lid] = int(row[value_col]) % MOD3
        if len(seen) != 90:
            missing = [i for i in range(90) if i not in seen][:10]
            raise ValueError(f"{path}: expected 90 rows; missing e.g. {missing}")
        return out.astype(np.int16)


@dataclass(frozen=True)
class IdempotentInfo:
    eid: str
    multiplicity: int
    lambda_ameet: int
    epsilon_sigma: int


def _cluster_eigenvalues_int(evals: np.ndarray, tol: float = 1e-6) -> dict[int, np.ndarray]:
    """
    Cluster eigenvalues by rounding to nearest integer (with a tolerance check).
    Returns map: integer eigenvalue -> indices array.
    """
    rounded = np.rint(evals).astype(int)
    for i, (w, wr) in enumerate(zip(evals, rounded, strict=True)):
        if abs(w - wr) > tol:
            raise ValueError(f"Eigenvalue {i} not near integer: {w} (round {wr})")
    out: dict[int, list[int]] = {}
    for i, wr in enumerate(rounded):
        out.setdefault(int(wr), []).append(i)
    return {k: np.array(v, dtype=int) for k, v in out.items()}


def _as_int_close(x: float, tol: float = 1e-6) -> int:
    r = int(round(x))
    if abs(x - r) > tol:
        raise ValueError(f"Expected near-integer, got {x}")
    return r


def _sigma_sign_close(x: float, tol: float = 1e-6) -> int:
    r = int(round(x))
    if r not in (-1, 1) or abs(x - r) > tol:
        raise ValueError(f"Expected near ±1, got {x}")
    return r


def _fit_invariant_operator_mod3(B: list[np.ndarray], z: np.ndarray, m: np.ndarray) -> dict[str, object]:
    """
    Brute-force best D = sum_i a_i B_i over Z3 (243 combos).
    Returns best coefficients and mismatch stats.
    """
    z = z.astype(np.int16) % MOD3
    m = m.astype(np.int16) % MOD3
    Bz = [(Bi.astype(np.int16) @ z) % MOD3 for Bi in B]

    best = None
    for a0 in range(3):
        for a1 in range(3):
            for a2 in range(3):
                for a3 in range(3):
                    for a4 in range(3):
                        coeff = (a0, a1, a2, a3, a4)
                        y = (a0 * Bz[0] + a1 * Bz[1] + a2 * Bz[2] + a3 * Bz[3] + a4 * Bz[4]) % MOD3
                        mism = int(np.count_nonzero((y - m) % MOD3))
                        if best is None or mism < best["mismatches"]:
                            best = {
                                "coeff_B0_B1_B2_B3_B4_mod3": list(coeff),
                                "mismatches": mism,
                                "matches": int(90 - mism),
                            }
                            if mism == 0:
                                return best
    assert best is not None
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--scheme-bundle",
        type=Path,
        default=ROOT / "W33_nonisotropic_line_association_scheme_bundle.zip",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "W33_nonisotropic_line_scheme_spectral_bundle.zip",
    )
    ap.add_argument("--z-csv", type=Path, default=None, help="Optional 90-vector CSV (z observable)")
    ap.add_argument("--m-csv", type=Path, default=None, help="Optional 90-vector CSV (m observable)")
    args = ap.parse_args()

    bundle_path: Path = args.scheme_bundle
    if not bundle_path.exists():
        raise SystemExit(f"Missing input bundle: {bundle_path}")

    raw_npz = _read_bytes_from_zip(bundle_path, "scheme_matrices.npz")
    npz = np.load(io.BytesIO(raw_npz))

    B = [npz[f"B{i}"].astype(np.int16) for i in range(5)]
    Ameet = npz["Ameet"].astype(np.int16)
    S = npz["S"].astype(np.int16)

    # Basic consistency
    n = 90
    I = np.eye(n, dtype=np.int16)
    J = np.ones((n, n), dtype=np.int16)
    if any(b.shape != (n, n) for b in B) or Ameet.shape != (n, n) or S.shape != (n, n):
        raise SystemExit("Bad matrix shapes in scheme_matrices.npz")
    if not np.array_equal(B[4], I):
        raise SystemExit("Expected B4 == I")
    if not np.array_equal(B[1], S):
        raise SystemExit("Expected B1 == S")
    if not np.array_equal(B[2], Ameet):
        raise SystemExit("Expected B2 == Ameet")
    if not np.array_equal(S @ S, I):
        raise SystemExit("Expected S^2 == I")
    if not np.array_equal(sum(B), J):
        raise SystemExit("Expected B0+...+B4 == all-ones")

    # --- Compute primitive idempotents via Ameet eigenspaces, then split by S
    wA, vA = np.linalg.eigh(Ameet.astype(np.float64))
    groups_A = _cluster_eigenvalues_int(wA, tol=1e-6)
    expected_A = {32, 8, 2, -4}
    if set(groups_A.keys()) != expected_A:
        raise SystemExit(f"Unexpected Ameet spectrum keys: {sorted(groups_A.keys())}")

    E_by_pair: dict[tuple[int, int], np.ndarray] = {}
    mult_by_pair: dict[tuple[int, int], int] = {}
    for lamA, idxs in groups_A.items():
        V = vA[:, idxs]  # (90, mult)
        S_res = V.T @ (S.astype(np.float64) @ V)
        wS, uS = np.linalg.eigh(S_res)
        groups_S = _cluster_eigenvalues_int(wS, tol=1e-6)  # keys are ±1
        for epsS, jdxs in groups_S.items():
            if epsS not in (-1, 1):
                raise SystemExit(f"Unexpected sigma eigenvalue {epsS} on Ameet={lamA} space")
            Vc = V @ uS[:, jdxs]  # (90, mult2)
            E = Vc @ Vc.T
            mult = int(round(float(np.trace(E))))
            E_by_pair[(lamA, epsS)] = E
            mult_by_pair[(lamA, epsS)] = mult

    # Canonical order (forced by observed spectrum/splitting)
    order_pairs = [(32, 1), (8, -1), (2, 1), (-4, 1), (-4, -1)]
    if set(order_pairs) != set(E_by_pair.keys()):
        raise SystemExit(f"Unexpected idempotent pairs: got {sorted(E_by_pair.keys())}")

    E_list = [E_by_pair[pair] for pair in order_pairs]
    info_list = [
        IdempotentInfo(
            eid=f"E{j}",
            multiplicity=mult_by_pair[pair],
            lambda_ameet=pair[0],
            epsilon_sigma=pair[1],
        )
        for j, pair in enumerate(order_pairs)
    ]

    # --- Eigenmatrix P (integers)
    P_int: list[list[int]] = []
    for info, Ej in zip(info_list, E_list, strict=True):
        row = []
        m = info.multiplicity
        for Bi in B:
            lam = float(np.trace(Bi.astype(np.float64) @ Ej) / m)
            row.append(_as_int_close(lam, tol=1e-6))
        P_int.append(row)

    # --- Dual eigenmatrix Q = v * P^{-1} (exact rationals)
    v = 90
    Pinv = _invert_matrix_fraction(P_int)
    Q = [[Fraction(v, 1) * Pinv[i][j] for j in range(5)] for i in range(5)]  # (Bi row, Ej col)

    # --- Build exact coefficient representation of each Ej in the B-basis:
    #     Ej = (1/v) * sum_i Q[i][j] * B_i
    coeffs: list[dict[str, str]] = []
    E_from_coeff: list[np.ndarray] = []
    for j in range(5):
        cj: dict[str, str] = {}
        Ej = np.zeros((n, n), dtype=np.float64)
        for i in range(5):
            frac = Q[i][j] / Fraction(v, 1)
            cj[f"B{i}"] = _fraction_to_str(frac)
            Ej += (float(frac)) * B[i].astype(np.float64)
        coeffs.append(cj)
        E_from_coeff.append(Ej)

    # --- Generator identities: B0 = Ameet*S, and B3 polynomial in Ameet and S
    A = Ameet.astype(np.int64)
    S64 = S.astype(np.int64)
    AS = (A @ S64).astype(np.int64)
    A2 = (A @ A).astype(np.int64)
    gen_identities: dict[str, object] = {
        "basis_generators": ["I=B4", "S=B1", "A=Ameet=B2", "AS=A*S (=B0)", "A2=A^2"],
        "B0_equals_AS": bool(np.array_equal(B[0].astype(np.int64), AS)),
        "B3_expression_in_I_A_AS_A2": {
            "I_coeff": "-8/3",
            "S_coeff": "0",
            "A_coeff": "-13/12",
            "AS_coeff": "-3/4",
            "A2_coeff": "1/12",
        },
    }
    B3_recon = (
        (-8.0 / 3.0) * I.astype(np.float64)
        + (-13.0 / 12.0) * A.astype(np.float64)
        + (-3.0 / 4.0) * AS.astype(np.float64)
        + (1.0 / 12.0) * A2.astype(np.float64)
    )
    gen_identities["B3_expression_verifies"] = bool(np.allclose(B3_recon, B[3].astype(np.float64), atol=1e-9))

    # --- Sanity checks on idempotents (float)
    max_idem_err = 0.0
    max_orth_err = 0.0
    sumE = np.zeros((n, n), dtype=np.float64)
    for Ej in E_from_coeff:
        sumE += Ej
    max_sum_err = float(np.max(np.abs(sumE - I.astype(np.float64))))
    for a in range(5):
        Ea = E_from_coeff[a]
        max_idem_err = max(max_idem_err, float(np.max(np.abs(Ea @ Ea - Ea))))
        for b in range(5):
            if a == b:
                continue
            Eb = E_from_coeff[b]
            max_orth_err = max(max_orth_err, float(np.max(np.abs(Ea @ Eb))))

    # Reconstruction of B_i from E_j and P
    max_recon_err = 0.0
    for i in range(5):
        Bi_hat = np.zeros((n, n), dtype=np.float64)
        for j in range(5):
            Bi_hat += float(P_int[j][i]) * E_from_coeff[j]
        max_recon_err = max(max_recon_err, float(np.max(np.abs(Bi_hat - B[i].astype(np.float64)))))

    # Orthogonality P*Q = vI, Q*P = vI (exact check)
    P_frac = [[Fraction(x, 1) for x in row] for row in P_int]
    PQ = [[sum(P_frac[r][k] * Q[k][c] for k in range(5)) for c in range(5)] for r in range(5)]
    QP = [[sum(Q[r][k] * P_frac[k][c] for k in range(5)) for c in range(5)] for r in range(5)]
    pq_ok = all(PQ[r][c] == (Fraction(v, 1) if r == c else Fraction(0, 1)) for r in range(5) for c in range(5))
    qp_ok = all(QP[r][c] == (Fraction(v, 1) if r == c else Fraction(0, 1)) for r in range(5) for c in range(5))

    sanity = {
        "spectrum_Ameet": {str(k): int(len(vv)) for k, vv in sorted(groups_A.items(), key=lambda kv: -kv[0])},
        "idempotent_multiplicities": [info.multiplicity for info in info_list],
        "idempotent_pairs_(lambda_Ameet,epsilon_sigma)": [(info.lambda_ameet, info.epsilon_sigma) for info in info_list],
        "P_is_integer": True,
        "PQ_equals_vI": pq_ok,
        "QP_equals_vI": qp_ok,
        "max_idempotent_error_float": max_idem_err,
        "max_orthogonality_error_float": max_orth_err,
        "max_sumE_minus_I_error_float": max_sum_err,
        "max_reconstruct_B_from_E_error_float": max_recon_err,
    }

    # Optional m/z projection + mod-3 fit
    opt: dict[str, object] = {}
    if args.z_csv and args.m_csv:
        z = _read_90_vector_csv(args.z_csv)
        mvec = _read_90_vector_csv(args.m_csv)
        opt["inputs"] = {"z_csv": str(args.z_csv), "m_csv": str(args.m_csv)}
        opt["best_fit_mod3_in_B_basis"] = _fit_invariant_operator_mod3(B, z=z, m=mvec)

        # Real least-squares in B-basis (embed Z3 as {0,1,2} in R)
        X = np.stack([(Bi.astype(np.float64) @ z.astype(np.float64)) for Bi in B], axis=1)  # (90,5)
        y = mvec.astype(np.float64)
        coeff, residuals, rank, svals = np.linalg.lstsq(X, y, rcond=None)
        opt["least_squares_real_in_B_basis"] = {
            "coeff_B0_B1_B2_B3_B4": [float(c) for c in coeff],
            "residual_norm2": float(residuals[0]) if residuals.size else 0.0,
            "rank": int(rank),
            "singular_values": [float(x) for x in svals],
        }

        # Eigenspace projections (L2 norms) after removing trivial (constant) component
        ones = np.ones(90, dtype=np.float64)
        zf = z.astype(np.float64)
        mf = mvec.astype(np.float64)
        z0 = float(np.dot(zf, ones) / np.dot(ones, ones))
        m0 = float(np.dot(mf, ones) / np.dot(ones, ones))
        zc = zf - z0 * ones
        mc = mf - m0 * ones
        proj_rows = []
        for info, Ej in zip(info_list, E_from_coeff, strict=True):
            zj = Ej @ zc
            mj = Ej @ mc
            proj_rows.append(
                {
                    "E": info.eid,
                    "mult": info.multiplicity,
                    "lambda_Ameet": info.lambda_ameet,
                    "epsilon_sigma": info.epsilon_sigma,
                    "||proj(z)||_2": float(np.linalg.norm(zj)),
                    "||proj(m)||_2": float(np.linalg.norm(mj)),
                }
            )
        opt["centered_projections_L2"] = proj_rows

    # --- Write bundle
    out_dir = ROOT / "_out_noniso_line_scheme_spectral"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
        out_dir.rmdir()
    out_dir.mkdir()

    # P as CSV
    p_rows: list[dict[str, object]] = []
    for info, row in zip(info_list, P_int, strict=True):
        p_rows.append(
            {
                "E": info.eid,
                "multiplicity": info.multiplicity,
                "lambda_Ameet": info.lambda_ameet,
                "epsilon_sigma": info.epsilon_sigma,
                "P(B0)": row[0],
                "P(B1)": row[1],
                "P(B2)": row[2],
                "P(B3)": row[3],
                "P(B4)": row[4],
            }
        )
    _write_csv(
        out_dir / "P_eigenmatrix.csv",
        ["E", "multiplicity", "lambda_Ameet", "epsilon_sigma", "P(B0)", "P(B1)", "P(B2)", "P(B3)", "P(B4)"],
        p_rows,
    )

    # Q as CSV (fractions)
    q_rows: list[dict[str, object]] = []
    for i in range(5):
        q_rows.append(
            {
                "B": f"B{i}",
                "Q(E0)": _fraction_to_str(Q[i][0]),
                "Q(E1)": _fraction_to_str(Q[i][1]),
                "Q(E2)": _fraction_to_str(Q[i][2]),
                "Q(E3)": _fraction_to_str(Q[i][3]),
                "Q(E4)": _fraction_to_str(Q[i][4]),
            }
        )
    _write_csv(out_dir / "Q_dual_eigenmatrix.csv", ["B", "Q(E0)", "Q(E1)", "Q(E2)", "Q(E3)", "Q(E4)"], q_rows)

    _write_json(out_dir / "primitive_idempotents_coeffs.json", {"E_order": [i.eid for i in info_list], "coeffs": coeffs})
    _write_json(out_dir / "generator_identities.json", gen_identities)
    _write_json(out_dir / "sanity_checks.json", sanity)
    if opt:
        _write_json(out_dir / "optional_vector_fit_and_projections.json", opt)

    # Save float idempotent matrices
    np.savez_compressed(out_dir / "primitive_idempotents_float.npz", **{info.eid: E for info, E in zip(info_list, E_from_coeff, strict=True)})

    readme = f"""\
Non-isotropic 90-line association scheme: spectral decomposition

Input:
  - {bundle_path.name} (scheme_matrices.npz)

Adjacency basis (as in input bundle):
  - B4 = I (identity)
  - B1 = S (fixed-point-free involution; 45 disjoint transpositions)
  - B2 = Ameet (meet/intersection graph adjacency; 32-regular)
  - B0,B3 are the remaining Aut(W33) orbitals on ordered pairs

Key algebraic identities (verified):
  - B0 = Ameet * S  (so the full 5D commutant is generated by Ameet and S)
  - B3 = (-8/3) I + (-13/12) Ameet + (-3/4) (Ameet*S) + (1/12) Ameet^2

Files:
  - P_eigenmatrix.csv
      Eigenvalues P_{E,B} (integers) of each B_i on each primitive idempotent E_j.
  - Q_dual_eigenmatrix.csv
      Dual eigenmatrix entries Q_{B,E} as exact rationals.
  - primitive_idempotents_coeffs.json
      Exact expansion of each E_j in the B-basis: E_j = (1/90) * sum_i Q[i,j] * B_i.
  - primitive_idempotents_float.npz
      Float64 matrices for E0..E4 (derived from the exact coefficients).
  - generator_identities.json, sanity_checks.json

Optional:
  - If you pass --z-csv and --m-csv (90-entry CSVs indexed by line_id),
    optional_vector_fit_and_projections.json records:
      * best-fit Aut-invariant D = sum a_i B_i mapping z->m over Z3 (brute force over 243 combos)
      * real least-squares fit in the same basis
      * eigenspace projection norms after removing the constant component.
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip: Path = args.out
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    # cleanup
    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

