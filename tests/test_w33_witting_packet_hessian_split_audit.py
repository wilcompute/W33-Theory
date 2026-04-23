from __future__ import annotations

from scripts.w33_witting_packet_hessian_split_audit import analyze


def test_packet_hessian_split_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_hessian_split_theorem"]

    assert theorem["the_36_packet_shell_triangles_project_to_exactly_the_12_affine_lines_of_ag23"] is True
    assert theorem["each_affine_line_supports_exactly_3_packet_triangles_partitioning_its_9_points"] is True
    assert theorem["the_12_affine_lines_split_into_4_direction_classes_of_3_lines_each"] is True
    assert theorem["each_balanced_packet_lies_on_exactly_one_affine_lift_in_each_direction_plus_its_unique_fiber"] is True
    assert theorem["the_balanced_packet_layer_realizes_the_full_hessian_split_9_plus_12_times_3"] is True
    assert theorem["the_witting_packet_layer_reconstructs_the_exact_local_hessian_split"] is True


def test_packet_hessian_split_records_match_expected_geometry() -> None:
    payload = analyze()
    affine = payload["affine_line_dictionary"]
    directions = payload["direction_dictionary"]
    incidence = payload["packet_incidence_dictionary"]
    split = payload["hessian_split_dictionary"]

    assert affine["affine_packet_triangle_count"] == 36
    assert affine["ag23_line_count"] == 12
    assert affine["packet_projected_lines_equal_ag23_lines"] is True
    assert affine["packet_lifts_per_line_distribution"] == {3: 12}
    assert affine["line_partition_failures"] == []

    assert directions["direction_count"] == 4
    assert directions["lines_per_direction_distribution"] == {3: 4}
    assert set(directions["triangles_per_direction"].values()) == {9}
    assert len(directions["direction_classes"]) == 4

    assert incidence["affine_incidence_distribution"] == {4: 27}
    assert incidence["fiber_incidence_distribution"] == {1: 27}
    assert len(incidence["direction_set_distribution"]) == 1
    assert len(incidence["direction_multiset_distribution"]) == 1

    assert split["fiber_triple_count"] == 9
    assert split["affine_triple_count"] == 36
    assert split["support_total"] == 45
    assert len(split["sample_line_lifts"]) > 0
