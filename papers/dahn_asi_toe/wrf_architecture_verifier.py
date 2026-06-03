#!/usr/bin/env python3
"""Verify the key numerical claims in witting_architecture_v2.tex.

The script intentionally checks only architecture-paper claims: Atlas density,
CSS storage budget, WRF control-plane constants, 70M TPS throughput identities,
the 70B model frame estimate, and the bounded flow-cell harness claims cited
in the architecture edition.
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import ceil, log2
from pathlib import Path


def ceil_fraction(value: Fraction) -> int:
    return (value.numerator + value.denominator - 1) // value.denominator


def main() -> None:
    q = 3
    mu = 4
    valency = 12
    vertices = 40
    edges = 240
    directed_edges = 2 * edges
    aut_order = 51_840
    conjugacy_classes = 30
    normalizer = 1_296
    atlas_pages = 48
    atlas_bytes_per_page = 256
    atlas_rclasses = 96
    atlas_frame_bytes = atlas_pages * atlas_bytes_per_page
    tps = 70_000_000
    model_params = 70_000_000_000

    atlas_density = Fraction(atlas_rclasses, atlas_bytes_per_page)
    chiral_density = Fraction(15, vertices)
    css_rate = Fraction(q ** (q + 1), edges)
    protection_gap = atlas_density - css_rate
    raw_payload_bytes = atlas_frame_bytes * atlas_density
    css_payload_bytes = atlas_frame_bytes * css_rate

    four_bit_weight_bytes = model_params // 2
    eight_bit_weight_bytes = model_params
    raw_frames_4bit = ceil_fraction(Fraction(four_bit_weight_bytes, raw_payload_bytes))
    css_frames_4bit = ceil_fraction(Fraction(four_bit_weight_bytes, css_payload_bytes))
    css_frames_8bit = ceil_fraction(Fraction(eight_bit_weight_bytes, css_payload_bytes))

    assert atlas_frame_bytes == 12_288
    assert atlas_density == Fraction(3, 8)
    assert chiral_density == Fraction(3, 8)
    assert css_rate == Fraction(27, 80)
    assert protection_gap == Fraction(3, 80)
    assert raw_payload_bytes == 4_608
    assert css_payload_bytes == Fraction(20_736, 5)
    assert vertices**6 == 4_096_000_000
    assert directed_edges == 480
    assert aut_order == vertices * normalizer
    assert aut_order // conjugacy_classes == 1_728
    assert valency - 1 == 11
    assert edges * 7**3 == 82_320

    handle_residual_bits = 64 - log2(vertices * normalizer)
    assert 48.33 < handle_residual_bits < 48.34

    throughput = {
        "substrate_cycles_per_second": tps * 1_728,
        "logical_qutrit_ops_per_second": tps * css_rate,
        "atlas_frames_per_second": Fraction(tps * edges, atlas_frame_bytes),
        "coherence_blocks_per_second": Fraction(tps, 384),
        "ecc_syndromes_per_second": tps * edges // mu,
    }
    assert throughput["substrate_cycles_per_second"] == 120_960_000_000
    assert throughput["logical_qutrit_ops_per_second"] == 23_625_000
    assert throughput["atlas_frames_per_second"] == Fraction(10_937_500, 8)
    assert throughput["coherence_blocks_per_second"] == Fraction(2_187_500, 12)
    assert throughput["ecc_syndromes_per_second"] == 4_200_000_000
    assert raw_frames_4bit == 7_595_487
    assert css_frames_4bit == 8_439_430
    assert css_frames_8bit == 16_878_859

    here = Path(__file__).resolve().parent
    paper = here.joinpath("witting_architecture_v2.tex").read_text(encoding="utf-8")
    bt110 = json.loads(here.joinpath("wrf_bt110_bt111_results.json").read_text(encoding="utf-8"))
    bt112 = json.loads(here.joinpath("wrf_bt112_results.json").read_text(encoding="utf-8"))
    bt113 = json.loads(here.joinpath("wrf_bt113_flow_registers_results.json").read_text(encoding="utf-8"))

    assert max(row["max"] for row in bt110["write_protocol"].values()) == 37
    assert all(row["forward_preserve_500trials"] == 1.0 for row in bt110["noise_model"].values())
    assert bt110["lattice_4cell"]["zero_cross_talk"] is True
    assert bt110["capacity"]["total_distinct_cids"] == 1_138
    assert len(bt110["capacity"]["six_attractor_seeds"]) == 3
    assert bt110["hamming"]["min"] == 18
    assert bt110["hamming"]["error_correction_t"] == 9
    assert all(row["verified"] is True for row in bt110["spectral_trace_tower"].values())

    assert bt112["bt112a_tr_A8"]["tr_A8"] == 430_970_880
    assert bt112["bt112a_tr_A8"]["verified"] is True
    assert bt112["bt112a_tr_A8"]["residual_value"] == 1_067_520
    assert bt112["bt112d_shannon"]["M_observed"] == 1_138
    assert bt112["bt112e_seed661_base6"]["num_symbols"] == 6
    assert bt112["bt112e_seed661_base6"]["all_write_latencies_under_7"] is True
    assert bt112["bt112f_3x3_lattice"]["cross_talk_events"] == 0
    assert bt112["bt112f_3x3_lattice"]["center_to_center_lock_prob"] == 0.98
    assert bt113["bt113a_ihara_and_spectral_identities"]["ihara_inverse_degree"] == 480
    assert bt113["bt113a_ihara_and_spectral_identities"]["newton_e2_equals_negative_edges"] is True
    assert bt113["bt113a_ihara_and_spectral_identities"]["product_3_minus_E8_cartan_equals_25"] is True
    assert bt113["bt113_summary"]["all_registers_are_base6"] is True
    assert bt113["bt113_summary"]["all_target_writes_reachable"] is True
    assert bt113["bt113_summary"]["global_max_target_write_steps"] == 3
    assert bt113["bt113_summary"]["all_phase_reads_invariant"] is True
    assert bt113["bt113_summary"]["global_max_controlled_repair_steps"] == 3
    assert bt113["bt113_summary"]["passive_off_rule_preserve_rates"] == [0.175926, 0.286957, 0.188571]
    assert bt113["bt113c_three_register_composition"]["all_18_symbol_cids_distinct"] is True
    assert bt113["bt113c_three_register_composition"]["min_24hex_distance_across_18_symbols"] == 19

    required_phrases = [
        "The Witting Reference Fabric",
        "$81/240 = 27/80$",
        "$3/80$ gap",
        "$82{,}320$",
        "$8.44\\times 10^6$ CSS-budgeted Atlas frames",
        "referenceable flow cell",
        "$37$ deterministic steps",
        "$3$ legal",
        "$24$-hex-character distance $19$",
        "$(1-u^2)^{200}(1-12u+11u^2)(1-2u+11u^2)^{24}(1+4u+11u^2)^{15}",
        "$1{,}138$ distinct $24$-hex-character flow CIDs",
        "not a ToE paper",
    ]
    forbidden_phrases = [
        "Witting Architecture is",
        "W-Arch",
        "Blake3 provides post-quantum collision resistance",
        "Aggregate miss rate is \\textbf{zero by construction}",
        "\\sim 460$ Atlas",
        "Logical-error rate   & $\\sim 3^{-256}",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in paper]
    forbidden = [phrase for phrase in forbidden_phrases if phrase in paper]
    assert not missing, {"missing": missing}
    assert not forbidden, {"forbidden": forbidden}

    report = {
        "atlas": {
            "frame_bytes": atlas_frame_bytes,
            "density": str(atlas_density),
            "raw_payload_bytes": int(raw_payload_bytes),
            "css_rate": str(css_rate),
            "css_payload_bytes": float(css_payload_bytes),
            "protection_gap": str(protection_gap),
        },
        "control_plane": {
            "vertices": vertices,
            "edges": edges,
            "directed_edges": directed_edges,
            "automorphism_order": aut_order,
            "instruction_families": conjugacy_classes,
            "branching_factor": valency - 1,
            "level_6_nodes": vertices**6,
            "protected_lift_length": edges * 7**3,
            "handle_residual_bits": round(handle_residual_bits, 3),
        },
        "throughput": {
            key: float(value) if isinstance(value, Fraction) else value
            for key, value in throughput.items()
        },
        "70b_model_frames": {
            "four_bit_raw_atlas_frames": raw_frames_4bit,
            "four_bit_css_budgeted_frames": css_frames_4bit,
            "eight_bit_css_budgeted_frames": css_frames_8bit,
        },
        "flow_cell_harness": {
            "global_max_transient_steps": max(row["max"] for row in bt110["write_protocol"].values()),
            "distinct_cids_500_seed_survey": bt110["capacity"]["total_distinct_cids"],
            "six_attractor_seed_count": len(bt110["capacity"]["six_attractor_seeds"]),
            "sampled_min_24hex_hamming": bt110["hamming"]["min"],
            "sampled_symbolic_correction_t": bt110["hamming"]["error_correction_t"],
            "bt112_tr_A8": bt112["bt112a_tr_A8"]["tr_A8"],
            "bt112_3x3_cross_talk_events": bt112["bt112f_3x3_lattice"]["cross_talk_events"],
            "bt113_target_write_steps": bt113["bt113_summary"]["global_max_target_write_steps"],
            "bt113_controlled_repair_steps": bt113["bt113_summary"]["global_max_controlled_repair_steps"],
            "bt113_three_register_min_cid_distance": bt113["bt113c_three_register_composition"]["min_24hex_distance_across_18_symbols"],
        },
        "latex_scan": "passed",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
