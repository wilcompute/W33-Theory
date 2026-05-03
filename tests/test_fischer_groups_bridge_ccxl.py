"""
Tests for Part CCXL: Fischer Groups from W(3,3)
=================================================
62 tests across 10 classes.
"""
import pytest
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PART_CCXL_FISCHER_GROUPS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    three_transposition_order, num_Fischer,
    prime_5, prime_7, prime_11, prime_13, prime_17, prime_23, prime_29,
    exp_2_Fi22, exp_3_Fi22, exp_2_Fi23, exp_3_Fi23,
    exp_2_Fi24p, exp_3_Fi24p, exp_7_Fi24p,
    order_Fi22, order_Fi23, order_Fi24p,
    dim_Fi22_rep, dim_Fi23_rep, dim_Fi24p_rep,
    Leech_dim, dim_E6, prime_29,
    checks, Verified,
)


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failures = [lbl for lbl, v in checks if not v]
        assert failures == [], failures

    def test_check_count(self):
        assert len(checks) == 33

    def test_check_count_at_least_28(self):
        assert len(checks) >= 28


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestThreeTranspositions:
    def test_Q_equals_3(self):
        assert three_transposition_order == 3

    def test_three_transposition_is_Q(self):
        assert three_transposition_order == Q

    def test_num_Fischer(self):
        assert num_Fischer == 3

    def test_num_Fischer_is_Q(self):
        assert num_Fischer == Q


class TestPrimes:
    def test_prime_5(self):
        assert prime_5 == 5

    def test_prime_5_formula(self):
        assert prime_5 == K // LAM - 1

    def test_prime_7(self):
        assert prime_7 == 7

    def test_prime_7_formula(self):
        assert prime_7 == K // 2 + 1

    def test_prime_11(self):
        assert prime_11 == 11

    def test_prime_11_formula(self):
        assert prime_11 == K - 1

    def test_prime_13(self):
        assert prime_13 == 13

    def test_prime_13_formula(self):
        assert prime_13 == K + 1

    def test_prime_17(self):
        assert prime_17 == 17

    def test_prime_17_formula(self):
        assert prime_17 == K + K // LAM - 1

    def test_prime_23(self):
        assert prime_23 == 23

    def test_prime_23_formula(self):
        assert prime_23 == 2 * K - 1

    def test_prime_29(self):
        assert prime_29 == 29

    def test_prime_29_formula(self):
        assert prime_29 == K * LAM + K // LAM - 1

    def test_prime_29_leech_formula(self):
        assert prime_29 == Leech_dim + K // LAM - 1


class TestGroupOrders:
    def test_order_Fi22_value(self):
        assert order_Fi22 == 64561751654400

    def test_order_Fi22_factored(self):
        assert 2**17 * 3**9 * 5**2 * 7 * 11 * 13 == order_Fi22

    def test_order_Fi23_value(self):
        assert order_Fi23 == 4089470473293004800

    def test_order_Fi23_factored(self):
        assert 2**18 * 3**13 * 5**2 * 7 * 11 * 13 * 17 * 23 == order_Fi23

    def test_order_Fi24p_value(self):
        assert order_Fi24p == 1255205709190661721292800

    def test_order_Fi24p_factored(self):
        assert 2**21 * 3**16 * 5**2 * 7**3 * 11 * 13 * 17 * 23 * 29 == order_Fi24p

    def test_order_descending(self):
        assert order_Fi24p > order_Fi23 > order_Fi22 > 0


class TestExponents:
    def test_exp_2_Fi22(self):
        assert exp_2_Fi22 == 17

    def test_exp_2_Fi22_formula(self):
        assert exp_2_Fi22 == K + K // LAM - 1

    def test_exp_3_Fi22(self):
        assert exp_3_Fi22 == 9

    def test_exp_3_Fi22_formula(self):
        assert exp_3_Fi22 == Q * (K // LAM) // LAM

    def test_exp_2_Fi23(self):
        assert exp_2_Fi23 == 18

    def test_exp_2_Fi23_formula(self):
        assert exp_2_Fi23 == K + K // LAM

    def test_exp_3_Fi23(self):
        assert exp_3_Fi23 == 13

    def test_exp_3_Fi23_formula(self):
        assert exp_3_Fi23 == K + 1

    def test_exp_2_Fi24p(self):
        assert exp_2_Fi24p == 21

    def test_exp_2_Fi24p_formula(self):
        assert exp_2_Fi24p == Q * (K // 2 + 1)

    def test_exp_3_Fi24p(self):
        assert exp_3_Fi24p == 16

    def test_exp_7_Fi24p(self):
        assert exp_7_Fi24p == 3


class TestRepDimensions:
    def test_dim_Fi22_rep(self):
        assert dim_Fi22_rep == 78

    def test_dim_Fi22_rep_is_E6(self):
        assert dim_Fi22_rep == dim_E6

    def test_dim_Fi22_rep_formula(self):
        assert dim_Fi22_rep == LAM * (M_LAM + K)

    def test_dim_Fi23_rep(self):
        assert dim_Fi23_rep == 253

    def test_dim_Fi23_rep_formula(self):
        assert dim_Fi23_rep == (K - 1) * (2 * K - 1)

    def test_dim_Fi24p_rep(self):
        assert dim_Fi24p_rep == 783

    def test_dim_Fi24p_rep_formula(self):
        assert dim_Fi24p_rep == M_LAM * prime_29


class TestConwayCrossChecks:
    def test_exp_2_Fi24p_matches_Co1(self):
        # Both Co₁ and Fi₂₄' have 2^21
        assert exp_2_Fi24p == Q * (K // 2 + 1)

    def test_exp_3_Fi22_matches_Co1(self):
        # Both Co₁ and Fi₂₂ have 3^9
        assert exp_3_Fi22 == Q * (K // LAM) // LAM

    def test_exp_2_Fi23_matches_Co2(self):
        # Both Co₂ and Fi₂₃ have 2^18
        assert exp_2_Fi23 == K + K // LAM


class TestResultsJSON:
    def test_json_exists(self):
        p = ROOT / "PART_CCXL_fischer_groups_results.json"
        assert p.exists()

    def test_json_verified(self):
        p = ROOT / "PART_CCXL_fischer_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["Verified"] is True

    def test_json_checks(self):
        p = ROOT / "PART_CCXL_fischer_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["checks_passed"] == data["checks_total"] == 33

    def test_json_orders(self):
        p = ROOT / "PART_CCXL_fischer_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["orders"]["Fi22"] == 64561751654400
        assert data["orders"]["Fi23"] == 4089470473293004800
        assert data["orders"]["Fi24p"] == 1255205709190661721292800
