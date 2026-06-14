#!/usr/bin/env python3
"""BT1025: manual K3 level-2 degree-2 full-rank runner.

This driver uses the real degree-2 incidence shard machinery from BT1021 to run
the full d2 rank target in a checkout/CI environment. It defaults to manifest
mode; use --run-full to execute the long all-row rank pass.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from bt1015_f2_bitset_rank_core import rank_mod2_integer_rows
    from bt1021_k3_real_degree2_incidence_shard import degree2_real_rows
except ImportError:
    from analysis.bt1015_f2_bitset_rank_core import rank_mod2_integer_rows
    from analysis.bt1021_k3_real_degree2_incidence_shard import degree2_real_rows

ROWS = 45120
COLS = 152960
NNZ = 458880
TARGET_RANK = 42345


def manifest(block_size: int) -> dict:
    return {
        "theorem": "BT1025 K3 level-2 degree-2 full rank runner",
        "map": "degree_2",
        "shape": [ROWS, COLS],
        "nnz": NNZ,
        "target_rank": TARGET_RANK,
        "block_size": block_size,
        "manual_command": f"python analysis/bt1025_k3_degree2_full_rank_runner.py --run-full --block-size {block_size}",
        "boundary": "Manifest mode only unless --run-full is supplied in checkout/CI. The full rank pass is long and not claimed here.",
    }


def run_full(block_size: int) -> dict:
    all_rows: list[int] = []
    for start in range(0, ROWS, block_size):
        rows, _ = degree2_real_rows(start, min(block_size, ROWS - start))
        all_rows.extend(rows)
    rank = rank_mod2_integer_rows(all_rows)
    return {
        "theorem": "BT1025 K3 level-2 degree-2 full rank run",
        "map": "degree_2",
        "shape": [ROWS, COLS],
        "rows_reduced": len(all_rows),
        "rank": rank,
        "target_rank": TARGET_RANK,
        "target_hit": rank == TARGET_RANK,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-size", type=int, default=512)
    parser.add_argument("--run-full", action="store_true")
    args = parser.parse_args()
    out = run_full(args.block_size) if args.run_full else manifest(args.block_size)
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1025_k3_degree2_full_rank_runner.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
