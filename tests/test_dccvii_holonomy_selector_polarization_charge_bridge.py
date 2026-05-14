from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccvii_holonomy_selector_polarization_charge_bridge import build_bridge


def test_dccvii_summary_matches_signed_polarization_budget() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["selector_value_count"] == 2
    assert summary["conditioned_packet_budget"] == 81
    assert summary["total_absolute_budget"] == 162


def test_dccvii_flip_negates_charge_profiles() -> None:
    payload = build_bridge()
    profiles = payload["charge_profiles"]
    flip_map = payload["selector_flip_map"]

    assert flip_map == {"1": 2, "2": 1}
    for value in ["1", "2"]:
        flipped = str(flip_map[value])
        for line_type in ["negative", "positive"]:
            assert profiles[value]["charge_by_ordered_line_type"][line_type] == -profiles[flipped]["charge_by_ordered_line_type"][line_type]
        assert profiles[value]["net_charge"] == 0
        assert profiles[value]["absolute_charge_budget"] == 162


def test_dccvii_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())