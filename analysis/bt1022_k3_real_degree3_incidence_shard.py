#!/usr/bin/env python3
"""BT1022: real K3 level-2 degree-3 incidence shard.

Rows are triangles, columns are tetrahedra, and each tetrahedron contributes to
its four triangle rows.  The script reuses the accepted BT998 subdivision helpers
and emits a bounded real-incidence window for the third boundary map.
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

ROWS = 152960
COLS = 184320
NNZ = 737280
TARGET_RANK = 110593


def k3_level2_faces():
    top = relabel_initial(k3_facets())
    top = edgewise_subdivide(top)
    top = edgewise_subdivide(top)
    return faces_by_dim(top)


def degree3_real_rows(start: int, count: int):
    faces = k3_level2_faces()
    triangles = faces[2]
    tetrahedra = faces[3]
    triangle_index = {t: i for i, t in enumerate(triangles)}
    selected = list(range(start, min(start + count, len(triangles))))
    selected_set = set(selected)
    rows = {i: 0 for i in selected}
    for col, tet in enumerate(tetrahedra):
        for tri in combinations(tet, 3):
            idx = triangle_index[tuple(sorted(tri))]
            if idx in selected_set:
                rows[idx] ^= 1 << col
    return [rows[i] for i in selected], [len(x) for x in faces]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=64)
    args = parser.parse_args()
    rows, f_vector = degree3_real_rows(args.start, args.count)
    out = {
        "theorem": "BT1022 real K3 level-2 degree-3 incidence shard",
        "map": "degree_3",
        "shape": [ROWS, COLS],
        "global_nnz": NNZ,
        "target_rank": TARGET_RANK,
        "f_vector": f_vector,
        "window": {"start": args.start, "count": len(rows)},
        "row_weight_minmax": [min(row_weight(r) for r in rows), max(row_weight(r) for r in rows)] if rows else [0, 0],
        "window_rank": rank_mod2_integer_rows(rows),
        "real_incidence": True,
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1022_k3_real_degree3_incidence_shard.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
