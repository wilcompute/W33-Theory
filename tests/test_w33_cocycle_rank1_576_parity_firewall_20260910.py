from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_cocycle_rank1_576_parity_firewall import build_result  # noqa: E402


def test_cocycle_support_firewall_and_D8_core() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())

    support = data["support_geometry"]
    assert support["quotient_size"] == 48
    assert support["ordered_pair_count"] == 2304
    assert support["twisted_pairs"] == 576
    assert support["untwisted_pairs"] == 1728
    assert support["factorization"] == "576=24^2; 1728=3*576"

    firewall = data["parity_firewall"]
    assert firewall["A4_size"] == 12
    assert firewall["C2_times_A4_size"] == 24

    core = data["abelianization_core"]
    assert core["matrix_in_basis_b_sign"] == [[0, 1], [1, 0]]
    assert core["nondegenerate"] is True
    assert core["central_lift_isomorphism"] == "D8"
    assert core["central_lift_order_histogram"] == {"1": 1, "2": 5, "4": 2}
