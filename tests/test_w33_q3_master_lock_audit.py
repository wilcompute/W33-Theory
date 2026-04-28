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
    assert summary["representation_triangle_gap"] == "q*(q - 3)*(q + 1)"
    assert summary["q3_evaluations"] == {
        "n_zero_gap_at_3": 0,
        "m2_minus_k_gap_at_3": 0,
        "disc_r_gap_at_3": 0,
        "disc_s_gap_at_3": 0,
        "representation_triangle_gap_at_3": 0,
    }
    assert summary["exact_factors"] == {
        "n_zero_gap_factor_is_exact": True,
        "m2_minus_k_gap_factor_is_exact": True,
        "disc_r_gap_factor_is_exact": True,
        "disc_s_gap_factor_is_exact": True,
        "representation_triangle_gap_factor_is_exact": True,
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
    assert summary["parseval_measurement_frame"] == {
        "line_module_resolution": "40 = 1 + 15 + 24",
        "spread_count": 36,
        "anti_line_count": 90,
        "spread_density": "1/4",
        "anti_line_density": "2/5",
        "centered_spread_probe_spectrum": {0: 25, 18: 15},
        "centered_anti_line_probe_spectrum": {0: 16, 36: 24},
    }
    assert summary["parseval_representation_triangle"] == {
        "line_module": "40 = 1 + 15 + 24",
        "spread_module": "36 = 1 + 15 + 20",
        "anti_line_quotient_module": "45 = 1 + 24 + 20",
        "total_dimension_identity": "40 + 36 + 45 = 121 = (k - 1)^2",
        "sector_double_count_identity": "3 + 2(15 + 20 + 24) = 121",
        "nonbacktracking_outdegree": "k - 1 = 11",
        "qutrit_hilbert_dimension_identity": "q^4 = C(q^2,2) + C(q^2+1,2) = 36 + 45 = 81",
        "representation_triangle_uniqueness": "(k-1)^2 = v + q^4 iff q = 3: gap = q(q-3)(q+1)",
        "common_singular_constant": "sqrt(18) = 3sqrt(2)",
        "sector_sharing_triangle": {
            "L_intersect_S": "1 + 15",
            "L_intersect_Q": "1 + 24",
            "S_intersect_Q": "1 + 20",
            "hidden_target_sector": 20,
        },
    }
    assert summary["parseval_chiral_exact_sequence"] == {
        "positive_chirality": "P_+ = L_15 + L_24 + S_20",
        "negative_chirality": "P_- = S_15 + Q_24 + Q_20",
        "harmonic_sector": "H = 1_L + 1_S + 1_Q",
        "nonzero_forward_blocks": ["S_15 -> L_15", "Q_24 -> L_24", "Q_20 -> S_20"],
        "exact_dimension_identity": "2(15 + 24 + 20) = 118",
        "total_dimension_identity": "121 = 59_+ + 59_- + 3_harm",
        "cohomology_statement": "the only cohomology is the three module means",
        "rank_Q": 59,
        "nullity_Q": 62,
    }
    assert summary["parseval_target_geometry"] == {
        "spread_target": {
            "frame_type": "ETF(36,15)",
            "sector_dimension": 15,
            "normalized_coherence": "1/5",
            "positive_sign_graph": {
                "vertices": 36,
                "degree": 15,
                "lambda": 6,
                "mu": 6,
                "edge_count": 270,
                "spectrum": {"-3": 20, "3": 15, "15": 1},
            },
            "negative_sign_graph": {
                "vertices": 36,
                "degree": 20,
                "lambda": 10,
                "mu": 12,
                "edge_count": 360,
                "spectrum": {"-4": 15, "2": 20, "20": 1},
            },
        },
        "anti_line_target": {
            "frame_type": "doubled two-distance tight frame(45,24)",
            "duplicate_class_count": 45,
            "sector_dimension": 24,
            "positive_sign_graph": {
                "vertices": 45,
                "degree": 32,
                "lambda": 22,
                "mu": 24,
                "edge_count": 720,
                "spectrum": {"-4": 20, "2": 24, "32": 1},
            },
            "negative_sign_graph": {
                "vertices": 45,
                "degree": 12,
                "lambda": 3,
                "mu": 3,
                "edge_count": 270,
                "spectrum": {"-3": 24, "3": 20, "12": 1},
            },
            "positive_sign_isomorphic_to_transport_graph": True,
            "canonical_transport_carrier": {
                "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                "duplicate_pairing_equals_center_quad_antipodes": True,
                "duplicate_classes_equal_quotient_point_quad_pairs": True,
                "paired_supports_equal_quotient_point_supports": True,
                "quotient_line_count": 27,
                "support_partitions_equal_quotient_lines": True,
                "line_size_distribution": {5: 27},
                "point_line_incidence_distribution": {3: 45},
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "positive_sign_equals_transport_graph_without_relabeling": True,
                "negative_sign_equals_quotient_point_graph_without_relabeling": True,
            },
        },
        "common_naimark_shadow": {
            "shared_shadow_dimension": 21,
            "shared_shadow_split": "1 + 20",
            "spread_shadow_frame_type": "ETF(36,21)",
            "spread_shadow_coherence": "1/7",
            "anti_line_shadow_normalized_off_diagonal": ["-1/14", "2/7"],
            "naimark_complement_swaps_sign_graphs": True,
        },
    }
    assert summary["two_spectral_shells"] == {
        "light_shell_rank": 78,
        "heavy_shell_rank": 40,
        "harmonic_dimension": 3,
        "total_dimension": 121,
        "shell_scale_ratio": 2.0,
        "parseval_identity_holds": True,
    }
    assert summary["mass_weighted_hodge_factorization"] == {
        "rank_d": 59,
        "nullity_d": 62,
        "harmonic_part": 3,
        "forward_block_count": 3,
        "forward_blocks": ["S_15 -> L_15", "Q_24 -> L_24", "Q_20 -> S_20"],
        "shell_values": [18, 18, 72],
        "three_exact_two_term_complexes_plus_three_harmonic": True,
        "shell_hierarchy_inside_differential": True,
        "massive_hodge_laplacian_spectrum": True,
    }
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
    assert summary["finite_ordered_path_carrier"] == {
        "path_count": 4320,
        "seed_stabilizer_size": 6,
        "completion_fibre_size": 3,
        "seed_completion_action_size": 6,
    }
    assert summary["quadrangle_exact_cover_model"] == {
        "ordered_path_count": 4320,
        "nonlocal_quadrangle_count": 1620,
        "target_cover_size": 540,
        "found_exact_cover": False,
        "visited_search_nodes": 1106,
    }
    assert summary["shared_finite_to_continuum_transport_shadow"] == {
        "reduced_group_order": 6,
        "unique_invariant_projective_line": [1, 2],
        "invariant_complement_count": 0,
        "is_nonsplit_extension_of_sign_by_trivial": True,
        "fiber_nilpotent_increment": [[0, 1], [0, 0]],
        "matter_extension_dimensions": [81, 162, 81],
        "matter_extension_rank": 81,
    }
    assert summary["current_zero_witness_point"] == {
        "C": "0",
        "L": "0",
        "Q_seed": "0",
        "Q_sd1": "0",
    }
    assert summary["exact_witness_point"] == {
        "C": "14105",
        "L": "143654",
        "Q_seed": "3396050/3",
        "Q_sd1": "3904481/4",
    }
    assert summary["affine_witness_displacement"] == summary["exact_witness_point"]
    assert summary["affine_displacement_recovered_scales"] == {
        "C": "217/12",
        "L": "217/12",
        "Q_seed": "217/12",
        "Q_sd1": "217/12",
    }
    assert all(summary["exact_factorizations"].values())


def test_q3_master_lock_analysis_keeps_the_boundary_honest() -> None:
    records = {record["name"]: record for record in classify_q3_master_lock()}
    summary = analyze()
    theorem = summary["q3_master_lock_theorem"]

    assert records["q3_local_qutrit_kernel_lock"]["support_level"] == "repo-exact finite kernel"
    assert "ETF(36,15)" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "121 = (k-1)^2" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "36 = 1 + 15 + 20" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "45 = 1 + 24 + 20" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "same canonical 45-point transport carrier" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "full 27-line dual GQ(4,2) incidence" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "27 five-cliques of the negative sign graph" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "21 = 1 + 20" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "121 = 59_+ + 59_- + 3_harm" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "S_15 -> L_15" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "Q_24 -> L_24" in records["q3_local_qutrit_kernel_lock"]["statement"]
    assert "Q_20 -> S_20" in records["q3_local_qutrit_kernel_lock"]["statement"]
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
    assert theorem["the_local_kernel_already_contains_the_exact_line_module_parseval_frame"] is True
    assert theorem["the_local_kernel_already_contains_the_exact_121_representation_triangle"] is True
    assert theorem["the_local_kernel_already_contains_the_exact_chiral_exact_sequence"] is True
    assert theorem[
        "the_local_kernel_already_contains_the_exact_target_side_parseval_geometry_and_naimark_shadow"
    ] is True
    assert theorem["the_corrected_spectral_core_exactly_realizes_the_q3_lock"] is True
    assert theorem["the_continuum_seed_exactly_realizes_the_q3_packet_8_56_320_2240_12480"] is True
    assert theorem["the_electron_seed_packet_exactly_splices_into_the_same_q3_backbone"] is True
    assert theorem["the_q3_lock_is_now_overdetermined_across_local_spectral_and_continuum_seed_layers"] is True
    assert theorem["the_q3_lock_is_now_overdetermined_across_local_spectral_continuum_and_electron_seed_layers"] is True
    assert theorem["the_transport_algebra_exactly_reduces_the_smooth_realization_wall_to_one_unipotent_sign_trivial_witness"] is True
    assert theorem["the_finite_h4_frontier_already_exhibits_the_same_transport_shadow_as_the_k3_witness"] is True
    assert theorem["the_missing_finite_selector_is_not_a_bare_540_quadrangle_exact_cover"] is True
    assert theorem["the_transport_algebra_exactly_refines_the_same_wall_to_one_nonzero_nilpotent_increment"] is True
    assert theorem["the_remaining_wall_refines_to_the_first_sign_trivial_unipotent_transport_witness"] is True
    assert theorem["the_remaining_wall_refines_equivalently_to_the_first_nonzero_nilpotent_holonomy_increment"] is True
    assert theorem["the_next_exact_positive_target_is_the_unique_minimal_tail_datum_in_the_existing_slot"] is True
    assert theorem["the_remaining_wall_refines_further_to_any_one_promoted_coordinate_witness_equivalently_dC_equals_14105"] is True
    assert theorem["the_live_positive_target_can_be_stated_as_one_exact_affine_witness_displacement_from_the_current_zero_candidate"] is True
    assert theorem["the_live_positive_target_is_the_same_ordered_path_transport_law_written_on_the_fixed_k3_chart"] is True
    assert theorem["the_remaining_wall_is_not_finite_q_selection_but_smooth_realization"] is True
    assert "ordered nonlocal 2-path S3 packet" in summary["boundary_note"]
    assert "540-packet model has no exact cover" in summary["boundary_note"]
    assert "non-identity unipotent sign-trivial transport witness" in summary["boundary_note"]
    assert "nonzero nilpotent holonomy increment" in summary["boundary_note"]
    assert "217/12" in summary["boundary_note"]
    assert "dC = 14105" in summary["boundary_note"]
    assert "(14105,143654,3396050/3,3904481/4)" in summary["boundary_note"]
