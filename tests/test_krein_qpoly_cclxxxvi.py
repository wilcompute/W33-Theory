"""
Tests for Part CCLXXXVI: Krein Parameters and Q-Polynomial Association Scheme of W(3,3)
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))
from PART_CCLXXXVI_KREIN_QPOLY_BRIDGE import (
    V, K, LAM, MU, Q,
    K2, K2_VAL, PHI4, PHI3, PHI6, LINES_27, EDGES, AUT_ORDER,
    TRANSPORT_EDGES, STABILIZER_STATES, E8_RANK, SP4F3_ORDER, PSP4F3_ORDER,
    DISCRIMINANT, R_EIGENVALUE, S_EIGENVALUE, R2_EIGENVALUE, S2_EIGENVALUE,
    MULT_R, MULT_S, DET_P,
    P_MATRIX, Q_MATRIX, Q_MATRIX_INT,
    P111, P112, P122, P211, P212, P222,
    P212_CORRECT, P222_CORRECT,
    KREIN_Q0_11, KREIN_Q0_22,
    KREIN_Q1_11, KREIN_Q1_12, KREIN_Q1_22,
    KREIN_Q2_11, KREIN_Q2_12, KREIN_Q2_22,
    CLIQUE_BOUND_HOFFMAN, INDSET_BOUND_HOFFMAN, ABSOLUTE_BOUND,
    DUAL_K0, DUAL_K1, DUAL_K2,
    Q_POLY_CONDITION,
    verify_srg_parameters, verify_p_matrix, verify_q_matrix,
    verify_krein_parameters, verify_intersection_numbers,
    verify_eigenvalue_multiplicities, verify_hoffman_bounds,
    verify_dual_scheme, verify_q_polynomial_chain, verify_scheme_numerology,
    verify_all, build_cclxxxvi_bridge_summary,
    krein_param,
)


# ── SRG parameter tests ───────────────────────────────────────────────────────

class TestSRGParameters:
    def test_v_eq_40(self): assert V == 40
    def test_k_eq_12(self): assert K == 12
    def test_lam_eq_2(self): assert LAM == 2
    def test_mu_eq_4(self): assert MU == 4
    def test_q_eq_3(self): assert Q == 3
    def test_k2_eq_27(self): assert K2 == 27
    def test_k2_eq_lines27(self): assert K2 == LINES_27
    def test_k_plus_k2_eq_v_minus_1(self): assert K + K2 == V - 1
    def test_k_times_k2_eq_324(self): assert K * K2 == 324
    def test_v_times_k_eq_lam_times_edges(self): assert V * K == LAM * EDGES


# ── SRG eigenvalue tests ──────────────────────────────────────────────────────

class TestEigenvalues:
    def test_discriminant_36(self): assert DISCRIMINANT == 36
    def test_discriminant_eq_lam_q_sq(self): assert DISCRIMINANT == (LAM * Q) ** 2
    def test_r_eigenvalue_eq_2(self): assert R_EIGENVALUE == 2
    def test_s_eigenvalue_eq_neg4(self): assert S_EIGENVALUE == -4
    def test_r_plus_s_eq_lam_minus_mu(self): assert R_EIGENVALUE + S_EIGENVALUE == LAM - MU
    def test_r_minus_s_eq_lam_q(self): assert R_EIGENVALUE - S_EIGENVALUE == LAM * Q
    def test_r_times_s_eq_neg8(self): assert R_EIGENVALUE * S_EIGENVALUE == -8
    def test_r2_eq_neg3(self): assert R2_EIGENVALUE == -3
    def test_s2_eq_3(self): assert S2_EIGENVALUE == 3
    def test_r2_eq_neg_q(self): assert R2_EIGENVALUE == -Q
    def test_s2_eq_q(self): assert S2_EIGENVALUE == Q
    def test_r2_plus_s2_eq_0(self): assert R2_EIGENVALUE + S2_EIGENVALUE == 0
    def test_r2_eq_neg_r_minus_1(self): assert R2_EIGENVALUE == -(R_EIGENVALUE + 1)
    def test_s2_eq_neg_s_minus_1(self): assert S2_EIGENVALUE == -(S_EIGENVALUE + 1)


# ── Eigenvalue multiplicity tests ────────────────────────────────────────────

class TestMultiplicities:
    def test_mult_r_eq_24(self): assert MULT_R == 24
    def test_mult_s_eq_15(self): assert MULT_S == 15
    def test_mult_sum_eq_v_minus_1(self): assert MULT_R + MULT_S == V - 1
    def test_mult_r_eq_lam_k(self): assert MULT_R == LAM * K
    def test_mult_r_eq_lines27_minus_q(self): assert MULT_R == LINES_27 - Q
    def test_mult_r_eq_mu_times_e8_minus_lam(self): assert MULT_R == MU * (E8_RANK - LAM)
    def test_mult_s_eq_q_times_q_plus_lam(self): assert MULT_S == Q * (Q + LAM)
    def test_dual_k1_eq_mult_r(self): assert DUAL_K1 == MULT_R
    def test_dual_k2_eq_mult_s(self): assert DUAL_K2 == MULT_S
    def test_dual_sum_eq_v_minus_1(self): assert DUAL_K1 + DUAL_K2 == V - 1


# ── P-matrix tests ────────────────────────────────────────────────────────────

class TestPMatrix:
    def test_p_row0(self): assert P_MATRIX[0] == [1, K, K2]
    def test_p_row1(self): assert P_MATRIX[1] == [1, R_EIGENVALUE, R2_EIGENVALUE]
    def test_p_row2(self): assert P_MATRIX[2] == [1, S_EIGENVALUE, S2_EIGENVALUE]
    def test_p_row0_sum_eq_v(self): assert sum(P_MATRIX[0]) == V
    def test_det_p_eq_neg240(self): assert DET_P == -240
    def test_det_p_eq_neg_edges(self): assert DET_P == -EDGES
    def test_p_col1_eigenvalues(self):
        assert [P_MATRIX[i][1] for i in range(3)] == [K, R_EIGENVALUE, S_EIGENVALUE]
    def test_p_col2_eigenvalues(self):
        assert [P_MATRIX[i][2] for i in range(3)] == [K2, R2_EIGENVALUE, S2_EIGENVALUE]
    def test_p_col0_ones(self):
        assert all(P_MATRIX[i][0] == 1 for i in range(3))


# ── Q-matrix tests ────────────────────────────────────────────────────────────

class TestQMatrix:
    def test_q_row0_eq_mults(self): assert Q_MATRIX_INT[0] == [1, MULT_R, MULT_S]
    def test_q_row1_col0_eq_1(self): assert Q_MATRIX_INT[1][0] == 1
    def test_q_row1_col1_eq_4(self): assert Q_MATRIX_INT[1][1] == 4
    def test_q_row1_col2_eq_neg5(self): assert Q_MATRIX_INT[1][2] == -5
    def test_q_dual_k1_eq_mu(self): assert Q_MATRIX_INT[1][1] == MU
    def test_q_dual_k2_eq_s_minus_1(self): assert Q_MATRIX_INT[1][2] == S_EIGENVALUE - 1
    def test_q_row0_sum_eq_v(self): assert sum(Q_MATRIX_INT[0]) == V
    def test_pq_product_vI_00(self):
        assert abs(sum(P_MATRIX[0][l] * Q_MATRIX[l][0] for l in range(3)) - V) < 1e-8
    def test_pq_product_vI_11(self):
        assert abs(sum(P_MATRIX[1][l] * Q_MATRIX[l][1] for l in range(3)) - V) < 1e-8
    def test_pq_product_vI_22(self):
        assert abs(sum(P_MATRIX[2][l] * Q_MATRIX[l][2] for l in range(3)) - V) < 1e-8
    def test_pq_off_diag_01_zero(self):
        assert abs(sum(P_MATRIX[0][l] * Q_MATRIX[l][1] for l in range(3))) < 1e-8
    def test_pq_off_diag_10_zero(self):
        assert abs(sum(P_MATRIX[1][l] * Q_MATRIX[l][0] for l in range(3))) < 1e-8
    def test_pq_off_diag_12_zero(self):
        assert abs(sum(P_MATRIX[1][l] * Q_MATRIX[l][2] for l in range(3))) < 1e-8


# ── Krein parameter tests ────────────────────────────────────────────────────

class TestKreinParameters:
    def test_q0_11_nonneg(self): assert KREIN_Q0_11 >= 0
    def test_q0_22_nonneg(self): assert KREIN_Q0_22 >= 0
    def test_q1_11_nonneg(self): assert KREIN_Q1_11 >= 0
    def test_q1_12_nonneg(self): assert KREIN_Q1_12 >= 0
    def test_q1_22_nonneg(self): assert KREIN_Q1_22 >= 0
    def test_q2_11_nonneg(self): assert KREIN_Q2_11 >= 0
    def test_q2_12_nonneg(self): assert KREIN_Q2_12 >= 0
    def test_q2_22_nonneg(self): assert KREIN_Q2_22 >= 0
    def test_q_poly_condition(self): assert Q_POLY_CONDITION
    def test_krein_q1_sum_nonneg(self): assert KREIN_Q1_11 + KREIN_Q1_12 + KREIN_Q1_22 >= 0
    def test_krein_q2_sum_nonneg(self): assert KREIN_Q2_11 + KREIN_Q2_12 + KREIN_Q2_22 >= 0
    def test_krein_all_nonneg(self):
        params = [KREIN_Q0_11, KREIN_Q0_22, KREIN_Q1_11, KREIN_Q1_12,
                  KREIN_Q1_22, KREIN_Q2_11, KREIN_Q2_12, KREIN_Q2_22]
        assert all(p >= 0 for p in params)
    def test_krein_param_symmetry_12_21(self):
        assert krein_param(1, 2, 1) == krein_param(2, 1, 1)
    def test_krein_param_symmetry_12_21_dual(self):
        assert krein_param(1, 2, 2) == krein_param(2, 1, 2)


# ── Intersection number tests ────────────────────────────────────────────────

class TestIntersectionNumbers:
    def test_p111_eq_lam(self): assert P111 == LAM
    def test_p112_eq_9(self): assert P112 == 9
    def test_p112_eq_k_minus_lam_minus_1(self): assert P112 == K - LAM - 1
    def test_p112_eq_k2_over_q(self): assert P112 == K2 // Q
    def test_p211_eq_mu(self): assert P211 == MU
    def test_p212_correct_eq_8(self): assert P212_CORRECT == 8
    def test_p212_correct_eq_k_minus_mu(self): assert P212_CORRECT == K - MU
    def test_p222_correct_eq_18(self): assert P222_CORRECT == 18
    def test_p222_correct_eq_k2_minus_1_minus_k_minus_mu(self):
        assert P222_CORRECT == K2 - 1 - (K - MU)
    def test_symmetry_k1_p112_eq_k2_p211(self): assert K * P112 == K2 * P211
    def test_p111_plus_p112_eq_k_minus_1(self): assert P111 + P112 == K - 1
    def test_p212_plus_p211_eq_k(self): assert P212_CORRECT + P211 == K


# ── Hoffman bound tests ──────────────────────────────────────────────────────

class TestHoffmanBounds:
    def test_clique_bound_eq_4(self): assert CLIQUE_BOUND_HOFFMAN == 4
    def test_clique_bound_eq_mu(self): assert CLIQUE_BOUND_HOFFMAN == MU
    def test_indset_bound_eq_10(self): assert INDSET_BOUND_HOFFMAN == 10
    def test_indset_bound_eq_phi4(self): assert INDSET_BOUND_HOFFMAN == PHI4
    def test_absolute_bound_eq_300(self): assert ABSOLUTE_BOUND == 300
    def test_absolute_bound_geq_v(self): assert ABSOLUTE_BOUND >= V
    def test_clique_times_indset_eq_v(self):
        assert CLIQUE_BOUND_HOFFMAN * INDSET_BOUND_HOFFMAN == V
    def test_hoffman_clique_formula(self):
        assert 1 - K // S_EIGENVALUE == MU
    def test_hoffman_indset_formula(self):
        assert V * (-S_EIGENVALUE) // (K - S_EIGENVALUE) == PHI4
    def test_absolute_bound_eq_mult_r_times_mult_r_plus_1_over_2(self):
        assert ABSOLUTE_BOUND == MULT_R * (MULT_R + 1) // 2


# ── Q-polynomial chain tests ─────────────────────────────────────────────────

class TestQPolynomialChain:
    def test_q_poly_condition_holds(self): assert Q_POLY_CONDITION
    def test_discriminant_eq_lam_q_sq(self): assert DISCRIMINANT == (LAM * Q) ** 2
    def test_sqrt_discriminant_eq_lam_q(self): assert 36 == (LAM * Q) ** 2
    def test_r_eq_lam_q_minus_lam_over_2(self):
        assert R_EIGENVALUE == (LAM * Q - LAM) // 2
    def test_s_eq_neg_lam_q_plus_lam_over_2(self):
        assert S_EIGENVALUE == -(LAM * Q + LAM) // 2
    def test_r_minus_s_eq_lam_q(self): assert R_EIGENVALUE - S_EIGENVALUE == LAM * Q
    def test_r_plus_s_eq_lam_minus_mu(self): assert R_EIGENVALUE + S_EIGENVALUE == LAM - MU
    def test_k_times_k2_eq_q_sq_times_discriminant(self):
        assert K * K2 == Q**2 * DISCRIMINANT


# ── Dual scheme tests ────────────────────────────────────────────────────────

class TestDualScheme:
    def test_dual_k0_eq_1(self): assert DUAL_K0 == 1
    def test_dual_k1_eq_24(self): assert DUAL_K1 == 24
    def test_dual_k2_eq_15(self): assert DUAL_K2 == 15
    def test_dual_sum_eq_v(self): assert DUAL_K0 + DUAL_K1 + DUAL_K2 == V
    def test_dual_k1_eq_lam_k(self): assert DUAL_K1 == LAM * K
    def test_dual_k2_eq_q_times_q_plus_lam(self): assert DUAL_K2 == Q * (Q + LAM)
    def test_r2_eq_neg_q(self): assert R2_EIGENVALUE == -Q
    def test_s2_eq_q(self): assert S2_EIGENVALUE == Q
    def test_dual_eigenval_sum_zero(self): assert R2_EIGENVALUE + S2_EIGENVALUE == 0


# ── Full verify_all test ──────────────────────────────────────────────────────

class TestVerifyAll:
    def test_all_checks_pass(self):
        results = verify_all()
        failed = [k for k, v in results.items() if not v]
        assert failed == [], f"Failed checks: {failed}"

    def test_total_check_count(self):
        results = verify_all()
        assert len(results) >= 100

    def test_bridge_summary_all_pass(self):
        summary = build_cclxxxvi_bridge_summary()
        assert summary["all_pass"] is True

    def test_bridge_summary_title(self):
        summary = build_cclxxxvi_bridge_summary()
        assert "CCLXXXVI" in summary["part"]

    def test_bridge_summary_part_eq_cclxxxvi(self):
        summary = build_cclxxxvi_bridge_summary()
        assert summary["part"] == "CCLXXXVI"

    def test_bridge_summary_total_checks(self):
        summary = build_cclxxxvi_bridge_summary()
        assert summary["total_checks"] >= 100

    def test_bridge_summary_srg_constants(self):
        summary = build_cclxxxvi_bridge_summary()
        assert summary["V"] == 40
        assert summary["K"] == 12
        assert summary["LAM"] == 2
        assert summary["MU"] == 4
        assert summary["Q"] == 3

    def test_bridge_summary_eigenvalues(self):
        summary = build_cclxxxvi_bridge_summary()
        assert summary["R_EIGENVALUE"] == 2
        assert summary["S_EIGENVALUE"] == -4
        assert summary["MULT_R"] == 24
        assert summary["MULT_S"] == 15

    def test_bridge_summary_krein_nonneg(self):
        summary = build_cclxxxvi_bridge_summary()
        for key in ["KREIN_Q1_11", "KREIN_Q1_12", "KREIN_Q1_22",
                    "KREIN_Q2_11", "KREIN_Q2_12", "KREIN_Q2_22"]:
            assert summary[key] >= 0, f"{key} = {summary[key]} < 0"
