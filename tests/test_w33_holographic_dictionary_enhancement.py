from __future__ import annotations

from analysis.w33_holographic_dictionary_enhancement import (
    holographic_dictionary_enhancement_packet,
)


def test_mccv_packets() -> None:
    packet = holographic_dictionary_enhancement_packet()

    assert packet["packets"] == {
        "k": 12,
        "n": 72,
        "k_code": 66,
        "v": 40,
        "bulk_edges": 240,
        "h1": 81,
    }
    assert packet["dictionary"] == {
        "boundary_rate": "11/12",
        "bulk_rate": "27/80",
        "projection_edges_per_boundary_vertex": 20,
        "identity": "R_boundary=66/72=11/12, R_bulk=81/240=27/80, projection=240/12=20=v/2",
    }
    assert packet["enhancement"]["ratio"] == "220/81"


def test_mccv_all_checks_pass() -> None:
    packet = holographic_dictionary_enhancement_packet()

    assert packet["checks"] == {
        "horizon_code_is_72_66": True,
        "boundary_rate_is_11_over_12": True,
        "bulk_edges_is_240": True,
        "bulk_rate_is_81_over_240": True,
        "bulk_rate_reduces_to_27_over_80": True,
        "projection_is_20": True,
        "projection_equals_v_over_2": True,
        "enhancement_is_220_over_81": True,
        "enhancement_numeric_gt_1": True,
        "k_minus_1_over_k_lock": True,
    }
    assert packet["n_verified"] == 10
