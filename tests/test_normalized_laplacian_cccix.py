"""Tests for PART CCCIX — Normalized Laplacian Spectrum of W(3,3)"""
import pytest
from fractions import Fraction
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCIX_NORMALIZED_LAPLACIAN_BRIDGE import (
    V, K, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    ALPHA, GENERATIONS, EW_GAUGE_4,
    NL_EIG_0, NL_EIG_1, NL_EIG_2,
    NL_MULT_0, NL_MULT_1, NL_MULT_2, NL_MULT_SUM,
    NL_TRACE, NL_TRACE_EQ_V,
    NL_TRACE_SQ, NL_TRACE_SQ_EQ,
    NL_LARGEST, NL_LARGEST_LT_2,
    NL_GAP, NL_GAP_EQ,
    NL_DIFF_21, NL_DIFF_21_SM,
    NL_EIG1_NUM, NL_EIG1_DEN, NL_EIG1_NUM_SM, NL_EIG1_DEN_SM,
    NL_EIG2_NUM, NL_EIG2_DEN, NL_EIG2_NUM_SM, NL_EIG2_DEN_SM,
    NL_SUM_12, NL_SUM_12_SM,
    NL_PROD_12, NL_PROD_12_SM,
    NL_TRACE_SM, NL_FIEDLER_SM,
    NL_CHEEGER_LB, NL_CHEEGER_LB_NUM_SM,
    NL_ORDERING, NL_MULTS_SUM_EQ_V,
    verify_all, build_cccix_summary,
)


class TestSRGConstants:
    def test_V_K(self):
        assert V == 40 and K == 12

    def test_edges(self):
        assert EDGES == 240

    def test_adj_eigs(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_mults(self):
        assert MULT_R == 24 and MULT_S == 15

    def test_sm_constants(self):
        assert ALPHA == 10 and MU == 4 and GENERATIONS == 3


class TestNormalizedLaplacianEigenvalues:
    def test_eig0_zero(self):
        assert NL_EIG_0 == Fraction(0)

    def test_eig1_exact(self):
        assert NL_EIG_1 == Fraction(5, 6)

    def test_eig2_exact(self):
        assert NL_EIG_2 == Fraction(4, 3)

    def test_eig1_formula(self):
        assert NL_EIG_1 == 1 - Fraction(R_EIG, K)

    def test_eig2_formula(self):
        assert NL_EIG_2 == 1 - Fraction(S_EIG, K)

    def test_mult_sum(self):
        assert NL_MULTS_SUM_EQ_V is True
        assert NL_MULT_SUM == V

    def test_ordering(self):
        assert NL_ORDERING is True
        assert NL_EIG_0 < NL_EIG_1 < 1 < NL_EIG_2 < 2


class TestSpectralIdentities:
    def test_trace_eq_V(self):
        assert NL_TRACE_EQ_V is True
        assert NL_TRACE == V

    def test_trace_sq_eq(self):
        assert NL_TRACE_SQ_EQ is True

    def test_trace_sq_exact(self):
        assert NL_TRACE_SQ == Fraction(130, 3)

    def test_largest_lt_2(self):
        assert NL_LARGEST_LT_2 is True
        assert NL_LARGEST == Fraction(4, 3)

    def test_gap_exact(self):
        assert NL_GAP_EQ is True
        assert NL_GAP == Fraction(5, 6)

    def test_diff_21(self):
        assert NL_DIFF_21_SM is True
        assert NL_DIFF_21 == Fraction(1, 2)


class TestSMEncodings:
    def test_eig1_num_sm(self):
        assert NL_EIG1_NUM_SM is True
        assert NL_EIG1_NUM == MU + 1

    def test_eig1_den_sm(self):
        assert NL_EIG1_DEN_SM is True
        assert NL_EIG1_DEN == K // 2

    def test_eig2_num_sm(self):
        assert NL_EIG2_NUM_SM is True
        assert NL_EIG2_NUM == MU

    def test_eig2_den_sm(self):
        assert NL_EIG2_DEN_SM is True
        assert NL_EIG2_DEN == GENERATIONS

    def test_sum12_sm(self):
        assert NL_SUM_12_SM is True
        assert NL_SUM_12 == Fraction(13, 6)
        assert NL_SUM_12.numerator == ALPHA + GENERATIONS
        assert NL_SUM_12.denominator == K // 2

    def test_prod12_sm(self):
        assert NL_PROD_12_SM is True
        assert NL_PROD_12 == Fraction(10, 9)
        assert NL_PROD_12.numerator == ALPHA


class TestAlgebraicCheeger:
    def test_trace_sm(self):
        assert NL_TRACE_SM is True
        assert NL_TRACE == V
        assert V == ALPHA * EW_GAUGE_4

    def test_fiedler_sm(self):
        assert NL_FIEDLER_SM is True
        assert 6 * NL_EIG_1 == MU + 1

    def test_cheeger_lb_sm(self):
        assert NL_CHEEGER_LB_NUM_SM is True
        assert NL_CHEEGER_LB == Fraction(5, 12)
        assert NL_CHEEGER_LB.numerator == MU + 1
        assert NL_CHEEGER_LB.denominator == K


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total == 27

    def test_each_check_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert c["ok"] is True, f"Failed: {c['name']}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_cccix_summary()

    def test_part(self):
        assert self.s["part"] == "CCCIX"

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_checks(self):
        assert self.s["checks_pass"] == 27
        assert self.s["checks_total"] == 27

    def test_title(self):
        assert "Normalized" in self.s["title"]

    def test_fields(self):
        f = self.s["fields"]
        assert f["NL_EIG_1"] == "5/6"
        assert f["NL_EIG_2"] == "4/3"
        assert f["NL_TRACE_SQ"] == "130/3"

    def test_discoveries(self):
        assert len(self.s["discoveries"]) >= 5
