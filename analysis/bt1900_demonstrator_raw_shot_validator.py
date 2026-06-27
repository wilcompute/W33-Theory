#!/usr/bin/env python3
"""BT1900 raw-shot validator for the single-photon Holonet demonstrator.

Usage:
  python analysis/bt1900_demonstrator_raw_shot_validator.py shots.jsonl

Input rows are JSON objects, one per line, matching schemas/bt1900_demonstrator_raw_shot_schema.json.
The validator performs lightweight schema checks plus schedule-integrity counts.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

REQUIRED = [
    "shot_id", "witting_tetrad", "alice_slot", "bob_slot", "logical_pair_type",
    "transaction_tick", "time_bin", "detector_id", "polarization_setting",
    "tritter_phase_setting", "modulator_phase", "click_pattern", "dark_reference",
    "loss_probe", "accepted_flag", "witness_class",
]
PAIR_TYPES = {"same_ray", "compatible_distinct", "retry_shadow"}
WITNESS_CLASSES = {"diagonal_contextual", "off_diagonal_data", "calibration", "guard", "unknown"}


def fail(msg: str) -> None:
    raise SystemExit(f"BT1900 validation failed: {msg}")


def check_row(row: dict, line_no: int) -> None:
    missing = [k for k in REQUIRED if k not in row]
    if missing:
        fail(f"line {line_no}: missing fields {missing}")
    if not (0 <= int(row["witting_tetrad"]) <= 39):
        fail(f"line {line_no}: witting_tetrad out of range")
    if not (0 <= int(row["alice_slot"]) <= 3 and 0 <= int(row["bob_slot"]) <= 3):
        fail(f"line {line_no}: slot out of range")
    if row["logical_pair_type"] not in PAIR_TYPES:
        fail(f"line {line_no}: bad logical_pair_type")
    if not (0 <= int(row["transaction_tick"]) <= 71):
        fail(f"line {line_no}: transaction_tick out of range")
    if not (0 <= int(row["time_bin"]) <= 2047):
        fail(f"line {line_no}: time_bin out of range")
    if row["witness_class"] not in WITNESS_CLASSES:
        fail(f"line {line_no}: bad witness_class")
    for key in ["dark_reference", "loss_probe", "accepted_flag"]:
        if not isinstance(row[key], bool):
            fail(f"line {line_no}: {key} must be boolean")


def main(path: str) -> None:
    rows = []
    for line_no, line in enumerate(Path(path).read_text().splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        check_row(row, line_no)
        rows.append(row)

    frame_keys = {(r["witting_tetrad"], r["alice_slot"], r["bob_slot"]) for r in rows}
    witness_counts = Counter(r["witness_class"] for r in rows)
    pair_counts = Counter(r["logical_pair_type"] for r in rows)
    accepted = sum(1 for r in rows if r["accepted_flag"])

    summary = {
        "rows": len(rows),
        "basis_local_frame_records_seen": len(frame_keys),
        "basis_local_frame_records_target": 640,
        "schedule_integrity_pass": len(frame_keys) == 640,
        "accepted_rows": accepted,
        "accepted_rate_target": "13/40",
        "witness_counts": dict(witness_counts),
        "logical_pair_counts": dict(pair_counts),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("expected one JSONL file path")
    main(sys.argv[1])
