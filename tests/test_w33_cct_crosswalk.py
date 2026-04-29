"""Checked crosswalk between Cycle Clock Theory terms and W(3,3)."""

from pathlib import Path
import pytest

from scripts.w33_cct_crosswalk import (
    BACKBONE_INVARIANT_REGISTRY,
    CHECKED_PERIODIC_ROWS,
    E,
    E8_WEYL_ORDER,
    K,
    MU,
    ORGANIZATION_LAYER_ORDER,
    Q,
    a2_prime_power_hexagon_count,
    build_cct_crosswalk,
    cct_chapter2_trit_economy_summary,
    cct_chapter3_mathematical_foundations_summary,
    cct_chapter4_quasicrystal_fig_summary,
    cct_chapter5_shelling_scaling_summary,
    cct_chapter6_nonlocal_life_summary,
    cct_chapter7_loop_zeta_equilibrium_summary,
    cct_chapter8_chiral_mass_sector_summary,
    cct_chapter9_yukawa_mass_generation_summary,
    cct_chapter10_transport_holonomy_summary,
    cct_chapter11_gauge_flavor_frontier_summary,
    cct_chapter12_realization_theorem_summary,
    divisor_power_sum,
    e8_h4_projection_summary,
    full_symmetry_no_go_summary,
    projective_qutrit_phase_space_counts,
    q_factorial_equals_two_q_only_at_three,
    w33_clock_language_summary,
)


DOC_NOTE = Path("docs/W33_PERIODIC_TABLE_ORGANIZATION.md")
PAPER_TEX = Path("w33_paper.tex")


class TestCCT1FiniteCodeLanguage:
    def test_q_factorial_selector_is_three(self):
        assert q_factorial_equals_two_q_only_at_three() == [3]

    def test_projective_two_qutrit_symbol_count(self):
        counts = projective_qutrit_phase_space_counts()
        assert counts["affine_vectors"] == Q**MU == 81
        assert counts["nonzero_vectors"] == 80
        assert counts["nonzero_scalars"] == Q - 1 == 2
        assert counts["projective_points"] == 40
        assert counts["projective_points"] == counts["w33_vertices"]

    def test_code_language_has_three_cct_parts(self):
        summary = w33_clock_language_summary()
        assert set(summary) == {"symbols", "relational_rules", "syntactical_freedom"}


class TestCCT2RelationalRules:
    def test_srg_master_equation(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert rules["srg_parameters"] == (40, 12, 2, 4)
        assert rules["master_equation_left"] == 108
        assert rules["master_equation_right"] == 108

    def test_edge_relation_count(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert rules["edge_relations"] == E == 240

    def test_symplectic_rule_is_ternary(self):
        rules = w33_clock_language_summary()["relational_rules"]
        assert "F_3" in rules["symplectic_commutation_rule"]


class TestCCTChapter2TritEconomy:
    def test_chapter2_trit_model_routes_to_q3_and_projective_collapse(self):
        summary = cct_chapter2_trit_economy_summary()

        assert summary["source_scope"]["chapter"] == 2
        assert summary["source_scope"]["chapter_title"] == (
            "Trits, the Irreducible Computational Element of Thought"
        )
        assert summary["trit_model"] == {
            "off_state": "empty set / no point",
            "on_state": "singleton point / activated point",
            "undecided_state": "unresolved empty-or-singleton state",
            "state_count": 3,
            "maintain_unresolved_cost": 1,
            "resolve_choice_cost": 2,
            "extra_resolution_cost": 1,
        }

        certificate = summary["w33_qutrit_certificate"]
        assert certificate["q_selector"] == Q == 3
        assert certificate["q_factorial_equals_two_q_hits"] == [3]
        assert certificate["two_qutrit_exponent_vectors"] == 81
        assert certificate["zero_vector"] == 1
        assert certificate["nonzero_exponent_vectors"] == 80
        assert certificate["projective_scalar_orbit_size"] == 2
        assert certificate["projective_symbols"] == 40

    def test_chapter2_sparse_symbolic_economy_is_checked_by_w33(self):
        summary = cct_chapter2_trit_economy_summary()
        sparse = summary["sparse_point_economy"]

        assert sparse["complete_pair_count_on_40_symbols"] == 780
        assert sparse["active_commutation_edges"] == E == 240
        assert sparse["inactive_pairs"] == 540
        assert sparse["edge_density"] == "4/13"
        assert sparse["line_clock_states"] == 120
        assert sparse["cycle_rank"] == 201
        assert sparse["nonneighbors_per_symbol"] == 27
        assert sparse["adjacent_shared_neighbors"] == 2
        assert sparse["nonadjacent_shared_neighbors"] == 4
        assert sparse["srg_overlap_balance"] == 108

        root_bridge = summary["e8_sparse_root_bridge"]
        assert root_bridge["w33_edges"] == 240
        assert root_bridge["e8_root_vectors"] == 240
        assert root_bridge["e8_weyl_order"] == E8_WEYL_ORDER == 696_729_600
        assert root_bridge["w33_edges_match_e8_roots"] is True

    def test_chapter2_theorem(self):
        summary = cct_chapter2_trit_economy_summary()
        assert all(summary["theorem"].values())


class TestCCTChapter3MathematicalFoundations:
    def test_chapter3_root_chain_routes_cayley_integer_e8_claim(self):
        summary = cct_chapter3_mathematical_foundations_summary()

        assert summary["source_scope"]["chapter"] == 3
        assert summary["source_scope"]["chapter_title"] == (
            "The Mathematical Foundations of Cycle Clock Theory"
        )

        chain = summary["division_algebra_root_chain"]
        assert chain["dimensions"] == (1, 2, 4, 8)
        assert chain["root_systems"] == ("A1", "A2", "D4", "E8")
        assert chain["root_counts"] == {
            "A1": 2,
            "A2": 6,
            "D4": 24,
            "E8": 240,
        }
        assert chain["orientation_composition"] == {
            "A1_to_A2_orientation_classes": 3,
            "A2_to_D4_orientation_classes": 4,
            "D4_to_E8_orientation_classes": 10,
            "D4_24_cell_root_count": 24,
            "E8_roots_from_ten_D4_24_cells": 240,
            "E8_perpendicular_24_cell_pairs": 5,
        }

    def test_chapter3_cyclic_packet_and_line_clock_cover_are_exact(self):
        summary = cct_chapter3_mathematical_foundations_summary()

        assert summary["cyclic_permutation_packet"] == {
            "A2_three_orientation_cycle": 3,
            "D4_four_class_cyclic_permutations": 6,
            "D4_reverse_pairs": 3,
            "E8_five_24_cell_subset_size": 5,
            "E8_cyclic_permutations_per_subset": 24,
            "E8_reverse_pairs_per_subset": 12,
            "E8_reverse_pairs_across_two_subsets": 24,
            "E8_cyclic_permutations_across_two_subsets": 48,
            "C5_times_C5_times_C2_order": 50,
        }
        assert summary["w33_cycle_clock_packet"] == {
            "line_carriers": 40,
            "trit_steps_per_line": 3,
            "line_clock_states": 120,
            "line_clock_edge_cover": 240,
            "cycle_rank": 201,
            "directed_hashimoto_states": 480,
            "non_backtracking_branch_count": 11,
            "first_self_consistency_loop_length": 3,
            "first_self_consistency_loop_probability": "2/1331",
        }

    def test_chapter3_clifford_hopf_and_least_change_packets_are_checked(self):
        summary = cct_chapter3_mathematical_foundations_summary()

        assert summary["clifford_hopf_sparse_shadow"] == {
            "coarse_sphere_sequence": ("S0", "S1", "S3", "S7"),
            "coarse_root_counts": (2, 6, 24, 240),
            "clifford_process_group_order": 51_840,
            "h4_internal_matching_states": 120,
            "shared_coxeter_number": 30,
            "e8_dimension": 248,
        }
        assert summary["least_change_packet"] == {
            "projective_symbol_collapse": "81 -> 40",
            "complete_pair_count_on_40_symbols": 780,
            "active_commutation_edges": 240,
            "inactive_pairs": 540,
            "sparse_edge_density": "4/13",
            "srg_overlap_balance": 108,
        }
        assert all(summary["theorem"].values())


class TestCCTChapter4QuasicrystalFIG:
    def test_chapter4_hopf_es_packet_routes_to_e8_and_h4_counts(self):
        summary = cct_chapter4_quasicrystal_fig_summary()

        assert summary["source_scope"]["chapter"] == 4
        assert summary["source_scope"]["chapter_title"] == (
            "Quasicrystal Primer and the FIG: A 3D Conformal Shadow of E8"
        )

        hopf = summary["elser_sloane_hopf_packet"]
        assert hopf == {
            "e8_root_vectors": 240,
            "hopf_fiber_count": 10,
            "roots_per_24_cell_fiber": 24,
            "orthoplex_vertices_in_base_S4": 10,
            "orthoplex_axes": 5,
            "symmetric_diagonal_directions": 32,
            "A_fibers": 5,
            "B_fibers": 5,
            "orthogonal_Ai_Bi_pairs": 5,
            "projected_600_cell_vertices_from_A_shell": 120,
            "projected_600_cell_vertices_from_B_shell": 120,
            "two_projected_600_cell_shells": 2,
            "total_projected_shell_vertices": 240,
            "isoclinic_cycle_length": 5,
            "isoclinic_rotation_angle": "2*pi/5",
            "fibonacci_angle_relation": "tan(theta_B)=1/phi",
        }

    def test_chapter4_fig_and_c5c_counts_are_source_scoped(self):
        summary = cct_chapter4_quasicrystal_fig_summary()

        fig = summary["fibonacci_fig_source_packet"]
        assert fig["golden_spacing_model"] == "palindromic Fibonacci multigrid"
        assert fig["pentagrid_normal_count"] == 5
        assert fig["icosagrid_normal_count"] == 10
        assert fig["tetragrid_normal_count"] == 4
        assert fig["tetragrid_sets_inside_icosagrid"] == 5
        assert fig["tetrahedra_per_4G"] == 4
        assert fig["tetrahedra_per_20G"] == 20
        assert fig["central_20G_tetrahedral_vertices"] == 61
        assert fig["plane_classes_before_golden_twist"] == 70
        assert fig["plane_classes_after_golden_twist"] == 10
        assert "source claim" in fig["source_level_subset_claim"]

        c5c = summary["cuboctahedral_c5c_packet"]
        assert c5c == {
            "twenty_four_cells_in_compound": 5,
            "cuboctahedral_equators_per_24_cell": 12,
            "initial_cuboctahedron_choices": 60,
            "left_isoclinic_limit_images": 1,
            "right_isoclinic_limit_images": 5,
            "C5C_members": 5,
            "tetrahedra_per_4G": 4,
            "4G_compounds_per_20G": 5,
            "tetrahedra_per_20G": 20,
            "handed_20G_options": 2,
        }

    def test_chapter4_w33_h4_certificate_preserves_frontier_boundary(self):
        summary = cct_chapter4_quasicrystal_fig_summary()
        certificate = summary["w33_h4_certificate"]

        assert certificate["w33_edge_root_shell"] == E == 240
        assert certificate["h4_roots_600_cell_vertices"] == 120
        assert certificate["two_h4_shells_recover_e8_root_shell"] == 240
        assert certificate["line_clock_states"] == 120
        assert certificate["coxeter_number"] == 30
        assert certificate["h4_degrees"] == (2, 12, 20, 30)
        assert certificate["h4_degrees_embed_in_e8"] is True
        assert certificate["full_psp43_orbital_degrees"] == (2, 27, 36, 54)
        assert certificate["full_symmetry_can_make_600_cell_graph"] is False
        assert certificate["required_selector"] == "golden/icosahedral H4 projection data"
        assert "frontier data" in certificate["frontier_status"]
        assert all(summary["theorem"].values())


class TestCCTChapter5ShellingScaling:
    def test_divisor_and_a2_prime_power_helpers(self):
        assert divisor_power_sum(1, 3) == 1
        assert divisor_power_sum(Q, 3) == 28
        assert divisor_power_sum(Q, 1, odd_only=True) == 4
        assert divisor_power_sum(2, 1, odd_only=True) == 1

        assert [a2_prime_power_hexagon_count(Q, a) for a in range(4)] == [1, 1, 1, 1]
        assert a2_prime_power_hexagon_count(7, 2) == 3
        assert a2_prime_power_hexagon_count(2, 1) == 0
        assert a2_prime_power_hexagon_count(2, 2) == 1

    def test_chapter5_base_shells_route_to_A2_D4_E8_sequence(self):
        summary = cct_chapter5_shelling_scaling_summary()

        assert summary["source_scope"]["chapter"] == 5
        assert summary["source_scope"]["chapter_title"] == "Shelling and Scaling Lattices"

        objectives = summary["root_lattice_objectives_packet"]
        assert objectives["lattices"] == ("A2", "D4", "E8")
        assert objectives["ambient_dimensions"] == (2, 4, 8)
        assert objectives["base_shell_multiplicities"] == (6, 24, 240)
        assert objectives["comparison_irregular_lattices"] == ("A4", "A6", "A8")
        assert objectives["quasilattice_extension"] == "E8 projection / Sadoc-Mosseri shelling"

    def test_chapter5_A2_D4_E8_shelling_packets_are_exact(self):
        summary = cct_chapter5_shelling_scaling_summary()

        assert summary["a2_shelling_packet"] == {
            "root_count": 6,
            "normalized_hexagons_at_unit_shell": 1,
            "q_adic_prime": 3,
            "N_prime_of_q_power_for_exponents_0_to_3": {0: 1, 1: 1, 2: 1, 3: 1},
            "prime_1_mod_3_example": {
                "prime": 7,
                "exponent": 2,
                "N_prime": 3,
            },
            "prime_2_mod_3_examples": {
                "p2_odd_exponent": 0,
                "p2_even_exponent": 1,
            },
            "w33_selector_match": True,
        }

        assert summary["d4_shelling_packet"] == {
            "root_count": 24,
            "K_n_4_formula": "24 * sum_{d|n, d odd} d",
            "K_1_4": 24,
            "K_2_4": 24,
            "K_q_4": 96,
            "odd_divisor_sum_at_q": 4,
            "w33_24_cell_packet": True,
        }

        assert summary["e8_shelling_packet"] == {
            "root_count": 240,
            "K_n_8_formula": "240 * sum_{d|n} d^3",
            "K_1_8": 240,
            "K_2_8": 2160,
            "K_q_8": 6720,
            "sigma3_at_q": 28,
            "q_shell_amplifier": 28,
            "amplifier_matches_v_minus_k": True,
            "w33_edge_root_shell": 240,
            "w33_edge_shell_matches_e8_unit_shell": True,
        }

    def test_chapter5_scaling_and_omega_team_boundary(self):
        summary = cct_chapter5_shelling_scaling_summary()

        assert summary["scaling_comparison_packet"] == {
            "sphere_sequence": ("S1", "S3", "S7"),
            "K_1_d": {2: 6, 4: 24, 8: 240},
            "seed_counts_after_dividing_by_K_1_d": {2: 1, 4: 1, 8: 1},
            "chapter5_normalized_seed_name": "Sigma(n,d)",
            "w33_line_clock_uses_five_24_cell_packets": 5,
            "w33_e8_shell_uses_ten_24_cell_packets": 10,
        }
        assert "source guidance only" in summary["omega_team_source_packet"]["local_status"]
        assert all(summary["theorem"].values())


class TestCCTChapter6NonlocalLife:
    def test_chapter6_penrose_game_source_packet_has_finite_neighbor_skeleton(self):
        summary = cct_chapter6_nonlocal_life_summary()

        assert summary["source_scope"]["chapter"] == 6
        assert summary["source_scope"]["chapter_title"] == (
            "Non-local game of life in quasicrystals - first attempt of a cycle clock model"
        )
        assert summary["penrose_game_source_packet"] == {
            "mother_lattice": "Z5",
            "quasicrystal_dimension": 2,
            "penrose_vertex_types": 8,
            "chosen_dominant_vertex_type": "K",
            "local_clusters_are_tiles_sharing_one_vertex": True,
            "ideal_K_neighbors": 8,
            "clockwise_neighbor_labels": (1, 2, 3, 4),
            "counterclockwise_neighbor_labels": (5, 6, 7, 8),
            "two_pentagons_in_perpendicular_space": True,
            "living_vertex_type_may_not_stay_fixed": True,
        }

        assert summary["least_change_rule_packet"] == {
            "candidate_next_steps": 8,
            "self_position_excluded": True,
            "overlap_score": "|E0 intersect Ei|",
            "preferred_move": "argmax_i |E0 intersect Ei|",
            "tie_rule": "random choice among maximizing neighbors",
            "trit_measure": "number of cut-window shifts / changed tiles",
            "status": (
                "finite rule skeleton only; no W(3,3) theorem is asserted for "
                "the simulated Penrose trajectories."
            ),
        }

    def test_chapter6_d4_cycle_and_fig_packets_reuse_exact_counts(self):
        summary = cct_chapter6_nonlocal_life_summary()

        assert summary["d4_copy_cycle_packet"] == {
            "Z5_parallel_D4_copies": 10,
            "projected_K_vertex_types": 10,
            "roots_per_D4_copy": 24,
            "total_D4_copy_states": 240,
            "matches_W33_E8_edge_shell": True,
            "chapter5_scaling_source": "240 = 10 x 24",
        }

        assert summary["fig_3d_source_packet"] == {
            "carrier_elements": ("20G", "4G"),
            "tetrahedra_per_4G": 4,
            "tetrahedra_per_20G": 20,
            "compounded_4G_count_per_20G": 5,
            "higher_dimensional_mother_lattice": "E8",
            "CE_selection_for_probability_runs": "4G",
            "integrated_step_window_examples": (5, 10, 15, 20, 25, 30),
            "source_run_range": (30, 1000),
            "source_particle_range": (1, 10),
            "status": (
                "3D FIG empire rays and trajectory probabilities are recorded "
                "as source dynamics, not as an exact W(3,3) probability law."
            ),
        }

    def test_chapter6_w33_certificate_keeps_empire_dynamics_frontier_scoped(self):
        summary = cct_chapter6_nonlocal_life_summary()
        certificate = summary["w33_cycle_clock_certificate"]

        assert certificate["neighbor_options_match_e8_rank"] is True
        assert certificate["clockwise_counterclockwise_split"] == (4, 4)
        assert certificate["split_matches_mu_plus_mu"] is True
        assert certificate["ten_D4_packets_recover_edge_shell"] == E == 240
        assert certificate["twenty_group_from_five_4G"] == (5, 4, 20)
        assert "frontier/source behavior" in certificate["frontier_boundary"]
        assert all(summary["theorem"].values())


class TestCCT3ClockAndProjection:
    def test_line_clock_states_are_h4_sized(self):
        clock = w33_clock_language_summary()["syntactical_freedom"]
        assert clock["line_count"] == 40
        assert clock["matchings_per_line"] == Q == 3
        assert clock["line_clock_states"] == 120
        assert clock["line_clock_edge_cover"] == E

    def test_cycle_rank_is_finite_feedback_budget(self):
        clock = w33_clock_language_summary()["syntactical_freedom"]
        assert clock["cycle_rank"] == E - 40 + 1 == 201

    def test_e8_h4_arithmetic(self):
        projection = e8_h4_projection_summary()
        assert projection["w33_edges"] == projection["e8_roots"] == 240
        assert projection["h4_roots"] == 120
        assert projection["e8_dimension"] == 248
        assert projection["coxeter_number"] == 30
        assert projection["h4_degrees_embed_in_e8"] is True


class TestCCT4H4Selector:
    def test_full_symmetry_no_go_demands_selector(self):
        no_go = full_symmetry_no_go_summary()
        assert no_go["m120_states"] == 120
        assert no_go["six_hundred_cell_degree"] == K == 12
        assert no_go["full_psp43_orbital_degrees"] == (2, 27, 36, 54)
        assert no_go["full_symmetry_can_make_600_cell_graph"] is False
        assert "golden" in no_go["required_selector"]

    def test_crosswalk_rows_cover_cct_source_concepts(self):
        crosswalk = build_cct_crosswalk()
        desiderata = {row["cct_desideratum"] for row in crosswalk["crosswalk_rows"]}
        assert desiderata == {
            "finite code/language",
            "principle of efficient language",
            "trit savings",
            "Clifford/root-system process objects",
            "E8 to H4 quasicrystal pathway",
            "feedback loop / cycle-clock dynamics",
            "measurement / shadow duality",
            "finite propagator / operator calculus",
            "mass-weighted Hodge factorization",
            "non-arbitrary H4 emergence",
        }

    def test_crosswalk_rows_now_carry_five_layer_routes_and_checked_row_tags(self):
        crosswalk = build_cct_crosswalk()

        assert crosswalk["layer_order"] == ORGANIZATION_LAYER_ORDER
        assert crosswalk["checked_periodic_rows"] == CHECKED_PERIODIC_ROWS
        assert crosswalk["backbone_invariant_registry"] == BACKBONE_INVARIANT_REGISTRY
        assert crosswalk["aligned_periodic_rows_used"] == [
            "exceptional_envelope_row",
            "frontier_witness_row",
            "pascal_computation_row",
        ]
        assert crosswalk["same_table_backbone_invariants_used"] == [
            "240_edge_root_shell",
            "40_point_shell",
            "81_seed",
            "q3_selector",
        ]

        for row in crosswalk["crosswalk_rows"]:
            route = row["five_layer_route"]
        assert tuple(route) == ORGANIZATION_LAYER_ORDER
        assert all(route[layer] for layer in ORGANIZATION_LAYER_ORDER)
        assert row["aligned_periodic_rows"]
        assert all(name in CHECKED_PERIODIC_ROWS for name in row["aligned_periodic_rows"])
        assert row["same_table_backbone_invariants"]
        assert all(
                name in BACKBONE_INVARIANT_REGISTRY for name in row["same_table_backbone_invariants"]
            )

        language_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "finite code/language"
        )
        assert language_row["aligned_periodic_rows"] == ["exceptional_envelope_row"]
        assert language_row["same_table_backbone_invariants"] == ["40_point_shell"]
        assert language_row["five_layer_route"] == {
            "carrier": "projective two-qutrit/W(3,3) finite symbol shell",
            "realization": "F_3^4 projective Pauli symbols modulo nonzero scalars",
            "algebra": "ternary symplectic commutation law",
            "computation": "projectivize the two-qutrit exponent space to the 40-symbol shell",
            "witness": "40 projective symbols",
        }

        trit_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "trit savings"
        )
        assert trit_row["same_table_backbone_invariants"] == ["81_seed", "40_point_shell"]

        measurement_row = next(
            row
            for row in crosswalk["crosswalk_rows"]
            if row["cct_desideratum"] == "measurement / shadow duality"
        )
        assert measurement_row["aligned_periodic_rows"] == ["pascal_computation_row"]
        assert measurement_row["same_table_backbone_invariants"] == [
            "40_point_shell",
            "240_edge_root_shell",
        ]
        assert measurement_row["five_layer_route"] == {
            "carrier": "the centered 40-point line module, its Pascal target channels, the induced 59 + 59 + 3 chiral split, and the raw 18/72 two-shell triangle operator",
            "realization": "the 121 = (k-1)^2 representation triangle with 36 spread features, a 45-point anti-line quotient carrier whose 27 lines are the five-cliques of the negative sign graph, the chiral identity 121 = 59_+ + 59_- + 3_harm, and the raw shell split 0^3, 18^78, 72^40",
            "algebra": "Parseval/Naimark target-side sign algebra, the sector-sharing 40/36/45 triangle, the exact chiral block sum S_15 -> L_15, Q_24 -> L_24, Q_20 -> S_20, and the massive Laplacian relation Delta_H = d d* + d* d = 18 P_light + 72 P_heavy",
            "computation": "center the spread and anti-line probes, isolate the 15-, 24-, and shared 20-sectors, identify duplicate anti-lines with the center-quad quotient carrier, recover the 27 negative-sign five-cliques, pass to the Naimark complement, expose the three exact forward blocks, and verify shell ratio sqrt(72)/sqrt(18)=2 with rank(d)=59 and nullity(d)=62",
            "witness": "ETF(36,15), the 121 = (k-1)^2 representation triangle, the 59_+ + 59_- + 3_harm chiral exact sequence, the canonical 45-point transport carrier with 27 negative-sign five-cliques, the shared shadow 21 = 1 + 20, and the two-shell/mass-weighted Hodge spectrum 0^3, 18^78, 72^40",
        }

        propagator_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "finite propagator / operator calculus"
        )
        assert propagator_row["integer_certificate"] == 78
        assert propagator_row["aligned_periodic_rows"] == ["pascal_computation_row"]
        assert "40_point_shell" in propagator_row["same_table_backbone_invariants"]
        assert "P0, P_light, P_heavy" in propagator_row["w33_witness"]
        assert "ranks 3" in propagator_row["w33_witness"]
        assert "Green kernel" in propagator_row["w33_witness"]

        no_go_row = next(
            row for row in crosswalk["crosswalk_rows"] if row["cct_desideratum"] == "non-arbitrary H4 emergence"
        )
        assert no_go_row["aligned_periodic_rows"] == [
            "frontier_witness_row",
            "exceptional_envelope_row",
        ]
        assert no_go_row["same_table_backbone_invariants"] == ["240_edge_root_shell"]
        assert "12 is absent" in no_go_row["five_layer_route"]["witness"]

    def test_crosswalk_theorem(self):
        crosswalk = build_cct_crosswalk()
        assert crosswalk["theorem"]["w33_realizes_cct_finite_language_template"]
        assert crosswalk["theorem"]["every_crosswalk_row_has_a_full_five_layer_route"]
        assert crosswalk["theorem"]["crosswalk_rows_route_only_to_checked_periodic_rows"]
        assert crosswalk["theorem"]["crosswalk_terms_are_forced_onto_exact_carriers_and_witnesses"]
        assert crosswalk["theorem"]["the_pascal_row_now_routes_the_target_side_measurement_shadow_dictionary"]
        assert crosswalk["theorem"]["crosswalk_rows_name_the_same_table_backbone_invariants_they_use"]
        assert crosswalk["theorem"]["the_source_dictionary_explicitly_uses_the_shared_40_81_240_backbone"]
        assert crosswalk["theorem"]["chapter2_trit_economy_is_routed_to_exact_w33_certificates"]
        assert crosswalk["theorem"]["chapter3_foundations_are_routed_to_exact_w33_certificates"]
        assert crosswalk["theorem"]["chapter4_quasicrystal_fig_layer_is_routed_to_exact_w33_certificates"]
        assert crosswalk["theorem"]["chapter5_shelling_scaling_layer_is_routed_to_exact_w33_certificates"]
        assert crosswalk["theorem"]["chapter6_nonlocal_life_layer_is_routed_to_exact_w33_certificates"]
        assert "carrier -> realization -> algebra -> computation -> witness" in crosswalk["theorem"]["interpretation"]
        assert "shared q=3 backbone invariant" in crosswalk["theorem"]["interpretation"]
        assert "121 = (k-1)^2 representation triangle" in crosswalk["theorem"]["interpretation"]
        assert "59_+ + 59_- + 3_harm chiral exact sequence" in crosswalk["theorem"]["interpretation"]
        assert "45-point transport carrier" in crosswalk["theorem"]["interpretation"]
        assert "negative-sign five-cliques" in crosswalk["theorem"]["interpretation"]
        assert "two-shell and mass-weighted-Hodge package 0^3, 18^78, 72^40" in crosswalk["theorem"]["interpretation"]
        assert "projector calculus" in crosswalk["theorem"]["interpretation"]
        assert "H4/quasicrystal step" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 2 trit-economy layer" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 3 mathematical foundations layer" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 4 FIG/quasicrystal layer" in crosswalk["theorem"]["interpretation"]
        assert "H4/600-cell packet 5 x 24 = 120" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 5 shelling/scaling layer" in crosswalk["theorem"]["interpretation"]
        assert "q=3 E8 shell count 240 x sigma_3(3) = 6720" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 6 non-local game-of-life layer" in crosswalk["theorem"]["interpretation"]
        assert "ten D4/K-VT packets giving 10 x 24 = 240" in crosswalk["theorem"]["interpretation"]

    def test_crosswalk_interpretation_covers_chapters_7_through_12(self):
        crosswalk = build_cct_crosswalk()

        assert "Chapter 7 routes" in crosswalk["theorem"]["interpretation"]
        assert "480 directed edges" in crosswalk["theorem"]["interpretation"]
        assert "Ramanujan" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 8 routes" in crosswalk["theorem"]["interpretation"]
        assert "121 = 59_+ + 59_- + 3_harm" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 9 routes" in crosswalk["theorem"]["interpretation"]
        assert "coherence-law" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 10 routes" in crosswalk["theorem"]["interpretation"]
        assert "dC = 14105" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 11 routes" in crosswalk["theorem"]["interpretation"]
        assert "E6/CKM bridge" in crosswalk["theorem"]["interpretation"]
        assert "27-line dual GQ(4,2) graph" in crosswalk["theorem"]["interpretation"]
        assert "45 cubic-support triangles" in crosswalk["theorem"]["interpretation"]
        assert "C ~ 3.55e-6" in crosswalk["theorem"]["interpretation"]
        assert "affine-in-epsilon^2 normal form" in crosswalk["theorem"]["interpretation"]
        assert "Chapter 12 states the boundary-explicit CCT closure" in crosswalk["theorem"]["interpretation"]
        assert "11 repo-exact" in crosswalk["theorem"]["interpretation"]

    def test_crosswalk_has_a_chapter2_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][2]

        assert chapter["source_title"] == "Trits, the Irreducible Computational Element of Thought"
        assert "q=3 selector" in chapter["primary_connection"]
        assert "81 -> 40" in chapter["primary_connection"]
        assert "240 edge/root shell" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter3_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][3]

        assert chapter["source_title"] == "The Mathematical Foundations of Cycle Clock Theory"
        assert "10 x 24 = 240" in chapter["primary_connection"]
        assert "120-state" in chapter["primary_connection"]
        assert "480-state Hashimoto" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter4_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][4]

        assert chapter["source_title"] == (
            "Quasicrystal Primer and the FIG: A 3D Conformal Shadow of E8"
        )
        assert "10 x 24 = 240" in chapter["primary_connection"]
        assert "5 x 24 = 120" in chapter["primary_connection"]
        assert "two-shell 240 recovery" in chapter["primary_connection"]
        assert "full-symmetry no-go" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter5_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][5]

        assert chapter["source_title"] == "Shelling and Scaling Lattices"
        assert "6/24/240" in chapter["primary_connection"]
        assert "240 x sigma_3(3) = 6720" in chapter["primary_connection"]
        assert "120 = 5 x 24" in chapter["primary_connection"]
        assert "240 = 10 x 24" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter6_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][6]

        assert chapter["source_title"] == (
            "Non-local game of life in quasicrystals - first attempt of a cycle clock model"
        )
        assert "eight K-neighbor moves" in chapter["primary_connection"]
        assert "4 + 4" in chapter["primary_connection"]
        assert "10 x 24 = 240" in chapter["primary_connection"]
        assert "5 x 4 = 20" in chapter["primary_connection"]
        assert "source dynamics" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_docs_and_paper_mention_the_cct_backbone_invariants_explicitly(self):
        doc_text = DOC_NOTE.read_text(encoding="utf-8")
        paper_text = PAPER_TEX.read_text(encoding="utf-8")

        assert "scripts/w33_cct_crosswalk.py" in doc_text
        assert "tests/test_w33_cct_crosswalk.py" in doc_text
        assert "the `40` shell, the `81` seed, or the `240`" in doc_text
        assert "edge/root shell" in doc_text

        assert "The executable crosswalk now enforces that rule row by row." in paper_text
        assert r"\texttt{scripts/w33\_cct\_crosswalk.py}" in paper_text
        assert r"\texttt{tests/test\_w33\_cct\_crosswalk.py}" in paper_text
        assert "the $40$ shell, the" in paper_text
        assert "the $240$ edge/root shell" in paper_text
        assert "$121$-dimensional representation triangle" in paper_text

    def test_crosswalk_has_a_chapter7_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][7]

        assert chapter["source_title"] == (
              "Transtemporal feedback and cycle-clock loop equilibrium"
        )
        assert "480 directed edges" in chapter["primary_connection"]
        assert "11 branches" in chapter["primary_connection"]
        assert "1/480" in chapter["primary_connection"]
        assert "Ramanujan" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter8_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][8]

        assert chapter["source_title"] == (
            "Chiral symmetry breaking and mass-sector emergence in the cycle clock"
        )
        assert "121 = 59_+ + 59_- + 3_harm" in chapter["primary_connection"]
        assert "18^78, 72^40" in chapter["primary_connection"]
        assert "shell ratio 2" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter9_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][9]

        assert chapter["source_title"] == (
            "Yukawa coupling, mass generation, and the coherence law"
        )
        assert "coherence law" in chapter["primary_connection"]
        assert "206" in chapter["primary_connection"]
        assert "3478" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter10_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][10]

        assert chapter["source_title"] == (
            "Transport algebra, holonomy witnesses, and the realization wall"
        )
        assert "217/12" in chapter["primary_connection"]
        assert "dC = 14105" in chapter["primary_connection"]
        assert "Jordan" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter11_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][11]

        assert chapter["source_title"] == (
            "Gauge symmetry, E6 structure, and the flavor/CP frontier"
        )
        assert "E6/CKM" in chapter["primary_connection"]
        assert "27-line/45-triangle cubic carrier" in chapter["primary_connection"]
        assert "identity CKM" in chapter["primary_connection"]
        assert "CP-breaking" in chapter["primary_connection"]
        assert "C ~ 3.55e-6" in chapter["primary_connection"]
        assert "affine-in-epsilon^2 normal form" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())

    def test_crosswalk_has_a_chapter12_certificate(self):
        chapter = build_cct_crosswalk()["chapter_crosswalks"][12]

        assert chapter["source_title"] == (
            "Smooth realization boundary: exact finite spine with frontier response"
        )
        assert "11 repo-exact" in chapter["primary_connection"]
        assert "boundary-explicit" in chapter["primary_connection"]
        assert "dC = 14105" in chapter["primary_connection"]
        assert all(chapter["certificate"]["theorem"].values())


class TestCCTChapter7LoopZetaEquilibrium:
    def test_chapter7_source_scope(self):
        ch = cct_chapter7_loop_zeta_equilibrium_summary()
        assert ch["source_scope"]["chapter"] == 7
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter7_directed_edge_packet(self):
        ch = cct_chapter7_loop_zeta_equilibrium_summary()
        pkt = ch["directed_edge_packet"]
        assert pkt["directed_edges"] == 480
        assert pkt["branch_count"] == 11
        assert pkt["matches_twice_edge_shell"] is True

    def test_chapter7_theorem_all_pass(self):
        ch = cct_chapter7_loop_zeta_equilibrium_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter7 theorem {key!r} not True"


class TestCCTChapter8ChiralMassSector:
    def test_chapter8_source_scope(self):
        ch = cct_chapter8_chiral_mass_sector_summary()
        assert ch["source_scope"]["chapter"] == 8
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter8_chiral_split(self):
        ch = cct_chapter8_chiral_mass_sector_summary()
        pkt = ch["chiral_sequence_packet"]
        assert pkt["plus_sector"] == 59
        assert pkt["minus_sector"] == 59
        assert pkt["harmonic_modes"] == 3
        assert pkt["sum_checks"] is True

    def test_chapter8_theorem_all_pass(self):
        ch = cct_chapter8_chiral_mass_sector_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter8 theorem {key!r} not True"


class TestCCTChapter9YukawaMassGeneration:
    def test_chapter9_source_scope(self):
        ch = cct_chapter9_yukawa_mass_generation_summary()
        assert ch["source_scope"]["chapter"] == 9
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter9_mass_hierarchy(self):
        ch = cct_chapter9_yukawa_mass_generation_summary()
        pkt = ch["mass_hierarchy_packet"]
        assert pkt["three_generation_count"] == 3
        assert pkt["muon_to_electron_ratio"] == pytest.approx(206, rel=0.01)
        assert pkt["tau_to_electron_ratio"] == pytest.approx(3478, rel=0.01)

    def test_chapter9_theorem_all_pass(self):
        ch = cct_chapter9_yukawa_mass_generation_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter9 theorem {key!r} not True"


class TestCCTChapter10TransportHolonomy:
    def test_chapter10_source_scope(self):
        ch = cct_chapter10_transport_holonomy_summary()
        assert ch["source_scope"]["chapter"] == 10
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter10_transport_packet(self):
        ch = cct_chapter10_transport_holonomy_summary()
        pkt = ch["affine_closure_packet"]
        assert pkt["affine_dc_target"] == 14105
        assert ch["holonomy_witness_packet"]["nilpotent_order"] == 2

    def test_chapter10_theorem_all_pass(self):
        ch = cct_chapter10_transport_holonomy_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter10 theorem {key!r} not True"


class TestCCTChapter11GaugeFlavorFrontier:
    def test_chapter11_source_scope(self):
        ch = cct_chapter11_gauge_flavor_frontier_summary()
        assert ch["source_scope"]["chapter"] == 11
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter11_ckm_bridge(self):
        ch = cct_chapter11_gauge_flavor_frontier_summary()
        pkt = ch["e6_ckm_bridge_packet"]
        assert pkt["aligned_vev_ckm_is_identity"] is True
        assert pkt["misaligned_vev_ckm_nontrivial"] is True
        cubic = ch["e6_cubic_carrier_packet"]
        assert cubic["line_count"] == 27
        assert cubic["triangle_count"] == 45
        assert cubic["each_line_lies_on_cubic_terms"] == 5
        cp = ch["spontaneous_cp_packet"]
        assert cp["cubic_coefficient_band"][0] > 3.3e-6
        assert cp["cubic_coefficient_band"][1] < 3.8e-6
        assert cp["cubic_coefficient_ratio_max_over_min"] < 1.12
        assert abs(cp["odd_cubic_affine_intercept"]) > 3.2e-6
        assert abs(cp["odd_cubic_affine_intercept"]) < 3.6e-6
        assert cp["odd_cubic_affine_relative_max_residual"] < 0.02
        assert "affine in epsilon^2" in cp["odd_cubic_normal_form_statement"]

    def test_chapter11_theorem_all_pass(self):
        ch = cct_chapter11_gauge_flavor_frontier_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter11 theorem {key!r} not True"


class TestCCTChapter12RealizationTheorem:
    def test_chapter12_source_scope(self):
        ch = cct_chapter12_realization_theorem_summary()
        assert ch["source_scope"]["chapter"] == 12
        assert ch["source_scope"]["book"] == "Cycle Clock Theory"

    def test_chapter12_master_lock_packet(self):
        ch = cct_chapter12_realization_theorem_summary()
        pkt = ch["realization_summary_packet"]
        assert pkt["q3_selector_exact"] is True
        assert pkt["transport_holonomy_exact"] is True

    def test_chapter12_theorem_all_pass(self):
        ch = cct_chapter12_realization_theorem_summary()
        for key, val in ch["theorem"].items():
            assert val is True, f"chapter12 theorem {key!r} not True"
