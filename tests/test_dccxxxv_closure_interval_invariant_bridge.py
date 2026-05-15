from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxv_closure_interval_invariant_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["causal_class_count"] == 6
    assert s["maximal_interval"] == 5
    assert s["maximal_interval_squared"] == 25
    assert s["final_scale_ratio"] == 32


def test_diagonal_and_maximal_interval() -> None:
    payload = build_bridge()
    table = payload["interval_table"]
    assert all(table[i][i]["sigma"] == 0 for i in range(6))
    assert table[0][5]["delta_tau"] == 5
    assert table[0][5]["sigma"] == 25
    assert table[0][5]["scale_ratio"] == 32


def test_scale_ratios_match_time_differences() -> None:
    payload = build_bridge()
    for item in payload["logarithmic_ratio_witness"]:
        assert item["scale_ratio"] == 2 ** item["delta_tau"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
