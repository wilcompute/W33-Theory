from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcii_holonomy_rank_one_update_bridge import build_bridge


def test_dcxcii_summary_matches_rank_jump() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["support_packet_size"] == 162
    assert summary["current_nilpotent_rank"] == 0
    assert summary["live_nilpotent_rank"] == 1
    assert summary["rank_jump"] == 1


def test_dcxcii_live_increments_are_rank_one_square_zero_updates() -> None:
    payload = build_bridge()
    rank_data = payload["rank_data"]

    assert rank_data["current_increment"] == [[0, 0], [0, 0]]
    assert rank_data["current_rank"] == 0
    assert rank_data["live_increments"] == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
    assert rank_data["live_ranks"] == [1, 1]


def test_dcxcii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())