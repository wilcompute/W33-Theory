from __future__ import annotations

from scripts.w33_witting_packet_quotient_geometry_audit import analyze


def test_packet_quotient_geometry_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_quotient_geometry_theorem"]

    assert theorem["the_45_packet_leaves_form_the_exact_exceptional_point_graph_srg_45_12_3_3"] is True
    assert theorem["the_packet_leaf_graph_is_isomorphic_to_the_exact_centerquad_45point_quotient_graph"] is True
    assert theorem["the_27_packets_are_exactly_the_27_maximal_k5_cliques_of_the_leaf_graph"] is True
    assert theorem["packet_leaf_incidence_is_exact_dual_gq42"] is True
    assert theorem["the_packet_line_graph_is_exactly_srg_27_10_1_5_and_matches_the_quotient_line_graph"] is True
    assert theorem["the_witting_packet_layer_reconstructs_the_full_exact_45point_quotient_geometry"] is True


def test_packet_quotient_geometry_records_match_expected_counts() -> None:
    payload = analyze()
    leafs = payload["leaf_graph_dictionary"]
    packet_lines = payload["packet_line_dictionary"]
    crosswalk = payload["quotient_crosswalk"]

    assert leafs["leaf_count"] == 45
    assert leafs["graph_parameters"] == {
        "vertices": 45,
        "degree_distribution": {12: 45},
        "lambda_distribution": {3: 270},
        "mu_distribution": {3: 720},
        "edge_count": 270,
    }
    assert len(leafs["sample_leaves"]) > 0

    assert packet_lines["packet_line_count"] == 27
    assert packet_lines["maximal_k5_count"] == 27
    assert packet_lines["leafs_per_packet_line_distribution"] == {5: 27}
    assert packet_lines["packets_per_leaf_distribution"] == {3: 45}
    assert len(packet_lines["sample_packet_lines"]) > 0

    assert crosswalk == {
        "leaf_graph_isomorphic_to_quotient_point_graph": True,
        "packet_line_graph_isomorphic_to_quotient_line_graph": True,
        "quotient_point_count": 45,
        "quotient_line_count": 27,
        "quotient_incidences": 135,
    }
