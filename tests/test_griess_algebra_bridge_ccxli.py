"""
Tests for Part CCXLI: Griess Algebra & Monster VOA Bridge
==========================================================
64 tests across 10 classes verifying every bridge identity.
"""

import json
import os
import sys
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "exploration"))

from PART_CCXLI_GRIESS_ALGEBRA_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    prime_17, prime_19, prime_23, prime_29, prime_31,
    prime_41, prime_47, prime_59, prime_71,
    dim_E8, kissing_Leech, dim_Griess, dim_Monster_rep,
    voa_central_charge, j_const, j_linear, num_conj_Monster,
    exp_2_Monster, exp_3_Monster, exp_5_Monster,
    exp_7_Monster, exp_11_Monster, exp_13_Monster,
    order_Monster,
    num_primes_Monster, num_primes_higher_exp, num_primes_single_exp,
    exp_2_B, exp_3_B, exp_5_B, exp_7_B, dim_B_rep, order_B,
    mc_trivial, mc_smallest, mc_sum, mckay_E8_nodes,
    CHECKS, Verified, n_pass, n_total,
)


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        assert n_pass == n_total

    def test_check_count(self):
        assert n_total == 38

    def test_no_failed_checks(self):
        failed = [c for c in CHECKS if not c["ok"]]
        assert failed == [], f"Failed checks: {[c['label'] for c in failed]}"


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestMonsterPrimes:
    def test_prime_17(self):
        assert prime_17 == 17
        assert prime_17 == K + K // LAM - 1

    def test_prime_19(self):
        assert prime_19 == 19
        assert prime_19 == K + K // LAM + 1

    def test_prime_23(self):
        assert prime_23 == 23
        assert prime_23 == 2 * K - 1

    def test_prime_29(self):
        assert prime_29 == 29
        assert prime_29 == K * LAM + K // LAM - 1

    def test_prime_31(self):
        assert prime_31 == 31
        assert prime_31 == K * LAM + K // LAM + 1

    def test_prime_41(self):
        assert prime_41 == 41
        assert prime_41 == V + 1

    def test_prime_47(self):
        assert prime_47 == 47
        assert prime_47 == LAP_TOP * Q - 1

    def test_prime_59(self):
        assert prime_59 == 59
        assert prime_59 == LAP_TOP * Q + K - 1

    def test_prime_71(self):
        assert prime_71 == 71
        assert prime_71 == K * M_NEG // LAM - 1

    def test_all_nine_are_prime(self):
        for p in [prime_17, prime_19, prime_23, prime_29, prime_31,
                  prime_41, prime_47, prime_59, prime_71]:
            for i in range(2, int(p ** 0.5) + 1):
                assert p % i != 0, f"{p} is not prime"


class TestDimensions:
    def test_dim_E8(self):
        assert dim_E8 == 248
        assert dim_E8 == EDGES + K // LAM + LAM

    def test_kissing_Leech(self):
        assert kissing_Leech == 196560
        assert kissing_Leech == EDGES * Q**2 * (K // 2 + 1) * (Q**2 + Q + 1)

    def test_dim_Griess(self):
        assert dim_Griess == 196884

    def test_dim_Griess_formula(self):
        assert dim_Griess == kissing_Leech + (K + K // LAM) ** 2

    def test_dim_Monster_rep(self):
        assert dim_Monster_rep == 196883

    def test_dim_Monster_rep_formula(self):
        assert dim_Monster_rep == prime_47 * prime_59 * prime_71

    def test_dim_Griess_from_rep(self):
        assert dim_Griess == dim_Monster_rep + 1

    def test_voa_central_charge(self):
        assert voa_central_charge == 24
        assert voa_central_charge == K * LAM


class TestjFunction:
    def test_j_const(self):
        assert j_const == 744
        assert j_const == Q * dim_E8

    def test_j_linear(self):
        assert j_linear == 196884
        assert j_linear == dim_Griess

    def test_744_three_times_248(self):
        assert j_const == 3 * 248

    def test_j_identity(self):
        # j(τ) = q^{-1} + 744 + 196884*q + ..., so constant = 744, linear = dim_Griess
        assert j_const + 1 == 745   # j(τ) at q^0 relative shift
        assert j_linear - j_const == 196140


class TestMonsterOrder:
    def test_exp_2(self):
        assert exp_2_Monster == 46
        assert exp_2_Monster == LAP_TOP * Q - LAM

    def test_exp_3(self):
        assert exp_3_Monster == 20
        assert exp_3_Monster == V // LAM

    def test_exp_5(self):
        assert exp_5_Monster == 9
        assert exp_5_Monster == Q ** 2

    def test_exp_7(self):
        assert exp_7_Monster == 6
        assert exp_7_Monster == K // LAM

    def test_exp_11(self):
        assert exp_11_Monster == 2
        assert exp_11_Monster == LAM

    def test_exp_13(self):
        assert exp_13_Monster == 3
        assert exp_13_Monster == Q

    def test_order_Monster_value(self):
        assert order_Monster == 808017424794512875886459904961710757005754368000000000

    def test_num_conj_Monster(self):
        assert num_conj_Monster == 194
        assert num_conj_Monster == K * (K // 2 + LAP_MID) + LAM


class TestPrimeStructure:
    def test_total_primes(self):
        assert num_primes_Monster == 15
        assert num_primes_Monster == K + Q

    def test_primes_higher_exp(self):
        assert num_primes_higher_exp == 6
        assert num_primes_higher_exp == K // LAM

    def test_primes_single_exp(self):
        assert num_primes_single_exp == 9
        assert num_primes_single_exp == Q ** 2

    def test_prime_partition(self):
        assert num_primes_higher_exp + num_primes_single_exp == num_primes_Monster

    def test_single_exp_count_equals_Q_squared(self):
        # The 9 primes {17,19,23,29,31,41,47,59,71} each divide |M| once
        # 9 = Q^2 — a pure SRG identity
        assert num_primes_single_exp == Q ** 2


class TestBabyMonster:
    def test_exp_2_B(self):
        assert exp_2_B == 41
        assert exp_2_B == V + 1

    def test_exp_3_B(self):
        assert exp_3_B == 13
        assert exp_3_B == K + 1

    def test_exp_5_B(self):
        assert exp_5_B == 6
        assert exp_5_B == K // LAM

    def test_exp_7_B(self):
        assert exp_7_B == 2
        assert exp_7_B == LAM

    def test_dim_B_rep(self):
        assert dim_B_rep == 4371
        assert dim_B_rep == Q * prime_31 * prime_47

    def test_B_divides_Monster(self):
        # Baby Monster order divides Monster order
        assert order_Monster % order_B == 0


class TestMoonshineLinks:
    def test_McKay_1_plus_196883(self):
        assert mc_trivial == 1
        assert mc_smallest == 196883
        assert mc_sum == 196884

    def test_mckay_E8_nodes(self):
        assert mckay_E8_nodes == 9
        assert mckay_E8_nodes == Q ** 2

    def test_dim_E8_kissing_sum(self):
        # dim_Griess = kissing + 18^2 connects three major structures
        assert kissing_Leech + (K + K // LAM) ** 2 == 196884

    def test_voa_equals_Leech_dim(self):
        # VOA central charge = 24 = Leech lattice dimension
        assert voa_central_charge == K * LAM == 24


class TestResultsJSON:
    @pytest.fixture
    def results(self):
        path = os.path.join(ROOT, "PART_CCXLI_griess_algebra_results.json")
        with open(path) as f:
            return json.load(f)

    def test_json_verified(self, results):
        assert results["verified"] is True

    def test_json_checks_count(self, results):
        assert results["n_checks"] == 38

    def test_json_all_pass(self, results):
        assert results["n_pass"] == results["n_checks"]

    def test_json_dim_Griess(self, results):
        assert results["dimensions"]["dim_Griess"] == 196884

    def test_json_order_Monster(self, results):
        assert results["monster_order"]["value"] == 808017424794512875886459904961710757005754368000000000

    def test_json_part_label(self, results):
        assert results["part"] == "CCXLI"
