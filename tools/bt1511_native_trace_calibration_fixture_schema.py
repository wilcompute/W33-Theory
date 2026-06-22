#!/usr/bin/env python3
"""BT1511: hardware-facing calibration fixture schema for native D4 traces."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "data" / "bt1511_native_trace_calibration_fixture_schema.json"
OUT_CSV = ROOT / "data" / "bt1511_native_trace_calibration_fixture_schema.csv"
OUT_MD = ROOT / "analysis" / "BT1511_native_trace_calibration_fixture_schema.md"

ACTIONS = ["id", "r90", "r180", "r270", "reflect_vertical", "reflect_horizontal", "reflect_diag", "reflect_antidiag"]
SLOTS = [("active_value_1", "ERASE", "active", 1), ("active_value_2", "ROUTE", "active", 2), ("guard0_value_1", "PHASE", "guard", 1), ("guard0_value_2", "X_CORR", "guard", 2), ("guard1_value_1", "Z_CORR", "guard", 1), ("guard1_value_2", "T_BIT", "guard", 2)]


def main() -> None:
    rows = []
    for action in ACTIONS:
        for c3 in range(3):
            for branch in range(4):
                strand = 4 * c3 + branch
                for slot_index, (slot, lane, kind, value) in enumerate(SLOTS):
                    if kind == "active":
                        css_col = 14 * strand + 13
                    elif slot.startswith("guard0"):
                        css_col = 216 + 2 * strand
                    else:
                        css_col = 216 + 2 * strand + 1
                    rows.append({
                        "fixture_id": f"BT1511.{action}.{c3}.{branch}.{slot_index}",
                        "d4_generator": action,
                        "c3_channel": c3,
                        "v4_branch": branch,
                        "tick_in_word": len([r for r in rows if r.get("d4_generator") == action]),
                        "detector_setting": branch,
                        "mirror_residue_mod4": branch % 4,
                        "hesse_lane": lane,
                        "row_slot": slot,
                        "qutrit_value": value,
                        "expected_css_row_class": kind,
                        "expected_css_col": css_col,
                        "measurement_placeholder": "pending_lab_measurement",
                        "acceptance_rule": "match detector/mirror/lane setting and CSS class before measuring loss/noise",
                    })
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    checks = {
        "fixture_rows_576": len(rows) == 576,
        "eight_generators": sorted({r["d4_generator"] for r in rows}) == sorted(ACTIONS),
        "rows_per_generator_72": sorted([sum(1 for r in rows if r["d4_generator"] == a) for a in ACTIONS]) == [72] * 8,
        "all_measurements_pending": all(r["measurement_placeholder"] == "pending_lab_measurement" for r in rows),
        "csv_written": OUT_CSV.exists(),
    }
    result = {
        "bt": 1511,
        "title": "Native trace calibration fixture schema",
        "verified": all(checks.values()),
        "csv": "data/bt1511_native_trace_calibration_fixture_schema.csv",
        "row_count": len(rows),
        "columns": list(rows[0].keys()),
        "interpretation": "BT1505 symbolic D4 route traces are converted into a hardware-facing calibration fixture schema with detector, mirror, Hesse lane, CSS row class, and measurement placeholder fields.",
        "honesty_boundary": "Measurement fields are placeholders only; this is a fixture schema, not lab data.",
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text("# BT1511 Native Trace Calibration Fixture Schema\n\n576 fixture rows: 8 native D4 generators times 72 ticks. Measurement fields remain pending lab data.\n", encoding="utf-8")
    print(json.dumps({"bt": 1511, "verified": result["verified"], "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
