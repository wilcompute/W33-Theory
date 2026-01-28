#!/usr/bin/env python3
"""Export explicit W33 edge <-> E8 root bijection as CSV/JSON.

Uses artifacts/explicit_bijection_decomposition.json and W(E6) orbit labels.
Outputs:
- artifacts/edge_root_bijection.csv
- artifacts/edge_root_bijection.json
"""

from __future__ import annotations

import csv
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33_vertices_edges():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def main():
    proj_points, edges = build_w33_vertices_edges()

    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}

    rows = []
    for eidx, (i, j) in enumerate(edges):
        if eidx not in edge_to_root_idx:
            continue
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        r_key = tuple(int(x) for x in r)
        info = root_to_orbit.get(r_key, {})

        rows.append(
            {
                "edge_index": eidx,
                "v_i": i,
                "v_j": j,
                "v_i_coords": proj_points[i],
                "v_j_coords": proj_points[j],
                "root_index": ridx,
                "root_coords": r,
                "we6_orbit_id": info.get("orbit_id"),
                "we6_orbit_size": info.get("orbit_size"),
            }
        )

    out_json = ROOT / "artifacts" / "edge_root_bijection.json"
    out_csv = ROOT / "artifacts" / "edge_root_bijection.csv"

    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {out_json}")
    print(f"Wrote {out_csv}")


if __name__ == "__main__":
    main()
