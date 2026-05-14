from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxix_holonomy_common_packet_host_bridge import build_bridge


def test_dclxxxix_summary_matches_host_packet_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["common_packet_size"] == 162
    assert summary["positive_support_size"] == 81
    assert summary["negative_support_size"] == 81
    assert summary["host_support_total"] == 162
    assert summary["global_selector_carrier"] == 1620


def test_dclxxxix_packet_has_three_exact_readings() -> None:
    payload = build_bridge()
    readings = payload["packet_readings"]

    assert readings["selector_side"] == [6, 27]
    assert readings["photonic_side"] == [2, 81]
    assert readings["host_side"] == [81, 81]


def test_dclxxxix_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())