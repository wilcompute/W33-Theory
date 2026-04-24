"""Supplement M - no full PSp(4,3)-invariant 600-cell skeleton on M_120."""

from scripts.w33_h4_orbital_no_go import (
    compute_anchored_local_symmetry_obstruction,
    compute_cycle_holonomy_carrier,
    compute_quadrangle_adjacent_transport_heisenberg_packet,
    compute_quadrangle_adjacent_transport_section_obstruction,
    compute_quadrangle_cover_group_structure,
    compute_quadrangle_ordered_path_s3_carrier,
    compute_local_selector_reduction,
    compute_pair_orbitals,
    compute_point_residue_transport_reduction,
    compute_quadrangle_cover_nonsplitting_obstruction,
    compute_quadrangle_kernel_fibre_action,
    compute_quadrangle_mixed_cover_structure,
    compute_quadrangle_self_duality,
    compute_quadrangle_stabilizer_structure,
)


class TestM1PairOrbitals:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_state_count(self):
        assert self.summary["checks"]["state_count_is_120"]

    def test_transvection_generator_count(self):
        assert self.summary["checks"]["generator_count_is_40"]

    def test_pair_orbital_count(self):
        assert self.summary["checks"]["pair_orbital_count_is_4"]

    def test_pair_sizes_partition_all_pairs(self):
        assert self.summary["checks"]["pair_sizes_sum_to_all_pairs"]

    def test_orbital_degrees(self):
        assert self.summary["orbital_degrees"] == [2, 27, 36, 54]


class TestM2OrbitalGeometry:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_same_line_orbital(self):
        same = self.summary["orbitals"][0]
        assert same["degree"] == 2
        assert same["same_line_pairs"] == 120
        assert same["intersecting_line_pairs"] == 0
        assert same["disjoint_line_pairs"] == 0

    def test_intersecting_line_orbital(self):
        crossing = self.summary["orbitals"][2]
        assert crossing["degree"] == 36
        assert crossing["same_line_pairs"] == 0
        assert crossing["intersecting_line_pairs"] == 2160
        assert crossing["disjoint_line_pairs"] == 0

    def test_disjoint_line_orbitals(self):
        disjoint_degrees = [
            row["degree"]
            for row in self.summary["orbitals"]
            if row["disjoint_line_pairs"] > 0
        ]
        assert disjoint_degrees == [27, 54]


class TestM3NoGo:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_pair_orbitals()

    def test_possible_invariant_degrees(self):
        assert self.summary["possible_invariant_degrees"] == [
            0,
            2,
            27,
            29,
            36,
            38,
            54,
            56,
            63,
            65,
            81,
            83,
            90,
            92,
            117,
            119,
        ]

    def test_no_degree_12_relation(self):
        assert self.summary["checks"]["no_invariant_degree_12_relation"]
        assert 12 not in self.summary["possible_invariant_degrees"]

    def test_no_full_symmetry_600_cell_skeleton(self):
        assert self.summary["theorem"]["no_full_psp43_invariant_600_cell_skeleton_on_M120"]

    def test_next_structure_requires_symmetry_breaking(self):
        assert "break PSp(4,3)" in self.summary["theorem"]["required_next_structure"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM4LocalSelectorReduction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_local_selector_reduction()

    def test_line_graph_is_self_dual_w33(self):
        line_graph = self.summary["line_graph"]
        assert line_graph == {
            "vertex_count": 40,
            "degree": 12,
            "edge_count": 240,
            "adjacent_common_neighbor_count": 2,
            "disjoint_common_neighbor_count": 4,
        }

    def test_intersecting_orbital_is_twelve_lines_times_three_states(self):
        fibres = self.summary["matching_fibres"]
        reduction = self.summary["selector_reduction"]
        assert fibres["fibre_size"] == 3
        assert fibres["state_count"] == 120
        assert fibres["intersecting_state_degree"] == 36
        assert reduction["adjacent_lines_per_base_vertex"] == 12
        assert reduction["one_state_choice_per_adjacent_line"] == 12

    def test_local_blocks_are_permutations(self):
        reduction = self.summary["selector_reduction"]
        assert reduction["local_block_shape"] == [3, 3]
        assert reduction["local_permutation_count"] == 6
        assert reduction["undirected_transport_edges"] == 240
        assert reduction["directed_transport_edges"] == 480

    def test_reduction_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem["the_h4_selector_base_graph_is_the_self_dual_line_copy_of_w33"]
        assert theorem[
            "any_local_12_neighborhood_selector_on_M120_is_equivalent_to_s3_transport_on_that_base_graph"
        ]
        assert "ternary transport law" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM5PointResidueTransportReduction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_point_residue_transport_reduction()

    def test_each_point_carries_a_tetrahedral_line_residue(self):
        residues = self.summary["point_residues"]
        assert residues == {
            "point_count": 40,
            "lines_per_point": 4,
            "undirected_line_pairs_per_point": 6,
            "directed_line_pairs_per_point": 12,
            "triangles_per_point": 4,
            "total_residue_triangles": 160,
        }

    def test_fibres_are_indexed_by_anchor_point_partners(self):
        indexing = self.summary["fibre_indexing"]
        assert indexing["states_per_line"] == 3
        assert indexing["partner_choices_per_incident_point"] == 3
        assert indexing["incident_point_line_records"] == 160

    def test_residue_slots_match_line_graph_edges(self):
        slots = self.summary["transport_slots"]
        assert slots == {
            "undirected_line_graph_edges": 240,
            "directed_line_graph_edges": 480,
            "undirected_residue_slots": 240,
            "directed_residue_slots": 480,
        }

    def test_first_order_local_blocks_are_uniform(self):
        uniformity = self.summary["local_block_uniformity"]
        assert uniformity == {
            "distinct_adjacent_line_block_patterns": 1,
            "distinct_cell_signatures": 1,
            "cell_signature": {
                "common_neighbor_count": 4,
                "other_residue_line_counts": [0, 0],
                "outside_residue_common_neighbor_count": 3,
            },
        }

    def test_point_residue_reduction_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem["each_transport_edge_is_anchored_at_a_unique_w33_point"]
        assert theorem["the_s3_selector_problem_refines_to_point_residue_transport_on_40_k4_stars"]
        assert theorem["bare_point_residue_geometry_does_not_single_out_a_transport_permutation"]
        assert "point-anchored S3 connection" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM6AnchoredLocalSymmetryObstruction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_anchored_local_symmetry_obstruction()

    def test_group_action_on_anchored_slots(self):
        action = self.summary["group_action"]
        assert action == {
            "group_order": 25_920,
            "ordered_anchored_slot_count": 480,
            "seed_slot_orbit_size": 480,
            "seed_slot_stabilizer_size": 54,
        }

    def test_local_choice_block_stays_single_orbit(self):
        block = self.summary["local_choice_block"]
        assert block == {
            "shape": [3, 3],
            "choice_count": 9,
            "stabilizer_orbit_sizes": [9],
        }

    def test_anchored_symmetry_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "even_after_fixing_a_point_and_an_ordered_transport_edge_the_nine_local_choices_remain_symmetry_equivalent"
        ]
        assert "single orbit" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM7CycleHolonomyCarrier:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_cycle_holonomy_carrier()

    def test_triangles_remain_one_orbit(self):
        triangles = self.summary["triangle_cycles"]
        assert triangles == {
            "cycle_count": 160,
            "orbit_sizes": [160],
        }

    def test_quadrangles_split_into_local_and_nonlocal_orbits(self):
        quadrangles = self.summary["quadrangle_cycles"]
        assert quadrangles["cycle_count"] == 1_740
        assert quadrangles["orbit_sizes"] == [120, 1_620]

    def test_small_orbit_is_local_residue_quadrangles(self):
        local_orbit = next(
            record for record in self.summary["quadrangle_cycles"]["orbit_records"]
            if record["is_local_residue_cycle"]
        )
        assert local_orbit["orbit_size"] == 120
        assert local_orbit["distinct_edge_anchor_count"] == 1
        assert local_orbit["all_four_line_intersection_size"] == 1
        assert local_orbit["opposite_intersection_sizes"] == [1, 1]

    def test_large_orbit_is_first_global_quadrangle_carrier(self):
        nonlocal_orbit = next(
            record for record in self.summary["quadrangle_cycles"]["orbit_records"]
            if not record["is_local_residue_cycle"]
        )
        assert nonlocal_orbit["orbit_size"] == 1_620
        assert nonlocal_orbit["distinct_edge_anchor_count"] == 4
        assert nonlocal_orbit["all_four_line_intersection_size"] == 0
        assert nonlocal_orbit["opposite_intersection_sizes"] == [0, 0]

    def test_cycle_holonomy_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem["the_first_nontrivial_holonomy_carrier_appears_on_four_cycles"]
        assert theorem[
            "the_local_120_orbit_is_residue_tetrahedral_and_the_1620_orbit_is_the_first_global_quadrangle_carrier"
        ]
        assert "1620 global 4-cycles" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM8QuadrangleSelfDuality:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_self_duality()

    def test_point_quadrangles_match_line_side_split(self):
        point_quadrangles = self.summary["point_quadrangles"]
        assert point_quadrangles == {
            "cycle_count": 1_740,
            "orbit_sizes": [120, 1_620],
            "local_cycle_count": 120,
            "nonlocal_cycle_count": 1_620,
        }

    def test_nonlocal_line_and_point_quadrangles_match_bijectively(self):
        duality = self.summary["line_point_duality"]
        assert duality == {
            "nonlocal_line_quadrangle_count": 1_620,
            "nonlocal_point_quadrangle_count": 1_620,
            "anchor_image_size": 1_620,
            "anchor_collision_count": 0,
            "inverse_failure_count": 0,
        }

    def test_self_duality_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_first_global_holonomy_carrier_is_a_self_dual_1620_quadrangle_correspondence"
        ]
        assert "canonically self-dual" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM9QuadrangleStabilizerStructure:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_stabilizer_structure()

    def test_stabilizer_counts(self):
        stabilizer = self.summary["stabilizer"]
        assert stabilizer == {
            "size": 16,
            "visible_line_square_action_size": 8,
            "visible_anchor_square_action_size": 8,
            "hidden_line_kernel_size": 2,
            "hidden_anchor_kernel_size": 2,
        }

    def test_visible_square_symmetry_is_dihedral(self):
        visible = self.summary["visible_square_symmetry"]
        assert visible["position_permutation_count"] == 8
        assert visible["position_permutations"] == [
            [0, 1, 2, 3],
            [0, 3, 2, 1],
            [1, 0, 3, 2],
            [1, 2, 3, 0],
            [2, 1, 0, 3],
            [2, 3, 0, 1],
            [3, 0, 1, 2],
            [3, 2, 1, 0],
        ]

    def test_quadrangle_stabilizer_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_first_global_quadrangle_carrier_has_visible_d4_square_symmetry_with_a_hidden_c2_kernel"
        ]
        assert "full D4 visible symmetry" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM10QuadrangleKernelFibreAction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_kernel_fibre_action()

    def test_kernel_counts(self):
        kernel = self.summary["kernel"]
        assert kernel == {
            "size": 2,
            "fixed_anchor_count": 4,
            "quadrangle_line_count": 4,
        }

    def test_hidden_kernel_cycle_type_on_quadrangle_states(self):
        fibre_action = self.summary["fibre_action"]
        assert fibre_action["fixed_state_count"] == 4
        assert fibre_action["swapped_pair_count"] == 4
        assert fibre_action["cycle_type"] == [1, 1, 1, 1, 2, 2, 2, 2]

    def test_each_line_fibre_splits_as_one_fixed_plus_one_swapped_pair(self):
        records = self.summary["fibre_action"]["line_records"]
        for record in records:
            assert len(record["anchors"]) == 2
            assert len(record["nonanchors"]) == 2
            assert len(record["fixed_state_ids"]) == 1
            assert record["fixed_state_ids"] == [record["anchor_pair_state_id"]]
            assert len(record["swapped_state_pairs"]) == 1
            assert len(record["swapped_state_pairs"][0]) == 2

    def test_kernel_fibre_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_hidden_c2_acts_fibrewise_as_anchor_pair_fixing_and_cross_state_swap"
        ]
        assert "anchor-pair state is fixed" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM11QuadrangleMixedCoverStructure:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_mixed_cover_structure()

    def test_bundle_split_counts(self):
        bundle = self.summary["bundle_split"]
        assert bundle == {
            "fixed_state_count": 4,
            "mixed_state_count": 8,
            "mixed_block_count": 4,
            "mixed_block_size": 2,
        }

    def test_mixed_cover_is_two_sheeted_over_visible_square(self):
        cover = self.summary["mixed_cover"]
        assert cover == {
            "visible_block_action_size": 8,
            "lifted_action_size": 16,
            "lifts_per_visible_element": [2],
            "deck_involution": {
                "block_permutation": [0, 1, 2, 3],
                "within_block_flips": [1, 1, 1, 1],
            },
        }

    def test_mixed_cover_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_mixed_8_state_orbit_is_a_two_sheeted_cover_of_the_visible_square"
        ]
        assert "global deck involution" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM12QuadrangleCoverNonsplittingObstruction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_cover_nonsplitting_obstruction()

    def test_extension_counts(self):
        extension = self.summary["extension"]
        assert extension == {
            "action_order": 16,
            "visible_quotient_order": 8,
            "deck_involution": {
                "block_permutation": [0, 1, 2, 3],
                "within_block_flips": [1, 1, 1, 1],
            },
            "complement_exists": False,
        }

    def test_nonsplitting_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_mixed_cover_is_a_non_split_central_extension_of_visible_d4_by_the_deck_c2"
        ]
        assert "no D4-equivariant global choice of sheet" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM13QuadrangleCoverGroupStructure:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_cover_group_structure()

    def test_group_invariants(self):
        assert self.summary["group"] == {
            "action_order": 16,
            "center_order": 4,
            "commutator_subgroup_order": 2,
            "order_distribution": {1: 1, 2: 7, 4: 8},
            "square_count": 3,
        }

    def test_central_elements(self):
        assert self.summary["central_elements"] == {
            "deck_involution": {
                "block_permutation": [0, 1, 2, 3],
                "within_block_flips": [1, 1, 1, 1],
            },
            "square_half_turn_lift": {
                "block_permutation": [2, 3, 0, 1],
                "within_block_flips": [0, 1, 0, 1],
            },
            "commutator_half_turn_lift": {
                "block_permutation": [2, 3, 0, 1],
                "within_block_flips": [1, 0, 1, 0],
            },
        }

    def test_presentation_exists(self):
        presentation = self.summary["presentation"]
        assert presentation["reflection_square"] == {
            "block_permutation": [0, 1, 2, 3],
            "within_block_flips": [1, 1, 1, 1],
        }
        assert presentation["rotation_square"] == {
            "block_permutation": [2, 3, 0, 1],
            "within_block_flips": [0, 1, 0, 1],
        }

    def test_group_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_mixed_cover_group_has_center_v4_commutator_c2_and_a_deck_twisted_order_4_presentation"
        ]
        assert "center V4" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM14QuadrangleAdjacentTransportHeisenbergPacket:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_adjacent_transport_heisenberg_packet()

    def test_packet_counts(self):
        assert self.summary["ordered_adjacent_pair"] == {
            "line_ids": [0, 1],
            "packet_size": 27,
            "stabilizer_image_order": 54,
        }

    def test_local_shadow_counts(self):
        shadow = self.summary["local_shadow"]
        assert shadow["left_line_state_count"] == 3
        assert shadow["right_line_state_count"] == 3
        assert shadow["cell_count"] == 9
        assert shadow["cell_fibre_size"] == 3
        assert set(shadow["cell_counts"].values()) == {3}

    def test_heisenberg_packet_invariants(self):
        assert self.summary["heisenberg_packet"] == {
            "group_order": 27,
            "center_order": 3,
            "commutator_order": 3,
            "cell_fibre_group_order": 3,
            "central_quotient_order": 9,
            "nonidentity_element_order": 3,
        }

    def test_semidirect_extension_invariants(self):
        extension = self.summary["semidirect_extension"]
        assert extension["full_packet_symmetry_order"] == 54
        assert extension["full_cell_shadow_symmetry_order"] == 18
        assert extension["reflection_count"] == 9
        assert extension["reflection_witness"]["packet_order"] == 2
        assert extension["reflection_witness"]["generated_group_order"] == 54
        assert sorted(extension["reflection_witness"]["cell_action"]) == list(range(9))
        assert extension["reflection_witness"]["cell_action"] != list(range(9))

    def test_heisenberg_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_27_global_quadrangles_over_an_ordered_adjacent_line_pair_form_a_heisenberg_packet"
        ]
        assert theorem[
            "the_full_packet_symmetry_is_the_heisenberg_packet_extended_by_a_reflection_involution"
        ]
        assert "canonical Heisenberg packet" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM15QuadrangleAdjacentTransportSectionObstruction:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_adjacent_transport_section_obstruction()

    def test_obstruction_counts(self):
        assert self.summary["obstruction"] == {
            "heisenberg_packet_order": 27,
            "central_fibre_order": 3,
            "visible_local_shadow_order": 9,
            "full_packet_symmetry_order": 54,
            "full_local_shadow_symmetry_order": 18,
            "heisenberg_complement_exists": False,
            "full_symmetry_complement_exists": False,
        }

    def test_section_obstruction_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "the_visible_9_cell_adjacent_transport_shadow_has_no_packet_equivariant_section"
        ]
        assert "no packet-equivariant lift" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())


class TestM16QuadrangleOrderedPathS3Carrier:
    @classmethod
    def setup_class(cls):
        cls.summary = compute_quadrangle_ordered_path_s3_carrier()

    def test_ordered_path_action_counts(self):
        assert self.summary["ordered_path_action"] == {
            "path_count": 4320,
            "seed_orbit_size": 4320,
            "seed_stabilizer_size": 6,
            "completion_fibre_size": 3,
        }

    def test_seed_path_completion_data(self):
        assert self.summary["seed_path"] == {
            "line_ids": [0, 1, 13],
            "completion_quadrangles": [
                [0, 1, 13, 4],
                [0, 1, 13, 7],
                [0, 1, 13, 10],
            ],
            "completion_action_size": 6,
        }

    def test_s3_carrier_theorem_holds(self):
        theorem = self.summary["theorem"]
        assert theorem[
            "ordered_nonlocal_2_paths_are_the_first_exact_s3_completion_carrier"
        ]
        assert "first exact S3 object" in theorem["interpretation"]

    def test_all_checks_pass(self):
        assert all(self.summary["checks"].values())
