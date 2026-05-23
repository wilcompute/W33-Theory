from __future__ import annotations

from analysis.w33_horizon_code_distance_q3_conditional import (
    horizon_code_distance_q3_conditional_packet,
)


def test_mccxi_packet() -> None:
    packet = horizon_code_distance_q3_conditional_packet()

    assert packet["packet"] == {
        "q": 3,
        "n": 72,
        "k_code": 66,
        "rank_H": 6,
        "zero_columns_full_H": 0,
    }
    assert packet["distance_claim"] == {
        "upper_bound_constructive": "d <= 3",
        "conditional_exact": "if minimal symmetric K12 embedding + no proportional edge columns, then d = 3 = q",
        "identity": "d=q=3 (conditional C346c)",
    }


def test_mccxi_all_checks_pass() -> None:
    packet = horizon_code_distance_q3_conditional_packet()

    assert packet["checks"] == {
        "packet_is_72_66_q3": True,
        "full_parity_rank_is_6": True,
        "all_columns_nonzero_constructive": True,
        "no_weight1_constructive": True,
        "triangle_witness_weight3": True,
        "d_le_3_from_triangle_witness": True,
        "d_le_3_from_mccix_upper_bound": True,
        "assumption_minimal_embedding_declared": True,
        "assumption_no_proportional_edge_columns_declared": True,
        "conditional_d_eq_3": True,
    }
    assert packet["n_verified"] == 10
