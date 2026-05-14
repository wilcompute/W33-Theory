from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcvi_holonomy_pure_k3_existence_frontier_bridge import build_bridge


def test_dcxcvi_summary_matches_pure_existence_frontier_reduction() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["fixed_packet_dimension"] == 162
    assert summary["finite_ambiguity_count"] == 0
    assert summary["remaining_curved_theorem_count"] == 1


def test_dcxcvi_frontier_data_matches_fixed_host_package() -> None:
    payload = build_bridge()
    frontier = payload["frontier_data"]

    assert frontier["fixed_carrier_plane"] == "U1"
    assert frontier["fixed_shell"] == [81, 162, 81]
    assert frontier["fixed_slot_shape"] == [81, 81]
    assert frontier["remaining_theorem"] == "existence_of_carrier_preserving_transport_twisted_k3_lift"


def test_dcxcvi_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())