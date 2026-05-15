from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlv_nilpotent_hessian_convexity_bridge import build_bridge


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]
    assert s["state_count"] == 6
    assert s["hessian_0_to_2_numerator"] == 1
    assert s["hessian_0_to_2_denominator"] == 4
    assert s["hessian_0_to_5_numerator"] == 1
    assert s["hessian_0_to_5_denominator"] == 8
    assert s["trace_hessian"] == 0


def test_sample_hessian_entries() -> None:
    payload = build_bridge()
    h1 = payload["sample_hessians"]["1"]
    assert h1[0][0] == {"numerator": 0, "denominator": 1}
    assert h1[0][1] == {"numerator": 0, "denominator": 1}
    assert h1[0][2] == {"numerator": 1, "denominator": 4}
    assert h1[0][3] == {"numerator": 1, "denominator": 4}
    assert h1[0][5] == {"numerator": 1, "denominator": 8}


def test_formula_witness_matches_closed_form() -> None:
    payload = build_bridge()
    for item in payload["formula_witness_at_z1"]:
        assert item["entry"] == item["expected"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
