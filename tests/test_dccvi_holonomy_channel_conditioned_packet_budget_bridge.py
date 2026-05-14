from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccvi_holonomy_channel_conditioned_packet_budget_bridge import build_bridge


def test_dccvi_summary_matches_conditioned_budget_split() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["selector_value_count"] == 2
    assert summary["routes_per_channel"] == 9
    assert summary["local_fiber_count"] == 9
    assert summary["conditioned_packet_size"] == 81
    assert summary["total_packet_size"] == 162


def test_dccvi_each_live_value_has_balanced_81_81_packet_budget() -> None:
    payload = build_bridge()
    conditioned = payload["conditioned_budgets"]

    assert sorted(conditioned.keys()) == ["1", "2"]
    for value in ["1", "2"]:
        assert conditioned[value]["selected_route_budget"] == 9
        assert conditioned[value]["complement_route_budget"] == 9
        assert conditioned[value]["selected_packet_budget"] == 81
        assert conditioned[value]["complement_packet_budget"] == 81


def test_dccvi_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())