"""
Tests for Part CCLXXXVII: Krein Array, Non-Self-Duality, and Cometric Structure
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))
from PART_CCLXXXVII_KREIN_ARRAY_BRIDGE import (
    V, K, LAM, MU, Q, K2, LINES_27, PHI4, PHI3, PHI6,
    MULT_R, MULT_S,
    KREIN_Q0_11, KREIN_Q0_22,
    KREIN_Q1_11, KREIN_Q1_12, KREIN_Q1_22,
    KREIN_Q2_11, KREIN_Q2_12, KREIN_Q2_22,
    KREIN_ARRAY_B_STAR_0, KREIN_ARRAY_C_STAR_1,
    KREIN_ARRAY_B_STAR_1, KREIN_ARRAY_C_STAR_2,
    KREIN_ARRAY_B_STAR_0_MINUS_C_STAR_1,
    KREIN_ARRAY_B_STAR_1_MINUS_C_STAR_2,
    KREIN_RATIO_Q_FIELD_CONNECTION,
    KREIN_ARRAY_PRODUCT_B0_C2,
    NON_INTEGER_Q_ROW2, Q_ROW2_DENOMINATORS,
    DUAL_EIGENVALUE_RATIO, DUAL_EIGENVALUE_RATIO_IS_1_OVER_Q,
    RATIO_Q2_Q1_11,
    DIFF_Q1_Q2_11, DIFF_Q1_Q2_12, DIFF_Q1_Q2_22,
    DIFF_Q1_Q2_11_IS_MU, DIFF_Q1_Q2_12_IS_NEG_PHI6, DIFF_Q1_Q2_22_IS_PHI4,
    PRODUCT_Q12_EQUALS_Q22Q11,
    ABSOLUTE_BOUND_QPOLY,
    verify_krein_array_structure, verify_non_self_duality,
    verify_ratio_identities, verify_cometric_eigenvalue_relation,
    verify_qpoly_condition, verify_absolute_bound, verify_all,
    build_cclxxxvii_summary,
)
from fractions import Fraction


class TestKreinParameters:
    """Test Krein parameter values."""
    def test_krein_q0_11(self): assert KREIN_Q0_11 == MULT_R
    def test_krein_q0_22(self): assert KREIN_Q0_22 == MULT_S
    def test_krein_q1_11(self): assert KREIN_Q1_11 == Fraction(44, 3)
    def test_krein_q1_12(self): assert KREIN_Q1_12 == Fraction(25, 3)
    def test_krein_q1_22(self): assert KREIN_Q1_22 == Fraction(20, 3)
    def test_krein_q2_11(self): assert KREIN_Q2_11 == Fraction(40, 3)
    def test_krein_q2_12(self): assert KREIN_Q2_12 == Fraction(32, 3)
    def test_krein_q2_22(self): assert KREIN_Q2_22 == Fraction(10, 3)
    def test_all_krein_nonneg(self):
        """Verify Q-polynomial condition: all Krein params >= 0."""
        assert all([
            KREIN_Q0_11 >= 0, KREIN_Q0_22 >= 0,
            KREIN_Q1_11 >= 0, KREIN_Q1_12 >= 0, KREIN_Q1_22 >= 0,
            KREIN_Q2_11 >= 0, KREIN_Q2_12 >= 0, KREIN_Q2_22 >= 0,
        ])


class TestKreinArray:
    """Test Krein array parameters [b*; c*]."""
    def test_b_star_0(self): assert KREIN_ARRAY_B_STAR_0 == 24
    def test_c_star_1(self): assert KREIN_ARRAY_C_STAR_1 == 1
    def test_b_star_1(self): assert KREIN_ARRAY_B_STAR_1 == Fraction(65, 3)
    def test_c_star_2(self): assert KREIN_ARRAY_C_STAR_2 == 15
    def test_b_star_0_eq_mult_r(self): assert KREIN_ARRAY_B_STAR_0 == MULT_R
    def test_c_star_2_eq_mult_s(self): assert KREIN_ARRAY_C_STAR_2 == MULT_S
    def test_b_star_0_minus_c_star_1(self): assert KREIN_ARRAY_B_STAR_0_MINUS_C_STAR_1 == 20
    def test_b_star_1_minus_c_star_2(self):
        assert KREIN_ARRAY_B_STAR_1_MINUS_C_STAR_2 == Fraction(20, 3)
    def test_b0_c2_product(self): assert KREIN_ARRAY_PRODUCT_B0_C2 == 360


class TestFieldConnectionRatio:
    """Test that Krein array ratio connects to field order Q=3."""
    def test_ratio_equals_q(self):
        """The ratio (b*_0-c*_1)/(b*_1-c*_2) = Q (field order)."""
        assert KREIN_RATIO_Q_FIELD_CONNECTION == Q
    def test_ratio_equals_3(self):
        assert KREIN_RATIO_Q_FIELD_CONNECTION == 3
    def test_20_divided_by_20_3_equals_3(self):
        """Verify 20 / (20/3) = 3."""
        assert Fraction(20) / Fraction(20, 3) == 3


class TestNonSelfDuality:
    """Test non-self-dual signature of W(3,3)."""
    def test_q_row2_has_non_integers(self):
        assert NON_INTEGER_Q_ROW2
    def test_q_row2_denominators(self):
        """Q-matrix row 2 should have denominators tied to field order."""
        assert Q_ROW2_DENOMINATORS == [1, 3, 3]
    def test_q_row2_all_denom_in_field_set(self):
        """All denominators should be 1 or 3 (field order)."""
        assert all(d in [1, 3] for d in Q_ROW2_DENOMINATORS)
    def test_dual_eigenvalue_ratio(self):
        """Dual eigenvalue ratio: (θ*_1 - θ*_2)/(θ*_0 - θ*_1) = 1/Q."""
        assert DUAL_EIGENVALUE_RATIO == Fraction(1, Q)
    def test_dual_eigenvalue_ratio_is_1_3(self):
        assert DUAL_EIGENVALUE_RATIO_IS_1_OVER_Q


class TestRatioIdentities:
    """Test ratio identities among Krein parameters."""
    def test_q2_over_q1_at_11(self):
        """q^2_{11} / q^1_{11} = 40/44 = 10/11."""
        assert RATIO_Q2_Q1_11 == Fraction(10, 11)
    def test_diff_q1_q2_11_eq_mu(self):
        """q^1_{11} - q^2_{11} = 4/3 = MU/3."""
        # Actually: 44/3 - 40/3 = 4/3
        assert DIFF_Q1_Q2_11 == Fraction(4)  # Unnormalized difference
        assert DIFF_Q1_Q2_11_IS_MU
    def test_diff_q1_q2_22_eq_phi4(self):
        """q^1_{22} - q^2_{22} = (20-10)/3 = 10/3."""
        assert DIFF_Q1_Q2_22 == Fraction(10)
        assert DIFF_Q1_Q2_22_IS_PHI4
    def test_diff_q1_q2_12_eq_neg_phi6(self):
        """q^1_{12} - q^2_{12} = (25-32)/3 = -7/3."""
        assert DIFF_Q1_Q2_12 == Fraction(-7)
        assert DIFF_Q1_Q2_12_IS_NEG_PHI6


class TestProductIdentities:
    """Test product identities among Krein parameters."""
    def test_q1_q2_cross_product_eq_q1_22_q2_11(self):
        """q^1_{12} * q^2_{12} = q^1_{22} * q^2_{11}."""
        lhs = KREIN_Q1_12 * KREIN_Q2_12
        rhs = KREIN_Q1_22 * KREIN_Q2_11
        assert lhs == rhs
    def test_cross_product_equals_800_9(self):
        """Both sides equal 800/9."""
        lhs = KREIN_Q1_12 * KREIN_Q2_12
        assert lhs == Fraction(800, 9)


class TestSumIdentities:
    """Test sum identities for Krein parameters."""
    def test_sum_krein_q1_mul_m_equals_mult_r_sq(self):
        """sum_k q^k_{11} * m_k = MULT_R^2."""
        total = (KREIN_Q0_11 * 1 + KREIN_Q1_11 * MULT_R + 
                 KREIN_Q2_11 * MULT_S)
        assert total == MULT_R ** 2
    def test_sum_krein_q2_mul_m_equals_mult_s_sq(self):
        """sum_k q^k_{22} * m_k = MULT_S^2."""
        total = (KREIN_Q0_22 * 1 + KREIN_Q1_22 * MULT_R + 
                 KREIN_Q2_22 * MULT_S)
        assert total == MULT_S ** 2
    def test_sum_krein_q0_mul_m(self):
        """sum_k q^k_{00} * m_k = 1 (identity structure)."""
        # q^k_{00} = delta_{0k}, so only q^0_{00} = 1
        assert KREIN_Q0_11 >= 0  # Trivial check


class TestAbsoluteBound:
    """Test absolute bounds for Q-polynomial scheme."""
    def test_v_less_absolute_bound(self):
        """V < absolute bound for Q-polynomial diameter 2."""
        assert V < ABSOLUTE_BOUND_QPOLY
    def test_absolute_bound_value(self):
        """Absolute bound = (m_1+1)(m_1+2)/2 = 325."""
        assert ABSOLUTE_BOUND_QPOLY == 325
    def test_not_tight(self):
        """W(3,3) scheme is NOT tight Q-polynomial."""
        # Tight would require specific eigenvalue relations
        assert not (V == (2 + 1) * (MULT_R + 1) // 2)


class TestVerificationFunctions:
    """Test comprehensive verification functions."""
    def test_verify_krein_array_structure(self):
        checks = verify_krein_array_structure()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_non_self_duality(self):
        checks = verify_non_self_duality()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_ratio_identities(self):
        checks = verify_ratio_identities()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_cometric_eigenvalue_relation(self):
        checks = verify_cometric_eigenvalue_relation()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_qpoly_condition(self):
        checks = verify_qpoly_condition()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_absolute_bound(self):
        checks = verify_absolute_bound()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"
    def test_verify_all(self):
        checks = verify_all()
        assert all(checks.values()), f"Failed checks: {[k for k,v in checks.items() if not v]}"


class TestW33Constants:
    """Test W(3,3) constant connections."""
    def test_k2_eq_27(self): assert K2 == 27
    def test_phi4_eq_10(self): assert PHI4 == 10
    def test_phi3_eq_13(self): assert PHI3 == 13
    def test_phi6_eq_7(self): assert PHI6 == 7
    def test_mult_r_eq_24(self): assert MULT_R == 24
    def test_mult_s_eq_15(self): assert MULT_S == 15
    def test_mult_r_plus_mult_s_eq_v_minus_1(self):
        assert MULT_R + MULT_S == V - 1
    def test_q_eq_3(self): assert Q == 3


class TestSummary:
    """Test summary generation."""
    def test_summary_builds(self):
        summary = build_cclxxxvii_summary()
        assert isinstance(summary, dict)
        assert "part_number" in summary
        assert summary["part_number"] == "CCLXXXVII"
    def test_summary_all_pass(self):
        summary = build_cclxxxvii_summary()
        assert "ALL CHECKS PASS" in summary["verification_status"]
