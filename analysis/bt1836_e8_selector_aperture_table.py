#!/usr/bin/env python3
"""BT1836: E8 selector aperture table.

Extends the 1440-row BT1825 aperture readout skeleton with the canonical
BT1853 runtime selector API. The four winner-2 selector pairs are attached to
the four local striations from one importable source of truth.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1825_aperture_shot_table_exporter as aperture  # noqa: E402
import bt1853_runtime_selector_api as selector_api  # noqa: E402

CSV_OUT = Path("data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE.csv")
JSON_OUT = Path("data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE_summary.json")


def selector_rows():
    for row in aperture.rows():
        striation = int(row["striation"])
        out = dict(row)
        out.update(selector_api.selector_record(striation))
        yield out


def theorem_summary():
    rs = list(selector_rows())
    assert len(rs) == 1440
    assert sorted(set(r["e8_metric_winner"] for r in rs)) == [selector_api.METRIC_WINNER]
    pair_counts = {}
    for r in rs:
        pair = (r["e8_selector_pair_a"], r["e8_selector_pair_b"])
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    assert set(pair_counts.values()) == {360}
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rs[0].keys()))
        writer.writeheader()
        writer.writerows(rs)
    summary = {
        "theorem": "BT1836 E8 Selector Aperture Table",
        "rows": len(rs),
        "metric_winner": selector_api.METRIC_WINNER,
        "canonical_basis_name": selector_api.CANONICAL_BASIS_NAME,
        "winner_decomposition": [list(p) for p in selector_api.CANONICAL_SELECTOR_PAIRS],
        "selector_pair_counts": {str(k): v for k, v in sorted(pair_counts.items())},
        "csv": str(CSV_OUT),
        "checks": {
            "full_1440_rows_exported": True,
            "winner_2_attached_to_all_rows": True,
            "four_selector_pairs_each_appear_360_times": True,
            "uses_BT1853_runtime_selector_api": True,
            "local_A2_boundary_recorded": "local_A2" in rs[0]["tetracode_quotient_status"]
        },
        "honest_scope": "E8 selector labels are imported from BT1853. Local A2/Weyl/glue refinement remains open."
    }
    JSON_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = theorem_summary()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
