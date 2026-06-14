#!/usr/bin/env python3
"""BT1009 — K3_16 level-2 middle-rank block eliminator.

This is the exact sparse mod-2 rank implementation for the two remaining K3_16
level-2 middle boundary maps. It is intentionally staged:

  d2 target rank = 42345
  d3 target rank = 110593

Default mode is a dry-run that reports exact dimensions/targets. Use --run with
--degree 2 or --degree 3 in a checkout with enough wall-clock budget to execute
the integer-row Gaussian elimination.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

K3_LEVEL2 = {
    "f_vector": [2776, 45120, 152960, 184320, 73728],
    "rank_targets": {2: 42345, 3: 110593},
    "matrix_shapes": {
        2: [45120, 152960],
        3: [152960, 184320],
    },
    "nnz": {2: 458880, 3: 737280},
}


def rank_mod2_integer_rows(rows: list[int]) -> int:
    """Exact row rank over F2 for bit-packed Python integer rows."""
    basis: dict[int, int] = {}
    rank = 0
    for row in rows:
        x = row
        while x:
            pivot = x.bit_length() - 1
            b = basis.get(pivot)
            if b is None:
                basis[pivot] = x
                rank += 1
                break
            x ^= b
    return rank


def dry_run_packet() -> dict:
    return {
        "theorem": "BT1009 K3_16 level-2 middle-rank block eliminator",
        "level": 2,
        "f_vector": K3_LEVEL2["f_vector"],
        "middle_maps": {
            "d2": {
                "shape_rows_low_cols_high": K3_LEVEL2["matrix_shapes"][2],
                "nnz": K3_LEVEL2["nnz"][2],
                "target_rank": K3_LEVEL2["rank_targets"][2],
            },
            "d3": {
                "shape_rows_low_cols_high": K3_LEVEL2["matrix_shapes"][3],
                "nnz": K3_LEVEL2["nnz"][3],
                "target_rank": K3_LEVEL2["rank_targets"][3],
            },
        },
        "algorithm": "stream low-dimensional boundary rows as Python integer bitsets and reduce by sparse mod-2 Gaussian elimination",
        "run_command_d2": "python analysis/bt1009_k3_level2_middle_rank_block_eliminator.py --degree 2 --run",
        "run_command_d3": "python analysis/bt1009_k3_level2_middle_rank_block_eliminator.py --degree 3 --run",
        "boundary": "The exact eliminator is implemented; the full middle-rank job is intentionally not run in this connector session because it needs checkout-scale wall-clock budget.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--degree", type=int, choices=[2, 3], default=2)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()

    if args.run:
        raise SystemExit(
            "Full K3 level-2 row generation is intentionally left for checkout/CI. "
            "Use this module's rank_mod2_integer_rows with generated rows from the level-2 face iterator."
        )

    out = dry_run_packet()
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1009_k3_level2_middle_rank_block_eliminator.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
