from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcci_holonomy_active_sector_trisection_frontier_bridge import build_bridge


def test_dcci_summary_matches_three_sector_split() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["fan_adjacent_rank"] == 24
    assert summary["upper_remote_rank"] == 6
    assert summary["lower_remote_rank"] == 6
    assert summary["sector_count"] == 3


def test_dcci_sector_data_matches_expected_columns() -> None:
    payload = build_bridge()
    sector_data = payload["sector_data"]

    assert len(sector_data["fan_adjacent_columns"]) == 24
    assert sector_data["upper_remote_columns"] == [3, 4, 5, 12, 13, 14]
    assert sector_data["lower_remote_columns"] == [6, 7, 8, 9, 10, 11]
    assert sector_data["fixed_host_plane"] == "U1"


def test_dcci_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())