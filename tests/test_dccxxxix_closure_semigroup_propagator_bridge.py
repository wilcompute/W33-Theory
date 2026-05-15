from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxix_closure_semigroup_propagator_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["causal_class_count"] == 6
    assert s["maximal_value"] == 5
    assert s["minimal_propagator_numerator"] == 1
    assert s["minimal_propagator_denominator"] == 32


def test_value_and_propagator_tables() -> None:
    payload = build_bridge()
    values = payload["value_table"]
    props = payload["propagator_table"]
    assert values[0][5] == 5
    assert props[0][5] == {"numerator": 1, "denominator": 32}
    assert values[2][4] == 2
    assert props[2][4] == {"numerator": 1, "denominator": 4}


def test_every_midpoint_saturates_semigroup_identity() -> None:
    payload = build_bridge()
    for witness in payload["semigroup_witness"]:
        target_value = witness["target_value"]
        target_prop = witness["target_propagator"]
        for candidate in witness["candidates"]:
            assert candidate["value_sum"] == target_value
            assert candidate["propagator_product"] == target_prop


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
