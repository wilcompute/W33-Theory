from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxx_holonomy_markov_tomography_bridge import build_bridge


def test_dclxx_summary_matches_expected_tomography_ranks() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["determinant_num"] == 3
    assert summary["determinant_den"] == 200
    assert summary["recovered_positive_rank"] == 24
    assert summary["recovered_negative_rank"] == 15


def test_dclxx_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxx_exact_reconstruction_coefficients_are_correct() -> None:
    payload = build_bridge()
    assert payload["tomography_coefficients"] == {
        "P_plus_from_X1_X2": ["32/3", "-80/3"],
        "P_minus_from_X1_X2": ["-25/6", "50/3"],
        "determinant": "3/200",
    }


def test_dclxx_recovered_entry_values_match_cccliii() -> None:
    payload = build_bridge()
    assert payload["recovered_entry_values"] == {
        "P_plus": {"diagonal": "3/5", "edge": "1/10", "nonedge": "-1/15"},
        "P_minus": {"diagonal": "3/8", "edge": "-1/8", "nonedge": "1/24"},
    }