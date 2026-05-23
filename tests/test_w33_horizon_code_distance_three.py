from __future__ import annotations

from analysis.w33_horizon_code_distance_three import horizon_code_distance_three_packet


def test_mccix_packets() -> None:
    packet = horizon_code_distance_three_packet()

    assert packet["packet"] == {
        "q": 3,
        "n": 72,
        "k_code": 66,
        "redundancy": 6,
        "q_redundancy": 729,
    }
    assert packet["hamming_analysis"] == {
        "v_t2_d5": 10369,
        "v_t1_d4": 145,
        "identity": "d=5 would require V2<=3^6, but 10369>729; triangle witness gives weight 3",
    }
    assert packet["distance_statement"] == {
        "upper_bound": 3,
        "status": "d <= 3 established (d=5 excluded; explicit weight-3 witness provided)",
    }


def test_mccix_all_checks_pass() -> None:
    packet = horizon_code_distance_three_packet()

    assert packet["checks"] == {
        "packet_is_72_66_q3": True,
        "redundancy_is_6": True,
        "q_to_redundancy_is_729": True,
        "hamming_v_t2_is_10369": True,
        "d5_excluded_by_hamming": True,
        "hamming_v_t1_is_145": True,
        "d4_not_excluded_by_hamming": True,
        "triangle_boundary_witness_has_weight3": True,
        "witness_implies_d_le_3": True,
        "combined_upper_bound_is_3": True,
    }
    assert packet["n_verified"] == 10
