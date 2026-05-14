from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxxiii_holonomy_q_phi6_interface_bridge import build_bridge


def test_dclxxxiii_summary_matches_expected_ternary_data() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["q"] == 3
    assert summary["phi6"] == 7
    assert summary["carrier_size"] == 40



def test_dclxxxiii_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxxiii_interface_description_matches_closed_forms() -> None:
    payload = build_bridge()
    assert payload["ternary_interface"] == {
        "exchange_square": "Y^2 = q/(q^2+1) = q/(q+Phi_6) = k/v",
        "exchange_complement": "1-Y^2 = Phi_6/(q^2+1) = Phi_6/(q+Phi_6)",
        "size_square": "Z^2 = (q^2+1)/q = (q+Phi_6)/q = v/k",
        "size_excess": "Z^2 - 1 = Phi_6/q",
    }
