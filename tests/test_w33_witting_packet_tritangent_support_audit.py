from __future__ import annotations

from scripts.w33_witting_packet_tritangent_support_audit import analyze


def test_packet_tritangent_support_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_tritangent_support_theorem"]

    assert theorem["the_27_balanced_packets_carry_exactly_36_shell_triangles_plus_9_fiber_triples"] is True
    assert theorem["the_rank_intersection_16_graph_has_exactly_the_same_45_support_triples"] is True
    assert theorem["each_balanced_packet_lies_on_exactly_five_support_triples"] is True
    assert theorem["the_packet_support_transports_fiber_preservingly_to_the_canonical_local_h27_support_package"] is True
    assert theorem["the_balanced_packet_support_matches_the_canonical_local_45_support_package"] is True
    assert theorem["the_witting_communication_layer_reconstructs_the_exact_local_albert_shadow_support"] is True


def test_packet_tritangent_support_records_match_local_counts() -> None:
    payload = analyze()
    support = payload["balanced_packet_support_dictionary"]
    rank16 = payload["rank16_support_dictionary"]
    crosswalk = payload["local_support_crosswalk"]

    assert support["packet_count"] == 27
    assert support["shell_triangle_count"] == 36
    assert support["fiber_triple_count"] == 9
    assert support["support_total"] == 45
    assert support["packet_support_incidence_distribution"] == {5: 27}

    assert rank16["rank16_triangle_count"] == 45
    assert rank16["rank16_triangles_equal_support"] is True

    assert crosswalk["transport_isomorphism_exists"] is True
    assert crosswalk["transported_support_matches_local_support"] is True
    assert crosswalk["transported_shell_triangles_match_local_affine_support"] is True
    assert crosswalk["transported_fibers_match_local_fiber_support"] is True
    assert crosswalk["local_support_total"] == 45
    assert crosswalk["local_shell_triangle_count"] == 36
    assert crosswalk["local_fiber_triple_count"] == 9
    assert crosswalk["local_support_incidence_distribution"] == {5: 27}
    assert crosswalk["canonical_local_support_counts"] == {
        "support_total": 45,
        "shell_triangle_count": 36,
        "fiber_triple_count": 9,
        "point_support_incidence": 5,
    }
    assert len(crosswalk["sample_mapping"]) > 0
