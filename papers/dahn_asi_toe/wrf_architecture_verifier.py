#!/usr/bin/env python3
"""Verify the key numerical claims in witting_architecture_v2.tex.

The script intentionally checks only architecture-paper claims: Atlas density,
CSS storage budget, WRF control-plane constants, 70M TPS throughput identities,
and the 70B model frame estimate.
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

    paper = Path(__file__).with_name("witting_architecture_v2.tex").read_text(encoding="utf-8")
    required_phrases = [
        "The Witting Reference Fabric",
        "$81/240 = 27/80$",
        "$3/80$ gap",
        "$82{,}320$",
        "$8.44\\times 10^6$ CSS-budgeted Atlas frames",
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
        "latex_scan": "passed",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
