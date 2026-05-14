from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcciii_holonomy_remote_qutrit_coupler_bridge import build_bridge


def test_dcciii_summary_matches_two_complete_qutrit_couplers() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["component_count"] == 2
    assert summary["ports_per_side"] == 3
    assert summary["routes_per_component"] == 9
    assert summary["total_route_count"] == 18


def test_dcciii_every_component_realizes_full_three_by_three_route_table() -> None:
    payload = build_bridge()
    components = payload["remote_qutrit_couplers"]["components"]

    for component in components:
        assert component["realized_routes"] == component["expected_routes"]
        for profile in component["route_profiles"]:
            assert len(profile["left_hits"]) == 1
            assert len(profile["right_hits"]) == 1


def test_dcciii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())