from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclx_octahedral_return_recurrence_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["stationary_mass"] - (1.0 / 6.0)) < 1e-12
    assert abs(s["mean_return_time"] - 6.0) < 1e-10
    assert abs(s["p1_return"] - 0.0) < 1e-12
    assert abs(s["p2_return"] - 0.25) < 1e-12
    assert abs(s["p3_return"] - 0.125) < 1e-12


def test_return_profile_closed_form() -> None:
    payload = build_bridge()
    for row in payload["return_timeline"][1:13]:
        assert abs(row["direct"] - row["closed_form"]) < 1e-9


def test_generating_function_checks() -> None:
    payload = build_bridge()
    for row in payload["generating_checks"]:
        assert abs(row["difference"]) < 1e-8


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
