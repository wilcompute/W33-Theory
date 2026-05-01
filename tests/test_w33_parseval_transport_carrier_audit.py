from scripts.w33_parseval_transport_carrier_audit import build_parseval_transport_carrier_summary


def test_parseval_transport_carrier_matches_center_quad_carrier() -> None:
    summary = build_parseval_transport_carrier_summary()

    assert summary["status"] == "ok"
    assert summary["coordinate_conversion"] == {
        "line_carrier_to_center_quad": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
        "all_40_projective_points_match_after_permutation": True,
    }
    assert summary["anti_line_center_quad_bridge"] == {
        "anti_line_count": 90,
        "center_quad_count": 90,
        "mapped_anti_lines_equal_center_quads": True,
        "duplicate_class_count": 45,
        "duplicate_class_size_distribution": {2: 45},
        "duplicate_pairing_equals_center_quad_antipodes": True,
    }


def test_parseval_transport_carrier_matches_quotient_point_carrier() -> None:
    summary = build_parseval_transport_carrier_summary()

    assert summary["quotient_point_bridge"] == {
        "quotient_point_count": 45,
        "duplicate_pairs_equal_quotient_point_quad_pairs": True,
        "duplicate_pair_supports_equal_quotient_point_supports": True,
    }
    assert summary["quotient_line_bridge"] == {
        "quotient_line_count": 27,
        "recovered_support_partitions_equal_quotient_lines": True,
        "negative_sign_graph_five_cliques_equal_quotient_lines": True,
        "recovered_line_size_distribution": {5: 27},
        "recovered_point_line_incidence_distribution": {3: 45},
        "quotient_point_line_incidence_distribution": {3: 45},
    }
    assert summary["canonical_graph_identification"] == {
        "positive_sign_graph_equals_transport_graph": True,
        "negative_sign_graph_equals_quotient_point_graph": True,
        "transport_graph_parameters": {
            "vertices": 45,
            "degree": 32,
            "lambda": 22,
            "mu": 24,
            "edge_count": 720,
        },
        "quotient_point_graph_parameters": {
            "vertices": 45,
            "degree": 12,
            "lambda": 3,
            "mu": 3,
            "edge_count": 270,
        },
    }


def test_parseval_transport_carrier_theorem() -> None:
    summary = build_parseval_transport_carrier_summary()

    assert summary["theorem"] == {
        "the_90_parseval_anti_lines_are_exactly_the_90_center_quads_after_coordinate_conversion": True,
        "the_duplicate_anti_line_columns_are_exactly_the_45_quotient_points_of_dual_gq_4_2": True,
        "the_same_anti_line_carrier_recovers_the_full_27_line_dual_gq_4_2_incidence": True,
        "the_full_dual_gq_4_2_incidence_is_recoverable_from_the_negative_sign_graph_alone": True,
        "the_positive_and_negative_anti_line_sign_graphs_are_exactly_the_transport_and_quotient_point_graphs": True,
    }
    assert "the 90 anti-lines are the 90 center-quads" in summary["interpretation"]
    assert "canonically the quotient points of dual GQ(4,2)" in summary["interpretation"]
    assert "27 quotient lines recovered directly" in summary["interpretation"]
    assert "27 five-cliques of the negative sign graph" in summary["interpretation"]