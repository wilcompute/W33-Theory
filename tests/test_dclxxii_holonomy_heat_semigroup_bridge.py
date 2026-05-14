from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxii_holonomy_heat_semigroup_bridge import build_bridge


def test_dclxxii_summary_matches_expected_ranks() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["stationary_rank"] == 1
    assert summary["fast_rank"] == 24
    assert summary["slow_rank"] == 15


def test_dclxxii_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxxii_generator_coefficients_are_the_closed_form_logs() -> None:
    payload = build_bridge()
    assert payload["generator_coefficients"] == {
        "I": "log(40)/3",
        "A": "log(8/5)/6",
        "J": "(5 log 5 - 21 log 2)/120",
    }


def test_dclxxii_slow_and_fast_rates_are_ordered_correctly() -> None:
    payload = build_bridge()
    rates = payload["generator_rates"]
    assert float(rates["slow_rate"]) < float(rates["fast_rate"])
    assert float(rates["gap_ratio"]) > 1.0