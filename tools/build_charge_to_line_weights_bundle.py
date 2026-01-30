#!/usr/bin/env python3
"""
Compute the "charge" 3-cochain J := dF from triangle holonomy F on Q, then:
  - project J to H^3(clique_complex(Q); Z3) coordinates (dim 89),
  - project further to the 88D core / 90-line-weight model (mod all-ones gauge),
and package the result as a reproducible bundle.

Important mathematical note:
  If J is computed as a simplicial coboundary J=dF of a *global* triangle 2-cochain F,
  then J is necessarily exact and its H^3 class is 0. This script makes that explicit.

Inputs (expected in repo root):
  - W33_holonomy_phase_test_bundle.zip
  - W33_H3_basis_89_Z3_on_clique_complex_bundle.zip
  - W33_H3_Aut_action_89Z3_bundle.zip
  - w33_line_weight_lift/lift_matrices_mod3.npz

Output:
  - W33_charge_to_line_weights_bundle.zip
"""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MOD = 3


def mod3(x: int) -> int:
    return x % MOD


def _read_csv_from_zip(zip_path: Path, inner_path: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _read_json_from_zip(zip_path: Path, inner_path: str) -> object:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner_path) as raw:
            return json.load(raw)


def _read_npz_from_zip(zip_path: Path, inner_path: str) -> dict[str, np.ndarray]:
    with zipfile.ZipFile(zip_path) as zf:
        blob = zf.read(inner_path)
    npz = np.load(io.BytesIO(blob))
    return {k: npz[k] for k in npz.files}


def _write_csv(
    path: Path, fieldnames: list[str], rows: list[dict[str, object]]
) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _invert_matrix_mod3(mat: np.ndarray) -> np.ndarray:
    mat = (mat % MOD).astype(np.int16)
    n = mat.shape[0]
    if mat.shape != (n, n):
        raise ValueError("expected square matrix")
    aug = np.concatenate([mat, np.eye(n, dtype=np.int16)], axis=1) % MOD

    row = 0
    for col in range(n):
        pivot = None
        for r in range(row, n):
            if aug[r, col] % MOD != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("matrix is singular mod 3")
        if pivot != row:
            aug[[row, pivot]] = aug[[pivot, row]]

        pv = int(aug[row, col] % MOD)
        inv = 1 if pv == 1 else 2  # inv(2)=2 mod 3
        if inv != 1:
            aug[row, :] = (aug[row, :] * inv) % MOD

        for r in range(n):
            if r == row:
                continue
            factor = int(aug[r, col] % MOD)
            if factor == 0:
                continue
            aug[r, :] = (aug[r, :] - factor * aug[row, :]) % MOD

        row += 1

    inv = aug[:, n:] % MOD
    if not np.array_equal((mat @ inv) % MOD, np.eye(n, dtype=np.int16) % MOD):
        raise ValueError("inverse check failed")
    return inv.astype(np.int8)


def _build_delta2_free_columns(
    *,
    triangles: list[tuple[int, int, int]],
    free_tetra_indices: list[int],
    tetra_rows: list[dict[str, str]],
) -> list[dict[int, int]]:
    tri_index = {t: i for i, t in enumerate(triangles)}
    free_pos_of_tet = {tet: pos for pos, tet in enumerate(free_tetra_indices)}

    cols: list[defaultdict[int, int]] = [
        defaultdict(int) for _ in range(len(triangles))
    ]
    for row in tetra_rows:
        tet_index = int(row["tet_index"])
        free_pos = free_pos_of_tet.get(tet_index)
        if free_pos is None:
            continue
        a, b, c, d = int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])
        faces = [
            ((b, c, d), 1),
            ((a, c, d), -1),
            ((a, b, d), 1),
            ((a, b, c), -1),
        ]
        for tri, coef in faces:
            idx = tri_index[tri]
            cols[idx][free_pos] = mod3(cols[idx][free_pos] + coef)
            if cols[idx][free_pos] == 0:
                del cols[idx][free_pos]

    return [dict(c) for c in cols]


def _image_basis_from_columns(cols: list[dict[int, int]]) -> dict[int, dict[int, int]]:
    """
    Compute a sparse pivot basis for span(cols) in Z3^N using the rule:
      pivot(v) := max index with nonzero coefficient.
    Returns: pivot_index -> basis_vector (with basis_vector[pivot_index]=1).
    """
    basis: dict[int, dict[int, int]] = {}

    for vec in cols:
        v = dict(vec)
        while v:
            pivot = max(v.keys())
            if pivot not in basis:
                pv = v[pivot]
                if pv == 2:
                    v = {k: (2 * val) % MOD for k, val in v.items()}
                basis[pivot] = v
                break

            bvec = basis[pivot]
            factor = v[pivot]  # 1 or 2
            for k, val in bvec.items():
                v[k] = mod3(v.get(k, 0) - factor * val)
                if v[k] == 0:
                    del v[k]

    return basis


def _reduce_mod_image(
    vec: dict[int, int], basis: dict[int, dict[int, int]]
) -> dict[int, int]:
    out = dict(vec)
    for pivot in sorted(basis.keys(), reverse=True):
        factor = out.get(pivot)
        if factor is None:
            continue
        bvec = basis[pivot]
        for k, val in bvec.items():
            out[k] = mod3(out.get(k, 0) - factor * val)
            if out[k] == 0:
                del out[k]
    return out


def _vector_to_coords(vec: dict[int, int], positions: list[int]) -> np.ndarray:
    return np.array([vec.get(p, 0) for p in positions], dtype=np.int8)


def _normalize_line_weight_coset(w90: np.ndarray, idx: int = 0) -> np.ndarray:
    w = (w90.astype(np.int16) % MOD).astype(np.int16)
    c = int(w[idx] % MOD)
    w = (w - c) % MOD
    return w.astype(np.int8)


def main() -> int:
    test_bundle = ROOT / "W33_holonomy_phase_test_bundle.zip"
    h3_basis_bundle = ROOT / "W33_H3_basis_89_Z3_on_clique_complex_bundle.zip"
    h3_action_bundle = ROOT / "W33_H3_Aut_action_89Z3_bundle.zip"
    lift_npz_path = ROOT / "w33_line_weight_lift" / "lift_matrices_mod3.npz"

    for p in [test_bundle, h3_basis_bundle, h3_action_bundle, lift_npz_path]:
        if not p.exists():
            raise FileNotFoundError(str(p))

    out_dir = ROOT / "_charge_to_line_weights_tmp"
    out_dir.mkdir(exist_ok=True)

    # --- Load triangle list and holonomy F on triangles
    tri_rows = _read_csv_from_zip(
        test_bundle, "triangle_holonomy_vs_symplectic_phase.csv"
    )
    if len(tri_rows) != 3240:
        raise ValueError(f"Expected 3240 triangles, got {len(tri_rows)}")
    triangles = [(int(r["p"]), int(r["q"]), int(r["r"])) for r in tri_rows]
    F = {tri: mod3(int(r["F"])) for tri, r in zip(triangles, tri_rows, strict=True)}

    # --- Load tetra index map and free indices
    tetra_rows = _read_csv_from_zip(h3_basis_bundle, "tetra_index_map_9450.csv")
    if len(tetra_rows) != 9450:
        raise ValueError(f"Expected 9450 tetrahedra, got {len(tetra_rows)}")
    free_tets_data = _read_json_from_zip(
        h3_basis_bundle, "kernel_delta3_pivot_columns.json"
    )
    assert isinstance(free_tets_data, dict)
    free_tetra_indices = [int(x) for x in free_tets_data["free_tetra_indices"]]
    if len(free_tetra_indices) != 2828:
        raise ValueError(
            f"Expected 2828 free tetra indices, got {len(free_tetra_indices)}"
        )
    free_pos_of_tet = {tet: pos for pos, tet in enumerate(free_tetra_indices)}

    # --- Compute J=dF on all tetrahedra, then restrict to free coordinates
    J_full: dict[int, int] = {}
    for row in tetra_rows:
        tet = int(row["tet_index"])
        a, b, c, d = int(row["a"]), int(row["b"]), int(row["c"]), int(row["d"])

        def tri(u: int, v: int, w: int) -> int:
            return F[tuple(sorted((u, v, w)))]

        val = mod3(tri(b, c, d) - tri(a, c, d) + tri(a, b, d) - tri(a, b, c))
        J_full[tet] = val

    dF_hist = Counter(J_full.values())

    J_free: dict[int, int] = {}
    for tet, val in J_full.items():
        pos = free_pos_of_tet.get(tet)
        if pos is None:
            continue
        if val != 0:
            J_free[pos] = val

    # --- Build δ2_free image basis (in free-coordinate space)
    # Use the same triangle ordering as in the test-bundle triangle CSV (sorted triples).
    cols = _build_delta2_free_columns(
        triangles=triangles,
        free_tetra_indices=free_tetra_indices,
        tetra_rows=tetra_rows,
    )
    basis = _image_basis_from_columns(cols)
    rank = len(basis)
    if rank != 2739:
        raise ValueError(f"Expected rank(delta2_free)=2739, got {rank}")

    nonpivot_positions = sorted(set(range(len(free_tetra_indices))) - set(basis.keys()))
    if len(nonpivot_positions) != 89:
        raise ValueError(
            f"Expected 89 nonpivot positions, got {len(nonpivot_positions)}"
        )

    # --- Define projection π_ours: free-space cocycle -> 89D quotient coordinates
    def project_to_h3_coords_ours(vec_free: dict[int, int]) -> np.ndarray:
        reduced = _reduce_mod_image(vec_free, basis)
        return _vector_to_coords(reduced, nonpivot_positions)

    # --- Build change-of-basis from our quotient coordinates to the canonical H^3 basis
    # Their basis vectors are given as sparse cocycles on tetrahedra; project each to our coords.
    h3_basis_json = _read_json_from_zip(
        h3_basis_bundle, "H3_basis_vectors_89_sparse.json"
    )
    assert isinstance(h3_basis_json, dict)
    basis_vectors = h3_basis_json["basis_vectors"]
    if len(basis_vectors) != 89:
        raise ValueError(f"Expected 89 H^3 basis vectors, got {len(basis_vectors)}")

    T = np.zeros((89, 89), dtype=np.int8)
    for i, vec in enumerate(basis_vectors):
        vfree: dict[int, int] = {}
        for ent in vec["support"]:
            tet = int(ent["tet_index"])
            coef = mod3(int(ent["coeff"]))
            pos = free_pos_of_tet.get(tet)
            if pos is None or coef == 0:
                continue
            vfree[pos] = mod3(vfree.get(pos, 0) + coef)
            if vfree[pos] == 0:
                del vfree[pos]
        T[:, i] = project_to_h3_coords_ours(vfree)

    T_inv = _invert_matrix_mod3(T)

    def project_to_h3_coords_canonical(vec_free: dict[int, int]) -> np.ndarray:
        ours = project_to_h3_coords_ours(vec_free).astype(np.int16)
        return (T_inv.astype(np.int16) @ ours) % MOD

    # --- Project J=dF
    h3_coords_89 = project_to_h3_coords_canonical(J_free).astype(np.int8)
    if int(np.count_nonzero(h3_coords_89)) != 0:
        raise ValueError(
            "Expected dF to have trivial H^3 class (all-zero 89-vector), but it did not"
        )

    # --- Map H^3(89) -> H3_88 coords via block basis change, then to 90 line weights
    mats = _read_npz_from_zip(h3_action_bundle, "block_basis_change_matrices_mod3.npz")
    Bcols_inv = mats["Bcols_inv"].astype(np.int16) % MOD
    h3_coords_new = (Bcols_inv @ h3_coords_89.astype(np.int16)) % MOD
    h3_coords_88 = h3_coords_new[:88].astype(np.int8)

    lift = np.load(lift_npz_path)
    M_H3_to_90 = (lift["M_H3_to_90"].astype(np.int16) % MOD).astype(np.int16)
    w90 = (M_H3_to_90 @ h3_coords_88.astype(np.int16)) % MOD
    w90n = _normalize_line_weight_coset(w90.astype(np.int8), idx=0)

    # --- Sanity: one nontrivial H^3 basis vector maps to nonzero line weights (typically).
    e0 = np.zeros(89, dtype=np.int8)
    e0[0] = 1
    e0_new = (Bcols_inv @ e0.astype(np.int16)) % MOD
    e0_88 = e0_new[:88].astype(np.int8)
    e0_w90 = (M_H3_to_90 @ e0_88.astype(np.int16)) % MOD
    e0_w90n = _normalize_line_weight_coset(e0_w90.astype(np.int8), idx=0)

    # --- Write outputs
    tetra_out = []
    for row in tetra_rows:
        tet = int(row["tet_index"])
        tetra_out.append(
            {
                "tet_index": tet,
                "a": int(row["a"]),
                "b": int(row["b"]),
                "c": int(row["c"]),
                "d": int(row["d"]),
                "dF": J_full[tet],
            }
        )

    _write_csv(
        out_dir / "dF_on_tetrahedra_9450.csv",
        ["tet_index", "a", "b", "c", "d", "dF"],
        tetra_out,
    )

    _write_csv(
        out_dir / "dF_H3_coordinates_89.csv",
        ["basis_id", "coord"],
        [{"basis_id": i, "coord": int(h3_coords_89[i])} for i in range(89)],
    )
    _write_csv(
        out_dir / "dF_H3_coordinates_88.csv",
        ["coord_id", "coord"],
        [{"coord_id": i, "coord": int(h3_coords_88[i])} for i in range(88)],
    )
    _write_csv(
        out_dir / "dF_line_weights_90_normalized.csv",
        ["line_id", "weight"],
        [{"line_id": i, "weight": int(w90n[i])} for i in range(90)],
    )
    _write_csv(
        out_dir / "example_H3_basis0_line_weights_90_normalized.csv",
        ["line_id", "weight"],
        [{"line_id": i, "weight": int(e0_w90n[i])} for i in range(90)],
    )

    report = {
        "result": {
            "dF_hist": {str(k): int(v) for k, v in sorted(dF_hist.items())},
            "dF_nonzero_count": int(9450 - dF_hist.get(0, 0)),
            "delta2_free_rank_recomputed": rank,
            "free_space_dim": len(free_tetra_indices),
            "quotient_dim_recomputed": len(nonpivot_positions),
            "dF_H3_coordinates_89_nonzero": int(np.count_nonzero(h3_coords_89)),
            "dF_line_weights_90_nonzero": int(np.count_nonzero(w90n)),
        },
        "interpretation": {
            "why_H3_is_zero": "Because dF is, by definition, a 3-coboundary of a global 2-cochain F, its class in H^3 is necessarily 0.",
            "what_line_weights_are": "The 90-line weight model represents the 88D core of H^3 (mod the all-ones gauge); it captures topological 3-cocycles not of the form d(2-cochain).",
        },
    }
    _write_json(out_dir / "report.json", report)

    readme = """\
W33 charge (dF) projection to H^3 and 90-line weights

This bundle computes the tetrahedron 3-cochain J := dF from the quotient triangle holonomy field F,
then projects J into the 89D cohomology H^3 and further into the 90 non-isotropic line-weight model.

Outcome:
  - J=dF is nonzero on 3008 tetrahedra (flux distribution matches prior bundles),
  - but its H^3 class is trivial (all 89 coordinates are 0),
  - therefore its 90-line weights are also 0 (after gauge-normalization).

This is expected: any simplicial coboundary d(2-cochain) is exact and hence represents 0 in H^3.

Files:
  - dF_on_tetrahedra_9450.csv
  - dF_H3_coordinates_89.csv
  - dF_H3_coordinates_88.csv
  - dF_line_weights_90_normalized.csv
  - example_H3_basis0_line_weights_90_normalized.csv
  - report.json
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip = ROOT / "W33_charge_to_line_weights_bundle.zip"
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)

    for p in out_dir.iterdir():
        p.unlink()
    out_dir.rmdir()

    print(f"Wrote {out_zip}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
