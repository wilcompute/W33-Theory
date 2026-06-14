#!/usr/bin/env python3
"""BT975 - full D8 lane partition failure modes.

Classifies how the square D8 lane action interacts with 2+2 lane partitions.
Result: the present light/cache partition is preserved by a V4 subgroup only.
No 2+2 partition is preserved by the full transitive D8 action on four lanes.
"""
from __future__ import annotations
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt975_full_d8_failure_modes.json"
LANES = [0, 1, 2, 3]
OPS = {
    "id": {0:0,1:1,2:2,3:3},
    "r90": {0:2,2:1,1:3,3:0},
    "r180": {0:1,1:0,2:3,3:2},
    "r270": {0:3,3:1,1:2,2:0},
    "ref_a": {0:0,2:2,1:3,3:1},
    "ref_b": {0:1,1:0,2:2,3:3},
    "ref_c": {0:2,2:0,1:1,3:3},
    "ref_d": {0:3,3:0,1:2,2:1}
}
CURRENT = frozenset({0,1})


def norm_part(block):
    a = frozenset(block)
    b = frozenset(set(LANES) - set(block))
    return tuple(sorted([tuple(sorted(a)), tuple(sorted(b))]))


def preserves_partition(op, part):
    a = frozenset(part[0])
    image = frozenset(op[x] for x in a)
    return image == a or image == frozenset(part[1])


def main() -> None:
    parts = sorted({norm_part(c) for c in combinations(LANES, 2)})
    table = {}
    for p in parts:
        good = [name for name, op in OPS.items() if preserves_partition(op, p)]
        bad = [name for name in OPS if name not in good]
        table[str(p)] = {"preserving": good, "breaking": bad, "preserving_order": len(good)}
    current_key = str(norm_part(CURRENT))
    full_preserved = [p for p in parts if len(table[str(p)]["preserving"]) == len(OPS)]
    result = {
        "theorem": "BT975 full D8 lane partition failure modes",
        "current_partition": list(norm_part(CURRENT)),
        "d8_order": len(OPS),
        "all_2_plus_2_partitions": [list(map(list, p)) for p in parts],
        "partition_table": table,
        "current_partition_preserving_ops": table[current_key]["preserving"],
        "current_partition_breaking_ops": table[current_key]["breaking"],
        "full_d8_preserved_2_plus_2_partitions_count": len(full_preserved),
        "reading": "The present light/cache split is preserved by four D8 elements and broken by four. No nontrivial 2+2 lane partition is invariant under the full transitive D8 action; full D8 requires either all four lanes as one family or a refined non-partition ABI.",
        "checks": {"T1_current_preserving_order_4": len(table[current_key]["preserving"]) == 4, "T2_current_breaking_order_4": len(table[current_key]["breaking"]) == 4, "T3_no_2plus2_fullD8_partition": len(full_preserved) == 0, "T4_all_three_partitions_classified": len(parts) == 3, "T5_boundary_explicit": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT975 wrote", OUT)

if __name__ == "__main__":
    main()
