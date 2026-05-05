"""Tests for PART CCCI — Lovász Theta Function of W(3,3)."""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from exploration.PART_CCCI_LOVASZ_THETA_BRIDGE import (
    V, K, K2, LAM, MU, EDGES,
    R_EIG, S_EIG, MULT_R, MULT_S,
    EW_GAUGE_4, ALPHA, GUT_DIM, GENERATIONS,
    THETA_W, THETA_W_BAR, THETA_W_BAR_DIRECT,
    THETA_PRODUCT, THETA_RATIO, THETA_RATIO_SM,
    THETA_RATIO_MATCHES_SM, COUPLING_COINCIDENCE,
    COMPLEMENT_S_EIG, COMPLEMENT_R_EIG, COMPLEMENT_K,
    THETA_COMPLEMENT, INDEPENDENCE_BOUND, CAPACITY_UPPER_BOUND,
    CHI_F_LOWER_BOUND, THETA_PLUS_K, THETA_SUM, THETA_PRODUCT_V,
    SM_COUPLING_G1_PROXY, SM_COUPLING_G2_PROXY, SM_COUPLING_G3_PROXY,
    verify_all, build_ccci_summary,
)


class TestSRGConstants:
    def test_V(self):        assert V == 40
    def test_K(self):        assert K == 12
    def test_K2(self):       assert K2 == V - 1 - K
    def test_EDGES(self):    assert EDGES == V * K // 2
    def test_MULT_SUM(self): assert 1 + MULT_R + MULT_S == V


class TestThetaFormula:
    def test_theta_w_formula(self):
        assert THETA_W == Fraction(-V * S_EIG, K - S_EIG)

    def test_theta_w_equals_10(self):
        assert THETA_W == Fraction(10)

    def test_theta_w_equals_alpha(self):
        assert THETA_W == Fraction(ALPHA)

    def test_theta_w_bar_equals_4(self):
        assert THETA_W_BAR == Fraction(4)

    def test_theta_w_bar_direct(self):
        assert THETA_W_BAR_DIRECT == Fraction(4)

    def test_product_identity(self):
        assert THETA_PRODUCT == Fraction(V)

    def test_theta_w_bar_equals_ew(self):
        # ϑ(W̅) = 4 = EW_GAUGE_4
        assert THETA_W_BAR == Fraction(EW_GAUGE_4)


class TestComplementTheta:
    def test_complement_s_eig(self):
        assert COMPLEMENT_S_EIG == -3
        assert COMPLEMENT_S_EIG == -1 - R_EIG

    def test_complement_r_eig(self):
        assert COMPLEMENT_R_EIG == 3
        assert COMPLEMENT_R_EIG == -1 - S_EIG

    def test_complement_k(self):
        assert COMPLEMENT_K == K2
        assert COMPLEMENT_K == 27

    def test_theta_complement_direct(self):
        assert THETA_COMPLEMENT == Fraction(4)

    def test_theta_complement_product(self):
        assert THETA_COMPLEMENT == Fraction(V) / THETA_W


class TestRatioAndSMEncoding:
    def test_theta_ratio(self):
        assert THETA_RATIO == Fraction(5, 2)

    def test_theta_ratio_sm(self):
        assert THETA_RATIO_SM == Fraction(ALPHA, EW_GAUGE_4)

    def test_ratio_matches(self):
        assert THETA_RATIO_MATCHES_SM is True
        assert THETA_RATIO == THETA_RATIO_SM

    def test_coupling_coincidence(self):
        assert COUPLING_COINCIDENCE is True


class TestCapacityAndIndependence:
    def test_independence_bound(self):
        assert INDEPENDENCE_BOUND == Fraction(10)

    def test_capacity_upper_bound(self):
        assert CAPACITY_UPPER_BOUND == Fraction(10)

    def test_chi_f_lower_bound(self):
        assert CHI_F_LOWER_BOUND == Fraction(4)

    def test_product_identity_v(self):
        assert THETA_PRODUCT_V == Fraction(V)


class TestSumRules:
    def test_theta_plus_k(self):
        assert THETA_PLUS_K == 22

    def test_theta_sum(self):
        assert THETA_SUM == Fraction(14)

    def test_sm_coupling_g1(self):
        assert SM_COUPLING_G1_PROXY == Fraction(1, 4)

    def test_sm_coupling_g2(self):
        assert SM_COUPLING_G2_PROXY == Fraction(1, 12)

    def test_sm_coupling_g3(self):
        assert SM_COUPLING_G3_PROXY == Fraction(1, 27)

    def test_coupling_ordering(self):
        # g1 > g2 > g3  (1/4 > 1/12 > 1/27)
        assert SM_COUPLING_G1_PROXY > SM_COUPLING_G2_PROXY > SM_COUPLING_G3_PROXY


class TestVerifyAll:
    def test_returns_triple(self):
        assert len(verify_all()) == 3

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total == 27

    def test_checks_length(self):
        checks, _, _ = verify_all()
        assert len(checks) == 27

    def test_all_ok(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert c["ok"] is True

    def test_checks_have_name(self):
        checks, _, _ = verify_all()
        for c in checks:
            assert "name" in c


class TestBuildSummary:
    def test_returns_dict(self):
        assert isinstance(build_ccci_summary(), dict)

    def test_part(self):
        assert build_ccci_summary()["part"] == "CCCI"

    def test_title(self):
        title = build_ccci_summary()["title"].lower()
        assert "lovász" in title or "lovasz" in title or "theta" in title

    def test_checks_pass(self):
        assert build_ccci_summary()["checks_pass"] == 27

    def test_checks_total(self):
        assert build_ccci_summary()["checks_total"] == 27

    def test_status(self):
        assert build_ccci_summary()["status"] == "PASS"

    def test_fields_theta_w(self):
        assert build_ccci_summary()["fields"]["THETA_W"] == str(Fraction(10))

    def test_discoveries_count(self):
        assert len(build_ccci_summary()["discoveries"]) >= 10

    def test_fields_alpha(self):
        assert build_ccci_summary()["fields"]["ALPHA"] == 10
