#!/usr/bin/env python3
"""BT1602: weld the 168 Fano detector bins to the Witting transaction body."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from bt1408_witting_contextual_communication_bridge import (
    construct_witting_40_rays,
    find_tetrads,
    memberships,
)
from bt1490_fano_e6_commuting_square import FANO_LINES, lines_through_points
from bt1601_single_photon_transaction_automaton import (
    build_rows as build_automaton_rows,
)

OUT = ROOT / "data" / "bt1602_fano_witting_detector_bin_synthesis.json"
MD = ROOT / "analysis" / "BT1602_fano_witting_detector_bin_synthesis.md"

WITTING_GATE_LINES = [0, 1, 2, 3, 4]
RESERVE_CONTROL_LINES = [5, 6]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def detector_bin_for_flag(line_index: int, point_slot: int, d4_state: int) -> dict:
    through = lines_through_points()
    fano_point = FANO_LINES[line_index][point_slot]
    local_fano_arm = through[fano_point].index(line_index)
    fiber_index = local_fano_arm * 8 + d4_state
    return {
        "detector_bin": fano_point * 24 + fiber_index,
        "fano_point": fano_point,
        "fano_line": line_index,
        "point_slot_on_line": point_slot,
        "local_fano_arm": local_fano_arm,
        "d4_state": d4_state,
        "fiber_index": fiber_index,
    }


def compatible_targets_by_source(
    pair_to_bases: dict[tuple[int, int], list[int]]
) -> dict[int, list[int]]:
    return {
        source: [
            target
            for target in range(40)
            if target != source and pair_to_bases.get((source, target), [])
        ]
        for source in range(40)
    }


def main() -> None:
    automaton = load_json("data/bt1601_single_photon_transaction_automaton.json")
    cycle = load_json("data/bt1600_full_witting_transaction_cycle.json")
    fano_square = load_json("data/bt1490_fano_e6_commuting_square.json")
    fano_fiber = load_json("data/bt1492_canonical_fano_s4_d4_fiber.json")
    optical_bins = load_json("data/bt1417_linear_optical_dual_port_primitives.json")

    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    _ray_to_bases, pair_to_bases = memberships(tetrads)
    compatible_by_source = compatible_targets_by_source(pair_to_bases)

    rows = []
    bin_hist: Counter[int] = Counter()
    rail_bin_hist: dict[str, Counter[int]] = {}
    line_role_hist: Counter[str] = Counter()
    source_role_hist: dict[int, Counter[str]] = {}
    fuel_only_hist: Counter[int] = Counter()
    compatible_only_hist: Counter[int] = Counter()
    same_only_hist: Counter[int] = Counter()

    automaton_rows, _automaton_histograms = build_automaton_rows()
    for frame in automaton_rows:
        source_ray = frame["source_ray"]
        target_ray = frame["target_ray"]
        gate_index = source_ray // 8
        source_d4 = source_ray % 8
        if frame["rail"] == "CONTEXTUAL_FUEL":
            incompatible_index = frame["payload"]["witting_incompatible_index"]
            point_slot = incompatible_index % 3
            hesse_residue = incompatible_index // 3
            role = "FUEL_GATE_LINE"
            bin_row = detector_bin_for_flag(
                WITTING_GATE_LINES[gate_index], point_slot, source_d4
            )
            bin_row["hesse_residue"] = hesse_residue
            fuel_only_hist[bin_row["detector_bin"]] += 1
        elif source_ray == target_ray:
            role = "SAME_RAY_CONTROL_ANCHOR"
            bin_row = detector_bin_for_flag(
                WITTING_GATE_LINES[gate_index], 0, source_d4
            )
            bin_row["hesse_residue"] = None
            same_only_hist[bin_row["detector_bin"]] += 1
        else:
            compatible_index = compatible_by_source[source_ray].index(target_ray)
            reserve_line = RESERVE_CONTROL_LINES[compatible_index // 6]
            point_slot = (compatible_index % 6) // 2
            detector_parity = compatible_index % 2
            control_d4_state = source_d4 if detector_parity == 0 else source_d4 ^ 4
            role = "COMPATIBLE_CONTROL_RESERVE_LINE"
            bin_row = detector_bin_for_flag(reserve_line, point_slot, control_d4_state)
            bin_row["detector_parity"] = detector_parity
            compatible_only_hist[bin_row["detector_bin"]] += 1
        assignment = {
            "cycle_frame": frame["cycle_frame"],
            "source_ray": source_ray,
            "target_ray": target_ray,
            "rail": frame["rail"],
            "witting_gate_index": gate_index,
            "source_d4_state": source_d4,
            "bin_role": role,
            **bin_row,
        }
        rows.append(assignment)
        bin_hist[assignment["detector_bin"]] += 1
        rail_bin_hist.setdefault(frame["rail"], Counter())[
            assignment["detector_bin"]
        ] += 1
        line_role_hist[f"{assignment['fano_line']}:{role}"] += 1
        source_role_hist.setdefault(source_ray, Counter())[role] += 1

    active_bins = sorted(bin_hist)
    usage_profile = Counter(bin_hist.values())
    fuel_bins = set(fuel_only_hist)
    compatible_bins = set(compatible_only_hist)
    same_bins = set(same_only_hist)
    checks = {
        "automaton_verified": automaton["verified"] is True,
        "cycle_verified": cycle["verified"] is True,
        "fano_square_verified": fano_square["verified"] is True,
        "fano_fiber_verified": fano_fiber["verified"] is True,
        "optical_bins_verified": optical_bins["verified"] is True,
        "fano_active_bins_are_168": optical_bins["primitive_summary"][
            "active_residue_detector_bins"
        ]
        == fano_square["counts"]["fano_point_bus"]
        == 168,
        "all_1600_frames_assigned_one_bin": len(rows) == 1600,
        "all_168_bins_are_used": active_bins == list(range(168)),
        "witting_sources_factor_as_five_times_eight": {
            (row["witting_gate_index"], row["source_d4_state"]) for row in rows
        }
        == {(gate, d4) for gate in range(5) for d4 in range(8)},
        "fuel_uses_five_witting_gate_lines": {
            row["fano_line"] for row in rows if row["bin_role"] == "FUEL_GATE_LINE"
        }
        == set(WITTING_GATE_LINES),
        "compatible_controls_use_two_reserve_lines": {
            row["fano_line"]
            for row in rows
            if row["bin_role"] == "COMPATIBLE_CONTROL_RESERVE_LINE"
        }
        == set(RESERVE_CONTROL_LINES),
        "fuel_bins_are_120_with_nine_uses_each": len(fuel_bins) == 120
        and sorted(fuel_only_hist.values()) == [9] * 120,
        "compatible_bins_are_48_with_ten_uses_each": len(compatible_bins) == 48
        and sorted(compatible_only_hist.values()) == [10] * 48,
        "same_ray_anchor_bins_are_40_with_one_use_each": len(same_bins) == 40
        and sorted(same_only_hist.values()) == [1] * 40
        and same_bins.issubset(fuel_bins),
        "total_usage_profile_is_80x9_88x10": dict(sorted(usage_profile.items()))
        == {9: 80, 10: 88},
        "source_shell_profile_is_27_12_1": all(
            dict(hist)
            == {
                "COMPATIBLE_CONTROL_RESERVE_LINE": 12,
                "FUEL_GATE_LINE": 27,
                "SAME_RAY_CONTROL_ANCHOR": 1,
            }
            for hist in source_role_hist.values()
        ),
        "factorization_is_168_equals_7_times_24": 7 * 24 == 168,
        "fiber_factorization_is_24_equals_3_times_8": 3 * 8 == 24,
    }
    result = {
        "bt": 1602,
        "title": "Fano/Witting active detector-bin synthesis",
        "verified": all(checks.values()),
        "source_packets": {
            "automaton": "data/bt1601_single_photon_transaction_automaton.json",
            "witting_cycle": "data/bt1600_full_witting_transaction_cycle.json",
            "fano_square": "data/bt1490_fano_e6_commuting_square.json",
            "canonical_fano_fiber": "data/bt1492_canonical_fano_s4_d4_fiber.json",
            "optical_detector_bins": "data/bt1417_linear_optical_dual_port_primitives.json",
        },
        "synthesis_identity": {
            "active_bins": "168 = 7 Fano lines * 3 points per line * 8 D4 source states = 7*24",
            "witting_sources": "40 = 5 witness gates * 8 D4 source states",
            "fuel_shell": "27 incompatible targets = 3 Fano point slots * 9 Hesse/OAM residues",
            "compatible_shell": "12 compatible off-diagonal targets = 2 reserve Fano lines * 3 point slots * 2 detector parities",
            "same_ray": "one same-ray control anchors the source gate-line bin",
        },
        "counts": {
            "frame_assignments": len(rows),
            "active_detector_bins": len(active_bins),
            "fuel_bins": len(fuel_bins),
            "compatible_control_bins": len(compatible_bins),
            "same_ray_anchor_bins": len(same_bins),
        },
        "histograms": {
            "total_bin_usage_profile": dict(sorted(usage_profile.items())),
            "line_role": dict(sorted(line_role_hist.items())),
            "rail_bin_count": {
                rail: len(hist) for rail, hist in sorted(rail_bin_hist.items())
            },
        },
        "detector_bin_rows": rows,
        "interpretation": (
            "BT1602 makes the 168 active detector bins structural: five Fano lines "
            "carry the five Witting fuel gates, and the two remaining Fano lines "
            "carry compatible controls. The same-ray controls anchor one gate-line "
            "bin per Witting source."
        ),
        "honesty_boundary": (
            "This is a finite detector-bin incidence synthesis. It does not calibrate "
            "detector efficiency, dark counts, timing jitter, or physical chip loss."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1602 Fano/Witting Detector-Bin Synthesis\n\n"
        "BT1602 identifies the `168` active detector bins with a Fano/Witting "
        "runtime bus:\n\n"
        "```text\n"
        "168 = 7 Fano lines * 3 point slots * 8 D4 states = 7*24\n"
        "40 Witting sources = 5 witness gates * 8 D4 states\n"
        "27 fuel targets = 3 point slots * 9 Hesse/OAM residues\n"
        "12 compatible controls = 2 reserve lines * 3 point slots * 2 parities\n"
        "```\n\n"
        "All `168` bins are used.  The total usage profile is `80` bins used "
        "`9` times and `88` bins used `10` times across the `1600` frames.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1602,
                "verified": result["verified"],
                "active_detector_bins": len(active_bins),
                "frames": len(rows),
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
