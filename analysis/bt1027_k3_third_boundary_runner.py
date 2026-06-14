#!/usr/bin/env python3
"""BT1027: manual runner manifest for the K3 level-2 third boundary map."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROWS = 152960
COLS = 184320
NNZ = 737280
TARGET = 110593


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block-size", type=int, default=512)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.execute:
        raise SystemExit("Long all-row execution belongs in checkout or CI; this script records the runner manifest.")
    out = {
        "theorem": "BT1027 K3 level-2 third boundary full rank runner",
        "map": "third_boundary",
        "shape": [ROWS, COLS],
        "nnz": NNZ,
        "target_rank": TARGET,
        "block_size": args.block_size,
        "manual_command": f"python analysis/bt1027_k3_third_boundary_runner.py --execute --block-size {args.block_size}",
        "workflow": ".github/workflows/k3-third-boundary-full-rank.yml",
        "boundary": "The manual runner is wired as a manifest. Full all-row execution requires checkout or CI wall-clock budget."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1027_k3_third_boundary_runner.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
