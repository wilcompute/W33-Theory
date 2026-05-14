from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxi_holonomy_constitutive_carrier_bridge import build_bridge


def test_dclxxxi_summary_matches_expected_ternary_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["q"] == 3
    assert summary["point_count"] == 40
    assert summary["dynamic_rank"] == 39



def test_dclxxxi_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxxi_carrier_law_matches_expected_closed_forms() -> None:
    payload = build_bridge()
    assert payload["carrier_law"] == {
        "dynamic_rank": "1/(mu*epsilon) - 1",
        "point_count": "1/(mu*epsilon)",
        "ternary_dynamic_count": "q * Phi_3 = 3 * 13 = 39",
        "ternary_total_count": "1 + q * Phi_3 = 40",
        "host_split": "1 + 24 + 15",
    }
