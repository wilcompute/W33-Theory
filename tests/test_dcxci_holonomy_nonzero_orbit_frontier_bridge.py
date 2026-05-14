from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxci_holonomy_nonzero_orbit_frontier_bridge import build_bridge


def test_dcxci_summary_matches_binary_orbit_reduction() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["current_orbit_size"] == 1
    assert summary["live_orbit_size"] == 2
    assert summary["orbit_count"] == 2


def test_dcxci_live_increments_form_one_nonzero_orbit() -> None:
    payload = build_bridge()
    orbit_data = payload["orbit_data"]

    assert orbit_data["zero_orbit_representative"] == [[0, 0], [0, 0]]
    assert orbit_data["nonzero_orbit_representatives"] == [[[0, 1], [0, 0]], [[0, 2], [0, 0]]]
    assert orbit_data["mapped_live_increment"] == [[0, 2], [0, 0]]


def test_dcxci_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())