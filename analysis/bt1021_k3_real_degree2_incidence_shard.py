#!/usr/bin/env python3
"""BT1021: real K3 level-2 degree-2 incidence shard.

This shard reuses the accepted BT998 edgewise subdivision helpers, but feeds them
K3_16 facets.  It builds the actual level-2 K3 face sets and emits a bounded
window of real degree-2 boundary rows: rows are edges, columns are triangles,
and each triangle contributes to its three edge rows.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "exploration"))

from bt1015_f2_bitset_rank_core import rank_mod2_integer_rows, row_weight  # noqa: E402
from bt998_cp2_level2_edgewise_rank_pipeline import edgewise_subdivide, faces_by_dim, relabel_initial  # noqa: E402
from w33_explicit_curved_4d_complexes import k3_facets  # noqa: E402

EXPECTED = {
    "rows": 45120,
    "cols": 152960,
    "nnz": 458880,
    "row_weight_min": 1,
    "target_rank": 42345,
}


def k3_level2_faces():
    top = relabel_initial(k3_facets())
    top = edgewise_subdivide(top)
    top = edgewise_subdivide(top)
    return faces_by_dim(top)


def degree2_real_rows(start: int, count: int):
    faces = k3_level2_faces()
    edges = faces[1]
    triangles = faces[2]
    edge_index = {e: i for i, e in enumerate(edges)}
    selected = list(range(start, min(start + count, len(edges))))
    selected_set = set(selected)
    rows = {i: 0 for i in selected}
    for col, tri in enumerate(triangles):
        for e in combinations(tri, 2):
            idx = edge_index[tuple(sorted(e))]
            if idx in selected_set:
                rows[idx] ^= 1 << col
    return [rows[i] for i in selected], [len(x) for x in faces]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=64)
    args = parser.parse_args()
    rows, f_vector = degree2_real_rows(args.start, args.count)
    out = {
        "theorem": "BT1021 real K3 level-2 degree-2 incidence shard",
        "map": "degree_2",
        "expected_contract": EXPECTED,
        "f_vector": f_vector,
        "window": {"start": args.start, "count": len(rows)},
        "row_weight_minmax": [min(row_weight(r) for r in rows), max(row_weight(r) for r in rows)] if rows else [0, 0],
        "window_rank": rank_mod2_integer_rows(rows),
        "real_incidence": True,
        "status": "bounded real edge-triangle incidence shard generated from the actual K3 level-2 edgewise complex",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1021_k3_real_degree2_incidence_shard.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
