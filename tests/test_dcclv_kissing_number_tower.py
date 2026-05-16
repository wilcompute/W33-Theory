"""Part DCCLV -- Kissing-number tower tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclv_kissing_number_tower import (  # noqa: E402
    E_W33,
    F_EIGEN,
    K,
    KNOWN_KISSING,
    LAM,
    OUT_PATH,
    PHI3,
    PHI4,
    PHI6,
    Q,
    build_bridge,
    kissing_w33_table,
    w33_factorisations,
    write_bridge,
)


def test_six_solved_dimensions():
    assert set(KNOWN_KISSING.keys()) == {1, 2, 3, 4, 8, 24}


def test_K_1_eq_lambda():
    assert KNOWN_KISSING[1]["K"] == 2 == LAM


def test_K_2_eq_q_factorial():
    assert KNOWN_KISSING[2]["K"] == 6 == math.factorial(Q)


def test_K_3_eq_codec():
    assert KNOWN_KISSING[3]["K"] == 12 == K


def test_K_4_eq_f_eigen():
    assert KNOWN_KISSING[4]["K"] == 24 == F_EIGEN


def test_K_8_eq_E_W33():
    assert KNOWN_KISSING[8]["K"] == 240 == E_W33


def test_K_24_eq_leech_kissing():
    leech = E_W33 * Q ** 2 * PHI6 * PHI3
    assert KNOWN_KISSING[24]["K"] == 196560 == leech


def test_dim_3_eq_q():
    assert 3 == Q


def test_dim_4_eq_q_plus_1():
    assert 4 == Q + 1


def test_dim_8_eq_2_to_q():
    assert 8 == 2 ** Q


def test_dim_24_eq_f_eigen():
    assert 24 == F_EIGEN


def test_dim_2_eq_lambda():
    assert 2 == LAM


def test_w33_factorisations_all_pass():
    fact = w33_factorisations()
    for name, val in fact.items():
        assert val is True, f"factorisation {name} failed"


def test_kissing_table_has_6_rows():
    assert len(kissing_w33_table()) == 6


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Kissing-Number Tower" in b["theorem"]
    assert "196560" in b["one_line"]


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
        "known_kissing_dimensions",
        "kissing_w33_table",
        "w33_factorisations",
        "kissing_growth_ratios",
        "E8_and_Leech_interpretation",
        "viazovska_sphere_packing",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
