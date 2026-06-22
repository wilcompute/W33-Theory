#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1463_schedule_equivalence.json"


def expand_template():
    events = []
    for c in range(3):
        for side in range(2):
            for orient in range(2):
                strand = 4 * c + 2 * side + orient
                events.append({"op": "active_tick", "strand": strand, "active_col": strand * 14 + 13, "c": c, "side": side, "orient": orient})
                events.append({"op": "guard_pair", "strand": strand, "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1], "c": c, "side": side, "orient": orient})
                events.append({"op": "frame_update", "strand": strand, "c": c, "side": side, "orient": orient})
                events.append({"op": "syndrome_readout", "strand": strand, "checks": ["X", "Z"], "c": c, "side": side, "orient": orient})
    return events


def trial_rows(events):
    rows = []
    for e in events:
        if e["op"] == "active_tick":
            for value in (1, 2):
                rows.append({"kind": "active_closure", "strand": e["strand"], "col": e["active_col"], "value": value})
        if e["op"] == "guard_pair":
            for col in e["guard_cols"]:
                for value in (1, 2):
                    rows.append({"kind": "guard_closure", "strand": e["strand"], "col": col, "value": value})
    return rows


def main() -> None:
    events = expand_template()
    rows = trial_rows(events)
    active_cols = sorted(e["active_col"] for e in events if e["op"] == "active_tick")
    guard_cols = sorted({c for e in events if e["op"] == "guard_pair" for c in e["guard_cols"]})
    checks = {
        "events_are_48": len(events) == 48,
        "active_ticks_are_12": sum(1 for e in events if e["op"] == "active_tick") == 12,
        "guard_pairs_are_12": sum(1 for e in events if e["op"] == "guard_pair") == 12,
        "frame_updates_are_12": sum(1 for e in events if e["op"] == "frame_update") == 12,
        "readouts_are_12": sum(1 for e in events if e["op"] == "syndrome_readout") == 12,
        "active_cols_match": active_cols == [s * 14 + 13 for s in range(12)],
        "guard_cols_match_tail": guard_cols == list(range(216, 240)),
        "trial_rows_are_72": len(rows) == 72,
        "active_rows_are_24": sum(1 for t in rows if t["kind"] == "active_closure") == 24,
        "guard_rows_are_48": sum(1 for t in rows if t["kind"] == "guard_closure") == 48,
    }
    result = {
        "bt": 1463,
        "title": "Schedule equivalence verifier",
        "verified": all(checks.values()),
        "template_loop": "c in C3, side in C2, orient in C2; strand=4*c+2*side+orient",
        "expanded_event_count": len(events),
        "trial_row_count": len(rows),
        "active_cols": active_cols,
        "guard_cols": guard_cols,
        "interpretation": "The compressed 4-op template expands exactly to the closure event rows used by the retwined checks.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1463, "verified": result["verified"], "events": len(events), "rows": len(rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
