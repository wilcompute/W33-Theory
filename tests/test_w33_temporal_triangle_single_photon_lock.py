from __future__ import annotations

from analysis.w33_temporal_triangle_single_photon_lock import (
    temporal_triangle_single_photon_lock_packet,
)


def test_mcciii_packets() -> None:
    packet = temporal_triangle_single_photon_lock_packet()

    assert packet["packet"] == {
        "q": 3,
        "Phi_6": 7,
        "triangle_cells": [3, 3, 1, 7],
        "history_split": [9, 3, 6],
        "w33_split": [1, 12, 27, 40],
        "cloud": 81,
        "lambda_gauge": 72,
    }
    assert packet["lock"] == {
        "identity": "(3+3+1)=7=Phi_6; 9=3+6=q+q!; 40=1+12+27; 81=27*3",
        "single_photon_reading": "three time bins (past, now, future) as one-photon self-entangled qutrit mode",
    }


def test_mcciii_all_checks_pass() -> None:
    packet = temporal_triangle_single_photon_lock_packet()

    assert packet["checks"] == {
        "triangle_cells_are_phi6": True,
        "history_split_is_q_plus_qfact": True,
        "diagonal_equals_q": True,
        "directed_equals_qfact": True,
        "w33_split_is_1_12_27": True,
        "w33_total_is_40": True,
        "bell_cloud_is_81": True,
        "lambda_gauge_is_72": True,
        "rank_root_link": True,
        "all_draft_synthesis_checks_true": True,
    }
    assert packet["n_verified"] == 10
