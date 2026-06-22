#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1451_closure_schedule_compiler.json"

FACE_ORDER = [4, 0, 1, 2, 6, 3, 5]
OPPOSITE_PAIRS = [[11, 10], [9, 8], [12, 13]]


def main() -> None:
    schedule = []
    for strand in range(12):
        active_col = strand * 14 + 13
        guard_cols = [216 + 2 * strand, 216 + 2 * strand + 1]
        pair_index = strand // 4
        side = (strand // 2) % 2
        orient = strand % 2
        context = {"strand": strand, "fixed_face": 4, "pair": OPPOSITE_PAIRS[pair_index], "side": side, "orient": orient}
        schedule.append({"step": len(schedule), "op": "active_tick", "col": active_col, **context})
        schedule.append({"step": len(schedule), "op": "guard_pair", "cols": guard_cols, **context})
        schedule.append({"step": len(schedule), "op": "frame_update", "rule": "retwined CSS frame update", **context})
        schedule.append({"step": len(schedule), "op": "syndrome_readout", "checks": ["X", "Z"], **context})
    op_counts = {op: sum(1 for row in schedule if row["op"] == op) for op in {row["op"] for row in schedule}}
    checks = {
        "twelve_active_ticks": op_counts.get("active_tick") == 12,
        "twelve_guard_pairs": op_counts.get("guard_pair") == 12,
        "twelve_frame_updates": op_counts.get("frame_update") == 12,
        "twelve_readouts": op_counts.get("syndrome_readout") == 12,
        "total_steps_are_48": len(schedule) == 48,
        "active_cols_are_tick_13": sorted(row["col"] for row in schedule if row["op"] == "active_tick") == [s * 14 + 13 for s in range(12)],
        "guard_cols_cover_tail": sorted({c for row in schedule if row["op"] == "guard_pair" for c in row["cols"]}) == list(range(216, 240)),
        "pairs_balanced": sorted([sum(1 for row in schedule if row.get("pair") == pair and row["op"] == "active_tick") for pair in OPPOSITE_PAIRS]) == [4, 4, 4],
    }
    result = {
        "bt": 1451,
        "title": "Closure schedule compiler",
        "verified": all(checks.values()),
        "schedule_type": "symbolic closure schedule for the Szilassi/Fano closure tick",
        "canonical_seed": {"fixed_face": 4, "face_order": FACE_ORDER, "opposite_pairs": OPPOSITE_PAIRS},
        "op_counts": op_counts,
        "schedule": schedule,
        "interpretation": "Each closure strand executes active tick, guard pair, retwined frame update, and X/Z syndrome readout.",
        "boundary": "Symbolic schedule only; hardware pulse amplitudes and phases are not specified.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1451, "verified": result["verified"], "steps": len(schedule)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
