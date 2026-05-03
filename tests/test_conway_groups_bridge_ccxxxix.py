"""
Tests for Part CCXXXIX: Conway Groups from W(3,3)
===================================================
64 tests across 10 classes.
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

from PART_CCXXXIX_CONWAY_GROUPS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    Leech_dim, kissing_Leech,
    prime_K1, prime_Kp1, prime_2K1, prime_Kh1, prime_5,
    exp_2_Co1, exp_3_Co1, exp_2_Co2, exp_3_Co2, exp_2_Co3, exp_3_Co3,
    order_Co1, order_Co2, order_Co3,
    index_Co1_Co2, orbit_stabilizer_Co1_Co2,
    checks, Verified,
)


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failures = [lbl for lbl, v in checks if not v]
        assert failures == [], failures

    def test_check_count(self):
        assert len(checks) == 32

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


class TestLeechLattice:
    def test_leech_dim(self):
        assert Leech_dim == 24

    def test_leech_dim_formula(self):
        assert Leech_dim == K * LAM

    def test_kissing_leech(self):
        assert kissing_Leech == 196560

    def test_kissing_formula(self):
        assert kissing_Leech == EDGES * Q**2 * (K // 2 + 1) * (Q**2 + Q + 1)

    def test_kissing_half(self):
        # 196560 / 2 = 98280 pairs of opposite vectors
        assert kissing_Leech // 2 == 98280

    def test_kissing_div_lam(self):
        assert kissing_Leech // LAM == 98280


class TestPrimeExpressions:
    def test_prime_K1(self):
        assert prime_K1 == 11

    def test_prime_K1_formula(self):
        assert prime_K1 == K - 1

    def test_prime_Kp1(self):
        assert prime_Kp1 == 13

    def test_prime_Kp1_formula(self):
        assert prime_Kp1 == K + 1

    def test_prime_2K1(self):
        assert prime_2K1 == 23

    def test_prime_2K1_formula(self):
        assert prime_2K1 == 2 * K - 1

    def test_prime_Kh1(self):
        assert prime_Kh1 == 7

    def test_prime_Kh1_formula(self):
        assert prime_Kh1 == K // 2 + 1

    def test_prime_5(self):
        assert prime_5 == 5

    def test_prime_5_formula(self):
        assert prime_5 == K // LAM - 1


class TestExponents:
    def test_exp_2_Co1(self):
        assert exp_2_Co1 == 21

    def test_exp_2_Co1_formula(self):
        assert exp_2_Co1 == Q * (K // 2 + 1)

    def test_exp_3_Co1(self):
        assert exp_3_Co1 == 9

    def test_exp_3_Co1_formula(self):
        assert exp_3_Co1 == Q * (K // LAM) // LAM

    def test_exp_2_Co2(self):
        assert exp_2_Co2 == 18

    def test_exp_2_Co2_formula(self):
        assert exp_2_Co2 == K + K // LAM

    def test_exp_3_Co2(self):
        assert exp_3_Co2 == 6

    def test_exp_3_Co2_formula(self):
        assert exp_3_Co2 == K // LAM

    def test_exp_2_Co3(self):
        assert exp_2_Co3 == 10

    def test_exp_2_Co3_formula(self):
        assert exp_2_Co3 == K - LAM

    def test_exp_3_Co3(self):
        assert exp_3_Co3 == 7

    def test_exp_3_Co3_formula(self):
        assert exp_3_Co3 == K // 2 + 1


class TestGroupOrders:
    def test_order_Co1_value(self):
        assert order_Co1 == 4157776806543360000

    def test_order_Co1_factored(self):
        assert 2**21 * 3**9 * 5**4 * 7**2 * 11 * 13 * 23 == order_Co1

    def test_order_Co2_value(self):
        assert order_Co2 == 42305421312000

    def test_order_Co2_factored(self):
        assert 2**18 * 3**6 * 5**3 * 7 * 11 * 23 == order_Co2

    def test_order_Co3_value(self):
        assert order_Co3 == 495766656000

    def test_order_Co3_factored(self):
        assert 2**10 * 3**7 * 5**3 * 7 * 11 * 23 == order_Co3

    def test_Co1_larger_than_Co2(self):
        assert order_Co1 > order_Co2

    def test_Co2_larger_than_Co3(self):
        assert order_Co2 > order_Co3


class TestOrbitStabilizer:
    def test_index_Co1_Co2_value(self):
        assert index_Co1_Co2 == 98280

    def test_index_Co1_Co2_formula(self):
        assert index_Co1_Co2 == kissing_Leech // LAM

    def test_orbit_stabilizer(self):
        assert orbit_stabilizer_Co1_Co2

    def test_order_Co1_div_Co2(self):
        assert order_Co1 // order_Co2 == index_Co1_Co2

    def test_Co1_Co3_index(self):
        # |Co₁|/|Co₃| = 2^(K-1) × Q^LAM × (K//LAM-1)×(K//2+1)×(K+1)
        expected = 2**(K - 1) * Q**LAM * (K // LAM - 1) * (K // 2 + 1) * (K + 1)
        assert order_Co1 // order_Co3 == expected

    def test_Co1_Co3_index_value(self):
        assert order_Co1 // order_Co3 == 2**11 * 3**2 * 5 * 7 * 13


class TestResultsJSON:
    def test_json_exists(self):
        p = ROOT / "PART_CCXXXIX_conway_groups_results.json"
        assert p.exists()

    def test_json_verified(self):
        p = ROOT / "PART_CCXXXIX_conway_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["Verified"] is True

    def test_json_checks(self):
        p = ROOT / "PART_CCXXXIX_conway_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["checks_passed"] == data["checks_total"] == 32

    def test_json_orders(self):
        p = ROOT / "PART_CCXXXIX_conway_groups_results.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        assert data["orders"]["Co1"] == 4157776806543360000
        assert data["orders"]["Co2"] == 42305421312000
        assert data["orders"]["Co3"] == 495766656000
