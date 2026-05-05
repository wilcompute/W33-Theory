"""
Tests for Part CCXCIII: Lovász Theta Function and Spectral Independence Bounds for W(3,3).
"""
import pytest
from fractions import Fraction
from exploration.PART_CCXCIII_LOVÁSZ_THETA_BRIDGE import (
    # SRG constants
    V, K, LAM, MU, K2, MULT_R, MULT_S, EDGES,
    # SM constants
    EW_GAUGE_4, QUARKS_36, TOTAL_SM_40, SM_GENERATIONS, SM_WEYL_PER_GEN, Q,
    # Eigenvalues
    DISC_INT, R_EIG, S_EIG,
    # Lovász theta
    THETA_NUM, THETA_DEN, THETA_LOVÁSZ,
    # Complement
    K_COMP, LAM_COMP, MU_COMP, R_COMP, S_COMP,
    THETA_COMP_NUM, THETA_COMP_DEN, THETA_COMP,
    # Products / sums
    THETA_PRODUCT, THETA_SUM,
    # Independence
    RATIO_BOUND, ALPHA_EXACT, ALPHA_RATIO,
    # Fractional chromatic
    CHI_FRAC, CHI_FRAC_INT,
    # Clique
    OMEGA_CLIQUE,
    # Sandwich
    OMEGA_BOUND_HOLDS, ALPHA_BOUND_HOLDS,
    # SM triple
    SM_THETA_COMP, SM_CHI_FRAC, SM_OMEGA, SM_TRIPLE_CONSISTENT,
    SM_ALPHA_FOUR_TIMES,
    # Eigenvalue ratio
    K_OVER_ABS_S,
    # Functions
    verify_all, build_ccxciii_summary,
)


class TestSRGConstants:
    def test_V(self):        assert V == 40
    def test_K(self):        assert K == 12
    def test_LAM(self):      assert LAM == 2
    def test_MU(self):       assert MU == 4
    def test_K2(self):       assert K2 == 27
    def test_K_K2_V(self):   assert K + K2 + 1 == V
    def test_MULT_R(self):   assert MULT_R == 24
    def test_MULT_S(self):   assert MULT_S == 15
    def test_EDGES(self):    assert EDGES == 240
    def test_mults_sum(self): assert 1 + MULT_R + MULT_S == V


class TestSMConstants:
    def test_EW_GAUGE_4(self):       assert EW_GAUGE_4 == 4
    def test_QUARKS_36(self):        assert QUARKS_36 == 36
    def test_TOTAL_SM_40(self):      assert TOTAL_SM_40 == 40
    def test_Q(self):                assert Q == 3


class TestEigenvalues:
    def test_DISC_INT(self):         assert DISC_INT == 36
    def test_R_EIG(self):            assert R_EIG == 2
    def test_S_EIG(self):            assert S_EIG == -4
    def test_eigenvalue_sum(self):   assert R_EIG + S_EIG == LAM - MU
    def test_eigenvalue_product(self): assert R_EIG * S_EIG == MU - K
    def test_r_positive(self):       assert R_EIG > 0
    def test_s_negative(self):       assert S_EIG < 0
    def test_k_not_eigenvalue(self): assert K != R_EIG and K != S_EIG


class TestThetaLovász:
    def test_THETA_NUM(self):        assert THETA_NUM == 160
    def test_THETA_DEN(self):        assert THETA_DEN == 16
    def test_THETA_LOVÁSZ(self):     assert THETA_LOVÁSZ == Fraction(10)
    def test_THETA_is_int(self):     assert THETA_LOVÁSZ.denominator == 1
    def test_THETA_formula(self):
        assert THETA_LOVÁSZ == Fraction(V * abs(S_EIG), K - S_EIG)
    def test_THETA_SUM(self):        assert THETA_SUM == 14


class TestComplementSRG:
    def test_K_COMP(self):           assert K_COMP == 27
    def test_LAM_COMP(self):         assert LAM_COMP == 18
    def test_MU_COMP(self):          assert MU_COMP == 18
    def test_R_COMP(self):           assert R_COMP == 3
    def test_S_COMP(self):           assert S_COMP == -3
    def test_comp_k_sum(self):       assert K + K_COMP == V - 1
    def test_THETA_COMP_NUM(self):   assert THETA_COMP_NUM == 120
    def test_THETA_COMP_DEN(self):   assert THETA_COMP_DEN == 30
    def test_THETA_COMP(self):       assert THETA_COMP == Fraction(4)
    def test_THETA_COMP_is_int(self): assert THETA_COMP.denominator == 1
    def test_THETA_COMP_eq_EW4(self): assert int(THETA_COMP) == EW_GAUGE_4


class TestThetaProduct:
    def test_THETA_PRODUCT(self):    assert THETA_PRODUCT == Fraction(V)
    def test_product_eq_V(self):     assert THETA_PRODUCT == 40
    def test_product_int(self):      assert THETA_PRODUCT.denominator == 1
    def test_product_formula(self):  assert THETA_LOVÁSZ * THETA_COMP == THETA_PRODUCT


class TestIndependenceNumber:
    def test_RATIO_BOUND(self):      assert RATIO_BOUND == Fraction(10)
    def test_ALPHA_EXACT(self):      assert ALPHA_EXACT == 10
    def test_ALPHA_RATIO(self):      assert ALPHA_RATIO == Fraction(1, 4)
    def test_alpha_eq_theta(self):   assert Fraction(ALPHA_EXACT) == THETA_LOVÁSZ
    def test_alpha_eq_ratio_bound(self): assert ALPHA_EXACT == int(RATIO_BOUND)
    def test_alpha_positive(self):   assert ALPHA_EXACT > 0
    def test_alpha_leq_V(self):      assert ALPHA_EXACT <= V


class TestFractionalChromatic:
    def test_CHI_FRAC(self):         assert CHI_FRAC == Fraction(4)
    def test_CHI_FRAC_INT(self):     assert CHI_FRAC_INT == 4
    def test_CHI_FRAC_eq_EW4(self):  assert CHI_FRAC_INT == EW_GAUGE_4
    def test_chi_frac_formula(self): assert CHI_FRAC == Fraction(V, ALPHA_EXACT)
    def test_chi_frac_alpha_V(self): assert ALPHA_EXACT * CHI_FRAC_INT == V


class TestClique:
    def test_OMEGA(self):            assert OMEGA_CLIQUE == 4
    def test_OMEGA_eq_EW4(self):     assert OMEGA_CLIQUE == EW_GAUGE_4
    def test_OMEGA_eq_theta_comp(self): assert OMEGA_CLIQUE == int(THETA_COMP)
    def test_OMEGA_eq_chi_frac(self): assert OMEGA_CLIQUE == CHI_FRAC_INT


class TestSandwichBounds:
    def test_OMEGA_BOUND(self):      assert OMEGA_BOUND_HOLDS is True
    def test_ALPHA_BOUND(self):      assert ALPHA_BOUND_HOLDS is True
    def test_omega_leq_theta_comp(self): assert OMEGA_CLIQUE <= int(THETA_COMP)
    def test_alpha_leq_theta(self):  assert ALPHA_EXACT <= int(THETA_LOVÁSZ)


class TestSMTriple:
    def test_SM_THETA_COMP(self):    assert SM_THETA_COMP == 4
    def test_SM_CHI_FRAC(self):      assert SM_CHI_FRAC == 4
    def test_SM_OMEGA(self):         assert SM_OMEGA == 4
    def test_triple_consistent(self): assert SM_TRIPLE_CONSISTENT is True
    def test_triple_eq_EW4(self):
        assert SM_THETA_COMP == SM_CHI_FRAC == SM_OMEGA == EW_GAUGE_4
    def test_alpha_four_times(self): assert SM_ALPHA_FOUR_TIMES == V


class TestEigenvalueRatios:
    def test_K_OVER_ABS_S(self):     assert K_OVER_ABS_S == Fraction(3)
    def test_K_OVER_ABS_S_eq_Q(self): assert K_OVER_ABS_S == Fraction(Q)


class TestVerifyFunctions:
    def test_verify_all_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple) and len(result) == 3

    def test_verify_all_passed(self):
        _, passed, _ = verify_all()
        assert passed == 27

    def test_verify_all_total(self):
        _, _, total = verify_all()
        assert total == 27

    def test_verify_all_perfect(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_verify_all_checks_list(self):
        checks, _, _ = verify_all()
        assert all(ok for _, ok, _ in checks)


class TestBuildSummary:
    def setup_method(self):
        self.s = build_ccxciii_summary()

    def test_part_number(self):      assert self.s["part"] == "CCXCIII"
    def test_checks_pass(self):      assert self.s["checks_pass"] == 27
    def test_checks_total(self):     assert self.s["checks_total"] == 27
    def test_status(self):           assert self.s["status"] == "ALL_PASS"
    def test_theta_lovász(self):     assert self.s["theta_lovász"] == 10
    def test_theta_comp(self):       assert self.s["theta_comp"] == 4
    def test_theta_product(self):    assert self.s["theta_product"] == 40
    def test_chi_frac(self):         assert self.s["chi_frac"] == 4
    def test_omega(self):            assert self.s["omega_clique"] == 4
    def test_sm_triple(self):        assert self.s["sm_triple"]["all_equal_EW_GAUGE_4"] is True
    def test_discoveries(self):      assert len(self.s["discoveries"]) >= 5
