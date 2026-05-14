from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxv_holonomy_screen_universality_bridge import build_bridge


def test_dclxv_summary_matches_universal_family_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["field_order"] == 3
    assert summary["anchor_count"] == 40
    assert summary["transvection_order"] == 3
    assert summary["fixed_screen_size"] == 13
    assert summary["mobile_bulk_size"] == 27
    assert summary["three_cycle_count"] == 9
    assert summary["distinct_fixed_screens"] == 40
    assert summary["point_screen_incidence_count"] == 13


def test_dclxv_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxv_every_anchor_has_same_shell_profile() -> None:
    payload = build_bridge()
    anchors = payload["anchor_records"]

    assert len(anchors) == 40
    assert {tuple(sorted(record["orbit_size_counts"].items())) for record in anchors} == {
        ((1, 13), (3, 9))
    }
    assert {record["fixed_count"] for record in anchors} == {13}
    assert {record["mobile_count"] for record in anchors} == {27}


def test_dclxv_fixed_screens_are_closed_neighborhoods() -> None:
    payload = build_bridge()
    anchors = payload["anchor_records"]
    stats = payload["carrier_statistics"]

    assert all(record["fixed_screen_matches_closed_neighborhood"] for record in anchors)
    assert all(record["fixed_screen_matches_perp_hyperplane"] for record in anchors)
    assert stats["point_screen_membership_histogram"] == {13: 40}