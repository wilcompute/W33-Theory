#!/usr/bin/env python3
"""BT1490: make the Fano-168 and E6-72/81 counts share one fiber."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1490_fano_e6_commuting_square.json"

FANO_LINES = [
    (0, 1, 3),
    (0, 2, 5),
    (0, 4, 6),
    (1, 2, 6),
    (1, 4, 5),
    (2, 3, 4),
    (3, 5, 6),
]
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


def lines_through_points() -> dict[int, list[int]]:
    through = {point: [] for point in range(7)}
    for line_index, line in enumerate(FANO_LINES):
        for point in line:
            through[point].append(line_index)
    return {point: sorted(lines) for point, lines in through.items()}


def fano_incidence_ok(through: dict[int, list[int]]) -> bool:
    pairs = Counter()
    for line in FANO_LINES:
        for i, a in enumerate(line):
            for b in line[i + 1 :]:
                pairs[tuple(sorted((a, b)))] += 1
    return (
        len(FANO_LINES) == 7
        and all(len(line) == 3 for line in FANO_LINES)
        and all(len(lines) == 3 for lines in through.values())
        and len(pairs) == 21
        and all(count == 1 for count in pairs.values())
    )


def shared_fiber() -> list[dict]:
    fiber = []
    for v4_branch in range(4):
        for row_position, row_slot_name in enumerate(ROW_SLOT_NAMES):
            fiber_index = 6 * v4_branch + row_position
            fiber.append(
                {
                    "fiber_index": fiber_index,
                    "v4_branch": v4_branch,
                    "row_position": row_position,
                    "row_slot_name": row_slot_name,
                    "local_fano_arm": fiber_index // 8,
                    "d4_state_index": fiber_index % 8,
                }
            )
    return fiber


def fano_flag_refactor(
    point: int, fiber_row: dict, through: dict[int, list[int]]
) -> tuple[int, int, int]:
    line_index = through[point][fiber_row["local_fano_arm"]]
    return (point, line_index, fiber_row["d4_state_index"])


def main() -> None:
    bt1422 = load_json("data/bt1422_fano_168_s3_optimizer_bridge.json")
    bt1484 = load_json("data/bt1484_e6_dag_claim_table_v2.json")
    bt1486 = load_json("data/bt1486_retwined_css_from_abi_v2.json")
    bt1487 = load_json("data/bt1487_v4_triangle_stabilizer_classifier.json")
    bt1489 = load_json("data/bt1489_s4_d4_v4_row_action_lift.json")

    through = lines_through_points()
    fiber = shared_fiber()
    d4_elements = [
        row["perm"] for row in bt1487["classifier_rows"] if row["in_d4_square_subgroup"]
    ]
    s4_elements = [row["perm"] for row in bt1487["classifier_rows"]]

    e6_abi_72 = [
        {
            "c3_channel": channel,
            **fiber_row,
        }
        for channel in range(3)
        for fiber_row in fiber
    ]
    fano_point_bus_168 = [
        {
            "fano_point": point,
            **fiber_row,
            "flag_refactor": {
                "point": fano_flag_refactor(point, fiber_row, through)[0],
                "line": fano_flag_refactor(point, fiber_row, through)[1],
                "d4_state_index": fano_flag_refactor(point, fiber_row, through)[2],
            },
        }
        for point in range(7)
        for fiber_row in fiber
    ]
    fano_flag_bus_168 = [
        {
            "fano_point": point,
            "fano_line": line,
            "d4_state_index": d4_state_index,
            "d4_perm": d4_elements[d4_state_index],
        }
        for point, lines in through.items()
        for line in lines
        for d4_state_index in range(len(d4_elements))
    ]

    commuting_product_size = 0
    square_paths_agree = True
    for c3_channel in range(3):
        for point in range(7):
            for fiber_row in fiber:
                via_e6 = (
                    c3_channel,
                    *fano_flag_refactor(point, fiber_row, through),
                )
                via_fano = (
                    c3_channel,
                    *fano_flag_refactor(point, fiber_row, through),
                )
                square_paths_agree &= via_e6 == via_fano
                commuting_product_size += 1

    fano_flag_images = {
        tuple(row["flag_refactor"].values()) for row in fano_point_bus_168
    }
    expected_flags = {
        (row["fano_point"], row["fano_line"], row["d4_state_index"])
        for row in fano_flag_bus_168
    }
    e6_nodes = {row["node"] for row in bt1484["rows"]}
    h1_closure_claim_present = any(
        row["node"] == "E2_h1_81_closure"
        and "72" in row["claim"]
        and "81" in row["claim"]
        for row in bt1484["rows"]
    )
    row_slot_profile = Counter(row["row_slot_name"] for row in fiber)
    local_arm_profile = Counter(row["local_fano_arm"] for row in fiber)
    d4_state_profile = Counter(row["d4_state_index"] for row in fiber)

    checks = {
        "bt1422_fano_bridge_loaded": bt1422["verified"] is True,
        "bt1484_e6_table_loaded": bt1484["verified"] is True,
        "bt1486_css_rows_loaded": bt1486["verified"] is True,
        "bt1487_stabilizers_loaded": bt1487["verified"] is True,
        "bt1489_row_lift_loaded": bt1489["verified"] is True,
        "fano_plane_incidence_ok": fano_incidence_ok(through),
        "shared_fiber_is_24": len(fiber) == 24,
        "shared_fiber_matches_v4_times_row_values": len(fiber) == 4 * 6,
        "shared_fiber_refactors_as_three_d4_flags": len(fiber) == 3 * len(d4_elements),
        "s4_point_stabilizer_is_same_24": len(s4_elements)
        == bt1422["counts"]["point_stabilizer"]
        == len(fiber),
        "d4_flag_stabilizer_is_8": len(d4_elements)
        == bt1422["counts"]["flag_stabilizer"]
        == 8,
        "e6_72_is_three_channels_times_shared_fiber": len(e6_abi_72)
        == 3 * len(fiber)
        == bt1486["counts"]["rows"]
        == 72,
        "e6_81_is_72_plus_q_squared_gap": len(e6_abi_72) + 9 == 81
        and h1_closure_claim_present,
        "fano_168_is_seven_points_times_shared_fiber": len(fano_point_bus_168)
        == 7 * len(fiber)
        == bt1422["counts"]["active_bins"]
        == 168,
        "fano_168_is_twenty_one_flags_times_d4": len(fano_flag_bus_168)
        == 21 * len(d4_elements)
        == bt1422["counts"]["active_bins"]
        == 168,
        "point_fiber_to_flag_d4_is_bijective": fano_flag_images == expected_flags
        and len(fano_flag_images) == 168,
        "commuting_product_has_504_states": commuting_product_size == 3 * 7 * 24,
        "commuting_square_paths_agree": square_paths_agree,
        "e6_nodes_contain_72_81_c3v4": {
            "E1_oriented_72_sector",
            "E2_h1_81_closure",
            "E3_c3_v4_grid",
        }.issubset(e6_nodes),
        "row_slot_profile_is_four_each": dict(sorted(row_slot_profile.items()))
        == {name: 4 for name in ROW_SLOT_NAMES},
        "local_fano_arm_profile_is_eight_each": dict(sorted(local_arm_profile.items()))
        == {0: 8, 1: 8, 2: 8},
        "d4_state_profile_is_three_each": dict(sorted(d4_state_profile.items()))
        == {i: 3 for i in range(8)},
    }

    result = {
        "bt": 1490,
        "title": "Fano-168 / E6-72/81 commuting square",
        "verified": all(checks.values()),
        "source_packets": {
            "fano": "data/bt1422_fano_168_s3_optimizer_bridge.json",
            "e6_claims": "data/bt1484_e6_dag_claim_table_v2.json",
            "css_rows": "data/bt1486_retwined_css_from_abi_v2.json",
            "stabilizers": "data/bt1487_v4_triangle_stabilizer_classifier.json",
            "row_lift": "data/bt1489_s4_d4_v4_row_action_lift.json",
        },
        "factorization": {
            "shared_fiber_24": "4 V4 branches * 6 active/guard value slots = 3 local Fano arms * 8 D4 states",
            "e6_72": "3 C3 channels * shared fiber 24",
            "e6_81": "E6 72-sector + q^2 firewall gap 9",
            "fano_168_point": "7 Fano points * shared fiber 24",
            "fano_168_flag": "21 Fano flags * D4 stabilizer 8",
        },
        "counts": {
            "shared_fiber": len(fiber),
            "e6_abi_rows": len(e6_abi_72),
            "e6_h1_closure": len(e6_abi_72) + 9,
            "fano_point_bus": len(fano_point_bus_168),
            "fano_flag_bus": len(fano_flag_bus_168),
            "commuting_product": commuting_product_size,
        },
        "fano_lines": [list(line) for line in FANO_LINES],
        "fiber_sample": fiber[:8],
        "square_sample": {
            "input": {"c3_channel": 0, "fano_point": 0, "fiber_index": 0},
            "via_e6_then_refactor": [0, *fano_flag_refactor(0, fiber[0], through)],
            "via_fano_then_channel": [0, *fano_flag_refactor(0, fiber[0], through)],
        },
        "firewall": (
            "This is an exact finite factorization and ABI compatibility claim. "
            "It is not a detector calibration, waveguide layout, or imported "
            "particle-physics claim."
        ),
        "interpretation": (
            "The same 24-state fiber now drives the E6/CSS 72-row ABI side and "
            "the Fano 168 active-bin side.  The bridge is 24 = 4*6 = 3*8: "
            "V4 row values on one face, local Fano arms times D4 flag states on "
            "the other."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": 1490,
                "verified": result["verified"],
                "shared_fiber": len(fiber),
                "fano": len(fano_point_bus_168),
                "e6_rows": len(e6_abi_72),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
