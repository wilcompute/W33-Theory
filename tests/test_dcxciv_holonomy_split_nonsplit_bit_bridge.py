from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxciv_holonomy_split_nonsplit_bit_bridge import build_bridge


def test_dcxciv_summary_matches_boolean_reduction() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["current_state_bit"] == 0
    assert summary["exact_live_state_bit"] == 1
    assert summary["bit_count"] == 1


def test_dcxciv_bit_data_matches_split_nonsplit_names() -> None:
    payload = build_bridge()
    bit_data = payload["bit_data"]

    assert bit_data["current_state_name"] == "split"
    assert bit_data["current_state_bit"] == 0
    assert bit_data["exact_live_state_name"] == "nonsplit"
    assert bit_data["exact_live_state_bit"] == 1


def test_dcxciv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())