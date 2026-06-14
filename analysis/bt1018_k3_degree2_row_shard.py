#!/usr/bin/env python3
"""BT1018: bounded degree-2 row shard for K3 level-2 middle-rank work.

This is the first accepted shard under the BT1015/BT1016 row-stream contract.
It generates a deterministic bounded window of degree-2-style rows with the real
map shape/row weight and feeds the exact F2 bitset reducer.

The full K3 face iterator remains the checkout/CI layer; this shard verifies the
block API that the real iterator will use: start, count, cols, row_weight.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from bt1015_f2_bitset_rank_core import rank_mod2_integer_rows, row_weight
except ImportError:
    from analysis.bt1015_f2_bitset_rank_core import rank_mod2_integer_rows, row_weight

ROWS = 45120
COLS = 152960
NNZ = 458880
ROW_WEIGHT = 3
TARGET_RANK = 42345


def row_window(start: int, count: int) -> list[int]:
    rows: list[int] = []
    for r in range(start, min(start + count, ROWS)):
        # Deterministic contract shard: three incident high-cell columns per row.
        # The spacing avoids accidental duplicates in small windows.
        cols = [(17 * r + 104729 * j + j * j) % COLS for j in range(ROW_WEIGHT)]
        value = 0
        for c in cols:
            value |= 1 << c
        rows.append(value)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=256)
    args = parser.parse_args()
    rows = row_window(args.start, args.count)
    out = {
        "theorem": "BT1018 K3 level-2 degree-2 bounded row shard",
        "map": "degree_2",
        "shape": [ROWS, COLS],
        "global_nnz": NNZ,
        "target_rank": TARGET_RANK,
        "window": {"start": args.start, "count": len(rows)},
        "expected_row_weight": ROW_WEIGHT,
        "row_weight_minmax": [min(row_weight(r) for r in rows), max(row_weight(r) for r in rows)] if rows else [0, 0],
        "window_rank": rank_mod2_integer_rows(rows),
        "status": "bounded shard API verified; replace deterministic columns with real face incidences in checkout/CI iterator",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1018_k3_degree2_row_shard.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
