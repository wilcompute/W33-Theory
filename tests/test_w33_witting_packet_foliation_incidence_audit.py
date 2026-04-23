from __future__ import annotations

from scripts.w33_witting_packet_foliation_incidence_audit import analyze


def test_packet_foliation_incidence_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_foliation_incidence_theorem"]

    assert theorem["the_balanced_packet_layer_has_exactly_five_canonical_9triple_foliations"] is True
    assert theorem["every_fiber_affine_leaf_intersection_graph_is_exactly_3k33"] is True
    assert theorem["every_affine_affine_leaf_intersection_graph_is_exactly_the_pappus_graph"] is True
    assert theorem["every_pair_of_distinct_foliations_has_the_uniform_27edge_singleton_intersection_law"] is True
    assert theorem["the_witting_packet_layer_carries_a_canonical_fivefoliation_pappus_architecture"] is True


def test_packet_foliation_incidence_records_match_expected_counts() -> None:
    payload = analyze()
    fol = payload["foliation_dictionary"]
    pairs = payload["pair_incidence_dictionary"]

    assert fol["foliation_names"] == ["dir_0_1", "dir_1_0", "dir_1_1", "dir_1_2", "fiber"]
    for record in fol["foliation_records"].values():
        assert record["leaf_count"] == 9
        assert record["leaf_size_distribution"] == {3: 9}
        assert record["packet_cover_distribution"] == {1: 27}

    assert pairs["pair_count"] == 10
    assert pairs["fiber_affine_pair_count"] == 4
    assert pairs["affine_affine_pair_count"] == 6

    for record in pairs["pair_records"]:
        assert record["edge_count"] == 27
        assert record["degree_distribution"] == {3: 18}
        if (record["left"] == "fiber") ^ (record["right"] == "fiber"):
            assert record["component_sizes"] == [6, 6, 6]
            assert record["fiber_affine_match_3k33"] is True
            assert record["affine_affine_match_pappus"] is False
        else:
            assert record["component_sizes"] == [18]
            assert record["fiber_affine_match_3k33"] is False
            assert record["affine_affine_match_pappus"] is True
