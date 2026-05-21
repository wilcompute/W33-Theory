from __future__ import annotations

from analysis.w33_commensuration_clock import commensuration_clock_packet


def test_mclxix_action_clock() -> None:
    packet = commensuration_clock_packet()

    assert packet["base_moduli"] == {
        "history_cells": 9,
        "w33_rays": 40,
        "S_holo": 20,
        "sigma0": 15,
        "mult_gap": 24,
        "modulus_set": [9, 40, 20, 15, 24],
    }
    assert packet["action_clock"] == {
        "A_star": 360,
        "lcm_modulus_set": 360,
        "dual_pairs": {
            "temporal_geometric": ["360/40=9", "360/9=40"],
            "holographic_morita": ["360/20=18", "360/18=20"],
            "uv_shell": ["360/15=24", "360/24=15"],
        },
    }


def test_mclxix_cloud_beat_identity() -> None:
    packet = commensuration_clock_packet()

    assert packet["cloud_beat"] == {
        "cloud_total": 81,
        "beat_period": 3240,
        "identity": "3240 = lcm(360,81) = 9*360 = 40*81",
        "beat_over_action": 9,
        "beat_over_cloud": 40,
        "action_over_cloud": "40/9",
    }


def test_mclxix_all_checks_pass() -> None:
    packet = commensuration_clock_packet()

    assert packet["checks"] == {
        "action_star_is_360": True,
        "action_star_is_lcm_of_base_moduli": True,
        "action_star_is_minimal_common_period": True,
        "all_base_moduli_divide_action_star": True,
        "dual_pair_temporal_geometric": True,
        "dual_pair_holographic_morita": True,
        "dual_pair_uv_shell": True,
        "cloud_beat_is_lcm_action_star_and_cloud": True,
        "cloud_beat_duality_maps_to_histories_and_rays": True,
        "cloud_beat_factorization": True,
    }
    assert packet["n_verified"] == 10
