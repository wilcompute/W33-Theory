from __future__ import annotations

from scripts.w33_projective_affine_shell_audit import analyze


def test_projective_affine_shell_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["projective_affine_shell_theorem"]

    assert theorem["the_40_points_of_pg_3_3_match_the_repo_w33_vertices_and_projective_two_qutrit_pauli_points"] is True
    assert theorem["the_40_totally_isotropic_lines_form_the_symplectic_generalized_quadrangle_gq_3_3"] is True
    assert theorem["the_point_graph_is_exactly_srg_40_12_2_4"] is True
    assert theorem["every_point_perp_is_a_pg_2_3_hyperplane_of_size_13"] is True
    assert theorem["every_hyperplane_complement_is_an_ag_3_3_affine_cube_of_size_27"] is True
    assert theorem["every_affine_cube_has_exactly_13_direction_classes_of_9_parallel_lines"] is True
    assert theorem["the_canonical_anchor_chart_recovers_f3_cubed_and_the_9_times_3_fiber_packet"] is True
    assert theorem["the_projective_affine_shell_bridge_is_fully_closed"] is True


def test_projective_affine_shell_counts_match_pg33_and_ag33() -> None:
    payload = analyze()
    projective = payload["projective_space"]
    generalized_quadrangle = payload["symplectic_generalized_quadrangle"]
    hyperplanes = payload["hyperplane_profiles"]
    anchor = payload["canonical_anchor_chart"]

    assert projective["point_count"] == 40
    assert projective["projective_line_count"] == 130
    assert projective["projective_line_size_set"] == [4]

    assert generalized_quadrangle["isotropic_line_count"] == 40
    assert generalized_quadrangle["isotropic_line_size_set"] == [4]
    assert generalized_quadrangle["point_graph_parameters"] == {"n": 40, "k": 12, "lambda": 2, "mu": 4}
    assert generalized_quadrangle["repo_w33_edge_count"] == 240
    assert generalized_quadrangle["repo_vertex_count"] == 40
    assert generalized_quadrangle["repo_adjacency_matches_symplectic_point_graph"] is True

    assert hyperplanes["distinct_hyperplane_sizes"] == [13]
    assert hyperplanes["distinct_hyperplane_line_counts"] == [13]
    assert hyperplanes["distinct_isotropic_line_counts_through_anchor"] == [4]
    assert hyperplanes["distinct_affine_point_counts"] == [27]
    assert hyperplanes["distinct_affine_line_counts"] == [117]
    assert hyperplanes["distinct_affine_direction_counts"] == [13]

    assert anchor["anchor_point"] == (1, 0, 0, 0)
    assert anchor["direction_at_infinity"] == (0, 0, 0, 1)
    assert anchor["coordinate_count"] == 27
    assert anchor["coordinates_cover_f3_cube"] is True
    assert anchor["fiber_count"] == 9
    assert anchor["fiber_size_set"] == [3]
    assert anchor["all_fibers_extend_to_projective_lines"] is True
