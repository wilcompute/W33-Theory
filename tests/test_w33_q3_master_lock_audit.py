from __future__ import annotations

from scripts.w33_q3_master_lock_audit import (
    analyze,
    classify_q3_master_lock,
    q3_continuum_seed_summary,
    q3_fermion_seed_summary,
    q3_local_kernel_summary,
    q3_spectral_uniqueness_summary,
    q3_transport_algebra_summary,
    symbolic_q3_lock_summary,
)


def test_symbolic_q3_lock_summary_has_exact_gap_factors() -> None:
    summary = symbolic_q3_lock_summary()

    assert summary["n_zero_gap"] == "(q - 3)*(q + 1)*(q**2 + 1)"
    assert summary["m2_minus_k_gap"] == "-q*(q - 3)*(q + 1)/(q - 1)"
    assert summary["disc_r_plus_4phi4_gap"] == "(q - 3)**2"
    assert summary["disc_s_plus_4phi6_gap"] == "(q - 3)**2"
    assert summary["q3_evaluations"] == {
        "n_zero_gap_at_3": 0,
        "m2_minus_k_gap_at_3": 0,
        "disc_r_gap_at_3": 0,
        "disc_s_gap_at_3": 0,
    }
    assert summary["exact_factors"] == {
        "n_zero_gap_factor_is_exact": True,
        "m2_minus_k_gap_factor_is_exact": True,
        "disc_r_gap_factor_is_exact": True,
        "disc_s_gap_factor_is_exact": True,
        "all_symbolic_gaps_vanish_at_q3": True,
    }


def test_q3_local_kernel_summary_matches_finite_qutrit_packet() -> None:
    summary = q3_local_kernel_summary()

    assert summary["q"] == 3
    assert summary["phi3"] == 13
    assert summary["phi4"] == 10
    assert summary["phi6"] == 7
    assert summary["visible_shell_size"] == 27
    assert summary["fiber_count"] == 9
    assert summary["fiber_size"] == 3
    assert summary["line_size"] == 4
    assert summary["lines_per_point"] == 4
    assert summary["projective_point_count"] == 40
    assert summary["edge_count"] == 240
    assert summary["e8_root_count"] == 240
    assert summary["cartan_rank_candidate"] == 8
    assert all(summary["exact_factorizations"].values())


def test_q3_spectral_uniqueness_summary_matches_corrected_live_packet() -> None:
    summary = q3_spectral_uniqueness_summary()

    assert summary["q"] == 3
    assert summary["srg_parameters"] == (40, 12, 2, 4)
    assert summary["adjacency_eigenpairs"] == ((12, 1), (2, 24), (-4, 15))
    assert summary["bipartite_zero_mode_count"] == 0
    assert summary["canonical_hamiltonian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
    assert summary["fourth_moment_per_vertex"] == 624
    assert summary["even_moment_characteristic_roots"] == (144, 16, 4)
    assert summary["even_moment_recurrence_coefficients"] == (164, -2944, 9216)
    assert summary["ihara_nontrivial_discriminants"] == (-40, -28)
    assert summary["expected_discriminants"] == (-40, -28)
    assert summary["zeta_regularised_determinant"] == 10**24 * 16**15
    assert all(summary["exact_factorizations"].values())


def test_q3_continuum_seed_summary_matches_exact_coefficient_seed() -> None:
    summary = q3_continuum_seed_summary()

    assert summary["q"] == 3
    assert summary["phi3"] == 13
    assert summary["phi6"] == 7
    assert summary["cartan_packet"] == 8
    assert summary["topological_packet"] == 56
    assert summary["continuum_eh_coefficient"] == 320
    assert summary["topological_coefficient"] == 2240
    assert summary["discrete_eh_coefficient"] == 12480
    assert summary["rank39"] == 39
    assert summary["spectral_negative_weight"] == 4
    assert summary["total_mode_count"] == 80
    assert all(summary["exact_factorizations"].values())


def test_q3_fermion_seed_summary_matches_exact_backbone_splice() -> None:
    summary = q3_fermion_seed_summary()

    assert summary["q"] == 3
    assert summary["mu"] == 4
    assert summary["phi6"] == 7
    assert summary["cartan_packet"] == 8
    assert summary["shifted_gaussian_norm"] == 17
    assert summary["up_sector_suppressor"] == 136
    assert summary["barrier_shell"] == 98
    assert summary["g2_dimension"] == 14
    assert summary["charged_lepton_shell"] == 208
    assert summary["f4_dimension"] == 52
    assert summary["discrete_6_mode_over_a0"] == 26
    assert all(summary["exact_factorizations"].values())


def test_q3_transport_algebra_summary_reduces_the_live_wall_to_one_witness() -> None:
    summary = q3_transport_algebra_summary()

    assert summary["triangle_count"] == 5280
    assert summary["parity0_triangles"] == 3120
    assert summary["parity1_triangles"] == 2160
    assert summary["identity_triangle_holonomies"] == 240
    assert summary["three_cycle_triangle_holonomies"] == 2880
    assert summary["transposition_triangle_holonomies"] == 2160
    assert summary["fiber_shift_matrix"] == [[0, 1], [0, 0]]
    assert summary["canonical_nontrivial_holonomy"] == [[1, 1], [0, 1]]
    assert summary["gauge_related_nontrivial_holonomy"] == [[1, 2], [0, 1]]
    assert summary["current_sign_trivial_holonomies"] == [[[1, 0], [0, 1]]]
    assert summary["canonical_nonzero_increment"] == [[0, 1], [0, 0]]
    assert summary["gauge_related_nonzero_increment"] == [[0, 2], [0, 0]]
    assert summary["current_nilpotent_increment"] == [[0, 0], [0, 0]]
    assert summary["current_nonzero_nilpotent_increments"] == []
    assert summary["minimal_tail_slot_state"] == "unique_nonzero_orbit_in_existing_glue_slot"
    assert summary["minimal_tail_primitive_generator"] == {
        "C": "780",
        "L": "7944",
        "Q_seed": "62600",
        "Q_sd1": "53979",
    }
    assert summary["minimal_tail_transport_pair"] == {
        "denominator_lcm": 12,
        "cleared_coordinate_gcd": 217,
        "recovered_scale": "217/12",
    }
    assert summary["promoted_coordinate_witnesses"] == {
        "C": {
            "primitive_coordinate": "780",
            "exact_coordinate": "14105",
            "recovered_scale": "217/12",
        },
        "L": {
            "primitive_coordinate": "7944",
            "exact_coordinate": "143654",
            "recovered_scale": "217/12",
        },
        "Q_seed": {
            "primitive_coordinate": "62600",
            "exact_coordinate": "3396050/3",
            "recovered_scale": "217/12",
        },
        "Q_sd1": {
            "primitive_coordinate": "53979",
            "exact_coordinate": "3904481/4",
            "recovered_scale": "217/12",
        },
    }
    assert summary["current_coordinate_witness_matches"] == {
        "C": False,
        "L": False,
        "Q_seed": False,
        "Q_sd1": False,
    }
    assert summary["canonical_chart_target"] == {
        "coordinate": "dC",
        "required_value": "14105",
        "primitive_c_direction": "780",
        "transport_scale": "217/12",
        "factorization": "780 * (217/12)",
    }
    assert all(summary["exact_factorizations"].values())


def test_q3_master_lock_analysis_keeps_the_boundary_honest() -> None:
    records = {record["name"]: record for record in classify_q3_master_lock()}
    summary = analyze()
    theorem = summary["q3_master_lock_theorem"]

    assert records["q3_local_qutrit_kernel_lock"]["support_level"] == "repo-exact finite kernel"
    assert records["q3_spectral_ihara_uniqueness_lock"]["support_level"] == "repo-exact spectral uniqueness"
    assert records["q3_toroidal_continuum_seed_lock"]["support_level"] == "repo-exact continuum seed"
    assert records["q3_electron_seed_backbone_lock"]["support_level"] == "repo-exact fermion seed"
    assert records["q3_transport_holonomy_reduction_lock"]["support_level"] == "repo-exact transport algebra reduction"
    assert records["q3_full_physical_realization_theorem"]["support_level"] == "not-yet-exact smooth realization theorem"

    assert summary["status"] == "ok"
    assert summary["record_names_exact_or_boundary"] == (
        "q3_local_qutrit_kernel_lock",
        "q3_spectral_ihara_uniqueness_lock",
        "q3_toroidal_continuum_seed_lock",
        "q3_electron_seed_backbone_lock",
        "q3_transport_holonomy_reduction_lock",
    )
    assert summary["record_names_open"] == ("q3_full_physical_realization_theorem",)
    assert theorem["the_local_kernel_exactly_realizes_the_q3_packet_1_3_9_27_40_240"] is True
    assert theorem["the_corrected_spectral_core_exactly_realizes_the_q3_lock"] is True
    assert theorem["the_continuum_seed_exactly_realizes_the_q3_packet_8_56_320_2240_12480"] is True
    assert theorem["the_electron_seed_packet_exactly_splices_into_the_same_q3_backbone"] is True
    assert theorem["the_q3_lock_is_now_overdetermined_across_local_spectral_and_continuum_seed_layers"] is True
    assert theorem["the_q3_lock_is_now_overdetermined_across_local_spectral_continuum_and_electron_seed_layers"] is True
    assert theorem["the_transport_algebra_exactly_reduces_the_smooth_realization_wall_to_one_unipotent_sign_trivial_witness"] is True
    assert theorem["the_transport_algebra_exactly_refines_the_same_wall_to_one_nonzero_nilpotent_increment"] is True
    assert theorem["the_remaining_wall_refines_to_the_first_sign_trivial_unipotent_transport_witness"] is True
    assert theorem["the_remaining_wall_refines_equivalently_to_the_first_nonzero_nilpotent_holonomy_increment"] is True
    assert theorem["the_next_exact_positive_target_is_the_unique_minimal_tail_datum_in_the_existing_slot"] is True
    assert theorem["the_remaining_wall_refines_further_to_any_one_promoted_coordinate_witness_equivalently_dC_equals_14105"] is True
    assert theorem["the_remaining_wall_is_not_finite_q_selection_but_smooth_realization"] is True
    assert "non-identity unipotent sign-trivial transport witness" in summary["boundary_note"]
    assert "nonzero nilpotent holonomy increment" in summary["boundary_note"]
    assert "217/12" in summary["boundary_note"]
    assert "dC = 14105" in summary["boundary_note"]
