"""Part DCCLIV -- Frobenius selection and Ouroboros loop tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccliv_frobenius_selection_and_ouroboros import (  # noqa: E402
    E_W33,
    K,
    OUT_PATH,
    Q,
    V,
    build_bridge,
    cascade_consistency_check,
    frobenius_count,
    frobenius_selection_scan,
    frobenius_selection_solution,
    one_ninety_two_identifications,
    ouroboros_loop,
    stabilizer_cascade,
    twenty_four_identifications,
    write_bridge,
)


def test_frobenius_at_q_3_is_240():
    assert frobenius_count(3) == 240 == E_W33


def test_frobenius_at_q_2_is_30():
    assert frobenius_count(2) == 30


def test_frobenius_selection_unique_at_q_3():
    scan = frobenius_selection_scan(11)
    matches = [r["q"] for r in scan if r["match"]]
    assert matches == [3]


def test_frobenius_solution_returns_q_3():
    sol = frobenius_selection_solution()
    assert "q = 3" in sol["solution"]
    assert sol["match_E_W33"] is True
    assert sol["match_E8_roots"] is True


def test_stabilizer_cascade_5_steps():
    cascade = stabilizer_cascade()
    assert len(cascade) == 5


def test_W_E6_order_51840():
    cascade = stabilizer_cascade()
    assert cascade[0]["name"] == "W(E_6)"
    assert cascade[0]["order"] == 51840


def test_final_stabiliser_192():
    cascade = stabilizer_cascade()
    final = cascade[-1]
    assert final["order"] == 192
    assert "W(D_4)" in final["name"] or "Aut(C_2 x Q_8)" in final["name"]


def test_cascade_orders_descending():
    cascade = stabilizer_cascade()
    for i in range(len(cascade) - 1):
        assert cascade[i]["order"] > cascade[i + 1]["order"]


def test_cascade_divisors_consistent():
    check = cascade_consistency_check()
    assert check["all_divisors_consistent"] is True


def test_ouroboros_loop_closes_at_Q_8():
    loop = ouroboros_loop()
    assert "Q_8" in loop[-1]["to"]
    assert loop[0]["from"] == "Q_8"


def test_ouroboros_has_7_steps():
    loop = ouroboros_loop()
    assert len(loop) == 7


def test_24_identifications_all_equal_24():
    items = twenty_four_identifications()
    for r in items:
        assert r["value"] == 24


def test_192_identifications_all_equal_192():
    items = one_ninety_two_identifications()
    for r in items:
        assert r["value"] == 192


def test_24_eq_S_4():
    assert 24 == math.factorial(4)


def test_192_eq_8_times_24():
    assert 192 == 8 * 24


def test_192_eq_24_plus_84_plus_84():
    """Tomotope flag count from DCCXXV."""
    assert 192 == 24 + 84 + 84


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Frobenius Selection" in b["theorem"]
    assert "q^5 - q" in b["one_line"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "frobenius_selection_principle",
        "stabilizer_cascade",
        "cascade_consistency_check",
        "ouroboros_loop",
        "twenty_four_identifications",
        "one_ninety_two_identifications",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
