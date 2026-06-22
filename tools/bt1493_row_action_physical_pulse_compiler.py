#!/usr/bin/env python3
"""BT1493: compile ABI row actions into holonet pulse lanes."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1489_s4_d4_v4_row_action_lift import build_rows, lift_branch_perm, perm_order

OUT = ROOT / "data" / "bt1493_row_action_physical_pulse_compiler.json"
ROW_SLOT_NAMES = [
    "active_value_1",
    "active_value_2",
    "guard0_value_1",
    "guard0_value_2",
    "guard1_value_1",
    "guard1_value_2",
]


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def row_slot_name(row: dict) -> str:
    if row["kind"] == "active":
        return f"active_value_{row['value']}"
    return f"guard{row['guard_slot']}_value_{row['value']}"


def epilogue_lane_table(bt1407: dict) -> dict[tuple[int, int], dict]:
    table: dict[tuple[int, int], dict] = {}
    for tick in bt1407["epilogue_ticks"]:
        phase_trit = int(tick["phase_trit"])
        word_tick = int(tick["word_tick"])
        if word_tick < len(ROW_SLOT_NAMES):
            table[(phase_trit, word_tick)] = tick
    return table


def action_level(classifier_row: dict) -> str:
    if classifier_row["in_d4_square_subgroup"]:
        return "native_d4_square_pulse"
    return "s4_analyzer_relabel"


def main() -> None:
    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")
    bt1411 = load_json("data/bt1411_witting_basis_analyzer_unitaries.json")
    bt1487 = load_json("data/bt1487_v4_triangle_stabilizer_classifier.json")
    bt1489 = load_json("data/bt1489_s4_d4_v4_row_action_lift.json")
    bt1492 = load_json("data/bt1492_canonical_fano_s4_d4_fiber.json")

    rows = build_rows()
    row_index = {
        (row["c3_channel"], row["v4_branch"], row["row_position"]): index
        for index, row in enumerate(rows)
    }
    epilogue = epilogue_lane_table(bt1407)
    branch_lines = bt1492["canonical_objects"]["v4_branch_lines_not_through_anchor"]
    classifier_rows = sorted(bt1487["classifier_rows"], key=lambda row: row["perm"])
    d4_perms = {
        tuple(row["perm"]) for row in classifier_rows if row["in_d4_square_subgroup"]
    }

    compiled_pulses = []
    action_summaries = []
    for action_index, classifier_row in enumerate(classifier_rows):
        perm = tuple(classifier_row["perm"])
        lift = lift_branch_perm(perm, rows, row_index)
        level = action_level(classifier_row)
        action_pulses = []
        for source_index, target_index in enumerate(lift):
            source = rows[source_index]
            target = rows[target_index]
            lane_tick = epilogue[(source["c3_channel"], source["row_position"])]
            pulse = {
                "action_index": action_index,
                "action_level": level,
                "branch_perm": list(perm),
                "source_row_id": source["row_id"],
                "target_row_id": target["row_id"],
                "c3_channel": source["c3_channel"],
                "row_slot": row_slot_name(source),
                "frame_tick": int(lane_tick["frame_tick"]),
                "word_tick": source["row_position"],
                "hesse_lane": lane_tick["op"],
                "source_branch": source["v4_branch"],
                "target_branch": target["v4_branch"],
                "source_branch_line": branch_lines[source["v4_branch"]],
                "target_branch_line": branch_lines[target["v4_branch"]],
                "detector_slot": target["v4_branch"],
                "mirror_slot_mod_4": target["v4_branch"],
                "qutrit_value": source["value"],
                "hardware_reads": [
                    "BT1411 analyzer maps the target branch ray to detector slot j",
                    "BT1374 consumes detector slot j as mirror_slot mod 4",
                    "BT1407 schedules the C3 row lane inside the Hesse epilogue word",
                ],
            }
            compiled_pulses.append(pulse)
            action_pulses.append(pulse)
        action_summaries.append(
            {
                "action_index": action_index,
                "perm": list(perm),
                "level": level,
                "row_pulses": len(action_pulses),
                "order": classifier_row["order"],
                "frame_ticks": sorted({pulse["frame_tick"] for pulse in action_pulses}),
                "detector_slots": sorted(
                    {pulse["detector_slot"] for pulse in action_pulses}
                ),
            }
        )

    level_counts = Counter(pulse["action_level"] for pulse in compiled_pulses)
    tick_counts = Counter(pulse["frame_tick"] for pulse in compiled_pulses)
    slot_counts = Counter(pulse["detector_slot"] for pulse in compiled_pulses)
    lane_counts = Counter(pulse["hesse_lane"] for pulse in compiled_pulses)
    d4_order_profile = Counter(perm_order(perm) for perm in d4_perms)
    expected_lane_by_position = {
        position: epilogue[(0, position)]["op"]
        for position in range(len(ROW_SLOT_NAMES))
    }

    checks = {
        "bt1374_slot_rule_loaded": bt1374["checks"]["transversal_is_mirror_slot_mod_4"]
        is True,
        "bt1407_microframe_loaded": bt1407["verified"] is True,
        "bt1411_analyzers_loaded": bt1411["verified"] is True,
        "bt1489_row_lift_loaded": bt1489["verified"] is True,
        "bt1492_canonical_fiber_loaded": bt1492["verified"] is True,
        "compiled_all_s4_actions_on_72_rows": len(compiled_pulses) == 24 * 72,
        "native_d4_actions_are_8_times_72": level_counts["native_d4_square_pulse"]
        == 8 * 72,
        "s4_relabel_actions_are_16_times_72": level_counts["s4_analyzer_relabel"]
        == 16 * 72,
        "each_action_has_72_row_pulses": all(
            summary["row_pulses"] == 72 for summary in action_summaries
        ),
        "row_slots_use_first_six_hesse_lanes": expected_lane_by_position
        == {
            0: "ERASE",
            1: "ROUTE",
            2: "PHASE",
            3: "X-CORR",
            4: "Z-CORR",
            5: "T-BIT",
        },
        "frame_ticks_are_hesse_epilogue_row_ticks": sorted(tick_counts)
        == [48, 49, 50, 51, 52, 53, 56, 57, 58, 59, 60, 61, 64, 65, 66, 67, 68, 69],
        "detector_slots_are_four_branch_slots": dict(sorted(slot_counts.items()))
        == {0: 432, 1: 432, 2: 432, 3: 432},
        "mirror_residue_equals_detector_slot": all(
            pulse["mirror_slot_mod_4"] == pulse["detector_slot"]
            for pulse in compiled_pulses
        ),
        "target_branch_follows_branch_perm": all(
            pulse["target_branch"] == pulse["branch_perm"][pulse["source_branch"]]
            for pulse in compiled_pulses
        ),
        "native_d4_order_profile_matches": dict(sorted(d4_order_profile.items()))
        == {1: 1, 2: 5, 4: 2},
        "lane_counts_are_balanced": dict(sorted(lane_counts.items()))
        == {lane: 288 for lane in expected_lane_by_position.values()},
    }

    result = {
        "bt": 1493,
        "title": "ABI row-action physical pulse compiler",
        "verified": all(checks.values()),
        "source_packets": {
            "slot_rule": "data/bt1374_q6_tomotope_packet_route_compiler.json",
            "microframe": "data/bt1407_microframe_transaction_composer.json",
            "analyzers": "data/bt1411_witting_basis_analyzer_unitaries.json",
            "row_lift": "data/bt1489_s4_d4_v4_row_action_lift.json",
            "canonical_fiber": "data/bt1492_canonical_fano_s4_d4_fiber.json",
        },
        "counts": {
            "compiled_actions": len(action_summaries),
            "compiled_row_pulses": len(compiled_pulses),
            "native_d4_row_pulses": level_counts["native_d4_square_pulse"],
            "s4_analyzer_relabel_row_pulses": level_counts["s4_analyzer_relabel"],
            "row_ticks_per_action": 18,
            "detector_slots": 4,
        },
        "epilogue_lane_map": {
            ROW_SLOT_NAMES[position]: lane
            for position, lane in expected_lane_by_position.items()
        },
        "action_summaries": action_summaries,
        "compiled_pulses_sample": compiled_pulses[:48],
        "physical_firewall": (
            "The D4 square subgroup is compiled as native square-pulse routing. "
            "The remaining S4 actions are analyzer/ABI relabel actions: they are "
            "finite pulse schedules, not a calibrated optical switch-loss model."
        ),
        "interpretation": (
            "The row symmetries now touch the physical holonet interfaces.  A row "
            "action selects a BT1411 detector slot, hands that slot to the BT1374 "
            "mirror residue, and occupies the matching BT1407 Hesse epilogue lane "
            "for its C3 channel and row-value slot."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1493,
                "verified": result["verified"],
                "compiled_row_pulses": len(compiled_pulses),
                "native_d4_row_pulses": level_counts["native_d4_square_pulse"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
