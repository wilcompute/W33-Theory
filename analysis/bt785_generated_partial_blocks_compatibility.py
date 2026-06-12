#!/usr/bin/env python3
"""BT785: generated source-local partial block compatibility.

Generalizes BT782 from one 48-row block to the whole 540*2 family of source-local
blocks.  Target-side fields remain unresolved by design.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT785_GENERATED_PARTIAL_BLOCKS_COMPATIBILITY_summary.json"


def partner(inner: int) -> int:
    branch, residue = divmod(inner, 12)
    duo, phase = divmod(residue, 6)
    return branch * 12 + (1 - duo) * 6 + phase


def main():
    total = 0
    triple_count = Counter()
    block_count = Counter()
    partner_ok = True
    for id540 in range(540):
        for bit in range(2):
            ids = [f"b_{id540:03d}_{bit}_{i:02d}" for i in range(48)]
            idset = set(ids)
            for inner in range(48):
                rid = ids[inner]
                pid = ids[partner(inner)]
                if pid not in idset or partner(partner(inner)) != inner:
                    partner_ok = False
                triple_count[(id540, bit, inner)] += 1
                block_count[(id540, bit)] += 1
                total += 1
    checks = {
        "rows_51840": total == 51840,
        "blocks_1080_each_48": len(block_count) == 1080 and Counter(block_count.values()) == Counter({48: 1080}),
        "triples_540_2_48_once": len(triple_count) == 540 * 2 * 48 and Counter(triple_count.values()) == Counter({1: 540 * 2 * 48}),
        "partner_involution_all_blocks": partner_ok,
        "id540_distribution": Counter(k[0] for k in triple_count) == Counter({i: 96 for i in range(540)}),
        "bit_distribution": Counter(k[1] for k in triple_count) == Counter({0: 25920, 1: 25920}),
        "inner_distribution": Counter(k[2] for k in triple_count) == Counter({i: 1080 for i in range(48)}),
    }
    result = {
        "theorem": "BT785 Generated Partial Blocks Compatibility",
        "summary": {"rows": total, "blocks": len(block_count), "ids540": 540, "bits": 2, "inner_ids": 48},
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "boundary": "This generates source-local 48-row blocks for all 540*2 metadata blocks and verifies partner consistency. Target-side Q43 fields remain unresolved."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]: raise SystemExit(1)

if __name__ == "__main__": main()
