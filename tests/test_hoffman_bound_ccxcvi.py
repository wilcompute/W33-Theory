"""
Tests for Part CCXCVI: Hoffman Ratio Bound for W(3,3).
"""

from fractions import Fraction
import pytest
from exploration.PART_CCXCVI_HOFFMAN_BOUND_BRIDGE import (
    V, K, LAM, MU, K2, EDGES, MULT_R, MULT_S,
    R_EIG, S_EIG,
    EW_GAUGE_4, QUARKS_36, Q,
    LAMBDA_MIN, ABS_LAMBDA_MIN,
    HOFFMAN_NUMER, HOFFMAN_DENOM, HOFFMAN_BOUND,
    ALPHA, BOUND_IS_INTEGER, BOUND_EQUALS_ALPHA, IS_DELSARTE,
    NUMER_VALUE, DENOM_VALUE,
    DENOM_POWER2, DENOM_AS_POWER, DENOM_EW_SQ, DENOM_FORMULA,
    NUMER_FORMULA, NUMER_FROM_EDGES,
    ALPHA_FROM_V, ALPHA_FROM_LOVÁSZ,
    COMPL_K, COMPL_LAMBDA_MIN, COMPL_NUMER, COMPL_DENOM,
    CLIQUE_BOUND, OMEGA, CLIQUE_IS_EW_GAUGE,
    ALPHA_TIMES_OMEGA, ALPHA_OMEGA_EQ_V,
    verify_all, build_ccxcvi_summary,
)


class TestSRGConstants:
    def test_v(self):      assert V == 40
    def test_k(self):      assert K == 12
    def test_lam(self):    assert LAM == 2
    def test_mu(self):     assert MU == 4
    def test_k2(self):     assert K2 == 27
    def test_edges(self):  assert EDGES == 240
    def test_mult_r(self): assert MULT_R == 24
    def test_mult_s(self): assert MULT_S == 15
    def test_q(self):      assert Q == 3
    def test_ew(self):     assert EW_GAUGE_4 == 4


class TestHoffmanBound:
    def test_lambda_min(self):
        assert LAMBDA_MIN == -4

    def test_abs_lambda_min(self):
        assert ABS_LAMBDA_MIN == 4

    def test_abs_lambda_min_eq_ew(self):
        assert ABS_LAMBDA_MIN == EW_GAUGE_4

    def test_hoffman_numer(self):
        assert HOFFMAN_NUMER == Fraction(160)

    def test_hoffman_denom(self):
        assert HOFFMAN_DENOM == Fraction(16)

    def test_hoffman_bound(self):
        assert HOFFMAN_BOUND == Fraction(10)

    def test_bound_is_integer(self):
        assert BOUND_IS_INTEGER is True

    def test_bound_formula(self):
        # Verify the Hoffman formula directly
        bound = Fraction(V * abs(S_EIG), K + abs(S_EIG))
        assert bound == Fraction(10)


class TestIndependenceNumber:
    def test_alpha(self):
        assert ALPHA == 10

    def test_bound_equals_alpha(self):
        assert BOUND_EQUALS_ALPHA is True

    def test_is_delsarte(self):
        assert IS_DELSARTE is True

    def test_alpha_from_v(self):
        assert ALPHA_FROM_V == 10

    def test_alpha_v_div_ew(self):
        assert ALPHA_FROM_V == V // EW_GAUGE_4

    def test_alpha_lovász(self):
        assert ALPHA_FROM_LOVÁSZ == ALPHA


class TestNumerator:
    def test_numer_value(self):
        assert NUMER_VALUE == 160

    def test_numer_v_times_abs_s(self):
        assert NUMER_VALUE == V * abs(S_EIG)

    def test_numer_formula(self):
        assert NUMER_FORMULA == 160

    def test_numer_v_times_ew(self):
        assert NUMER_FORMULA == V * EW_GAUGE_4

    def test_numer_from_edges(self):
        assert NUMER_FROM_EDGES == Fraction(160)

    def test_numer_edges_fraction(self):
        assert NUMER_FROM_EDGES == Fraction(EDGES * (Q - 1), Q)


class TestDenominator:
    def test_denom_value(self):
        assert DENOM_VALUE == 16

    def test_denom_k_plus_abs_s(self):
        assert DENOM_VALUE == K + abs(S_EIG)

    def test_denom_formula(self):
        assert DENOM_FORMULA == 16

    def test_denom_power2(self):
        assert DENOM_POWER2 == 4

    def test_denom_as_power(self):
        assert DENOM_AS_POWER == 16

    def test_denom_2_to_4(self):
        assert DENOM_AS_POWER == 2 ** 4

    def test_denom_ew_sq(self):
        assert DENOM_EW_SQ == 16

    def test_denom_ew_sq_formula(self):
        assert DENOM_EW_SQ == EW_GAUGE_4 ** 2


class TestCliqueBound:
    def test_compl_k(self):
        assert COMPL_K == 27

    def test_compl_lambda_min(self):
        assert COMPL_LAMBDA_MIN == -3

    def test_compl_numer(self):
        assert COMPL_NUMER == Fraction(120)

    def test_compl_denom(self):
        assert COMPL_DENOM == Fraction(30)

    def test_clique_bound(self):
        assert CLIQUE_BOUND == Fraction(4)

    def test_omega(self):
        assert OMEGA == 4

    def test_omega_eq_ew(self):
        assert OMEGA == EW_GAUGE_4

    def test_clique_is_ew(self):
        assert CLIQUE_IS_EW_GAUGE is True


class TestProductIdentity:
    def test_alpha_times_omega(self):
        assert ALPHA_TIMES_OMEGA == 40

    def test_alpha_times_omega_eq_v(self):
        assert ALPHA_OMEGA_EQ_V is True

    def test_alpha_times_omega_formula(self):
        assert ALPHA * OMEGA == V

    def test_numer_div_alpha(self):
        assert NUMER_VALUE // ALPHA == DENOM_VALUE


class TestVerifyAll:
    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_total_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_27_pass(self):
        _, passed, _ = verify_all()
        assert passed == 27

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [name for name, ok, _ in checks if not ok]
        assert failed == [], f"Failed checks: {failed}"


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxcvi_summary()

    def test_part(self):              assert self.s["part"] == "CCXCVI"
    def test_title_hoffman(self):     assert "Hoffman" in self.s["title"]
    def test_checks_pass(self):       assert self.s["checks_pass"] == 27
    def test_checks_total(self):      assert self.s["checks_total"] == 27
    def test_status(self):            assert self.s["status"] == "ALL_PASS"
    def test_lambda_min(self):        assert self.s["lambda_min"] == -4
    def test_hoffman_numer(self):     assert self.s["hoffman_numer"] == 160
    def test_hoffman_denom(self):     assert self.s["hoffman_denom"] == 16
    def test_hoffman_bound(self):     assert self.s["hoffman_bound"] == 10
    def test_alpha(self):             assert self.s["alpha"] == 10
    def test_omega(self):             assert self.s["omega"] == 4
    def test_alpha_times_omega(self): assert self.s["alpha_times_omega"] == 40
    def test_is_delsarte(self):       assert self.s["is_delsarte"] is True
    def test_clique_bound(self):      assert self.s["clique_bound"] == 4
    def test_discoveries(self):
        assert isinstance(self.s["discoveries"], list)
        assert len(self.s["discoveries"]) >= 5
