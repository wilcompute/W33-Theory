"""
Tests for Part CCXC: MacWilliams Transform and Eberlein Polynomials.

Tests the Hamming scheme H(4,3), Krawtchouk polynomials, the MacWilliams
weight enumerator transform Ham(4,3) ↔ Sim(4,3), and the W(3,3) SRG
eigenvalue derivation via the P-matrix.
"""

import pytest
from fractions import Fraction
from math import comb

from exploration.PART_CCXC_MACWILLIAMS_EBERLEIN_BRIDGE import (
    # W(3,3) constants
    V, K, LAM, MU, Q, K2, MULT_R, MULT_S, EDGES,
    # SM constants
    QUARKS_36, EW_GAUGE_4, TOTAL_SM,
    # Scheme constants
    SCHEME_N, SCHEME_Q, SCHEME_CLASSES, SCHEME_SIZE,
    VALENCIES,
    # Krawtchouk
    krawtchouk, build_P_matrix, P_MATRIX,
    build_Q_matrix, Q_MATRIX,
    P_MATRIX_ORTHOGONAL, SCHEME_SELF_DUAL,
    KRAWTCHOUK_1_0, KRAWTCHOUK_1_1, KRAWTCHOUK_1_2,
    KRAWTCHOUK_1_3, KRAWTCHOUK_1_4,
    # Weight enumerator
    HAM_N, HAM_K, HAM_D, HAM_Q,
    SIM_SIZE, SIM_NONZERO, SIM_MIN_DIST,
    SIM_WEIGHT_DIST, HAM_WEIGHT_DIST,
    HAM_SIZE, HAM_A0, HAM_A1, HAM_A2, HAM_A3,
    HAM_A0_IS_1, HAM_NO_LOW_WEIGHTS, HAM_TOTAL_CHECK,
    HAM_ALL_NONNEG_INT, MACWILLIAMS_CONSISTENT,
    macwilliams_transform,
    # SRG eigenvalues
    DELTA, SQRT_DELTA, SRG_R, SRG_S, EIGENVALUE_R, EIGENVALUE_S,
    # Misc
    EXPECTED_COSET_LEADERS_WT1, COSET_LEADER_COUNT_CORRECT,
    HAM_R,
    # Functions
    hamming_scheme_valency,
    verify_scheme_parameters, verify_krawtchouk,
    verify_weight_enumerator, verify_srg_connection,
    verify_all, build_ccxc_summary,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Hamming scheme H(4,3) parameter checks
# ─────────────────────────────────────────────────────────────────────────────

class TestHammingSchemeParameters:
    def test_scheme_n_equals_4(self):
        assert SCHEME_N == 4

    def test_scheme_q_equals_3(self):
        assert SCHEME_Q == 3
        assert SCHEME_Q == Q

    def test_scheme_size_is_81(self):
        assert SCHEME_SIZE == 81

    def test_scheme_size_is_q_pow_n(self):
        assert SCHEME_SIZE == SCHEME_Q ** SCHEME_N

    def test_scheme_classes_is_4(self):
        assert SCHEME_CLASSES == 4

    def test_valency_0_is_1(self):
        assert VALENCIES[0] == 1

    def test_valency_sum_equals_81(self):
        assert sum(VALENCIES) == 81

    def test_valency_1_equals_8(self):
        # C(4,1)*(3-1)^1 = 4*2 = 8
        assert VALENCIES[1] == 8

    def test_valency_2_equals_24(self):
        # C(4,2)*(3-1)^2 = 6*4 = 24
        assert VALENCIES[2] == 24

    def test_valency_3_equals_32(self):
        # C(4,3)*(3-1)^3 = 4*8 = 32
        assert VALENCIES[3] == 32

    def test_valency_4_equals_16(self):
        # C(4,4)*(3-1)^4 = 1*16 = 16
        assert VALENCIES[4] == 16


# ─────────────────────────────────────────────────────────────────────────────
# 2. Krawtchouk polynomial properties
# ─────────────────────────────────────────────────────────────────────────────

class TestKrawtchoukPolynomials:
    def test_k0_is_always_1(self):
        for x in range(SCHEME_N + 1):
            assert krawtchouk(0, x, SCHEME_N, SCHEME_Q) == Fraction(1)

    def test_kk_at_0_eq_valency(self):
        for k in range(SCHEME_N + 1):
            assert krawtchouk(k, 0, SCHEME_N, SCHEME_Q) == \
                   hamming_scheme_valency(SCHEME_N, SCHEME_Q, k)

    def test_k1_at_0_eq_8(self):
        assert KRAWTCHOUK_1_0 == 8

    def test_k1_at_1_eq_5(self):
        assert KRAWTCHOUK_1_1 == 5

    def test_k1_at_2_eq_2(self):
        # K_1(2;4,3) = 4*2 - 2*2 = 8-4 = 4 ? No. Let me compute:
        # K_1(x;n,q) = sum_{j=0}^{1} (-1)^j*(q-1)^{1-j}*C(x,j)*C(n-x,1-j)
        #   j=0: (q-1)*C(x,0)*C(n-x,1) = 2*(n-x)
        #   j=1: (-1)*(q-1)^0*C(x,1)*C(n-x,0) = -x
        # K_1(x;4,3) = 2*(4-x) - x = 8 - 3x
        # K_1(2;4,3) = 8 - 6 = 2
        assert KRAWTCHOUK_1_2 == 2

    def test_k1_at_3_eq_minus1(self):
        # K_1(3;4,3) = 8 - 9 = -1
        assert KRAWTCHOUK_1_3 == -1

    def test_k1_at_4_eq_minus4(self):
        # K_1(4;4,3) = 8 - 12 = -4
        assert KRAWTCHOUK_1_4 == -4

    def test_p_matrix_orthogonal(self):
        assert P_MATRIX_ORTHOGONAL is True

    def test_p_matrix_shape(self):
        assert len(P_MATRIX) == SCHEME_N + 1
        assert all(len(row) == SCHEME_N + 1 for row in P_MATRIX)

    def test_q_matrix_shape(self):
        assert len(Q_MATRIX) == SCHEME_N + 1
        assert all(len(row) == SCHEME_N + 1 for row in Q_MATRIX)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Simplex code Sim(4,3) weight distribution
# ─────────────────────────────────────────────────────────────────────────────

class TestSimplexWeightDistribution:
    def test_sim_size_is_81(self):
        assert SIM_SIZE == 81

    def test_sim_nonzero_is_80(self):
        assert SIM_NONZERO == 80

    def test_sim_min_dist_equals_k2(self):
        assert SIM_MIN_DIST == 27
        assert SIM_MIN_DIST == K2

    def test_sim_min_dist_formula(self):
        assert SIM_MIN_DIST == HAM_Q ** (HAM_R - 1)

    def test_sim_weight_dist_keys(self):
        assert 0 in SIM_WEIGHT_DIST
        assert SIM_MIN_DIST in SIM_WEIGHT_DIST
        assert len(SIM_WEIGHT_DIST) == 2

    def test_sim_a0_is_1(self):
        assert SIM_WEIGHT_DIST[0] == 1

    def test_sim_a27_is_80(self):
        assert SIM_WEIGHT_DIST[27] == 80

    def test_sim_total_is_81(self):
        assert sum(SIM_WEIGHT_DIST.values()) == SIM_SIZE


# ─────────────────────────────────────────────────────────────────────────────
# 4. MacWilliams transform
# ─────────────────────────────────────────────────────────────────────────────

class TestMacWilliamsTransform:
    def test_ham_a0_is_1(self):
        assert HAM_A0_IS_1 is True
        assert HAM_A0 == 1

    def test_ham_a1_is_0(self):
        assert HAM_A1 == 0

    def test_ham_a2_is_0(self):
        assert HAM_A2 == 0

    def test_ham_no_low_weights(self):
        assert HAM_NO_LOW_WEIGHTS is True

    def test_ham_a3_positive(self):
        assert HAM_A3 > 0

    def test_ham_total_correct(self):
        assert HAM_TOTAL_CHECK is True

    def test_ham_all_nonneg_int(self):
        assert HAM_ALL_NONNEG_INT is True

    def test_macwilliams_consistent(self):
        assert MACWILLIAMS_CONSISTENT is True

    def test_transform_returns_dict(self):
        result = macwilliams_transform(SIM_WEIGHT_DIST, HAM_N, HAM_K, HAM_Q)
        assert isinstance(result, dict)

    def test_transform_divisor_is_dual_size(self):
        # Manually: A_0 = (1/81) * (1*1 + 80*1) = 1
        result = macwilliams_transform({0: 1, 27: 80}, HAM_N, HAM_K, HAM_Q)
        assert result.get(0, Fraction(0)) == Fraction(1)


# ─────────────────────────────────────────────────────────────────────────────
# 5. Ham(4,3) weight distribution properties
# ─────────────────────────────────────────────────────────────────────────────

class TestHamWeightDistribution:
    def test_min_weight_is_3(self):
        nonzero = [w for w, v in HAM_WEIGHT_DIST.items() if w > 0 and v > 0]
        assert min(nonzero) == 3

    def test_all_weights_integer(self):
        for w, v in HAM_WEIGHT_DIST.items():
            assert v.denominator == 1

    def test_all_weights_nonneg(self):
        for w, v in HAM_WEIGHT_DIST.items():
            assert v >= 0

    def test_weight_0_count_is_1(self):
        assert HAM_WEIGHT_DIST[0] == Fraction(1)

    def test_total_is_3_pow_36(self):
        total = sum(HAM_WEIGHT_DIST.values())
        assert total == Fraction(HAM_Q ** HAM_K)

    def test_weights_at_most_n(self):
        assert all(w <= HAM_N for w in HAM_WEIGHT_DIST.keys())


# ─────────────────────────────────────────────────────────────────────────────
# 6. W(3,3) SRG eigenvalue derivation
# ─────────────────────────────────────────────────────────────────────────────

class TestSRGEigenvalues:
    def test_delta_is_36(self):
        assert DELTA == 36

    def test_sqrt_delta_is_6(self):
        assert SQRT_DELTA == 6
        assert SQRT_DELTA ** 2 == DELTA

    def test_eigenvalue_r_is_2(self):
        assert EIGENVALUE_R == 2

    def test_eigenvalue_s_is_minus4(self):
        assert EIGENVALUE_S == -4

    def test_srg_r_exact(self):
        assert SRG_R == Fraction(2)

    def test_srg_s_exact(self):
        assert SRG_S == Fraction(-4)

    def test_multiplicities_sum_to_v(self):
        assert MULT_R + MULT_S + 1 == V

    def test_mult_r_is_24(self):
        assert MULT_R == 24

    def test_mult_s_is_15(self):
        assert MULT_S == 15


# ─────────────────────────────────────────────────────────────────────────────
# 7. Coset leader / error correction
# ─────────────────────────────────────────────────────────────────────────────

class TestCosetLeaders:
    def test_expected_coset_leaders_wt1(self):
        assert EXPECTED_COSET_LEADERS_WT1 == 80

    def test_coset_leader_count_correct(self):
        assert COSET_LEADER_COUNT_CORRECT is True

    def test_coset_count_equals_sim_nonzero(self):
        assert EXPECTED_COSET_LEADERS_WT1 == SIM_NONZERO


# ─────────────────────────────────────────────────────────────────────────────
# 8. Verification functions
# ─────────────────────────────────────────────────────────────────────────────

class TestVerifyFunctions:
    def test_verify_scheme_all_true(self):
        result = verify_scheme_parameters()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_krawtchouk_all_true(self):
        result = verify_krawtchouk()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_weight_enumerator_all_true(self):
        result = verify_weight_enumerator()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_srg_all_true(self):
        result = verify_srg_connection()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_all_all_true(self):
        result = verify_all()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_all_count_is_22(self):
        assert len(verify_all()) == 22

    def test_verify_scheme_count_is_6(self):
        assert len(verify_scheme_parameters()) == 6

    def test_verify_krawtchouk_count_is_4(self):
        assert len(verify_krawtchouk()) == 4

    def test_verify_weight_count_is_6(self):
        assert len(verify_weight_enumerator()) == 6

    def test_verify_srg_count_is_6(self):
        assert len(verify_srg_connection()) == 6


# ─────────────────────────────────────────────────────────────────────────────
# 9. Build summary
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildSummary:
    def test_part_number(self):
        s = build_ccxc_summary()
        assert s["part_number"] == "CCXC"

    def test_verification_status_all_pass(self):
        s = build_ccxc_summary()
        assert s["verification_status"] == "ALL CHECKS PASS"

    def test_checks_pass_count(self):
        s = build_ccxc_summary()
        assert s["checks_pass"] == 22
        assert s["checks_total"] == 22

    def test_scheme_size_in_summary(self):
        s = build_ccxc_summary()
        assert s["scheme_parameters"]["size"] == 81

    def test_srg_eigenvalues_in_summary(self):
        s = build_ccxc_summary()
        assert s["srg_eigenvalues"]["r"] == 2
        assert s["srg_eigenvalues"]["s"] == -4

    def test_krawtchouk_k1_in_summary(self):
        s = build_ccxc_summary()
        assert s["krawtchouk_k1"]["K1(0)"] == 8
        assert s["krawtchouk_k1"]["K1(1)"] == 5
        assert s["krawtchouk_k1"]["K1(4)"] == -4

    def test_sim_weight_dist_in_summary(self):
        s = build_ccxc_summary()
        assert s["sim_weight_dist"][0] == 1
        assert s["sim_weight_dist"][27] == 80

    def test_key_discoveries_count(self):
        s = build_ccxc_summary()
        assert len(s["key_discoveries"]) == 7
