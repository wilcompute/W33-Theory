from __future__ import annotations

import pytest

from scripts.w33_yukawa_frontier_audit import (
    analyze,
    bott_triality_frontier_summary,
    classify_yukawa_frontier,
    finite_family_normal_form_summary,
    five_by_three_frontier_summary,
    generation_point_defect_summary,
    nonlinear_spectral_frontier_summary,
    quartic_lift_frontier_summary,
    quadratic_shadow_frontier_summary,
)


def test_frontier_packet_collapses_to_exact_five_by_three_v15() -> None:
    summary = five_by_three_frontier_summary()
    theorem = summary["yukawa_five_by_three_frontier_theorem"]
    packet = summary["frontier_packet_dictionary"]
    generation = summary["generation_algebra_packet"]

    assert summary["internal_recipe_packet"]["internal_recipe_count"] == 5
    assert summary["internal_recipe_packet"]["v4_character_orbit_labels"] == ["A", "AB", "B", "I"]
    assert generation["linear_rank"] == 3
    assert generation["enlarged_family_rank"] == 3
    assert generation["nilpotent_square_shared_exactly"] is True
    assert generation["generation_matrices_commute_exactly"] is True
    assert packet["five_times_three_packet"] == 15
    assert packet["internal_five_is_backbone_plus_v4_orbit"] == "1 + 4"
    assert packet["generation_three_is_universal_clean_pair_algebra"] == 3
    assert packet["matches_v15_count"] is True
    assert theorem["the_remaining_clean_pair_yukawa_frontier_collapses_to_an_exact_five_by_three_packet"] is True
    assert theorem["the_resulting_frontier_packet_matches_the_exact_w33_v15_count"] is True


def test_frontier_matches_exact_bott_five_tensor_triality_three() -> None:
    summary = bott_triality_frontier_summary()
    theorem = summary["bott_triality_frontier_theorem"]
    product = summary["product_dictionary"]
    triality = summary["triality_packet_origin"]["live_and_paper_zero_nonet_leakage"]

    assert product["bott_five"] == 5
    assert product["triality_three"] == 3
    assert product["product"] == 15
    assert product["frontier_packet"] == 15
    assert summary["bott_packet_origin"]["internal_five_recipe"] == "1 + 4"
    assert triality == {
        "live_positive_branch": 0.0,
        "live_conjugate_branch": 0.0,
        "paper_up": 0.0,
        "paper_down": 0.0,
    }
    assert theorem["the_internal_five_packet_is_exactly_the_old_bott_five"] is True
    assert theorem["the_generation_three_packet_is_exactly_the_old_triality_family_cp_carrier"] is True
    assert theorem["the_live_and_paper_family_packets_stay_entirely_in_triality_with_zero_color_nonet_leakage"] is True
    assert theorem["the_remaining_yukawa_frontier_is_exactly_bott_five_tensor_triality_three"] is True


def test_finite_family_side_has_exact_one_vs_two_normal_form() -> None:
    summary = finite_family_normal_form_summary()
    theorem = summary["finite_family_theorem"]
    graph = summary["a2_channel_graph"]
    normal_form = summary["generation_normal_form"]

    assert graph["distinguished_generation"] == 2
    assert graph["doublet_generations"] == [0, 1]
    assert graph["active_quartet"] == [[0, 2], [1, 2], [2, 0], [2, 1]]
    assert graph["dormant_pair"] == [[0, 1], [1, 0]]
    assert normal_form["plus_minus"] == [[1, 1, -2], [0, 1, 2], [0, 0, 1]]
    assert normal_form["minus_plus"] == [[1, -1, -2], [0, 1, -2], [0, 0, 1]]
    assert normal_form["plus_minus_nilpotent"] == [[0, 1, -2], [0, 0, 2], [0, 0, 0]]
    assert normal_form["minus_plus_nilpotent"] == [[0, -1, -2], [0, 0, -2], [0, 0, 0]]
    assert normal_form["common_square"] == [[0, 0, 2], [0, 0, 0], [0, 0, 0]]
    assert theorem["active_quartet_is_star_at_distinguished_generation"] is True
    assert theorem["dormant_pair_is_opposite_bidirectional_edge"] is True
    assert theorem["flag_basis_conjugates_generation_matrices_to_upper_unitriangular_form"] is True
    assert theorem["common_square_is_exact_central_e13_channel"] is True
    assert theorem["normal_form_is_exact_standard_upper_triangular_packet"] is True
    assert theorem["finite_family_side_has_exact_one_vs_two_normal_form"] is True


def test_first_nonlinear_packet_is_exact_quadratic_shadow() -> None:
    summary = quadratic_shadow_frontier_summary()
    theorem = summary["quadratic_shadow_theorem"]
    packet = summary["normal_form_packet"]

    assert packet["active_plus"] == [[0, 1, 0], [0, 0, 2], [0, 0, 0]]
    assert packet["active_minus"] == [[0, -1, 0], [0, 0, -2], [0, 0, 0]]
    assert packet["central_shadow"] == [[0, 0, 2], [0, 0, 0], [0, 0, 0]]
    assert packet["plus_minus_nilpotent"] == [[0, 1, -2], [0, 0, 2], [0, 0, 0]]
    assert packet["minus_plus_nilpotent"] == [[0, -1, -2], [0, 0, -2], [0, 0, 0]]
    assert theorem["active_plus_squares_to_central_shadow"] is True
    assert theorem["active_minus_squares_to_central_shadow"] is True
    assert theorem["central_shadow_is_simple_root_commutator"] is True
    assert theorem["universal_nilpotents_are_active_minus_central_shadow"] is True
    assert theorem["central_shadow_equals_common_square_from_family_normal_form"] is True
    assert theorem["first_nonlinear_family_packet_is_quadratic_shadow_of_active_packet"] is True


def test_distinguished_generation_texture_is_single_point_defect_packet() -> None:
    summary = generation_point_defect_summary()
    theorem = summary["generation_point_defect_theorem"]
    basis = summary["family_basis_in_cycle_model"]
    h2 = summary["slot_profiles"]["H_2"]
    hbar2 = summary["slot_profiles"]["Hbar_2"]
    fourier = summary["qutrit_point_defect_fourier_packet"]

    assert basis == {
        "symmetric_doublet_line": [1, 1, 1],
        "distinguished_generation_axis": [0, 2, 1],
        "doublet_difference_axis": [2, 0, 0],
    }
    assert h2["canonical_point_defect_profile"]["distinguished_generation"] == 0
    assert h2["canonical_point_defect_profile"]["point_defect_amplitude"] == pytest.approx(0.16053290838322168)
    assert h2["canonical_cycle_orbit_is_point_projector_orbit"] is True
    assert [item["distinguished_generation"] for item in h2["cycle_orbit_profiles"]] == [0, 1, 2]
    assert [item["point_defect_amplitude"] for item in h2["cycle_orbit_profiles"]] == pytest.approx(
        [0.16053290838322168, 0.16053290838322168, 0.16053290838322168]
    )
    assert hbar2["canonical_point_defect_profile"]["distinguished_generation"] == 0
    assert hbar2["canonical_point_defect_profile"]["point_defect_amplitude"] == pytest.approx(0.14785654428396075)
    assert hbar2["canonical_cycle_orbit_is_point_projector_orbit"] is True
    assert [item["distinguished_generation"] for item in hbar2["cycle_orbit_profiles"]] == [0, 1, 2]
    assert [item["point_defect_amplitude"] for item in hbar2["cycle_orbit_profiles"]] == pytest.approx(
        [0.14785654428396075, 0.14785654428396075, 0.14785654428396075]
    )
    assert fourier["point_projector_is_democratic_in_qutrit_basis"] is True
    assert theorem["doublet_difference_axis_becomes_single_generation_point_mod3"] is True
    assert theorem["distinguished_generation_axis_lands_in_augmentation_plane"] is True
    assert theorem["both_slots_have_exact_shell_plus_point_defect_form"] is True
    assert theorem["both_slots_have_exact_cyclic_point_defect_orbit"] is True
    assert theorem["point_defect_is_democratic_in_qutrit_fourier_basis"] is True
    assert theorem["distinguished_generation_texture_is_single_point_defect_packet"] is True


def test_residual_signed_packet_is_two_irreducible_d4_quartic_lifts() -> None:
    summary = quartic_lift_frontier_summary()
    theorem = summary["quartic_lift_theorem"]
    packet = summary["quartic_lift_packet"]
    records = packet["records"]

    assert packet["scaled_signed_variable"] == "x = 240 * sigma"
    assert packet["scaled_squared_variable"] == "u = x^2 = 57600 * sigma^2"
    assert packet["packet_size"] == 2
    assert records["H_2:-+"]["quartic_polynomial"] == "x**4 - 542*x**2 + 61200"
    assert records["H_2:-+"]["galois_group_label"] == "D4"
    assert records["H_2:-+"]["galois_group_order"] == 8
    assert records["Hbar_2:+-"]["quartic_polynomial"] == "x**4 - 982*x**2 + 137232"
    assert records["Hbar_2:+-"]["galois_group_label"] == "D4"
    assert records["Hbar_2:+-"]["galois_group_order"] == 8
    assert theorem["residual_active_quartics_are_exact_even_lifts_of_base_quadratic_packets"] is True
    assert theorem["both_even_lifts_are_irreducible_d4_quartics"] is True
    assert theorem["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True


def test_analysis_classifies_remaining_open_problem_as_nonlinear_spectral_packet() -> None:
    nonlinear = nonlinear_spectral_frontier_summary()
    theorem = nonlinear["nonlinear_frontier_theorem"]
    packet = nonlinear["finite_algebraic_packet"]
    summary = analyze()
    record_names = summary["frontier_record_names"]
    records = {record["name"]: record for record in classify_yukawa_frontier()}

    assert nonlinear["base_linear_l6_bottleneck"] == {
        "response_rank": 9,
        "augmented_rank": 10,
        "best_fit_residual_norm": 0.8266952645059751,
        "active_a2_modes": [],
    }
    assert nonlinear["native_nonlinear_rank_lift"]["minimal_rank_lift_seed_size"] == 2
    assert nonlinear["native_nonlinear_rank_lift"]["max_response_rank"] == 11
    assert nonlinear["native_nonlinear_rank_lift"]["max_augmented_rank"] == 12
    assert nonlinear["native_nonlinear_rank_lift"]["fan_closure_has_full_3x3_support"] is True
    assert nonlinear["native_nonlinear_rank_lift"]["fan_closure_has_isotropic_offdiag_shell"] is True
    assert nonlinear["native_nonlinear_rank_lift"]["no_exact_closure_in_unit_a2_seed_family"] is True

    assert packet["gram_denominator"] == 57600
    assert packet["shared_phi3_mode_numerator"] == 169
    assert packet["max_active_factor_degree"] == 4
    assert packet["residual_blocks"]["h2_minus_plus"] == {
        "numerator_matrix": [[367, -55], [-55, 175]],
        "trace": 542,
        "determinant": 61200,
        "discriminant": 48964,
        "squared_spectrum": [
            "271/57600 - sqrt(12241)/57600",
            "sqrt(12241)/57600 + 271/57600",
        ],
        "spectral_formula": "(542 +/- sqrt(48964)) / 115200",
    }
    assert packet["residual_blocks"]["hbar2_plus_minus"] == {
        "numerator_matrix": [[323, 275], [275, 659]],
        "trace": 982,
        "determinant": 137232,
        "discriminant": 415396,
        "squared_spectrum": [
            "491/57600 - sqrt(103849)/57600",
            "sqrt(103849)/57600 + 491/57600",
        ],
        "spectral_formula": "(982 +/- sqrt(415396)) / 115200",
    }
    assert theorem["diagonal_l6_bottleneck_is_9_to_10"] is True
    assert theorem["native_mixed_seed_lift_reaches_11_to_12"] is True
    assert theorem["remaining_base_packet_is_two_radical_pairs_plus_scalar_channels"] is True
    assert theorem["remaining_active_packet_is_finite_algebraic_shell"] is True
    assert theorem["remaining_yukawa_frontier_is_nonlinear_internal_spectral_data"] is True

    assert record_names == (
        "five_by_three_frontier_packet",
        "bott_triality_packet_factorization",
        "finite_family_normal_form",
        "quadratic_shadow_packet",
        "generation_point_defect_packet",
        "quartic_lift_packet",
        "nonlinear_spectral_frontier",
    )
    assert records["quadratic_shadow_packet"]["support_level"] == "repo-exact nonlinear precursor"
    assert records["generation_point_defect_packet"]["support_level"] == "repo-exact cyclic texture classification"
    assert records["quartic_lift_packet"]["support_level"] == "repo-exact signed spectral classification"
    assert records["quartic_lift_packet"]["evidence"]["shared_quadratic_subfield_squarefree_parts"] == []
    assert records["quartic_lift_packet"]["evidence"]["quartic_root_field_compositum_degree"] == 16
    assert records["quartic_lift_packet"]["evidence"]["quartic_splitting_field_compositum_degree"] == 64
    assert records["quartic_lift_packet"]["evidence"]["quartic_splitting_field_galois_group"] == "D4 x D4"
    assert records["quartic_lift_packet"]["evidence"]["mixed_product_degree"] == 8
    assert records["quartic_lift_packet"]["evidence"]["mixed_product_squared_degree"] == 4
    assert records["quartic_lift_packet"]["evidence"]["mixed_product_squared_matches_resultant"] is True
    assert records["quartic_lift_packet"]["evidence"]["mixed_squared_common_biquadratic_field_squarefree_parts"] == [12241, 103849, 1271215609]
    assert records["quartic_lift_packet"]["evidence"]["mixed_ratio_degree"] == 8
    assert records["quartic_lift_packet"]["evidence"]["mixed_ratio_squared_degree"] == 4
    assert records["quartic_lift_packet"]["evidence"]["mixed_ratio_squared_matches_resultant"] is True
    assert records["quartic_lift_packet"]["evidence"]["mixed_squared_packets_have_v4_galois_group"] is True
    assert records["quartic_lift_packet"]["evidence"]["mixed_sum_degree"] == 16
    assert records["nonlinear_spectral_frontier"]["support_level"] == "exact frontier classification"
    assert summary["frontier_packet_summary"] == {
        "internal_recipe_count": 5,
        "generation_rank": 3,
        "frontier_packet_size": 15,
        "bott_triality_product": 15,
        "matches_v15_count": True,
    }
    assert summary["quadratic_shadow_frontier"]["quadratic_shadow_theorem"][
        "first_nonlinear_family_packet_is_quadratic_shadow_of_active_packet"
    ] is True
    assert summary["generation_point_defect"]["generation_point_defect_theorem"][
        "distinguished_generation_texture_is_single_point_defect_packet"
    ] is True
    assert summary["quartic_lift_frontier"]["quartic_lift_theorem"][
        "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"
    ] is True
    assert summary["quartic_lift_frontier"]["quartic_lift_theorem"][
        "the_two_quartic_root_fields_are_linearly_disjoint_over_q"
    ] is True
    assert summary["quartic_lift_frontier"]["quartic_lift_theorem"][
        "the_two_d4_splitting_fields_are_linearly_disjoint_over_q"
    ] is True
    assert summary["quartic_lift_frontier"]["quartic_lift_theorem"][
        "the_signed_packet_splitting_field_has_galois_group_d4_times_d4"
    ] is True
    assert summary["current_open_problem"] == {
        "kind": "relation_above_two_linearly_disjoint_d4_splitting_fields",
        "exact_open_problem_is_relation_not_support_or_shape": True,
        "max_active_factor_degree": 4,
        "remaining_base_packet_is_two_radical_pairs_plus_scalar_channels": True,
        "remaining_active_packet_is_finite_algebraic_shell": True,
        "remaining_signed_packet_is_two_d4_quartic_lifts": True,
        "quadratic_overlap_between_the_two_d4_lifts_is_trivial": True,
        "quartic_root_fields_are_linearly_disjoint_over_q": True,
        "quartic_root_field_compositum_degree": 16,
        "quartic_splitting_fields_are_linearly_disjoint_over_q": True,
        "quartic_splitting_field_compositum_degree": 64,
        "quartic_splitting_field_galois_group": "D4 x D4",
        "canonical_mixed_product_degree": 8,
        "canonical_mixed_product_squared_degree": 4,
        "canonical_mixed_product_squared_matches_resultant": True,
        "canonical_mixed_squared_common_biquadratic_field_squarefree_parts": [12241, 103849, 1271215609],
        "canonical_mixed_ratio_degree": 8,
        "canonical_mixed_ratio_squared_degree": 4,
        "canonical_mixed_ratio_squared_matches_resultant": True,
        "canonical_mixed_squared_packets_have_v4_galois_group": True,
        "canonical_mixed_sum_degree": 16,
        "canonical_mixed_product_and_ratio_are_branch_stable_irreducible_octics": True,
        "canonical_mixed_product_and_ratio_are_even_lifts_of_branch_stable_irreducible_quartics": True,
        "canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_base_quadratics": True,
        "canonical_mixed_squared_packets_are_common_v4_biquadratic_carriers": True,
        "canonical_mixed_sum_generates_quartic_root_field_compositum": True,
    }