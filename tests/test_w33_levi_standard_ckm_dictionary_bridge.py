from __future__ import annotations

from exploration.w33_levi_standard_ckm_dictionary_bridge import build_summary


def test_levi_standard_ckm_dictionary_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_standard_ckm_dictionary_theorem"]
    dictionary = summary["levi_standard_ckm_dictionary"]

    assert theorem["the_branch_filtered_Cabibbo_parameter_is_exactly_q_squared_over_v"] is True
    assert theorem["the_Wolfenstein_A_squared_parameter_is_exactly_20_squared_over_q_six_times_53_over_43"] is True
    assert theorem["the_unitarity_triangle_radius_Ru_is_exactly_q_squared_k_over_5_times_53"] is True
    assert theorem["the_CKM_phase_tangent_squared_is_exactly_2_to_8_times_5_over_q_to_5"] is True
    assert theorem["the_gamma_phase_squares_are_exactly_the_packet_split_q5_over_q5_plus_2_to_8_5_and_2_to_8_5_over_q5_plus_2_to_8_5"] is True
    assert theorem["the_standard_Vcb_scale_is_exactly_q_squared_53_over_2_to_8_5_squared_43"] is True
    assert theorem["the_standard_Vub_scale_is_exactly_lambda_squared_times_Ru_squared_times_Vcb_squared"] is True
    assert theorem["the_standard_CKM_packet_lambda_A_Ru_gamma_is_already_closed_inside_the_old_W33_count_dictionary"] is True

    assert dictionary["lambda"]["exact"] == "9/40"
    assert dictionary["R_u"]["exact"] == "108/265"
    assert dictionary["tan2_gamma"]["exact"] == "1280/243"
    assert dictionary["cos2_gamma"]["exact"] == "243/1523"
    assert dictionary["sin2_gamma"]["exact"] == "1280/1523"
