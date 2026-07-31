#!/usr/bin/env python3
"""Passes 1601--1605: integral Smith structure of the W33 frame matrix.

The verifier rebuilds the canonical 540 x 240 frame/edge incidence matrix M,
proves the full Smith normal form of M^T by a deterministic p-adic reduction
plus an exact Bareiss determinant witness, and then refines the existing
frame-cokernel/signed-turn bridge at the integral lattice level.

All statements are finite exact matrix/lattice identities.  The result does
not decide the still-open global nine-cover resolution problem.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis" / "w33_frame_hoffman_resolution_theorem.py"
OUT = ROOT / "data" / "w33_pass1601_1605_integral_frame_cokernel.json"


def load_base():
    spec = importlib.util.spec_from_file_location("frame_base", BASE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rank_mod(A: np.ndarray, p: int) -> int:
    B = np.array(A, dtype=np.int64) % p
    m, n = B.shape
    r = 0
    for c in range(n):
        pivots = np.flatnonzero(B[r:, c])
        if not len(pivots):
            continue
        i = r + int(pivots[0])
        if i != r:
            B[[r, i]] = B[[i, r]]
        B[r] = (B[r] * pow(int(B[r, c]), -1, p)) % p
        rows = np.flatnonzero(B[:, c])
        rows = rows[rows != r]
        for start in range(0, len(rows), 256):
            rr = rows[start : start + 256]
            B[rr] = (B[rr] - B[rr, c, None] * B[r, None, :]) % p
        r += 1
        if r == m:
            break
    return r


def padic_pivot_certificate(A: np.ndarray, p: int, levels: int = 8) -> dict[str, Any]:
    """Return exact p-adic elementary-divisor counts and a full-rank minor."""
    B = np.array(A, dtype=np.int64)
    row_ids = list(range(B.shape[0]))
    col_ids = list(range(B.shape[1]))
    selected_rows: list[int] = []
    selected_cols: list[int] = []
    counts: list[int] = []

    for level in range(levels):
        modulus = p ** (levels - level)
        B %= modulus
        m, n = B.shape
        r = 0
        while r < m and r < n:
            locations = np.argwhere((B[r:, r:] % p) != 0)
            if not len(locations):
                break
            i, j = map(int, locations[0])
            i += r
            j += r
            if i != r:
                B[[r, i], :] = B[[i, r], :]
                row_ids[r], row_ids[i] = row_ids[i], row_ids[r]
            if j != r:
                B[:, [r, j]] = B[:, [j, r]]
                col_ids[r], col_ids[j] = col_ids[j], col_ids[r]
            inverse = pow(int(B[r, r]), -1, modulus)
            B[r, r:] = (B[r, r:] * inverse) % modulus
            factors = B[r + 1 :, r].copy()
            for start in range(0, len(factors), 128):
                f = factors[start : start + 128]
                rows = slice(r + 1 + start, r + 1 + start + len(f))
                B[rows, r:] = (B[rows, r:] - f[:, None] * B[r, r:][None, :]) % modulus
            B[r, r + 1 :] = 0
            r += 1
        selected_rows.extend(row_ids[:r])
        selected_cols.extend(col_ids[:r])
        counts.append(r)
        residual = B[r:, r:]
        assert np.all(residual % p == 0)
        B = (residual // p).astype(np.int64)
        row_ids = row_ids[r:]
        col_ids = col_ids[r:]
        if not B.size:
            break

    return {
        "prime": p,
        "valuation_counts": counts,
        "selected_rows": selected_rows,
        "selected_cols": selected_cols,
        "rank": len(selected_rows),
        "residual_shape": list(B.shape),
    }


def det_bareiss(A: np.ndarray) -> int:
    a = [list(map(int, row)) for row in np.asarray(A).tolist()]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        current = a[k][k]
        for i in range(k + 1, n):
            aik = a[i][k]
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * current - aik * a[k][j]) // previous
            a[i][k] = 0
        previous = current
    return sign * a[-1][-1]


def smith_witness(A: np.ndarray, p: int, levels: int = 8) -> dict[str, Any]:
    cert = padic_pivot_certificate(A, p, levels)
    rows = cert["selected_rows"]
    cols = cert["selected_cols"]
    minor = A[np.ix_(rows, cols)]
    determinant = det_bareiss(minor)
    cert.update({
        "minor_shape": list(minor.shape),
        "minor_nnz": int(np.count_nonzero(minor)),
        "minor_determinant": determinant,
        "minor_abs_determinant": abs(determinant),
        "minor_sha256": hashlib.sha256(minor.astype(np.int16).tobytes()).hexdigest(),
        "selected_rows_sha256": hashlib.sha256(np.array(rows, dtype=np.uint16).tobytes()).hexdigest(),
        "selected_cols_sha256": hashlib.sha256(np.array(cols, dtype=np.uint16).tobytes()).hexdigest(),
    })
    return cert


def build_bridge(g: dict[str, object]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    A = np.asarray(g["point_adjacency"], dtype=np.int64)
    edges = list(g["edges"])
    N = np.zeros((40, 240), dtype=np.int64)
    d = np.zeros((40, 240), dtype=np.int64)
    for j, (a, b) in enumerate(edges):
        N[a, j] = N[b, j] = 1
        d[a, j] = -1
        d[b, j] = 1
    I = np.eye(40, dtype=np.int64)
    P = (A - 12 * I) @ (A - 2 * I)
    Cnum = N.T @ P @ N
    Fnum = d.T @ P @ N
    C = Cnum // 16
    F = Fnum // 16
    assert np.array_equal(16 * C, Cnum)
    assert np.array_equal(16 * F, Fnum)
    return N, d, C, F


def enumerate_k44_octets(g: dict[str, object]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    import itertools
    adjacency = np.asarray(g["point_adjacency"], dtype=np.int64)
    edges = list(g["edges"])
    edge_index = {tuple(e): i for i, e in enumerate(edges)}
    octets = []
    seen = set()
    for left in itertools.combinations(range(40), 4):
        if any(adjacency[a, b] for a, b in itertools.combinations(left, 2)):
            continue
        right = tuple(v for v in range(40) if all(adjacency[v, u] for u in left))
        if len(right) != 4 or any(adjacency[a, b] for a, b in itertools.combinations(right, 2)):
            continue
        key = tuple(sorted((tuple(left), tuple(right))))
        if key in seen:
            continue
        seen.add(key)
        octets.append((tuple(left), tuple(right)))
    K = np.zeros((len(octets), 240), dtype=np.int64)
    for row, (left, right) in enumerate(octets):
        for a in left:
            for b in right:
                K[row, edge_index[tuple(sorted((a, b)))]] = 1
    gram = K @ K.T
    overlap = gram.copy()
    np.fill_diagonal(overlap, 0)
    return K, (overlap == 1).astype(np.int64), np.array(octets, dtype=np.int16)


def certificate() -> dict[str, Any]:
    g = load_base().build_geometry()
    M = np.asarray(g["incidence"], dtype=np.int64)
    Amap = M.T
    m2 = smith_witness(Amap, 2, 10)
    odd_ranks = {str(p): rank_mod(Amap, p) for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31)}
    gram_rows = M @ M.T
    gram_cols = M.T @ M
    rank_M_2 = rank_mod(M, 2)
    rank_row_gram_2 = rank_mod(gram_rows, 2)
    rank_col_gram_2 = rank_mod(gram_cols, 2)
    row_hull = rank_M_2 - rank_row_gram_2
    col_hull = rank_M_2 - rank_col_gram_2
    _, _, C, F = build_bridge(g)
    K44, A45, octet_labels = enumerate_k44_octets(g)
    MK = M @ K44.T
    assert np.max(MK % 2) == 0
    J = MK // 2
    Jgram_expected = 66 * np.eye(45, dtype=np.int64) + 3 * A45 + 6 * np.ones((45, 45), dtype=np.int64)
    C2, C3 = smith_witness(C, 2, 6), smith_witness(C, 3, 6)
    F2, F3 = smith_witness(F, 2, 6), smith_witness(F, 3, 6)
    quotient_rank = rank_mod(np.hstack([M, J]), 2) - rank_M_2

    checks = {
        "frame_matrix_shape_540_240": M.shape == (540, 240),
        "frame_rows_weight_4": np.array_equal(M.sum(axis=1), np.full(540, 4)),
        "edge_columns_weight_9": np.array_equal(M.sum(axis=0), np.full(240, 9)),
        "rank_M_Q_225_via_odd_prime": odd_ranks["5"] == 225,
        "rank_M_F2_195": rank_M_2 == 195,
        "M_snf_2adic_counts_195_30": m2["valuation_counts"][:3] == [195, 30, 0],
        "M_minor_det_2pow30": m2["minor_abs_determinant"] == 2**30,
        "M_minor_rank_225": m2["rank"] == 225,
        "M_all_tested_odd_ranks_225": set(odd_ranks.values()) == {225},
        "row_code_hull_31": row_hull == 31,
        "column_code_hull_95": col_hull == 95,
        "C_annihilates_frame_rows": np.max(np.abs(M @ C)) == 0,
        "F_descends_through_frame_cokernel": np.max(np.abs(F @ M.T)) == 0,
        "C_rank_Q_15": rank_mod(C, 5) == 15,
        "F_rank_Q_15": rank_mod(F, 5) == 15,
        "C_snf_1x10_3x5": C2["valuation_counts"][:2] == [15, 0] and C3["valuation_counts"][:3] == [10, 5, 0] and C3["minor_abs_determinant"] == 3**5,
        "F_snf_1x10_3x4_6x1": F2["valuation_counts"][:3] == [14, 1, 0] and F3["valuation_counts"][:3] == [10, 5, 0] and F2["minor_abs_determinant"] == 2 * 3**5,
        "intrinsic_k44_octets_45": K44.shape == (45, 240),
        "k44_weights_16_and_3": np.array_equal(K44.sum(axis=1), np.full(45, 16)) and np.array_equal(K44.sum(axis=0), np.full(240, 3)),
        "k44_basis_of_binary_dual": rank_mod(K44, 2) == 45 and np.max((M @ K44.T) % 2) == 0,
        "half_incidence_binary": set(map(int, np.unique(J))) == {0, 1},
        "half_incidence_regular_6_72": np.array_equal(J.sum(axis=1), np.full(540, 6)) and np.array_equal(J.sum(axis=0), np.full(45, 72)),
        "half_incidence_gram_identity": np.array_equal(J.T @ J, Jgram_expected),
        "half_incidence_mod2_quotient_30": quotient_rank == 30,
        "half_incidence_kernel_15": 45 - quotient_rank == 15,
        "modular_cokernel_dimension_45": 240 - rank_M_2 == 45,
        "torsion_dimension_30": 225 - rank_M_2 == 30,
        "ambient_bridge_mod2_rank_14": rank_mod(F, 2) == 14,
        "ambient_bridge_mod3_rank_10": rank_mod(F, 3) == 10,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    if not all(checks.values()):
        raise AssertionError([k for k, v in checks.items() if not v])

    return {
        "schema": "w33.pass1601_1605.integral_frame_cokernel.v1",
        "status": "PASS",
        "passes": {
            "1601": {"title": "Integral frame-cokernel Smith theorem", "smith_normal_form_M_transpose": {"1": 195, "2": 30, "0": 15}, "cokernel": "Z^15 direct-sum (Z/2Z)^30", "minor_witness": m2, "odd_prime_rank_checks": odd_ranks},
            "1602": {"title": "K4,4 Bockstein torsion theorem", "bockstein_sequence": "0 -> ker_Z(M)/2 -> ker_F2(M) -> Tor_2(coker(M)) -> 0", "dimensions": "15 -> 45 -> 30", "geometric_domain": "the 45 intrinsic K4,4 octets, which form a basis of ker_F2(M)", "half_incidence": "beta(y) is represented by M*y_lift/2 modulo im(M)", "explicit_quotient_rank": quotient_rank, "binary_frame_code_hulls": {"edge_matching_row_code": {"length": 240, "dimension": rank_M_2, "bilinear_rank": rank_row_gram_2, "hull_dimension": row_hull}, "edge_fiber_column_code": {"length": 540, "dimension": rank_M_2, "bilinear_rank": rank_col_gram_2, "hull_dimension": col_hull}, "pure_binary_defect_dimension": 30}},
            "1603": {"title": "Half-incidence design and bridge-lattice Smith theorem", "half_incidence_design": {"shape": [540, 45], "frame_degree": 6, "octet_degree": 72, "gram_identity": "J^T J = 66 I + 3 A_45 + 6 all-ones", "gram_spectrum": {"432": 1, "72": 24, "54": 20}, "octet_overlap_graph": "SRG(45,32,22,24)"}, "C_snf": {"1": 10, "3": 5, "0": 225}, "F_snf": {"1": 10, "3": 4, "6": 1, "0": 225}, "C_minor_det": C3["minor_abs_determinant"], "F_minor_det": F2["minor_abs_determinant"], "C_2adic": C2, "C_3adic": C3, "F_2adic": F2, "F_3adic": F3},
            "1604": {"title": "Integral bridge torsion-kernel theorem", "exact_sequence": "0 -> (Z/2Z)^30 -> coker(M^T) -> im(F) -> 0", "dual_bockstein": "the same 30-torsion is geometrically presented by the K4,4 Bockstein quotient ker_F2(M)/(ker_Z(M) mod 2)", "explanation": "F M^T=0, so F descends to the cokernel. Its rational rank is 15, equal to the free rank of the cokernel; its target im(F) is free. Therefore the kernel is exactly the full torsion subgroup (Z/2)^30.", "mod2_kernel_split": {"modular_cokernel_dimension": 45, "ambient_F_rank": 14, "ambient_kernel_dimension": 31, "torsion_kernel_dimension": 30, "extra_embedding_parity_dimension": 1, "cause": "the single even Smith factor 6 in the ambient image lattice of F"}},
            "1605": {"title": "Resolution-boundary and solver guidance", "statement": "The 30-dimensional elementary two-torsion is an exact integral invariant of the frame-edge carrier. It supplies 30 purely binary parity modes, but does not by itself decide the nine-cover resolution: the all-one edge vector is already in im(M^T) because exact covers exist. Any solver use must treat these modes as certified parity preprocessing, not as an UNSAT certificate."},
        },
        "checks": checks,
        "matrix_hashes": {
            "M_int8": hashlib.sha256(M.astype(np.int8).tobytes()).hexdigest(),
            "C_int16": hashlib.sha256(C.astype(np.int16).tobytes()).hexdigest(),
            "F_int16": hashlib.sha256(F.astype(np.int16).tobytes()).hexdigest(),
            "K44_int8": hashlib.sha256(K44.astype(np.int8).tobytes()).hexdigest(),
            "J_half_incidence_int8": hashlib.sha256(J.astype(np.int8).tobytes()).hexdigest(),
            "octet_labels_int16": hashlib.sha256(octet_labels.astype(np.int16).tobytes()).hexdigest(),
        },
        "boundary": "This packet determines the complete integral cokernel and the lattice content of the 15-dimensional bridge. It does not prove SAT or UNSAT for the global nine-cover resolution, and it does not identify the 30-dimensional torsion with a specific irreducible modular module without an independent character/MeatAxe certificate.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = certificate()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != text:
            raise SystemExit("Passes 1601-1605 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(payload["checks"])}))


if __name__ == "__main__":
    main()
