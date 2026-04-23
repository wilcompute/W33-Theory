from __future__ import annotations

from scripts.w33_temporal_spectral_toroidal_computer_audit import (
    analyze,
    classify_temporal_spectral_toroidal_computer,
)


def test_temporal_spectral_toroidal_computer_theorem_is_honest_and_constructive() -> None:
    payload = analyze()
    theorem = payload["temporal_spectral_toroidal_computer_theorem"]

    assert theorem["the_exact_w33_kernel_is_already_a_9dimensional_two_qutrit_processor"] is True
    assert theorem["the_exact_local_shell_is_a_projective_screen_plus_affine_bulk"] is True
    assert theorem["the_exact_36_spreads_are_36_complete_two_qutrit_measurement_programs"] is True
    assert theorem["the_exact_toroidal_seed_is_one_selector_plus_six_phi6_modes_on_the_first_closed_torus"] is True
    assert theorem["the_single_photon_temporal_spectral_hardware_dictionary_matches_the_exact_finite_counts"] is True
    assert theorem["the_remaining_nonclifford_universality_frontier_is_two_quartic_nonlinear_injection_channels"] is True
    assert theorem["the_realization_claim_is_a_conservative_hardware_hypothesis_not_a_finished_device_theorem"] is True


def test_temporal_spectral_toroidal_computer_records_keep_exact_and_hypothesis_layers_separate() -> None:
    records = {record["name"]: record for record in classify_temporal_spectral_toroidal_computer()}

    processor = records["exact_two_qutrit_processor"]["evidence"]
    screen = records["exact_screen_bulk_measurement_layer"]["evidence"]
    torus = records["exact_toroidal_harmonic_seed"]["evidence"]
    hardware = records["conservative_single_photon_hardware_hypothesis"]["evidence"]
    boundary = records["honest_photonic_universality_boundary"]["evidence"]

    assert processor["two_qutrit_hilbert_dimension"] == 9
    assert processor["projective_pauli_class_count"] == 40
    assert processor["weyl_operator_basis_size"] == 81
    assert processor["w33_vertex_count"] == 40
    assert processor["w33_edge_count"] == 240
    assert processor["all_symplectic_generators_verified"] is True
    assert processor["local_h27_size"] == 27
    assert processor["tetra_vertex_packet_dimension"] == 4
    assert processor["tetra_axis_packet_dimension"] == 3
    assert processor["transport_bundle_dimension"] == 135
    assert processor["transport_bundle_real_split"] == (1, 2)

    assert screen["projective_screen_size"] == 13
    assert screen["affine_bulk_size"] == 27
    assert screen["affine_direction_count"] == 13
    assert screen["anchor_fiber_count"] == 9
    assert screen["anchor_fiber_size"] == 3
    assert screen["spread_count"] == 36
    assert screen["spread_size"] == 10
    assert screen["sample_memory_lines"] == 1
    assert screen["sample_affine_measurement_lines"] == 9
    assert screen["mub_max_deviation"] < 1e-12

    assert torus["selector_line_dimension"] == 1
    assert torus["shared_six_channel"] == 6
    assert torus["phi6"] == 7
    assert torus["first_closed_torus_genus"] == 1
    assert torus["toroidal_seed_order"] == 7
    assert torus["nontrivial_spectral_trace"] == 42
    assert torus["tetrahedral_chart_vertices"] == 4
    assert torus["tetrahedral_local_modes"] == 3
    assert torus["tetrahedral_directed_packet"] == 12
    assert torus["balanced_chirality_split"] == (2, 2)
    assert torus["synthetic_torus_shape"] == (3, 3)
    assert torus["synthetic_torus_cell_count"] == 9

    assert hardware["carrier"] == "single photon"
    assert hardware["commuting_degrees_of_freedom"] == (
        "temporal_mode_qutrit",
        "synthetic_frequency_qutrit",
    )
    assert hardware["temporal_qutrit_labels"] == ("past", "now", "future")
    assert hardware["spectral_qutrit_labels"] == ("lower_sideband", "carrier", "upper_sideband")
    assert hardware["single_photon_hilbert_dimension"] == 9
    assert hardware["discrete_torus_shape"] == (3, 3)
    assert hardware["measurement_program_count"] == 36
    assert hardware["measurement_bases_per_program"] == 10
    assert hardware["harmonic_selector_packet"] == (1, 6, 7)
    assert hardware["quartic_magic_atom_count"] == 2
    assert hardware["quartic_magic_min_degree"] == 4
    assert "retrocausality" not in hardware["realization_boundary_note"].lower()

    assert boundary["clifford_processor_is_exact"] is True
    assert boundary["complete_measurement_layer_is_exact"] is True
    assert boundary["harmonic_toroidal_seed_is_exact"] is True
    assert boundary["nonclifford_frontier_is_two_quartic_atoms"] is True
    assert boundary["full_yukawa_eigenvalue_spectrum_still_open"] is True
