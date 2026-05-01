from __future__ import annotations

from pathlib import Path

import pytest

from scripts.w33_local_albert_shadow_audit import (
    analyze,
    canonical_signed_cubic_summary,
    classify_local_albert_shadow,
    cubic_cocycle_boundary_summary,
    jordan_boundary_summary,
    local_shell_summary,
)

SAGE_TRANSPORT = (
    Path(__file__).resolve().parents[1]
    / "artifacts"
    / "sage_h27_to_schlafli_effective_triads_conjugacy.json"
)

pytestmark = pytest.mark.skipif(
    not SAGE_TRANSPORT.exists(),
    reason="optional Sage H27-to-Schlafli transport artifact is absent",
)


def test_local_shell_summary_matches_exact_heisenberg_e6_package() -> None:
    summary = local_shell_summary()

    assert summary["visible_shell_size"] == 27
    assert summary["mub_class_count"] == 4
    assert summary["mub_class_sizes"] == (3, 3, 3, 3)
    assert summary["fiber_count"] == 9
    assert summary["fiber_size"] == 3
    assert summary["generation_fiber_sizes"] == (9, 9, 9)
    assert summary["schlafli_parameters"] == (27, 16, 10, 8)
    assert summary["classical_tritangent_total"] == 45
    assert summary["internal_tritangent_count"] == 36
    assert summary["missing_center_coset_count"] == 9
    assert summary["local_projective_symmetry_order"] == 648
    assert summary["local_affine_symmetry_order"] == 1296
    assert summary["local_affine_point_stabilizer_order"] == 48
    assert summary["full_graph_group_order"] == 51840


def test_canonical_signed_cubic_matches_the_full_45_tritangent_support() -> None:
    summary = canonical_signed_cubic_summary()

    assert summary["triad_count"] == 45
    assert summary["top_level_triads_match_solution"] is True
    assert summary["canonical_solution_solvable"] is True
    assert summary["triad_set_matches_hessian_partition"] is True
    assert summary["fiber_triad_count"] == 9
    assert summary["affine_triad_count"] == 36
    assert summary["u_line_count"] == 12
    assert summary["affine_lifts_per_u_line"] == 3
    assert summary["point_tritangent_incidence_values"] == (5,)
    assert summary["uniform_point_tritangent_incidence"] is True
    assert summary["point_tritangent_incidence"] == 5
    assert summary["total_positive_signs"] == 22
    assert summary["total_negative_signs"] == 23
    assert summary["fiber_positive_signs"] == 2
    assert summary["fiber_negative_signs"] == 7
    assert summary["affine_positive_signs"] == 20
    assert summary["affine_negative_signs"] == 16


def test_cocycle_boundary_separates_naive_we6_failure_from_canonical_gauge_success() -> (
    None
):
    summary = cubic_cocycle_boundary_summary()

    assert summary["canonical_generator_count"] == 6
    assert summary["canonical_failure_count"] == 0
    assert summary["canonical_global_bits"] == (0, 0, 0, 0, 0, 0)
    assert summary["naive_generator_count"] == 6
    assert summary["naive_strict_solved_count"] == 0
    assert summary["naive_projective_solved_count"] == 0
    assert summary["naive_strict_failure_count"] == 6
    assert summary["naive_projective_failure_count"] == 6
    assert summary["correct_invariance_requires_cocycle_gauge"] is True


def test_jordan_boundary_marks_the_current_local_certificate_as_graph_level() -> None:
    summary = jordan_boundary_summary()

    assert summary["graph_test_available"] is True
    assert summary["h27_edge_count"] == 108
    assert summary["h27_degree_set"] == (8,)
    assert summary["cn_determines_h27_adjacency"] is True
    assert summary["contains_explicit_jordan_identity_verdict"] is False
    assert summary["contains_explicit_local_product_table"] is False
    assert summary["contains_explicit_rank_spectrum"] is False


def test_record_classification_and_overall_audit_keep_the_boundary_honest() -> None:
    records = {record["name"]: record for record in classify_local_albert_shadow()}
    summary = analyze()
    theorem = summary["local_albert_shadow_theorem"]

    assert (
        records["local_h27_heisenberg_schlafli_shell"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert (
        records["canonical_45_tritangent_signed_cubic"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert (
        records["cocycle_gauge_local_invariance_boundary"]["support_level"]
        == "exact boundary condition"
    )
    assert (
        records["full_local_jordan_product_theorem"]["support_level"]
        == "not-yet-exact local product law"
    )

    assert summary["status"] == "ok"
    assert summary["record_names_exact_or_boundary"] == (
        "local_h27_heisenberg_schlafli_shell",
        "canonical_45_tritangent_signed_cubic",
        "cocycle_gauge_local_invariance_boundary",
    )
    assert summary["record_names_open"] == ("full_local_jordan_product_theorem",)
    assert (
        theorem["the_local_shell_has_exact_27_point_heisenberg_schlafli_geometry"]
        is True
    )
    assert (
        theorem[
            "the_canonical_signed_cubic_support_is_exactly_the_45_tritangents_split_as_9_plus_36"
        ]
        is True
    )
    assert theorem["each_local_line_lies_on_exactly_five_tritangents"] is True
    assert (
        theorem[
            "the_signed_cubic_support_requires_the_canonical_cocycle_gauge_for_we6_invariance"
        ]
        is True
    )
    assert (
        theorem["the_naive_we6_permutation_action_does_not_preserve_the_signed_cubic"]
        is True
    )
    assert (
        theorem[
            "the_repo_currently_reaches_a_local_albert_shadow_not_a_full_local_jordan_product"
        ]
        is True
    )
    assert "canonical cocycle gauge" in summary["boundary_note"]
