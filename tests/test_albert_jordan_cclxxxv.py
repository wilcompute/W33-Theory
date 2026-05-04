"""
Tests for Part CCLXXXV: Albert Algebra, Exceptional Jordan Algebra, and the 27 Lines of W(3,3)
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "exploration"))

from PART_CCLXXXV_ALBERT_JORDAN_BRIDGE import (
    ALBERT_DIM,
    ALBERT_E6_DIM,
    ALBERT_E6_RANK,
    ALBERT_E6_ROOTS,
    ALBERT_F4_DIM,
    ALBERT_F4_ORDER_WEYL,
    ALBERT_F4_RANK,
    ALBERT_F4_ROOTS,
    ALBERT_MIN_IDEMPOTENTS,
    ALBERT_OCTONION_DIM,
    ALBERT_RANK,
    ALBERT_27_REP,
    AUT_ORDER,
    CUBIC_DOUBLE_SIXES,
    CUBIC_LINE_PAIRS_MEET,
    CUBIC_LINES,
    CUBIC_TRITANGENT_PLANES,
    CUBIC_TRITANGENTS,
    E6_WEYL_ORDER,
    E7_FUND_DIM,
    E8_ADJOINT_DIM,
    E8_RANK,
    E8_ROOT_COUNT,
    EDGES,
    GEWIRTZ_V,
    K,
    LAM,
    LINES_27,
    MU,
    PHI3,
    PHI4,
    PHI6,
    Q,
    SP4F3_ORDER,
    STABILIZER_STATES,
    TRANSPORT_EDGES,
    V,
    build_cclxxxv_bridge_summary,
    verify_albert_basic,
    verify_albert_idempotents,
    verify_comprehensive_constant_web,
    verify_cubic_surface,
    verify_e6_constants,
    verify_e6_root_system,
    verify_e8_connection,
    verify_f4_constants,
    verify_f4_weyl_subgroup,
    verify_jordan_peirce,
    verify_jordan_trace_and_norm,
    verify_lines_27_srg,
    verify_magic_square,
    verify_octonion_algebra,
    verify_psp4f3_connection,
    verify_srg_40_12_2_4_vs_schlaefli,
    verify_27_lines_combinatorics,
    verify_all,
)


# ──────────────────────────────────────────────────────────────────────────────
# Helper — every verify_* function must return all-True
# ──────────────────────────────────────────────────────────────────────────────

def _assert_all(check_dict: dict) -> None:
    failed = [k for k, v in check_dict.items() if not v]
    assert not failed, f"Failed checks: {failed}"


# ──────────────────────────────────────────────────────────────────────────────
# Core constants
# ──────────────────────────────────────────────────────────────────────────────

class TestCoreConstants:
    def test_srg_parameters(self):
        assert V == 40 and K == 12 and LAM == 2 and MU == 4 and Q == 3

    def test_lines_27_eq_albert_dim(self):
        assert LINES_27 == ALBERT_DIM == 27

    def test_e8_rank_eq_octonion_dim(self):
        assert E8_RANK == ALBERT_OCTONION_DIM == 8

    def test_e6_rank_eq_lam_times_q(self):
        assert ALBERT_E6_RANK == LAM * Q == 6

    def test_e6_roots_eq_72(self):
        assert ALBERT_E6_ROOTS == 72

    def test_e6_weyl_eq_aut_order(self):
        assert E6_WEYL_ORDER == AUT_ORDER == SP4F3_ORDER == 51840

    def test_e7_fund_eq_gewirtz(self):
        assert E7_FUND_DIM == GEWIRTZ_V == 56

    def test_e8_roots_eq_edges(self):
        assert E8_ROOT_COUNT == EDGES == 240

    def test_phi4_eq_10(self):
        assert PHI4 == 10

    def test_transport_edges_eq_lines_27_times_phi4(self):
        assert TRANSPORT_EDGES == LINES_27 * PHI4


# ──────────────────────────────────────────────────────────────────────────────
# Albert basic verify
# ──────────────────────────────────────────────────────────────────────────────

class TestAlbertBasic:
    def test_all_checks_pass(self):
        _assert_all(verify_albert_basic())

    def test_albert_dim_27(self):
        assert ALBERT_DIM == 27

    def test_albert_rank_q(self):
        assert ALBERT_RANK == Q

    def test_min_idempotents_27(self):
        assert ALBERT_MIN_IDEMPOTENTS == LINES_27

    def test_octonion_dim_e8_rank(self):
        assert ALBERT_OCTONION_DIM == E8_RANK

    def test_dim_identity(self):
        assert ALBERT_DIM == K + PHI6 * LAM + 1


# ──────────────────────────────────────────────────────────────────────────────
# F₄ constants
# ──────────────────────────────────────────────────────────────────────────────

class TestF4Constants:
    def test_all_checks_pass(self):
        _assert_all(verify_f4_constants())

    def test_f4_rank_4(self):
        assert ALBERT_F4_RANK == 4

    def test_f4_roots_48(self):
        assert ALBERT_F4_ROOTS == MU * K == 48

    def test_f4_dim_52(self):
        assert ALBERT_F4_DIM == 52

    def test_f4_weyl_1152(self):
        assert ALBERT_F4_ORDER_WEYL == 1152

    def test_e6_weyl_over_f4_weyl_eq_45(self):
        assert E6_WEYL_ORDER // ALBERT_F4_ORDER_WEYL == 45

    def test_45_eq_lines_plus_e8_plus_phi4(self):
        assert LINES_27 + E8_RANK + PHI4 == 45


# ──────────────────────────────────────────────────────────────────────────────
# E₆ constants
# ──────────────────────────────────────────────────────────────────────────────

class TestE6Constants:
    def test_all_checks_pass(self):
        _assert_all(verify_e6_constants())

    def test_e6_rank_6(self):
        assert ALBERT_E6_RANK == 6

    def test_e6_roots_72(self):
        assert ALBERT_E6_ROOTS == 72

    def test_e6_dim_78(self):
        assert ALBERT_E6_DIM == 78

    def test_e6_27_rep(self):
        assert ALBERT_27_REP == LINES_27

    def test_e6_weyl_eq_aut(self):
        assert E6_WEYL_ORDER == AUT_ORDER

    def test_e6_dim_eq_roots_plus_rank(self):
        assert ALBERT_E6_DIM == ALBERT_E6_ROOTS + ALBERT_E6_RANK

    def test_e6_dim_eq_lam_phi3_q(self):
        assert ALBERT_E6_DIM == LAM * PHI3 * Q


# ──────────────────────────────────────────────────────────────────────────────
# Cubic surface
# ──────────────────────────────────────────────────────────────────────────────

class TestCubicSurface:
    def test_all_checks_pass(self):
        _assert_all(verify_cubic_surface())

    def test_cubic_lines_27(self):
        assert CUBIC_LINES == LINES_27

    def test_cubic_tritangents_45(self):
        assert CUBIC_TRITANGENTS == 45

    def test_cubic_double_sixes_36(self):
        assert CUBIC_DOUBLE_SIXES == 36

    def test_double_sixes_eq_51840_over_1440(self):
        assert CUBIC_DOUBLE_SIXES == 51840 // 1440

    def test_tritangents_eq_transport_over_lam_q(self):
        assert CUBIC_TRITANGENTS == TRANSPORT_EDGES // (LAM * Q)


# ──────────────────────────────────────────────────────────────────────────────
# Freudenthal magic square
# ──────────────────────────────────────────────────────────────────────────────

class TestMagicSquare:
    def test_all_checks_pass(self):
        _assert_all(verify_magic_square())

    def test_e6_dim_78(self):
        assert ALBERT_E6_DIM == 78

    def test_e8_adj_248(self):
        assert E8_ADJOINT_DIM == 248

    def test_e7_fund_56(self):
        assert E7_FUND_DIM == 56

    def test_e8_roots_240(self):
        assert E8_ROOT_COUNT == 240

    def test_e8_adjoint_eq_roots_plus_rank(self):
        assert E8_ADJOINT_DIM == E8_ROOT_COUNT + E8_RANK

    def test_e6_minus_f4_eq_lam_phi3(self):
        assert ALBERT_E6_DIM - ALBERT_F4_DIM == LAM * PHI3


# ──────────────────────────────────────────────────────────────────────────────
# Jordan Peirce decomposition
# ──────────────────────────────────────────────────────────────────────────────

class TestJordanPeirce:
    def test_all_checks_pass(self):
        _assert_all(verify_jordan_peirce())

    def test_peirce_diagonal_dim(self):
        assert ALBERT_RANK * 1 == Q

    def test_peirce_off_diagonal_dim(self):
        off = ALBERT_RANK * (ALBERT_RANK - 1) // 2 * ALBERT_OCTONION_DIM
        assert off == LAM * K == 24

    def test_peirce_total(self):
        diag = ALBERT_RANK
        off = ALBERT_RANK * (ALBERT_RANK - 1) // 2 * ALBERT_OCTONION_DIM
        assert diag + off == ALBERT_DIM == 27

    def test_peirce_off_eq_2k(self):
        off = ALBERT_RANK * (ALBERT_RANK - 1) // 2 * ALBERT_OCTONION_DIM
        assert off == LAM * K

    def test_peirce_off_eq_stabilizer_divisor(self):
        off = ALBERT_RANK * (ALBERT_RANK - 1) // 2 * ALBERT_OCTONION_DIM
        assert off == STABILIZER_STATES // (LINES_27 - K)


# ──────────────────────────────────────────────────────────────────────────────
# 27 lines combinatorics
# ──────────────────────────────────────────────────────────────────────────────

class TestLines27Combinatorics:
    def test_all_checks_pass(self):
        _assert_all(verify_27_lines_combinatorics())

    def test_line_degree_phi4(self):
        assert PHI4 == 10

    def test_total_incidence_270(self):
        assert LINES_27 * PHI4 == TRANSPORT_EDGES

    def test_meeting_pairs_135(self):
        assert CUBIC_LINE_PAIRS_MEET == 135

    def test_total_pairs_351(self):
        assert LINES_27 * (LINES_27 - 1) // 2 == 351

    def test_non_meeting_pairs_216(self):
        assert 351 - CUBIC_LINE_PAIRS_MEET == 216

    def test_non_meeting_eq_lam_q_cubed(self):
        assert 216 == (LAM * Q) ** 3

    def test_non_meeting_eq_lines_27_times_e8_rank(self):
        assert 216 == LINES_27 * E8_RANK


# ──────────────────────────────────────────────────────────────────────────────
# E₈ connection
# ──────────────────────────────────────────────────────────────────────────────

class TestE8Connection:
    def test_all_checks_pass(self):
        _assert_all(verify_e8_connection())

    def test_e8_roots_eq_edges(self):
        assert E8_ROOT_COUNT == EDGES

    def test_e8_rank_8(self):
        assert E8_RANK == 8

    def test_e8_roots_over_lam_q_eq_v(self):
        assert E8_ROOT_COUNT // (LAM * Q) == V

    def test_e8_rank_eq_k_minus_mu(self):
        assert E8_RANK == K - MU

    def test_e8_roots_over_k_eq_lam_phi4(self):
        assert E8_ROOT_COUNT // K == LAM * PHI4


# ──────────────────────────────────────────────────────────────────────────────
# Octonion algebra
# ──────────────────────────────────────────────────────────────────────────────

class TestOctonionAlgebra:
    def test_all_checks_pass(self):
        _assert_all(verify_octonion_algebra())

    def test_octonion_dim_8(self):
        assert ALBERT_OCTONION_DIM == E8_RANK == 8

    def test_g2_roots_eq_k(self):
        G2_ROOTS = 12
        assert G2_ROOTS == K

    def test_g2_dim_14(self):
        G2_DIM = 14
        assert G2_DIM == K + LAM

    def test_off_diag_calculation(self):
        off = (ALBERT_RANK * (ALBERT_RANK - 1) // 2) * ALBERT_OCTONION_DIM
        assert off == LAM * K

    def test_albert_total(self):
        total = ALBERT_RANK + (ALBERT_RANK * (ALBERT_RANK - 1) // 2) * ALBERT_OCTONION_DIM
        assert total == ALBERT_DIM


# ──────────────────────────────────────────────────────────────────────────────
# Jordan trace and norm
# ──────────────────────────────────────────────────────────────────────────────

class TestJordanTraceAndNorm:
    def test_all_checks_pass(self):
        _assert_all(verify_jordan_trace_and_norm())

    def test_norm_degree_q(self):
        assert ALBERT_RANK == Q == 3

    def test_trace_form_rank(self):
        assert ALBERT_DIM == LINES_27

    def test_e6_dim_eq_rank_times_phi3(self):
        assert ALBERT_E6_DIM == ALBERT_E6_RANK * PHI3

    def test_e6_27_rep_eq_albert(self):
        assert ALBERT_27_REP == ALBERT_DIM


# ──────────────────────────────────────────────────────────────────────────────
# PSp(4,3) / Sp(4,3) connection
# ──────────────────────────────────────────────────────────────────────────────

class TestPSp4F3Connection:
    def test_all_checks_pass(self):
        _assert_all(verify_psp4f3_connection())

    def test_sp4f3_eq_e6_weyl(self):
        assert SP4F3_ORDER == E6_WEYL_ORDER

    def test_sp4f3_factored(self):
        assert SP4F3_ORDER == 2**7 * 3**4 * 5

    def test_sp4f3_over_v_eq_lam_q_to_4(self):
        assert SP4F3_ORDER // V == (LAM * Q) ** 4

    def test_sp4f3_over_lines_27(self):
        assert SP4F3_ORDER // LINES_27 == 1920


# ──────────────────────────────────────────────────────────────────────────────
# E₆ root system
# ──────────────────────────────────────────────────────────────────────────────

class TestE6RootSystem:
    def test_all_checks_pass(self):
        _assert_all(verify_e6_root_system())

    def test_e6_roots_72(self):
        assert ALBERT_E6_ROOTS == 72

    def test_e6_pos_roots_36(self):
        assert ALBERT_E6_ROOTS // 2 == 36

    def test_pos_roots_eq_double_sixes(self):
        assert ALBERT_E6_ROOTS // 2 == CUBIC_DOUBLE_SIXES

    def test_pos_roots_eq_q_k(self):
        assert ALBERT_E6_ROOTS // 2 == Q * K

    def test_e6_dim_from_roots_rank(self):
        assert ALBERT_E6_ROOTS + ALBERT_E6_RANK == ALBERT_E6_DIM

    def test_pos_neg_rank_sum(self):
        pos = ALBERT_E6_ROOTS // 2
        assert pos + pos + ALBERT_E6_RANK == ALBERT_E6_DIM


# ──────────────────────────────────────────────────────────────────────────────
# Schläfli SRG(27,10,1,5)
# ──────────────────────────────────────────────────────────────────────────────

class TestSchlaefliSRG:
    def test_all_checks_pass(self):
        _assert_all(verify_lines_27_srg())

    def test_srg_params(self):
        V_S, K_S, L_S, M_S = 27, 10, 1, 5
        assert V_S == LINES_27
        assert K_S == PHI4
        assert M_S == Q + LAM

    def test_srg_feasibility(self):
        assert 10 * (10 - 1 - 1) == (27 - 10 - 1) * 5

    def test_discriminant_36(self):
        assert (1 - 5) ** 2 + 4 * (10 - 5) == 36

    def test_eigenvalues(self):
        assert (1 - 5 + 6) // 2 == 1
        assert (1 - 5 - 6) // 2 == -5

    def test_multiplicities(self):
        assert 20 == LAM * PHI4
        assert 6 == LAM * Q

    def test_schlaefli_edges(self):
        assert 27 * 10 // 2 == CUBIC_LINE_PAIRS_MEET


# ──────────────────────────────────────────────────────────────────────────────
# SRG(40,12,2,4) vs Schläfli comparison
# ──────────────────────────────────────────────────────────────────────────────

class TestSRGComparison:
    def test_all_checks_pass(self):
        _assert_all(verify_srg_40_12_2_4_vs_schlaefli())

    def test_both_discriminant_36(self):
        disc_w33 = (LAM - MU) ** 2 + 4 * (K - MU)
        disc_sch = (1 - 5) ** 2 + 4 * (10 - 5)
        assert disc_w33 == disc_sch == 36

    def test_v_diff_eq_phi3(self):
        assert V - LINES_27 == PHI3

    def test_k_diff_eq_lam(self):
        assert K - PHI4 == LAM

    def test_eigenvalue_sum_neg_q(self):
        # W33 r=2, Schlaefli s=-5; sum = -3 = -Q
        assert 2 + (-5) == -Q


# ──────────────────────────────────────────────────────────────────────────────
# F₄ as subgroup of E₆
# ──────────────────────────────────────────────────────────────────────────────

class TestF4SubgroupE6:
    def test_all_checks_pass(self):
        _assert_all(verify_f4_weyl_subgroup())

    def test_index_45(self):
        assert E6_WEYL_ORDER // ALBERT_F4_ORDER_WEYL == 45

    def test_index_eq_tritangents(self):
        assert E6_WEYL_ORDER // ALBERT_F4_ORDER_WEYL == CUBIC_TRITANGENTS

    def test_index_eq_lines_plus_e8_plus_phi4(self):
        assert LINES_27 + E8_RANK + PHI4 == 45

    def test_f4_weyl_factored(self):
        assert ALBERT_F4_ORDER_WEYL == 2**7 * 3**2

    def test_f4_weyl_eq_mu_lam_k_sq(self):
        assert ALBERT_F4_ORDER_WEYL == MU * LAM * K * K


# ──────────────────────────────────────────────────────────────────────────────
# Albert algebra primitive idempotents
# ──────────────────────────────────────────────────────────────────────────────

class TestAlbertIdempotents:
    def test_all_checks_pass(self):
        _assert_all(verify_albert_idempotents())

    def test_primitive_idempotents_27(self):
        assert ALBERT_MIN_IDEMPOTENTS == LINES_27

    def test_rank1_cone_dim_16(self):
        RANK1_DIM = 16
        assert RANK1_DIM == 1 + ALBERT_OCTONION_DIM + ALBERT_OCTONION_DIM - 1

    def test_idempotent_pairs(self):
        assert ALBERT_MIN_IDEMPOTENTS * (ALBERT_MIN_IDEMPOTENTS - 1) // 2 == 351

    def test_orthogonal_pairs_135(self):
        assert CUBIC_LINE_PAIRS_MEET == 135

    def test_non_orth_eq_lam_q_cubed(self):
        assert 351 - CUBIC_LINE_PAIRS_MEET == (LAM * Q) ** 3


# ──────────────────────────────────────────────────────────────────────────────
# Comprehensive constant web
# ──────────────────────────────────────────────────────────────────────────────

class TestComprehensiveConstantWeb:
    def test_all_checks_pass(self):
        _assert_all(verify_comprehensive_constant_web())

    def test_exceptional_ranks_sum_27(self):
        # G2(2) + F4(4) + E6(6) + E7(7) + E8(8) = 27
        assert 2 + 4 + 6 + 7 + 8 == LINES_27

    def test_e7_rank_eq_phi6(self):
        assert 7 == PHI6

    def test_f4_rank_eq_mu(self):
        assert ALBERT_F4_RANK == MU

    def test_transport_eq_lines_times_phi4(self):
        assert TRANSPORT_EDGES == LINES_27 * PHI4

    def test_v_times_k_eq_lam_edges(self):
        assert V * K == LAM * EDGES

    def test_e6_roots_div_rank_eq_k(self):
        assert ALBERT_E6_ROOTS // ALBERT_E6_RANK == K

    def test_f4_roots_div_rank_eq_k(self):
        assert ALBERT_F4_ROOTS // ALBERT_F4_RANK == K


# ──────────────────────────────────────────────────────────────────────────────
# Full verify_all and summary
# ──────────────────────────────────────────────────────────────────────────────

class TestVerifyAll:
    def test_verify_all_all_pass(self):
        checks = verify_all()
        failed = [k for k, v in checks.items() if not v]
        assert not failed, f"Failed: {failed}"

    def test_verify_all_count(self):
        checks = verify_all()
        assert len(checks) >= 140

    def test_summary_all_pass(self):
        s = build_cclxxxv_bridge_summary()
        assert s["all_pass"] is True

    def test_summary_fields(self):
        s = build_cclxxxv_bridge_summary()
        assert s["part"] == "CCLXXXV"
        assert s["LINES_27"] == 27
        assert s["ALBERT_DIM"] == 27
        assert s["E6_WEYL_ORDER"] == 51840
        assert s["CUBIC_DOUBLE_SIXES"] == 36

    def test_key_identities_present(self):
        s = build_cclxxxv_bridge_summary()
        assert len(s["key_identities"]) >= 10

    def test_sections_present(self):
        s = build_cclxxxv_bridge_summary()
        assert len(s["sections"]) >= 15
