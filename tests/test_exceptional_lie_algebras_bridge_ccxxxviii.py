"""
Tests for Part CCXXXVIII — Exceptional Lie Algebras Tower from W(3,3)
SRG(40,12,2,4) constants.

~65 tests across 10 classes.
"""

import json
from pathlib import Path
import pytest

from PART_CCXXXVIII_EXCEPTIONAL_LIE_ALGEBRAS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, EDGES, AUT_ORDER,
    num_exceptional,
    dim_G2, dim_F4, dim_E6, dim_E7, dim_E8,
    roots_G2, roots_F4, roots_E6, roots_E7, roots_E8,
    rank_G2, rank_F4, rank_E6, rank_E7, rank_E8,
    rank_sum_G2_F4_E6,
    Albert_dim, Albert_matrix_size, Albert_dim_from_Q, E6_min_rep,
    diff_F4_G2, diff_E6_F4, diff_E7_E6, diff_E8_E7,
    checks, Verified,
)

ROOT = Path(__file__).resolve().parents[1]


class TestBridgeMetadata:
    def test_verified_true(self):
        assert Verified is True

    def test_all_checks_pass(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_check_count_at_least_30(self):
        assert len(checks) >= 30

    def test_json_exists(self):
        assert (ROOT / "PART_CCXXXVIII_exceptional_lie_algebras_results.json").exists()

    def test_json_verified(self):
        d = json.loads(
            (ROOT / "PART_CCXXXVIII_exceptional_lie_algebras_results.json").read_text(encoding="utf-8")
        )
        assert d["Verified"] is True

    def test_json_checks_equal(self):
        d = json.loads(
            (ROOT / "PART_CCXXXVIII_exceptional_lie_algebras_results.json").read_text(encoding="utf-8")
        )
        assert d["checks_passed"] == d["checks_total"]


class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_EDGES(self):
        assert EDGES == 240

    def test_M_LAM(self):
        assert M_LAM == 27


class TestExceptionalCount:
    def test_num_exceptional_value(self):
        assert num_exceptional == 5

    def test_num_exceptional_eq_K_div_LAM_minus_1(self):
        assert num_exceptional == K // LAM - 1


class TestDimensions:
    def test_dim_G2_value(self):
        assert dim_G2 == 14

    def test_dim_G2_formula(self):
        assert dim_G2 == K + LAM

    def test_dim_F4_value(self):
        assert dim_F4 == 52

    def test_dim_F4_formula(self):
        assert dim_F4 == V + K

    def test_dim_E6_value(self):
        assert dim_E6 == 78

    def test_dim_E6_formula(self):
        assert dim_E6 == LAM * (M_LAM + K)

    def test_dim_E7_value(self):
        assert dim_E7 == 133

    def test_dim_E7_formula(self):
        assert dim_E7 == K * (K - 1) + 1

    def test_dim_E8_value(self):
        assert dim_E8 == 248

    def test_dim_E8_formula(self):
        assert dim_E8 == EDGES + 2 * MU


class TestRootCounts:
    def test_roots_G2_value(self):
        assert roots_G2 == 12

    def test_roots_G2_eq_K(self):
        assert roots_G2 == K

    def test_roots_F4_value(self):
        assert roots_F4 == 48

    def test_roots_F4_formula(self):
        assert roots_F4 == EDGES // (K // LAM - 1)

    def test_roots_E6_value(self):
        assert roots_E6 == 72

    def test_roots_E6_formula(self):
        assert roots_E6 == K * (K // 2)

    def test_roots_E7_value(self):
        assert roots_E7 == 126

    def test_roots_E7_formula(self):
        assert roots_E7 == V * Q + MU + LAM

    def test_roots_E8_value(self):
        assert roots_E8 == 240

    def test_roots_E8_eq_EDGES(self):
        assert roots_E8 == EDGES


class TestRanks:
    def test_rank_G2_value(self):
        assert rank_G2 == 2

    def test_rank_G2_eq_LAM(self):
        assert rank_G2 == LAM

    def test_rank_F4_value(self):
        assert rank_F4 == 4

    def test_rank_F4_eq_MU(self):
        assert rank_F4 == MU

    def test_rank_E6_value(self):
        assert rank_E6 == 6

    def test_rank_E6_eq_K_div_LAM(self):
        assert rank_E6 == K // LAM

    def test_rank_E7_value(self):
        assert rank_E7 == 7

    def test_rank_E7_eq_K_half_plus_1(self):
        assert rank_E7 == K // 2 + 1

    def test_rank_E8_value(self):
        assert rank_E8 == 8

    def test_rank_E8_eq_2_MU(self):
        assert rank_E8 == 2 * MU

    def test_rank_sum_G2_F4_E6_eq_K(self):
        assert rank_sum_G2_F4_E6 == K

    def test_LAM_plus_MU_plus_K_div_LAM_eq_K(self):
        assert LAM + MU + K // LAM == K

    def test_rank_E6_eq_rank_G2_plus_rank_F4(self):
        assert rank_E6 == rank_G2 + rank_F4


class TestAlbertAlgebra:
    def test_Albert_dim_value(self):
        assert Albert_dim == 27

    def test_Albert_dim_eq_M_LAM(self):
        assert Albert_dim == M_LAM

    def test_Albert_dim_eq_Q_cubed(self):
        assert Albert_dim_from_Q == Q**3

    def test_Q_cubed_eq_27(self):
        assert Q**3 == 27

    def test_Albert_matrix_size_eq_Q(self):
        assert Albert_matrix_size == Q

    def test_E6_min_rep_eq_27(self):
        assert E6_min_rep == 27

    def test_E6_min_rep_eq_M_LAM(self):
        assert E6_min_rep == M_LAM


class TestDimDifferences:
    def test_diff_F4_G2_eq_V_minus_LAM(self):
        assert diff_F4_G2 == V - LAM

    def test_diff_F4_G2_value(self):
        assert diff_F4_G2 == 38

    def test_diff_E6_F4_eq_26(self):
        assert diff_E6_F4 == 26

    def test_diff_E6_F4_eq_V_minus_K_minus_LAM(self):
        assert diff_E6_F4 == V - K - LAM

    def test_diff_E7_E6_formula(self):
        assert diff_E7_E6 == (K // LAM - 1) * (K - 1)

    def test_diff_E7_E6_value(self):
        assert diff_E7_E6 == 55

    def test_diff_E8_E7_formula(self):
        assert diff_E8_E7 == (K // LAM - 1) * (2 * K - 1)

    def test_diff_E8_E7_value(self):
        assert diff_E8_E7 == 115

    def test_roots_E6_eq_K_times_rank_E6(self):
        assert roots_E6 == K * rank_E6
