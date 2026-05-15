from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxliii_nilpotent_logarithm_action_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert s["logarithm_degree"] == 5
    assert s["action_0_to_1_numerator"] == 1
    assert s["action_0_to_1_denominator"] == 2
    assert s["action_0_to_5_numerator"] == 1
    assert s["action_0_to_5_denominator"] == 160


def test_sample_action_entries() -> None:
    payload = build_bridge()
    a1 = payload["sample_actions"]["1"]
    assert a1[0][1] == {"numerator": 1, "denominator": 2}
    assert a1[0][2] == {"numerator": 1, "denominator": 8}
    assert a1[0][3] == {"numerator": 1, "denominator": 24}
    assert a1[0][5] == {"numerator": 1, "denominator": 160}


def test_formula_witness_matches_closed_form() -> None:
    payload = build_bridge()
    for item in payload["formula_witness_at_z1"]:
        assert item["entry"] == item["expected"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
