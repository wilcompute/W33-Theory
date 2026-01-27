#!/usr/bin/env python3
"""
Build the explicit operator-chain bundles referenced by the complete draft:
  - W33_current_operator_C_lineface_bundle.zip
  - W33_bulk_operator_K0K1_curved_triangle_current_bundle.zip
  - W33_curved_triangle_to_noniso_line_operator_R_bundle.zip

All operators are Z3-linear and provided in sparse COO form.

Definitions (matching the field-equation layer):
  - C_lineface : Z3^{9450 tetra} -> Z3^{90 lines}
      For boundary tetrahedra (flat_face_count=1), add J(t) to the unique attached nonisotropic line.
  - K0, K1 : Z3^{9450 tetra} -> Z3^{2880 curved triangles}
      Incidence from tetrahedra to their curved triangular faces, split by tetra orbit:
        K0 = bulk contribution (flat_face_count=0)
        K1 = boundary contribution (flat_face_count=1)
      (Vacuum tetrahedra have no curved faces.)
  - R : Z3^{2880 curved triangles} -> Z3^{90 lines}
      For each curved triangle, distribute its value along its 3 edges; each edge lies on a unique nonisotropic line.

Then the bulk shadow satisfies:
  z_line = R (K0+K1) J
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from itertools import combinations
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
MOD3 = 3


def mod3(x: int) -> int:
    return x % MOD3


def _read_csv_from_zip(zip_path: Path, inner: str) -> list[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(inner) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            return list(csv.DictReader(text))


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _zip_dir(out_zip: Path, out_dir: Path) -> None:
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(out_dir.iterdir()):
            zf.write(p, arcname=p.name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--holonomy-phase-decomp",
        type=Path,
        default=ROOT / "W33_holonomy_phase_decomposition_bundle.zip",
    )
    ap.add_argument(
        "--quotient-bundle",
        type=Path,
        default=ROOT / "W33_quotient_closure_complement_and_noniso_line_curvature_bundle.zip",
    )
    ap.add_argument(
        "--line-scheme-bundle",
        type=Path,
        default=ROOT / "W33_nonisotropic_line_association_scheme_bundle.zip",
    )
    args = ap.parse_args()

    # --- Tetrahedra and J := dF
    trows = _read_csv_from_zip(args.holonomy_phase_decomp, "tetra_coboundary_dF_dPhi_9450.csv")
    tets = [tuple(map(int, [r["a"], r["b"], r["c"], r["d"]])) for r in trows]
    J = np.array([mod3(int(r["dF"])) for r in trows], dtype=np.int16)
    if len(tets) != 9450:
        raise SystemExit(f"Expected 9450 tetrahedra, got {len(tets)}")

    # --- Lines -> flat triples and edge->line map
    lrows = _read_csv_from_zip(args.line_scheme_bundle, "nonisotropic_lines_90.csv")
    line_points: list[str] = [""] * 90
    triple_to_line: dict[tuple[int, int, int], int] = {}
    edge_to_line: dict[tuple[int, int], int] = {}
    for r in lrows:
        lid = int(r["line_id"])
        pts = tuple(sorted(int(x) for x in r["points"].split()))
        line_points[lid] = " ".join(str(x) for x in pts)
        for tri in combinations(pts, 3):
            triple_to_line[tri] = lid
        for e in combinations(pts, 2):
            ee = tuple(sorted(e))
            prev = edge_to_line.get(ee)
            if prev is not None and prev != lid:
                raise SystemExit(f"Edge {ee} lies on two lines? {prev} and {lid}")
            edge_to_line[ee] = lid
    if len(triple_to_line) != 360 or len(edge_to_line) != 540:
        raise SystemExit("Unexpected flat triple / edge counts")

    # --- Curved triangles list (2880): triangles in Q that are not flat
    tri_rows = _read_csv_from_zip(args.quotient_bundle, "quotient_triangles_holonomy_3240.csv")
    curved: list[tuple[int, int, int]] = []
    tri_meta: dict[tuple[int, int, int], dict[str, str]] = {}
    for r in tri_rows:
        tri = tuple(map(int, [r["p"], r["q"], r["r"]]))
        tri_meta[tri] = r
        if tri not in triple_to_line:
            curved.append(tri)
    curved.sort()
    if len(curved) != 2880:
        raise SystemExit(f"Expected 2880 curved triangles, got {len(curved)}")
    curved_index = {tri: i for i, tri in enumerate(curved)}

    def faces_of_tet(a: int, b: int, c: int, d: int) -> list[tuple[int, int, int]]:
        return [(b, c, d), (a, c, d), (a, b, d), (a, b, c)]

    # --- Build C_lineface, K0, K1
    C_rows: list[dict[str, int]] = []
    K0_rows: list[dict[str, int]] = []
    K1_rows: list[dict[str, int]] = []

    m_raw = np.zeros(90, dtype=np.int16)
    y_curved = np.zeros(2880, dtype=np.int16)

    for ti, (a, b, c, d) in enumerate(tets):
        faces = faces_of_tet(a, b, c, d)
        flat_lids = [triple_to_line.get(tri) for tri in faces if tri in triple_to_line]
        flat_count = len(flat_lids)
        if flat_count == 1:
            lid = int(flat_lids[0])
            C_rows.append({"row_line_id": lid, "col_tet_index": ti, "value_mod3": 1})
            jv = int(J[ti])
            if jv:
                m_raw[lid] = mod3(int(m_raw[lid]) + jv)
        elif flat_count not in (0, 4):
            raise SystemExit(f"Unexpected flat_face_count={flat_count} at tet_index={ti}")

        for tri in faces:
            if tri in triple_to_line:
                continue
            rid = curved_index.get(tri)
            if rid is None:
                raise SystemExit(f"Curved face {tri} not in curved list")
            if flat_count == 0:
                K0_rows.append({"row_curved_tri": rid, "col_tet_index": ti, "value_mod3": 1})
            elif flat_count == 1:
                K1_rows.append({"row_curved_tri": rid, "col_tet_index": ti, "value_mod3": 1})
            # vacuum (flat_count==4) has no curved faces
            jv = int(J[ti])
            if jv:
                y_curved[rid] = mod3(int(y_curved[rid]) + jv)

    # m augmentation (sum=0 gauge)
    m_sum = int(np.sum(m_raw) % MOD3)
    m_aug = m_raw.copy()
    if m_sum:
        m_aug[0] = mod3(int(m_aug[0]) - m_sum)

    # --- Build R and z := R y
    R_rows: list[dict[str, int]] = []
    z_line = np.zeros(90, dtype=np.int16)
    for rid, (p, q, r) in enumerate(curved):
        edges = [(p, q), (p, r), (q, r)]
        for u, v in edges:
            ee = (u, v) if u < v else (v, u)
            lid = edge_to_line.get(ee)
            if lid is None:
                raise SystemExit(f"Edge {ee} missing from edge_to_line")
            R_rows.append({"row_line_id": int(lid), "col_curved_tri": rid, "value_mod3": 1})
            yv = int(y_curved[rid])
            if yv:
                z_line[int(lid)] = mod3(int(z_line[int(lid)]) + yv)

    if int(np.sum(z_line) % MOD3) != 0:
        raise SystemExit("Expected z_line in augmentation (sum=0)")

    # --- Emit bundles
    # 1) C_lineface bundle
    out1 = ROOT / "_out_C_lineface"
    out1.mkdir(exist_ok=True)
    for p in out1.iterdir():
        p.unlink()
    _write_csv(out1 / "operator_C_lineface_coo.csv", ["row_line_id", "col_tet_index", "value_mod3"], C_rows)
    _write_csv(
        out1 / "m_line_from_C_lineface_J.csv",
        ["line_id", "points", "m_raw_mod3", "m_aug_mod3"],
        [{"line_id": i, "points": line_points[i], "m_raw_mod3": int(m_raw[i]), "m_aug_mod3": int(m_aug[i])} for i in range(90)],
    )
    _write_json(
        out1 / "summary.json",
        {
            "shape": {"rows_lines": 90, "cols_tetra": 9450},
            "nnz": len(C_rows),
            "m_raw_sum_mod3": int(np.sum(m_raw) % MOD3),
            "m_aug_sum_mod3": int(np.sum(m_aug) % MOD3),
        },
    )
    (out1 / "README.txt").write_text(
        "C_lineface operator (COO) and resulting m_line = C_lineface * J (plus sum=0 gauge-fix).\n",
        encoding="utf-8",
    )
    _zip_dir(ROOT / "W33_current_operator_C_lineface_bundle.zip", out1)
    for p in out1.iterdir():
        p.unlink()
    out1.rmdir()

    # 2) K0K1 bundle
    out2 = ROOT / "_out_K0K1"
    out2.mkdir(exist_ok=True)
    for p in out2.iterdir():
        p.unlink()
    _write_csv(
        out2 / "curved_triangles_2880.csv",
        ["curved_tri_id", "p", "q", "r", "holonomy_type"],
        [
            {
                "curved_tri_id": i,
                "p": tri[0],
                "q": tri[1],
                "r": tri[2],
                "holonomy_type": tri_meta[tri]["holonomy_type"],
            }
            for i, tri in enumerate(curved)
        ],
    )
    _write_csv(out2 / "operator_K0_coo.csv", ["row_curved_tri", "col_tet_index", "value_mod3"], K0_rows)
    _write_csv(out2 / "operator_K1_coo.csv", ["row_curved_tri", "col_tet_index", "value_mod3"], K1_rows)
    _write_csv(
        out2 / "y_curved_triangle_current_from_J.csv",
        ["curved_tri_id", "y_mod3"],
        [{"curved_tri_id": i, "y_mod3": int(y_curved[i])} for i in range(2880)],
    )
    _write_json(
        out2 / "summary.json",
        {
            "shape": {"rows_curved_triangles": 2880, "cols_tetra": 9450},
            "nnz": {"K0": len(K0_rows), "K1": len(K1_rows), "K0_plus_K1": len(K0_rows) + len(K1_rows)},
            "y_hist": {
                str(int(val)): int(cnt)
                for val, cnt in zip(*np.unique(y_curved, return_counts=True), strict=True)
            },
        },
    )
    (out2 / "README.txt").write_text(
        "K0/K1 operators (COO) mapping tetra flux J to curved-triangle current y on the 2880 curved triangles.\n",
        encoding="utf-8",
    )
    _zip_dir(ROOT / "W33_bulk_operator_K0K1_curved_triangle_current_bundle.zip", out2)
    for p in out2.iterdir():
        p.unlink()
    out2.rmdir()

    # 3) R bundle
    out3 = ROOT / "_out_R"
    out3.mkdir(exist_ok=True)
    for p in out3.iterdir():
        p.unlink()
    _write_csv(out3 / "operator_R_coo.csv", ["row_line_id", "col_curved_tri", "value_mod3"], R_rows)
    _write_csv(
        out3 / "z_line_from_R_y.csv",
        ["line_id", "points", "z_mod3"],
        [{"line_id": i, "points": line_points[i], "z_mod3": int(z_line[i])} for i in range(90)],
    )
    _write_json(out3 / "summary.json", {"shape": {"rows_lines": 90, "cols_curved_triangles": 2880}, "nnz": len(R_rows)})
    (out3 / "README.txt").write_text(
        "R operator (COO) mapping curved-triangle current y to 90-line aggregates via edge incidence.\n",
        encoding="utf-8",
    )
    _zip_dir(ROOT / "W33_curved_triangle_to_noniso_line_operator_R_bundle.zip", out3)
    for p in out3.iterdir():
        p.unlink()
    out3.rmdir()

    print("Wrote bundles:")
    print(" - W33_current_operator_C_lineface_bundle.zip")
    print(" - W33_bulk_operator_K0K1_curved_triangle_current_bundle.zip")
    print(" - W33_curved_triangle_to_noniso_line_operator_R_bundle.zip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
