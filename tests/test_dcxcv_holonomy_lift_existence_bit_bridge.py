from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcxcv_holonomy_lift_existence_bit_bridge import build_bridge


def test_dcxcv_summary_matches_lift_existence_bit_reduction() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["current_lift_existence_bit"] == 0
    assert summary["exact_realization_lift_existence_bit"] == 1
    assert summary["bit_count"] == 1


def test_dcxcv_lift_bit_data_matches_fixed_carrier_package() -> None:
    payload = build_bridge()
    lift_bit_data = payload["lift_bit_data"]

    assert lift_bit_data["current_state_bit"] == 0
    assert lift_bit_data["exact_realization_state_bit"] == 1
    assert lift_bit_data["fixed_carrier_plane"] == "U1"
    assert lift_bit_data["fixed_shell"] == [81, 162, 81]


def test_dcxcv_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())