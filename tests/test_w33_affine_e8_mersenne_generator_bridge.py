from __future__ import annotations

from exploration.w33_affine_e8_mersenne_generator_bridge import build_summary


def test_affine_e8_mersenne_generator_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_mersenne_generator_theorem"]
    canonical = summary["affine_e8_mersenne_generator_dictionary"]["canonical_generators"]

    assert theorem["the_E8_packet_248_has_canonical_generator_8_times_31_from_m16"] is True
    assert theorem["the_Heawood_packet_336_has_canonical_generator_48_times_7_from_m20"] is True
    assert theorem["the_full_480_packet_has_canonical_generator_32_times_15_from_m24"] is True
    assert theorem["the_qE_720_packet_has_canonical_generator_48_times_15_from_m40"] is True
    assert theorem["the_A26_728_packet_has_canonical_generator_104_times_7_from_m36"] is True
    assert theorem["the_promoted_affine_shell_hierarchy_248_336_480_720_728_is_generated_by_low_odd_cores_1_3_5_9_and_low_Mersenne_multipliers_7_15_31"] is True
    assert theorem["the_base_packet_48_generates_both_336_and_720_under_the_Mersenne_steps_7_and_15"] is True

    assert canonical["248"]["m"] == 16
    assert canonical["336"]["m"] == 20
    assert canonical["480"]["m"] == 24
    assert canonical["720"]["m"] == 40
    assert canonical["728"]["m"] == 36
