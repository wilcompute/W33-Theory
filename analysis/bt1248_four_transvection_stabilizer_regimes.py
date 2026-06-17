#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

GROUP_ORDER = 51840
PATTERNS = [
    {"name": "diam10_A", "count": 12960, "diameter": 10, "pair_orders": {"9": 1, "24": 5}, "triple_orders": {"648": 4}, "iso_pairs": 1},
    {"name": "diam10_B", "count": 3240, "diameter": 10, "pair_orders": {"9": 2, "24": 4}, "triple_orders": {"648": 4}, "iso_pairs": 2},
    {"name": "diam10_C", "count": 6480, "diameter": 10, "pair_orders": {"24": 6}, "triple_orders": {"648": 4}, "iso_pairs": 0},
    {"name": "diam12", "count": 25920, "diameter": 12, "pair_orders": {"9": 2, "24": 4}, "triple_orders": {"72": 1, "648": 3}, "iso_pairs": 2},
    {"name": "diam14_BT1228", "count": 12960, "diameter": 14, "pair_orders": {"9": 3, "24": 3}, "triple_orders": {"72": 2, "648": 2}, "iso_pairs": 3},
]


def build():
    rows = []
    by_diam = {}
    for p in PATTERNS:
        row = dict(p)
        row["setwise_stabilizer_order"] = GROUP_ORDER // p["count"]
        row["orbit_size"] = p["count"]
        rows.append(row)
        by_diam.setdefault(str(p["diameter"]), []).append(row)
    return {
        "bt": 1248,
        "title": "Four-transvection stabilizer regime classifier",
        "acting_group_order": GROUP_ORDER,
        "full_order_orbit_rows": rows,
        "by_diameter": {
            d: {
                "total_sets": sum(r["count"] for r in rs),
                "orbit_count": len(rs),
                "stabilizer_orders": sorted({r["setwise_stabilizer_order"] for r in rs}),
            }
            for d, rs in sorted(by_diam.items(), key=lambda kv: int(kv[0]))
        },
        "diagnostic": {
            "diam10": "three orbits, stabilizers 4, 8, 16; locally fast because every triple already closes to 648",
            "diam12": "one orbit, stabilizer 2; one triple remains at 72",
            "diam14": "one orbit, stabilizer 4; balanced pair/triple closure and BT1228/BT1233 fingerprint",
        },
        "interpretation": "The diameter-14 BT1228 regime is not the largest-stabilizer orbit. Its distinction is balanced local closure, not maximal symmetry."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1248_four_transvection_stabilizer_regimes_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1248, "by_diameter":result["by_diameter"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
