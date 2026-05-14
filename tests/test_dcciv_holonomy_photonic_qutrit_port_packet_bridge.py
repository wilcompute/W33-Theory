from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcciv_holonomy_photonic_qutrit_port_packet_bridge import build_bridge


def test_dcciv_summary_matches_route_bundle_packet_factorization() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["helicity_count"] == 2
    assert summary["total_port_route_count"] == 18
    assert summary["local_qutrit_fiber_count"] == 9
    assert summary["common_packet_size"] == 162


def test_dcciv_common_packet_has_all_four_exact_readings() -> None:
    payload = build_bridge()
    common_packet = payload["factorizations"]["common_packet"]

    assert common_packet["route_bundle_side"] == [18, 9]
    assert common_packet["photonic_side"] == [2, 81]
    assert common_packet["selector_side"] == [6, 27]
    assert common_packet["host_side"] == [81, 81]


def test_dcciv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())