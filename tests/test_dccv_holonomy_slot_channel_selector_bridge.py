from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccv_holonomy_slot_channel_selector_bridge import build_bridge


def test_dccv_summary_matches_two_valued_selector_collapse() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["open_slot_count"] == 1
    assert summary["live_slot_value_count"] == 2
    assert summary["remote_coupler_count"] == 2
    assert summary["ordered_line_type_count"] == 2
    assert summary["helicity_count"] == 2


def test_dccv_selector_ledger_has_expected_two_value_maps() -> None:
    payload = build_bridge()
    ledger = payload["selector_ledger"]

    assert ledger["allowed_live_slot_values"] == [1, 2]
    assert sorted(ledger["value_to_component"].keys()) == ["1", "2"]
    assert sorted(ledger["value_to_ordered_line_type"].keys()) == ["1", "2"]


def test_dccv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())