from __future__ import annotations

from scripts.w33_witting_packet_transport_local_system_audit import analyze


def test_packet_transport_local_system_theorem_is_exact() -> None:
    payload = analyze()
    theorem = payload["packet_transport_local_system_theorem"]

    assert theorem["the_packet_transport_matchings_define_an_exact_135dimensional_connection_bundle"] is True
    assert theorem["the_packet_connection_bundle_splits_exactly_as_45_plus_90"] is True
    assert theorem["the_packet_signed_holonomy_operator_satisfies_s2_equals_4s_plus_32i"] is True
    assert theorem["the_packet_triangle_holonomy_cycle_types_are_exactly_240_2880_2160"] is True
    assert theorem["the_packet_a2_operator_has_exact_spectrum_and_cubic_relation"] is True
    assert theorem[
        "the_packet_local_system_recovers_the_same_transport_operator_holonomy_and_a2_invariants_as_the_centerquad_route"
    ] is True
    assert theorem["the_witting_packet_layer_carries_the_full_exact_transport_local_system"] is True


def test_packet_transport_local_system_records_match_expected_counts() -> None:
    payload = analyze()
    bundle = payload["packet_connection_bundle"]
    split = payload["packet_trivial_standard_split"]
    signed = payload["packet_signed_holonomy_operator"]
    holonomy = payload["packet_triangle_holonomy"]
    a2 = payload["packet_a2_local_system"]
    label = payload["label_gauge_dictionary"]
    crosswalk = payload["invariant_crosswalk"]

    assert bundle == {
        "base_vertices": 45,
        "fiber_dimension": 3,
        "total_dimension": 135,
        "adjacency_spectrum": {-16: 6, -4: 20, -1: 64, 2: 24, 8: 20, 32: 1},
        "laplacian_spectrum": {0: 1, 24: 20, 30: 24, 33: 64, 36: 20, 48: 6},
        "trace_a_squared": 4320,
        "trace_a_cubed": 17280,
    }
    assert split["trivial_dimension"] == 45
    assert split["standard_dimension"] == 90
    assert split["trivial_standard_coupling_max_abs"] < 1e-12
    assert split["trivial_block_equals_transport_adjacency"] is True
    assert split["trivial_block_spectrum"] == {-4: 20, 2: 24, 32: 1}
    assert split["standard_block_spectrum"] == {-16: 6, -1: 64, 8: 20}
    assert split["standard_block_laplacian_spectrum"] == {24: 20, 33: 64, 48: 6}

    assert signed == {
        "dimension": 45,
        "spectrum": {-4: 30, 8: 15},
        "quadratic_identity_s_squared_equals_4s_plus_32i": True,
        "trace_s_squared": 1440,
        "trace_s_cubed": 5760,
    }
    assert holonomy == {
        "transport_triangles": 5280,
        "cycle_type_counts": {
            "identity": 240,
            "three_cycle": 2880,
            "transposition": 2160,
        },
    }
    assert a2["rank"] == 2
    assert a2["cartan_matrix"] == [[2, -1], [-1, 2]]
    assert a2["spectrum"] == {-16: 6, -1: 64, 8: 20}
    assert a2["laplacian_spectrum"] == {24: 20, 33: 64, 48: 6}
    assert a2["trace_h_squared"] == 2880
    assert a2["trace_h_cubed"] == -14400
    assert a2["cubic_relation_h3_plus_9h2_minus_120h_minus_128i"] is True
    assert a2["all_six_weyl_matrices_realized"] is True
    assert a2["all_edge_weyl_matrices_preserve_cartan"] is True

    assert label["packet_sorted_label_permutation_counts"] == {
        "012": 176,
        "021": 133,
        "102": 130,
        "120": 95,
        "201": 95,
        "210": 91,
    }
    assert label["packet_sorted_label_parity_distribution"] == {0: 366, 1: 354}
    assert label["sorted_label_permutation_counts_match_centerquad"] is False

    assert crosswalk == {
        "connection_bundle_spectrum_matches_centerquad": True,
        "standard_sector_spectrum_matches_centerquad": True,
        "signed_operator_spectrum_matches_centerquad": True,
        "triangle_holonomy_counts_match_centerquad": True,
        "a2_operator_spectrum_matches_centerquad": True,
    }
