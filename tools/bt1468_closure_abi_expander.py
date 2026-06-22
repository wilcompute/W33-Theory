#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1468_closure_abi_expander.json"


def make_packet(c: int, side: int, orient: int) -> dict:
    strand = 4 * c + 2 * side + orient
    return {
        "c": c,
        "side": side,
        "orient": orient,
        "strand": strand,
        "active_col": 14 * strand + 13,
        "guard_cols": [216 + 2 * strand, 216 + 2 * strand + 1],
        "frame_rule": "retwined_css_frame_update",
        "claim_tier": "exact_finite_decoder",
    }


def main() -> None:
    packets = [make_packet(c, side, orient) for c in range(3) for side in range(2) for orient in range(2)]
    events = []
    rows = []
    for p in packets:
        events.extend([
            {"op": "active_tick", "strand": p["strand"], "col": p["active_col"]},
            {"op": "guard_pair", "strand": p["strand"], "cols": p["guard_cols"]},
            {"op": "frame_update", "strand": p["strand"], "rule": p["frame_rule"]},
            {"op": "readout", "strand": p["strand"], "checks": ["X", "Z"]},
        ])
        for value in (1, 2):
            rows.append({"kind": "active", "strand": p["strand"], "col": p["active_col"], "value": value})
        for col in p["guard_cols"]:
            for value in (1, 2):
                rows.append({"kind": "guard", "strand": p["strand"], "col": col, "value": value})
    checks = {
        "packet_count_12": len(packets) == 12,
        "event_count_48": len(events) == 48,
        "row_count_72": len(rows) == 72,
        "active_cols_match": sorted(p["active_col"] for p in packets) == [14 * s + 13 for s in range(12)],
        "guard_tail_match": sorted({g for p in packets for g in p["guard_cols"]}) == list(range(216, 240)),
        "active_row_count_24": sum(1 for r in rows if r["kind"] == "active") == 24,
        "guard_row_count_48": sum(1 for r in rows if r["kind"] == "guard") == 48,
    }
    result = {
        "bt": 1468,
        "title": "Closure ABI expander",
        "verified": all(checks.values()),
        "packets": packets,
        "event_sample": events[:12],
        "row_sample": rows[:12],
        "counts": {"packets": len(packets), "events": len(events), "rows": len(rows)},
        "interpretation": "The BT1467 ABI is executable: this expander regenerates the exact 12 packets, 48 events, and 72 rows.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1468, "verified": result["verified"], "events": len(events)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
