from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxvii_holonomy_screen_tripotent_bridge import build_bridge


def test_dclxvii_summary_matches_expected_ranks() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["zero_rank"] == 1
    assert summary["positive_rank"] == 24
    assert summary["negative_rank"] == 15


def test_dclxvii_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxvii_tripotent_coefficients_and_spectrum_are_exact() -> None:
    payload = build_bridge()
    assert payload["operator_coefficients"] == {"I": "1/3", "A": "1/3", "J": "-13/120"}
    assert payload["operator_statistics"]["tripotent_spectrum"] == {-1: 15, 0: 1, 1: 24}


def test_dclxvii_projector_ranks_recover_cccliii_split() -> None:
    payload = build_bridge()
    assert payload["projector_ranks"] == {"rank_P0": 1, "rank_P_plus": 24, "rank_P_minus": 15}