from scripts.w33_parseval_target_geometry_audit import build_parseval_target_geometry_summary


def test_parseval_target_geometry_records_visible_target_channels() -> None:
    summary = build_parseval_target_geometry_summary()

    assert summary["status"] == "ok"
    assert summary["target_side_frame_geometry"] == {
        "spread_etf": {
            "frame_type": "ETF(36,15)",
            "vector_count": 36,
            "sector_dimension": 15,
            "column_norm_squared": "15/2",
            "off_diagonal_inner_products": ["-3/2", "3/2"],
            "normalized_coherence": "1/5",
            "welch_bound_squared": "1/25",
            "frame_operator_spectrum": {"0": 21, "18": 15},
            "positive_sign_graph": {
                "vertices": 36,
                "degree": 15,
                "lambda": 6,
                "mu": 6,
                "edge_count": 270,
                "spectrum": {"-3": 20, "3": 15, "15": 1},
            },
            "negative_sign_graph": {
                "vertices": 36,
                "degree": 20,
                "lambda": 10,
                "mu": 12,
                "edge_count": 360,
                "spectrum": {"-4": 15, "2": 20, "20": 1},
            },
            "positive_sign_equals_overlap_4_graph": True,
            "negative_sign_equals_overlap_1_graph": True,
        },
        "anti_line_quotient": {
            "frame_type": "doubled two-distance tight frame(45,24)",
            "anti_line_count": 90,
            "duplicate_class_count": 45,
            "duplicate_multiplicity": 2,
            "duplicate_pairs_are_disjoint": True,
            "sector_dimension": 24,
            "column_norm_squared": "48/5",
            "off_diagonal_inner_products": ["-12/5", "3/5"],
            "frame_operator_spectrum": {"0": 21, "18": 24},
            "positive_sign_graph": {
                "vertices": 45,
                "degree": 32,
                "lambda": 22,
                "mu": 24,
                "edge_count": 720,
                "spectrum": {"-4": 20, "2": 24, "32": 1},
            },
            "negative_sign_graph": {
                "vertices": 45,
                "degree": 12,
                "lambda": 3,
                "mu": 3,
                "edge_count": 270,
                "spectrum": {"-3": 24, "3": 20, "12": 1},
            },
            "positive_sign_isomorphic_to_transport_graph": True,
            "canonical_transport_carrier": {
                "coordinate_conversion": "(x0,x1,x2,x3) -> (x0,x2,x1,x3)",
                "anti_lines_equal_center_quads_after_coordinate_conversion": True,
                "duplicate_pairing_equals_center_quad_antipodes": True,
                "duplicate_classes_equal_quotient_point_quad_pairs": True,
                "paired_supports_equal_quotient_point_supports": True,
                "quotient_line_count": 27,
                "support_partitions_equal_quotient_lines": True,
                "line_size_distribution": {5: 27},
                "point_line_incidence_distribution": {3: 45},
                "negative_sign_graph_five_cliques_equal_quotient_lines": True,
                "positive_sign_equals_transport_graph_without_relabeling": True,
                "negative_sign_equals_quotient_point_graph_without_relabeling": True,
            },
        },
    }


def test_parseval_target_geometry_records_common_naimark_shadow() -> None:
    summary = build_parseval_target_geometry_summary()

    assert summary["common_naimark_shadow"] == {
        "shared_shadow_dimension": 21,
        "shared_shadow_split": "1 + 20",
        "shared_shadow_arithmetic": {
            "21_equals_q_phi6": "3 * 7",
            "20_equals_edge_count_over_degree": "240 / 12",
        },
        "spread_shadow": {
            "frame_type": "ETF(36,21)",
            "parseval_diagonal": "7/12",
            "parseval_off_diagonal": ["-1/12", "1/12"],
            "normalized_coherence": "1/7",
            "positive_sign_graph": {
                "vertices": 36,
                "degree": 20,
                "lambda": 10,
                "mu": 12,
                "edge_count": 360,
                "spectrum": {"-4": 15, "2": 20, "20": 1},
            },
            "negative_sign_graph": {
                "vertices": 36,
                "degree": 15,
                "lambda": 6,
                "mu": 6,
                "edge_count": 270,
                "spectrum": {"-3": 20, "3": 15, "15": 1},
            },
        },
        "anti_line_shadow": {
            "frame_type": "two-distance shadow frame(45,21)",
            "vector_count": 45,
            "parseval_diagonal": "7/15",
            "parseval_off_diagonal": ["-1/30", "2/15"],
            "normalized_off_diagonal": ["-1/14", "2/7"],
            "positive_sign_graph": {
                "vertices": 45,
                "degree": 12,
                "lambda": 3,
                "mu": 3,
                "edge_count": 270,
                "spectrum": {"-3": 24, "3": 20, "12": 1},
            },
            "negative_sign_graph": {
                "vertices": 45,
                "degree": 32,
                "lambda": 22,
                "mu": 24,
                "edge_count": 720,
                "spectrum": {"-4": 20, "2": 24, "32": 1},
            },
        },
    }


def test_parseval_target_geometry_records_sign_duality_and_theorem() -> None:
    summary = build_parseval_target_geometry_summary()

    assert summary["naimark_sign_duality"] == {
        "spread_shadow_positive_equals_visible_negative": True,
        "spread_shadow_negative_equals_visible_positive": True,
        "anti_shadow_positive_equals_visible_negative": True,
        "anti_shadow_negative_equals_visible_positive": True,
    }
    assert summary["theorem"] == {
        "the_centered_spread_features_form_the_exact_etf_36_15": True,
        "the_anti_line_channel_collapses_to_a_doubled_45_vector_transport_frame_in_the_24_sector": True,
        "the_anti_line_transport_target_is_the_existing_center_quad_quotient_carrier": True,
        "the_anti_line_transport_target_recovers_the_full_27_line_dual_gq_4_2_incidence": True,
        "the_full_dual_gq_4_2_incidence_is_already_recoverable_from_the_negative_sign_graph_five_cliques": True,
        "both_target_systems_share_the_same_hidden_naimark_shadow_split_21_equals_1_plus_20": True,
        "naimark_complement_swaps_the_positive_and_negative_target_side_srg_signatures": True,
    }