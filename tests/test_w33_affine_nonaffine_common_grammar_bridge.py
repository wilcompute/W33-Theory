from __future__ import annotations

from exploration.w33_affine_nonaffine_common_grammar_bridge import build_summary


def test_affine_nonaffine_common_grammar_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_nonaffine_common_grammar_theorem"]
    rows = summary["affine_nonaffine_common_grammar_dictionary"]["grammar_rows"]

    assert theorem["mu_squared_is_the_exact_common_dirac_core_16"] is True
    assert theorem["mu_times_mu_plus_1_is_the_exact_4d_algebraic_curvature_shell_20"] is True
    assert theorem["mu_times_2q_is_the_exact_corrected_24_packet"] is True
    assert theorem["mu_times_q_squared_is_the_exact_spread_carrier_36"] is True
    assert theorem["mu_times_Theta_is_the_exact_point_carrier_40"] is True
    assert theorem["the_affine_mu_input_grammar_is_exactly_the_nonaffine_packet_ladder_16_20_24_36_40"] is True
    assert theorem["the_shared_input_grammar_maps_under_the_affine_divisor_kernel_to_248_336_480_728_720"] is True
    assert theorem["the_promoted_affine_shell_grammar_and_the_nonaffine_operator_spine_share_one_exact_input_grammar"] is True

    assert rows["mu"]["mu_times_input"] == rows["mu"]["nonaffine_value"] == 16
    assert rows["mu_plus_1"]["mu_times_input"] == rows["mu_plus_1"]["nonaffine_value"] == 20
    assert rows["2q"]["mu_times_input"] == rows["2q"]["nonaffine_value"] == 24
    assert rows["q_squared"]["mu_times_input"] == rows["q_squared"]["nonaffine_value"] == 36
    assert rows["Theta"]["mu_times_input"] == rows["Theta"]["nonaffine_value"] == 40

    assert rows["mu"]["affine_kernel_value"] == 248
    assert rows["mu_plus_1"]["affine_kernel_value"] == 336
    assert rows["2q"]["affine_kernel_value"] == 480
    assert rows["q_squared"]["affine_kernel_value"] == 728
    assert rows["Theta"]["affine_kernel_value"] == 720
