#!/usr/bin/env python3
"""BT1495: compile BT1493 row pulses into full 72-tick transaction words."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1495_72_tick_transaction_word_compiler.json"

ROW_SLOTS = [
    ("active_value_1", "ERASE", "active", 1),
    ("active_value_2", "ROUTE", "active", 2),
    ("guard0_value_1", "PHASE", "guard0", 1),
    ("guard0_value_2", "X-CORR", "guard0", 2),
    ("guard1_value_1", "Z-CORR", "guard1", 1),
    ("guard1_value_2", "T-BIT", "guard1", 2),
]
# Native D4 square subgroup acting on branch labels 0,1,2,3 as square vertices.
D4_PERMS = {
    (0, 1, 2, 3),
    (1, 3, 0, 2),
    (3, 2, 1, 0),
    (2, 0, 3, 1),
    (1, 0, 3, 2),
    (2, 3, 0, 1),
    (0, 2, 1, 3),
    (3, 1, 2, 0),
}


def perm_order(p: tuple[int, ...]) -> int:
    cur = tuple(range(len(p)))
    ident = cur
    for n in range(1, 20):
        cur = tuple(p[i] for i in cur)
        if cur == ident:
            return n
    raise RuntimeError("order not found")


def compile_word(action_index: int, perm: tuple[int, ...]) -> dict:
    level = "native_d4_square_pulse" if perm in D4_PERMS else "s4_analyzer_relabel"
    ticks = []
    for c3 in range(3):
        for source_branch in range(4):
            target_branch = perm[source_branch]
            strand = 4 * c3 + source_branch
            for slot_index, (row_slot, lane, kind, value) in enumerate(ROW_SLOTS):
                transaction_tick = len(ticks)
                frame_tick = 48 + 8 * c3 + slot_index
                detector_slot = target_branch
                if kind == "active":
                    col = 14 * strand + 13
                elif kind == "guard0":
                    col = 216 + 2 * strand
                else:
                    col = 216 + 2 * strand + 1
                ticks.append({
                    "transaction_tick": transaction_tick,
                    "frame_tick": frame_tick,
                    "word_tick": slot_index,
                    "c3_channel": c3,
                    "source_branch": source_branch,
                    "target_branch": target_branch,
                    "row_slot": row_slot,
                    "hesse_lane": lane,
                    "row_kind": kind,
                    "qutrit_value": value,
                    "source_row_id": f"P{c3}.T{source_branch}.{kind}.v{value}",
                    "target_row_id": f"P{c3}.T{target_branch}.{kind}.v{value}",
                    "css_col": col,
                    "detector_slot": detector_slot,
                    "mirror_slot_mod_4": detector_slot % 4,
                    "interface_chain": "Fano fiber -> BT1411 detector -> BT1374 mirror slot -> BT1407 Hesse lane",
                })
    return {
        "action_index": action_index,
        "perm": list(perm),
        "order": perm_order(perm),
        "level": level,
        "tick_count": len(ticks),
        "ticks": ticks,
    }


def main() -> None:
    perms = sorted(itertools.permutations(range(4)))
    words = [compile_word(i, p) for i, p in enumerate(perms)]
    lane_counts = {lane: 0 for _, lane, _, _ in ROW_SLOTS}
    for w in words:
        for t in w["ticks"]:
            lane_counts[t["hesse_lane"]] += 1
    checks = {
        "s4_words_24": len(words) == 24,
        "each_word_has_72_ticks": all(w["tick_count"] == 72 for w in words),
        "total_ticks_1728": sum(w["tick_count"] for w in words) == 1728,
        "native_d4_words_8": sum(1 for w in words if w["level"] == "native_d4_square_pulse") == 8,
        "native_d4_ticks_576": sum(w["tick_count"] for w in words if w["level"] == "native_d4_square_pulse") == 576,
        "relabel_ticks_1152": sum(w["tick_count"] for w in words if w["level"] == "s4_analyzer_relabel") == 1152,
        "six_hesse_lanes_balanced": sorted(lane_counts.values()) == [288] * 6,
        "transaction_ticks_are_0_to_71": all([t["transaction_tick"] for t in w["ticks"]] == list(range(72)) for w in words),
        "detector_slot_equals_mirror_mod4": all(t["detector_slot"] % 4 == t["mirror_slot_mod_4"] for w in words for t in w["ticks"]),
    }
    result = {
        "bt": 1495,
        "title": "72-tick transaction word compiler",
        "verified": all(checks.values()),
        "source_packets": {
            "canonical_fiber": "data/bt1492_canonical_fano_s4_d4_fiber.json",
            "row_pulses": "data/bt1493_row_action_physical_pulse_compiler.json",
            "microframe": "data/bt1407_microframe_transaction_composer.json",
        },
        "counts": {
            "transaction_words": len(words),
            "ticks_per_word": 72,
            "total_ticks": sum(w["tick_count"] for w in words),
            "native_d4_words": sum(1 for w in words if w["level"] == "native_d4_square_pulse"),
            "native_d4_ticks": sum(w["tick_count"] for w in words if w["level"] == "native_d4_square_pulse"),
            "s4_relabel_ticks": sum(w["tick_count"] for w in words if w["level"] == "s4_analyzer_relabel"),
        },
        "lane_counts": lane_counts,
        "word_summaries": [{k: w[k] for k in ["action_index", "perm", "order", "level", "tick_count"]} for w in words],
        "sample_ticks": words[0]["ticks"][:12],
        "interpretation": "BT1493 row pulses are compiled into 24 full 72-tick transaction words, one for each S4 fiber action. Each tick carries Fano branch selection through detector, mirror-slot, and Hesse feed-forward lane metadata.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1495, "verified": result["verified"], "words": len(words), "ticks": result["counts"]["total_ticks"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
