from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxli_closure_resolvent_kernel_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert s["truncation_degree"] == 5
    assert s["response_0_to_5_numerator"] == 1
    assert s["response_0_to_5_denominator"] == 32
    assert s["row0_sum_at_z1_numerator"] == 63
    assert s["row0_sum_at_z1_denominator"] == 32


def test_sample_resolvent_entries() -> None:
    payload = build_bridge()
    r1 = payload["sample_resolvents"]["1"]
    assert r1[0][0] == {"numerator": 1, "denominator": 1}
    assert r1[0][1] == {"numerator": 1, "denominator": 2}
    assert r1[0][2] == {"numerator": 1, "denominator": 4}
    assert r1[0][5] == {"numerator": 1, "denominator": 32}
    r2 = payload["sample_resolvents"]["2"]
    assert r2[0][5] == {"numerator": 1, "denominator": 1}


def test_formula_witness_matches_closed_form() -> None:
    payload = build_bridge()
    for item in payload["formula_witness_at_z1"]:
        assert item["entry"] == item["expected"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
