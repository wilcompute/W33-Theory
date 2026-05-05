"""Tests for PART CCCII — Delsarte LP Bound for W(3,3)"""
import pytest
from fractions import Fraction
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCCII_DELSARTE_LP_BOUND_BRIDGE import (
    V, K, K2, LAM, MU, EDGES, R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    COMPLEMENT_K, COMPLEMENT_LAM, COMPLEMENT_MU,
    COMPLEMENT_R_EIG, COMPLEMENT_S_EIG,
    HOFFMAN_BOUND_NUM, HOFFMAN_BOUND,
    CLIQUE_BOUND_RAT, CLIQUE_BOUND, ACTUAL_CLIQUE,
    COMPLEMENT_ALPHA_BOUND,
    HOFFMAN_TIGHT, CLIQUE_TIGHT,
    ALPHA_OMEGA_PRODUCT, ALPHA_OMEGA_SUM,
    PRODUCT_EQUALS_V, SUM_EQUALS_14,
    CHI_F, CHI_F_EQ_EW, CLIQUE_COVER_BOUND,
    LP_RATIO, LP_RATIO_EQ_THETA_RATIO,
    LP_SPREAD_IDENTITY,
    ALPHA_F, ALPHA_EQUALS_ALPHA_F,
    LP_CODE_RATE_BOUND,
    verify_all, build_cccii_summary,
)


class TestSRGConstants:
    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_K2(self):
        assert K2 == V - 1 - K == 27

    def test_edges(self):
        assert EDGES == V * K // 2 == 240

    def test_mult_sum(self):
        assert 1 + MULT_R + MULT_S == V

    def test_eigenvalues(self):
        assert R_EIG == 2
        assert S_EIG == -4

    def test_sm_constants(self):
        assert ALPHA == 10
        assert EW_GAUGE_4 == 4
        assert GUT_DIM == 27
        assert GENERATIONS == 3


class TestComplementParams:
    def test_complement_k(self):
        assert COMPLEMENT_K == K2 == 27

    def test_complement_s_eig(self):
        assert COMPLEMENT_S_EIG == -1 - R_EIG == -3

    def test_complement_r_eig(self):
        assert COMPLEMENT_R_EIG == -1 - S_EIG == 3

    def test_complement_lam_mu(self):
        assert COMPLEMENT_LAM == 18
        assert COMPLEMENT_MU == 18


class TestHoffmanBound:
    def test_hoffman_numerator(self):
        assert HOFFMAN_BOUND_NUM == Fraction(160, 16)

    def test_hoffman_bound_value(self):
        assert HOFFMAN_BOUND == Fraction(10)

    def test_hoffman_equals_alpha(self):
        assert HOFFMAN_BOUND == Fraction(ALPHA)

    def test_hoffman_formula(self):
        expected = Fraction(V * (-S_EIG), K - S_EIG)
        assert HOFFMAN_BOUND == expected

    def test_hoffman_tight(self):
        assert HOFFMAN_TIGHT is True


class TestCliqueBound:
    def test_clique_ratio(self):
        assert CLIQUE_BOUND_RAT == Fraction(K, -S_EIG)
        assert CLIQUE_BOUND_RAT == Fraction(3)

    def test_clique_bound_value(self):
        assert CLIQUE_BOUND == Fraction(4)

    def test_clique_bound_equals_ew(self):
        assert CLIQUE_BOUND == Fraction(EW_GAUGE_4)

    def test_clique_tight(self):
        assert CLIQUE_TIGHT is True
        assert ACTUAL_CLIQUE == 4


class TestComplementIndependence:
    def test_complement_alpha_bound(self):
        expected = Fraction(V * (-COMPLEMENT_S_EIG),
                            COMPLEMENT_K - COMPLEMENT_S_EIG)
        assert COMPLEMENT_ALPHA_BOUND == expected

    def test_complement_alpha_value(self):
        assert COMPLEMENT_ALPHA_BOUND == Fraction(4)

    def test_complement_alpha_equals_ew(self):
        assert COMPLEMENT_ALPHA_BOUND == Fraction(EW_GAUGE_4)

    def test_complement_formula_numerator(self):
        # numerator: V * (-s_bar) = 40 * 3 = 120
        assert V * (-COMPLEMENT_S_EIG) == 120

    def test_complement_formula_denominator(self):
        # denominator: k_bar - s_bar = 27 - (-3) = 30
        assert COMPLEMENT_K - COMPLEMENT_S_EIG == 30


class TestLPDuality:
    def test_product_equals_v(self):
        assert PRODUCT_EQUALS_V is True
        assert ALPHA_OMEGA_PRODUCT == Fraction(V)

    def test_sum_equals_14(self):
        assert SUM_EQUALS_14 is True
        assert ALPHA_OMEGA_SUM == Fraction(14)

    def test_lp_ratio(self):
        assert LP_RATIO == Fraction(5, 2)

    def test_lp_ratio_equals_theta_ratio(self):
        assert LP_RATIO_EQ_THETA_RATIO is True

    def test_spread_identity(self):
        assert LP_SPREAD_IDENTITY is True
        lhs = Fraction(ALPHA) * (1 + Fraction(K, MU))
        assert lhs == Fraction(V)

    def test_spread_explicit(self):
        # 10 * (1 + 12/4) = 10 * 4 = 40
        assert Fraction(ALPHA) * (1 + Fraction(K, MU)) == Fraction(40)


class TestFractionalChromatic:
    def test_chi_f_value(self):
        assert CHI_F == Fraction(4)

    def test_chi_f_equals_ew(self):
        assert CHI_F_EQ_EW is True

    def test_clique_cover_bound(self):
        assert CLIQUE_COVER_BOUND == Fraction(ALPHA)
        assert CLIQUE_COVER_BOUND == Fraction(10)

    def test_alpha_f_equals_alpha(self):
        assert ALPHA_EQUALS_ALPHA_F is True
        assert ALPHA_F == HOFFMAN_BOUND

    def test_alpha_f_value(self):
        assert ALPHA_F == Fraction(10)


class TestSMEncoding:
    def test_hoffman_sm_proxy(self):
        # Hoffman bound = ALPHA = SM fine-structure proxy
        assert int(HOFFMAN_BOUND) == ALPHA == 10

    def test_clique_ew_proxy(self):
        # Clique bound = EW gauge factor
        assert int(CLIQUE_BOUND) == EW_GAUGE_4 == 4

    def test_chi_f_ew(self):
        # Fractional chromatic = EW gauge
        assert CHI_F == Fraction(EW_GAUGE_4)

    def test_lp_code_rate(self):
        # Rate ≈ 0.557 = log2(10)/log2(40)
        import math
        expected = math.log2(ALPHA) / math.log2(V)
        assert abs(LP_CODE_RATE_BOUND - expected) < 1e-10


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total == 27

    def test_checks_list_length(self):
        checks, _, _ = verify_all()
        assert len(checks) == 27

    def test_each_check_has_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "ok" in c
            assert c["ok"] is True


class TestBuildSummary:
    def setup_method(self):
        self.s = build_cccii_summary()

    def test_part(self):
        assert self.s["part"] == "CCCII"

    def test_checks_pass(self):
        assert self.s["checks_pass"] == 27

    def test_checks_total(self):
        assert self.s["checks_total"] == 27

    def test_status(self):
        assert self.s["status"] == "PASS"

    def test_has_fields(self):
        assert "fields" in self.s

    def test_hoffman_in_fields(self):
        assert "HOFFMAN_BOUND" in self.s["fields"]
        assert self.s["fields"]["HOFFMAN_BOUND"] == "10"

    def test_clique_in_fields(self):
        assert self.s["fields"]["CLIQUE_BOUND"] == "4"

    def test_discoveries_present(self):
        assert "discoveries" in self.s
        assert len(self.s["discoveries"]) >= 5

    def test_title(self):
        assert "Delsarte" in self.s["title"]
