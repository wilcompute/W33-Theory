#!/usr/bin/env python3
"""BT1012: K3 level-2 middle row streamer manifest and exact F2 rank kernel.

The full face iterator is intentionally invoked only in checkout/CI.  This file
contains the exact bitset row-reduction kernel plus the hard dimensions/targets
for the two middle maps.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

F_VECTOR = [2776, 45120, 152960, 184320, 73728]
MAPS = {
    2: {"shape": [45120, 152960], "nnz": 458880, "target_rank": 42345},
    3: {"shape": [152960, 184320], "nnz": 737280, "target_rank": 110593},
}


def rank_mod2_integer_rows(rows: Iterable[int]) -> int:
    basis: dict[int, int] = {}
    rank = 0
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            old = basis.get(pivot)
            if old is None:
                basis[pivot] = x
                rank += 1
                break
            x ^= old
    return rank


def row_streamer_contract(degree: int) -> dict:
    m = MAPS[degree]
    return {
        "degree": degree,
        "rows": m["shape"][0],
        "cols": m["shape"][1],
        "nnz": m["nnz"],
        "target_rank": m["target_rank"],
        "row_format": "Python int bitset over high-dimensional simplex columns",
        "consumer": "rank_mod2_integer_rows(rows)",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, choices=[2, 3], default=2)
    args = parser.parse_args()
    out = {
        "theorem": "BT1012 K3_16 level-2 middle row streamer",
        "f_vector": F_VECTOR,
        "stream_contracts": {"degree_2": row_streamer_contract(2), "degree_3": row_streamer_contract(3)},
        "selected_contract": row_streamer_contract(args.degree),
        "status": "row-stream contract and exact F2 reducer committed; full face generation/rank execution belongs in checkout or CI",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1012_k3_level2_middle_row_streamer.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
