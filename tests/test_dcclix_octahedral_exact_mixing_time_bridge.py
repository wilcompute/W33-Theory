from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclix_octahedral_exact_mixing_time_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert abs(s["tv_t0"] - (5.0 / 6.0)) < 1e-12
    assert abs(s["tv_prefactor"] - (2.0 / 3.0)) < 1e-12
    assert abs(s["contraction_base"] - 0.5) < 1e-12
    assert s["tau_eps_0_1"] == 3
    assert s["tau_eps_0_01"] == 7


def test_tv_closed_form() -> None:
    payload = build_bridge()
    tl = payload["tv_timeline"]
    for row in tl[1:12]:
        assert abs(row["tv"] - row["closed_form"]) < 1e-9


def test_mixing_table_formula_matches_bruteforce() -> None:
    payload = build_bridge()
    for row in payload["mixing_table"]:
        assert row["tau_formula"] == row["tau_bruteforce"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
