#!/usr/bin/env python3
"""BT1366: grade the 2160 D12 atlas by the BT1363 local clock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1366_global_2160_d12_clock_grading.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_result() -> dict[str, object]:
    bt1363 = load_json(ROOT / "data" / "bt1363_q4_clock_tomotope_medial_descent.json")
    bt815 = load_json(ROOT / "data" / "bt815_global_2160_transversal_gset.json")

    geography = 45
    local_middle_blocks = 48
    global_slots = geography * local_middle_blocks
    pure_c4_local_cycles = len(bt1363["pure_c4_clock"]["middle_block_orbit_profile"])
    pure_c4_cycle_size = bt1363["pure_c4_clock"]["middle_block_orbit_profile"][0]
    descended_local_sheets = len(
        bt1363["descended_clock"]["middle_block_orbit_profile"]
    )
    descended_sheet_size = bt1363["descended_clock"]["middle_block_orbit_profile"][0]

    chart_count_from_clock = geography * pure_c4_local_cycles
    slots_from_chart_cycles = chart_count_from_clock * pure_c4_cycle_size
    descended_global_orbits = geography * descended_local_sheets
    slots_from_descended_sheets = descended_global_orbits * descended_sheet_size

    checks = {
        "bt815_slots_are_2160": bt815["slot_counts"]["chart_transversal_slots"] == 2160,
        "global_product_is_45_times_48": global_slots == 2160,
        "pure_c4_cycles_make_540_charts": chart_count_from_clock
        == bt815["slot_counts"]["charts"]
        == 540,
        "four_ticks_per_chart_match_bt815": pure_c4_cycle_size == 4
        and bt815["slot_counts"]["slots_per_chart"] == [4],
        "chart_cycles_recover_all_slots": slots_from_chart_cycles == 2160,
        "descended_clock_gives_135_sixteen_slot_orbits": descended_global_orbits == 135
        and descended_sheet_size == 16,
        "descended_sheets_recover_all_slots": slots_from_descended_sheets == 2160,
        "three_phase_geographies": descended_global_orbits == geography * 3,
        "d12_boundary_preserved": bt815["stabilizer"]["gap_witness"]["structure"]
        == "D12"
        and bt815["comparison"]["BT778_rectangle_slots"].startswith(
            "same cardinality 2160 but cyclic C12"
        ),
    }

    return {
        "bt": 1366,
        "title": "Global 2160 D12 clock grading",
        "verified": all(checks.values()),
        "inputs": {
            "bt1363_local_middle_blocks": local_middle_blocks,
            "bt815_slots": bt815["slot_counts"]["chart_transversal_slots"],
            "polar_pair_geography": geography,
        },
        "grading": {
            "identity": "2160 = 45 * 48 = 45 * 12 * 4 = 45 * 3 * 16",
            "chart_count_from_clock": chart_count_from_clock,
            "slots_per_chart_from_c4": pure_c4_cycle_size,
            "descended_global_orbits": descended_global_orbits,
            "descended_global_orbit_size": descended_sheet_size,
        },
        "d12_boundary": {
            "bt815_stabilizer": bt815["stabilizer"]["gap_witness"],
            "meaning": "BT1366 grades the D12 mirror atlas; it does not replace D12 by the local C4 clock.",
        },
        "interpretation": (
            "The local BT1363 clock explains the BT815 global atlas factorization. "
            "The twelve local C4 four-tick cycles, crossed with the 45 polar-pair "
            "geographies, are the 540 charts; each chart contributes four D12 "
            "mirror slots.  Equivalently, the three local ternary sheets crossed "
            "with the same 45 geographies give 135 global 16-slot phase orbits."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "identity": result["grading"]["identity"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
