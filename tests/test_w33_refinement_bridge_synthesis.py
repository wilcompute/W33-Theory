from __future__ import annotations

# PASS1150_SHIFTED_ADJACENCY_RETRACTION
import pytest as _w33_retraction_pytest
pytestmark=_w33_retraction_pytest.mark.skip(reason="Legacy test depends on the retracted shifted-adjacency spectrum; Pass 1150 quarantine.")

import json
from pathlib import Path

import pytest

from w33_refinement_bridge_synthesis import (
    build_refinement_bridge_synthesis,
    write_summary,
)


def test_synthesis_keeps_the_dimension_firewall_explicit() -> None:
    summary = build_refinement_bridge_synthesis()
    assert summary["status"] == "ok"
    assert summary["bridge_firewall"]["finite_spectrum_alone_is_insufficient"] is True
    assert summary["bridge_firewall"]["explicit_cover_family_exists"] is True
    assert summary["bridge_firewall"]["tomotope_native_dimension"] == 3.0
    assert summary["bridge_firewall"]["external_refinement_dimension"] == 4.0
    assert summary["bridge_firewall"]["flat_external_scalar_curvature_term"] == 0.0


def test_synthesis_records_curved_external_candidates() -> None:
    summary = build_refinement_bridge_synthesis()
    curved = summary["curved_external_candidates"]
    assert curved["cp2_vertices"] == 9
    assert curved["cp2_euler_characteristic"] == 3
    assert curved["cp2_signature"] == 1
    assert curved["k3_vertices"] == 16
    assert curved["k3_euler_characteristic"] == 24
    assert curved["k3_signature"] == -16
    assert curved["cp2_weyl_l2_floor"] > 0.0
    assert curved["k3_weyl_l2_floor"] > curved["cp2_weyl_l2_floor"]
    assert curved["flat_metric_forbidden_for_cp2"] is True
    assert curved["flat_metric_forbidden_for_k3"] is True
    assert curved["barycentric_top_simplex_multiplier"] == 120


def test_synthesis_records_refinement_invariant_curvature_budget() -> None:
    summary = build_refinement_bridge_synthesis()
    budget = summary["curvature_budget_bridge"]
    assert budget["comparison_seed"] == "T4"
    assert budget["torus_weyl_l2_floor"] == 0.0
    assert budget["cp2_nonconformally_flat_topologically_forced"] is True
    assert budget["k3_nonconformally_flat_topologically_forced"] is True
    assert budget["cp2_hitchin_thorpe_plus"] == 9
    assert budget["cp2_hitchin_thorpe_minus"] == 3
    assert sorted((budget["k3_hitchin_thorpe_plus"], budget["k3_hitchin_thorpe_minus"])) == [0, 96]
    assert budget["refinement_preserves_cp2_chi"] == [3, 3, 3]
    assert budget["refinement_preserves_k3_chi"] == [24, 24, 24]


def test_synthesis_records_explicit_curved_external_complexes() -> None:
    summary = build_refinement_bridge_synthesis()
    complexes = summary["explicit_curved_complexes"]
    assert complexes["cp2_facets"] == 36
    assert complexes["cp2_betti_numbers"] == (1, 0, 1, 0, 1)
    assert complexes["cp2_harmonic_form_total"] == 3
    assert complexes["k3_facets"] == 288
    assert complexes["k3_betti_numbers"] == (1, 0, 22, 0, 1)
    assert complexes["k3_harmonic_form_total"] == 24
    assert complexes["k3_orbit_group_order"] == 240


def test_synthesis_records_explicit_curved_external_operator_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    operators = summary["curved_external_operator_bridge"]
    assert operators["cp2_total_chain_dim"] == 255
    assert operators["cp2_zero_modes_by_degree"] == (1, 0, 1, 0, 1)
    assert operators["cp2_total_spectral_gap"] > 1.9
    assert operators["cp2_trace_dk_squared"] == pytest.approx(1728.0)
    assert operators["k3_total_chain_dim"] == 1704
    assert operators["k3_zero_modes_by_degree"] == (1, 0, 22, 0, 1)
    assert operators["k3_total_spectral_gap"] > 0.68
    assert operators["k3_trace_dk_squared"] == pytest.approx(12480.0)
    assert operators["product_heat_factorizes_on_explicit_spectra"] is True


def test_synthesis_records_curved_h2_host_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    host = summary["curved_h2_host_bridge"]
    assert host["cp2_h2_dimension"] == 1
    assert host["cp2_b2_plus"] == 1
    assert host["cp2_b2_minus"] == 0
    assert host["cp2_rank2_h2_branch_available"] is False
    assert host["k3_h2_dimension"] == 22
    assert host["k3_b2_plus"] == 3
    assert host["k3_b2_minus"] == 19
    assert host["k3_rank2_h2_branch_available"] is True
    assert host["k3_mixed_sign_h2_plane_available"] is True
    assert host["cp2_six_mode"] == "156/19"
    assert host["k3_six_mode"] == "-880/19"
    assert host["six_mode_sign_matches_signature_on_both_explicit_seeds"] is True
    assert host["first_explicit_rank2_h2_host_is_k3"] is True


def test_synthesis_records_curved_h2_qutrit_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_h2_qutrit_bridge"]
    assert bridge["logical_qutrits"] == 81
    assert bridge["cp2_middle_degree_qutrit_channel"] == 81
    assert bridge["k3_middle_degree_qutrit_channel"] == 1782
    assert bridge["k3_minus_cp2_middle_degree_gap"] == 1701
    assert bridge["k3_positive_middle_degree_qutrit_channel"] == 243
    assert bridge["k3_negative_middle_degree_qutrit_channel"] == 1539
    assert bridge["cp2_is_not_rank2_middle_degree_host"] is True
    assert bridge["k3_is_rank2_middle_degree_host"] is True
    assert bridge["k3_has_both_middle_degree_sign_channels"] is True
    assert bridge["first_exact_middle_degree_qutrit_host_is_k3"] is True


def test_synthesis_records_curved_harmonic_qutrit_split_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_harmonic_qutrit_split_bridge"]
    assert bridge["logical_qutrits"] == 81
    assert bridge["universal_endpoint_qutrit_channel"] == 162
    assert bridge["endpoint_qutrit_channel_matches_on_all_explicit_seeds"] is True
    assert bridge["cp2_total_harmonic_qutrit_channel"] == 243
    assert bridge["k3_total_harmonic_qutrit_channel"] == 1944
    assert bridge["cp2_middle_degree_qutrit_channel"] == 81
    assert bridge["k3_middle_degree_qutrit_channel"] == 1782
    assert bridge["all_seed_dependence_is_middle_degree"] is True
    assert bridge["k3_minus_cp2_total_harmonic_gap"] == 1701
    assert bridge["k3_minus_cp2_middle_degree_gap"] == 1701


def test_synthesis_records_curved_h2_cup_plane_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_h2_cup_plane_bridge"]
    assert bridge["cp2_cup_signature"] == 1
    assert bridge["k3_cup_signature"] == -16
    assert bridge["k3_positive_h2_directions_from_cup_form"] == 3
    assert bridge["k3_negative_h2_directions_from_cup_form"] == 19
    assert bridge["k3_canonical_mixed_plane_selector_triangle"] == (1, 2, 3)
    assert bridge["k3_canonical_mixed_plane_split"] == (81, 81)
    assert bridge["k3_canonical_mixed_plane_is_split"] is True
    assert bridge["canonical_k3_mixed_plane_has_nonzero_intersection_determinant"] is True


def test_synthesis_records_k3_rank2_qutrit_plane_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_rank2_qutrit_plane_bridge"]
    assert bridge["minimal_rank2_qutrit_branch_dimension"] == 162
    assert bridge["mixed_rank2_qutrit_split"] == [81, 81]
    assert bridge["k3_supports_positive_rank2_plane"] is True
    assert bridge["k3_supports_mixed_rank2_plane"] is True
    assert bridge["k3_supports_negative_rank2_plane"] is True
    assert bridge["minimal_rank2_branch_matches_transport_extension_size"] is True


def test_synthesis_records_transport_mixed_plane_obstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_mixed_plane_obstruction_bridge"]
    assert bridge["dimension_pattern_matches_exactly"] is True
    assert bridge["internal_transport_162_is_nonsplit"] is True
    assert bridge["external_mixed_plane_162_is_split"] is True
    assert bridge["exact_split_vs_nonsplit_obstruction_is_present"] is True
    assert bridge["exact_identification_between_current_structures_is_supported"] is False


def test_synthesis_records_k3_mixed_plane_a4_projection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_mixed_plane_a4_projection_bridge"]
    assert bridge["branch_dimension_is_162"] is True
    assert bridge["finite_trace_multiplier_is_81"] is True
    assert bridge["branch_dimension_equals_2_times_trace_multiplier"] is True
    assert bridge["factor_of_two_is_exact_rank2_external_factor"] is True
    assert bridge["eightyone_vs_one_sixtytwo_is_dimension_vs_trace_split"] is True
    assert bridge["projecting_to_canonical_mixed_plane_does_not_promote_multiplier_to_162"] is True


def test_synthesis_records_k3_refined_plane_persistence_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_refined_plane_persistence_bridge"]
    assert bridge["first_refinement_scale_factor"] == 120
    assert bridge["first_barycentric_pullback_scales_restricted_form_by_120"] is True
    assert bridge["restricted_determinant_scales_by_120_squared"] is True
    assert bridge["normalized_restricted_form_is_refinement_invariant"] is True
    assert bridge["mixed_signature_survives_first_refinement"] is True


def test_synthesis_records_k3_integral_h2_lattice_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_integral_h2_lattice_bridge"]
    assert bridge["h2_rank"] == 22
    assert bridge["cocycle_rank"] == 127
    assert bridge["exact_rank"] == 105
    assert bridge["determinant"] == -1
    assert bridge["positive_directions"] == 3
    assert bridge["negative_directions"] == 19
    assert bridge["diagonal_even"] is True
    assert bridge["unimodular"] is True
    assert bridge["primitive_plane_gram_matrix"] == [[0, 1], [1, 0]]
    assert bridge["primitive_plane_minor_gcd"] == 1
    assert bridge["explicit_k3_seed_realizes_full_even_unimodular_k3_lattice"] is True


def test_synthesis_records_k3_primitive_plane_global_a4_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_primitive_plane_global_a4_bridge"]
    assert bridge["primitive_plane_seed_form"] == [[0, 1], [1, 0]]
    assert bridge["primitive_plane_first_refinement_form"] == [[0, 120], [120, 0]]
    assert bridge["Q_curv"] == "52"
    assert bridge["normalized_global_prefactor"] == "351/(4 pi^2)"
    assert bridge["raw_first_refinement_prefactor"] == "10530/pi^2"
    assert bridge["primitive_plane_first_refinement_quantum_is_plus_120"] is True
    assert bridge["reduced_global_prefactor_is_351_over_4_pi_squared"] is True
    assert bridge["sign_is_fixed_positive_on_the_canonical_oriented_plane"] is True


def test_synthesis_records_k3_three_u_decomposition_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_three_u_decomposition_bridge"]
    assert bridge["three_u_block_gram_matrix"] == [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
    ]
    assert bridge["three_u_block_unit_minor_rows"] == [0, 1, 3, 7, 19, 21]
    assert bridge["three_u_block_unit_minor_determinant"] == 1
    assert bridge["three_u_block_has_signature_3_3"] is True
    assert bridge["three_u_block_is_primitive_in_the_ambient_lattice"] is True
    assert bridge["orthogonal_complement_rank"] == 16
    assert bridge["orthogonal_complement_signature"] == [0, 16]
    assert bridge["orthogonal_complement_is_even_negative_definite_unimodular"] is True
    assert bridge["explicit_k3_seed_contains_primitive_orthogonal_3U_core"] is True


def test_synthesis_records_k3_three_u_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_three_u_refinement_bridge"]
    assert bridge["three_u_seed_form"] == [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
    ]
    assert bridge["three_u_first_refinement_form"] == [
        [0, 120, 0, 0, 0, 0],
        [120, 0, 0, 0, 0, 0],
        [0, 0, 0, 120, 0, 0],
        [0, 0, 120, 0, 0, 0],
        [0, 0, 0, 0, 0, 120],
        [0, 0, 0, 0, 120, 0],
    ]
    assert bridge["three_u_block_scales_by_120"] is True
    assert bridge["seed_form_is_exact_3u"] is True
    assert bridge["first_refinement_form_is_exact_120_times_3u"] is True
    assert bridge["normalized_three_u_block_is_refinement_invariant"] is True
    assert bridge["three_u_signature_survives_first_refinement"] is True
    assert bridge["three_u_determinant_scales_by_120_to_the_6"] is True


def test_synthesis_records_k3_three_u_complement_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_three_u_complement_refinement_bridge"]
    assert bridge["three_u_complement_basis_shape"] == [22, 16]
    assert bridge["three_u_complement_seed_form"][0][0] == -2
    assert bridge["three_u_complement_seed_form"][0][2] == -1
    assert bridge["three_u_complement_seed_form"][4][4] == -4
    assert bridge["three_u_complement_first_refinement_form"][0][0] == -240
    assert bridge["three_u_complement_first_refinement_form"][0][2] == -120
    assert bridge["three_u_complement_first_refinement_form"][4][4] == -480
    assert bridge["full_split_seed_form"][0][1] == 1
    assert bridge["full_split_seed_form"][5][4] == 1
    assert bridge["full_split_seed_form"][6][6] == -2
    assert bridge["full_split_first_refinement_form"][0][1] == 120
    assert bridge["full_split_first_refinement_form"][5][4] == 120
    assert bridge["full_split_first_refinement_form"][6][6] == -240
    assert bridge["three_u_and_complement_are_exactly_orthogonal"] is True
    assert bridge["complement_has_signature_0_16"] is True
    assert bridge["complement_form_scales_by_120"] is True
    assert bridge["full_split_form_scales_by_120"] is True
    assert bridge["full_split_cross_terms_remain_zero"] is True
    assert bridge["full_split_signature_survives_first_refinement"] is True
    assert bridge["explicit_k3_lattice_split_is_first_refinement_rigid"] is True


def test_synthesis_records_k3_n16_e8e8_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_n16_e8e8_bridge"]
    assert bridge["root_representative_count"] == 240
    assert bridge["total_root_count"] == 480
    assert bridge["root_span_smith_diagonal"] == [1] * 16
    assert bridge["root_span_rank"] == 16
    assert bridge["root_span_index"] == 1
    assert bridge["n16_has_480_roots"] is True
    assert bridge["root_span_equals_the_full_lattice"] is True
    assert bridge["explicit_n16_is_not_d16_plus"] is True
    assert bridge["explicit_n16_is_e8_plus_e8_by_rank16_even_unimodular_classification"] is True


def test_synthesis_records_k3_e8_factor_split_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_e8_factor_split_bridge"]
    assert bridge["representative_root_component_sizes"] == [120, 120]
    assert bridge["full_root_component_sizes"] == [240, 240]
    assert bridge["combined_simple_root_change_of_basis_determinant"] in {-1, 1}
    assert bridge["factor_one_has_exact_negative_e8_cartan"] is True
    assert bridge["factor_two_has_exact_negative_e8_cartan"] is True
    assert bridge["the_two_e8_factor_bases_are_exactly_orthogonal"] is True
    assert bridge["combined_simple_root_basis_is_unimodular_in_the_explicit_complement"] is True
    assert bridge["explicit_n16_is_constructively_split_as_e8_plus_e8"] is True


def test_synthesis_records_k3_e8_factor_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_e8_factor_refinement_bridge"]
    assert bridge["factor_one_refined_form_is_exact_120_times_negative_e8_cartan"] is True
    assert bridge["factor_two_refined_form_is_exact_120_times_negative_e8_cartan"] is True
    assert bridge["e8_factors_remain_exactly_orthogonal_after_refinement"] is True
    assert bridge["full_named_split_scales_by_120"] is True
    assert bridge["normalized_named_split_is_refinement_invariant"] is True
    assert bridge["explicit_named_k3_split_is_first_refinement_rigid"] is True


def test_synthesis_records_k3_primitive_plane_three_u_alignment_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_primitive_plane_three_u_alignment_bridge"]
    assert bridge["primitive_plane_coefficients"] == bridge["three_u_factor_one_coefficients"]
    assert bridge["selector_three_u_shadow_reconstruction_error_linf"] < 1e-10
    assert bridge["primitive_plane_equals_the_first_explicit_u_factor"] is True
    assert bridge["selector_three_u_shadow_decomposes_exactly_across_the_three_u_factors"] is True
    assert bridge["selector_has_nonzero_projection_on_u_factor_one"] is True
    assert bridge["selector_has_nonzero_projection_on_u_factor_two"] is True
    assert bridge["selector_has_nonzero_projection_on_u_factor_three"] is True
    assert bridge["selector_three_u_shadow_is_not_supported_on_the_primitive_plane_alone"] is True
    assert bridge["primitive_plane_is_distinguished_but_not_equal_to_the_selector_positive_channel"] is True


def test_synthesis_records_k3_selector_three_u_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_three_u_shadow_bridge"]
    assert bridge["selector_plane_form"][0][0] == pytest.approx(0.1705210828229612)
    assert bridge["selector_plane_form"][0][1] == pytest.approx(0.0, abs=1e-10)
    assert bridge["selector_plane_form"][1][1] == pytest.approx(-0.1262119267461511)
    assert bridge["three_u_shadow_form"][0][0] == pytest.approx(2.8024851868813414)
    assert bridge["three_u_shadow_form"][1][1] == pytest.approx(0.2518300163799658)
    assert bridge["rank16_residual_form"][0][0] == pytest.approx(-2.6319641040583726)
    assert bridge["rank16_residual_form"][1][1] == pytest.approx(-0.37804194312612105)
    assert bridge["principal_cosines_against_three_u_core"][0] == pytest.approx(0.6939852722886527)
    assert bridge["principal_cosines_against_three_u_core"][1] == pytest.approx(0.4318086483648292)
    assert bridge["selector_plane_shadow_on_three_u_is_positive_definite"] is True
    assert bridge["selector_plane_residual_on_rank16_complement_is_negative_definite"] is True
    assert bridge["selector_plane_is_not_contained_in_three_u_core"] is True
    assert bridge["selector_plane_straddles_both_k3_lattice_pieces"] is True


def test_synthesis_records_k3_selector_e8_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_e8_shadow_bridge"]
    assert bridge["reconstruction_error_linf"] < 1e-10
    assert bridge["selector_projection_on_three_u_is_positive_definite"] is True
    assert bridge["selector_projection_on_e8_factor_one_is_negative_definite"] is True
    assert bridge["selector_projection_on_e8_factor_two_is_negative_definite"] is True
    assert bridge["selector_projection_on_e8_factor_one_is_nonzero"] is True
    assert bridge["selector_projection_on_e8_factor_two_is_nonzero"] is True
    assert bridge["selector_decomposes_orthogonally_across_three_u_and_both_e8_factors"] is True
    assert bridge["selector_is_not_supported_on_single_e8_factor"] is True
    assert bridge["selector_bridges_three_u_and_both_e8_factors"] is True


def test_synthesis_records_k3_selector_shadow_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_shadow_refinement_bridge"]
    assert bridge["selector_seed_form"][0][0] == pytest.approx(0.17052108282296116)
    assert bridge["selector_seed_form"][1][1] == pytest.approx(-0.12621192674615103)
    assert bridge["selector_first_refinement_form"][0][0] == pytest.approx(20.462529938755336)
    assert bridge["selector_first_refinement_form"][1][1] == pytest.approx(-15.145431209538124)
    assert bridge["three_u_shadow_seed_form"][0][0] == pytest.approx(2.80248518688132)
    assert bridge["three_u_shadow_seed_form"][1][1] == pytest.approx(0.2518300163799555)
    assert bridge["rank16_residual_seed_form"][0][0] == pytest.approx(-2.6319641040583783)
    assert bridge["rank16_residual_seed_form"][1][1] == pytest.approx(-0.3780419431261282)
    assert bridge["selector_plane_scales_by_120"] is True
    assert bridge["three_u_shadow_scales_by_120"] is True
    assert bridge["rank16_residual_scales_by_120"] is True
    assert bridge["three_u_shadow_stays_positive_definite"] is True
    assert bridge["rank16_residual_stays_negative_definite"] is True


def test_synthesis_records_k3_selector_a4_lattice_split_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_a4_lattice_split_bridge"]
    assert bridge["common_scalar_prefactor"] == "351/(4 pi^2)"
    assert bridge["selector_packet_reconstructs_as_three_u_plus_e8_plus_e8"] is True
    assert bridge["three_u_packet_piece_is_positive_definite"] is True
    assert bridge["e8_factor_one_packet_piece_is_negative_definite"] is True
    assert bridge["e8_factor_two_packet_piece_is_negative_definite"] is True
    assert bridge["all_three_packet_pieces_are_nonzero"] is True
    assert bridge["reduced_selector_packet_is_tri_supported_across_the_named_k3_split"] is True
    assert bridge["scalar_prefactor_remains_exactly_351_over_4_pi_squared"] is True


def test_synthesis_records_k3_selector_a4_five_factor_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_a4_five_factor_bridge"]
    assert bridge["common_scalar_prefactor"] == "351/(4 pi^2)"
    assert bridge["reconstruction_error_linf"] < 1e-10
    assert bridge["u_factor_one_packet_form"][0][0] == pytest.approx(0.469558153807232)
    assert bridge["u_factor_two_packet_form"][1][1] == pytest.approx(0.06475792755064227)
    assert bridge["u_factor_three_packet_form"][0][0] == pytest.approx(2.3201042391973585)
    assert bridge["e8_factor_one_packet_form"][0][0] == pytest.approx(-0.2369079021220062)
    assert bridge["e8_factor_two_packet_form"][0][0] == pytest.approx(-2.3950562019433925)
    assert bridge["three_u_packet_reconstructs_as_u1_plus_u2_plus_u3"] is True
    assert bridge["selector_packet_reconstructs_as_u1_plus_u2_plus_u3_plus_e8_plus_e8"] is True
    assert bridge["u_factor_one_packet_piece_is_mixed_signature"] is True
    assert bridge["u_factor_two_packet_piece_is_mixed_signature"] is True
    assert bridge["u_factor_three_packet_piece_is_mixed_signature"] is True
    assert bridge["all_five_packet_pieces_are_nonzero"] is True
    assert bridge["distinguished_u1_plane_has_nonzero_selector_packet_piece"] is True
    assert bridge["selector_hyperbolic_packet_is_not_supported_on_u1_alone"] is True
    assert bridge["reduced_selector_packet_is_five_supported_across_u_u_u_e8_e8"] is True


def test_synthesis_records_k3_selector_a4_five_factor_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["k3_selector_a4_five_factor_refinement_bridge"]
    assert bridge["u_factor_one_seed_form"][0][0] == pytest.approx(0.469558153807232)
    assert bridge["u_factor_one_first_refinement_form"][0][0] == pytest.approx(56.34697845686784)
    assert bridge["u_factor_three_first_refinement_form"][0][0] == pytest.approx(278.412508703683)
    assert bridge["e8_factor_two_first_refinement_form"][0][0] == pytest.approx(-287.40674423320713)
    assert bridge["u_factor_one_packet_piece_scales_by_120"] is True
    assert bridge["u_factor_two_packet_piece_scales_by_120"] is True
    assert bridge["u_factor_three_packet_piece_scales_by_120"] is True
    assert bridge["e8_factor_one_packet_piece_scales_by_120"] is True
    assert bridge["e8_factor_two_packet_piece_scales_by_120"] is True
    assert bridge["all_five_normalized_packet_forms_are_refinement_invariant"] is True
    assert bridge["all_three_u_factor_packet_pieces_stay_mixed_signature"] is True
    assert bridge["both_e8_packet_pieces_stay_negative_definite"] is True
    assert bridge["fine_selector_packet_split_is_first_refinement_rigid"] is True


def test_synthesis_records_u1_family_a4_carrier_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["u1_family_a4_carrier_bridge"]
    assert bridge["delta_A4"] == "1209/9194 a0"
    assert bridge["canonical_external_carrier"] == "U1"
    assert bridge["normalized_global_prefactor"] == "351/(4 pi^2)"
    assert bridge["common_line_generator"] == [1, 1, 0]
    assert bridge["common_plane_equation"] == "x = y"
    assert bridge["distinguished_generation"] == 2
    assert bridge["first_family_entry_is_a4_only"] is True
    assert bridge["canonical_external_carrier_equals_u_factor_one"] is True
    assert bridge["canonical_u1_carrier_has_exact_351_over_4_pi_squared_coupling"] is True
    assert bridge["u1_is_nonzero_piece_of_full_selector_packet"] is True
    assert bridge["full_selector_packet_is_not_supported_on_u1_alone"] is True
    assert bridge["internal_family_side_has_exact_one_vs_two_flag_boundary_condition"] is True
    assert bridge["exact_identification_of_u1_with_transport_162_extension_is_obstructed"] is True
    assert bridge["minimal_canonical_family_bridge_carrier_is_delta_a4_on_u1"] is True


def test_synthesis_records_u1_isotropic_line_obstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["u1_isotropic_line_obstruction_bridge"]
    assert bridge["u1_seed_form"] == [[0, 1], [1, 0]]
    assert bridge["u1_swapped_seed_form"] == [[0, 1], [1, 0]]
    assert bridge["internal_common_line_generator"] == [1, 1, 0]
    assert bridge["line_one_is_primitive"] is True
    assert bridge["line_two_is_primitive"] is True
    assert bridge["line_one_is_isotropic"] is True
    assert bridge["line_two_is_isotropic"] is True
    assert bridge["line_pair_has_unit_hyperbolic_pairing"] is True
    assert bridge["swapping_the_two_isotropic_lines_preserves_the_u1_seed_form"] is True
    assert bridge["current_u1_data_do_not_distinguish_one_isotropic_line_from_the_other"] is True
    assert bridge["exact_identification_of_the_internal_common_line_with_a_canonical_u1_line_is_not_yet_supported"] is True


def test_synthesis_records_selector_a4_weight_hierarchy_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["selector_a4_weight_hierarchy_bridge"]
    assert bridge["factor_frobenius_norms"]["U1"] == pytest.approx(0.5070148472753923)
    assert bridge["factor_frobenius_norms"]["U2"] == pytest.approx(0.0814269981830142)
    assert bridge["factor_frobenius_norms"]["U3"] == pytest.approx(2.4712362068942952)
    assert bridge["factor_frobenius_norms"]["E8_1"] == pytest.approx(0.2957919585266082)
    assert bridge["factor_frobenius_norms"]["E8_2"] == pytest.approx(2.505700578655349)
    assert bridge["hyperbolic_weight_shares"]["U3"] == pytest.approx(0.8076785088529392)
    assert bridge["exceptional_weight_shares"]["E8_2"] == pytest.approx(0.894416296099026)
    assert bridge["hyperbolic_weight_order_is_u3_gt_u1_gt_u2"] is True
    assert bridge["exceptional_weight_order_is_e8_factor_two_gt_e8_factor_one"] is True
    assert bridge["u3_carries_more_than_four_fifths_of_hyperbolic_packet_weight"] is True
    assert bridge["e8_factor_two_carries_more_than_eight_ninths_of_exceptional_packet_weight"] is True
    assert bridge["fine_weight_hierarchy_is_refinement_invariant"] is True


def test_synthesis_records_transport_semisimplification_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_semisimplification_shadow_bridge"]
    assert bridge["internal_transport_semisimplification"] == [81, 81]
    assert bridge["external_split_shadow"] == [81, 81]
    assert bridge["internal_semisimplification_is_81_plus_81"] is True
    assert bridge["external_split_shadow_is_81_plus_81"] is True
    assert bridge["internal_and_external_objects_match_exactly_at_semisimplified_shadow_level"] is True
    assert bridge["internal_extension_class_is_nonzero"] is True
    assert bridge["external_extension_class_is_zero"] is True
    assert bridge["transport_k3_match_is_semisimplified_shadow_not_extension_identity"] is True


def test_synthesis_records_transport_filtered_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_filtered_shadow_bridge"]
    assert bridge["internal_transport_filtration"] == [81, 162, 81]
    assert bridge["internal_distinguished_invariant_line"] == [1, 2]
    assert bridge["external_canonical_split_filtration"] == [81, 162, 81]
    assert bridge["external_ordered_line_types"] == ["positive", "negative"]
    assert bridge["internal_transport_has_canonical_ordered_81_in_162_out_81_filtration"] is True
    assert bridge["external_k3_mixed_plane_has_canonical_ordered_split_81_in_162_out_81_filtration"] is True
    assert bridge["internal_and_external_match_at_ordered_filtered_dimension_level"] is True
    assert bridge["external_filtered_shadow_refines_old_81_plus_81_graded_shadow"] is True
    assert bridge["external_filtered_shadow_is_first_refinement_rigid"] is True
    assert bridge["extension_class_mismatch_remains_exact"] is True
    assert bridge["current_bridge_reaches_filtered_split_shadow_but_not_nonsplit_extension_identity"] is True


def test_synthesis_records_transport_nilpotent_glue_obstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_nilpotent_glue_obstruction_bridge"]
    assert bridge["internal_transport_nilpotent_glue_rank"] == 81
    assert bridge["internal_transport_nilpotent_glue_nullity"] == 81
    assert bridge["external_split_filtered_shadow"] == [81, 162, 81]
    assert bridge["internal_transport_162_has_nontrivial_rank_81_square_zero_glue_operator"] is True
    assert bridge["external_transport_shadow_matches_the_ordered_81_in_162_out_81_filtration"] is True
    assert bridge["external_transport_shadow_is_split_and_has_zero_extension_class"] is True
    assert bridge["internal_and_external_transport_packets_match_at_filtered_dimension_level_but_not_at_glue_operator_level"] is True
    assert bridge["current_bridge_reaches_head_middle_tail_and_ordering_but_not_nilpotent_glue"] is True


def test_synthesis_records_transport_polarized_line_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_polarized_line_shadow_bridge"]
    assert bridge["internal_ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["internal_head_type"] == "invariant"
    assert bridge["internal_tail_type"] == "sign"
    assert bridge["internal_nilpotent_glue_direction"] == "tail_to_head"
    assert bridge["external_ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["external_ordered_filtered_shadow_line_types"] == ["positive", "negative"]
    assert bridge["internal_transport_has_canonical_head_middle_tail_structure"] is True
    assert bridge["external_bridge_has_canonical_head_biased_and_tail_biased_u1_lines"] is True
    assert bridge["dominant_u1_line_is_head_biased_and_recessive_u1_line_is_tail_biased"] is True
    assert bridge["current_bridge_reaches_a_canonical_head_tail_polarized_split_shadow"] is True
    assert bridge["current_bridge_does_not_yet_realize_the_internal_tail_to_head_nilpotent_glue"] is True
    assert bridge["polarized_shadow_is_stronger_than_filtered_dimension_match_but_weaker_than_extension_identity"] is True


def test_synthesis_records_transport_jordan_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_jordan_shadow_bridge"]
    assert bridge["internal_jordan_partition"] == "2^81"
    assert bridge["internal_jordan_block_size_2_count"] == 81
    assert bridge["internal_jordan_block_size_1_count"] == 0
    assert bridge["internal_associated_graded_dimensions"] == [81, 81]
    assert bridge["internal_head_type"] == "invariant"
    assert bridge["internal_tail_type"] == "sign"
    assert bridge["external_ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["external_ordered_filtered_shadow_line_types"] == ["positive", "negative"]
    assert bridge["internal_transport_glue_has_exact_jordan_type_two_power_81"] is True
    assert bridge["internal_transport_associated_graded_is_exactly_81_head_plus_81_tail"] is True
    assert bridge["external_bridge_fixes_the_polarized_associated_graded_of_the_transport_jordan_packet"] is True
    assert bridge["current_bridge_does_not_yet_realize_the_internal_nontrivial_size_two_jordan_blocks"] is True
    assert bridge["current_bridge_reaches_the_polarized_jordan_shadow_but_not_the_internal_jordan_identity"] is True


def test_synthesis_records_transport_single_glue_slot_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_single_glue_slot_bridge"]
    assert bridge["internal_head_dimension"] == 81
    assert bridge["internal_middle_dimension"] == 162
    assert bridge["internal_tail_dimension"] == 81
    assert bridge["slot_direction"] == "tail_to_head"
    assert bridge["slot_shape"] == [81, 81]
    assert bridge["required_internal_rank"] == 81
    assert bridge["current_external_slot_rank"] == 0
    assert bridge["current_external_slot_state"] == "zero_by_splitness"
    assert bridge["current_bridge_fixes_the_semisimplified_shadow_of_the_transport_packet"] is True
    assert bridge["current_bridge_fixes_the_ordered_filtered_shadow_of_the_transport_packet"] is True
    assert bridge["current_bridge_fixes_the_polarized_jordan_shadow_of_the_transport_packet"] is True
    assert bridge["exact_transport_identity_would_require_a_tail_to_head_rank_81_square_zero_glue_operator"] is True
    assert bridge["the_current_external_bridge_forces_that_single_glue_slot_to_be_zero"] is True
    assert bridge["the_only_missing_exact_transport_datum_is_one_tail_to_head_81_by_81_operator_slot"] is True


def test_synthesis_records_external_glue_zero_forcing_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["external_glue_zero_forcing_bridge"]

    assert bridge["source"] == "canonical_mixed_k3_plane_qutrit_lift"
    assert bridge["qutrit_lift_split"] == [81, 81]
    assert bridge["total_qutrit_lift_dimension"] == 162
    assert bridge["ordered_line_types"] == ["positive", "negative"]
    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["extension_class_zero"] is True
    assert bridge["slot_direction"] == "tail_to_head"
    assert bridge["slot_shape"] == [81, 81]
    assert bridge["current_external_rank"] == 0
    assert bridge["current_external_state"] == "zero_by_splitness"
    assert bridge[
        "current_external_162_sector_is_exactly_the_split_qutrit_lift_of_the_canonical_mixed_k3_plane"
    ] is True
    assert bridge["current_external_transport_shadow_has_zero_extension_class"] is True
    assert bridge["split_vs_nonsplit_obstruction_is_already_exact_at_the_current_bridge_level"] is True
    assert bridge[
        "the_unique_external_tail_to_head_glue_slot_is_structurally_zero_on_the_present_bridge_object"
    ] is True
    assert bridge[
        "any_nonzero_external_glue_operator_would_require_new_external_data_beyond_the_current_bridge_objects"
    ] is True


def test_synthesis_records_transport_rigid_split_avatar_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_rigid_split_avatar_bridge"]

    assert bridge["head_line"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["tail_line"] == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0]
    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["glue_direction"] == "tail_to_head"
    assert bridge["external_glue_rank"] == 0
    assert bridge["external_glue_state"] == "zero_by_splitness"
    assert bridge["current_bridge_fixes_a_head_compatible_external_head_line"] is True
    assert bridge["current_bridge_fixes_a_canonical_external_tail_line"] is True
    assert bridge["current_bridge_fixes_the_ordered_81_in_162_out_81_split_avatar_dimensions"] is True
    assert bridge["current_bridge_forces_the_external_glue_of_that_avatar_to_be_zero"] is True
    assert bridge["current_bridge_fixes_one_canonical_rigid_split_avatar_of_the_internal_transport_packet"] is True
    assert bridge["that_avatar_is_still_not_the_internal_nonsplit_transport_object"] is True


def test_synthesis_records_transport_avatar_deformation_wall_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_avatar_deformation_wall_bridge"]

    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["glue_direction"] == "tail_to_head"
    assert bridge["external_glue_rank"] == 0
    assert bridge["external_glue_state"] == "zero_by_splitness"
    assert bridge["slot_direction"] == "tail_to_head"
    assert bridge["slot_shape"] == [81, 81]
    assert bridge["required_internal_rank"] == 81
    assert bridge["required_internal_square_zero"] is True
    assert bridge["current_bridge_has_already_fixed_one_canonical_rigid_split_transport_avatar"] is True
    assert bridge["exact_transport_identity_would_require_adjoining_a_nonzero_tail_to_head_81_by_81_glue_operator_to_that_avatar"] is True
    assert bridge["any_exact_completion_must_preserve_the_fixed_head_line_tail_line_and_ordered_dimensions_of_the_avatar"] is True
    assert bridge["the_remaining_transport_wall_is_a_nonsplit_deformation_problem_not_a_search_for_an_unfixed_external_packet"] is True


def test_synthesis_records_transport_full_rank_glue_normal_form_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_full_rank_glue_normal_form_bridge"]

    assert bridge["slot_direction"] == "tail_to_head"
    assert bridge["slot_shape"] == [81, 81]
    assert bridge["required_rank"] == 81
    assert bridge["slot_matrix_normal_form"] == "I_81"
    assert bridge["polarized_nilpotent_normal_form"] == "J2^81"
    assert bridge["any_exact_completion_in_the_fixed_polarized_81_to_162_to_81_shell_has_full_rank_glue"] is True
    assert bridge["up_to_independent_head_tail_basis_change_any_full_rank_glue_completion_has_identity_slot_matrix"] is True
    assert bridge["up_to_polarized_isomorphism_any_exact_completion_has_canonical_jordan_normal_form_two_power_81"] is True
    assert bridge["the_remaining_transport_wall_is_existence_of_a_nonsplit_completion_not_glue_shape"] is True


def test_synthesis_records_transport_internal_operator_normal_form_match_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_internal_operator_normal_form_match_bridge"]

    assert bridge["fiber_shift_matrix"] == [[0, 1], [0, 0]]
    assert bridge["operator_model"] == "I_81 ⊗ [[0,1],[0,0]]"
    assert bridge["slot_matrix_normal_form"] == "I_81"
    assert bridge["polarized_nilpotent_normal_form"] == "J2^81"
    assert bridge["internal_transport_extension_has_exact_operator_normal_form_i81_tensor_fiber_shift"] is True
    assert bridge["any_exact_external_completion_of_the_rigid_avatar_has_the_same_linear_algebraic_normal_form_up_to_head_tail_basis_gauge"] is True
    assert bridge["the_remaining_transport_wall_is_realization_of_the_nontrivial_cocycle_class_not_operator_shape"] is True


def test_synthesis_records_transport_unique_nonzero_cocycle_orbit_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_unique_nonzero_cocycle_orbit_bridge"]

    assert bridge["base_shift"] == [[0, 1], [0, 0]]
    assert bridge["other_nonzero_scalar_multiple"] == [[0, 2], [0, 0]]
    assert bridge["conjugating_basis_change"] == [[1, 0], [0, 2]]
    assert bridge["the_internal_transport_cocycle_is_nontrivial"] is True
    assert bridge["the_only_nonzero_scalar_multiples_of_the_fiber_shift_over_f3_are_n_and_2n"] is True
    assert bridge["the_two_nonzero_scalar_multiples_are_gauge_equivalent_by_adapted_diagonal_basis_change"] is True
    assert bridge["up_to_the_natural_head_tail_basis_gauge_there_is_a_unique_nonzero_ternary_glue_orbit"] is True
    assert bridge["the_remaining_external_wall_is_existence_of_that_unique_nonzero_orbit_not_selection_among_several_nonzero_types"] is True


def test_synthesis_records_refined_k3_zero_orbit_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["refined_k3_zero_orbit_bridge"]

    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["extension_class_zero"] is True
    assert bridge["first_refinement_scale_factor"] == 120
    assert bridge["current_refined_k3_shadow_is_split_with_zero_extension_class"] is True
    assert bridge["current_refined_k3_shadow_remains_refinement_rigid_at_first_barycentric_step"] is True
    assert bridge["the_unique_nonzero_ternary_orbit_is_not_realized_on_the_current_refined_k3_side"] is True
    assert bridge["any_realization_of_the_unique_nonzero_orbit_requires_new_external_data_beyond_the_current_refined_k3_bridge"] is True


def test_synthesis_records_common_line_exact_image_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["common_line_exact_image_bridge"]

    assert bridge["generator"] == [1, 1, 0]
    assert bridge["carrier_plane"] == "U1"
    assert bridge["internal_common_line_is_exactly_the_image_of_the_common_square"] is True
    assert bridge["internal_transport_operator_image_is_the_head_invariant_line"] is True
    assert bridge["the_head_compatible_u1_line_is_the_exact_bridge_image_of_the_internal_common_line_in_any_exact_completion"] is True
    assert bridge["what_remains_open_is_existence_of_that_exact_completion_not_choice_of_image_line"] is True


def test_synthesis_records_e13_a4_support_stratification_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["e13_a4_support_stratification_bridge"]

    assert bridge["minimal_a4_carrier_plane"] == "U1"
    assert bridge["rigid_transport_avatar_dimensions"] == [81, 162, 81]
    assert bridge["broader_local_packet_dominant_piece"] == "U3"
    assert bridge["the_central_image_side_2e13_channel_localizes_to_the_head_line_in_any_exact_completion"] is True
    assert bridge["the_first_family_sensitive_a4_bridge_packet_has_minimal_canonical_plane_carrier_u1"] is True
    assert bridge["exact_transport_completion_uses_the_full_rigid_avatar_shell_81_to_162_to_81"] is True
    assert bridge["the_broader_five_factor_packet_is_local_selector_context_not_the_minimal_exact_family_carrier"] is True
    assert bridge["the_live_2e13_a4_bridge_is_exactly_stratified_as_head_line_inside_u1_inside_avatar"] is True


def test_synthesis_records_minimal_external_completion_data_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["minimal_external_completion_data_bridge"]

    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["slot_direction"] == "tail_to_head"
    assert bridge["slot_shape"] == [81, 81]
    assert bridge["current_external_slot_state"] == "zero_by_splitness"
    assert bridge["slot_matrix_normal_form"] == "I_81"
    assert bridge["polarized_nilpotent_normal_form"] == "J2^81"
    assert bridge[
        "the_minimal_new_external_data_is_exactly_replacing_zero_by_the_unique_nonzero_orbit_in_the_existing_slot"
    ] is True
    assert bridge[
        "no_additional_line_plane_or_dimension_choice_remains_after_the_current_bridge_reductions"
    ] is True


def test_synthesis_records_formal_external_completion_avatar_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["formal_external_completion_avatar_bridge"]

    assert bridge["carrier_plane"] == "U1"
    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["slot_matrix_normal_form"] == "I_81"
    assert bridge["polarized_nilpotent_normal_form"] == "J2^81"
    assert bridge[
        "the_forced_image_line_and_the_nonzero_glue_live_on_one_common_formal_external_object"
    ] is True
    assert bridge[
        "the_missing_piece_is_now_current_k3_realization_not_common_object_design"
    ] is True


def test_synthesis_records_yukawa_transport_coupling_hierarchy_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_transport_coupling_hierarchy_bridge"]

    assert bridge["plane_level"] == "U1"
    assert bridge["avatar_level"] == [81, 162, 81]
    assert bridge["broader_local_context"] == "U3"
    assert bridge[
        "the_live_unresolved_family_closure_is_support_filtered_as_line_inside_plane_inside_avatar"
    ] is True
    assert bridge[
        "the_unresolved_family_packet_does_not_reduce_to_u3_even_though_u3_is_locally_dominant"
    ] is True


def test_synthesis_records_e13_rigid_avatar_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["e13_rigid_avatar_bridge"]

    assert bridge["common_square"] == [[0, 0, 2], [0, 0, 0], [0, 0, 0]]
    assert bridge["common_line_generator"] == [1, 1, 0]
    assert bridge["head_line"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["tail_line"] == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0]
    assert bridge["ordered_filtration_dimensions"] == [81, 162, 81]
    assert bridge["external_glue_state"] == "zero_by_splitness"
    assert bridge["internal_central_2e13_channel_is_exact"] is True
    assert bridge["the_unique_bridge_compatible_external_image_of_the_internal_common_line_is_the_head_line_of_the_rigid_avatar"] is True
    assert bridge["the_current_external_realization_of_the_central_channel_factors_through_the_canonical_rigid_split_avatar"] is True
    assert bridge["exact_external_realization_of_the_central_2e13_channel_would_require_a_nonsplit_deformation_of_that_avatar"] is True
    assert bridge["any_exact_completion_of_that_avatar_has_the_unique_full_rank_glue_normal_form_two_power_81"] is True
    assert bridge["any_exact_completion_of_that_avatar_matches_the_internal_transport_operator_normal_form_up_to_basis_gauge"] is True


def test_synthesis_records_global_local_carrier_split_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["global_local_carrier_split_bridge"]
    assert bridge["canonical_global_carrier"] == "U1"
    assert bridge["dominant_hyperbolic_packet_piece"] == "U3"
    assert bridge["dominant_exceptional_packet_piece"] == "E8_2"
    assert bridge["hyperbolic_dominance_ratio_u3_over_u1"] == pytest.approx(
        4.874090414066333
    )
    assert bridge["exceptional_dominance_ratio_e8_factor_two_over_e8_factor_one"] == (
        pytest.approx(8.471158550545743)
    )
    assert bridge["canonical_global_carrier_is_u1"] is True
    assert bridge["dominant_hyperbolic_packet_piece_is_u3"] is True
    assert bridge["dominant_exceptional_packet_piece_is_e8_factor_two"] is True
    assert bridge["canonical_global_carrier_differs_from_dominant_hyperbolic_packet_piece"] is True
    assert bridge["first_family_packet_has_canonical_global_support_but_non_u1_local_dominance"] is True
    assert bridge["global_local_carrier_split_is_refinement_invariant"] is True


def test_synthesis_records_u1_selector_line_selection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["u1_selector_line_selection_bridge"]
    assert bridge["u1_isotropic_line_weights"][0] == pytest.approx(0.29249916729399683)
    assert bridge["u1_isotropic_line_weights"][1] == pytest.approx(0.22063099582377832)
    assert bridge["dominant_isotropic_line_index"] == 0
    assert bridge["recessive_isotropic_line_index"] == 1
    assert bridge["dominance_ratio"] == pytest.approx(1.3257392335192142)
    assert bridge["carrier_metric_alone_is_line_blind"] is True
    assert bridge["canonical_selector_u1_component_has_full_rank_2"] is True
    assert bridge["canonical_selector_u1_component_assigns_unequal_weights_to_the_two_isotropic_lines"] is True
    assert bridge["there_is_a_unique_dominant_isotropic_line_inside_u1"] is True
    assert bridge["dominant_isotropic_line_is_the_first_u1_line_in_the_current_canonical_basis"] is True
    assert bridge["selector_line_weights_are_invariant_under_selector_basis_signs_and_swap"] is True
    assert bridge["u1_carrier_form_scales_by_120_at_first_refinement"] is True
    assert bridge["u1_selector_packet_form_scales_by_120_at_first_refinement"] is True
    assert bridge["dominant_line_candidate_is_first_refinement_rigid"] is True
    assert bridge["full_current_external_packet_selects_a_canonical_isotropic_line_candidate_inside_u1"] is True


def test_synthesis_records_u1_filtered_shadow_line_order_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["u1_filtered_shadow_line_order_bridge"]
    assert bridge["ordered_filtered_shadow_line_types"] == ["positive", "negative"]
    assert bridge["u1_positive_selector_weights"][0] == pytest.approx(0.2773869501109481)
    assert bridge["u1_positive_selector_weights"][1] == pytest.approx(0.19871596313260903)
    assert bridge["u1_negative_selector_weights"][0] == pytest.approx(0.015112217183048728)
    assert bridge["u1_negative_selector_weights"][1] == pytest.approx(0.021915032691169296)
    assert bridge["u1_positive_minus_negative_selector_gaps"][0] == pytest.approx(
        0.2622747329278994
    )
    assert bridge["u1_positive_minus_negative_selector_gaps"][1] == pytest.approx(
        0.17680093044143974
    )
    assert bridge["dominant_isotropic_line_index"] == 0
    assert bridge["recessive_isotropic_line_index"] == 1
    assert bridge["filtered_shadow_basis_is_canonically_ordered_positive_then_negative"] is True
    assert bridge["dominant_u1_line_has_strictly_larger_positive_selector_weight"] is True
    assert bridge["dominant_u1_line_has_strictly_smaller_negative_selector_contamination"] is True
    assert bridge["dominant_u1_line_maximizes_positive_minus_negative_selector_gap"] is True
    assert bridge["sign_order_refines_total_weight_order"] is True
    assert bridge["sign_ordered_line_candidate_is_first_refinement_rigid"] is True
    assert bridge["current_bridge_fixes_a_rigid_positive_ordered_line_candidate_inside_u1"] is True


def test_synthesis_records_u1_head_compatible_line_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["u1_head_compatible_line_bridge"]
    assert bridge["internal_common_line_generator"] == [1, 1, 0]
    assert bridge["internal_common_line_role"] == "image_of_common_square"
    assert bridge["transport_head_type"] == "invariant"
    assert bridge["transport_tail_type"] == "sign"
    assert bridge["transport_glue_direction"] == "tail_to_head"
    assert bridge["head_compatible_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["tail_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0]
    assert bridge["internal_common_line_is_exact_image_side_data"] is True
    assert bridge["internal_transport_head_is_the_image_side_of_the_current_polarity_dictionary"] is True
    assert bridge["external_bridge_fixes_head_biased_and_tail_biased_u1_lines"] is True
    assert bridge["the_sign_ordered_rigid_u1_line_is_exactly_the_head_biased_line"] is True
    assert bridge["the_tail_biased_u1_line_is_not_compatible_with_an_image_side_realization_of_the_internal_common_line"] is True
    assert bridge["the_current_external_line_ambiguity_collapses_to_one_head_compatible_candidate"] is True


def test_synthesis_records_family_flag_visibility_obstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["family_flag_visibility_obstruction_bridge"]
    assert bridge["internal_common_line_generator"] == [1, 1, 0]
    assert bridge["internal_common_plane_equation"] == "x = y"
    assert bridge["external_canonical_carrier_plane"] == "U1"
    assert bridge["external_canonical_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_sign_ordered_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_head_compatible_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_semisimplified_shadow"] == [81, 81]
    assert bridge["external_filtered_split_shadow"] == [81, 162, 81]
    assert bridge["external_nilpotent_glue_visibility"] == {
        "matches_internal_nilpotent_glue": False,
        "reason": "external_filtered_shadow_is_split",
    }
    assert bridge["internal_family_flag_is_exact_line_in_plane_data"] is True
    assert bridge["external_side_fixes_a_canonical_carrier_plane_u1"] is True
    assert bridge["carrier_metric_alone_is_line_blind_inside_u1"] is True
    assert bridge["full_external_packet_selects_a_canonical_line_candidate_inside_u1"] is True
    assert bridge["filtered_shadow_sign_order_fixes_the_same_canonical_u1_line_candidate"] is True
    assert bridge["transport_polarity_collapses_external_line_ambiguity_to_one_head_compatible_candidate"] is True
    assert bridge["external_side_still_matches_the_graded_shadow_of_the_transport_162_sector"] is True
    assert bridge["external_side_matches_a_canonical_filtered_split_shadow_of_the_transport_162_sector"] is True
    assert bridge["external_side_does_not_yet_realize_the_internal_rank_81_nilpotent_glue"] is True
    assert bridge["exact_external_identification_of_the_internal_common_line_is_not_yet_supported"] is True
    assert bridge["exact_external_identification_of_the_internal_transport_extension_is_not_yet_supported"] is True
    assert bridge["current_bridge_fixes_plane_line_candidate_and_filtered_shadow_but_not_full_extension_object"] is True


def test_synthesis_records_e13_visibility_obstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["e13_visibility_obstruction_bridge"]
    assert bridge["internal_common_square"] == [[0, 0, 2], [0, 0, 0], [0, 0, 0]]
    assert bridge["internal_common_line_generator"] == [1, 1, 0]
    assert bridge["external_canonical_carrier_plane"] == "U1"
    assert bridge["external_canonical_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_sign_ordered_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_head_compatible_line_candidate"] == [0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    assert bridge["external_graded_shadow"] == [81, 81]
    assert bridge["external_filtered_shadow"] == [81, 162, 81]
    assert bridge["external_nilpotent_glue_visibility"] == {
        "matches_internal_central_channel_glue": False,
        "reason": "external_filtered_shadow_is_split",
    }
    assert bridge["internal_common_square_is_exact_central_2e13_channel"] is True
    assert bridge["image_of_the_common_square_is_the_internal_common_line"] is True
    assert bridge["current_external_bridge_fixes_the_canonical_u1_carrier_plane"] is True
    assert bridge["current_external_bridge_picks_a_canonical_line_candidate_for_the_e13_image"] is True
    assert bridge["current_external_bridge_sign_orders_that_line_candidate_by_the_filtered_shadow_basis"] is True
    assert bridge["current_external_bridge_collapses_line_ambiguity_to_a_head_compatible_e13_candidate"] is True
    assert bridge["exact_external_identification_of_the_e13_image_with_the_internal_common_line_is_not_yet_supported"] is True
    assert bridge["current_external_bridge_matches_a_canonical_filtered_split_shadow_of_the_transport_channel"] is True
    assert bridge["current_external_bridge_does_not_yet_realize_the_rank_81_nilpotent_glue_of_the_transport_channel"] is True
    assert bridge["current_bridge_captures_carrier_plane_line_candidate_and_filtered_shadow_of_the_central_channel"] is True
    assert bridge["exact_external_realization_of_the_central_2e13_channel_is_not_yet_supported"] is True


def test_synthesis_records_curved_refinement_density_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    density = summary["curved_refinement_density_bridge"]
    assert density["vanishing_barycentric_modes"] == [2, 24]
    assert density["external_chain_density_limit"] == "120/19"
    assert density["external_trace_density_limit"] == "860/19"
    assert density["product_chain_density_limit"] == "19440/19"
    assert density["product_trace_density_limit"] == "7512120/19"
    assert density["cp2_six_mode"] == "156/19"
    assert density["k3_six_mode"] == "-880/19"
    assert density["cp2_step4_chain_density"] == pytest.approx(120.0 / 19.0)
    assert density["k3_step4_chain_density"] == pytest.approx(120.0 / 19.0)
    assert density["product_zero_modes_vanish_exactly"] is True


def test_synthesis_records_adjacency_dirac_closure_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["adjacency_dirac_closure_bridge"]
    assert bridge["vertex_laplacian_formula"] == "L0 = 12 I - A"
    assert bridge["vertex_laplacian_matches_formula_exactly"] is True
    assert bridge["vertex_laplacian_spectrum"] == {0: 1, 10: 24, 16: 15}
    assert bridge["edge_harmonic_dimension"] == 81
    assert bridge["edge_exact_dimension"] == 39
    assert bridge["edge_coexact_dimension"] == 120
    assert bridge["exact_one_form_spectrum_is_vertex_nonzero_spectrum"] is True
    assert bridge["triangle_laplacian_is_scalar_4"] is True
    assert bridge["tetrahedron_laplacian_is_scalar_4"] is True
    assert bridge["df2_spectrum"] == {0: 82, 4: 320, 10: 48, 16: 30}
    assert bridge["a0_f"] == 480
    assert bridge["a2_f"] == 2240
    assert bridge["a4_f"] == 17600
    assert bridge["mu_squared"] == "14/3"
    assert bridge["lambda"] == "110/3"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["full_finite_spectrum_forced_from_adjacency_plus_clique_regularities"] is True


def test_synthesis_records_three_channel_and_dual_bose_mesner_bridges() -> None:
    summary = build_refinement_bridge_synthesis()
    three_channel = summary["three_channel_operator_bridge"]
    dual = summary["dual_bose_mesner_bridge"]
    assert three_channel["basis"] == ["I", "A", "J"]
    assert three_channel["three_entry_classes"] == ["diagonal", "edge", "nonedge"]
    assert three_channel["positive_projector_entry_values"] == {
        "diagonal": "5/8",
        "edge": "1/8",
        "nonedge": "-1/24",
    }
    assert three_channel["laplacian_pseudoinverse_entry_values"] == {
        "diagonal": "267/3200",
        "edge": "7/3200",
        "nonedge": "-13/3200",
    }
    assert three_channel["effective_resistance_adjacent"] == "13/80"
    assert three_channel["effective_resistance_nonadjacent"] == "7/40"
    assert three_channel["kemeny_constant"] == "801/20"
    assert three_channel["exact_mixing_rate"] == "1/3"
    assert dual["w33_constant_projector_matches_exactly"] is True
    assert dual["transport_constant_projector_matches_exactly"] is True
    assert dual["shared_nontrivial_polynomial"] == "x^2 + 2x - 8"
    assert dual["kills_mean_zero_on_w33"] is True
    assert dual["kills_mean_zero_on_transport"] is True
    assert dual["positive_channel_coefficients"] == {"alpha": "2/3", "beta": "1/6"}
    assert dual["negative_channel_coefficients"] == {"alpha": "1/3", "beta": "-1/6"}


def test_synthesis_records_vacuum_unity_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["vacuum_unity_bridge"]
    assert bridge["alpha_inverse"] == "152247/1111"
    assert bridge["alpha"] == "1111/152247"
    assert bridge["unity_relation"] == "1"
    assert bridge["impedance_admittance_unity"] == "1"
    assert bridge["z0_equals_mu0_c"] is True
    assert bridge["z0_equals_one_over_epsilon0_c"] is True
    assert bridge["mu0_formula"] == "2 alpha h / (c e^2)"
    assert bridge["epsilon0_formula"] == "e^2 / (2 alpha h c)"
    assert bridge["z0_formula"] == "2 alpha h / e^2"
    assert bridge["mu0_prediction"].startswith("1.256637020705")
    assert bridge["epsilon0_prediction"].startswith("8.854188104604")
    assert bridge["z0_prediction"].startswith("3.767303012510")
    assert bridge["mu0_error_tracks_alpha"] is True
    assert bridge["epsilon0_error_tracks_negative_alpha"] is True
    assert bridge["z0_error_tracks_alpha"] is True
    assert bridge["selector_line_dimension"] == 1
    assert bridge["vacuum_unity_matches_selector_rank"] is True


def test_synthesis_records_quantum_vacuum_standards_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["quantum_vacuum_standards_bridge"]
    assert bridge["rk_formula"] == "h / e^2"
    assert bridge["kj_formula"] == "2 e / h"
    assert bridge["g0_formula"] == "2 e^2 / h"
    assert bridge["phi0_formula"] == "h / (2 e)"
    assert bridge["rk_prediction"].startswith("2.58128074593045066600455")
    assert bridge["kj_prediction"].startswith("4.83597848416983632447658")
    assert bridge["g0_prediction"].startswith("7.74809172986365064668082")
    assert bridge["phi0_prediction"].startswith("2.06783384846192932308111")
    assert bridge["phi0_times_kj"] == "1"
    assert bridge["rk_times_g0"] == "2"
    assert bridge["kj_squared_rk_h"] == "4"
    assert bridge["z0_equals_2_alpha_rk"] is True
    assert bridge["mu0_equals_2_alpha_rk_over_c"] is True
    assert bridge["epsilon0_equals_one_over_2_alpha_rk_c"] is True
    assert bridge["y0_equals_g0_over_4alpha"] is True
    assert bridge["alpha_from_z0_over_2rk"] == "1111/152247"
    assert bridge["alpha_from_z0_g0_over_4"] == "1111/152247"
    assert bridge["z0_times_g0"] == "4444/152247"
    assert bridge["rk_over_z0"] == "152247/2222"


def test_synthesis_records_natural_units_meaning_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_meaning_bridge"]
    assert bridge["convention"] == "hbar = c = epsilon0 = mu0 = Z0 = Y0 = 1"
    assert bridge["alpha_formula"] == "e_HL^2 / (4 pi)"
    assert bridge["e_hl_squared_symbolic"] == "4 pi alpha"
    assert bridge["e_hl_squared"] == pytest.approx(0.09170123386702556)
    assert bridge["e_hl"] == pytest.approx(0.30282211588162705)
    assert bridge["rk_natural_symbolic"] == "1 / (2 alpha)"
    assert bridge["rk_natural"] == pytest.approx(68.51800180018002)
    assert bridge["g0_natural_symbolic"] == "4 alpha"
    assert bridge["g0_natural"] == pytest.approx(0.029189409315126078)
    assert bridge["kj_natural"] == pytest.approx(0.09639127324021538)
    assert bridge["phi0_natural"] == pytest.approx(10.374383140555823)
    assert bridge["vacuum_unity_becomes_unit_element"] is True
    assert bridge["z0_equals_2alpha_rk_becomes_unit_identity"] is True
    assert bridge["alpha_equals_g0_over_4"] is True
    assert bridge["rk_times_g0_equals_2"] is True
    assert bridge["phi0_times_kj_equals_1"] is True
    assert bridge["gaussian_alpha_formula"] == "e_G^2"
    assert bridge["heaviside_equals_4pi_gaussian"] is True
    assert bridge["weinberg_x"] == "3/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["topological_over_continuum"] == "7"
    assert bridge["graphs_mean_couplings_and_mode_weights_in_natural_units"] is True
    assert bridge["si_vacuum_is_reexpression_of_dimensionless_package"] is True


def test_synthesis_records_natural_units_topological_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_topological_bridge"]
    assert bridge["q"] == 3
    assert bridge["lambda"] == 2
    assert bridge["mu"] == 4
    assert bridge["phi6"] == 7
    assert bridge["q_squared"] == 9
    assert bridge["lambda_plus_phi6"] == 9
    assert bridge["rk_formula"] == "1 / (lambda alpha)"
    assert bridge["g0_formula"] == "mu alpha"
    assert bridge["z0_unit_formula"] == "1 = lambda alpha R_K"
    assert bridge["y0_unit_formula"] == "1 = G_0 / (mu alpha)"
    assert bridge["flux_josephson_unit_formula"] == "Phi_0 K_J = 1"
    assert bridge["rk"] == "152247/2222"
    assert bridge["g0"] == "4444/152247"
    assert bridge["rk_times_g0"] == "2"
    assert bridge["mu_over_lambda"] == "2"
    assert bridge["packet_dimension"] == 7
    assert bridge["fano_selector_formula"] == "2I + J"
    assert bridge["toroidal_shell_formula"] == "7I - J"
    assert bridge["normalized_unit_formula"] == "I = ((2I + J) + (7I - J)) / 9"
    assert bridge["vacuum_unit_from_local_shell"] == "1"
    assert bridge["fano_nontrivial_trace"] == 12
    assert bridge["toroidal_nontrivial_trace"] == 42
    assert bridge["combined_nontrivial_trace"] == 54
    assert bridge["rk_equals_one_over_lambda_alpha"] is True
    assert bridge["g0_equals_mu_alpha"] is True
    assert bridge["z0_unit_matches_lambda_alpha_rk"] is True
    assert bridge["y0_unit_matches_g0_over_mu_alpha"] is True
    assert bridge["rk_times_g0_equals_mu_over_lambda"] is True
    assert bridge["lambda_plus_phi6_equals_q_squared"] is True
    assert bridge["vacuum_unit_equals_lambda_plus_phi6_over_q_squared"] is True
    assert bridge["normalized_complement_is_identity"] is True
    assert bridge["flux_josephson_unit_matches_selector_line"] is True
    assert bridge["unit_operator_matches_natural_vacuum"] is True
    assert bridge["transport_standards_live_on_same_local_shell"] is True


def test_synthesis_records_natural_units_electroweak_split_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_electroweak_split_bridge"]
    assert bridge["q"] == 3
    assert bridge["lambda"] == 2
    assert bridge["phi6"] == 7
    assert bridge["q_squared"] == 9
    assert bridge["theta_w33"] == 10
    assert bridge["phi3"] == 13
    assert bridge["local_unit_formula"] == "(lambda + Phi_6) / q^2 = 1"
    assert bridge["electroweak_unit_formula"] == "1 = q/Phi_3 + Theta(W33)/Phi_3"
    assert bridge["local_unit_value"] == "1"
    assert bridge["electroweak_unit_value"] == "1"
    assert bridge["weinberg_formula"] == "sin^2(theta_W) = q / Phi_3"
    assert bridge["cosine_formula"] == "cos^2(theta_W) = Theta(W33) / Phi_3"
    assert bridge["electric_reciprocal_formula"] == "(4 pi alpha) / e^2 = 1"
    assert bridge["weak_reciprocal_formula"] == "(4 pi alpha) / g^2 = q / Phi_3"
    assert bridge["hypercharge_reciprocal_formula"] == "(4 pi alpha) / g'^2 = Theta(W33) / Phi_3"
    assert bridge["neutral_reciprocal_formula"] == "(4 pi alpha) / g_Z^2 = q Theta(W33) / Phi_3^2"
    assert bridge["sin2_theta_w"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["q_over_phi3"] == "3/13"
    assert bridge["theta_over_phi3"] == "10/13"
    assert bridge["reciprocal_g"] == "3/13"
    assert bridge["reciprocal_gprime"] == "10/13"
    assert bridge["reciprocal_gz"] == "30/169"
    assert bridge["tan2_theta_w"] == "3/10"
    assert bridge["theta_over_q"] == "10/3"
    assert bridge["lambda_plus_phi6_equals_q_squared"] is True
    assert bridge["theta_equals_q_plus_phi6"] is True
    assert bridge["q_plus_theta_equals_phi3"] is True
    assert bridge["phi3_equals_2q_plus_phi6"] is True
    assert bridge["weinberg_equals_q_over_phi3"] is True
    assert bridge["cosine_equals_theta_over_phi3"] is True
    assert bridge["sin2_plus_cos2_equals_unity"] is True
    assert bridge["weak_reciprocal_matches_weinberg"] is True
    assert bridge["hypercharge_reciprocal_matches_cosine"] is True
    assert bridge["electric_reciprocal_harmonic_sum_closes"] is True
    assert bridge["g_squared_over_gprime_squared_equals_theta_over_q"] is True
    assert bridge["neutral_reciprocal_equals_q_theta_over_phi3_squared"] is True
    assert bridge["local_and_electroweak_are_nested_unit_laws"] is True


def test_synthesis_records_heawood_weinberg_denominator_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_weinberg_denominator_bridge"]
    assert bridge["middle_quadratic_polynomial"] == "x^2 - 6x + 7"
    assert bridge["shared_six_channel"] == 6
    assert bridge["phi6"] == 7
    assert bridge["phi3"] == 13
    assert bridge["theta_w33"] == 10
    assert bridge["denominator_formula"] == "Phi_3 = 6 + Phi_6"
    assert bridge["theta_formula"] == "Theta(W33) = q + Phi_6"
    assert bridge["weinberg_from_heawood_formula"] == "sin^2(theta_W) = q / (6 + Phi_6)"
    assert bridge["cosine_from_heawood_formula"] == "cos^2(theta_W) = (q + Phi_6) / (6 + Phi_6)"
    assert bridge["pmns23_from_heawood_formula"] == "sin^2(theta_23) = Phi_6 / (6 + Phi_6)"
    assert bridge["sin2_theta_w"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["q_over_heawood_denominator"] == "3/13"
    assert bridge["theta_over_heawood_denominator"] == "10/13"
    assert bridge["phi6_over_heawood_denominator"] == "7/13"
    assert bridge["phi3_equals_shared_six_plus_phi6"] is True
    assert bridge["theta_equals_q_plus_phi6"] is True
    assert bridge["weinberg_equals_q_over_heawood_denominator"] is True
    assert bridge["cosine_equals_theta_over_heawood_denominator"] is True
    assert bridge["pmns23_equals_phi6_over_heawood_denominator"] is True


def test_synthesis_records_heawood_q_center_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_q_center_bridge"]
    assert bridge["middle_quadratic_polynomial"] == "x^2 - 6x + 7"
    assert bridge["q_centered_formula"] == "x^2 - 2q x + Phi_6"
    assert bridge["root_formula"] == "x = q +- sqrt(lambda)"
    assert bridge["q"] == 3
    assert bridge["lambda"] == 2
    assert bridge["phi6"] == 7
    assert bridge["phi3"] == 13
    assert bridge["middle_branch_minus"] == "3 - sqrt(2)"
    assert bridge["middle_branch_plus"] == "3 + sqrt(2)"
    assert bridge["middle_shell_trace_exact"] == "36"
    assert bridge["middle_shell_pseudodeterminant_exact"] == "117649"
    assert bridge["linear_term_equals_2q"] is True
    assert bridge["constant_term_equals_phi6"] is True
    assert bridge["q_squared_minus_phi6_equals_lambda"] is True
    assert bridge["roots_equal_q_plus_minus_sqrt_lambda"] is True
    assert bridge["phi3_equals_2q_plus_phi6"] is True
    assert bridge["middle_trace_equals_q_times_gauge_dimension"] is True
    assert bridge["middle_pseudodeterminant_equals_phi6_to_6"] is True


def test_synthesis_records_heawood_involution_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_involution_bridge"]
    assert bridge["middle_quadratic_polynomial"] == "x^2 - 6x + 7"
    assert bridge["centered_quadratic_formula"] == "(x - q)^2 = lambda"
    assert bridge["operator_formula"] == "(P_mid (L_H - qI) P_mid)^2 = lambda P_mid"
    assert bridge["normalized_involution_formula"] == "J_mid = P_mid (L_H - qI) P_mid / sqrt(lambda)"
    assert bridge["q"] == 3
    assert bridge["lambda"] == 2
    assert bridge["phi6"] == 7
    assert bridge["adjacency_quartic_polynomial"] == "x^4 - 11*x^2 + 18"
    assert bridge["middle_projector_rank"] == 12
    assert bridge["q_squared_minus_phi6_equals_lambda"] is True
    assert bridge["centered_shell_relation_holds"] is True
    assert bridge["normalized_operator_is_involution"] is True
    assert bridge["middle_projector_is_idempotent"] is True
    assert bridge["middle_shell_rank_is_12"] is True


def test_synthesis_records_heawood_clifford_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_clifford_bridge"]
    assert bridge["gamma_formula"] == "Gamma = diag(I_7,-I_7)"
    assert bridge["gamma_mid_formula"] == "Gamma_mid = P_mid Gamma P_mid"
    assert bridge["j_mid_formula"] == "J_mid = P_mid (L_H - qI) P_mid / sqrt(lambda)"
    assert bridge["k_mid_formula"] == "K_mid = Gamma_mid J_mid"
    assert bridge["pi_plus_formula"] == "Pi_+ = (P_mid + J_mid)/2"
    assert bridge["pi_minus_formula"] == "Pi_- = (P_mid - J_mid)/2"
    assert bridge["middle_shell_rank"] == 12
    assert bridge["complex_rank"] == 6
    assert bridge["gamma_mid_squared_equals_middle_projector"] is True
    assert bridge["j_mid_squared_equals_middle_projector"] is True
    assert bridge["gamma_and_j_anticommute"] is True
    assert bridge["k_mid_squared_equals_minus_middle_projector"] is True
    assert bridge["pi_plus_is_projector"] is True
    assert bridge["pi_minus_is_projector"] is True
    assert bridge["pi_plus_pi_minus_zero"] is True
    assert bridge["pi_plus_rank_is_6"] is True
    assert bridge["pi_minus_rank_is_6"] is True
    assert bridge["middle_shell_is_12_equals_6_plus_6"] is True


def test_synthesis_records_natural_units_projective_denominator_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_projective_denominator_bridge"]
    assert bridge["fano_selector_formula"] == "B B^T = 2I + J"
    assert bridge["metrology_selector_formula"] == "B B^T = (R_K G_0) I + J"
    assert bridge["toroidal_shell_formula"] == "L_K7 = Phi_6 I - J"
    assert bridge["local_sum_formula"] == "B B^T + L_K7 = (R_K G_0 + Phi_6) I = q^2 I"
    assert bridge["q_from_selector_and_metrology_formula"] == "q = 1 + R_K G_0"
    assert bridge["shared_six_formula"] == "6 = 1 + q + R_K G_0"
    assert bridge["selector_line"] == 1
    assert bridge["q"] == 3
    assert bridge["rk_times_g0"] == "2"
    assert bridge["phi6"] == 7
    assert bridge["q_squared"] == 9
    assert bridge["phi3_formula"] == "Phi_3 = 1 + q + R_K G_0 + Phi_6"
    assert bridge["theta_formula"] == "Theta(W33) = 1 + R_K G_0 + Phi_6"
    assert bridge["phi3"] == 13
    assert bridge["theta_w33"] == 10
    assert bridge["selector_plus_projective_plus_shells"] == "13"
    assert bridge["theta_from_selector_and_shells"] == "10"
    assert bridge["sin2_theta_w_formula"] == "sin^2(theta_W) = q / (1 + q + R_K G_0 + Phi_6)"
    assert bridge["cos2_theta_w_formula"] == "cos^2(theta_W) = (1 + R_K G_0 + Phi_6) / (1 + q + R_K G_0 + Phi_6)"
    assert bridge["sin2_theta_w"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["q_over_projective_denominator"] == "3/13"
    assert bridge["theta_over_projective_denominator"] == "10/13"
    assert bridge["selector_coefficient_equals_metrology_coefficient"] is True
    assert bridge["q_equals_selector_line_plus_metrology_shell"] is True
    assert bridge["shared_six_equals_selector_plus_projective_plus_metrology_shell"] is True
    assert bridge["metrology_plus_qcd_shell_equals_q_squared"] is True
    assert bridge["phi3_equals_selector_plus_projective_plus_shells"] is True
    assert bridge["theta_equals_selector_plus_shells"] is True
    assert bridge["weinberg_equals_q_over_projective_denominator"] is True
    assert bridge["cosine_equals_theta_over_projective_denominator"] is True
    assert bridge["projective_denominator_rebuilds_from_natural_units_shells"] is True


def test_synthesis_records_natural_units_custodial_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_custodial_bridge"]
    assert bridge["phi3"] == 13
    assert bridge["theta_w33"] == 10
    assert bridge["selector_line"] == 1
    assert bridge["q"] == 3
    assert bridge["rk_times_g0"] == "2"
    assert bridge["phi6"] == 7
    assert bridge["custodial_numerator_formula"] == "Theta(W33) = 1 + R_K G_0 + Phi_6"
    assert bridge["denominator_formula"] == "Phi_3 = 1 + q + R_K G_0 + Phi_6"
    assert bridge["mass_ratio_formula"] == "m_W^2 / m_Z^2 = Theta(W33) / Phi_3"
    assert bridge["gap_formula"] == "(m_Z^2 - m_W^2) / m_Z^2 = q / Phi_3"
    assert bridge["mw_squared_over_mz_squared"] == "10/13"
    assert bridge["z_gap_over_z_squared"] == "3/13"
    assert bridge["sin2_theta_w"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["theta_over_phi3"] == "10/13"
    assert bridge["q_over_phi3"] == "3/13"
    assert bridge["rho_parameter"] == "1"
    assert bridge["theta_equals_selector_plus_metrology_plus_qcd"] is True
    assert bridge["phi3_equals_selector_plus_projective_plus_metrology_plus_qcd"] is True
    assert bridge["mw_over_mz_squared_equals_cos2_theta_w"] is True
    assert bridge["z_gap_over_z_squared_equals_sin2_theta_w"] is True
    assert bridge["cos2_equals_theta_over_phi3"] is True
    assert bridge["sin2_equals_q_over_phi3"] is True
    assert bridge["custodial_split_sums_to_unity"] is True
    assert bridge["rho_equals_one"] is True


def test_synthesis_records_natural_units_sigma_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_sigma_shell_bridge"]
    assert bridge["sigma_formula"] == "sigma = 1 + q + R_K G_0"
    assert bridge["sigma"] == 6
    assert bridge["metrology_eigenvalue"] == 2
    assert bridge["toroidal_eigenvalue"] == 7
    assert bridge["complement_eigenvalue"] == 9
    assert bridge["phi3_formula"] == "Phi_3 = sigma + Phi_6"
    assert bridge["heawood_middle_rank_formula"] == "rank_mid(Heawood) = 2 sigma"
    assert bridge["heawood_middle_trace_formula"] == "Tr(L_H|mid) = 2 q sigma"
    assert bridge["metrology_trace"] == 12
    assert bridge["toroidal_trace"] == 42
    assert bridge["complement_trace"] == 54
    assert bridge["heawood_middle_rank"] == 12
    assert bridge["heawood_middle_trace"] == 36
    assert bridge["single_surface_flags"] == 84
    assert bridge["dual_pair_flags"] == 168
    assert bridge["full_heawood_order"] == 336
    assert bridge["sigma_equals_selector_plus_projective_plus_metrology"] is True
    assert bridge["phi3_equals_sigma_plus_phi6"] is True
    assert bridge["metrology_trace_equals_sigma_times_rk_times_g0"] is True
    assert bridge["toroidal_trace_equals_sigma_times_phi6"] is True
    assert bridge["complement_trace_equals_sigma_times_q_squared"] is True
    assert bridge["complement_trace_equals_metrology_plus_toroidal_trace"] is True
    assert bridge["heawood_middle_rank_equals_two_sigma"] is True
    assert bridge["heawood_middle_trace_equals_two_q_sigma"] is True
    assert bridge["single_surface_flags_equals_two_toroidal_traces"] is True
    assert bridge["dual_pair_flags_equals_four_toroidal_traces"] is True
    assert bridge["full_heawood_order_equals_eight_toroidal_traces"] is True


def test_synthesis_records_natural_units_neutral_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_neutral_shell_bridge"]
    assert bridge["neutral_numerator_formula"] == "q Theta(W33)"
    assert bridge["neutral_reciprocal_formula"] == "(4 pi alpha) / g_Z^2 = q Theta(W33) / Phi_3^2"
    assert bridge["q"] == 3
    assert bridge["theta_w33"] == 10
    assert bridge["phi3"] == 13
    assert bridge["sigma"] == 6
    assert bridge["q_squared"] == 9
    assert bridge["rk_times_g0"] == 2
    assert bridge["phi6"] == 7
    assert bridge["ag21_length"] == 21
    assert bridge["neutral_numerator"] == 30
    assert bridge["neutral_reciprocal"] == "30/169"
    assert bridge["single_surface_flags"] == 84
    assert bridge["complement_trace"] == 54
    assert bridge["neutral_numerator_equals_q_times_theta"] is True
    assert bridge["neutral_reciprocal_equals_q_theta_over_phi3_squared"] is True
    assert bridge["q_times_rk_times_g0_equals_sigma"] is True
    assert bridge["q_times_phi6_equals_ag21"] is True
    assert bridge["neutral_numerator_equals_q_plus_sigma_plus_ag21"] is True
    assert bridge["complement_trace_equals_sigma_times_q_squared"] is True
    assert bridge["surface_flags_equals_complement_trace_plus_neutral_numerator"] is True


def test_synthesis_records_natural_units_root_gap_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_root_gap_bridge"]
    assert bridge["quadratic_formula"] == "t^2 - t + q Theta(W33) / Phi_3^2 = 0"
    assert bridge["sum_formula"] == "x + y = 1"
    assert bridge["product_formula"] == "xy = q Theta(W33) / Phi_3^2"
    assert bridge["discriminant_formula"] == "1 - 4 q Theta(W33) / Phi_3^2 = Phi_6^2 / Phi_3^2"
    assert bridge["gap_formula"] == "y - x = Phi_6 / Phi_3 = sin^2(theta_23)"
    assert bridge["weak_root_formula"] == "x = (1 - Phi_6 / Phi_3) / 2 = q / Phi_3"
    assert bridge["hypercharge_root_formula"] == "y = (1 + Phi_6 / Phi_3) / 2 = Theta(W33) / Phi_3"
    assert bridge["q"] == 3
    assert bridge["theta_w33"] == 10
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["weak_share"] == "3/13"
    assert bridge["hypercharge_share"] == "10/13"
    assert bridge["neutral_product"] == "30/169"
    assert bridge["discriminant"] == "49/169"
    assert bridge["root_gap"] == "7/13"
    assert bridge["atmospheric_share"] == "7/13"
    assert bridge["weak_plus_hypercharge_equals_unity"] is True
    assert bridge["weak_times_hypercharge_equals_neutral_product"] is True
    assert bridge["discriminant_equals_phi6_squared_over_phi3_squared"] is True
    assert bridge["root_gap_equals_phi6_over_phi3"] is True
    assert bridge["root_gap_equals_atmospheric_share"] is True
    assert bridge["weak_root_reconstructs_from_gap"] is True
    assert bridge["hypercharge_root_reconstructs_from_gap"] is True
    assert bridge["weak_root_equals_q_over_phi3"] is True
    assert bridge["hypercharge_root_equals_theta_over_phi3"] is True
    assert bridge["heawood_denominator_matches_root_gap"] is True


def test_synthesis_records_heawood_electroweak_polarization_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_electroweak_polarization_bridge"]
    assert bridge["operator_formula"] == "R_EW = (q Pi_- + Theta(W33) Pi_+) / Phi_3"
    assert bridge["projector_form_formula"] == "R_EW = P_mid/2 + (Phi_6 / (2 Phi_3)) J_mid"
    assert bridge["centered_gap_formula"] == "2 R_EW - P_mid = (Phi_6 / Phi_3) J_mid"
    assert bridge["quadratic_formula"] == "R_EW^2 - R_EW + (q Theta(W33)/Phi_3^2) P_mid = 0"
    assert bridge["reduced_packet_formula"] == "M_EW = [[1/2, Phi_6/(2 Phi_3)], [Phi_6/(2 Phi_3), 1/2]]"
    assert bridge["q"] == 3
    assert bridge["theta_w33"] == 10
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["middle_rank"] == 12
    assert bridge["complex_rank"] == 6
    assert bridge["weak_share"] == "3/13"
    assert bridge["hypercharge_share"] == "10/13"
    assert bridge["neutral_product"] == "30/169"
    assert bridge["root_gap"] == "7/13"
    assert bridge["polarization_amplitude"] == "7/26"
    assert bridge["middle_trace"] == 36
    assert bridge["reduced_trace"] == "1"
    assert bridge["reduced_determinant"] == "30/169"
    assert bridge["reduced_eigenvalue_minus"] == "3/13"
    assert bridge["reduced_eigenvalue_plus"] == "10/13"
    assert bridge["pi_plus_rank_is_6"] is True
    assert bridge["pi_minus_rank_is_6"] is True
    assert bridge["polarization_operator_has_expected_trace"] is True
    assert bridge["average_trace_on_middle_shell_equals_half"] is True
    assert bridge["operator_equals_projector_plus_polarization_form"] is True
    assert bridge["centered_gap_is_atmospheric_selector"] is True
    assert bridge["operator_satisfies_neutral_shell_quadratic"] is True
    assert bridge["reduced_packet_trace_is_one"] is True
    assert bridge["reduced_packet_determinant_is_neutral_product"] is True
    assert bridge["reduced_packet_eigenvalues_match_weak_and_hypercharge"] is True
    assert bridge["neutral_numerator_is_heawood_trace_minus_clifford_rank"] is True
    assert bridge["clifford_packet_is_available"] is True


def test_synthesis_records_natural_units_cosmological_complement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_cosmological_complement_bridge"]
    assert bridge["reduced_complement_formula"] == "I_2 - (2 M_EW - I_2)^2 = ((Phi_3^2 - Phi_6^2)/Phi_3^2) I_2"
    assert bridge["lifted_complement_formula"] == "P_mid - (2 R_EW - P_mid)^2 = ((Phi_3^2 - Phi_6^2)/Phi_3^2) P_mid"
    assert bridge["numerator_formula"] == "Phi_3^2 - Phi_6^2 = 4 q Theta(W33)"
    assert bridge["surface_formula"] == "120 = 84 + 36"
    assert bridge["q"] == 3
    assert bridge["theta_w33"] == 10
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["root_gap"] == "7/13"
    assert bridge["cosmological_fraction"] == "120/169"
    assert bridge["cosmological_numerator"] == 120
    assert bridge["single_surface_flags"] == 84
    assert bridge["heawood_middle_trace"] == 36
    assert bridge["middle_rank"] == 12
    assert bridge["external_chain_density_limit"] == "120/19"
    assert bridge["cosmological_numerator_equals_phi3_squared_minus_phi6_squared"] is True
    assert bridge["cosmological_numerator_equals_4_q_theta"] is True
    assert bridge["cosmological_fraction_equals_one_minus_gap_squared"] is True
    assert bridge["reduced_complement_is_120_over_169_identity"] is True
    assert bridge["four_det_equals_cosmological_fraction"] is True
    assert bridge["surface_plus_middle_trace_equals_120"] is True
    assert bridge["lifted_coefficient_matches_cosmological_fraction"] is True
    assert bridge["lifted_average_trace_matches_cosmological_fraction"] is True
    assert bridge["curved_bridge_uses_universal_120_mode"] is True


def test_synthesis_records_natural_units_unit_balance_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["natural_units_unit_balance_bridge"]
    assert bridge["reduced_balance_formula"] == "I_2 = (2 M_EW - I_2)^2 + 4 det(M_EW) I_2"
    assert bridge["lifted_balance_formula"] == "P_mid = (2 R_EW - P_mid)^2 + ((Phi_3^2 - Phi_6^2)/Phi_3^2) P_mid"
    assert bridge["mixed_product_formula"] == "I_2 - (2 M_EW - I_2)^2 = 4 M_EW (I_2 - M_EW)"
    assert bridge["fraction_formula"] == "1 = (Phi_6/Phi_3)^2 + (Phi_3^2 - Phi_6^2)/Phi_3^2"
    assert bridge["numerator_formula"] == "Phi_3^2 = Phi_6^2 + (Phi_3^2 - Phi_6^2)"
    assert bridge["shell_balance_formula"] == "169 = 84 + 36 + 49"
    assert bridge["shell_formula"] == "169 = 84 + 36 + 42 + 7"
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["denominator_square"] == 169
    assert bridge["polarization_fraction"] == "49/169"
    assert bridge["cosmological_fraction"] == "120/169"
    assert bridge["polarization_numerator"] == 49
    assert bridge["cosmological_numerator"] == 120
    assert bridge["single_surface_flags"] == 84
    assert bridge["heawood_middle_trace"] == 36
    assert bridge["toroidal_trace"] == 42
    assert bridge["qcd_selector"] == 7
    assert bridge["reduced_balance_is_identity"] is True
    assert bridge["polarization_fraction_equals_gap_squared"] is True
    assert bridge["cosmological_fraction_equals_four_det"] is True
    assert bridge["unit_splits_into_polarization_plus_complement"] is True
    assert bridge["denominator_square_equals_two_numerators"] is True
    assert bridge["polarization_numerator_equals_toroidal_trace_plus_qcd_selector"] is True
    assert bridge["cosmological_numerator_equals_surface_plus_heawood_trace"] is True
    assert bridge["denominator_square_equals_surface_heawood_plus_polarization"] is True
    assert bridge["denominator_square_equals_surface_heawood_toroidal_qcd_shells"] is True


def test_synthesis_records_electroweak_lagrangian_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["electroweak_lagrangian_bridge"]
    assert bridge["vev_ew_gev"] == 246
    assert bridge["weinberg_x"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["lambda_h"] == "7/55"
    assert bridge["g_squared_over_4pi_alpha"] == "13/3"
    assert bridge["gprime_squared_over_4pi_alpha"] == "13/10"
    assert bridge["gz_squared_over_4pi_alpha"] == "169/30"
    assert bridge["one_over_e_squared_equals_sum"] is True
    assert bridge["g_squared_over_gprime_squared"] == "10/3"
    assert bridge["rho_parameter"] == "1"
    assert bridge["mw_squared_over_mz_squared"] == "10/13"
    assert bridge["e"].startswith("3.0282211588162705")
    assert bridge["g"].startswith("6.303745025171762")
    assert bridge["gprime"].startswith("3.452703347047545")
    assert bridge["gZ"].startswith("7.18737516379179")
    assert bridge["mw_tree_gev"].startswith("7.753606380961267")
    assert bridge["mz_tree_gev"].startswith("8.840471451463902")
    assert bridge["mh_tree_gev"].startswith("1.241131448609402")
    assert bridge["fermi_constant_tree"].startswith("1.168462524268867")
    assert bridge["e_equals_g_sin_theta"] is True
    assert bridge["e_equals_gprime_cos_theta"] is True
    assert bridge["mz_equals_mw_over_cos_theta"] is True
    assert bridge["mh_equals_v_sqrt_2lambda"] is True
    assert bridge["gf_equals_one_over_sqrt2_v2"] is True


def test_synthesis_records_one_scale_bosonic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["one_scale_bosonic_bridge"]
    assert bridge["vev_ew_gev"] == 246
    assert bridge["weinberg_x"] == "3/13"
    assert bridge["cos2_theta_w"] == "10/13"
    assert bridge["lambda_h"] == "7/55"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["mu_h_squared_over_v_squared"] == "7/55"
    assert bridge["mh_squared_over_v_squared"] == "14/55"
    assert bridge["vacuum_energy_over_v_fourth"] == "-7/220"
    assert bridge["mu_equals_lambda_v_squared"] is True
    assert bridge["mh_squared_equals_2lambda_v_squared"] is True
    assert bridge["vacuum_energy_equals_minus_lambda_v_fourth_over_4"] is True
    assert bridge["mw_squared_over_mz_squared"] == "10/13"
    assert bridge["z_minus_w_split_over_z"] == "3/13"
    assert bridge["rho_parameter"] == "1"
    assert bridge["mw_over_v"].startswith("3.151872512585881")
    assert bridge["mz_over_v"].startswith("3.593687581895895")
    assert bridge["mh_over_v"].startswith("5.04524979109513")
    assert bridge["mw_over_mz_equals_sqrt_cos2"] is True
    assert bridge["mh_over_v_equals_sqrt_higgs_ratio"] is True
    assert bridge["all_dimensionless_bosonic_data_fixed"] is True
    assert bridge["only_overall_scale_is_v"] is True
    assert bridge["vev_is_graph_fixed_as_q5_plus_q"] is True
    assert bridge["vev_is_graph_fixed_as_edges_plus_2q"] is True
    assert bridge["zero_extra_parameter_bosonic_closure_if_promoted_vev_accepted"] is True


def test_synthesis_records_bosonic_action_completion_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["bosonic_action_completion_bridge"]
    assert bridge["lagrangian_formula"].startswith("L_bos = -1/4 W^a_{mu nu}")
    assert bridge["covariant_derivative_formula"] == "D_mu = partial_mu - i g tau^a W^a_mu / 2 - i g' B_mu / 2"
    assert bridge["potential_formula"] == "V(H) = -mu_H^2 (H^dagger H) + lambda_H (H^dagger H)^2"
    assert bridge["alpha"] == "1111/152247"
    assert bridge["weinberg_x"] == "3/13"
    assert bridge["lambda_h"] == "7/55"
    assert bridge["vev_ew_gev"] == 246
    assert bridge["g_squared_over_4pi_alpha"] == "13/3"
    assert bridge["gprime_squared_over_4pi_alpha"] == "13/10"
    assert bridge["gz_squared_over_4pi_alpha"] == "169/30"
    assert bridge["g_squared_over_gprime_squared"] == "10/3"
    assert bridge["mw_squared_over_mz_squared"] == "10/13"
    assert bridge["rho_parameter"] == "1"
    assert bridge["mu_h_squared_over_v_squared"] == "7/55"
    assert bridge["mh_squared_over_v_squared"] == "14/55"
    assert bridge["vacuum_energy_over_v_fourth"] == "-7/220"
    assert bridge["canonical_gauge_kinetics_fixed"] is True
    assert bridge["covariant_derivative_fixed_by_alpha_and_x"] is True
    assert bridge["higgs_potential_fixed_by_x_and_v"] is True
    assert bridge["no_free_bosonic_parameter_beyond_graph_fixed_alpha_x_v"] is True
    assert bridge["graph_fixes_full_tree_level_bosonic_electroweak_action"] is True


def test_synthesis_records_standard_model_action_backbone_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["standard_model_action_backbone_bridge"]
    assert bridge["alpha"] == "1111/152247"
    assert bridge["weinberg_x"] == "3/13"
    assert bridge["lambda_h"] == "7/55"
    assert bridge["vev_ew_gev"] == 246
    assert bridge["mw_squared_over_mz_squared"] == "10/13"
    assert bridge["rho_parameter"] == "1"
    assert bridge["one_generation_spinor_dimension"] == 16
    assert bridge["three_generation_matter_dimension"] == 48
    assert bridge["left_right_split"] == "8+8"
    assert bridge["one_generation_counts"] == {
        "Q": 6,
        "u_c": 3,
        "d_c": 3,
        "L": 2,
        "e_c": 1,
        "nu_c": 1,
    }
    assert bridge["clean_higgs_slots"] == ["H_2", "Hbar_2"]
    assert bridge["tan_theta_c"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["all_anomalies_cancel"] is True
    assert bridge["full_bosonic_action_fixed"] is True
    assert bridge["decomposition_16_equals_6_3_3_2_1_1"] is True
    assert bridge["clean_higgs_pair_is_h2_hbar2"] is True
    assert bridge["bosonic_action_complete"] is True
    assert bridge["fermion_representations_complete"] is True
    assert bridge["mixing_backbone_complete"] is True
    assert bridge["anomaly_backbone_complete"] is True
    assert bridge["full_yukawa_eigenvalue_spectrum_still_open"] is True


def test_synthesis_records_q3_fermion_hierarchy_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["q3_fermion_hierarchy_bridge"]
    assert bridge["alpha_inverse_exact"] == "152247/1111"
    assert bridge["alpha_tree_inverse"] == "137"
    assert bridge["gaussian_norm_mu_plus_i"] == "17"
    assert bridge["up_sector_suppressor"] == "136"
    assert bridge["alpha_tree_minus_one_equals_up_sector_suppressor"] is True
    assert bridge["vertex_correction_term"] == "40/1111"
    assert bridge["mc_over_mt"] == "1/136"
    assert bridge["mu_over_mc"] == "1/544"
    assert bridge["mb_over_mc"] == "13/4"
    assert bridge["ms_over_mb"] == "1/44"
    assert bridge["md_over_ms"] == "1/20"
    assert bridge["mmu_over_me"] == "208"
    assert bridge["charm_suppressor_is_alpha_tree_minus_one"] is True
    assert bridge["bottom_ratio_is_projective_plane_over_line"] is True
    assert bridge["strange_ratio_is_inverse_nonbacktracking_degree_times_mu"] is True
    assert bridge["down_ratio_is_lambda_over_v"] is True
    assert bridge["muon_ratio_is_phi3_mu_squared"] is True


def test_synthesis_records_alpha_hierarchy_gaussian_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["alpha_hierarchy_gaussian_bridge"]
    assert bridge["outer_alpha_formula"] == "|(k-1) + i mu|^2"
    assert bridge["outer_alpha_vector"] == [11, 4]
    assert bridge["outer_alpha_norm"] == "137"
    assert bridge["inner_hierarchy_formula"] == "|mu + i|^2"
    assert bridge["inner_hierarchy_vector"] == [4, 1]
    assert bridge["inner_hierarchy_norm"] == "17"
    assert bridge["transport_prefactor"] == "8"
    assert bridge["up_sector_suppressor"] == "136"
    assert bridge["selector_line_dimension"] == "1"
    assert bridge["alpha_tree_equals_up_sector_plus_selector"] is True
    assert bridge["vertex_correction_term"] == "40/1111"
    assert bridge["alpha_full_equals_nested_shell_plus_vertex_correction"] is True
    assert bridge["mc_over_mt"] == "1/136"
    assert bridge["mu_over_mc"] == "1/544"
    assert bridge["charm_ratio_is_inverse_selector_reduced_tree_alpha"] is True
    assert bridge["second_up_step_is_extra_mu_factor"] is True


def test_synthesis_records_qcd_beta_phi6_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["qcd_beta_phi6_bridge"]
    assert bridge["beta0_formula"] == "11 - 2 n_f / 3"
    assert bridge["beta0_su3"] == "7"
    assert bridge["phi6_formula"] == "q^2 - q + 1"
    assert bridge["phi6_q3"] == "7"
    assert bridge["pmns_atmospheric_ratio"] == "7/13"
    assert bridge["higgs_quartic"] == "7/55"
    assert bridge["topological_over_continuum_ratio"] == "7"
    assert bridge["beta0_equals_phi6"] is True
    assert bridge["positive_integer_solution_of_phi6_equals_7"] == [3]


def test_synthesis_records_jones_mu4_selector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["jones_mu4_selector_bridge"]
    assert bridge["jones_value_set"] == "{4 cos^2(pi/n) : n >= 3} union [4, infinity)"
    assert bridge["critical_boundary"] == "4"
    assert bridge["mu"] == "4"
    assert bridge["spectral_gap"] == "4"
    assert bridge["external_dimension"] == "4"
    assert bridge["mu_equals_q_plus_one"] is True
    assert bridge["mu_hits_jones_boundary"] is True
    assert bridge["mu_equals_spectral_gap"] is True
    assert bridge["mu_equals_external_dimension"] is True
    assert bridge["positive_integer_solution_of_q_plus_one_equals_4"] == [3]


def test_synthesis_records_f4_neutrino_scale_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["f4_neutrino_scale_bridge"]
    assert bridge["f4_dimension"] == 52
    assert bridge["vev_ew_gev"] == 246
    assert bridge["mr_over_vew"] == "1/52"
    assert bridge["mnu_over_me_squared_if_dirac_seed_is_electron"] == "26/123"
    assert bridge["f4_dimension_equals_phi3_times_mu"] is True
    assert bridge["f4_dimension_equals_v_plus_k"] is True
    assert bridge["majorana_scale_is_inverse_f4_dimension"] is True
    assert bridge["seesaw_coefficient_is_exact_f4_over_vew"] is True
    assert bridge["seesaw_coefficient_reduces_to_26_over_123"] is True


def test_synthesis_records_one_input_fermion_spectrum_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["one_input_fermion_spectrum_bridge"]
    assert bridge["vev_ew_gev"] == 246
    assert bridge["mt_over_vew"] == "sqrt(2)/2"
    assert bridge["mc_over_vew"] == "sqrt(2)/272"
    assert bridge["mu_over_vew"] == "sqrt(2)/147968"
    assert bridge["mb_over_vew"] == "13*sqrt(2)/1088"
    assert bridge["ms_over_vew"] == "13*sqrt(2)/47872"
    assert bridge["md_over_vew"] == "13*sqrt(2)/957440"
    assert bridge["mu_over_mt"] == "1/73984"
    assert bridge["residual_seed"] == "m_e"
    assert bridge["mmu_over_me"] == "208"
    assert bridge["koide_q"] == "2/3"
    assert bridge["sqrt_mtau_over_me"] == "2 + sqrt(48*sqrt(13) + 627) + 8*sqrt(13)"
    assert bridge["mtau_over_me_minpoly"] == "y**4 - 5852*y**3 + 8322694*y**2 - 302918748*y + 1628364609"
    assert bridge["mnu_over_me_squared_if_dirac_seed_is_electron"] == "26/123"
    assert bridge["quark_ladder_fixed_by_graph_scale_and_q3_ratios"] is True
    assert bridge["charged_lepton_ladder_reduced_to_one_electron_seed"] is True
    assert bridge["koide_packet_closes_tau_over_e_algebraically"] is True
    assert bridge["neutrino_scale_reduced_to_same_electron_seed_plus_f4_coefficient"] is True
    assert bridge["remaining_fermion_frontier_is_one_seed_plus_final_internal_spectral_packet"] is True


def test_synthesis_records_l3_pfaffian_packet_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l3_pfaffian_packet_bridge"]
    assert bridge["support_count"] == 2592
    assert bridge["plus_count"] == 1296
    assert bridge["minus_count"] == 1296
    assert bridge["balanced_signs"] is True
    assert bridge["all_supported_entries_are_antisymmetric"] is True
    assert bridge["vector_vev_count"] == 10
    assert bridge["all_vector_packets_have_determinant_plus_one"] is True
    assert bridge["all_vector_packets_have_full_skew_rank"] is True
    assert bridge["type_a_directions"] == [17, 19, 24, 26]
    assert bridge["type_a_charpoly"] == "(x**2 + 1)**4*(x**8 + 22*x**6 + 87*x**4 + 26*x**2 + 1)"
    assert bridge["type_b_directions"] == [18, 20, 23, 25]
    assert bridge["type_b_charpoly"] == "(x**2 + 1)**4*(x**8 + 22*x**6 + 123*x**4 + 26*x**2 + 1)"
    assert bridge["democratic_directions"] == [21, 22]
    assert bridge["democratic_labels"] == ["H", "Hbar"]
    assert bridge["democratic_characteristic_polynomial"] == "(x**2 + 1)**8"
    assert bridge["democratic_packet_is_exactly_higgs_higgsbar"] is True
    assert bridge["remaining_direction_labels"] == ["H", "Hbar", "T", "T", "T", "Tbar", "Tbar", "Tbar"]


def test_synthesis_records_selector_firewall_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["selector_firewall_bridge"]
    assert bridge["identity"] == "A^2 + 2A - 8I = 4J"
    assert bridge["srg_parameters"] == [40, 12, 2, 4]
    assert bridge["identity_holds_for_canonical_w33"] is True
    assert bridge["classification_count_for_srg_40_12_2_4"] == 28
    assert bridge["master_equation_alone_does_not_force_unique_graph"] is True
    assert bridge["canonical_realization"] == "symplectic W(3,3) on PG(3,3)"
    assert bridge["gf3_rank_of_adjacency"] == 39
    assert bridge["gf3_rank_selector_matches_v_minus_1"] is True
    assert bridge["all_neighborhoods_decompose_as_4K3"] is True
    assert bridge["neighborhood_component_sizes"] == [3, 3, 3, 3]
    assert bridge["symplectic_group_order"] == 51840


def test_synthesis_records_theta_hierarchy_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["theta_hierarchy_bridge"]
    assert bridge["lovasz_theta"] == "10"
    assert bridge["theta_complement"] == "4"
    assert bridge["theta_times_theta_complement"] == "40"
    assert bridge["theta_times_theta_complement_equals_v"] is True
    assert bridge["small_selector_formula"] == "1/Theta(W33) = mu/v"
    assert bridge["small_selector"] == "1/10"
    assert bridge["mu_over_v"] == "1/10"
    assert bridge["selector_matches_mu_over_v"] is True
    assert bridge["selector_times_theta_is_unity"] is True
    assert bridge["betti_numbers"] == [1, 81, 40]
    assert bridge["zero_mode_count"] == 122
    assert bridge["zero_mode_formula"] == "k^2 - k - Theta(W33)"
    assert bridge["zero_mode_formula_value"] == 122
    assert bridge["betti_sum_equals_formula"] is True


def test_synthesis_records_truncated_dirac_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["truncated_dirac_shell_bridge"]
    assert bridge["chain_dimensions"] == [40, 240, 160]
    assert bridge["total_dimension"] == 440
    assert bridge["boundary_ranks"] == [39, 120]
    assert bridge["betti_numbers"] == [1, 81, 40]
    assert bridge["zero_mode_count"] == 122
    assert bridge["lovasz_theta"] == 10
    assert bridge["zero_mode_formula"] == "k^2 - k - Theta(W33)"
    assert bridge["zero_mode_formula_value"] == 122
    assert bridge["zero_modes_equal_graph_formula"] is True
    assert bridge["d2_spectrum"] == {"0": 122, "4": 240, "10": 48, "16": 30}
    assert bridge["f0"] == 440
    assert bridge["f2"] == 1920
    assert bridge["f4"] == 16320
    assert bridge["f6"] == 186240
    assert bridge["f2_over_f0"] == "48/11"
    assert bridge["f4_over_f2"] == "17/2"
    assert bridge["f6_over_f4"] == "194/17"
    assert bridge["f2_over_f0_formula"] == "mu*k/(k-1)"
    assert bridge["f4_over_f2_formula"] == "(k+mu+1)/2"
    assert bridge["f2_over_f0_matches_formula"] is True
    assert bridge["f4_over_f2_matches_formula"] is True
    assert bridge["f2_equals_k_times_triangle_count"] is True


def test_synthesis_records_yukawa_scaffold_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_scaffold_bridge"]
    assert bridge["clean_higgs_slots"] == ["H_2", "Hbar_2"]
    assert bridge["clean_higgs_pair_is_h2_hbar2"] is True
    assert bridge["one_generation_spinor_dimension"] == 16
    assert bridge["three_generation_matter_dimension"] == 48
    assert bridge["label_matrix"] == [
        ["AB", "I", "A"],
        ["AB", "I", "A"],
        ["A", "B", "0"],
    ]
    assert bridge["label_matrix_is_slot_independent"] is True
    assert bridge["reconstructs_exactly_for_both_slots"] is True
    assert bridge["generation_0_diagonal_delta_equals_offdiag_1_to_0"] is True
    assert bridge["generation_1_diagonal_delta_equals_offdiag_0_to_1"] is True
    assert bridge["generation_2_diagonal_block_unchanged"] is True
    assert bridge["h2_split"] == {
        "minus_plus": ["u_c_1", "u_c_3"],
        "plus_minus": ["u_c_2", "nu_c"],
    }
    assert bridge["hbar2_split"] == {
        "minus_plus": ["d_c_1"],
        "plus_minus": ["d_c_2", "d_c_3", "e_c"],
    }
    assert bridge["minimal_full_a2_activation_seed_modes"] == [[8, 9], [246, 247]]
    assert bridge["minimal_rank_lift_seed_modes"] == [[8, 246], [8, 247], [9, 246], [9, 247]]
    assert bridge["max_response_rank_within_unit_seed_family"] == 11
    assert bridge["max_augmented_rank_within_unit_seed_family"] == 12
    assert bridge["generated_source_unit_count"] == 144
    assert bridge["projected_mode_count"] == 54
    assert bridge["response_rank"] == 28
    assert bridge["augmented_rank"] == 28
    assert bridge["arbitrary_quark_screen_rank"] == 36
    assert bridge["arbitrary_quark_screen_nullity"] == 0
    assert bridge["trivial_closure_total_residual_norm"] == 0.0
    assert bridge["zero_is_unique_clean_point"] is True
    assert bridge["l4_response_contained_in_ce2"] is True
    assert bridge["yukawa_scaffold_is_exact"] is True
    assert bridge["nonzero_yukawa_eigenvalues_still_open"] is True
    assert bridge["exact_open_problem_is_spectrum_not_support_or_symmetry"] is True


def test_synthesis_records_yukawa_unipotent_reduction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_unipotent_reduction_bridge"]
    assert bridge["h2_plus_minus_support"] == ["u_c_2", "nu_c"]
    assert bridge["h2_minus_plus_support"] == ["u_c_1", "u_c_3"]
    assert bridge["hbar2_plus_minus_support"] == ["d_c_2", "d_c_3", "e_c"]
    assert bridge["hbar2_minus_plus_support"] == ["d_c_1"]
    assert bridge["h2_plus_minus_compressed_rank"] == 6
    assert bridge["h2_minus_plus_compressed_rank"] == 6
    assert bridge["hbar2_plus_minus_compressed_rank"] == 9
    assert bridge["hbar2_minus_plus_compressed_rank"] == 3
    assert bridge["all_active_sector_block_spans_have_rank_2"] is True
    assert bridge["all_active_sector_ranks_saturate_three_generation_support"] is True
    assert bridge["plus_minus_generation_matrix"] == [
        [0, 1, 1],
        [-1, 2, 1],
        [1, -1, 1],
    ]
    assert bridge["minus_plus_generation_matrix"] == [
        [0, 1, -1],
        [-1, 2, -1],
        [-1, 1, 1],
    ]
    assert bridge["plus_minus_charpoly"] == "(lambda - 1)**3"
    assert bridge["minus_plus_charpoly"] == "(lambda - 1)**3"
    assert bridge["plus_minus_is_unipotent_jordan_type"] is True
    assert bridge["minus_plus_is_unipotent_jordan_type"] is True
    assert bridge["nilpotent_squares_match_exactly"] is True
    assert bridge["common_nilpotent_square"] == [
        [1, -1, 0],
        [1, -1, 0],
        [0, 0, 0],
    ]
    assert bridge["generation_matrices_commute_exactly"] is True
    assert bridge["slot_independent_plus_minus_matrix"] is True
    assert bridge["slot_independent_minus_plus_matrix"] is True


def test_synthesis_records_yukawa_kronecker_reduction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_kronecker_reduction_bridge"]
    assert bridge["plus_minus_matrix"] == [
        [0, 1, 1],
        [-1, 2, 1],
        [1, -1, 1],
    ]
    assert bridge["minus_plus_matrix"] == [
        [0, 1, -1],
        [-1, 2, -1],
        [-1, 1, 1],
    ]
    assert bridge["conjugating_matrix"] == [
        [-2, 1, 0],
        [-1, 0, 0],
        [0, 0, 1],
    ]
    assert bridge["conjugating_matrix_determinant"] == 1
    assert bridge["exact_integer_conjugacy_between_generation_matrices"] is True
    assert bridge["plus_minus_charpoly"] == "(lambda - 1)**3"
    assert bridge["minus_plus_charpoly"] == "(lambda - 1)**3"
    assert bridge["common_jordan_form"] == [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 1],
    ]
    assert bridge["all_active_sectors_have_exact_kronecker_form"] is True
    assert bridge["all_active_sectors_have_exact_reduced_gram_formula"] is True
    assert bridge["all_active_sector_singular_spectra_match_reduced_gram_exactly"] is True
    assert bridge["template_ranks_match_active_sector_widths"] is True
    assert bridge["h2_plus_minus_sector_width"] == 2
    assert bridge["h2_minus_plus_sector_width"] == 2
    assert bridge["hbar2_plus_minus_sector_width"] == 3
    assert bridge["hbar2_minus_plus_sector_width"] == 1


def test_synthesis_records_yukawa_gram_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_gram_shell_bridge"]
    assert bridge["root_denominator"] == 240
    assert bridge["gram_denominator"] == 57600
    assert bridge["all_template_grams_scale_exactly_to_integer_shell"] is True
    assert bridge["plus_minus_slots_share_exact_phi3_mode_13_over_240"] is True
    assert bridge["h2_plus_minus_base_gram_numerator"] == [[275, 0], [0, 169]]
    assert bridge["h2_minus_plus_base_gram_numerator"] == [[367, -55], [-55, 175]]
    assert bridge["hbar2_plus_minus_base_gram_numerator"] == [[323, 275, 0], [275, 659, 0], [0, 0, 169]]
    assert bridge["hbar2_minus_plus_base_gram_numerator"] == [[323]]
    assert bridge["residual_frontier_is_two_integer_2x2_blocks_plus_exact_scalar_channels"] is True
    assert bridge["h2_minus_plus_residual_block_numerator"] == [[367, -55], [-55, 175]]
    assert bridge["hbar2_plus_minus_residual_block_numerator"] == [[323, 275], [275, 659]]
    assert bridge["exact_scalar_channel_numerators"] == {
        "shared_phi3_mode": 169,
        "h2_plus_minus_companion": 275,
        "hbar2_minus_plus_scalar": 323,
    }
    assert bridge["h2_plus_minus_contains_exact_phi3_mode"] is True
    assert bridge["h2_minus_plus_contains_exact_phi3_mode"] is False
    assert bridge["hbar2_plus_minus_contains_exact_phi3_mode"] is True
    assert bridge["hbar2_minus_plus_contains_exact_phi3_mode"] is False


def test_synthesis_records_yukawa_base_spectrum_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_base_spectrum_bridge"]
    assert bridge["gram_denominator"] == 57600
    assert bridge["h2_plus_minus_squared_spectrum"] == ["169/57600", "275/57600"]
    assert bridge["h2_minus_plus_squared_spectrum"] == [
        "271/57600 - sqrt(12241)/57600",
        "sqrt(12241)/57600 + 271/57600",
    ]
    assert bridge["hbar2_plus_minus_squared_spectrum"] == [
        "169/57600",
        "491/57600 - sqrt(103849)/57600",
        "sqrt(103849)/57600 + 491/57600",
    ]
    assert bridge["hbar2_minus_plus_squared_spectrum"] == ["323/57600"]
    assert bridge["shared_phi3_scalar_channel"] == "169/57600"
    assert bridge["h2_plus_minus_companion_scalar_channel"] == "275/57600"
    assert bridge["hbar2_minus_plus_scalar_channel"] == "323/57600"
    assert bridge["all_base_squared_spectra_are_exact_algebraic_numbers_on_240_shell"] is True
    assert bridge["residual_base_frontier_is_two_radical_pairs_plus_exact_scalar_channels"] is True
    assert bridge["h2_minus_plus_block_trace"] == 542
    assert bridge["h2_minus_plus_block_determinant"] == 61200
    assert bridge["hbar2_plus_minus_block_trace"] == 982
    assert bridge["hbar2_plus_minus_block_determinant"] == 137232


def test_synthesis_records_yukawa_active_spectrum_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["yukawa_active_spectrum_bridge"]
    assert bridge["gram_denominator"] == 57600
    assert bridge["scaled_variable"] == "y = 57600 * sigma^2"
    assert bridge["h2_plus_minus_factors"] == [
        "y - 275",
        "y - 169",
        "y**2 - 5350*y + 675625",
        "y**2 - 4946*y + 143761",
    ]
    assert bridge["h2_minus_plus_factors"] == [
        "y**2 - 542*y + 61200",
        "y**4 - 7292*y**3 + 7645348*y**2 - 2031422400*y + 153044640000",
    ]
    assert bridge["hbar2_plus_minus_factors"] == [
        "y - 169",
        "y**2 - 1138*y + 143761",
        "y**2 - 982*y + 137232",
        "y**4 - 13100*y**3 + 44831236*y**2 - 23791760064*y + 246961799424",
    ]
    assert bridge["hbar2_minus_plus_factors"] == [
        "y - 323",
        "y**2 - 4646*y + 896329",
    ]
    assert bridge["all_active_sector_scaled_spectra_factor_over_z"] is True
    assert bridge["max_factor_degree"] == 4
    assert bridge["h2_plus_minus_contains_exact_base_scalar_packet"] is True
    assert bridge["h2_minus_plus_contains_exact_base_quadratic_packet"] is True
    assert bridge["hbar2_plus_minus_contains_exact_base_packet"] is True
    assert bridge["hbar2_minus_plus_contains_exact_base_scalar_packet"] is True
    assert bridge["remaining_full_active_frontier_is_finite_algebraic_packet"] is True


def test_synthesis_records_curved_eh_mode_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_eh_mode_bridge"]
    assert "860 a0 + 120 a2" in bridge["master_density_formula"]
    assert "12 a0 + 3 a2" in bridge["master_density_formula"]
    assert "6^r" in bridge["master_integrated_formula"]
    assert bridge["exact_scale_separation"] == "120 / 6 = 20"
    assert bridge["finite_df2_cosmological_limit"] == "681600/19"
    assert bridge["finite_df2_eh_6_mode_coefficient"] == "12480"
    assert bridge["finite_df2_topological_1_mode_coefficient"] == "2240"
    assert bridge["a2_transport_cosmological_limit"] == "423000/19"
    assert bridge["transport_dirac_cosmological_limit"] == "19370040/19"
    assert bridge["matter_transport_dirac_cosmological_limit"] == "1568973240/19"
    assert bridge["cp2_finite_df2_curvature_mode_density"] == "54080/19"
    assert bridge["k3_finite_df2_curvature_mode_density"] == "-114400/57"
    assert bridge["cp2_curvature_sign_matches_signature"] is True
    assert bridge["k3_curvature_sign_matches_signature"] is True


def test_synthesis_records_eh_continuum_lock_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["eh_continuum_lock_bridge"]
    assert bridge["continuum_eh_coefficient"] == "320"
    assert bridge["discrete_eh_6_mode_coefficient"] == "12480"
    assert bridge["rank_factor"] == "39"
    assert bridge["discrete_equals_rank_factor_times_continuum"] is True
    assert bridge["rank_d1"] == 39
    assert bridge["rank_mod_3_adjacency"] == 39
    assert bridge["nontrivial_adjacency_multiplicity_sum"] == 39
    assert bridge["all_rank_39_identifications_agree"] is True
    assert bridge["topological_1_mode_coefficient"] == "2240"
    assert bridge["absolute_euler_characteristic"] == 80
    assert bridge["q_cubic_plus_1"] == 28
    assert bridge["topological_equals_q_cubic_plus_1_times_abs_chi"] is True


def test_synthesis_records_exceptional_channel_continuum_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["exceptional_channel_continuum_bridge"]
    assert bridge["continuum_eh_coefficient"] == 320
    assert bridge["continuum_equals_spinor_e6_times_cartan"] is True
    assert bridge["shared_six_l6_a2_root_support"] == 6
    assert bridge["shared_six_transport_weyl_a2_order"] == 6
    assert bridge["shared_six_firewall_triplet_fibers"] == 6
    assert bridge["shared_six_tomotope_triality_factor"] == 6
    assert bridge["all_shared_six_channels_agree"] is True
    assert bridge["discrete_6_mode_coefficient"] == 12480
    assert bridge["discrete_equals_edges_times_f4"] is True
    assert bridge["discrete_equals_spinor_e6_times_shared_six_times_f4"] is True
    assert bridge["cartan_rank_times_rank39_equals_shared_six_times_f4"] is True
    assert bridge["topological_equals_spinor_e6_times_e7_fund"] is True
    assert bridge["topological_equals_continuum_times_phi6"] is True
    assert bridge["tomotope_automorphism_equals_16_times_shared_six"] is True
    assert bridge["firewall_full_clean_quark_block_exists"] is False


def test_synthesis_records_exceptional_operator_projector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["exceptional_operator_projector_bridge"]
    assert bridge["spinor_operator_dimension"] == 2304
    assert bridge["channel_ranks"] == {"e6": 40, "a2": 6, "cartan": 8}
    assert bridge["frobenius_channels_are_pairwise_orthogonal_exactly"] is True
    assert bridge["projector_traces_equal_ranks"] is True
    assert bridge["combined_gauge_package_rank"] == 54
    assert bridge["combined_rank_matches_spinor_total_rank"] is True
    assert bridge["e6_generation_preserving"] is True
    assert bridge["a2_generation_mixing_only"] is True
    assert bridge["cartan_generation_preserving"] is True
    assert bridge["continuum_from_projector_ranks"] == 320
    assert bridge["discrete_from_projector_ranks_and_f4"] == 12480
    assert bridge["topological_from_projector_rank_and_e7_fund"] == 2240
    assert bridge["tomotope_from_a2_projector_rank"] == 96
    assert bridge["firewall_triplet_fibers_from_a2_projector_rank"] == 6
    assert bridge["continuum_matches_live_bridge"] is True
    assert bridge["discrete_matches_live_bridge"] is True
    assert bridge["topological_matches_live_bridge"] is True
    assert bridge["tomotope_matches_live_bridge"] is True
    assert bridge["firewall_matches_live_bridge"] is True
    assert bridge["firewall_full_clean_quark_block_exists"] is False


def test_synthesis_records_exceptional_tensor_rank_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["exceptional_tensor_rank_bridge"]
    assert bridge["e6_projector_rank"] == 40
    assert bridge["a2_projector_rank"] == 6
    assert bridge["cartan_projector_rank"] == 8
    assert bridge["a2_transfer_block_rank"] == 16
    assert bridge["all_a2_transfer_blocks_have_rank_16"] is True
    assert bridge["w33_edge_or_e8_root_count"] == 240
    assert bridge["continuum_eh_coefficient"] == 320
    assert bridge["tomotope_automorphism_order"] == 96
    assert bridge["discrete_curvature_coefficient"] == 12480
    assert bridge["topological_coefficient"] == 2240
    assert bridge["edge_count_equals_e6_rank_times_a2_rank"] is True
    assert bridge["continuum_equals_e6_rank_times_cartan_rank"] is True
    assert bridge["tomotope_equals_a2_rank_times_a2_block_rank"] is True
    assert bridge["discrete_equals_edge_count_times_f4"] is True
    assert bridge["topological_equals_e6_rank_times_e7_fund"] is True
    assert bridge["all_promoted_exceptional_counts_match"] is True


def test_synthesis_records_exceptional_residue_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["exceptional_residue_bridge"]
    assert bridge["e6_projector_rank"] == 40
    assert bridge["a2_projector_rank"] == 6
    assert bridge["cartan_projector_rank"] == 8
    assert bridge["edge_or_e8_root_count"] == 240
    assert bridge["discrete_curvature_from_6_pole"] == 12480
    assert bridge["continuum_eh_from_rank39_normalized_6_pole"] == 320
    assert bridge["topological_from_1_pole"] == 2240
    assert bridge["discrete_equals_e6_times_a2_times_f4"] is True
    assert bridge["discrete_equals_edges_times_f4"] is True
    assert bridge["continuum_equals_e6_times_cartan"] is True
    assert bridge["topological_equals_e6_times_e7_fund"] is True
    assert bridge["all_seed_checks_pass"] is True


def test_synthesis_records_d4_f4_tomotope_reye_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["d4_f4_tomotope_reye_bridge"]
    assert bridge["weyl_d4_order"] == 192
    assert bridge["tomotope_flag_count"] == 192
    assert bridge["tomotope_automorphism_order"] == 96
    assert bridge["weyl_d4_equals_tomotope_flags"] is True
    assert bridge["weyl_d4_equals_2_times_tomotope_automorphism"] is True
    assert bridge["aut_q8_order"] == 24
    assert bridge["d4_root_count"] == 24
    assert bridge["twenty_four_cell_vertex_count"] == 24
    assert bridge["aut_q8_equals_d4_root_count"] is True
    assert bridge["d4_root_count_equals_24cell_vertices"] is True
    assert bridge["reye_points"] == 12
    assert bridge["reye_lines"] == 16
    assert bridge["twenty_four_cell_axes"] == 12
    assert bridge["twenty_four_cell_hexagon_shadow_count"] == 16
    assert bridge["all_twelve_counts_agree"] is True
    assert bridge["all_sixteen_counts_agree"] is True
    assert bridge["outer_d4_order"] == 6
    assert bridge["weyl_f4_order"] == 1152
    assert bridge["twenty_four_cell_rotational_symmetry_order"] == 576
    assert bridge["weyl_f4_equals_triality_times_weyl_d4"] is True
    assert bridge["weyl_f4_equals_triality_times_tomotope_flags"] is True
    assert bridge["weyl_f4_equals_twelve_times_tomotope_automorphism"] is True
    assert bridge["rotational_24_equals_triality_times_tomotope_automorphism"] is True
    assert bridge["weyl_f4_equals_2_times_rotational_24"] is True


def test_synthesis_records_triality_ladder_algebra_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["triality_ladder_algebra_bridge"]
    assert bridge["q8_vertex_block"] == 24
    assert bridge["tomotope_aut_block"] == 96
    assert bridge["d4_weyl_flag_block"] == 192
    assert bridge["rotational_24cell_block"] == 576
    assert bridge["f4_weyl_block"] == 1152
    assert bridge["e6_weyl_closure"] == 51840
    assert bridge["tomotope_equals_a2_rank_times_block_rank"] is True
    assert bridge["d4_equals_d4_roots_times_cartan_rank"] is True
    assert bridge["rotational_24_equals_e6_root_support_times_cartan_rank"] is True
    assert bridge["f4_equals_e6_root_support_times_block_rank"] is True
    assert bridge["we6_equals_tritangents_times_wf4"] is True
    assert bridge["we6_equals_directed_transport_edges_times_wd4"] is True
    assert bridge["we6_equals_e6_root_support_times_transport_edges"] is True
    assert bridge["tritangents"] == 45
    assert bridge["directed_transport_edges"] == 270
    assert bridge["transport_edges"] == 720


def test_synthesis_records_triality_moonshine_spine_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["triality_moonshine_spine_bridge"]
    assert bridge["q8_vertex_block"] == 24
    assert bridge["weyl_e6_order"] == 51840
    assert bridge["monster_semisimple_shell"] == 2160
    assert bridge["monster_local_complement"] == 2187
    assert bridge["leech_kissing_number"] == 196560
    assert bridge["first_moonshine_coefficient"] == 196884
    assert bridge["moonshine_gap"] == 324
    assert bridge["weyl_e6_quotiented_by_q8_vertex_block_equals_shell"] is True
    assert bridge["shell_equals_tritangents_times_spinor_dimension"] is True
    assert bridge["shell_equals_directed_transport_edges_times_cartan_rank"] is True
    assert bridge["shell_equals_transport_edges_times_q"] is True
    assert bridge["shell_equals_w33_edges_times_q_squared"] is True
    assert bridge["local_complement_equals_shell_plus_generation"] is True
    assert bridge["leech_equals_shell_times_phi3_phi6"] is True
    assert bridge["first_moonshine_equals_leech_plus_gap"] is True
    assert bridge["gap_equals_gauge_rank_times_shared_six"] is True
    assert bridge["gap_equals_spacetime_factor_times_logical_qutrits"] is True


def test_synthesis_records_s12_klein_projective_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["s12_klein_projective_bridge"]
    assert bridge["harmonic_cube_order"] == 27
    assert bridge["ternary_golay_code_size"] == 729
    assert bridge["sl27_shell_dimension"] == 728
    assert bridge["projectivized_shell_size"] == 364
    assert bridge["ambient_pg53_points"] == 364
    assert bridge["w33_klein_slice_points"] == 40
    assert bridge["moonshine_gap"] == 324
    assert bridge["harmonic_cube_square_equals_golay_size"] is True
    assert bridge["nonzero_golay_equals_sl27_dimension"] is True
    assert bridge["projectivized_nonzero_shell_equals_pg53_points"] is True
    assert bridge["projective_shell_minus_w33_klein_slice_equals_gap"] is True
    assert bridge["projective_shell_splits_as_w33_slice_plus_gap"] is True
    assert bridge["projective_weight_distribution"] == {6: 132, 9: 220, 12: 12}
    assert bridge["external_plane_points"] == 13
    assert bridge["plane_quartic_bitangent_count"] == 28
    assert bridge["ambient_equals_bitangents_times_external_plane_points"] is True


def test_synthesis_records_klein_quartic_ag21_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_quartic_ag21_bridge"]
    assert bridge["klein_quartic_ag_code_length"] == 21
    assert bridge["fano_flags"] == 21
    assert bridge["heawood_edges"] == 21
    assert bridge["csaszar_edges"] == 21
    assert bridge["szilassi_edges"] == 21
    assert bridge["ag21_equals_q_times_phi6"] is True
    assert bridge["all_promoted_21_counts_agree"] is True


def test_synthesis_records_klein_harmonic_vogel_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_harmonic_vogel_bridge"]
    assert bridge["harmonic_packet_total"] == 14
    assert bridge["klein_quartic_vertices"] == 24
    assert bridge["klein_quartic_triangles"] == 56
    assert bridge["klein_quartic_edges"] == 84
    assert bridge["klein_quartic_automorphism_order"] == 168
    assert bridge["bitangent_count"] == 28
    assert bridge["ag21_length"] == 21
    assert bridge["phi3"] == 13
    assert bridge["g2_dimension"] == 14
    assert bridge["a26_rank"] == 26
    assert bridge["ambient_pg53_points"] == 364
    assert bridge["w33_klein_slice_points"] == 40
    assert bridge["moonshine_gap"] == 324
    assert bridge["sl27_shell_dimension"] == 728
    assert bridge["harmonic_packet_total_equals_g2_dimension"] is True
    assert bridge["triangles_equals_packets_times_spacetime"] is True
    assert bridge["triangles_equals_two_times_bitangents"] is True
    assert bridge["triangles_equals_cartan_times_phi6"] is True
    assert bridge["edges_equals_packets_times_shared_six"] is True
    assert bridge["edges_equals_four_times_ag21"] is True
    assert bridge["edges_equals_gauge_closure_times_phi6"] is True
    assert bridge["automorphisms_equals_two_times_edges"] is True
    assert bridge["automorphisms_equals_eight_times_ag21"] is True
    assert bridge["automorphisms_equals_vertex_seed_times_phi6"] is True
    assert bridge["ambient_equals_g2_times_a26"] is True
    assert bridge["ambient_equals_bitangents_times_phi3"] is True
    assert bridge["ambient_equals_w33_slice_plus_gap"] is True
    assert bridge["sl27_equals_two_times_ambient"] is True
    assert bridge["sl27_equals_bitangents_times_a26"] is True
    assert bridge["sl27_equals_triangles_times_phi3"] is True
    assert bridge["gap_equals_spacetime_times_logical_qutrits"] is True


def test_synthesis_records_klein_clifford_topological_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_clifford_topological_bridge"]
    assert bridge["external_plane_points"] == 13
    assert bridge["bitangent_count"] == 28
    assert bridge["quartic_triangle_count"] == 56
    assert bridge["e7_fundamental_dimension"] == 56
    assert bridge["w33_klein_slice_points"] == 40
    assert bridge["topological_1_mode_coefficient"] == 2240
    assert bridge["quartic_triangles_equal_e7_fund"] is True
    assert bridge["quartic_triangles_equal_two_times_bitangents"] is True
    assert bridge["quartic_triangles_equal_cartan_times_phi6"] is True
    assert bridge["bitangents_equal_q_cubic_plus_1"] is True
    assert bridge["topological_equals_w33_slice_times_quartic_triangles"] is True
    assert bridge["ambient_pg53_points"] == 364
    assert bridge["sl27_shell_dimension"] == 728
    assert bridge["ambient_equals_bitangents_times_phi3"] is True
    assert bridge["sl27_equals_quartic_triangles_times_phi3"] is True
    assert bridge["sl27_equals_two_times_ambient"] is True


def test_synthesis_records_klein_bitangent_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_bitangent_shell_bridge"]
    assert bridge["bitangent_shell"] == 28
    assert bridge["phi3"] == 13
    assert bridge["a26_rank"] == 26
    assert bridge["quartic_triangle_shell"] == 56
    assert bridge["w33_slice"] == 40
    assert bridge["supertrace_magnitude"] == 80
    assert bridge["euler_magnitude"] == 80
    assert bridge["ambient_pg53_points"] == 364
    assert bridge["sl27_shell_dimension"] == 728
    assert bridge["topological_1_mode_coefficient"] == 2240
    assert bridge["ambient_equals_bitangents_times_phi3"] is True
    assert bridge["sl27_equals_bitangents_times_a26_rank"] is True
    assert bridge["topological_equals_bitangents_times_supertrace_magnitude"] is True
    assert bridge["topological_equals_bitangents_times_euler_magnitude"] is True
    assert bridge["quartic_triangles_equals_two_times_bitangents"] is True
    assert bridge["quartic_triangles_equals_cartan_times_phi6"] is True
    assert bridge["topological_equals_w33_slice_times_quartic_triangles"] is True
    assert bridge["a26_rank_equals_two_times_phi3"] is True
    assert bridge["dressings"] == [1, 13, 26, 80]
    assert bridge["shell_ladder"] == [28, 364, 728, 2240]
    assert bridge["topological_over_ambient"] == "80/13"
    assert bridge["topological_over_sl27"] == "40/13"


def test_synthesis_records_s12_vogel_spine_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["s12_vogel_spine_bridge"]
    assert bridge["sl27_dimension"] == 728
    assert bridge["a_family_rank"] == 26
    assert bridge["projective_shell_dimension"] == 364
    assert bridge["g2_dimension"] == 14
    assert bridge["d4_dimension"] == 28
    assert bridge["f4_dimension"] == 52
    assert bridge["e8_dimension"] == 248
    assert bridge["finite_w33_dimension"] == 480
    assert bridge["sl27_is_exactly_a26"] is True
    assert bridge["projective_shell_equals_g2_times_a26_rank"] is True
    assert bridge["sl27_equals_d4_dimension_times_a26_rank"] is True
    assert bridge["sl27_equals_g2_times_f4"] is True
    assert bridge["sl27_equals_finite_w33_plus_e8"] is True
    assert bridge["dim_242_in_positive_exceptional_hit_set"] is False
    assert bridge["dim_486_in_positive_exceptional_hit_set"] is False
    assert bridge["dim_728_in_positive_exceptional_hit_set"] is False
    assert bridge["nearest_positive_exceptional_hits_to_728"] == [782]
    assert bridge["distance_from_728_to_nearest_positive_exceptional_hit"] == 54


def test_synthesis_records_curved_inverse_rosetta_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_inverse_rosetta_bridge"]
    assert bridge["w33_vertex_count"] == 40
    assert bridge["w33_edge_or_e8_root_count"] == 240
    assert bridge["spinor_cartan_rank"] == 8
    assert bridge["shared_six_channel"] == 6
    assert bridge["tomotope_automorphism_order"] == 96
    assert bridge["vertex_count_matches"] is True
    assert bridge["edge_count_matches"] is True
    assert bridge["cartan_rank_matches"] is True
    assert bridge["shared_six_matches"] is True
    assert bridge["tomotope_aut_matches"] is True
    assert bridge["all_samples_constant"] is True


def test_synthesis_records_curved_weinberg_lock_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_weinberg_lock_bridge"]
    assert bridge["master_variable"] == "3/13"
    assert bridge["curved_reconstruction_formula"] == "x = 9 * c_EH,cont / c_6"
    assert bridge["cp2_step0_reconstructed_x"] == "3/13"
    assert bridge["cp2_step1_reconstructed_x"] == "3/13"
    assert bridge["k3_step0_reconstructed_x"] == "3/13"
    assert bridge["k3_step1_reconstructed_x"] == "3/13"
    assert bridge["all_curved_samples_match_master_variable"] is True
    assert bridge["exceptional_formula"] == "x = 9 * (40*8) / (40*6*52)"
    assert bridge["exceptional_reconstructed_x"] == "3/13"
    assert bridge["exceptional_matches_master_variable"] is True
    assert bridge["tan_theta_c"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["all_promoted_observables_match_public_generator_values"] is True


def test_synthesis_records_curved_rosetta_reconstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_rosetta_reconstruction_bridge"]
    assert bridge["master_variable"] == "3/13"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["phi6_from_topological_over_continuum"] == "7"
    assert bridge["vertex_count_from_topological_over_e7_fund"] == 40
    assert bridge["edge_count_from_discrete_over_f4"] == 240
    assert bridge["k_from_two_edges_over_vertices"] == "12"
    assert bridge["q"] == 3
    assert bridge["phi3"] == "13"
    assert bridge["phi6"] == "7"
    assert bridge["srg_data"] == {"v": 40, "k": 12, "lambda": 2, "mu": 4}
    assert bridge["spectral_data"] == {"k": 12, "r": 2, "s": -4}
    assert bridge["all_promoted_observables_match"] is True
    assert bridge["all_samples_constant"] is True


def test_synthesis_records_curved_finite_spectral_reconstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_finite_spectral_reconstruction_bridge"]
    assert bridge["q"] == 3
    assert bridge["line_count"] == 40
    assert bridge["edge_count"] == 240
    assert bridge["triangle_count"] == 160
    assert bridge["tetrahedron_count"] == 40
    assert bridge["betti_numbers"] == {"b0": 1, "b1": 81, "b2": 0, "b3": 0}
    assert bridge["boundary_ranks"] == {"rank_d1": 39, "rank_d2": 120, "rank_d3": 40}
    assert bridge["vertex_laplacian_spectrum"] == {0: 1, 10: 24, 16: 15}
    assert bridge["df2_spectrum"] == {0: 82, 4: 320, 10: 48, 16: 30}
    assert bridge["a0_f"] == 480
    assert bridge["a2_f"] == 2240
    assert bridge["a4_f"] == 17600
    assert bridge["mu_squared"] == "14/3"
    assert bridge["lambda"] == "110/3"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["df2_spectrum_match"] is True
    assert bridge["moments_match"] is True
    assert bridge["all_samples_constant"] is True


def test_synthesis_records_curved_roundtrip_closure_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_roundtrip_closure_bridge"]
    assert bridge["a0_f"] == 480
    assert bridge["a2_f"] == 2240
    assert bridge["a4_f"] == 17600
    assert bridge["df2_spectrum"] == {0: 82, 4: 320, 10: 48, 16: 30}
    assert bridge["continuum_eh_from_finite"] == "320"
    assert bridge["discrete_eh_from_finite"] == "12480"
    assert bridge["topological_from_finite"] == "2240"
    assert bridge["master_variable_from_roundtrip"] == "3/13"
    assert bridge["continuum_matches"] is True
    assert bridge["discrete_matches"] is True
    assert bridge["topological_matches"] is True
    assert bridge["master_variable_matches"] is True
    assert bridge["all_samples_close_exactly"] is True


def test_synthesis_records_three_sample_master_closure_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["three_sample_master_closure_bridge"]
    assert bridge["minimal_seed"] == "CP2"
    assert bridge["steps"] == [0, 1, 2]
    assert bridge["discrete_eh"] == "12480"
    assert bridge["continuum_eh"] == "320"
    assert bridge["topological_a2"] == "2240"
    assert bridge["master_variable"] == "3/13"
    assert bridge["q"] == 3
    assert bridge["phi3"] == "13"
    assert bridge["phi6"] == "7"
    assert bridge["srg_data"] == {"v": 40, "k": 12, "lambda": 2, "mu": 4}
    assert bridge["spectral_data"] == {"k": 12, "r": 2, "s": -4}
    assert bridge["df2_spectrum"] == {0: 82, 4: 320, 10: 48, 16: 30}
    assert bridge["a0_f"] == 480
    assert bridge["a2_f"] == 2240
    assert bridge["a4_f"] == 17600
    assert bridge["exceptional_data"] == {
        "w33_vertex_count": 40,
        "w33_edge_or_e8_root_count": 240,
        "spinor_cartan_rank": 8,
        "shared_six_channel": 6,
        "tomotope_automorphism_order": 96,
    }
    assert bridge["full_master_closure"] is True


def test_synthesis_records_curvature_cyclotomic_lock_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curvature_cyclotomic_lock_bridge"]
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["q_phi3"] == 39
    assert bridge["q_plus_1_phi6"] == 28
    assert bridge["gravity_is_q_phi3_times_continuum"] is True
    assert bridge["topology_is_q_plus_1_phi6_times_abs_chi"] is True
    assert bridge["topology_is_q_cubic_plus_1_times_abs_chi"] is True


def test_synthesis_records_q3_curved_selection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["q3_curved_selection_bridge"]
    assert bridge["gravity_polynomial"] == "q^3 - 2q^2 - 2q - 3"
    assert bridge["gravity_factorization"] == "(q - 3)(q^2 + q + 1)"
    assert bridge["gravity_unique_positive_integer_solution"] == 3
    assert bridge["topology_polynomial"] == "q^2 + q - 12"
    assert bridge["topology_factorization"] == "(q - 3)(q + 4)"
    assert bridge["topology_unique_positive_integer_solution"] == 3


def test_synthesis_records_spectral_action_cyclotomic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["spectral_action_cyclotomic_bridge"]
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["four_phi3_plus_q"] == 55
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["a2_over_a0_matches_formula"] is True
    assert bridge["a4_over_a0_matches_formula"] is True
    assert bridge["higgs_ratio_square_matches_formula"] is True
    assert bridge["continuum_eh_over_a0"] == "2/3"
    assert bridge["discrete_6_mode_over_a0"] == "26"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["continuum_eh_over_a0_matches_formula"] is True
    assert bridge["discrete_6_mode_over_a0_matches_formula"] is True
    assert bridge["discrete_to_continuum_matches_formula"] is True


def test_synthesis_records_spectral_action_q3_selection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["spectral_action_q3_selection_bridge"]
    assert bridge["internal_polynomial"] == "3q^2 - 10q + 3"
    assert bridge["internal_factorization"] == "(q - 3)(3q - 1)"
    assert bridge["internal_unique_positive_integer_solution"] == 3
    assert bridge["a4_uses_same_polynomial"] is True
    assert bridge["higgs_uses_same_polynomial"] is True
    assert bridge["gravity_polynomial"] == "q^2 + q - 12"
    assert bridge["gravity_factorization"] == "(q - 3)(q + 4)"
    assert bridge["gravity_unique_positive_integer_solution"] == 3


def test_synthesis_records_standard_model_cyclotomic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["standard_model_cyclotomic_bridge"]
    assert bridge["sin2_theta_w_ew"] == "3/13"
    assert bridge["tan_theta_c"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["tan_cabibbo_equals_ew_weinberg"] is True
    assert bridge["pmns_23_equals_weinberg_plus_pmns_12"] is True
    assert bridge["omega_lambda_equals_q_times_weinberg"] is True
    assert bridge["reactor_has_phi3_phi6_denominator"] is True
    assert bridge["higgs_uses_four_phi3_plus_q_denominator"] is True


def test_synthesis_records_monster_landauer_ternary_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_landauer_ternary_bridge"]
    assert bridge["monster_class"] == "3B"
    assert bridge["shell_states"] == 3**13
    assert bridge["shell_trits"] == 13
    assert bridge["shell_landauer_over_kT"] == "13 ln(3)"
    assert bridge["heisenberg_irrep_states"] == 3**6
    assert bridge["heisenberg_irrep_trits"] == 6
    assert bridge["complement_states"] == 3**7
    assert bridge["complement_trits"] == 7
    assert bridge["logical_qutrits"] == 81
    assert bridge["logical_trits"] == 4
    assert bridge["phi3_equals_shell_trits"] is True
    assert bridge["shared_six_equals_irrep_trits"] is True
    assert bridge["phi6_equals_complement_trits"] is True
    assert bridge["phi6_equals_shell_minus_irrep"] is True
    assert bridge["heisenberg_irrep_equals_q_squared_times_logical_qutrits"] is True
    assert bridge["weinberg_from_generation_over_shell"] == "3/13"
    assert bridge["theta12_from_logical_over_shell"] == "4/13"
    assert bridge["theta23_from_complement_over_shell"] == "7/13"
    assert bridge["weinberg_matches_promoted_value"] is True
    assert bridge["theta12_matches_promoted_value"] is True
    assert bridge["theta23_matches_promoted_value"] is True
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["discrete_to_continuum_equals_shell_times_generation_trits"] is True
    assert bridge["topological_over_continuum"] == "7"
    assert bridge["topological_over_continuum_equals_complement_trits"] is True


def test_synthesis_records_monster_shell_factorization_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_shell_factorization_bridge"]
    assert bridge["shell_states"] == 3**13
    assert bridge["heisenberg_states"] == 3**6
    assert bridge["logical_states"] == 3**4
    assert bridge["generation_states"] == 3**3
    assert bridge["complement_states"] == 3**7
    assert bridge["shell_equals_heisenberg_times_logical_times_generation"] is True
    assert bridge["complement_equals_logical_times_generation"] is True
    assert bridge["shell_trits_split"] == [6, 4, 3]
    assert bridge["shell_trits_factorization_exact"] is True
    assert bridge["complement_trits_split"] == [4, 3]
    assert bridge["complement_trits_factorization_exact"] is True
    assert bridge["weinberg_from_generation_over_shell"] == "3/13"
    assert bridge["theta12_from_logical_over_shell"] == "4/13"
    assert bridge["active_heisenberg_share"] == "6/13"
    assert bridge["theta23_from_complement_over_shell"] == "7/13"
    assert bridge["theta23_equals_theta12_plus_weinberg"] is True
    assert bridge["theta23_plus_active_heisenberg_share_equals_one"] is True
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["topological_over_continuum"] == "7"
    assert bridge["discrete_to_continuum_equals_shell_times_generation"] is True
    assert bridge["topological_over_continuum_equals_logical_plus_generation"] is True


def test_synthesis_records_monster_3adic_closure_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_3adic_closure_bridge"]
    assert bridge["three_primary_states"] == 3**20
    assert bridge["three_primary_trits"] == 20
    assert bridge["full_landauer_over_kT"] == "20 ln(3)"
    assert bridge["shell_states"] == 3**13
    assert bridge["complement_states"] == 3**7
    assert bridge["full_three_primary_equals_shell_times_complement"] is True
    assert bridge["full_three_primary_equals_heisenberg_times_logical_squared_times_generation_squared"] is True
    assert bridge["full_three_primary_trits_equal_phi3_plus_phi6"] is True
    assert bridge["landauer_additivity_exact"] is True
    assert bridge["shell_share_of_full_monster_three_primary"] == "13/20"
    assert bridge["complement_share_of_full_monster_three_primary"] == "7/20"
    assert bridge["gravity_over_q"] == "13"
    assert bridge["topological_over_continuum"] == "7"
    assert bridge["shell_from_curved_gravity_exact"] is True
    assert bridge["complement_from_curved_topology_exact"] is True
    assert bridge["full_monster_three_primary_from_curved_coefficients_exact"] is True
    assert bridge["monster_three_trits_equal_phi3_plus_phi6"] is True


def test_synthesis_records_monster_3b_centralizer_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_3b_centralizer_bridge"]
    assert bridge["centralizer_label"] == "3^(1+12).2Suz"
    assert bridge["monster_three_primary_states"] == 3**20
    assert bridge["centralizer_three_primary_states"] == 3**20
    assert bridge["centralizer_three_primary_matches_monster"] is True
    assert bridge["shell_states"] == 3**13
    assert bridge["two_suz_three_primary_states"] == 3**7
    assert bridge["two_suz_three_primary_trits"] == 7
    assert bridge["two_suz_three_primary_equals_logical_times_generation"] is True
    assert bridge["landauer_additivity_exact"] is True
    assert bridge["gravity_over_q"] == "13"
    assert bridge["topology_over_continuum"] == "7"
    assert bridge["shell_from_curved_gravity_exact"] is True
    assert bridge["two_suz_from_curved_topology_exact"] is True
    assert bridge["centralizer_three_primary_from_curved_coefficients_exact"] is True


def test_synthesis_records_monster_lagrangian_complement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_lagrangian_complement_bridge"]
    assert bridge["max_abelian_subgroup_order"] == 3**7
    assert bridge["complement_states"] == 3**7
    assert bridge["lagrangian_quotient_states"] == 3**6
    assert bridge["complement_equals_lifted_max_abelian_exactly"] is True
    assert bridge["lagrangian_quotient_equals_heisenberg_irrep"] is True
    assert bridge["lagrangian_quotient_equals_golay_codewords"] is True
    assert bridge["lagrangian_quotient_equals_sl27_operator_basis"] is True
    assert bridge["center_times_lagrangian_quotient_equals_complement"] is True
    assert bridge["complement_equals_logical_times_generation"] is True
    assert bridge["logical_plus_generation_trits"] == [4, 3]
    assert bridge["center_plus_heisenberg_trits"] == [1, 6]
    assert bridge["complement_trits_equal_logical_plus_generation"] is True
    assert bridge["complement_trits_equal_center_plus_heisenberg"] is True
    assert bridge["dual_trit_splits_agree_exactly"] is True
    assert bridge["topological_over_continuum"] == "7"
    assert bridge["topological_equals_complement_trits"] is True
    assert bridge["topological_equals_logical_plus_generation"] is True
    assert bridge["topological_equals_center_plus_heisenberg"] is True


def test_synthesis_records_monster_selector_completion_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_selector_completion_bridge"]
    assert bridge["complement_states"] == 3**7
    assert bridge["center_states"] == 3
    assert bridge["heisenberg_completion_states"] == 3**6
    assert bridge["sl27_traceless_dimension"] == 728
    assert bridge["nonzero_golay_codewords"] == 728
    assert bridge["full_golay_codewords"] == 729
    assert bridge["selector_line_dimension"] == 1
    assert bridge["projective_selector_line"] == [1, 2]
    assert bridge["w33_kernel_dimension_mod_3"] == 1
    assert bridge["full_codewords_equal_sl27_plus_selector"] is True
    assert bridge["nonzero_codewords_equal_sl27_traceless"] is True
    assert bridge["complement_equals_center_times_selector_completion"] is True
    assert bridge["selector_completion_decomposition_exact"] is True
    assert bridge["sl27_z3_total_dimension"] == 728
    assert bridge["sl27_bridge_claim_holds"] is True
    assert bridge["golay_nonzero_equals_sl27_total"] is True
    assert bridge["transport_selector_is_unique"] is True
    assert bridge["w33_all_ones_spans_mod_3_kernel"] is True
    assert bridge["transport_projective_selector_line_is_unique"] is True
    assert bridge["path_groupoid_has_unique_invariant_line"] is True


def test_synthesis_records_monster_q5_completion_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_q5_completion_bridge"]
    assert bridge["q"] == 3
    assert bridge["q5"] == 243
    assert bridge["q7"] == 2187
    assert bridge["grade_split"] == [242, 243, 243]
    assert bridge["selector_line_dimension"] == 1
    assert bridge["restored_blocks"] == [243, 243, 243]
    assert bridge["restored_blocks_are_three_q5_blocks"] is True
    assert bridge["full_codewords"] == 729
    assert bridge["full_codewords_equal_3q5"] is True
    assert bridge["complement_states"] == 3**7
    assert bridge["complement_equals_q7"] is True
    assert bridge["edge_count"] == 240
    assert bridge["edge_count_equals_q5_minus_q"] is True
    assert bridge["semisimple_curved_states"] == 2160
    assert bridge["generation_states"] == 27
    assert bridge["semisimple_curved_equals_q_squared_times_edges"] is True
    assert bridge["semisimple_curved_equals_q7_minus_q3"] is True
    assert bridge["complement_equals_semisimple_curved_plus_generation"] is True
    assert bridge["complement_equals_q_squared_edges_plus_q_cubed"] is True


def test_synthesis_records_monster_transport_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_transport_shell_bridge"]
    assert bridge["q"] == 3
    assert bridge["w33_edge_count"] == 240
    assert bridge["transport_edge_count"] == 720
    assert bridge["local_line_bundle_dimension"] == 135
    assert bridge["a2_transfer_block_rank"] == 16
    assert bridge["semisimple_transport_shell"] == 2160
    assert bridge["generation_states"] == 27
    assert bridge["monster_complement_states"] == 3**7
    assert bridge["semisimple_equals_q_squared_times_w33_edges"] is True
    assert bridge["semisimple_equals_q_times_transport_edges"] is True
    assert bridge["semisimple_equals_a2_block_rank_times_bundle_dimension"] is True
    assert bridge["complement_equals_semisimple_plus_generation"] is True
    assert bridge["complement_equals_q_squared_edges_plus_q_cubed"] is True
    assert bridge["complement_equals_q_transport_edges_plus_q_cubed"] is True
    assert bridge["complement_equals_block_bundle_plus_generation"] is True


def test_synthesis_records_monster_supertrace_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_supertrace_bridge"]
    assert bridge["euler_characteristic"] == -80
    assert bridge["supertrace"] == -80
    assert bridge["supertrace_magnitude"] == 80
    assert bridge["selector_line_dimension"] == 1
    assert bridge["logical_qutrits"] == 81
    assert bridge["generation_states"] == 27
    assert bridge["e8_second_shell"] == 2160
    assert bridge["semisimple_transport_shell"] == 2160
    assert bridge["monster_complement_states"] == 3**7
    assert bridge["euler_matches_supertrace_exactly"] is True
    assert bridge["semisimple_equals_e8_second_shell"] is True
    assert bridge["semisimple_equals_generation_times_supertrace_magnitude"] is True
    assert bridge["logical_equals_supertrace_magnitude_plus_selector"] is True
    assert bridge["monster_complement_equals_generation_times_logical"] is True
    assert bridge["monster_complement_equals_e8_second_shell_plus_generation"] is True


def test_synthesis_records_monster_moonshine_lift_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_moonshine_lift_bridge"]
    assert bridge["q"] == 3
    assert bridge["phi3"] == 13
    assert bridge["phi6"] == 7
    assert bridge["cyclotomic_lift_factor"] == 91
    assert bridge["local_second_shell"] == 2160
    assert bridge["leech_kissing_number"] == 196560
    assert bridge["logical_qutrits"] == 81
    assert bridge["spacetime_factor"] == 4
    assert bridge["moonshine_gap"] == 324
    assert bridge["first_moonshine_coefficient"] == 196884
    assert bridge["smallest_monster_irrep"] == 196883
    assert bridge["selector_line_dimension"] == 1
    assert bridge["local_second_shell_matches_theta_e8_second_shell"] is True
    assert bridge["leech_equals_local_second_shell_times_phi3_phi6"] is True
    assert bridge["moonshine_gap_equals_q_plus_1_times_logical_qutrits"] is True
    assert bridge["moonshine_gap_equals_q_plus_1_times_q_to_four"] is True
    assert bridge["first_moonshine_equals_leech_plus_gap"] is True
    assert bridge["first_moonshine_equals_selector_plus_smallest_monster_irrep"] is True
    assert bridge["first_moonshine_equals_cyclotomic_lifted_shell_plus_spacetime_matter"] is True


def test_synthesis_records_monster_transport_moonshine_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_transport_moonshine_bridge"]
    assert bridge["sl27_traceless_dimension"] == 728
    assert bridge["sl27_completed_dimension"] == 729
    assert bridge["directed_transport_edges"] == 270
    assert bridge["gauge_package_rank"] == 54
    assert bridge["leech_kissing_number"] == 196560
    assert bridge["moonshine_gap"] == 324
    assert bridge["first_moonshine_coefficient"] == 196884
    assert bridge["leech_equals_sl27_traceless_times_transport_edges"] is True
    assert bridge["first_moonshine_equals_completed_sl27_times_transport_plus_gauge_rank"] is True
    assert bridge["moonshine_gap_equals_transport_plus_gauge_rank"] is True
    assert bridge["gauge_package_rank_equals_e6_plus_a2_plus_cartan"] is True


def test_synthesis_records_monster_gap_duality_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_gap_duality_bridge"]
    assert bridge["leech_kissing_number"] == 196560
    assert bridge["first_moonshine_coefficient"] == 196884
    assert bridge["moonshine_gap"] == 324
    assert bridge["gauge_package_rank"] == 54
    assert bridge["shared_six_channel_rank"] == 6
    assert bridge["spacetime_factor"] == 4
    assert bridge["logical_qutrits"] == 81
    assert bridge["gap_equals_exceptional_gauge_rank_times_shared_six"] is True
    assert bridge["gap_equals_spacetime_factor_times_logical_qutrits"] is True
    assert bridge["exceptional_gap_matches_spacetime_matter_gap"] is True
    assert bridge["first_moonshine_equals_traceless_transport_plus_exceptional_gap"] is True
    assert bridge["first_moonshine_equals_completed_transport_plus_gauge_rank"] is True
    assert bridge["gauge_rank_equals_e6_plus_a2_plus_cartan"] is True
    assert bridge["shared_six_is_live_a2_rank"] is True


def test_synthesis_records_monster_triangle_landauer_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["monster_triangle_landauer_bridge"]
    assert bridge["q"] == 3
    assert bridge["vertices"] == 40
    assert bridge["degree"] == 12
    assert bridge["lambda"] == 2
    assert bridge["triangle_count"] == 160
    assert bridge["automorphism_order"] == 51840
    assert bridge["triangle_stabilizer"] == 324
    assert bridge["moonshine_gap"] == 324
    assert bridge["triangle_stabilizer_matches_general_formula"] is True
    assert bridge["triangle_stabilizer_equals_moonshine_gap"] is True
    assert bridge["triangle_stabilizer_equals_exceptional_times_shared_six"] is True
    assert bridge["triangle_stabilizer_equals_spacetime_times_logical_qutrits"] is True
    assert bridge["triangle_stabilizer_equals_degree_times_generation"] is True
    assert bridge["first_moonshine_equals_transport_traceless_plus_triangle_stabilizer"] is True
    assert bridge["landauer_gap_over_kT"] == "ln(324)"
    assert bridge["landauer_exceptional_split"] == "ln(54) + ln(6)"
    assert bridge["landauer_matter_split"] == "ln(4) + ln(81)"
    assert bridge["landauer_exceptional_split_matches"] is True
    assert bridge["landauer_matter_split_matches"] is True


def test_synthesis_records_weinberg_generator_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["weinberg_generator_bridge"]
    assert bridge["generator"] == "3/13"
    assert bridge["tan_theta_c"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["discrete_6_mode_over_a0"] == "26"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["sin2_theta_23_plus_2weinberg_equals_1"] is True
    assert bridge["sin2_theta_12_equals_four_thirds_weinberg"] is True
    assert bridge["omega_lambda_equals_3weinberg"] is True
    assert bridge["cabibbo_equals_weinberg"] is True
    assert bridge["gravity_ratio_equals_9_over_weinberg"] is True


def test_synthesis_records_weinberg_reconstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["weinberg_reconstruction_bridge"]
    assert bridge["master_variable"] == "3/13"
    assert bridge["from_cabibbo"] == "3/13"
    assert bridge["from_pmns_12"] == "3/13"
    assert bridge["from_pmns_23"] == "3/13"
    assert bridge["from_omega_lambda"] == "3/13"
    assert bridge["from_higgs_ratio"] == "3/13"
    assert bridge["from_a2_over_a0"] == "3/13"
    assert bridge["from_a4_over_a0"] == "3/13"
    assert bridge["from_discrete_6_mode_over_a0"] == "3/13"
    assert bridge["from_discrete_to_continuum_ratio"] == "3/13"
    assert bridge["all_channels_match_master_variable"] is True


def test_synthesis_records_srg_rosetta_lock_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["srg_rosetta_lock_bridge"]
    assert bridge["q_from_lambda_plus_one"] == 3
    assert bridge["phi3_from_k_plus_one"] == 13
    assert bridge["phi6_from_k_minus_lambda_minus_mu_plus_one"] == 7
    assert bridge["sin2_theta_w_ew"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["discrete_6_mode_over_a0"] == "26"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["all_matches_formula"] is True


def test_synthesis_records_spectral_rosetta_lock_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["spectral_rosetta_lock_bridge"]
    assert bridge["q_from_r_plus_one"] == 3
    assert bridge["phi3_from_k_plus_one"] == 13
    assert bridge["phi6_from_one_plus_r_minus_s"] == 7
    assert bridge["sin2_theta_w_ew"] == "3/13"
    assert bridge["sin2_theta_12"] == "4/13"
    assert bridge["sin2_theta_23"] == "7/13"
    assert bridge["sin2_theta_13"] == "2/91"
    assert bridge["omega_lambda"] == "9/13"
    assert bridge["higgs_ratio_square"] == "14/55"
    assert bridge["a2_over_a0"] == "14/3"
    assert bridge["a4_over_a0"] == "110/3"
    assert bridge["discrete_6_mode_over_a0"] == "26"
    assert bridge["discrete_to_continuum_ratio"] == "39"
    assert bridge["all_matches_formula"] is True


def test_synthesis_records_curved_mode_projector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_mode_projector_bridge"]
    assert bridge["tower_characteristic_polynomial"] == "x^3 - 127x^2 + 846x - 720"
    assert bridge["p120"] == "((E-6)(E-1))/13566"
    assert bridge["p6"] == "-((E-120)(E-1))/570"
    assert bridge["p1"] == "((E-120)(E-6))/595"
    assert bridge["finite_einstein_hilbert_coefficient"] == "12480"
    assert bridge["cp2_eh_extracted"] == "12480"
    assert bridge["k3_eh_extracted"] == "12480"
    assert bridge["cp2_continuum_eh"] == "320"
    assert bridge["k3_continuum_eh"] == "320"
    assert bridge["all_projector_samples_match"] is True


def test_synthesis_records_curved_mode_residue_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_mode_residue_bridge"]
    assert bridge["generating_function_formula"] == "A/(1 - 120 z) + B/(1 - 6 z) + C/(1 - z)"
    assert bridge["residue_definition"] == "R_alpha(G) = -alpha * Res_{z = 1/alpha} G(z)"
    assert bridge["expected_eh"] == "12480"
    assert bridge["cp2_eh_from_residue"] == "12480"
    assert bridge["k3_eh_from_residue"] == "12480"
    assert bridge["cp2_continuum_from_residue"] == "320"
    assert bridge["k3_continuum_from_residue"] == "320"
    assert bridge["all_seed_residues_match_expected"] is True


def test_synthesis_records_curved_continuum_extractor_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_continuum_extractor_bridge"]
    assert bridge["discrete_eh_formula"] == "-(M_{r+2} - 121 M_{r+1} + 120 M_r) / (570 * six * 6^r)"
    assert bridge["continuum_eh_formula"] == "-(M_{r+2} - 121 M_{r+1} + 120 M_r) / (570 * six * 39 * 6^r)"
    assert bridge["topological_a2_formula"] == "(M_{r+2} - 126 M_{r+1} + 720 M_r) / (595 * chi)"
    assert bridge["expected_discrete_eh"] == "12480"
    assert bridge["expected_continuum_eh"] == "320"
    assert bridge["cp2_step0_continuum_eh"] == "320"
    assert bridge["k3_step0_continuum_eh"] == "320"
    assert bridge["all_samples_match_expected"] is True


def test_synthesis_records_center_quad_exceptional_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_exceptional_bridge"]
    assert bridge["center_quads"] == 90
    assert bridge["quotient_points"] == 45
    assert bridge["quotient_lines"] == 27
    assert bridge["incidences"] == 135
    assert bridge["line_graph_vertices"] == 27
    assert bridge["line_graph_degree"] == 10
    assert bridge["line_graph_lambda"] == 1
    assert bridge["line_graph_mu"] == 5
    assert bridge["line_graph_triangles"] == 45
    assert bridge["point_graph_edges"] == 270
    assert bridge["line_lifts_partition_w33"] is True


def test_synthesis_records_center_quad_transport_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_transport_bridge"]
    assert bridge["cover_vertices"] == 90
    assert bridge["cover_degree"] == 32
    assert bridge["transport_quotient_vertices"] == 45
    assert bridge["transport_quotient_edges"] == 720
    assert bridge["transport_quotient_degree"] == 32
    assert bridge["raw_z2_distribution"] == {0: 414, 1: 306}
    assert bridge["canonical_z2_distribution"] == {0: 414, 1: 306}
    assert bridge["triangle_count"] == 5280
    assert bridge["triangle_parity0"] == 3120
    assert bridge["triangle_parity1"] == 2160
    assert bridge["v14_triangle_stats_match_exactly"] is True
    assert bridge["transport_edges_270"] == 270
    assert bridge["s3_sheet_pockets"] == 54
    assert bridge["s3_sheet_transport_exact"] is True
    assert bridge["nonzero_sheet_generator"] == ["g3"]
    assert bridge["z2_trivial_but_s3_odd"] is True


def test_synthesis_records_transport_complement_theorem() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_transport_complement_bridge"]
    assert bridge["point_graph_degree"] == 12
    assert bridge["point_graph_lambda"] == 3
    assert bridge["point_graph_mu"] == 3
    assert bridge["transport_graph_degree"] == 32
    assert bridge["transport_graph_lambda"] == 22
    assert bridge["transport_graph_mu"] == 24
    assert bridge["transport_is_complement_of_point_graph"] is True
    assert bridge["transport_is_triangle_disjointness_graph"] is True
    assert bridge["all_six_local_s3_matchings"] is True
    assert bridge["raw_z2_not_determined_by_matching_permutation"] is True
    assert bridge["raw_z2_not_determined_by_matching_parity"] is True


def test_synthesis_records_transport_holonomy_theorem() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_transport_holonomy_bridge"]
    assert bridge["transport_triangles"] == 5280
    assert bridge["triangle_parity0"] == 3120
    assert bridge["triangle_parity1"] == 2160
    assert bridge["holonomy_cycle_types"] == {
        "identity": 240,
        "three_cycle": 2880,
        "transposition": 2160,
    }
    assert bridge["z2_parity_equals_holonomy_sign_exactly"] is True


def test_synthesis_records_uor_transport_shadow_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["uor_transport_shadow_bridge"]
    assert bridge["shadow_ring"] == "Z/2Z"
    assert bridge["transport_group"] == "Weyl(A2) ~= S3 ~= D3"
    assert bridge["shadow_is_holonomy_sign_not_raw_voltage"] is True
    assert bridge["weyl_group_order"] == 6
    assert bridge["sign_kernel_order"] == 3
    assert bridge["sign_coset_order"] == 3
    assert bridge["edge_sign_shadow_surjective"] is True
    assert bridge["triangle_shadow_forgets_identity_vs_three_cycle"] is True


def test_synthesis_records_transport_path_groupoid_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_path_groupoid_bridge"]
    assert bridge["objects"] == 45
    assert bridge["directed_generators"] == 1440
    assert bridge["tree_edges"] == 44
    assert bridge["fundamental_cycles"] == 676
    assert bridge["tree_edges_gauge_trivialized"] is True
    assert bridge["fundamental_cycle_holonomy_group_order"] == 6
    assert bridge["real_flat_section_dimension"] == 0
    assert bridge["ternary_flat_section_dimension"] == 1
    assert bridge["ternary_invariant_line"] == [1, 2]
    assert bridge["ternary_quotient_character_values"] == [1, 2]


def test_synthesis_records_transport_operator_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_transport_operator_bridge"]
    assert bridge["bundle_dimension"] == 135
    assert bridge["bundle_spectrum"] == {
        -16: 6,
        -4: 20,
        -1: 64,
        2: 24,
        8: 20,
        32: 1,
    }
    assert bridge["bundle_laplacian_spectrum"] == {
        0: 1,
        24: 20,
        30: 24,
        33: 64,
        36: 20,
        48: 6,
    }
    assert bridge["trivial_dimension"] == 45
    assert bridge["standard_dimension"] == 90
    assert bridge["trivial_block_equals_transport_adjacency"] is True
    assert bridge["standard_block_spectrum"] == {-16: 6, -1: 64, 8: 20}
    assert bridge["signed_holonomy_spectrum"] == {-4: 30, 8: 15}
    assert bridge["signed_operator_quadratic_identity"] is True
    assert bridge["signed_trace_matches_triangle_excess"] is True


def test_synthesis_records_native_a2_transport_sector() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["center_quad_transport_a2_bridge"]
    assert bridge["fiber_rank"] == 2
    assert bridge["cartan_matrix"] == [[2, -1], [-1, 2]]
    assert bridge["all_six_weyl_matrices_realized"] is True
    assert bridge["determinant_character_equals_permutation_parity"] is True
    assert bridge["a2_operator_dimension"] == 90
    assert bridge["a2_operator_spectrum"] == {-16: 6, -1: 64, 8: 20}
    assert bridge["a2_operator_cubic_relation"] is True
    assert bridge["matches_standard_sector_up_to_local_basis_change"] is True
    assert bridge["triangle_character_sum"] == -2400
    assert bridge["trace_cube_matches_character_sum"] is True


def test_synthesis_records_ternary_homological_code_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["ternary_homological_code_bridge"]
    assert bridge["field"] == "F3"
    assert bridge["physical_qutrits"] == 240
    assert bridge["x_check_rank"] == 39
    assert bridge["z_check_rank"] == 120
    assert bridge["logical_qutrits"] == 81
    assert bridge["stabilizer_rank_total"] == 159
    assert bridge["primal_logical_distance"] == 4
    assert bridge["weight_four_witness_cycle"] == [0, 4, 1, 13]


def test_synthesis_records_transport_ternary_line_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_ternary_line_bridge"]
    assert bridge["real_flat_section_dimension"] == 0
    assert bridge["ternary_flat_section_dimension"] == 1
    assert bridge["invariant_line"] == [1, 2]
    assert bridge["logical_qutrits"] == 81
    assert bridge["canonical_transport_stable_sector_dimension"] == 81
    assert bridge["matter_flavour_dimension"] == 162
    assert bridge["matches_flat_internal_dimension_exactly"] is True


def test_synthesis_records_transport_ternary_extension_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_ternary_extension_bridge"]
    assert bridge["field"] == "F3"
    assert bridge["holonomy_group_order"] == 6
    assert bridge["unique_invariant_line"] == [1, 2]
    assert bridge["invariant_complement_count"] == 0
    assert bridge["top_character_values"] == [1]
    assert bridge["quotient_character_values"] == [1, 2]
    assert bridge["nonsplit_extension_witness_count"] == 4
    assert bridge["is_nonsplit_extension_of_sign_by_trivial"] is True
    assert bridge["base_logical_qutrits"] == 81
    assert bridge["short_exact_sequence_dimensions"] == [81, 162, 81]
    assert bridge["matches_flat_internal_dimension_exactly"] is True


def test_synthesis_records_transport_ternary_cocycle_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_ternary_cocycle_bridge"]
    assert bridge["field"] == "F3"
    assert bridge["adapted_group_order"] == 6
    assert bridge["twisted_cocycle_identity_exact"] is True
    assert bridge["cocycle_values_on_sign_trivial_subgroup"] == [0, 1, 2]
    assert bridge["cocycle_is_not_a_coboundary"] is True
    assert bridge["fiber_shift_rank"] == 1
    assert bridge["fiber_shift_square_zero"] is True
    assert bridge["matter_operator_dimension"] == 162
    assert bridge["matter_operator_rank"] == 81
    assert bridge["matter_operator_square_zero"] is True
    assert bridge["matter_operator_image_equals_kernel"] is True


def test_synthesis_records_transport_curvature_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_curvature_bridge"]
    assert bridge["triangles"] == 5280
    assert bridge["all_six_reduced_holonomy_classes_realized"] is True
    assert bridge["curvature_rank_counts"] == {0: 528, 1: 4752}
    assert bridge["curvature_vanishes_exactly_on_identity_holonomy_triangles"] is True
    assert bridge["global_curvature_operator_rank"] == 42
    assert bridge["global_curvature_operator_nullity"] == 48


def test_synthesis_records_transport_borel_factor_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_borel_factor_bridge"]
    assert bridge["group_order"] == 6
    assert bridge["parity0_total"] == 3120
    assert bridge["parity1_total"] == 2160
    assert bridge["flat_total"] == 528
    assert bridge["pure_nilpotent_total"] == 2592
    assert bridge["semisimple_curved_total"] == 2160
    assert bridge["parity0_splits_as_flat_plus_pure_nilpotent"] is True


def test_synthesis_records_transport_twisted_precomplex_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_twisted_precomplex_bridge"]
    assert bridge["c0_dimension"] == 90
    assert bridge["c1_dimension"] == 1440
    assert bridge["c2_dimension"] == 10560
    assert bridge["d0_rank"] == 89
    assert bridge["d1_rank"] == 1393
    assert bridge["d0_lower_left_block_vanishes"] is True
    assert bridge["d1_lower_left_block_vanishes"] is True
    assert bridge["trivial_h0_dimension"] == 1
    assert bridge["trivial_h1_dimension"] == 0
    assert bridge["sign_h0_flat_dimension"] == 0
    assert bridge["semisimple_curvature_rank"] == 42
    assert bridge["semisimple_curvature_support_triangles"] == 2160
    assert bridge["semisimple_curvature_support_equals_parity1_triangles"] is True
    assert bridge["full_curvature_rank"] == 42
    assert bridge["off_diagonal_curvature_rank"] == 36
    assert bridge["curvature_factors_through_sign_quotient"] is True
    assert bridge["upper_right_curvature_identity_exact"] is True


def test_synthesis_records_transport_matter_curved_harmonic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_matter_curved_harmonic_bridge"]
    assert bridge["logical_qutrits"] == 81
    assert bridge["matter_extension_dimension"] == 162
    assert bridge["coupled_c0_dimension"] == 7290
    assert bridge["coupled_c1_dimension"] == 116640
    assert bridge["coupled_c2_dimension"] == 855360
    assert bridge["protected_flat_h0_dimension"] == 81
    assert bridge["full_curvature_rank"] == 3402
    assert bridge["off_diagonal_curvature_rank"] == 2916
    assert bridge["cp2_protected_flat_matter_zero_modes"] == 243
    assert bridge["k3_protected_flat_matter_zero_modes"] == 1944
    assert bridge["cp2_curvature_rank_on_harmonics"] == 10206
    assert bridge["k3_curvature_rank_on_harmonics"] == 81648
    assert bridge["protected_flat_sector_is_exactly_one_81_copy"] is True


def test_synthesis_records_transport_spectral_selector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_spectral_selector_bridge"]
    assert bridge["w33_rank_mod_3"] == 39
    assert bridge["w33_kernel_dimension_mod_3"] == 1
    assert bridge["w33_all_ones_spans_mod_3_kernel"] is True
    assert bridge["transport_projector_rank"] == 1
    assert bridge["transport_walk_gap_exact"] == "7/8"
    assert bridge["transport_kemeny_exact"] == "1952/45"
    assert bridge["a2_positive_laplacian_gap"] == 24
    assert bridge["protected_flat_selector_rank_after_tensoring"] == 81
    assert bridge["matches_protected_flat_matter_dimension"] is True
    assert bridge["protected_flat_curved_harmonic_lifts"] == {
        "CP2_9": 243,
        "K3_16": 1944,
    }


def test_synthesis_records_transport_curved_dirac_refinement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_curved_dirac_refinement_bridge"]
    assert bridge["transport_dirac_dimension"] == 12090
    assert bridge["transport_trace_d_squared"] == 74772
    assert bridge["transport_curvature_corner_rank"] == 42
    assert bridge["matter_dirac_dimension"] == 979290
    assert bridge["matter_trace_d_squared"] == 6056532
    assert bridge["protected_flat_subsector_dimension"] == 81
    assert bridge["transport_constant_limit"] == "1450800/19"
    assert bridge["transport_linear_limit"] == "19370040/19"
    assert bridge["matter_constant_limit"] == "117514800/19"
    assert bridge["matter_linear_limit"] == "1568973240/19"
    assert bridge["cp2_transport_step0_constant"] == "171275/2"
    assert bridge["k3_matter_step0_linear"] == "78270381"


def test_synthesis_records_transport_curved_dirac_quadratic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_curved_dirac_quadratic_bridge"]
    assert bridge["transport_trace_d_fourth"] == 2116184
    assert bridge["matter_trace_d_fourth"] == 171410904
    assert bridge["cp2_transport_seed_quadratic"] == "39997843/3"
    assert bridge["k3_transport_seed_quadratic"] == "36601793/3"
    assert bridge["cp2_transport_sd1_quadratic"] == "4701453583/360"
    assert bridge["k3_transport_sd1_quadratic"] == "5052856873/360"
    assert bridge["cp2_matter_seed_quadratic"] == "1079941761"
    assert bridge["k3_matter_sd1_quadratic"] == "45475711857/40"
    assert bridge["transport_first_refinement_contracts_gap"] is True
    assert bridge["matter_first_refinement_contracts_gap"] is True


def test_synthesis_records_curved_a2_transport_product_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_a2_transport_product_bridge"]
    assert bridge["internal_dimension"] == 90
    assert bridge["internal_laplacian_spectrum"] == {24: 20, 33: 64, 48: 6}
    assert bridge["internal_gap"] == 24
    assert bridge["cp2_product_dimension"] == 22950
    assert bridge["cp2_product_trace"] == 889920
    assert bridge["k3_product_dimension"] == 153360
    assert bridge["k3_product_trace"] == 6030720
    assert bridge["product_heat_factorizes_exactly"] is True
    assert bridge["product_chain_density_limit"] == "10800/19"
    assert bridge["product_trace_density_limit"] == "423000/19"


def test_synthesis_records_curved_a2_heat_density_asymptotics() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_a2_heat_density_asymptotics"]
    assert bridge["persistent_gap"] == 24
    assert bridge["constant_limit"] == "10800/19"
    assert bridge["linear_limit"] == "423000/19"
    assert bridge["cp2_constant_corr_20"] == "1170/19"
    assert bridge["cp2_linear_corr_20"] == "42120/19"
    assert bridge["k3_constant_corr_20"] == "-825/19"
    assert bridge["k3_linear_corr_20"] == "-29700/19"
    assert bridge["step_zero_small_t_checks_improve"] is True


def test_synthesis_records_curved_a2_quadratic_seed_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_a2_quadratic_seed_bridge"]
    assert bridge["cp2_external_second_moment"] == 13392
    assert bridge["k3_external_second_moment"] == 128640
    assert bridge["cp2_triangle_tetra_degree_distribution"] == {3: 21, 4: 27, 5: 27, 6: 9}
    assert bridge["k3_triangle_tetra_degree_distribution"] == {3: 80, 4: 240, 7: 240}
    assert bridge["cp2_quadratic_density_coefficient"] == "491580"
    assert bridge["k3_quadratic_density_coefficient"] == "426060"
    assert bridge["second_order_step_zero_prediction_improves_first_order"] is True


def test_synthesis_records_curved_a2_refined_quadratic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["curved_a2_refined_quadratic_bridge"]
    assert bridge["cp2_sd1_f_vector"] == (255, 2916, 9144, 10800, 4320)
    assert bridge["k3_sd1_f_vector"] == (1704, 22320, 72480, 86400, 34560)
    assert bridge["cp2_sd1_external_second_moment"] == 2104848
    assert bridge["k3_sd1_external_second_moment"] == 22872000
    assert bridge["cp2_sd1_product_quadratic_density_coefficient"] == "908925/2"
    assert bridge["k3_sd1_product_quadratic_density_coefficient"] == "1835497/4"
    assert bridge["seed_quadratic_gap"] == "65520"
    assert bridge["sd1_quadratic_gap"] == "17647/4"
    assert bridge["sd1_f_vectors_match_exact_barycentric_transform_for_both_seeds"] is True
    assert bridge["first_refinement_contracts_cp2_k3_product_quadratic_gap"] is True


def test_synthesis_records_uor_gluing_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["uor_gluing_bridge"]
    assert bridge["all_pairwise_overlaps_are_compatible"] is True
    assert bridge["all_cells_are_covered"] is True
    assert bridge["forward_route_glues_to_canonical_section"] is True
    assert bridge["reverse_route_glues_to_canonical_section"] is True
    assert bridge["full_cover_has_unique_global_section"] is True
    assert bridge["canonical_global_section_is_slot_independent"] is True


def test_synthesis_records_transport_lie_tower_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["transport_lie_tower_bridge"]
    assert bridge["transport_identity_edge_count"] == 192
    assert bridge["transport_reflection_edge_count"] == 396
    assert bridge["transport_three_cycle_edge_count"] == 132
    assert bridge["l6_e6_root_support_size"] == 72
    assert bridge["l6_a2_root_support_size"] == 6
    assert bridge["l6_cartan_support_size"] == 8
    assert bridge["l6_spinor_action_ranks"] == (40, 6, 8)
    assert bridge["complete_oriented_three_generation_graph"] is True
    assert bridge["a2_channels_are_signed_permutation_blocks"] is True
    assert bridge["cartan_modes_are_generation_diagonal"] is True
    assert bridge["current_l6_bridge_activates_only_cartan_modes"] is True


def test_synthesis_records_structural_l6_a2_selection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_a2_selection_bridge"]
    assert bridge["seed_block_unions_h2"] == [[0, 0], [1, 1], [2, 2]]
    assert bridge["seed_block_unions_hbar2"] == [[0, 0], [1, 1], [2, 2]]
    assert bridge["seed_residual_unions_h2"] == [[0, 0], [1, 1], [2, 2]]
    assert bridge["seed_residual_unions_hbar2"] == [[0, 0], [1, 1], [2, 2]]
    assert bridge["seed_yukawas_are_generation_diagonal"] is True
    assert bridge["seed_residuals_are_generation_diagonal"] is True
    assert bridge["a2_zero_response_mode_indices"] == [127, 128]
    assert bridge["a2_nonzero_mode_indices"] == [8, 9, 246, 247]
    assert bridge["a2_nonzero_channels_are_single_off_diagonal_blocks"] is True
    assert bridge["a2_response_channels_stay_single_off_diagonal_blocks"] is True
    assert bridge["replicated_seed_only_realizes_generation_2_star"] is True
    assert bridge["a2_rhs_is_exactly_zero"] is True
    assert bridge["a2_cartan_cross_gram_is_zero"] is True
    assert bridge["current_l6_solution_has_no_active_a2_modes"] is True
    assert bridge["cartan_only_selection_is_structurally_forced"] is True


def test_synthesis_records_exact_l6_a2_mixed_seed_activation_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_a2_mixed_seed_bridge"]
    assert bridge["base_response_rank"] == 9
    assert bridge["base_augmented_rank"] == 10
    assert bridge["minimal_full_activation_seed_size"] == 2
    assert sorted(bridge["minimal_full_activation_seed_modes"]) == [[8, 9], [246, 247]]
    assert bridge["minimal_full_activation_profiles_are_exactly_fans"] is True
    assert bridge["minimal_rank_lift_seed_size"] == 2
    assert sorted(bridge["minimal_rank_lift_seed_modes"]) == [
        [8, 246],
        [8, 247],
        [9, 246],
        [9, 247],
    ]
    assert bridge["minimal_rank_lift_profiles_are_paths_or_bidirected_edges"] is True
    assert bridge["max_response_rank"] == 11
    assert bridge["max_augmented_rank"] == 12
    assert bridge["fan_closure_seeds_have_full_3x3_support"] is True
    assert bridge["fan_closure_seeds_have_slotwise_isotropic_off_diagonal_shell"] is True
    assert bridge["fan_closure_seeds_keep_all_six_a2_modes_active"] is True
    assert bridge["single_edge_seed_activates_exact_unordered_edge_pair"] is True
    assert bridge["no_exact_closure_within_unit_a2_seed_family"] is True


def test_synthesis_records_l6_a2_v4_mode_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_a2_v4_mode_bridge"]
    assert bridge["all_mode_blocks_are_pure_right_character_twists"] is True
    assert bridge["pure_a_modes_are_exactly_8_and_128"] is True
    assert bridge["pure_b_modes_are_exactly_9_and_127"] is True
    assert bridge["mixed_i_a_ab_modes_are_exactly_246_and_247"] is True
    assert bridge["all_four_v4_characters_already_realized_on_fan_seed"] is True
    assert bridge["dormant_modes_127_128_awaken_as_single_block_channels"] is True


def test_synthesis_records_delta27_envelope_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_delta27_texture_bridge"]
    assert bridge["fan_closures_match_for_both_slots"] is True
    assert bridge["canonical_closure_is_not_cycle_invariant"] is True
    assert bridge["canonical_closure_has_delta27_envelope_shape"] is True
    assert bridge["cycle_orbit_has_three_distinguished_generations"] is True
    assert bridge["h2_distinguished_generation"] == 0
    assert bridge["hbar2_distinguished_generation"] == 0


def test_synthesis_records_delta27_v4_matrix_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_delta27_v4_bridge"]
    assert bridge["all_off_diagonal_blocks_share_exact_support_for_both_slots"] is True
    assert bridge["all_relative_row_signs_are_trivial_for_both_slots"] is True
    assert bridge["all_off_diagonal_blocks_are_exact_right_sign_twists_for_both_slots"] is True
    assert bridge["four_v4_characters_realized_for_both_slots"] is True
    assert bridge["generators_are_commuting_involutions_for_both_slots"] is True
    assert bridge["pair_character_pattern_is_slot_independent"] is True
    assert bridge["cycle_orbit_preserves_v4_structure_for_both_slots"] is True
    assert bridge["h2_active_right_support_labels"] == ["u_c_1", "u_c_2", "u_c_3", "nu_c"]
    assert bridge["hbar2_active_right_support_labels"] == ["d_c_1", "d_c_2", "d_c_3", "e_c"]
    assert bridge["h2_generator_a_flipped_labels"] == ["u_c_1", "u_c_3"]
    assert bridge["h2_generator_b_flipped_labels"] == ["u_c_2", "nu_c"]
    assert bridge["hbar2_generator_a_flipped_labels"] == ["d_c_1"]
    assert bridge["hbar2_generator_b_flipped_labels"] == ["d_c_2", "d_c_3", "e_c"]
    assert bridge["pair_character_labels"] == {
        "0->1": "I",
        "0->2": "A",
        "1->0": "AB",
        "1->2": "A",
        "2->0": "A",
        "2->1": "B",
    }


def test_synthesis_records_v4_projector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_v4_projector_bridge"]
    assert bridge["minus_minus_projector_vanishes_for_both_slots"] is True
    assert bridge["plus_plus_projector_is_exact_inactive_support_for_both_slots"] is True
    assert bridge["h2_active_support_splits_as_2_plus_2"] is True
    assert bridge["hbar2_active_support_splits_as_1_plus_3"] is True
    assert bridge["h2_plus_minus_support"] == ["u_c_2", "nu_c"]
    assert bridge["h2_minus_plus_support"] == ["u_c_1", "u_c_3"]
    assert bridge["hbar2_plus_minus_support"] == ["d_c_2", "d_c_3", "e_c"]
    assert bridge["hbar2_minus_plus_support"] == ["d_c_1"]


def test_synthesis_records_v4_seed_reconstruction_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_v4_seed_reconstruction_bridge"]
    assert bridge["label_matrix_is_slot_independent"] is True
    assert bridge["expected_label_matrix"] == [
        ["AB", "I", "A"],
        ["AB", "I", "A"],
        ["A", "B", "0"],
    ]
    assert bridge["reconstructs_canonical_closure_exactly_for_both_slots"] is True
    assert bridge["generation_0_diagonal_delta_equals_offdiag_1_to_0_for_both_slots"] is True
    assert bridge["generation_1_diagonal_delta_equals_offdiag_0_to_1_for_both_slots"] is True
    assert bridge["generation_2_diagonal_block_is_unchanged_for_both_slots"] is True
    assert bridge["reference_projector_rank_split_matches_h2_2_plus_2_and_hbar2_3_plus_1"] is True


def test_synthesis_records_v4_closure_selection_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["l6_v4_closure_selection_bridge"]
    assert bridge["forward_fan_is_exact_generation_2_row_for_both_slots"] is True
    assert bridge["reverse_completion_adds_exact_double_ab_i_a_row_for_both_slots"] is True
    assert bridge["reverse_fan_is_exact_two_row_a_column_shell_for_both_slots"] is True
    assert bridge["forward_completion_supplies_exact_missing_ab_i_and_a_b_entries_for_both_slots"] is True
    assert bridge["forward_route_assembles_canonical_label_matrix_for_both_slots"] is True
    assert bridge["reverse_route_assembles_canonical_label_matrix_for_both_slots"] is True
    assert bridge["canonical_label_matrix_is_slot_independent"] is True


def test_synthesis_records_lie_tower_cycle_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["lie_tower_cycle_bridge"]
    assert bridge["l3_support_size"] == 72
    assert bridge["l3_uniform_output_term_count"] == 36
    assert bridge["l4_support_size"] == 81
    assert bridge["l4_uniform_output_term_count"] == 320
    assert bridge["l5_support_size"] == 81
    assert bridge["l5_uniform_output_term_count"] == 3520
    assert bridge["l6_support_size"] == 86
    assert bridge["l6_multi_entry_count"] == 68040
    assert bridge["pure_single_term_layers_before_l6"] is True
    assert bridge["l6_first_full_gauge_return"] is True
    assert bridge["l6_multi_terms_only_cartan_only_democratic"] is True
    assert bridge["l4_effective_mode_count"] == 6
    assert bridge["l6_total_chiral_mode_count"] == 14
    assert bridge["l6_currently_activates_only_cartan"] is True


def test_synthesis_records_lie_tower_s12_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["lie_tower_s12_bridge"]
    assert bridge["s12_total_nonzero_dimension"] == 728
    assert bridge["s12_grade_split"] == [242, 243, 243]
    assert bridge["s12_jacobi_failure_count"] == 6
    assert bridge["sl27_partition"] == [9, 9, 9]
    assert bridge["sl27_a_family_rank"] == 26
    assert bridge["exact_channel_set_matches_across_layers"] is True
    assert bridge["monster_heisenberg_irrep_dimension"] == 729
    assert bridge["phase_resolution_mechanism_exact"] is True
    assert bridge["current_linearized_l6_bridge_activates_only_cartan_modes"] is True


def test_synthesis_records_local_fano_tomotope_model() -> None:
    summary = build_refinement_bridge_synthesis()
    local = summary["fano_tomotope_local_model"]
    assert local["fano_flags"] == 21
    assert local["dual_toroidal_pair_flags"] == 168
    assert local["tetrahedron_midpoint_flags"] == 24
    assert local["fano_point_stabilizer_order"] == 24
    assert local["fano_flag_stabilizer_order"] == 8
    assert local["flag_stabilizer_is_d8"] is True
    assert local["local_tomotope_flags_per_edge"] == 16


def test_synthesis_records_explicit_mobius_fano_surface_split() -> None:
    summary = build_refinement_bridge_synthesis()
    surface = summary["mobius_fano_surface_bridge"]
    assert surface["standard_heptad_size"] == 7
    assert surface["complementary_heptad_size"] == 7
    assert surface["torus_face_count"] == 14
    assert surface["torus_euler_characteristic"] == 0
    assert surface["each_edge_seen_once_per_heptad"] is True
    assert surface["triangle_vertex_incidences"] == 42
    assert surface["triangle_vertex_incidences_equals_two_fano_flag_sets"] is True


def test_synthesis_records_mod7_fano_duality_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["mod7_fano_duality_bridge"]
    assert bridge["quadratic_residues"] == [1, 2, 4]
    assert bridge["quadratic_nonresidues"] == [3, 5, 6]
    assert bridge["decimal_generator_mod_7"] == 3
    assert bridge["decimal_square_mod_7"] == 2
    assert bridge["decimal_generator_order"] == 6
    assert bridge["point_cycle_type"] == {"fixed": [0], "six_cycle": [1, 3, 2, 6, 4, 5]}
    assert bridge["affine_group_order"] == 42
    assert bridge["heptad_preserver_subgroup_order"] == 21
    assert bridge["heptad_duality_coset_order"] == 21
    assert bridge["decimal_and_translation_generate_full_affine_group"] is True
    assert bridge["residues_preserve_each_heptad"] is True
    assert bridge["nonresidues_swap_heptads"] is True
    assert bridge["decimal_power_targets_on_A"] == ["A", "B", "A", "B", "A", "B"]
    assert bridge["odd_decimal_powers_swap_heptads"] is True
    assert bridge["even_decimal_powers_preserve_heptads"] is True
    assert bridge["c6_splits_into_c3_and_z2_shadow"] is True


def test_synthesis_records_explicit_szilassi_dual() -> None:
    summary = build_refinement_bridge_synthesis()
    dual = summary["mobius_szilassi_dual_bridge"]
    assert dual["dual_vertex_count"] == 14
    assert dual["dual_edge_count"] == 21
    assert dual["dual_face_count"] == 7
    assert dual["dual_face_size"] == 6
    assert dual["dual_is_heawood_skeleton"] is True
    assert dual["dual_face_adjacency_is_k7"] is True


def test_synthesis_records_surface_congruence_selector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["surface_congruence_selector_bridge"]
    assert bridge["vertex_integral_residues_mod_12"] == [0, 3, 4, 7]
    assert bridge["face_integral_residues_mod_12"] == [0, 3, 4, 7]
    assert bridge["admissible_residues_are_0_3_4_7"] is True
    assert bridge["tetrahedron_fixed_point_value"] == 4
    assert bridge["tetrahedron_is_self_dual_fixed_point"] is True
    assert bridge["first_toroidal_dual_value"] == 7
    assert bridge["csaszar_and_szilassi_share_first_toroidal_value"] is True


def test_synthesis_records_heawood_harmonic_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_harmonic_bridge"]
    assert bridge["selector_eigenvalues_exact"] == ["2", "2", "2", "2", "2", "2", "9"]
    assert bridge["adjacency_minimal_polynomial"] == "x^4 - 11*x^2 + 18"
    assert bridge["adjacency_quartic_relation_holds"] is True
    assert bridge["laplacian_gap_exact"] == "3 - sqrt(2)"
    assert bridge["tetra_weight_for_same_gap_exact"] == "3/4 - sqrt(2)/4"
    assert bridge["weighted_tetra_nonzero_laplacian_equals_heawood_gap"] is True


def test_synthesis_records_heawood_tetra_radical_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_tetra_radical_bridge"]
    assert bridge["full_laplacian_minimal_polynomial"] == "x (x - 6) (x^2 - 6x + 7)"
    assert bridge["middle_shell_dimension"] == 12
    assert bridge["middle_quadratic_polynomial"] == "x^2 - 6x + 7"
    assert bridge["middle_quadratic_relation_holds"] is True
    assert bridge["middle_branch_eigenvalues_exact"] == {
        "minus": "3 - sqrt(2)",
        "plus": "sqrt(2) + 3",
    }
    assert bridge["middle_branch_multiplicity_each"] == 6
    assert bridge["middle_shell_trace_exact"] == "36"
    assert bridge["middle_shell_pseudodeterminant_exact"] == "117649"
    assert bridge["projector_three_rank"] == 1
    assert bridge["projector_sqrt2_rank"] == 6
    assert bridge["low_shell_projector_rank"] == 7
    assert bridge["weighted_tetra_branch_weights_exact"] == {
        "minus": "3/4 - sqrt(2)/4",
        "plus": "sqrt(2)/4 + 3/4",
    }
    assert bridge["weighted_tetra_minus_spectrum_exact"] == [
        "0",
        "3 - sqrt(2)",
        "3 - sqrt(2)",
        "3 - sqrt(2)",
    ]
    assert bridge["weighted_tetra_plus_spectrum_exact"] == [
        "0",
        "sqrt(2) + 3",
        "sqrt(2) + 3",
        "sqrt(2) + 3",
    ]
    assert bridge["middle_shell_dimension_equals_gauge_dimension"] is True
    assert bridge["low_shell_rank_equals_toroidal_seed_order"] is True
    assert bridge["middle_branch_product_equals_phi6"] is True
    assert bridge["weighted_klein_tetra_minus_realizes_middle_minus_branch"] is True
    assert bridge["weighted_klein_tetra_plus_realizes_middle_plus_branch"] is True


def test_synthesis_records_heawood_klein_symmetry_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_klein_symmetry_bridge"]
    assert bridge["bipartition_preserving_order"] == 168
    assert bridge["full_heawood_order"] == 336
    assert bridge["flag_edge_stabilizer_order"] == 8
    assert bridge["full_edge_stabilizer_order"] == 16
    assert bridge["polarity_formula"] == "i -> -i mod 7"
    assert bridge["polarity_permutation"] == [0, 6, 5, 4, 3, 2, 1]
    assert bridge["polarity_is_incidence_duality"] is True
    assert bridge["polarity_swap_is_involution"] is True
    assert bridge["matches_klein_quartic_orientation_preserving_order"] is True
    assert bridge["full_heawood_order_is_double_klein_order"] is True
    assert bridge["preserving_order_equals_8_times_21"] is True
    assert bridge["full_order_equals_16_times_21"] is True


def test_synthesis_records_heawood_shell_ladder_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["heawood_shell_ladder_bridge"]
    assert bridge["heptad_size"] == 7
    assert bridge["phi6"] == 7
    assert bridge["heawood_vertices"] == 14
    assert bridge["g2_dimension"] == 14
    assert bridge["heawood_edges"] == 21
    assert bridge["ag21_length"] == 21
    assert bridge["hurwitz_unit_order"] == 24
    assert bridge["d4_seed_order"] == 24
    assert bridge["affine_order"] == 42
    assert bridge["preserving_order"] == 168
    assert bridge["full_order"] == 336
    assert bridge["vertices_equal_2_times_phi6"] is True
    assert bridge["vertices_equal_g2_dimension"] is True
    assert bridge["edges_equal_ag21_length"] is True
    assert bridge["affine_order_equals_2_times_ag21"] is True
    assert bridge["preserving_order_equals_hurwitz_units_times_phi6"] is True
    assert bridge["preserving_order_equals_d4_seed_times_phi6"] is True
    assert bridge["full_order_equals_hurwitz_units_times_g2_dimension"] is True
    assert bridge["full_order_equals_d4_seed_times_g2_dimension"] is True
    assert bridge["full_order_equals_affine_order_times_preserving_edge_stabilizer"] is True


def test_synthesis_records_klein_quartic_gf3_tetra_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_quartic_gf3_tetra_bridge"]
    assert bridge["field"] == 3
    assert bridge["point_count"] == 4
    assert bridge["projective_points"] == [
        [0, 0, 1],
        [0, 1, 0],
        [1, 0, 0],
        [1, 1, 1],
    ]
    assert bridge["point_count_equals_q_plus_1"] is True
    assert bridge["point_count_equals_mu"] is True
    assert bridge["no_three_points_are_collinear"] is True
    assert bridge["induced_projective_packet_is_k4"] is True
    assert bridge["point_count_matches_surface_fixed_point"] is True
    assert bridge["tetra_automorphism_order_matches_hurwitz_units"] is True


def test_synthesis_records_surface_hurwitz_flag_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["surface_hurwitz_flag_bridge"]
    assert bridge["q"] == 3
    assert bridge["q_plus_one"] == 4
    assert bridge["phi6"] == 7
    assert bridge["genus_denominator"] == 12
    assert bridge["tetrahedron_fixed_point"] == 4
    assert bridge["nonzero_surface_residues_mod_12"] == [3, 4, 7]
    assert bridge["single_surface_flags"] == 84
    assert bridge["dual_pair_flags"] == 168
    assert bridge["heawood_preserving_order"] == 168
    assert bridge["heawood_full_order"] == 336
    assert bridge["heawood_vertices"] == 14
    assert bridge["heawood_edges"] == 21
    assert bridge["shared_six_channel"] == 6
    assert bridge["nonzero_surface_residues_are_q_q_plus_one_phi6"] is True
    assert bridge["nonzero_surface_residues_add_to_phi6"] is True
    assert bridge["single_surface_flags_equals_product_of_nonzero_surface_residues"] is True
    assert bridge["single_surface_flags_equals_genus_denominator_times_phi6"] is True
    assert bridge["single_surface_flags_equals_heawood_vertices_times_shared_six"] is True
    assert bridge["single_surface_flags_equals_heawood_edges_times_tetrahedron_fixed_point"] is True
    assert bridge["dual_pair_flags_equals_heawood_preserving_order"] is True
    assert bridge["full_heawood_order_equals_four_single_surface_flag_packets"] is True
    assert bridge["q3_is_unique_positive_solution"] is True


def test_synthesis_records_mod12_selector_closure_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["mod12_selector_closure_bridge"]
    assert bridge["modulus"] == 12
    assert bridge["nonzero_surface_residues_mod_12"] == [3, 4, 7]
    assert bridge["q"] == 3
    assert bridge["mu"] == 4
    assert bridge["phi6"] == 7
    assert bridge["theta_w33"] == 10
    assert bridge["k_minus_one"] == 11
    assert bridge["g2_dimension"] == 14
    assert bridge["single_surface_flags"] == 84
    assert bridge["residues_equal_q_mu_phi6"] is True
    assert bridge["q_plus_mu_equals_phi6"] is True
    assert bridge["q_plus_phi6_equals_theta"] is True
    assert bridge["mu_plus_phi6_equals_k_minus_one"] is True
    assert bridge["q_plus_mu_plus_phi6_equals_g2_dimension"] is True
    assert bridge["q_times_mu_times_phi6_equals_single_surface_flags"] is True
    assert bridge["modulus_equals_gauge_dimension"] is True


def test_synthesis_records_decimal_surface_flag_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["decimal_surface_flag_bridge"]
    assert bridge["decimal_generator_mod_7"] == 3
    assert bridge["decimal_generator_order_mod_7"] == 6
    assert bridge["decimal_square_order_mod_7"] == 3
    assert bridge["genus_denominator"] == 12
    assert bridge["first_toroidal_dual_value"] == 7
    assert bridge["phi6"] == 7
    assert bridge["heawood_vertices"] == 14
    assert bridge["heawood_edges"] == 21
    assert bridge["tetrahedral_fixed_point"] == 4
    assert bridge["shared_six_channel"] == 6
    assert bridge["single_surface_flags"] == 84
    assert bridge["decimal_order_equals_shared_six_channel"] is True
    assert bridge["single_surface_flags_equals_12_times_7"] is True
    assert bridge["single_surface_flags_equals_14_times_6"] is True
    assert bridge["single_surface_flags_equals_21_times_4"] is True
    assert bridge["decimal_order_plus_one_equals_first_toroidal_value"] is True


def test_synthesis_records_surface_physics_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["surface_physics_shell_bridge"]
    assert bridge["gauge_dimension"] == 12
    assert bridge["gauge_dimension_decomposition"] == [8, 3, 1]
    assert bridge["beta0_qcd"] == 7
    assert bridge["shared_six_channel"] == 6
    assert bridge["g2_dimension"] == 14
    assert bridge["topological_shell"] == 28
    assert bridge["quartic_e7_packet"] == 56
    assert bridge["single_surface_flags"] == 84
    assert bridge["dual_pair_flags"] == 168
    assert bridge["full_heawood_order"] == 336
    assert bridge["gauge_dimension_equals_8_plus_3_plus_1"] is True
    assert bridge["single_surface_flags_equals_gauge_dimension_times_beta0"] is True
    assert bridge["single_surface_flags_equals_g2_dimension_times_shared_six"] is True
    assert bridge["dual_pair_flags_equals_gauge_dimension_times_g2_dimension"] is True
    assert bridge["dual_pair_flags_equals_shared_six_times_topological_shell"] is True
    assert bridge["full_heawood_order_equals_gauge_dimension_times_topological_shell"] is True
    assert bridge["full_heawood_order_equals_shared_six_times_quartic_e7_packet"] is True


def test_synthesis_records_toroidal_k7_spectral_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["toroidal_k7_spectral_bridge"]
    assert bridge["toroidal_seed_order"] == 7
    assert bridge["csaszar_vertex_graph"] == "K7"
    assert bridge["szilassi_face_graph"] == "K7"
    assert bridge["adjacency_spectrum"] == [6, -1, -1, -1, -1, -1, -1]
    assert bridge["laplacian_spectrum"] == [0, 7, 7, 7, 7, 7, 7]
    assert bridge["selector_line_dimension"] == 1
    assert bridge["shared_six_channel"] == 6
    assert bridge["phi6"] == 7
    assert bridge["adjacency_square_trace"] == 42
    assert bridge["laplacian_trace"] == 42
    assert bridge["csaszar_vertex_graph_is_k7"] is True
    assert bridge["szilassi_face_graph_is_k7"] is True
    assert bridge["selector_plus_shared_six_equals_toroidal_seed_order"] is True
    assert bridge["nontrivial_laplacian_mode_equals_phi6"] is True
    assert bridge["nontrivial_adjacency_multiplicity_equals_shared_six"] is True
    assert bridge["laplacian_trace_equals_shared_six_times_phi6"] is True
    assert bridge["adjacency_square_trace_equals_shared_six_times_phi6"] is True


def test_synthesis_records_fano_toroidal_complement_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["fano_toroidal_complement_bridge"]
    assert bridge["space_dimension"] == 7
    assert bridge["fano_selector_formula"] == "2I + J"
    assert bridge["toroidal_laplacian_formula"] == "7I - J"
    assert bridge["complement_formula"] == "9I"
    assert bridge["q_squared"] == 9
    assert bridge["selector_spectrum_exact"] == ["2", "2", "2", "2", "2", "2", "9"]
    assert bridge["toroidal_laplacian_spectrum_exact"] == [0, 7, 7, 7, 7, 7, 7]
    assert bridge["selector_trace"] == 21
    assert bridge["selector_nontrivial_trace"] == 12
    assert bridge["toroidal_trace"] == 42
    assert bridge["combined_trace"] == 63
    assert bridge["combined_nontrivial_trace"] == 54
    assert bridge["selector_determinant"] == 576
    assert bridge["selector_determinant_square_root"] == 24
    assert bridge["selector_minimal_polynomial"] == "x^2 - 11x + 18"
    assert bridge["complement_operator_equals_q_squared_identity"] is True
    assert bridge["selector_trace_equals_ag21_length"] is True
    assert bridge["selector_nontrivial_trace_equals_gauge_dimension"] is True
    assert bridge["toroidal_trace_equals_6_times_phi6"] is True
    assert bridge["combined_nontrivial_trace_equals_exceptional_projector_rank"] is True
    assert bridge["selector_determinant_square_root_equals_hurwitz_unit_shell"] is True
    assert bridge["selector_quadratic_matches_heawood_quartic_in_x_squared"] is True
    assert bridge["gauge_plus_toroidal_equals_exceptional_rank"] is True


def test_synthesis_records_klein_hurwitz_extremal_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["klein_hurwitz_extremal_bridge"]
    assert bridge["klein_quartic_genus"] == 3
    assert bridge["hurwitz_coefficient"] == 84
    assert bridge["heawood_preserving_order"] == 168
    assert bridge["heawood_full_order"] == 336
    assert bridge["standard_model_gauge_dimension"] == 12
    assert bridge["phi6"] == 7
    assert bridge["g2_dimension"] == 14
    assert bridge["preserving_order_equals_hurwitz_bound_at_genus_3"] is True
    assert bridge["preserving_order_equals_two_times_hurwitz_coefficient"] is True
    assert bridge["preserving_order_equals_2_k_phi6"] is True
    assert bridge["preserving_order_equals_k_times_g2_dimension"] is True
    assert bridge["full_order_equals_two_times_preserving_order"] is True
    assert bridge["full_order_equals_four_times_hurwitz_coefficient"] is True


def test_synthesis_records_hurwitz_237_selector_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["hurwitz_237_selector_bridge"]
    assert bridge["triangle_signature"] == [2, 3, 7]
    assert bridge["duality_sheet_flip_order"] == 2
    assert bridge["q"] == 3
    assert bridge["phi6"] == 7
    assert bridge["affine_shell_order"] == 42
    assert bridge["single_surface_flags"] == 84
    assert bridge["heawood_preserving_order"] == 168
    assert bridge["heawood_full_order"] == 336
    assert bridge["affine_shell_equals_2_3_7"] is True
    assert bridge["affine_shell_is_agl_1_7"] is True
    assert bridge["decimal_c6_splits_into_c3_and_z2"] is True
    assert bridge["single_surface_flags_equals_2_times_affine_shell"] is True
    assert bridge["heawood_preserving_equals_4_times_affine_shell"] is True
    assert bridge["heawood_full_equals_8_times_affine_shell"] is True


def test_synthesis_records_affine_middle_shell_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["affine_middle_shell_bridge"]
    assert bridge["duality_factor"] == 2
    assert bridge["q"] == 3
    assert bridge["phi6"] == 7
    assert bridge["ag21_length"] == 21
    assert bridge["g2_dimension"] == 14
    assert bridge["shared_six_channel"] == 6
    assert bridge["affine_shell_order"] == 42
    assert bridge["affine_shell_equals_2_times_ag21"] is True
    assert bridge["affine_shell_equals_q_times_g2"] is True
    assert bridge["affine_shell_equals_shared_six_times_phi6"] is True
    assert bridge["ag21_equals_3_times_phi6"] is True
    assert bridge["g2_equals_2_times_phi6"] is True
    assert bridge["shared_six_equals_2_times_q"] is True


def test_synthesis_records_realization_orbit_package() -> None:
    summary = build_refinement_bridge_synthesis()
    realization = summary["realization_orbit_bridge"]
    assert realization["catalog_total"] == 7
    assert realization["common_symmetry_group"] == "Z2"
    assert realization["csaszar_vertex_orbits"] == 4
    assert realization["csaszar_face_orbits"] == 7
    assert realization["szilassi_vertex_orbits"] == 7
    assert realization["szilassi_face_orbits"] == 4
    assert realization["orbit_package_is_dual"] is True


def test_synthesis_records_witting_srg_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    witting = summary["witting_srg_bridge"]
    assert witting["states"] == 40
    assert witting["orthogonal_tetrads"] == 40
    assert witting["degree"] == 12
    assert witting["lambda_parameter"] == 2
    assert witting["mu_parameter"] == 4
    assert witting["graph_isomorphic_to_standard_w33"] is True
    assert witting["tetrads_match_symplectic_lines"] is True


def test_synthesis_records_cover_and_klitzing_towers() -> None:
    summary = build_refinement_bridge_synthesis()
    tower = summary["cover_and_operation_tower"]
    assert tower["aut_universal_equals_tomotope_flags"] is True
    assert tower["regular_cover_equals_flags_squared"] is True
    assert tower["klitzing_ladder"] == [12, 24, 48, 96]
    assert tower["klitzing_doublings"] == [2, 2, 2]


def test_synthesis_records_tomotope_partial_sheet_bridge() -> None:
    summary = build_refinement_bridge_synthesis()
    bridge = summary["tomotope_partial_sheet_bridge"]
    assert bridge["partial_a"] == [8, 24, 32, 8, 8]
    assert bridge["partial_b"] == [4, 12, 16, 4, 4]
    assert bridge["entrywise_ratio"] == [2, 2, 2, 2, 2]
    assert bridge["partial_a_equals_two_times_partial_b"] is True
    assert bridge["partial_b_matches_tomotope_edge_triangle_cell_counts"] is True
    assert bridge["partial_a_matches_universal_edge_triangle_cell_counts"] is True
    assert bridge["automorphism_ratio_matches_sheet_doubling"] is True
    assert bridge["flag_ratio_matches_sheet_doubling"] is True
    assert bridge["monodromy_ratio_is_quadratic_not_linear"] is True


def test_write_summary_emits_json(tmp_path: Path) -> None:
    out = write_summary(tmp_path / "w33_refinement_bridge_synthesis_summary.json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["focused_test_stack_size"] >= 503
