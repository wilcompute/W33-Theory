from pathlib import Path

import pytest

from scripts.w33_exact_lie_bridge_audit import (
    analyze,
    classify_lie_bridges,
    local_e6_bridge_summary,
    local_h27_affine_symmetry_summary,
    projective_symplectic_action_summary,
    psp43_order,
    sp43_order,
    we6_order,
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


def test_local_e6_bridge_matches_exact_shell_data() -> None:
    summary = local_e6_bridge_summary()
    assert summary["neighbor_count"] == 12
    assert summary["nonneighbor_count"] == 27
    assert summary["mub_class_count"] == 4
    assert summary["mub_class_sizes"] == (3, 3, 3, 3)
    assert summary["fiber_count"] == 9
    assert summary["fiber_size"] == 3
    assert summary["generation_fiber_sizes"] == (9, 9, 9)
    assert summary["schlafli_parameters"] == (27, 16, 10, 8)
    assert summary["tritangent_split"] == {
        "classical_total": 45,
        "internal_shell": 36,
        "missing_center_cosets": 9,
    }


def test_projective_symplectic_action_keeps_exact_orbits_visible() -> None:
    summary = projective_symplectic_action_summary()
    assert summary["generator_count"] > 0
    assert summary["generator_order_set"] == (3,)
    assert summary["enumerated_group_order"] == 25920
    assert summary["point_stabilizer_order"] == 648
    assert summary["point_orbit_size"] == 40
    assert summary["edge_orbit_size"] == 240
    assert summary["acts_transitively_on_points"] is True
    assert summary["acts_transitively_on_edges"] is True
    assert summary["classical_orders"] == {
        "psp43": 25920,
        "sp43": 51840,
        "we6": 51840,
    }
    assert psp43_order() == 25920
    assert sp43_order() == 51840
    assert we6_order() == 51840


def test_local_h27_affine_symmetry_separates_full_and_projective_stabilizers() -> None:
    summary = local_h27_affine_symmetry_summary()

    assert summary["full_graph_group_order"] == 51840
    assert summary["full_graph_point_stabilizer_order"] == 1296
    assert summary["full_graph_h27_restriction_order"] == 1296
    assert summary["full_graph_stabilizer_restricts_faithfully"] is True

    assert summary["projective_group_order"] == 25920
    assert summary["projective_point_stabilizer_order"] == 648
    assert summary["projective_h27_restriction_order"] == 648
    assert summary["projective_stabilizer_restricts_faithfully"] is True

    assert summary["local_affine_group_order"] == 1296
    assert summary["local_affine_point_stabilizer_order"] == 48
    assert summary["local_projective_subgroup_order"] == 648
    assert summary["local_projective_to_affine_index"] == 2
    assert summary["local_affine_transitive"] is True
    assert summary["local_affine_triads_invariant"] is True
    assert summary["local_projective_triads_invariant"] is True
    assert summary["matches_full_graph_local_order"] is True
    assert summary["matches_projective_local_order"] is True


def test_bridge_classification_keeps_e6_exact_and_e8_non_functorial() -> None:
    records = {record["name"]: record for record in classify_lie_bridges()}

    assert (
        records["local_schlafli_e6_bridge"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert records["local_schlafli_e6_bridge"]["depends_only_on_qutrit_kernel"] is True

    assert (
        records["local_h27_affine_symmetry"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert records["local_h27_affine_symmetry"]["depends_only_on_qutrit_kernel"] is True

    assert (
        records["projective_symplectic_we6_symmetry"]["support_level"]
        == "repo-exact + classical exact"
    )
    assert (
        records["projective_symplectic_we6_symmetry"]["depends_only_on_qutrit_kernel"]
        is True
    )

    assert (
        records["edge_count_equals_e8_root_count"]["support_level"]
        == "count identity only"
    )
    assert (
        records["edge_count_equals_e8_root_count"]["depends_only_on_qutrit_kernel"]
        is False
    )

    assert (
        records["spectral_248_e8_dimension"]["support_level"] == "later spectral layer"
    )
    assert (
        records["spectral_248_e8_dimension"]["depends_only_on_qutrit_kernel"] is False
    )


def test_analyze_summary_lists_exact_and_non_functorial_bridges() -> None:
    summary = analyze()
    assert summary["status"] == "ok"
    assert summary["exact_bridge_names"] == (
        "local_schlafli_e6_bridge",
        "local_h27_affine_symmetry",
        "projective_symplectic_we6_symmetry",
    )
    assert summary["non_functorial_bridge_names"] == (
        "edge_count_equals_e8_root_count",
        "spectral_248_e8_dimension",
    )
