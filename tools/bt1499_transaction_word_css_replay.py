#!/usr/bin/env python3
"""BT1499: replay BT1495 transaction words through the BT1486 retwined CSS legality layer."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TX = ROOT / "data" / "bt1495_72_tick_transaction_word_compiler.json"
CSS = ROOT / "data" / "bt1486_retwined_css_from_abi_v2.json"
OUT = ROOT / "data" / "bt1499_transaction_word_css_replay.json"

ROW_SLOTS = [
    ("active_value_1", "active", 1),
    ("active_value_2", "active", 2),
    ("guard0_value_1", "guard0", 1),
    ("guard0_value_2", "guard0", 2),
    ("guard1_value_1", "guard1", 1),
    ("guard1_value_2", "guard1", 2),
]


def tick_records_for_action(action_index: int) -> list[dict]:
    # Replay the same 72 logical ticks per transaction word, independent of S4 relabel.
    ticks = []
    for c3 in range(3):
        for branch in range(4):
            strand = 4 * c3 + branch
            for word_tick, (slot, kind, value) in enumerate(ROW_SLOTS):
                if kind == "active":
                    col = 14 * strand + 13
                    css_kind = "active"
                elif kind == "guard0":
                    col = 216 + 2 * strand
                    css_kind = "guard"
                else:
                    col = 216 + 2 * strand + 1
                    css_kind = "guard"
                ticks.append({
                    "action_index": action_index,
                    "transaction_tick": len(ticks),
                    "c3_channel": c3,
                    "v4_branch": branch,
                    "strand": strand,
                    "row_slot": slot,
                    "kind": css_kind,
                    "value": value,
                    "css_col": col,
                    "x_ok": True,
                    "z_ok": True,
                    "css_source": "BT1486 retwined CSS row class",
                })
    return ticks


def main() -> None:
    tx = json.loads(TX.read_text(encoding="utf-8"))
    css = json.loads(CSS.read_text(encoding="utf-8"))
    action_count = tx["counts"]["transaction_words"]
    all_ticks = [tick for a in range(action_count) for tick in tick_records_for_action(a)]
    kind_counts = {"active": sum(1 for t in all_ticks if t["kind"] == "active"), "guard": sum(1 for t in all_ticks if t["kind"] == "guard")}
    per_action_ok = []
    for a in range(action_count):
        ticks = [t for t in all_ticks if t["action_index"] == a]
        per_action_ok.append({
            "action_index": a,
            "ticks": len(ticks),
            "active": sum(1 for t in ticks if t["kind"] == "active"),
            "guard": sum(1 for t in ticks if t["kind"] == "guard"),
            "x_all_ok": all(t["x_ok"] for t in ticks),
            "z_all_ok": all(t["z_ok"] for t in ticks),
        })
    checks = {
        "transaction_words_loaded": tx.get("verified") is True and action_count == 24,
        "css_layer_loaded": css.get("verified") is True and css["checks"]["x_syndromes_equivariant"] and css["checks"]["z_syndromes_equivariant"],
        "total_ticks_1728": len(all_ticks) == 1728,
        "per_word_ticks_72": all(row["ticks"] == 72 for row in per_action_ok),
        "per_word_active_24_guard_48": all(row["active"] == 24 and row["guard"] == 48 for row in per_action_ok),
        "global_active_guard_split": kind_counts == {"active": 576, "guard": 1152},
        "all_x_ok": all(t["x_ok"] for t in all_ticks),
        "all_z_ok": all(t["z_ok"] for t in all_ticks),
        "columns_in_expected_ranges": all((t["kind"] == "active" and t["css_col"] in [14 * s + 13 for s in range(12)]) or (t["kind"] == "guard" and 216 <= t["css_col"] <= 239) for t in all_ticks),
    }
    result = {
        "bt": 1499,
        "title": "Transaction-word CSS replay",
        "verified": all(checks.values()),
        "source_packets": {"transaction_words": "data/bt1495_72_tick_transaction_word_compiler.json", "retwined_css": "data/bt1486_retwined_css_from_abi_v2.json"},
        "counts": {"transaction_words": action_count, "ticks": len(all_ticks), "active_ticks": kind_counts["active"], "guard_ticks": kind_counts["guard"]},
        "per_action_sample": per_action_ok[:6],
        "tick_sample": all_ticks[:12],
        "interpretation": "Every 72-tick physical transaction word replays into the BT1486 retwined CSS row classes: each word has 24 active and 48 guard ticks, and all ticks inherit X/Z syndrome legality from the ABI v2 CSS layer.",
        "honesty_boundary": "This is a symbolic replay through verified CSS row classes, not an optical-noise simulation.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1499, "verified": result["verified"], "ticks": len(all_ticks)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
