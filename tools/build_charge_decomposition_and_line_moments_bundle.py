#!/usr/bin/env python3
"""
Summarize the tetrahedra flux/charge cochain J := dF on the quotient Q and its
attachments to the 90 non-isotropic lines ("vacuum cells").

Produces:
  - W33_charge_decomposition_and_line_moments_bundle.zip

This bundle is complementary to:
  - W33_minimal_Z3_flux_cycles_tetrahedra_bundle.zip (nonzero list + examples)
  - W33_transfer_operators_J_to_lines_and_mode_injection_bundle.zip (explicit operators M,Z)
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter
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


def _read_json_from_zip(zip_path: Path, inner: str) -> object:
    with zipfile.ZipFile(zip_path) as zf:
        return json.loads(zf.read(inner).decode("utf-8"))


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--holonomy-phase-decomp",
        type=Path,
        default=ROOT / "W33_holonomy_phase_decomposition_bundle.zip",
    )
    ap.add_argument(
        "--line-scheme-bundle",
        type=Path,
        default=ROOT / "W33_nonisotropic_line_association_scheme_bundle.zip",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "W33_charge_decomposition_and_line_moments_bundle.zip",
    )
    args = ap.parse_args()

    # Tetrahedra + J
    trows = _read_csv_from_zip(args.holonomy_phase_decomp, "tetra_coboundary_dF_dPhi_9450.csv")
    tets = [tuple(map(int, [r["a"], r["b"], r["c"], r["d"]])) for r in trows]
    J = np.array([mod3(int(r["dF"])) for r in trows], dtype=np.int16)
    if len(tets) != 9450:
        raise SystemExit(f"Expected 9450 tetrahedra, got {len(tets)}")

    # Lines -> flat triples and edge->line mapping
    lrows = _read_csv_from_zip(args.line_scheme_bundle, "nonisotropic_lines_90.csv")
    triple_to_line: dict[tuple[int, int, int], int] = {}
    for r in lrows:
        lid = int(r["line_id"])
        pts = tuple(sorted(int(x) for x in r["points"].split()))
        for tri in combinations(pts, 3):
            triple_to_line[tri] = lid
    if len(triple_to_line) != 360:
        raise SystemExit(f"Expected 360 flat triples, got {len(triple_to_line)}")

    def faces_of_tet(a: int, b: int, c: int, d: int) -> list[tuple[int, int, int]]:
        return [(b, c, d), (a, c, d), (a, b, d), (a, b, c)]

    flat_face_count = np.zeros(len(tets), dtype=np.int16)
    attached_line = np.full(len(tets), -1, dtype=np.int32)

    for ti, (a, b, c, d) in enumerate(tets):
        faces = faces_of_tet(a, b, c, d)
        flat = [triple_to_line.get(tri) for tri in faces if tri in triple_to_line]
        flat_face_count[ti] = len(flat)
        if len(flat) == 1:
            attached_line[ti] = int(flat[0])
        elif len(flat) not in (0, 4):
            raise SystemExit(f"Unexpected flat_face_count={len(flat)} at tet_index={ti}")

    # Orbit label by flat-face count (purely geometric here)
    orbit_name = {0: "bulk_flat0", 1: "boundary_flat1", 4: "vacuum_line4"}
    orbit = np.array([int(fc) for fc in flat_face_count], dtype=np.int16)

    # Summary stats
    J_hist = Counter(int(x) for x in J.tolist())
    fc_hist = Counter(int(x) for x in flat_face_count.tolist())

    charged_idx = np.nonzero(J != 0)[0].tolist()
    charged_rows = []
    for ti in charged_idx:
        a, b, c, d = tets[ti]
        charged_rows.append(
            {
                "tet_index": ti,
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "J_dF_mod3": int(J[ti]),
                "flat_face_count": int(flat_face_count[ti]),
                "orbit_name": orbit_name[int(flat_face_count[ti])],
                "attached_line_id_if_boundary": int(attached_line[ti]),
            }
        )

    # Pointwise incidence of charge (sum of J over tetrahedra containing p)
    point_charge = np.zeros(40, dtype=np.int16)
    for ti in charged_idx:
        jv = int(J[ti])
        for p in tets[ti]:
            point_charge[p] = mod3(int(point_charge[p]) + jv)

    # Line attachment moment (boundary only): m_raw[lid] = sum J over boundary tetrahedra attached to lid
    m_raw = np.zeros(90, dtype=np.int16)
    for ti in charged_idx:
        if int(flat_face_count[ti]) != 1:
            continue
        lid = int(attached_line[ti])
        m_raw[lid] = mod3(int(m_raw[lid]) + int(J[ti]))

    m_sum = int(np.sum(m_raw) % MOD3)
    m_aug = m_raw.copy()
    if m_sum:
        m_aug[0] = mod3(int(m_aug[0]) - m_sum)

    # Per-orbit/per-flux counts
    class_counts = Counter()
    for ti in charged_idx:
        class_counts[(int(flat_face_count[ti]), int(J[ti]))] += 1

    # Write bundle
    out_dir = ROOT / "_out_charge_decomp"
    if out_dir.exists():
        for p in out_dir.iterdir():
            p.unlink()
        out_dir.rmdir()
    out_dir.mkdir()

    _write_csv(
        out_dir / "charged_tetrahedra_3008.csv",
        ["tet_index", "a", "b", "c", "d", "J_dF_mod3", "flat_face_count", "orbit_name", "attached_line_id_if_boundary"],
        charged_rows,
    )

    point_rows = [{"point_id": p, "charge_sum_mod3": int(point_charge[p])} for p in range(40)]
    _write_csv(out_dir / "point_charge_incidence_40.csv", ["point_id", "charge_sum_mod3"], point_rows)

    line_rows = [{"line_id": lid, "m_raw_mod3": int(m_raw[lid]), "m_aug_mod3": int(m_aug[lid])} for lid in range(90)]
    _write_csv(out_dir / "boundary_line_moment_m_90.csv", ["line_id", "m_raw_mod3", "m_aug_mod3"], line_rows)

    _write_json(
        out_dir / "summary.json",
        {
            "inputs": {
                "holonomy_phase_decomp": args.holonomy_phase_decomp.name,
                "line_scheme_bundle": args.line_scheme_bundle.name,
            },
            "counts": {
                "num_tetrahedra": len(tets),
                "J_hist": {str(k): int(v) for k, v in sorted(J_hist.items())},
                "flat_face_count_hist": {str(k): int(v) for k, v in sorted(fc_hist.items())},
                "charged_nonzero": int(len(charged_idx)),
                "charged_by_(flat_face_count,J)": {f"{fc},{j}": int(v) for (fc, j), v in sorted(class_counts.items())},
            },
            "notes": {
                "vacuum_line_tetrahedra_are_flux_free": bool(np.all(J[flat_face_count == 4] == 0)),
                "m_aug_is_sum0_gauge_fix": True,
            },
        },
    )

    readme = """\
Charge decomposition and line moments

This bundle records the nonzero support of J := dF on the 9450 quotient tetrahedra, and summarizes:
  - how charged tetrahedra split by flat-face-count orbit type (bulk/boundary/vacuum)
  - boundary attachments to the 90 non-isotropic lines (line moments)
  - pointwise charge incidence on the 40 quotient vertices

Files:
  - charged_tetrahedra_3008.csv
  - point_charge_incidence_40.csv
  - boundary_line_moment_m_90.csv
  - summary.json
"""
    (out_dir / "README.txt").write_text(readme, encoding="utf-8")

    out_zip: Path = args.out
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
