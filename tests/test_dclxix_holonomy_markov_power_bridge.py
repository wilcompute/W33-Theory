from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxix_holonomy_markov_power_bridge import build_bridge


def test_dclxix_summary_matches_expected_ranks_and_balance() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["stationary_rank"] == 1
    assert summary["fast_rank"] == 24
    assert summary["slow_rank"] == 15
    assert summary["one_step_fast_trace_num"] == 6
    assert summary["one_step_slow_trace_num"] == 6


def test_dclxix_core_identities_all_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())


def test_dclxix_t1_recovers_the_dclxviii_kernel() -> None:
    payload = build_bridge()
    first = payload["power_table"][0]
    assert first["diagonal"] == "13/40"
    assert first["edge"] == "0"
    assert first["nonedge"] == "1/40"
    assert first["fast_trace"] == "6"
    assert first["slow_trace"] == "6"


def test_dclxix_rank15_mode_dominates_after_t1() -> None:
    payload = build_bridge()
    rows = payload["power_table"]
    assert rows[1]["slow_to_fast_ratio"] == "8/5"
    assert rows[2]["slow_to_fast_ratio"] == "64/25"
    assert all(row["slow_to_fast_ratio"] != "1" for row in rows[1:])