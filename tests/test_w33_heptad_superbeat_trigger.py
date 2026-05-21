from __future__ import annotations

from analysis.w33_heptad_superbeat_trigger import heptad_superbeat_trigger_packet


def test_mclxx_base_clock_and_obstruction() -> None:
    packet = heptad_superbeat_trigger_packet()

    assert packet["base_clock"] == {
        "A_star": 360,
        "beat_B": 3240,
        "cloud_total": 81,
        "history_cells": 9,
        "w33_rays": 40,
        "identity": "3240 = 9*360 = 40*81",
    }
    assert packet["heptad_obstruction"] == {
        "phi6": 7,
        "B_mod_phi6": 6,
        "statement": "B is not divisible by 7, so heptad channel is the first unsynchronized residue",
    }


def test_mclxx_superbeat_values() -> None:
    packet = heptad_superbeat_trigger_packet()

    assert packet["superbeat_extension"] == {
        "H": 22680,
        "identity": "22680 = lcm(3240,7) = 7*3240",
        "H_over_A_star": 63,
        "H_over_cloud": 280,
        "duality_identity": "22680 = (7*9)*360 = (7*40)*81",
    }


def test_mclxx_all_checks_pass() -> None:
    packet = heptad_superbeat_trigger_packet()

    assert packet["checks"] == {
        "base_beat_is_3240": True,
        "base_beat_does_not_close_heptad": True,
        "heptad_obstruction_residue_is_6": True,
        "superbeat_is_minimal_heptad_closure": True,
        "superbeat_closes_action_clock": True,
        "superbeat_closes_cloud_packet": True,
        "superbeat_preserves_temporal_geometric_duality": True,
        "superbeat_factorization": True,
        "superbeat_over_beat_is_exact_heptad": True,
    }
    assert packet["n_verified"] == 9
