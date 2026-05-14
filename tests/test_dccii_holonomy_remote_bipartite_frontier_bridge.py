from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccii_holonomy_remote_bipartite_frontier_bridge import build_bridge


def test_dccii_summary_matches_remote_component_split() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["component_count"] == 2
    assert summary["upper_remote_rank"] == 6
    assert summary["lower_remote_rank"] == 6
    assert summary["component_size"] == 6


def test_dccii_remote_data_matches_exact_k33_components() -> None:
    payload = build_bridge()
    remote_data = payload["remote_data"]

    assert remote_data["upper_remote_component"]["left_part"] == [3, 4, 5]
    assert remote_data["upper_remote_component"]["right_part"] == [12, 13, 14]
    assert remote_data["lower_remote_component"]["left_part"] == [6, 7, 8]
    assert remote_data["lower_remote_component"]["right_part"] == [9, 10, 11]


def test_dccii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())