from __future__ import annotations

from scripts.w33_standard_model_magic_packet_audit import (
    analyze,
    classify_standard_model_magic_packet,
)


def test_standard_model_magic_packet_theorem_is_sharp_and_honest() -> None:
    payload = analyze()
    theorem = payload["standard_model_magic_packet_theorem"]

    assert theorem["the_exact_repo_already_contains_a_qutrit_clifford_processor"] is True
    assert theorem["the_exact_repo_already_contains_a_tetra_qutrit_control_transport_bus"] is True
    assert theorem["the_generation_algebra_is_already_an_exact_qutrit_memory_packet"] is True
    assert theorem["the_exact_nonclifford_frontier_has_collapsed_to_a_two_slot_quartic_magic_packet"] is True
    assert theorem["the_current_exact_universality_read_is_clifford_processor_plus_minimal_magic_packet_not_yet_explicit_injection"] is True


def test_standard_model_magic_packet_records_separate_processor_bus_memory_and_magic() -> None:
    records = {record["name"]: record for record in classify_standard_model_magic_packet()}

    processor = records["qutrit_clifford_processor"]["evidence"]
    bus = records["tetra_qutrit_control_transport_bus"]["evidence"]
    memory = records["qutrit_generation_memory"]["evidence"]
    magic = records["minimal_magic_packet_candidate"]["evidence"]
    boundary = records["honest_universality_boundary"]["evidence"]

    assert processor["w33_vertex_count"] == 40
    assert processor["w33_edge_count"] == 240
    assert processor["projective_pauli_point_count"] == 40
    assert processor["weyl_basis_size"] == 81
    assert processor["all_symplectic_generators_verified"] is True
    assert processor["local_h27_size"] == 27
    assert processor["local_triangle_sizes"] == (3, 3, 3, 3)
    assert processor["local_fiber_sizes"] == (3, 3, 3, 3, 3, 3, 3, 3, 3)
    assert processor["inter_fiber_counts"] == (3,)
    assert processor["h27_internal_triangle_count"] == 36
    assert processor["canonical_hamiltonian_spectrum"] == ((0, 1), (10, 24), (16, 15))

    assert bus["axis_group_order"] == 6
    assert bus["axis_group_is_exact_s3"] is True
    assert bus["local_axis_packet_dimension"] == 3
    assert bus["real_decomposition"] == (1, 2)
    assert bus["global_bundle_dimension"] == 135
    assert bus["global_radial_dimension"] == 45
    assert bus["global_tangential_dimension"] == 90
    assert bus["all_six_axis_permutations_occur_on_transport_edges"] is True
    assert bus["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
    assert bus["transport_135_is_45_times_3"] is True
    assert bus["transport_90_is_45_times_2"] is True

    assert memory["generation_reduces_to_one_c3_mod3"] is True
    assert memory["generation_module_is_regular_c3_module"] is True
    assert memory["repo_common_flag_matches_regular_module_loewy_flag"] is True
    assert memory["complex_regular_module_splits_as_qutrit_packet"] is True
    assert memory["repo_line_generator"] == (1, 1, 0)
    assert memory["line_in_cycle_basis"] == (1, 1, 1)
    assert memory["plane_in_cycle_basis"] == ((1, 1, 1), (0, 2, 1))
    assert memory["line_maps_to_fixed_line"] is True
    assert memory["plane_maps_to_augmentation_plane"] is True
    assert memory["fixed_line_equals_kernel_of_cycle_minus_identity"] is True
    assert memory["augmentation_plane_equals_image_of_cycle_minus_identity"] is True

    assert magic["packet_size"] == 2
    assert magic["scaled_signed_variable"] == "x = 240 * sigma"
    assert magic["scaled_squared_variable"] == "u = x^2 = 57600 * sigma^2"
    assert magic["h2_quartic_polynomial"] == "x**4 - 542*x**2 + 61200"
    assert magic["hbar2_quartic_polynomial"] == "x**4 - 982*x**2 + 137232"
    assert magic["h2_galois_group_label"] == "D4"
    assert magic["h2_galois_group_order"] == 8
    assert magic["hbar2_galois_group_label"] == "D4"
    assert magic["hbar2_galois_group_order"] == 8
    assert magic["shared_quadratic_subfield_squarefree_parts"] == ()
    assert magic["quartic_root_fields_are_linearly_disjoint_over_q"] is True
    assert magic["quartic_root_field_compositum_degree"] == 16
    assert magic["d4_splitting_fields_are_linearly_disjoint_over_q"] is True
    assert magic["quartic_splitting_field_compositum_degree"] == 64
    assert magic["quartic_splitting_field_galois_group"] == "D4 x D4"
    assert magic["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True

    assert boundary["bosonic_action_fixed"] is True
    assert boundary["all_anomalies_cancel"] is True
    assert boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
    assert boundary["remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"] is True
