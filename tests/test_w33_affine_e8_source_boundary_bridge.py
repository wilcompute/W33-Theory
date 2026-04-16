from __future__ import annotations

from exploration.w33_affine_e8_source_boundary_bridge import build_summary


def test_affine_e8_source_boundary_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_source_boundary_theorem"]
    search = summary["canonical_sparse_search"]
    terms = summary["q12_recurrence_terms"]

    assert theorem["the_theta_side_obeys_the_exact_local_law_qn_theta_e8_equals_240_times_sigma3_n_for_every_n_up_to_12"] is True
    assert theorem["the_q12_theta_coefficient_is_exactly_E_times_sigma3_k_with_k_equal_12"] is True
    assert theorem["the_eta_minus_8_coefficients_obey_the_exact_colored_partition_recurrence_at_q12"] is True
    assert theorem["the_q12_partition_recurrence_has_twelve_strictly_positive_terms"] is True
    assert theorem["the_last_canonical_sparse_sigma3_k_tau_residual_closure_occurs_at_q11_as_496_sigma3_k_plus_26_tau_plus_40"] is True
    assert theorem["the_q12_oscillator_coefficient_has_no_canonical_sparse_sigma3_k_tau_residual_closure"] is True
    assert theorem["the_q12_boundary_is_exactly_local_divisor_shell_saturation_on_the_theta_side_versus_cumulative_partition_growth_on_the_oscillator_side"] is True

    assert search["q11_sigma_tau_residual_solutions"] == [(496, 26, 40)]
    assert search["q12_sigma_tau_residual_solutions"] == []
    assert len(terms) == 12
    assert all(item["term"] > 0 for item in terms)
