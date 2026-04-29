from __future__ import annotations

from scripts.w33_e6_27line_cubic_carrier_audit import analyze, classify_e6_27line_cubic_carrier


def test_e6_27line_cubic_carrier_audit_keeps_carrier_and_witness_layers_distinct() -> None:
    records = {record["name"]: record for record in classify_e6_27line_cubic_carrier()}
    payload = analyze()
    theorem = payload["e6_27line_cubic_carrier_theorem"]

    assert records["dual_27line_gq42_carrier"]["support_level"] == "repo-exact carrier"
    assert records["canonical_signed_cubic_support_on_27line_carrier"]["support_level"] == "repo-exact cubic support"
    assert records["current_e6_trilinear_symmetry_breaking_as_downstream_witness"]["support_level"] == "downstream witness on exact carrier"

    carrier = payload["dual_27line_carrier"]
    assert carrier["dual_gq42_incidence"] == {
        "points": 45,
        "lines": 27,
        "points_per_line": 5,
        "lines_per_point": 3,
        "incidences": 135,
    }
    assert carrier["line_graph_srg"] == {
        "vertices": 27,
        "degree": 10,
        "lambda": 1,
        "mu": 5,
        "edge_count": 135,
        "degree_spectrum_singleton": True,
        "adjacent_common_singleton": True,
        "nonadjacent_common_singleton": True,
    }
    assert carrier["line_graph_triangle_count"] == 45
    assert carrier["points_equal_line_graph_triangles"] is True

    cubic = payload["signed_cubic_support"]
    assert cubic["triad_count"] == 45
    assert cubic["fiber_triad_count"] == 9
    assert cubic["affine_triad_count"] == 36
    assert cubic["uniform_point_tritangent_incidence"] is True
    assert cubic["point_tritangent_incidence_values"] == (5,)
    assert cubic["point_tritangent_incidence"] == 5
    assert cubic["canonical_solution_solvable"] is True

    witness = payload["downstream_trilinear_witness"]
    assert witness["artifact_present"] is True
    assert witness["line_product_closed_form_holds"] is True
    assert witness["line_product_mismatch_count"] in (0, 4)
    assert witness["full_sign_closed_form_holds"] is True
    assert witness["full_sign_mismatch_count"] in (0, 20)

    assert theorem["the_exact_exceptional_carrier_is_the_dual_27line_gq42_graph"] is True
    assert theorem["the_signed_cubic_support_is_exactly_the_45_triangles_on_that_carrier"] is True
    assert theorem["the_current_e6_trilinear_symmetry_breaking_surface_is_a_downstream_witness_on_that_exact_cubic"] is True
    assert "downstream witness" in payload["boundary_note"]
