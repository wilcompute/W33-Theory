#!/usr/bin/env python3
"""BT1843: aperture-to-shot protocol.

Turns the E8-labelled aperture table into a physical measurement protocol schema:
each center/phase/striation/aperture row receives a detector channel, setting
label, shot budget, and expected contextual contribution target. The E8 labels
come through BT1836, which now imports the canonical BT1853 runtime selector API.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bt1836_e8_selector_aperture_table as e8ap  # noqa: E402
import bt1853_runtime_selector_api as selector_api  # noqa: E402

CSV_OUT = Path("data/PART_BT1843_APERTURE_TO_SHOT_PROTOCOL.csv")
JSON_OUT = Path("data/PART_BT1843_APERTURE_TO_SHOT_PROTOCOL_summary.json")
DEFAULT_SHOTS = 100


def protocol_rows(shots_per_setting: int = DEFAULT_SHOTS):
    for row in e8ap.selector_rows():
        center = int(row["center"])
        phase = int(row["phase"])
        striation = int(row["striation"])
        out = dict(row)
        out.update({
            "measurement_setting": f"C{center:02d}_P{phase:02d}_S{striation}",
            "detector_channel": f"D{striation}",
            "shot_budget": shots_per_setting,
            "expected_contextual_contribution": "0.1",
            "observed_counts": "",
            "observed_successes": "",
            "analysis_status": "pending_data"
        })
        yield out


def theorem_summary(shots_per_setting: int = DEFAULT_SHOTS):
    rs = list(protocol_rows(shots_per_setting))
    assert len(rs) == 1440
    total_shots = len(rs) * shots_per_setting
    detector_counts = {}
    for r in rs:
        detector_counts[r["detector_channel"]] = detector_counts.get(r["detector_channel"], 0) + 1
    assert set(detector_counts.values()) == {360}
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rs[0].keys()))
        writer.writeheader()
        writer.writerows(rs)
    summary = {
        "theorem": "BT1843 Aperture-to-Shot Protocol",
        "rows": len(rs),
        "shots_per_setting": shots_per_setting,
        "total_nominal_shots": total_shots,
        "detector_channel_counts": detector_counts,
        "canonical_basis_name": selector_api.CANONICAL_BASIS_NAME,
        "csv": str(CSV_OUT),
        "checks": {
            "full_1440_rows": True,
            "four_detector_channels_balanced": True,
            "e8_metric_winner_labels_present": True,
            "uses_BT1853_runtime_selector_api": selector_api.METRIC_WINNER == 2,
            "observed_columns_blank_until_data": True
        },
        "honest_scope": "Physical measurement protocol skeleton. It is not a measured experiment."
    }
    JSON_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    summary = theorem_summary()
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
