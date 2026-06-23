#!/usr/bin/env python3
"""BT1594: overlay the Hesse/T non-Clifford port on the OAM witness loop."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1594_hesse_t_universality_witness_loop.json"
MD = ROOT / "analysis" / "BT1594_hesse_t_universality_witness_loop.md"


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    tomography = load_json("data/bt1592_synthetic_lab_tomography_harness.json")
    alphabet = load_json("data/bt1593_lg_mode_alphabet_selector.json")
    lane_sheet = load_json("data/bt1590_full_witness_lane_sheet_compiler.json")
    hesse_port = load_json("data/bt1403_hesse_port_eraser_lift.json")
    hesse_scope = load_json("data/bt1404_holonet_scope_microframe.json")
    contract = load_json("data/bt1377_physical_universal_computation_contract.json")

    segments = lane_sheet["counts"]["segments"]
    ticks_per_segment = lane_sheet["counts"]["ticks_per_segment"]
    total_ticks = lane_sheet["counts"]["total_ticks"]
    frames = hesse_scope["frames"]

    overlay_samples = []
    hesse_outcome_counts: Counter[int] = Counter()
    t_bit_counts: Counter[int] = Counter()
    pauli_counts: Counter[str] = Counter()
    branch_counts: Counter[str] = Counter()
    for segment_index in range(segments):
        start_tick = segment_index * ticks_per_segment
        for frame in frames:
            hesse_outcome_counts[frame["h"]] += 1
            t_bit_counts[frame["t_frame_bit"]] += 1
            pauli_counts[frame["pauli_correction"]] += 1
            branch_counts[frame["branch"]] += 1
            if len(overlay_samples) < 18 or segment_index >= segments - 2:
                overlay_samples.append(
                    {
                        "segment_index": segment_index,
                        "global_start_tick": start_tick
                        + frame["microframe_start_tick"],
                        "global_end_tick": start_tick + frame["microframe_end_tick"],
                        "hesse_outcome": frame["h"],
                        "route_trit": frame["route_trit"],
                        "phase_trit": frame["phase_trit"],
                        "branch": frame["branch"],
                        "pauli_correction": frame["pauli_correction"],
                        "t_frame_bit": frame["t_frame_bit"],
                    }
                )

    hesse_ticks_per_segment = (
        hesse_scope["timing"]["hesse_outcomes"] * hesse_scope["timing"]["word_ticks"]
    )
    checks = {
        "tomography_verified": tomography["verified"] is True,
        "alphabet_verified": alphabet["verified"] is True,
        "lane_sheet_verified": lane_sheet["verified"] is True,
        "hesse_port_verified": hesse_port["verified"] is True,
        "hesse_scope_verified": hesse_scope["verified"] is True,
        "universal_port_required_by_contract": contract["universal_port"]["required"]
        is True,
        "deterministic_kernel_not_universal_without_port": contract[
            "deterministic_kernel"
        ]["universal_without_port"]
        is False,
        "one_hesse_microframe_equals_one_witness_segment": hesse_ticks_per_segment
        == ticks_per_segment
        == 72,
        "no_tick_inflation": total_ticks == 77760,
        "all_hesse_outcomes_in_each_segment": dict(sorted(hesse_outcome_counts.items()))
        == {outcome: segments for outcome in range(9)},
        "t_frame_bit_profile": dict(sorted(t_bit_counts.items()))
        == {0: 5 * segments, 1: 4 * segments},
        "pauli_grid_balanced": set(pauli_counts.values()) == {segments}
        and len(pauli_counts) == 9,
        "eraser_branch_profile": dict(sorted(branch_counts.items()))
        == {"Omega": 3 * segments, "X Omega": 3 * segments, "Z Omega": 3 * segments},
        "sector_mode_addresses_survive": alphabet["counts"]["finite_addresses"] == 216,
        "lab_acceptance_survives": tomography["csv_ingest"]["all_rows_pass"] is True,
    }
    result = {
        "bt": 1594,
        "title": "Hesse/T universality witness loop inside the OAM holonet replay",
        "verified": all(checks.values()),
        "source_packets": {
            "tomography_harness": "data/bt1592_synthetic_lab_tomography_harness.json",
            "lg_mode_alphabet": "data/bt1593_lg_mode_alphabet_selector.json",
            "lane_sheet": "data/bt1590_full_witness_lane_sheet_compiler.json",
            "hesse_port": "data/bt1403_hesse_port_eraser_lift.json",
            "hesse_scope": "data/bt1404_holonet_scope_microframe.json",
            "universal_contract": "data/bt1377_physical_universal_computation_contract.json",
        },
        "overlay_identity": {
            "witness_segments": segments,
            "ticks_per_witness_segment": ticks_per_segment,
            "hesse_outcomes": hesse_scope["timing"]["hesse_outcomes"],
            "ticks_per_hesse_outcome": hesse_scope["timing"]["word_ticks"],
            "hesse_ticks_per_segment": hesse_ticks_per_segment,
            "total_ticks": total_ticks,
            "identity": "1080 segments * 72 ticks = 1080 Hesse/T microframes = 77760 ticks",
        },
        "universality_reading": {
            "finite_runtime": "BT1590 supplies the exact Clifford/OAM witness lane sheet.",
            "non_clifford_port": "BT1403/BT1404 supply the Hesse-SIC/T eraser-lift microframe.",
            "physical_test_loop": "Every 72-tick witness segment carries all nine Hesse outcomes as 9*8 ticks.",
            "claim_firewall": "The overlay tests ABI compatibility of the port; it does not prove physical Hesse optics or magic-state yield.",
        },
        "hesse_outcome_counts": dict(sorted(hesse_outcome_counts.items())),
        "t_frame_bit_counts": dict(sorted(t_bit_counts.items())),
        "pauli_correction_counts": dict(sorted(pauli_counts.items())),
        "eraser_branch_counts": dict(sorted(branch_counts.items())),
        "overlay_samples": overlay_samples,
        "interpretation": (
            "BT1594 closes the architecture loop: the exact OAM witness segment and "
            "the Hesse/T non-Clifford port have the same 72-tick shape. Universality "
            "can therefore be checked as an in-place port overlay across the same "
            "77760-tick leakage/covariance witness replay, rather than as a separate "
            "side schedule."
        ),
        "honesty_boundary": (
            "This proves schedule and ABI compatibility for the non-Clifford port inside "
            "the witness loop. Physical Hesse-SIC optics, injection fidelity, and fault "
            "tolerant magic-state yield remain explicit downstream requirements."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1594 Hesse/T Universality Witness Loop\n\n"
        "BT1594 overlays the BT1404 Hesse/T microframe on every BT1590 witness segment. "
        "Because both have the same `72`-tick shape, the non-Clifford port is tested "
        "inside the existing `77760`-tick leakage/covariance replay with no tick inflation. "
        "Each of the nine Hesse outcomes appears once per segment, giving `1080` uses of "
        "each outcome and the T-frame profile `0:5400, 1:4320`.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1594,
                "verified": result["verified"],
                "segments": segments,
                "ticks": total_ticks,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
