from __future__ import annotations

from exploration.w33_affine_e8_twelfth_mode_boundary_bridge import build_summary


def test_affine_e8_twelfth_mode_boundary_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_twelfth_mode_boundary_theorem"]
    search = summary["twelfth_mode_boundary_search"]

    assert theorem["the_theta_e8_twelfth_coefficient_is_exactly_490560_equals_E_times_sigma3_k"] is True
    assert theorem["the_eta_minus_8_twelfth_excited_coefficient_is_exactly_2418710"] is True
    assert theorem["the_twelfth_mode_has_no_sparse_solution_of_the_form_a_sigma3_k_plus_b_tau_plus_c_with_a_b_c_in_the_current_packet_dictionary"] is True
    assert theorem["the_twelfth_mode_has_no_sparse_solution_of_the_form_a_sigma3_k_plus_b_tau_plus_c_times_168_plus_d_with_a_b_c_d_in_the_current_packet_dictionary"] is True
    assert theorem["the_twelfth_mode_is_the_first_one_sided_affine_boundary_on_the_current_exact_w33_spine"] is True

    assert search["sigma_tau_plus_packet_solutions"] == []
    assert search["sigma_tau_dual_plus_packet_solutions"] == []
