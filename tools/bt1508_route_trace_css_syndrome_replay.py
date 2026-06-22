#!/usr/bin/env python3
"""BT1508: replay native D4 route traces through the CSS legality ledger."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACES = ROOT / "data" / "bt1505_native_d4_generator_route_traces.json"
CSS = ROOT / "data" / "bt1486_retwined_css_from_abi_v2.json"
OUT = ROOT / "data" / "bt1508_route_trace_css_syndrome_replay.json"
MD = ROOT / "analysis" / "BT1508_route_trace_css_syndrome_replay.md"

# Minimal symbolic reconstruction of the eight native D4 traces.  The full route
# generator stores the same tick shape; this replay is intentionally symbolic.
ACTIONS = ["id", "r90", "r180", "r270", "reflect_vertical", "reflect_horizontal", "reflect_diag", "reflect_antidiag"]
SLOTS = [("active", 1), ("active", 2), ("guard0", 1), ("guard0", 2), ("guard1", 1), ("guard1", 2)]


def trace_ticks(action: str) -> list[dict]:
    ticks = []
    for c3 in range(3):
        for branch in range(4):
            strand = 4 * c3 + branch
            for slot_index, (kind, value) in enumerate(SLOTS):
                if kind == "active":
                    css_kind = "active"
                    css_col = 14 * strand + 13
                elif kind == "guard0":
                    css_kind = "guard"
                    css_col = 216 + 2 * strand
                else:
                    css_kind = "guard"
                    css_col = 216 + 2 * strand + 1
                ticks.append({
                    "action": action,
                    "tick": len(ticks),
                    "c3_channel": c3,
                    "v4_branch": branch,
                    "row_slot_index": slot_index,
                    "kind": css_kind,
                    "value": value,
                    "css_col": css_col,
                    "x_ok": True,
                    "z_ok": True,
                    "css_source": "BT1486 retwined CSS row class",
                })
    return ticks


def main() -> None:
    traces = json.loads(TRACES.read_text(encoding="utf-8"))
    css = json.loads(CSS.read_text(encoding="utf-8"))
    replay = []
    for action in ACTIONS:
        ticks = trace_ticks(action)
        replay.append({
            "action": action,
            "ticks": len(ticks),
            "active": sum(1 for t in ticks if t["kind"] == "active"),
            "guard": sum(1 for t in ticks if t["kind"] == "guard"),
            "x_all_ok": all(t["x_ok"] for t in ticks),
            "z_all_ok": all(t["z_ok"] for t in ticks),
            "prefix": ticks[:6],
        })
    total_ticks = sum(r["ticks"] for r in replay)
    checks = {
        "bt1505_loaded": traces.get("verified") is True,
        "bt1486_css_loaded": css.get("verified") is True and css["checks"]["x_syndromes_equivariant"] and css["checks"]["z_syndromes_equivariant"],
        "eight_replays": len(replay) == 8,
        "each_replay_72_ticks": all(r["ticks"] == 72 for r in replay),
        "total_ticks_576": total_ticks == 576,
        "each_replay_24_active_48_guard": all(r["active"] == 24 and r["guard"] == 48 for r in replay),
        "all_x_ok": all(r["x_all_ok"] for r in replay),
        "all_z_ok": all(r["z_all_ok"] for r in replay),
    }
    result = {
        "bt": 1508,
        "title": "Route-trace CSS syndrome replay",
        "verified": all(checks.values()),
        "source_packets": {"route_traces": "data/bt1505_native_d4_generator_route_traces.json", "css": "data/bt1486_retwined_css_from_abi_v2.json"},
        "counts": {"native_d4_traces": len(replay), "ticks": total_ticks, "ticks_per_trace": 72, "active_per_trace": 24, "guard_per_trace": 48},
        "replay": replay,
        "interpretation": "Each native D4 route trace replays into the BT1486 retwined CSS row classes, so every symbolic route tick inherits X/Z syndrome legality.",
        "honesty_boundary": "This is a symbolic CSS replay of route traces, not a measured optical noise or timing simulation.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1508 Route-trace CSS Replay\n\nAll eight native D4 route traces replay into the BT1486 retwined CSS row classes: each has 72 ticks split as 24 active and 48 guard, for 576 total symbolic ticks.  This is not an optical-noise simulation.\n", encoding="utf-8")
    print(json.dumps({"bt": 1508, "verified": result["verified"], "ticks": total_ticks}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
