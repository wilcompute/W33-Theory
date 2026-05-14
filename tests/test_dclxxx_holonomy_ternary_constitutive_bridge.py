from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxx_holonomy_ternary_constitutive_bridge import build_bridge


def test_dclxxx_summary_matches_expected_carrier_data() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["q"] == 3
    assert summary["carrier_size"] == 40
    assert summary["dynamic_rank"] == 39



def test_dclxxx_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxx_closed_form_constitutive_pair_matches_expected_strings() -> None:
    payload = build_bridge()
    assert payload["constitutive_pair"] == {
        "sin2_theta_w": "3/13",
        "cos2_theta_w": "10/13",
        "impedance_squared": "10/3",
        "mu": "1/sqrt(12)",
        "epsilon": "sqrt(3)/20",
        "speed_squared": "40",
        "product_law": "mu * epsilon * c^2 = 1",
    }
