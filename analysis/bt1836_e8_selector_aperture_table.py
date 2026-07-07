#!/usr/bin/env python3
"""BT1836: E8 selector aperture table.

Extends the 1440-row BT1825 aperture readout skeleton with the BT954 metric
winner-2 E8 selector labels. The four winner hyperbolic pairs are attached to
the four local striations.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1825_aperture_shot_table_exporter as aperture  # noqa: E402

WINNER = 2
WINNER_DECOMPOSITION = [[3, 68], [4, 42], [38, 65], [90, 144]]
WINNER_SCORE = {"trace": 38, "frobenius_squared": 444, "max_abs_entry": 8}

CSV_OUT = Path("data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE.csv")
JSON_OUT = Path("data/PART_BT1836_E8_SELECTOR_APERTURE_TABLE_summary.json")


def selector_rows():
    for row in aperture.rows():
        striation = int(row["striation"])
        e8_pair = WINNER_DECOMPOSITION[striation]
        out = dict(row)
        out.update({
            "e8_metric_winner": WINNER,
            "e8_selector_pair_a": e8_pair[0],
            "e8_selector_pair_b": e8_pair[1],
            "e8_selector_trace": WINNER_SCORE["trace"],
            "e8_selector_frobenius_squared": WINNER_SCORE["frobenius_squared"],
            "e8_selector_max_abs_entry": WINNER_SCORE["max_abs_entry"],
            "tetracode_quotient_status": "open"
        })
        yield out


def theorem_summary():
    rs = list(selector_rows())
    assert len(rs) == 1440
    assert sorted(set(r["e8_metric_winner"] for r in rs)) == [2]
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
        "metric_winner": WINNER,
        "winner_decomposition": WINNER_DECOMPOSITION,
        "winner_score": WINNER_SCORE,
        "selector_pair_counts": {str(k): v for k, v in sorted(pair_counts.items())},
        "csv": str(CSV_OUT),
        "checks": {
            "full_1440_rows_exported": True,
            "winner_2_attached_to_all_rows": True,
            "four_selector_pairs_each_appear_360_times": True,
            "tetracode_quotient_status_remains_open": True
        },
        "honest_scope": "E8 selector labels are attached from the uploaded BT954 metric result. This does not close the BT953 tetracode quotient."
    }
    JSON_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = theorem_summary()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
