from __future__ import annotations

from exploration.w33_affine_e8_kernel_generator_bridge import build_summary


def test_affine_e8_kernel_generator_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_kernel_generator_theorem"]
    hits = summary["affine_e8_kernel_generator_dictionary"]["selected_hits"]

    assert theorem["the_divisor_kernel_hits_the_E8_adjoint_packet_exactly_at_m16"] is True
    assert theorem["the_divisor_kernel_hits_the_full_Heawood_shell_exactly_at_m20"] is True
    assert theorem["the_divisor_kernel_hits_the_promoted_480_shell_exactly_at_m24"] is True
    assert theorem["the_divisor_kernel_hits_the_A26_ambient_shell_exactly_at_m36"] is True
    assert theorem["the_divisor_kernel_hits_the_qE_shell_exactly_at_m40"] is True
    assert theorem["the_selected_hits_all_obey_the_exact_odd_core_dyadic_generator_formula"] is True
    assert theorem["the_promoted_even_shell_hierarchy_248_336_480_728_720_is_generated_inside_the_affine_divisor_kernel_by_the_low_odd_cores_1_3_5_9"] is True

    assert hits["16"]["value"] == 248
    assert hits["20"]["value"] == 336
    assert hits["24"]["value"] == 480
    assert hits["36"]["value"] == 728
    assert hits["40"]["value"] == 720
