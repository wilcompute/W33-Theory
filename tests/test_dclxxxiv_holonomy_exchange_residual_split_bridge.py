from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxiv_holonomy_exchange_residual_split_bridge import build_bridge


def test_dclxxxiv_summary_matches_expected_split_counts() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["carrier_size"] == 40
    assert summary["exchange_count"] == 12
    assert summary["residual_count"] == 28



def test_dclxxxiv_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxxiv_split_law_matches_closed_forms() -> None:
    payload = build_bridge()
    assert payload["split_law"] == {
        "exchange": "40 * Y^2 = 12",
        "residual": "40 * (1-Y^2) = 28 = 1 + 27",
        "dual": "12 * (Z^2 - 1) = 28",
        "carrier": "40 = 12 + 28 = 12 + 1 + 27",
    }
