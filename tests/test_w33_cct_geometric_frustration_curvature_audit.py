from __future__ import annotations

from scripts.w33_cct_geometric_frustration_curvature_audit import (
    cct_geometric_frustration_curvature_summary,
)


def test_cct_chapter4_frustration_packet_has_the_exact_20g_counts() -> None:
    summary = cct_geometric_frustration_curvature_summary()

    assert summary["cct_frustration_packet"] == {
        "encoding_methods": (
            "gaps",
            "discrete_curvature_into_fourth_dimension",
            "distortion",
            "twisting",
        ),
        "encoding_method_count": 4,
        "vertex_sharing_cluster": "20G",
        "tetrahedra_per_20g": 20,
        "fivefold_tetrahedra_per_orientation_class": 4,
        "plane_classes_before_closure": 70,
        "plane_classes_after_curvature_or_twist": 10,
        "plane_class_reduction_factor": 7,
        "curvature_twist_angle_matching_status": (
            "source-local equivalence; encoded here only through exact counts"
        ),
    }


def test_w33_curvature_packet_matches_4d_bivector_and_riemann_dimensions() -> None:
    summary = cct_geometric_frustration_curvature_summary()

    assert summary["w33_curvature_packet"] == {
        "q": 3,
        "mu": 4,
        "lambda": 2,
        "bivector_dimension": 6,
        "curvature_shell_dimension": 20,
        "oriented_curvature_decomposition": {
            "self_dual_weyl": 5,
            "tracefree_ricci": 9,
            "anti_self_dual_weyl": 5,
            "scalar": 1,
        },
        "full_weyl_dimension": 10,
        "edge_over_degree": 20,
        "two_ovoid_curvature_shell": 20,
        "four_ovoid_vertex_shell": 40,
    }


def test_h4_shell_is_simultaneously_five_24_cells_and_bivector_curvature() -> None:
    summary = cct_geometric_frustration_curvature_summary()

    assert summary["h4_curvature_factorization"] == {
        "h4_shell_vertices": 120,
        "h4_as_five_24_cell_packets": 5,
        "h4_as_bivector_times_curvature": 120,
        "bivector_factor": 6,
        "curvature_factor": 20,
    }


def test_conformal_shadow_packet_keeps_the_5_plus_5_and_240_counts_exact() -> None:
    summary = cct_geometric_frustration_curvature_summary()

    assert summary["conformal_shadow_packet"] == {
        "bipartite_24_cell_groups": (5, 5),
        "bipartite_group_total": 10,
        "roots_per_24_cell": 24,
        "ten_24_cell_e8_shell": 240,
        "w33_edge_root_shell": 240,
        "discrete_weyl_scale_status": (
            "source guidance; no continuum Weyl gauge field is asserted"
        ),
    }


def test_cct_geometric_frustration_theorem_flags_are_all_true() -> None:
    summary = cct_geometric_frustration_curvature_summary()

    assert summary["theorem"] == {
        "four_frustration_encodings_match_w33_mu": True,
        "twenty_g_packet_matches_curvature_shell": True,
        "plane_class_reduction_lands_on_phi4_weyl_shell": True,
        "h4_shell_factorizes_as_bivector_times_curvature": True,
        "conformal_shadow_5_plus_5_matches_phi4_and_e8_root_shell": True,
        "smooth_gravity_claim_remains_frontier_scoped": True,
    }
