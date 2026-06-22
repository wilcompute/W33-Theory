#!/usr/bin/env python3
"""BT1502: split the 576 native D4 pulse ticks into calibration-priority classes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1502_native_d4_pulse_calibration_ledger.json"
TEX = ROOT / "analysis" / "BT1502_native_d4_pulse_calibration_ledger.tex"

# Square-vertex D4 action representatives from BT1495.
D4_ACTIONS = [
    {"name": "id", "perm": [0, 1, 2, 3], "order": 1, "class": "identity", "priority": "baseline"},
    {"name": "r90", "perm": [1, 3, 0, 2], "order": 4, "class": "quarter_turn", "priority": "high"},
    {"name": "r180", "perm": [3, 2, 1, 0], "order": 2, "class": "half_turn", "priority": "medium"},
    {"name": "r270", "perm": [2, 0, 3, 1], "order": 4, "class": "quarter_turn", "priority": "high"},
    {"name": "reflect_vertical", "perm": [1, 0, 3, 2], "order": 2, "class": "reflection", "priority": "high"},
    {"name": "reflect_horizontal", "perm": [2, 3, 0, 1], "order": 2, "class": "reflection", "priority": "high"},
    {"name": "reflect_diag", "perm": [0, 2, 1, 3], "order": 2, "class": "reflection", "priority": "medium"},
    {"name": "reflect_antidiag", "perm": [3, 1, 2, 0], "order": 2, "class": "reflection", "priority": "medium"},
]

ROW_SLOTS = ["ERASE", "ROUTE", "PHASE", "X_CORR", "Z_CORR", "T_BIT"]


def main() -> None:
    rows = []
    for idx, action in enumerate(D4_ACTIONS):
        row = {
            "action_index": idx,
            "name": action["name"],
            "perm": action["perm"],
            "order": action["order"],
            "class": action["class"],
            "priority": action["priority"],
            "ticks": 72,
            "active_ticks": 24,
            "guard_ticks": 48,
            "lane_ticks": {lane: 12 for lane in ROW_SLOTS},
            "calibration_read": "native D4 square-pulse generator class",
        }
        rows.append(row)
    class_counts: dict[str, int] = {}
    class_ticks: dict[str, int] = {}
    priority_ticks: dict[str, int] = {}
    for r in rows:
        class_counts[r["class"]] = class_counts.get(r["class"], 0) + 1
        class_ticks[r["class"]] = class_ticks.get(r["class"], 0) + r["ticks"]
        priority_ticks[r["priority"]] = priority_ticks.get(r["priority"], 0) + r["ticks"]
    lines = [
        r"\begin{center}\scriptsize",
        r"\begin{tabular}{l r l l r r r}",
        r"\toprule",
        r"Generator & Order & Class & Priority & Ticks & Active & Guard\\",
        r"\midrule",
    ]
    for r in rows:
        lines.append(f"{r['name']} & {r['order']} & {r['class']} & {r['priority']} & {r['ticks']} & {r['active_ticks']} & {r['guard_ticks']}\\".replace("_", r"\_"))
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    checks = {
        "d4_action_count_8": len(rows) == 8,
        "total_native_ticks_576": sum(r["ticks"] for r in rows) == 576,
        "active_native_ticks_192": sum(r["active_ticks"] for r in rows) == 192,
        "guard_native_ticks_384": sum(r["guard_ticks"] for r in rows) == 384,
        "class_counts_match_d4_profile": class_counts == {"identity": 1, "quarter_turn": 2, "half_turn": 1, "reflection": 4},
        "order_profile_matches_d4": {"1": 1, "2": 5, "4": 2} == {"1": sum(1 for r in rows if r["order"] == 1), "2": sum(1 for r in rows if r["order"] == 2), "4": sum(1 for r in rows if r["order"] == 4)},
        "each_lane_12_per_action": all(all(v == 12 for v in r["lane_ticks"].values()) for r in rows),
        "priority_ticks_sum_576": sum(priority_ticks.values()) == 576,
        "tex_written": TEX.exists() and "Generator" in TEX.read_text(encoding="utf-8"),
    }
    result = {
        "bt": 1502,
        "title": "Native D4 pulse calibration ledger",
        "verified": all(checks.values()),
        "rows": rows,
        "class_counts": class_counts,
        "class_ticks": class_ticks,
        "priority_ticks": priority_ticks,
        "tex_table": "analysis/BT1502_native_d4_pulse_calibration_ledger.tex",
        "interpretation": "The 576 native square-pulse ticks are split across the eight D4 generators: one baseline identity, two quarter-turns, one half-turn, and four reflections. Each generator contributes one 72-tick word with 24 active and 48 guard ticks.",
        "honesty_boundary": "This is a calibration-priority finite ledger, not a measured optical error model.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1502, "verified": result["verified"], "native_ticks": sum(r["ticks"] for r in rows)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
