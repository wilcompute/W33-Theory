"""Tests for PART CCCXIII — Lovász Theta Function & Independence Bound of W(3,3)."""

import sys
import os
import pytest
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))
from PART_CCCXIII_LOVASZ_THETA_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, MULT_R, MULT_S,
    ALPHA, GUT_DIM, GENERATIONS,
    INDEP_NUM_ALPHA, CLIQUE_NUM_OMEGA,
    THETA_LB_INDEP, THETA_UB_HOFFMAN, CHI_LB,
    K_COMP, LAM_COMP, MU_COMP,
    verify_all, build_cccxiii_summary,
)


class TestSRGParameters:
    def test_V_K_LAM_MU(self):
        assert V == 40 and K == 12 and LAM == 2 and MU == 4

    def test_eigenvalues(self):
        assert R_EIG == 2 and S_EIG == -4

    def test_multiplicities(self):
        assert MULT_R == 24 and MULT_S == 15


class TestIndependenceNumber:
    def test_alpha_equals_4(self):
        assert INDEP_NUM_ALPHA == 4

    def test_alpha_eq_generations_plus_1(self):
        assert INDEP_NUM_ALPHA == GENERATIONS + 1

    def test_alpha_is_positive(self):
        assert INDEP_NUM_ALPHA > 0
        assert INDEP_NUM_ALPHA <= V


class TestCliqueNumber:
    def test_omega_equals_4(self):
        assert CLIQUE_NUM_OMEGA == 4

    def test_omega_eq_generations_plus_1(self):
        assert CLIQUE_NUM_OMEGA == GENERATIONS + 1

    def test_omega_eq_alpha(self):
        assert CLIQUE_NUM_OMEGA == INDEP_NUM_ALPHA

    def test_omega_is_positive(self):
        assert CLIQUE_NUM_OMEGA > 0
        assert CLIQUE_NUM_OMEGA <= V


class TestLovaszThetaBounds:
    def test_theta_lb_equals_alpha(self):
        assert THETA_LB_INDEP == INDEP_NUM_ALPHA

    def test_theta_ub_hoffman(self):
        assert THETA_UB_HOFFMAN == 10

    def test_theta_ub_hoffman_formula(self):
        expected = Fraction(V, 1 + Fraction(K, abs(S_EIG)))
        assert THETA_UB_HOFFMAN == expected

    def test_chi_lb_equals_V_div_alpha(self):
        assert CHI_LB == Fraction(V, INDEP_NUM_ALPHA)
        assert CHI_LB == 10

    def test_theta_bounds_sandwich(self):
        assert THETA_LB_INDEP <= THETA_UB_HOFFMAN


class TestComplementGraph:
    def test_K_complement_equals_27(self):
        assert K_COMP == 27

    def test_K_complement_equals_GUT_DIM(self):
        assert K_COMP == GUT_DIM

    def test_K_complement_formula(self):
        assert K_COMP == V - 1 - K

    def test_LAM_complement_equals_18(self):
        assert LAM_COMP == 18

    def test_MU_complement_equals_18(self):
        assert MU_COMP == 18

    def test_complement_is_regular(self):
        # Complement is also regular
        assert K_COMP == 27
        assert K + K_COMP == V - 1


class TestSMEncodings:
    def test_K_alpha_plus_lambda(self):
        assert K == ALPHA + LAM

    def test_alpha_digit_in_K(self):
        assert K == 12
        assert ALPHA == 10

    def test_generations_in_structures(self):
        assert INDEP_NUM_ALPHA == GENERATIONS + 1
        assert CLIQUE_NUM_OMEGA == GENERATIONS + 1

    def test_GUT_DIM_in_complement(self):
        assert K_COMP == GUT_DIM

    def test_generations_in_eigenvalues(self):
        assert GENERATIONS == 3


class TestVerifyAll:
    def test_returns_tuple_of_three(self):
        result = verify_all()
        assert len(result) == 3

    def test_total_is_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        checks, passed, total = verify_all()
        assert passed == total

    def test_check_names_unique(self):
        checks, _, _ = verify_all()
        names = [c["name"] for c in checks]
        assert len(names) == len(set(names))


class TestBuildSummary:
    def test_returns_dict(self):
        s = build_cccxiii_summary()
        assert isinstance(s, dict)

    def test_part_is_cccxiii(self):
        s = build_cccxiii_summary()
        assert s["part"] == "CCCXIII"

    def test_status_pass(self):
        s = build_cccxiii_summary()
        assert s["status"] == "PASS"

    def test_checks_27(self):
        s = build_cccxiii_summary()
        assert s["checks_total"] == 27

    def test_discoveries_nonempty(self):
        s = build_cccxiii_summary()
        assert len(s["discoveries"]) >= 5
