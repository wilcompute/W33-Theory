from __future__ import annotations

from scripts.w33_standard_model_tqc_boundary_audit import (
    analyze,
    classify_tqc_standard_model_boundary,
)


def test_tqc_standard_model_boundary_theorem_is_honest_and_constructive() -> None:
    payload = analyze()
    theorem = payload["tqc_standard_model_boundary_theorem"]

    assert theorem["the_exact_repo_contains_a_two_qutrit_pauli_clifford_backbone"] is True
    assert theorem["the_local_standard_model_carrier_is_exactly_a_three_qutrit_shell"] is True
    assert theorem["the_transport_and_control_packet_close_as_one_exact_tetra_qutrit_primitive"] is True
    assert theorem["the_exact_standard_model_backbone_is_fixed_while_the_yukawa_nonclifford_resource_remains_open"] is True
    assert theorem["the_current_exact_tqc_read_is_qutrit_clifford_plus_tetra_control_transport_not_yet_braiding_universal"] is True


def test_tqc_standard_model_boundary_records_keep_exact_and_open_layers_separate() -> None:
    records = {record["name"]: record for record in classify_tqc_standard_model_boundary()}

    clifford = records["exact_qutrit_clifford_backbone"]["evidence"]
    tetra = records["exact_tetra_qutrit_control_transport_primitive"]["evidence"]
    sm = records["exact_standard_model_action_backbone"]["evidence"]
    boundary = records["honest_universality_boundary"]["evidence"]

    assert clifford["w33_vertex_count"] == 40
    assert clifford["w33_edge_count"] == 240
    assert clifford["projective_pauli_point_count"] == 40
    assert clifford["weyl_basis_size"] == 81
    assert clifford["all_symplectic_generators_verified"] is True
    assert clifford["local_h27_size"] == 27
    assert clifford["local_triangle_sizes"] == (3, 3, 3, 3)
    assert clifford["local_fiber_sizes"] == (3, 3, 3, 3, 3, 3, 3, 3, 3)
    assert clifford["inter_fiber_counts"] == (3,)
    assert clifford["h27_internal_triangle_count"] == 36
    assert clifford["canonical_hamiltonian_spectrum"] == ((0, 1), (10, 24), (16, 15))

    assert tetra["tetra_vertex_packet_dimension"] == 4
    assert tetra["tetra_axis_packet_dimension"] == 3
    assert tetra["chart_axis_matches_canonical_tetra_axis_up_to_relabels"] is True
    assert tetra["axis_group_order"] == 6
    assert tetra["axis_group_is_exact_s3"] is True
    assert tetra["local_axis_packet_dimension"] == 3
    assert tetra["real_decomposition"] == (1, 2)
    assert tetra["global_bundle_dimension"] == 135
    assert tetra["global_radial_dimension"] == 45
    assert tetra["global_tangential_dimension"] == 90
    assert tetra["all_six_axis_permutations_occur_on_transport_edges"] is True
    assert tetra["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
    assert tetra["transport_135_is_45_times_3"] is True
    assert tetra["transport_90_is_45_times_2"] is True

    assert sm["fermion_representation_dimension"] == 16
    assert sm["three_generation_matter_dimension"] == 48
    assert sm["decomposition_16_equals_6_3_3_2_1_1"] is True
    assert sm["bosonic_action_complete"] is True
    assert sm["mixing_backbone_complete"] is True
    assert sm["all_anomalies_cancel"] is True
    assert sm["full_yukawa_eigenvalue_spectrum_still_open"] is True

    assert boundary["all_symplectic_generators_verified"] is True
    assert boundary["axis_group_is_exact_s3"] is True
    assert boundary["transport_cycle_diagonalizes_to_qutrit_packet_up_to_orientation"] is True
    assert boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
