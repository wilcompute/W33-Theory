from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxii_holonomy_ternary_admittance_bridge import build_bridge


def test_dclxxxii_summary_matches_expected_ternary_context() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["q"] == 3
    assert summary["carrier_size"] == 40



def test_dclxxxii_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxxii_dimensionless_pair_matches_expected_closed_forms() -> None:
    payload = build_bridge()
    assert payload["dimensionless_pair"] == {
        "exchange_channel": "Y = epsilon * c = sqrt(3/10)",
        "size_channel": "Z = mu * c = sqrt(10/3)",
        "reciprocity": "Y * Z = 1",
        "ternary_squares": "Y^2 = 3/10, Z^2 = 10/3",
    }
