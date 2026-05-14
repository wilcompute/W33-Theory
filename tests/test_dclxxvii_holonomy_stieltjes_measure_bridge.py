from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxvii_holonomy_stieltjes_measure_bridge import build_bridge


def test_dclxxvii_summary_matches_expected_measure_shape() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["point_count"] == 40
    assert summary["atom_count"] == 2
    assert summary["dynamic_rank"] == 39



def test_dclxxvii_all_core_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())



def test_dclxxvii_measure_description_matches_closed_forms() -> None:
    payload = build_bridge()
    assert payload["measure"] == {
        "atoms": ["log(5/2)", "log(4)"],
        "weights": ["P_-", "P_+"],
        "stieltjes_transform": "R(s) = P_+/(s+log(4)) + P_-/(s+log(5/2))",
        "total_mass": "P_+ + P_- = I - J/40",
        "first_moment": "log(4) P_+ + log(5/2) P_- = G",
    }



def test_dclxxvii_derivative_samples_cover_multiple_orders() -> None:
    payload = build_bridge()
    for sample in payload["derivative_samples"].values():
        assert set(sample) == {"order_0_trace", "order_1_trace", "order_2_trace", "order_3_trace"}
