#!/usr/bin/env python3
"""BT1015 contracts for the K3 level-2 middle row streams."""
from __future__ import annotations

import json
from pathlib import Path

F_VECTOR = [2776, 45120, 152960, 184320, 73728]
CONTRACTS = {
    "degree_2": {"rows": 45120, "cols": 152960, "nnz": 458880, "row_weight": 3, "target_rank": 42345},
    "degree_3": {"rows": 152960, "cols": 184320, "nnz": 737280, "row_weight": 4, "target_rank": 110593},
}


def manifest() -> dict:
    return {
        "theorem": "BT1015 K3 level-2 middle stream contracts",
        "f_vector": F_VECTOR,
        "contracts": CONTRACTS,
        "row_format": "Python integer bitset over high-dimensional simplex columns",
        "rank_core": "analysis/bt1015_f2_bitset_rank_core.py",
        "recovered_from": "BT1012 blocked monolith split into rank core, stream contracts, and smoke tests",
    }


if __name__ == "__main__":
    out = manifest()
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1015_k3_middle_stream_contracts.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
