#!/usr/bin/env python3
"""BT1519: materialize the full 576-row native D4 calibration fixture CSV."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "data" / "bt1519_full_native_d4_calibration_fixture.csv"
OUT_JSON = ROOT / "data" / "bt1519_full_fixture_csv_materializer.json"
MD = ROOT / "analysis" / "BT1519_full_fixture_csv_materializer.md"

ACTIONS = ["id", "r90", "r180", "r270", "reflect_vertical", "reflect_horizontal", "reflect_diag", "reflect_antidiag"]
SLOTS = [("active_value_1", "ERASE", "active", 1), ("active_value_2", "ROUTE", "active", 2), ("guard0_value_1", "PHASE", "guard", 1), ("guard0_value_2", "X_CORR", "guard", 2), ("guard1_value_1", "Z_CORR", "guard", 1), ("guard1_value_2", "T_BIT", "guard", 2)]


def rows():
    out = []
    for action in ACTIONS:
        tick = 0
        for c3 in range(3):
            for branch in range(4):
                strand = 4 * c3 + branch
                for slot, lane, kind, value in SLOTS:
                    col = 14 * strand + 13 if kind == "active" else (216 + 2 * strand if slot.startswith("guard0") else 216 + 2 * strand + 1)
                    out.append({
                        "fixture_id": f"BT1519.{action}.{tick:02d}",
                        "d4_generator": action,
                        "tick_in_word": tick,
                        "c3_channel": c3,
                        "v4_branch": branch,
                        "detector_setting": branch,
                        "mirror_residue_mod4": branch % 4,
                        "hesse_lane": lane,
                        "row_slot": slot,
                        "qutrit_value": value,
                        "expected_css_row_class": kind,
                        "expected_css_col": col,
                        "measurement_status": "pending_lab_measurement",
                        "measured_loss_db": "",
                        "measured_phase_error": "",
                        "notes": "",
                    })
                    tick += 1
    return out


def main() -> None:
    data = rows()
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    csv_size = OUT_CSV.stat().st_size
    checks = {
        "row_count_576": len(data) == 576,
        "eight_generators": len({r["d4_generator"] for r in data}) == 8,
        "rows_per_generator_72": all(sum(1 for r in data if r["d4_generator"] == a) == 72 for a in ACTIONS),
        "active_rows_192": sum(1 for r in data if r["expected_css_row_class"] == "active") == 192,
        "guard_rows_384": sum(1 for r in data if r["expected_css_row_class"] == "guard") == 384,
        "all_measurements_pending_blank": all(r["measurement_status"] == "pending_lab_measurement" and r["measured_loss_db"] == "" and r["measured_phase_error"] == "" for r in data),
        "csv_written_nonempty": OUT_CSV.exists() and csv_size > 10000,
    }
    result = {
        "bt": 1519,
        "title": "Full fixture CSV materializer",
        "verified": all(checks.values()),
        "csv": "data/bt1519_full_native_d4_calibration_fixture.csv",
        "row_count": len(data),
        "csv_size_bytes": csv_size,
        "size_note": "Full 576-row CSV committed; measurement fields are blank pending lab data.",
        "interpretation": "The compact BT1511 sample is expanded into the full 576-row native D4 calibration fixture CSV.",
        "honesty_boundary": "The CSV is a fixture to be filled by measurements; it contains no measured optical data.",
        "checks": checks,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(f"# BT1519 Full Fixture CSV Materializer\n\nMaterialized full native D4 calibration fixture CSV with 576 rows. Size: {csv_size} bytes. Measurement columns are blank placeholders.\n", encoding="utf-8")
    print(json.dumps({"bt": 1519, "verified": result["verified"], "rows": len(data), "bytes": csv_size}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
