from __future__ import annotations

from scripts.w33_witting_balanced_packet_shell_audit import analyze


def test_balanced_packet_shell_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["balanced_packet_shell_theorem"]

    assert theorem["the_36_decks_split_as_four_anchor_sectors_of_size_9"] is True
    assert theorem["inside_each_9deck_sector_the_overlap1_graph_is_three_disjoint_triangles"] is True
    assert theorem["the_135_fourdeck_packets_split_as_27_balanced_plus_108_skew"] is True
    assert theorem["the_27_balanced_packets_factor_as_9_sector_triangle_patterns_times_3_internal_states"] is True
    assert theorem["deck_overlap_1_on_the_balanced_packets_is_isomorphic_to_the_exact_local_h27_shell"] is True
    assert theorem["rank_intersection_14_on_the_balanced_packets_is_the_schlafli_graph"] is True
    assert theorem["rank_intersection_16_on_the_balanced_packets_is_the_intersection_graph"] is True
    assert theorem["the_balanced_packet_shell_reconstructs_the_local_cubic_surface_layer"] is True


def test_balanced_packet_shell_records_match_local_counts() -> None:
    payload = analyze()
    sectors = payload["anchor_sector_dictionary"]
    packets = payload["fourdeck_packet_dictionary"]
    chart = payload["balanced_packet_chart"]
    graphs = payload["balanced_packet_graphs"]

    assert sectors["sector_sizes"] == {"0": 9, "1": 9, "2": 9, "3": 9}
    assert all(len(components) == 3 for components in sectors["sector_triangle_components"].values())
    assert all(all(len(component) == 3 for component in components) for components in sectors["sector_triangle_components"].values())

    assert packets["packet_count"] == 135
    assert packets["balanced_packet_count"] == 27
    assert packets["skew_packet_count"] == 108
    assert packets["sector_profile_distribution"]["((0, 1), (1, 1), (2, 1), (3, 1))"] == 27

    assert chart["triangle_pattern_count"] == 9
    assert chart["triangle_pattern_multiplicity_distribution"] == {3: 9}
    assert chart["triangle_to_local_state_count_distribution"] == {3: 9}

    assert graphs["deck_overlap_distribution"] == {0: 243, 1: 108}
    assert graphs["rank_intersection_distribution"] == {14: 216, 16: 135}
    assert graphs["balanced_shell_parameters"] == {
        "n": 27,
        "k": 8,
        "lambda_values": [1],
        "mu_values": [0, 3],
        "is_strongly_regular": False,
    }
    assert graphs["balanced_rank14_parameters"] == {
        "n": 27,
        "k": 16,
        "lambda": 10,
        "mu": 8,
        "is_strongly_regular": True,
    }
    assert graphs["balanced_rank16_parameters"] == {
        "n": 27,
        "k": 10,
        "lambda": 1,
        "mu": 5,
        "is_strongly_regular": True,
    }
    assert graphs["isomorphic_to_local_shell"] is True
    assert graphs["isomorphic_to_schlafli"] is True
    assert graphs["isomorphic_to_intersection_graph"] is True

