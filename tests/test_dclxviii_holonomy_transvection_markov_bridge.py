from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxviii_holonomy_transvection_markov_bridge import build_bridge


def test_dclxviii_summary_matches_expected_probabilities() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["anchor_count"] == 40
    assert summary["stay_probability_num"] == 13
    assert summary["stay_probability_den"] == 40
    assert summary["nonneighbor_jump_probability_num"] == 1
    assert summary["nonneighbor_jump_probability_den"] == 40


def test_dclxviii_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxviii_markov_coefficients_and_spectrum_are_exact() -> None:
    payload = build_bridge()
    assert payload["markov_coefficients"] == {"I": "3/10", "A": "-1/40", "J": "1/40"}
    assert payload["markov_statistics"]["spectrum"] == {"1/4": 24, "2/5": 15, "1": 1}


def test_dclxviii_routing_counts_are_13_0_1() -> None:
    payload = build_bridge()
    assert payload["routing_statistics"] == {"diagonal_count": 13, "edge_count": 0, "nonedge_count": 1}