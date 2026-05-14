from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxc_holonomy_one_slot_frontier_bridge import build_bridge


def test_dcxc_summary_matches_one_slot_frontier() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["support_packet_size"] == 162
    assert summary["current_slot_value"] == 0
    assert summary["allowed_live_slot_values"] == [1, 2]
    assert summary["remaining_open_slot_count"] == 1


def test_dcxc_slot_data_is_exactly_the_upper_right_entry() -> None:
    payload = build_bridge()
    slot_data = payload["slot_data"]

    assert slot_data["open_slot_position"] == [0, 1]
    assert slot_data["current_increment"] == [[0, 0], [0, 0]]
    assert slot_data["allowed_live_increments"] == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]


def test_dcxc_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())