"""
Part CCLXVIII -- Schellekens c=24 VOAs and Conway prime triple
Regression tests for exploration/PART_CCLXVIII_SCHELLEKENS_CONWAY_BRIDGE.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from PART_CCLXVIII_SCHELLEKENS_CONWAY_BRIDGE import (
    Q, V, K, LAM, MU, F, G, EDGES,
    PHI3, PHI4, PHI6, H_0, AUT_ORDER,
    CONWAY_47, CONWAY_47_ALT,
    CONWAY_59, CONWAY_59_ALT,
    CONWAY_71, CONWAY_71_ALT,
    MONSTER_MIN_IRREP, SCHELLEKENS_COUNT,
    LEECH_KISSING, J_FIRST_COEF,
    checks, Verified,
)


# Master gates
def test_verified_true():
    assert Verified is True


def test_all_checks_pass():
    failed = [lbl for lbl, ok in checks if not ok]
    assert failed == []


def test_check_count():
    assert len(checks) == 31


# Conway prime 47
def test_47_form_a():
    assert CONWAY_47 == V + PHI6 == 47


def test_47_form_b():
    assert CONWAY_47_ALT == PHI4 * MU + PHI6 == 47


def test_47_forms_agree():
    assert CONWAY_47 == CONWAY_47_ALT == 47


def test_47_is_prime():
    for d in range(2, 8):
        assert 47 % d != 0


# Conway prime 59
def test_59_form_a():
    assert CONWAY_59 == PHI6 * LAM ** Q + Q == 59


def test_59_form_b():
    assert CONWAY_59_ALT == Q * PHI3 + LAM * PHI4 == 59


def test_59_is_prime():
    for d in range(2, 9):
        assert 59 % d != 0


# Conway prime 71
def test_71_form_a():
    assert CONWAY_71 == PHI6 * PHI4 + 1 == 71


def test_71_form_b():
    assert CONWAY_71_ALT == H_0 + 1 == 71


def test_71_is_prime():
    for d in range(2, 10):
        assert 71 % d != 0


# Schellekens link
def test_schellekens_count_71():
    # Schellekens (1993): exactly 71 holomorphic c=24 VOAs
    assert SCHELLEKENS_COUNT == 71


def test_schellekens_eq_H0_plus_1():
    assert SCHELLEKENS_COUNT == H_0 + 1
    assert SCHELLEKENS_COUNT == PHI6 * PHI4 + 1


# Monster minimal irrep
def test_monster_min_irrep_factorization():
    assert MONSTER_MIN_IRREP == 47 * 59 * 71 == 196883


def test_monster_eq_j_minus_one():
    assert MONSTER_MIN_IRREP == J_FIRST_COEF - 1


def test_monster_eq_leech_plus_correction_minus_one():
    assert MONSTER_MIN_IRREP == LEECH_KISSING + MU * Q ** MU - 1


# Leech / j-function
def test_leech_kissing():
    assert LEECH_KISSING == LAM ** MU * Q ** Q * (MU + 1) * PHI6 * PHI3
    assert LEECH_KISSING == 196560


def test_j_first_coef():
    assert J_FIRST_COEF == 196884
    assert J_FIRST_COEF == LEECH_KISSING + MU * Q ** MU


def test_correction_324():
    assert J_FIRST_COEF - LEECH_KISSING == 324
    assert MU * Q ** MU == 324


# THE DECISIVE FIND: Arithmetic progression
def test_conway_arith_progression_k():
    # 47, 59, 71 differ by exactly k = 12
    assert CONWAY_59 - CONWAY_47 == K
    assert CONWAY_71 - CONWAY_59 == K
    assert K == 12


def test_71_minus_47_eq_f():
    # 71 - 47 = 24 = f
    assert CONWAY_71 - CONWAY_47 == F


def test_three_primes_eq_q():
    # 3 Conway primes = q
    assert 3 == Q


# Hubble cross-link
def test_H0_eq_70():
    assert H_0 == 70 == PHI6 * PHI4


def test_H0_plus_1_is_71():
    assert H_0 + 1 == 71 == CONWAY_71


# JSON output
def test_json_exists():
    assert (ROOT / "PART_CCLXVIII_schellekens_conway_results.json").exists()


def test_json_verified():
    data = json.loads((ROOT / "PART_CCLXVIII_schellekens_conway_results.json").read_text(encoding="utf-8"))
    assert data["Verified"] is True
    assert data["checks_passed"] == data["checks_total"] == 31


def test_json_arith_progression():
    data = json.loads((ROOT / "PART_CCLXVIII_schellekens_conway_results.json").read_text(encoding="utf-8"))
    assert data["arithmetic_progressions"]["common_diff"] == 12


def test_json_schellekens_count():
    data = json.loads((ROOT / "PART_CCLXVIII_schellekens_conway_results.json").read_text(encoding="utf-8"))
    assert data["schellekens"]["count"] == 71
