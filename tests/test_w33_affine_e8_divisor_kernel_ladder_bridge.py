from __future__ import annotations

from exploration.w33_affine_e8_divisor_kernel_ladder_bridge import build_summary


def test_affine_e8_divisor_kernel_ladder_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_divisor_kernel_theorem"]
    kernel = summary["affine_e8_divisor_kernel_dictionary"]

    assert theorem["the_first_24_recurrence_kernel_weights_all_land_on_the_promoted_or_composite_packet_dictionary"] is True
    assert theorem["the_exact_dyadic_formula_8_sigma1_u_2_r_equals_8_sigma1_u_times_2_to_r_plus_1_minus_1_holds_for_every_channel_m_le_24"] is True
    assert theorem["the_pure_dyadic_ladder_is_exactly_8_24_56_120_248"] is True
    assert theorem["the_3_times_2_to_r_ladder_is_exactly_32_96_224_480"] is True
    assert theorem["the_5_times_2_to_r_ladder_is_exactly_48_144_336"] is True
    assert theorem["the_full_odd_core_split_up_to_24_is_exactly_1_3_5_7_9_11_13_15_17_19_21_23"] is True
    assert theorem["the_post_q11_cumulative_regime_is_driven_by_an_exact_divisor_kernel_packet_ladder_not_by_arbitrary_partition_weights"] is True

    assert kernel["odd_core_ladders"]["1"] == [8, 24, 56, 120, 248]
    assert kernel["odd_core_ladders"]["3"] == [32, 96, 224, 480]
    assert kernel["odd_core_ladders"]["5"] == [48, 144, 336]
    assert kernel["composite_packet_values"] == [160, 256]
