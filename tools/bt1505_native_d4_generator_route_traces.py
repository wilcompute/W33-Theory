#!/usr/bin/env python3
"""BT1505: representative 72-tick route traces for each native D4 generator."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1505_native_d4_generator_route_traces.json"
MD = ROOT / "analysis" / "BT1505_native_d4_generator_route_traces.md"

ACTIONS = [
    ("id", [0, 1, 2, 3], 1, "identity"),
    ("r90", [1, 3, 0, 2], 4, "quarter_turn"),
    ("r180", [3, 2, 1, 0], 2, "half_turn"),
    ("r270", [2, 0, 3, 1], 4, "quarter_turn"),
    ("reflect_vertical", [1, 0, 3, 2], 2, "reflection"),
    ("reflect_horizontal", [2, 3, 0, 1], 2, "reflection"),
    ("reflect_diag", [0, 2, 1, 3], 2, "reflection"),
    ("reflect_antidiag", [3, 1, 2, 0], 2, "reflection"),
]
SLOTS = [
    ("active_value_1", "ERASE", "active", 1),
    ("active_value_2", "ROUTE", "active", 2),
    ("guard0_value_1", "PHASE", "guard0", 1),
    ("guard0_value_2", "X_CORR", "guard0", 2),
    ("guard1_value_1", "Z_CORR", "guard1", 1),
    ("guard1_value_2", "T_BIT", "guard1", 2),
]


def trace_for(name: str, perm: list[int], order: int, cls: str) -> dict:
    ticks = []
    for c3 in range(3):
        for branch in range(4):
            target = perm[branch]
            strand = 4 * c3 + branch
            for word_tick, (slot, lane, kind, value) in enumerate(SLOTS):
                if kind == "active":
                    css_col = 14 * strand + 13
                elif kind == "guard0":
                    css_col = 216 + 2 * strand
                else:
                    css_col = 216 + 2 * strand + 1
                ticks.append({
                    "tick": len(ticks),
                    "c3_channel": c3,
                    "source_branch": branch,
                    "target_branch": target,
                    "detector_slot": target,
                    "mirror_slot_mod_4": target % 4,
                    "word_tick": word_tick,
                    "row_slot": slot,
                    "hesse_lane": lane,
                    "row_kind": kind,
                    "qutrit_value": value,
                    "css_col": css_col,
                    "route": f"P{c3}.T{branch}.{slot}->det{target}->mirror{target%4}->{lane}",
                })
    return {
        "name": name,
        "perm": perm,
        "order": order,
        "class": cls,
        "ticks": len(ticks),
        "active_ticks": sum(1 for t in ticks if t["row_kind"] == "active"),
        "guard_ticks": sum(1 for t in ticks if t["row_kind"] != "active"),
        "lane_counts": {lane: sum(1 for t in ticks if t["hesse_lane"] == lane) for _, lane, _, _ in SLOTS},
        "trace": ticks,
        "representative_prefix": ticks[:12],
    }


def main() -> None:
    traces = [trace_for(*a) for a in ACTIONS]
    checks = {
        "eight_traces": len(traces) == 8,
        "each_trace_72_ticks": all(t["ticks"] == 72 for t in traces),
        "total_ticks_576": sum(t["ticks"] for t in traces) == 576,
        "each_trace_active_24_guard_48": all(t["active_ticks"] == 24 and t["guard_ticks"] == 48 for t in traces),
        "each_lane_12_per_trace": all(sorted(t["lane_counts"].values()) == [12] * 6 for t in traces),
        "detector_mirror_match": all(x["detector_slot"] % 4 == x["mirror_slot_mod_4"] for t in traces for x in t["trace"]),
        "class_profile": {"identity": 1, "quarter_turn": 2, "half_turn": 1, "reflection": 4} == {cls: sum(1 for t in traces if t["class"] == cls) for cls in ["identity", "quarter_turn", "half_turn", "reflection"]},
    }
    md = ["# BT1505 Native D4 Generator Route Traces", "", "Each native generator has a full 72-tick detector/mirror/Hesse trace. Prefixes:", ""]
    for t in traces:
        md.append(f"## {t['name']} ({t['class']}, order {t['order']})")
        for row in t["representative_prefix"][:6]:
            md.append(f"- tick {row['tick']}: {row['route']}, css_col={row['css_col']}")
        md.append("")
    MD.write_text("\n".join(md), encoding="utf-8")
    result = {
        "bt": 1505,
        "title": "Native D4 generator route traces",
        "verified": all(checks.values()),
        "traces": traces,
        "markdown": "analysis/BT1505_native_d4_generator_route_traces.md",
        "interpretation": "Every native D4 calibration class now has a concrete 72-tick detector/mirror/Hesse route trace with CSS column metadata.",
        "honesty_boundary": "These are symbolic route traces for calibration planning, not measured optical losses or timings.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1505, "verified": result["verified"], "ticks": sum(t["ticks"] for t in traces)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
