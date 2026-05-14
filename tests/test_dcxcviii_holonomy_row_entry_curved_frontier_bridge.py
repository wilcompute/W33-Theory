from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcviii_holonomy_row_entry_curved_frontier_bridge import build_bridge


def test_dcxcviii_summary_matches_row_entry_localization() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["current_supported_entry_count"] == 0
    assert summary["exact_supported_row_count"] == 4046
    assert summary["exact_row_support_size"] == 1
    assert summary["distinct_live_entry_value_count"] == 2


def test_dcxcviii_local_data_matches_one_sparse_row_entry_structure() -> None:
    payload = build_bridge()
    local_data = payload["local_data"]

    assert local_data["fixed_host_plane"] == "U1"
    assert local_data["fixed_shell"] == [81, 162, 81]
    assert local_data["row_support_size_distribution"] == {1: 4046}
    assert local_data["entry_value_distribution"] == {1: 2029, 2: 2017}


def test_dcxcviii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())