"""
Tests for PART CCCXLVII -- Intersection Numbers as Primal Propagators of W(3,3)
"""
import pytest
from fractions import Fraction
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))
from PART_CCCXLVII_INTERSECTION_NUMBERS_BRIDGE import (
    V, K, LAM, MU, R_EIG, S_EIG, ABS_S, MULT_R, MULT_S, L,
    SU5_ADJ, SU5_MATTER_PER_GEN, SU5_DIM, GENERATIONS, GUT_DIM,
    EW_GAUGE_4, GLUON_COUNT, K_VAL,
    compute_intersection_numbers, p_ij_l,
    verify_all, build_cccxlvii_summary,
)


class TestConstants:
    """W(3,3) SRG and SM constants are correct."""

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_R_EIG(self):
        assert R_EIG == 2

    def test_S_EIG(self):
        assert S_EIG == -4

    def test_ABS_S(self):
        assert ABS_S == 4

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_L_complement_valency(self):
        assert L == V - K - 1

    def test_L_equals_27(self):
        assert L == 27

    def test_SU5_ADJ(self):
        assert SU5_ADJ == 24

    def test_GLUON_COUNT(self):
        assert GLUON_COUNT == 8

    def test_GUT_DIM(self):
        assert GUT_DIM == 27

    def test_EW_GAUGE_4(self):
        assert EW_GAUGE_4 == 4

    def test_GENERATIONS(self):
        assert GENERATIONS == 3

    def test_K_VAL(self):
        assert K_VAL == [1, K, L]

    def test_eigenvalue_relation(self):
        # r + s = LAM - MU  =>  2 + (-4) = -2 = 2 - 4 ✓
        assert R_EIG + S_EIG == LAM - MU

    def test_vertex_partition(self):
        # 1 + MULT_R + MULT_S = V
        assert 1 + MULT_R + MULT_S == V


class TestIdentityRelation:
    """A_0 = I acts as multiplicative identity."""

    def test_p000(self):
        assert p_ij_l(0, 0, 0) == Fraction(1)

    def test_p011(self):
        assert p_ij_l(0, 1, 1) == Fraction(1)

    def test_p022(self):
        assert p_ij_l(0, 2, 2) == Fraction(1)

    def test_p010(self):
        assert p_ij_l(0, 1, 0) == Fraction(0)

    def test_p020(self):
        assert p_ij_l(0, 2, 0) == Fraction(0)

    def test_p012_off(self):
        assert p_ij_l(0, 1, 2) == Fraction(0)

    def test_p021_off(self):
        assert p_ij_l(0, 2, 1) == Fraction(0)


class TestAdjacencySelfProduct:
    """p[1][1][l] from A_1^2 = K*A_0 + LAM*A_1 + MU*A_2."""

    def test_p110_eq_K(self):
        assert p_ij_l(1, 1, 0) == Fraction(K)

    def test_p111_eq_LAM(self):
        assert p_ij_l(1, 1, 1) == Fraction(LAM)

    def test_p112_eq_MU(self):
        assert p_ij_l(1, 1, 2) == Fraction(MU)

    def test_p110_eq_su5_adj_half(self):
        # K = 12 = SU5_ADJ / 2
        assert p_ij_l(1, 1, 0) == Fraction(SU5_ADJ, 2)

    def test_p111_eq_R_EIG(self):
        # Lambda (triangle count) = R eigenvalue = 2
        assert int(p_ij_l(1, 1, 1)) == R_EIG

    def test_p112_eq_ABS_S(self):
        # Mu (quad count) = |S eigenvalue| = 4
        assert int(p_ij_l(1, 1, 2)) == ABS_S

    def test_p112_eq_EW_GAUGE_4(self):
        # Common non-neighbors = 4 EW gauge bosons
        assert int(p_ij_l(1, 1, 2)) == EW_GAUGE_4

    def test_p110_is_integer(self):
        assert p_ij_l(1, 1, 0).denominator == 1

    def test_p111_is_integer(self):
        assert p_ij_l(1, 1, 1).denominator == 1

    def test_p112_is_integer(self):
        assert p_ij_l(1, 1, 2).denominator == 1

    def test_p111_plus_p112_eq_LAM_plus_MU(self):
        assert p_ij_l(1, 1, 1) + p_ij_l(1, 1, 2) == Fraction(LAM + MU)


class TestCrossProduct:
    """p[1][2][l] from A_1*A_2 = (K-LAM-1)*A_1 + (K-MU)*A_2."""

    def test_p120_eq_zero(self):
        assert p_ij_l(1, 2, 0) == Fraction(0)

    def test_p121_formula(self):
        assert p_ij_l(1, 2, 1) == Fraction(K - LAM - 1)

    def test_p121_value(self):
        assert int(p_ij_l(1, 2, 1)) == 9

    def test_p122_formula(self):
        assert p_ij_l(1, 2, 2) == Fraction(K - MU)

    def test_p122_value(self):
        assert int(p_ij_l(1, 2, 2)) == 8

    def test_p122_eq_GLUON_COUNT(self):
        # The cross number equals the SU(3)_C gluon octet count!
        assert int(p_ij_l(1, 2, 2)) == GLUON_COUNT

    def test_p121_plus_p122(self):
        expected = Fraction(2 * K - LAM - MU - 1)
        assert p_ij_l(1, 2, 1) + p_ij_l(1, 2, 2) == expected

    def test_p121_plus_p122_value(self):
        assert int(p_ij_l(1, 2, 1) + p_ij_l(1, 2, 2)) == 17

    def test_p210_symmetry(self):
        assert p_ij_l(2, 1, 0) == p_ij_l(1, 2, 0)

    def test_p211_symmetry(self):
        assert p_ij_l(2, 1, 1) == p_ij_l(1, 2, 1)

    def test_p212_symmetry(self):
        assert p_ij_l(2, 1, 2) == p_ij_l(1, 2, 2)


class TestComplementSelfProduct:
    """p[2][2][l] from A_2^2 = L*A_0 + 18*A_1 + 18*A_2."""

    def test_p220_eq_L(self):
        assert p_ij_l(2, 2, 0) == Fraction(L)

    def test_p220_eq_GUT_DIM(self):
        assert int(p_ij_l(2, 2, 0)) == GUT_DIM

    def test_p220_eq_V_K_1(self):
        assert p_ij_l(2, 2, 0) == Fraction(V - K - 1)

    def test_p221_value(self):
        assert int(p_ij_l(2, 2, 1)) == 18

    def test_p222_value(self):
        assert int(p_ij_l(2, 2, 2)) == 18

    def test_conference_equality(self):
        # complement is conference-type: lambda_c = mu_c
        assert p_ij_l(2, 2, 1) == p_ij_l(2, 2, 2)

    def test_p221_eq_6_generations(self):
        assert int(p_ij_l(2, 2, 1)) == 6 * GENERATIONS

    def test_p221_is_integer(self):
        assert p_ij_l(2, 2, 1).denominator == 1

    def test_p222_is_integer(self):
        assert p_ij_l(2, 2, 2).denominator == 1

    def test_p221_formula(self):
        # p[2][2][1] = L - (K-LAM-1)
        assert p_ij_l(2, 2, 1) == Fraction(L - (K - LAM - 1))

    def test_p222_formula(self):
        # p[2][2][2] = L - 1 - (K-MU)
        assert p_ij_l(2, 2, 2) == Fraction(L - 1 - (K - MU))


class TestValencyConservation:
    """Row-sum (valency) laws: sum_l p[i][j][l]*k_l = k_i*k_j."""

    def test_row11(self):
        row = sum(p_ij_l(1, 1, l) * K_VAL[l] for l in range(3))
        assert row == Fraction(K ** 2)

    def test_row12(self):
        row = sum(p_ij_l(1, 2, l) * K_VAL[l] for l in range(3))
        assert row == Fraction(K * L)

    def test_row22(self):
        row = sum(p_ij_l(2, 2, l) * K_VAL[l] for l in range(3))
        assert row == Fraction(L ** 2)

    def test_row11_numeric(self):
        row = sum(p_ij_l(1, 1, l) * K_VAL[l] for l in range(3))
        assert int(row) == 144  # 12^2

    def test_row12_numeric(self):
        row = sum(p_ij_l(1, 2, l) * K_VAL[l] for l in range(3))
        assert int(row) == 324  # 12*27

    def test_row22_numeric(self):
        row = sum(p_ij_l(2, 2, l) * K_VAL[l] for l in range(3))
        assert int(row) == 729  # 27^2


class TestSymmetry:
    """p[i][j][l] = p[j][i][l] for all i,j,l (undirected graph)."""

    def test_symmetry_11(self):
        for l in range(3):
            assert p_ij_l(1, 1, l) == p_ij_l(1, 1, l)

    def test_symmetry_12_vs_21(self):
        for l in range(3):
            assert p_ij_l(1, 2, l) == p_ij_l(2, 1, l)

    def test_symmetry_all(self):
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    assert p_ij_l(i, j, l) == p_ij_l(j, i, l)


class TestPhysicsIdentities:
    """Key physics connections encoded in intersection numbers."""

    def test_lambda_eq_r_eigenvalue(self):
        # Triangle count = R eigenvalue of W(3,3)
        assert LAM == R_EIG

    def test_mu_eq_abs_s_eigenvalue(self):
        # Quad count = |S eigenvalue| of W(3,3)
        assert MU == ABS_S

    def test_gluon_from_cross_product(self):
        # p[1][2][2] = K - MU = 8 = SU(3)_C octet
        assert int(p_ij_l(1, 2, 2)) == GLUON_COUNT

    def test_gut_dim_from_complement(self):
        # p[2][2][0] = L = 27 = GUT_DIM
        assert int(p_ij_l(2, 2, 0)) == GUT_DIM

    def test_ew_gauge_from_mu(self):
        # mu = 4 = EW_GAUGE_4
        assert MU == EW_GAUGE_4

    def test_triangle_quad_ratio(self):
        # p[1][1][1] / p[1][1][2] = R_EIG / ABS_S = 1/2
        ratio = p_ij_l(1, 1, 1) / p_ij_l(1, 1, 2)
        assert ratio == Fraction(R_EIG, ABS_S)

    def test_su5_adj_half_equals_K(self):
        # K = 12 = SU5_ADJ/2 = 24/2
        assert K * 2 == SU5_ADJ

    def test_complement_conference_physics(self):
        # Complement p[2][2][1] = p[2][2][2] = 18 = 6*GENERATIONS
        assert int(p_ij_l(2, 2, 1)) == 6 * GENERATIONS
        assert int(p_ij_l(2, 2, 2)) == 6 * GENERATIONS

    def test_cross_sum_physics(self):
        # p[1][2][1] + p[1][2][2] = 17 = SU5_ADJ - SU5_DIM - LAM
        total = int(p_ij_l(1, 2, 1) + p_ij_l(1, 2, 2))
        assert total == SU5_ADJ - SU5_DIM - LAM


class TestVerifyAll:
    """verify_all() passes all 27 checks."""

    def test_returns_tuple(self):
        result = verify_all()
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_total_is_27(self):
        _, _, total = verify_all()
        assert total == 27

    def test_all_pass(self):
        _, passed, total = verify_all()
        assert passed == total

    def test_no_failures(self):
        checks, _, _ = verify_all()
        failed = [c["name"] for c in checks if not c["passed"]]
        assert failed == []


class TestSummary:
    """build_cccxlvii_summary() returns complete, correct summary."""

    def setup_method(self):
        self.s = build_cccxlvii_summary()

    def test_part(self):
        assert self.s["part"] == "CCCXLVII"

    def test_status_pass(self):
        assert self.s["status"] == "PASS"

    def test_checks_pass(self):
        assert self.s["checks_pass"] == 27

    def test_checks_total(self):
        assert self.s["checks_total"] == 27

    def test_p110_field(self):
        assert self.s["fields"]["p_11_0"] == "12"

    def test_p111_field(self):
        assert self.s["fields"]["p_11_1"] == "2"

    def test_p112_field(self):
        assert self.s["fields"]["p_11_2"] == "4"

    def test_p120_field(self):
        assert self.s["fields"]["p_12_0"] == "0"

    def test_p122_field(self):
        assert self.s["fields"]["p_12_2"] == "8"

    def test_p220_field(self):
        assert self.s["fields"]["p_22_0"] == "27"

    def test_gluon_field(self):
        assert self.s["fields"]["gluon_octet"] == "8"

    def test_gut_dim_field(self):
        assert self.s["fields"]["gut_dim"] == "27"

    def test_discoveries_nonempty(self):
        assert len(self.s["discoveries"]) >= 5
