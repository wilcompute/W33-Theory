from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxviii_closure_bellman_principle_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["maximal_span"] == 5
    assert s["value_at_maximal_span"] == 5
    assert s["unique_local_minimizer"] == 1
    assert s["recursion_depth"] == 5


def test_value_function_and_policy() -> None:
    payload = build_bridge()
    vf = payload["value_function"]
    assert vf["values"] == [0, 1, 2, 3, 4, 5]
    assert [p["optimal_jump"] for p in vf["optimal_policy"]] == [1, 1, 1, 1, 1]


def test_bellman_candidates_have_unique_unit_minimizer() -> None:
    payload = build_bridge()
    for item in payload["value_function"]["bellman_witness"]:
        assert item["minimizers"] == [1]
        assert item["min_value"] == item["span"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
