from __future__ import annotations

from scripts.w33_witting_packet_transport_complement_audit import analyze


def test_packet_transport_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_transport_theorem"]

    assert theorem["the_packet_leaf_disjointness_graph_is_exactly_srg_45_32_22_24"] is True
    assert theorem["the_packet_transport_graph_is_isomorphic_to_the_exact_centerquad_transport_graph"] is True
    assert theorem["packet_transport_edges_are_exactly_disjoint_leaf_pairs"] is True
    assert theorem["the_27_packet_lines_become_exact_5cocliques_in_transport"] is True
    assert theorem["every_packet_transport_edge_has_a_unique_local_s3_packetline_matching"] is True
    assert theorem["all_six_s3_permutations_occur_under_sorted_packet_labels"] is True
    assert theorem["the_witting_packet_layer_reconstructs_the_full_exact_45point_transport_graph"] is True


def test_packet_transport_records_match_expected_counts() -> None:
    payload = analyze()
    transport = payload["transport_graph_dictionary"]
    packet_transport = payload["packet_transport_dictionary"]
    crosswalk = payload["transport_crosswalk"]
    matching = payload["local_s3_packet_matching"]

    assert transport == {
        "leaf_count": 45,
        "graph_parameters": {
            "vertices": 45,
            "degree_distribution": {32: 45},
            "lambda_distribution": {22: 720},
            "mu_distribution": {24: 270},
            "edge_count": 720,
        },
        "intersection_profile_by_transport_adjacency": {
            "true": {0: 720},
            "false": {1: 270},
        },
    }

    assert packet_transport["packet_line_count"] == 27
    assert packet_transport["packet_lines_per_leaf_distribution"] == {3: 45}
    assert packet_transport["transport_edges_inside_packet_line_distribution"] == {0: 27}
    assert len(packet_transport["sample_leaf_packet_lines"]) == 8

    assert crosswalk == {
        "packet_transport_isomorphic_to_centerquad_transport": True,
        "packet_transport_vertices": 45,
        "packet_transport_edges": 720,
        "centerquad_transport_vertices": 45,
        "centerquad_transport_edges": 720,
    }

    assert matching["every_transport_edge_has_unique_matching"] is True
    assert matching["all_six_permutations_realized_under_sorted_packet_labels"] is True
    assert matching["permutation_counts_under_sorted_packet_labels"] == {
        "012": 176,
        "021": 133,
        "102": 130,
        "120": 95,
        "201": 95,
        "210": 91,
    }
    assert matching["permutation_parity_distribution"] == {0: 366, 1: 354}
    assert len(matching["example_edges"]) == 6
