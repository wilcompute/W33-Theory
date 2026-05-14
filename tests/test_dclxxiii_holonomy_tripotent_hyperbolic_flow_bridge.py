from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxiii_holonomy_tripotent_hyperbolic_flow_bridge import build_bridge


def test_dclxxiii_summary_matches_expected_ranks() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["zero_rank"] == 1
    assert summary["positive_rank"] == 24
    assert summary["negative_rank"] == 15


def test_dclxxiii_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxiii_coefficients_match_closed_hyperbolic_form() -> None:
    payload = build_bridge()
    assert payload["tripotent_hyperbolic_coefficients"] == {
        "even": "log(10)/2",
        "odd": "log(8/5)/2",
    }



def test_dclxxiii_breakthrough_mentions_single_canonical_tripotent() -> None:
    payload = build_bridge()
    text = payload["flow"]["breakthrough"].lower()
    assert "single canonical tripotent" in text
