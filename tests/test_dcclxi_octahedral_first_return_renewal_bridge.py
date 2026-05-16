from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxi_octahedral_first_return_renewal_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["f1"] - 0.0) < 1e-12
    assert abs(s["f2"] - 0.25) < 1e-12
    assert abs(s["f3"] - 0.125) < 1e-12
    assert abs(s["first_return_mass"] - 1.0) < 1e-9
    assert abs(s["mean_return_from_first_return"] - 6.0) < 1e-7


def test_renewal_reconstruction_window() -> None:
    payload = build_bridge()
    for row in payload["reconstruction_window"]:
        assert abs(row["difference"]) < 1e-9


def test_generating_identity() -> None:
    payload = build_bridge()
    for row in payload["generating_checks"]:
        assert abs(row["G_series"] - row["G_closed"]) < 1e-8
        assert abs(row["F_series"] - row["F_closed"]) < 1e-8
        assert abs(row["G_minus_1_over_1_minus_F"]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
