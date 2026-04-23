from __future__ import annotations

from scripts.w33_e8_correspondence_boundary_audit import (
    analyze,
    classify_correspondence_claims,
    correspondence_surface_summary,
)


def test_surface_summary_keeps_exact_finite_backbone_visible() -> None:
    summary = correspondence_surface_summary()

    assert summary["w33"] == {"vertex_count": 40, "edge_count": 240}
    assert summary["e8"]["root_count"] == 240
    assert summary["e8"]["z3_root_counts"] == (78, 81, 81)
    assert summary["e8"]["z3_algebra_dims"] == (86, 81, 81)
    assert summary["edge_decomposition"] == {
        "incident": 12,
        "h12_internal": 12,
        "h27_internal": 108,
        "cross": 108,
    }
    assert summary["homology"]["betti_numbers"] == (1, 81, 0, 0)
    assert summary["homology"]["euler_characteristic"] == -80
    assert summary["tetrahedron_structure"] == {
        "tetrahedron_count": 40,
        "all_triangles_in_exactly_one_tet": True,
        "independent_constraints": 120,
    }
    assert summary["checks"]["ALL_VERIFIED"] is True


def test_claim_classification_separates_exact_interpretive_and_phenomenology_layers() -> None:
    records = {record["name"]: record for record in classify_correspondence_claims()}

    assert records["edge_root_count_identity"]["claim_class"] == "exact"
    assert records["edge_root_count_identity"]["support_level"] == "exact count identity"

    assert records["sp43_we6_edge_transitivity"]["claim_class"] == "exact"
    assert records["e8_z3_root_split_78_81_81"]["claim_class"] == "exact"
    assert records["w33_h1_rank_81"]["claim_class"] == "exact"
    assert records["tetrahedron_constraint_packet_40_times_3"]["claim_class"] == "exact"

    assert records["three_generation_finite_pattern"]["claim_class"] == "exact-pattern"
    assert records["e6_a2_zero_sector_algebraic_split"]["claim_class"] == "exact"

    assert records["cycle_space_as_matter_sector"]["claim_class"] == "interpretive"
    assert records["w33_sector_alignment_as_gauge_matter_antimatter"]["claim_class"] == "interpretive"

    assert records["dark_matter_ratio_27_over_5"]["claim_class"] == "phenomenology"
    assert records["weinberg_angle_3_over_8_inheritance"]["claim_class"] == "phenomenology"


def test_three_generation_pattern_is_exact_but_matter_identification_is_not() -> None:
    records = {record["name"]: record for record in classify_correspondence_claims()}
    finite = records["three_generation_finite_pattern"]["evidence"]
    matter = records["cycle_space_as_matter_sector"]["evidence"]

    assert finite["b1"] == 81
    assert finite["local_shell_size"] == 27
    assert finite["matter_lines_per_generation"] == 27
    assert finite["generation_count"] == 3
    assert finite["line_orbit_sizes"] == (36, 27, 27, 27, 1, 1, 1)

    assert matter["b1_equals_g1_dim"] is True
    assert matter["generation_routes_agree"] is True
    assert matter["g1_dim"] == 81
    assert matter["b1"] == 81


def test_phenomenology_layers_remain_present_but_are_not_marked_exact() -> None:
    records = {record["name"]: record for record in classify_correspondence_claims()}
    dark = records["dark_matter_ratio_27_over_5"]["evidence"]
    weinberg = records["weinberg_angle_3_over_8_inheritance"]["evidence"]

    assert dark["h27_vertices"] == 27
    assert dark["visible_dof"] == 5
    assert dark["ratio"] == 27 / 5
    assert dark["ratio_decimal"] == 5.4

    assert weinberg["gut_scale_prediction"]["value"] == 3 / 8
    assert weinberg["low_energy_running"]["experimental"] == 0.23122


def test_overall_boundary_audit_marks_old_all_verified_surface_as_broader_than_exact_boundary() -> None:
    summary = analyze()
    theorem = summary["boundary_theorem"]

    assert summary["status"] == "ok"
    assert summary["exact_record_names"] == (
        "edge_root_count_identity",
        "sp43_we6_edge_transitivity",
        "e8_z3_root_split_78_81_81",
        "w33_h1_rank_81",
        "tetrahedron_constraint_packet_40_times_3",
        "three_generation_finite_pattern",
        "e6_a2_zero_sector_algebraic_split",
    )
    assert summary["interpretive_record_names"] == (
        "cycle_space_as_matter_sector",
        "w33_sector_alignment_as_gauge_matter_antimatter",
    )
    assert summary["phenomenology_record_names"] == (
        "dark_matter_ratio_27_over_5",
        "weinberg_angle_3_over_8_inheritance",
    )
    assert theorem["the_count_group_homology_and_tetrahedron_claims_are_exact"] is True
    assert theorem["the_three_generation_pattern_is_exact_finite_structure_but_not_yet_full_physics_by_itself"] is True
    assert theorem["the_e6_plus_a2_zero_sector_is_exact_on_the_e8_side_but_physical_gauge_reading_is_later_input"] is True
    assert theorem["the_dark_matter_and_weinberg_outputs_are_phenomenology_layers_not_exact_bridge_theorems"] is True
    assert theorem["the_old_all_verified_surface_is_stronger_than_the_exact_boundary"] is True
    assert theorem["the_correspondence_boundary_is_now_cleanly_separated"] is True
    assert "ALL_VERIFIED" in summary["boundary_note"]
