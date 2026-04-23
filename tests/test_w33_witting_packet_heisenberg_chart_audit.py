from __future__ import annotations

from scripts.w33_witting_packet_heisenberg_chart_audit import analyze


def test_packet_heisenberg_chart_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_heisenberg_chart_theorem"]

    assert theorem["the_27_balanced_packets_split_canonically_as_9_fibers_of_size_3"] is True
    assert theorem["the_allowed_sector_triangle_patterns_form_an_affine_plane_in_f3_4"] is True
    assert theorem["the_balanced_shell_has_no_edges_within_a_fiber_and_exactly_3_between_any_two_fibers"] is True
    assert theorem["the_balanced_shell_is_fiber_preserving_isomorphic_to_the_canonical_local_h27_shell"] is True
    assert theorem["the_balanced_packet_layer_carries_an_exact_f3_squared_times_f3_chart"] is True


def test_packet_heisenberg_chart_records_are_uniform() -> None:
    payload = analyze()
    fibers = payload["fiber_dictionary"]
    plane = payload["affine_triangle_plane"]
    adjacency = payload["fiber_adjacency_dictionary"]
    iso = payload["fiber_preserving_isomorphism"]

    assert fibers["fiber_count"] == 9
    assert fibers["fiber_size_distribution"] == {3: 9}
    assert len(fibers["fiber_keys"]) == 9

    assert plane["triangle_pattern_count"] == 9
    assert plane["triangle_pattern_multiplicity_distribution"] == {3: 9}
    assert plane["exact_triangle_pattern_equations"] == {
        "c": "1 - a + b mod 3",
        "d": "2 + a + b mod 3",
    }
    assert plane["affine_pattern_failures"] == []

    assert adjacency["within_fiber_edge_distribution"] == {False: 27}
    assert adjacency["between_fiber_edge_count_distribution"] == {3: 36}

    assert iso["exists"] is True
    assert len(iso["sample_mapping"]) > 0

