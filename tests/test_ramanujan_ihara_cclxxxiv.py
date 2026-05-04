"""
Tests for Part CCLXXXIV: Ramanujan Graph Spectrum, Ihara Zeta Function,
and the W(3,3) Expander Atlas.
"""

import math
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'exploration'))

from PART_CCLXXXIV_RAMANUJAN_IHARA_BRIDGE import (
    V, K, LAM, MU, Q, PHI4, PHI3, PHI6, LINES_27, EDGES, AUT_ORDER,
    E8_RANK, LAP_TOP, LAP_MID, STABILIZER_STATES,
    ADJ_EV_K, ADJ_EV_R, ADJ_EV_S, MULT_K, MULT_R, MULT_S,
    SEIDEL_EV_TRIV, SEIDEL_EV_R, SEIDEL_EV_S,
    IHARA_EULER_FACTOR, K_MINUS_1, HASHIMOTO_MODULUS_SQ,
    HASH_IM_SQ_FROM_R, HASH_IM_SQ_FROM_S,
    SPECTRAL_GAP, ALGE_CONN,
    verify_srg_eigenvalue_formula,
    verify_eigenvalue_multiplicities,
    verify_ramanujan_condition,
    verify_laplacian_spectrum,
    verify_laplacian_constant_meanings,
    verify_signless_laplacian,
    verify_seidel_matrix,
    verify_two_graph_condition,
    verify_trace_moments,
    verify_ihara_euler_factor,
    verify_ihara_k_minus_1,
    verify_ihara_trivial_eigenvalue,
    verify_ihara_non_trivial_factors,
    verify_hashimoto_imaginary_parts,
    verify_graph_riemann_hypothesis,
    verify_spectral_gap,
    verify_random_walk,
    verify_expander_mixing_lemma,
    verify_alon_boppana,
    verify_cheeger_bounds,
    verify_ramanujan_modular_form_weight,
    verify_ramanujan_tau_k,
    verify_w33_spectrum_synopsis,
    verify_eigenvalue_polynomial,
    build_cclxxxiv_bridge_summary,
)


# ===========================================================================
# Section 1: Core W(3,3) constants
# ===========================================================================
class TestCoreConstants:
    def test_V(self):        assert V == 40
    def test_K(self):        assert K == 12
    def test_LAM(self):      assert LAM == 2
    def test_MU(self):       assert MU == 4
    def test_Q(self):        assert Q == 3
    def test_PHI4(self):     assert PHI4 == 10
    def test_PHI3(self):     assert PHI3 == 13
    def test_PHI6(self):     assert PHI6 == 7
    def test_LINES_27(self): assert LINES_27 == 27
    def test_EDGES(self):    assert EDGES == 240
    def test_E8_RANK(self):  assert E8_RANK == 8
    def test_LAP_TOP(self):  assert LAP_TOP == 16
    def test_LAP_MID(self):  assert LAP_MID == 10
    def test_STABILIZER_STATES(self): assert STABILIZER_STATES == 360

    def test_EDGES_from_VK(self):
        assert EDGES == V * K // 2

    def test_PHI4_as_Q2_plus1(self):
        assert PHI4 == Q**2 + 1

    def test_PHI6_as_Q2_minus_Q_plus1(self):
        assert PHI6 == Q**2 - Q + 1

    def test_PHI3_as_Q2_plus_Q_plus1(self):
        assert PHI3 == Q**2 + Q + 1


# ===========================================================================
# Section 2: Adjacency eigenvalues
# ===========================================================================
class TestAdjacencyEigenvalues:
    def test_r_eq_2(self):
        assert ADJ_EV_R == 2

    def test_s_eq_neg4(self):
        assert ADJ_EV_S == -4

    def test_r_eq_LAM(self):
        assert ADJ_EV_R == LAM

    def test_s_eq_neg_MU(self):
        assert ADJ_EV_S == -MU

    def test_eigenvalues_decreasing(self):
        assert ADJ_EV_K > ADJ_EV_R > ADJ_EV_S

    def test_delta_eq_36(self):
        delta = (LAM - MU)**2 + 4*(K - MU)
        assert delta == 36

    def test_r_from_formula(self):
        delta = (LAM - MU)**2 + 4*(K - MU)
        r = (LAM - MU + int(math.isqrt(delta))) // 2
        assert r == 2

    def test_s_from_formula(self):
        delta = (LAM - MU)**2 + 4*(K - MU)
        s = (LAM - MU - int(math.isqrt(delta))) // 2
        assert s == -4

    def test_K_plus_r_plus_s_eq_PHI4(self):
        assert ADJ_EV_K + ADJ_EV_R + ADJ_EV_S == PHI4

    def test_K_times_r_times_s(self):
        assert ADJ_EV_K * ADJ_EV_R * ADJ_EV_S == -E8_RANK * K


# ===========================================================================
# Section 3: Eigenvalue multiplicities
# ===========================================================================
class TestEigenvalueMultiplicities:
    def test_MULT_K(self):
        assert MULT_K == 1

    def test_MULT_R(self):
        assert MULT_R == 24

    def test_MULT_R_eq_2K(self):
        assert MULT_R == 2 * K

    def test_MULT_S(self):
        assert MULT_S == 15

    def test_MULT_S_eq_LINES27_minus_K(self):
        assert MULT_S == LINES_27 - K

    def test_mults_sum_to_V(self):
        assert MULT_K + MULT_R + MULT_S == V

    def test_trace_A_eq_0(self):
        assert ADJ_EV_K * MULT_K + ADJ_EV_R * MULT_R + ADJ_EV_S * MULT_S == 0

    def test_trace_A2_eq_2_EDGES(self):
        tr2 = K**2 + MULT_R * ADJ_EV_R**2 + MULT_S * ADJ_EV_S**2
        assert tr2 == 2 * EDGES

    def test_MULT_R_plus_MULT_S_eq_Vminus1(self):
        assert MULT_R + MULT_S == V - 1

    def test_MULT_R_times_MULT_S_eq_STABILIZER_STATES(self):
        assert MULT_R * MULT_S == STABILIZER_STATES


# ===========================================================================
# Section 4: Ramanujan condition
# ===========================================================================
class TestRamanujanCondition:
    def test_spectral_radius_eq_MU(self):
        assert max(abs(ADJ_EV_R), abs(ADJ_EV_S)) == MU

    def test_ramanujan_bound_sq(self):
        assert 4 * K_MINUS_1 == 44

    def test_r_sq_satisfies_ramanujan(self):
        assert ADJ_EV_R**2 <= 4 * K_MINUS_1

    def test_s_sq_satisfies_ramanujan(self):
        assert ADJ_EV_S**2 <= 4 * K_MINUS_1

    def test_strictly_ramanujan(self):
        assert max(abs(ADJ_EV_R), abs(ADJ_EV_S)) < 2 * math.sqrt(K_MINUS_1)

    def test_alon_boppana_gap_sq(self):
        # 4*(K-1) - MU^2 = 44 - 16 = 28 = MU * PHI6
        gap_sq = 4 * K_MINUS_1 - MU**2
        assert gap_sq == 28
        assert gap_sq == MU * PHI6


# ===========================================================================
# Section 5: Laplacian spectrum
# ===========================================================================
class TestLaplacianSpectrum:
    def test_laplacian_ev0(self):
        assert K - K == 0

    def test_laplacian_ev1_eq_PHI4(self):
        assert K - ADJ_EV_R == PHI4

    def test_laplacian_ev1_eq_LAP_MID(self):
        assert K - ADJ_EV_R == LAP_MID

    def test_laplacian_ev2_eq_LAP_TOP(self):
        assert K - ADJ_EV_S == LAP_TOP

    def test_laplacian_ev2_eq_K_plus_MU(self):
        assert K + MU == LAP_TOP

    def test_laplacian_ev2_eq_16(self):
        assert K - ADJ_EV_S == 16

    def test_fiedler_value_eq_PHI4(self):
        assert ALGE_CONN == PHI4

    def test_K_minus_LAM_eq_PHI4(self):
        assert K - LAM == PHI4

    def test_lap_top_eq_2_E8_RANK(self):
        assert LAP_TOP == 2 * E8_RANK


# ===========================================================================
# Section 6: Signless Laplacian
# ===========================================================================
class TestSignlessLaplacian:
    def test_sl_ev_K_eq_2K(self):
        assert K + ADJ_EV_K == 2 * K

    def test_sl_ev_r_eq_14(self):
        assert K + ADJ_EV_R == 14

    def test_sl_ev_s_eq_E8_RANK(self):
        assert K + ADJ_EV_S == E8_RANK

    def test_sl_ev_s_eq_8(self):
        assert K + ADJ_EV_S == 8


# ===========================================================================
# Section 7: Seidel matrix
# ===========================================================================
class TestSeidelMatrix:
    def test_seidel_triv_eq_15(self):
        assert SEIDEL_EV_TRIV == 15

    def test_seidel_from_r_eq_neg5(self):
        assert SEIDEL_EV_R == -5

    def test_seidel_from_s_eq_PHI6(self):
        assert SEIDEL_EV_S == PHI6

    def test_seidel_from_s_eq_7(self):
        assert SEIDEL_EV_S == 7

    def test_seidel_formula_from_s(self):
        assert -1 - 2 * ADJ_EV_S == PHI6

    def test_seidel_trace_eq_0(self):
        trace = SEIDEL_EV_TRIV + MULT_R * SEIDEL_EV_R + MULT_S * SEIDEL_EV_S
        assert trace == 0

    def test_seidel_mults_sum_to_V(self):
        assert 1 + MULT_R + MULT_S == V


# ===========================================================================
# Section 8: Two-graph condition
# ===========================================================================
class TestTwoGraphCondition:
    def test_lam_eq_mu_minus_2(self):
        assert LAM == MU - 2

    def test_two_graph_seidel_triv(self):
        assert V - 1 - 2 * K == 15

    def test_triangles_eq_160(self):
        assert V * K * LAM // 6 == 160

    def test_trace_A3_eq_960(self):
        tr3 = K**3 + MULT_R * ADJ_EV_R**3 + MULT_S * ADJ_EV_S**3
        assert tr3 == 960

    def test_trace_A3_eq_MU_EDGES(self):
        tr3 = K**3 + MULT_R * ADJ_EV_R**3 + MULT_S * ADJ_EV_S**3
        assert tr3 == MU * EDGES


# ===========================================================================
# Section 9: Ihara zeta constants
# ===========================================================================
class TestIharaZeta:
    def test_ihara_euler_factor_eq_200(self):
        assert IHARA_EULER_FACTOR == 200

    def test_ihara_euler_factor_eq_5V(self):
        assert IHARA_EULER_FACTOR == 5 * V

    def test_ihara_ef_formula(self):
        assert EDGES - V == IHARA_EULER_FACTOR

    def test_K_minus_1_eq_11(self):
        assert K_MINUS_1 == 11

    def test_K_minus_1_is_prime(self):
        n = K_MINUS_1
        assert all(n % i != 0 for i in range(2, n))

    def test_K1_eq_PHI4_plus1(self):
        assert K_MINUS_1 == PHI4 + 1

    def test_K1_eq_PHI6_plus_MU(self):
        assert K_MINUS_1 == PHI6 + MU

    def test_K1_eq_PHI3_minus_LAM(self):
        assert K_MINUS_1 == PHI3 - LAM

    def test_disc_r_negative(self):
        disc_r = ADJ_EV_R**2 - 4 * K_MINUS_1
        assert disc_r < 0

    def test_disc_r_eq_neg40(self):
        disc_r = ADJ_EV_R**2 - 4 * K_MINUS_1
        assert disc_r == -40

    def test_disc_s_negative(self):
        disc_s = ADJ_EV_S**2 - 4 * K_MINUS_1
        assert disc_s < 0

    def test_disc_s_eq_neg28(self):
        disc_s = ADJ_EV_S**2 - 4 * K_MINUS_1
        assert disc_s == -28

    def test_trivial_factor_root_at_1(self):
        # (1 - K*u + (K-1)*u^2) at u=1: 1 - K + K - 1 = 0
        assert 1 - K + K_MINUS_1 == 0


# ===========================================================================
# Section 10: Hashimoto eigenvalues
# ===========================================================================
class TestHashimotoEigenvalues:
    def test_hashimoto_modulus_sq_eq_K1(self):
        assert HASHIMOTO_MODULUS_SQ == K_MINUS_1

    def test_hash_im_sq_from_r_eq_PHI4(self):
        assert HASH_IM_SQ_FROM_R == PHI4

    def test_hash_im_sq_from_r_eq_10(self):
        assert HASH_IM_SQ_FROM_R == 10

    def test_hash_im_sq_from_s_eq_PHI6(self):
        assert HASH_IM_SQ_FROM_S == PHI6

    def test_hash_im_sq_from_s_eq_7(self):
        assert HASH_IM_SQ_FROM_S == 7

    def test_hash_re_from_r_plus_im_sq_eq_K1(self):
        re_r = ADJ_EV_R // 2
        assert re_r**2 + HASH_IM_SQ_FROM_R == K_MINUS_1

    def test_hash_re_from_s_plus_im_sq_eq_K1(self):
        re_s = ADJ_EV_S // 2
        assert re_s**2 + HASH_IM_SQ_FROM_S == K_MINUS_1

    def test_hash_both_modulus_sq_equal(self):
        re_r = ADJ_EV_R // 2
        re_s = ADJ_EV_S // 2
        assert re_r**2 + HASH_IM_SQ_FROM_R == re_s**2 + HASH_IM_SQ_FROM_S

    def test_PHI4_plus1_eq_K1(self):
        assert PHI4 + 1 == K_MINUS_1

    def test_PHI6_plus_MU_eq_K1(self):
        assert PHI6 + MU == K_MINUS_1


# ===========================================================================
# Section 11: Spectral gap and expansion
# ===========================================================================
class TestSpectralGap:
    def test_spectral_gap_eq_8(self):
        assert SPECTRAL_GAP == 8

    def test_spectral_gap_eq_E8_RANK(self):
        assert SPECTRAL_GAP == E8_RANK

    def test_spectral_gap_eq_K_minus_MU(self):
        assert SPECTRAL_GAP == K - MU

    def test_algebraic_connectivity_eq_PHI4(self):
        assert ALGE_CONN == PHI4

    def test_algebraic_connectivity_eq_10(self):
        assert ALGE_CONN == 10

    def test_alge_conn_eq_K_minus_LAM(self):
        assert ALGE_CONN == K - LAM


# ===========================================================================
# Section 12: Random walk
# ===========================================================================
class TestRandomWalk:
    def test_second_ev_MU_Q_eq_K(self):
        # |s|/K = MU/K = 1/Q iff MU*Q = K
        assert MU * Q == K

    def test_random_walk_gap_numerator(self):
        assert K - MU == E8_RANK

    def test_lazy_walk_ev_numerator_eq_LAP_TOP(self):
        assert K + MU == LAP_TOP

    def test_rw_second_ev_lt_1(self):
        assert MU < K

    def test_rw_spectral_gap_pos(self):
        assert K > MU


# ===========================================================================
# Section 13: Expander mixing lemma
# ===========================================================================
class TestExpanderMixingLemma:
    def test_eml_eigenvalue(self):
        assert abs(ADJ_EV_S) == MU

    def test_eml_full_set(self):
        assert abs(2 * EDGES - K * V) == 0

    def test_eml_mean_half_V(self):
        eml_mean = K * (V // 2)**2 // V
        assert eml_mean == 120

    def test_eml_error_half_V(self):
        eml_error = abs(ADJ_EV_S) * (V // 2)
        assert eml_error == 80


# ===========================================================================
# Section 14: Alon-Boppana
# ===========================================================================
class TestAlonBoppana:
    def test_ab_threshold_sq(self):
        assert 4 * K_MINUS_1 == 44

    def test_spectral_radius_sq(self):
        assert MU**2 == 16

    def test_W33_strictly_ramanujan(self):
        assert MU**2 < 4 * K_MINUS_1

    def test_alon_boppana_gap_sq_eq_MU_PHI6(self):
        gap_sq = 4 * K_MINUS_1 - MU**2
        assert gap_sq == MU * PHI6


# ===========================================================================
# Section 15: Cheeger bounds
# ===========================================================================
class TestCheegerBounds:
    def test_alge_conn_eq_PHI4(self):
        assert K - ADJ_EV_R == PHI4

    def test_cheeger_lower_eq_5(self):
        assert PHI4 // 2 == 5

    def test_cheeger_lower_eq_Q_plus_2(self):
        assert PHI4 // 2 == Q + 2

    def test_cheeger_upper_sq_eq_EDGES(self):
        cheeger_upper_sq = 2 * (K - ADJ_EV_R) * K
        assert cheeger_upper_sq == EDGES

    def test_cheeger_upper_sq_eq_240(self):
        assert 2 * PHI4 * K == 240


# ===========================================================================
# Section 16: Ramanujan modular form
# ===========================================================================
class TestRamanujanModularForm:
    def test_weight_Delta_eq_K(self):
        assert K == 12  # weight of Δ(z) in S_12(SL(2,Z))

    def test_RP_exponent_eq_K1(self):
        assert K - 1 == 11

    def test_tau_2_eq_neg_2K(self):
        assert -24 == -2 * K

    def test_tau_3_eq_21K(self):
        assert 252 == 21 * K

    def test_abs_tau_2_eq_2K(self):
        assert abs(-24) == 2 * K

    def test_tau_2_satisfies_RP_bound(self):
        tau_2 = -24
        # |tau(2)|^2 <= 4 * 2^{K-1}
        assert abs(tau_2)**2 <= 4 * 2**(K - 1)

    def test_tau_12_satisfies_RP_bound(self):
        tau_12 = -370944
        # |tau(12)|^2 <= 4 * 12^{K-1}
        assert abs(tau_12)**2 <= 4 * 12**(K - 1)

    def test_tau_multiplicativity_2_3(self):
        # tau(2) * tau(3) = tau(6)
        assert (-24) * 252 == -6048

    def test_tau_multiplicativity_2_5(self):
        # tau(2) * tau(5) = tau(10)
        assert (-24) * 4830 == -115920


# ===========================================================================
# Section 17: Synopsis identities
# ===========================================================================
class TestSynopsis:
    def test_r_and_s_encode_LAM_MU(self):
        assert ADJ_EV_R == LAM and ADJ_EV_S == -MU

    def test_spectral_constants_from_VKLAMMUMQ(self):
        # All computed from base params
        assert K - LAM == PHI4
        assert K + MU == LAP_TOP
        assert K + ADJ_EV_S == E8_RANK
        assert -1 - 2*ADJ_EV_S == PHI6

    def test_mults_encode_K_LINES27(self):
        assert MULT_R == 2*K
        assert MULT_S == LINES_27 - K

    def test_ihara_K1_encodes_PHI4_PHI6_MU(self):
        assert K_MINUS_1 == PHI4 + 1
        assert K_MINUS_1 == PHI6 + MU

    def test_MU_times_Q_eq_K(self):
        assert MU * Q == K


# ===========================================================================
# Section 18: All verify functions pass
# ===========================================================================
class TestAllVerifyFunctions:
    def test_verify_srg_eigenvalue_formula(self):
        r = verify_srg_eigenvalue_formula()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_eigenvalue_multiplicities(self):
        r = verify_eigenvalue_multiplicities()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ramanujan_condition(self):
        r = verify_ramanujan_condition()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_laplacian_spectrum(self):
        r = verify_laplacian_spectrum()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_laplacian_constant_meanings(self):
        r = verify_laplacian_constant_meanings()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_signless_laplacian(self):
        r = verify_signless_laplacian()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_seidel_matrix(self):
        r = verify_seidel_matrix()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_two_graph_condition(self):
        r = verify_two_graph_condition()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_trace_moments(self):
        r = verify_trace_moments()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ihara_euler_factor(self):
        r = verify_ihara_euler_factor()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ihara_k_minus_1(self):
        r = verify_ihara_k_minus_1()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ihara_trivial_eigenvalue(self):
        r = verify_ihara_trivial_eigenvalue()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ihara_non_trivial_factors(self):
        r = verify_ihara_non_trivial_factors()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_hashimoto_imaginary_parts(self):
        r = verify_hashimoto_imaginary_parts()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_graph_riemann_hypothesis(self):
        r = verify_graph_riemann_hypothesis()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_spectral_gap(self):
        r = verify_spectral_gap()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_random_walk(self):
        r = verify_random_walk()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_expander_mixing_lemma(self):
        r = verify_expander_mixing_lemma()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_alon_boppana(self):
        r = verify_alon_boppana()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_cheeger_bounds(self):
        r = verify_cheeger_bounds()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ramanujan_modular_form_weight(self):
        r = verify_ramanujan_modular_form_weight()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_ramanujan_tau_k(self):
        r = verify_ramanujan_tau_k()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_w33_spectrum_synopsis(self):
        r = verify_w33_spectrum_synopsis()
        assert all(r.values()), [k for k, v in r.items() if not v]

    def test_verify_eigenvalue_polynomial(self):
        r = verify_eigenvalue_polynomial()
        assert all(r.values()), [k for k, v in r.items() if not v]


# ===========================================================================
# Section 19: Bridge summary
# ===========================================================================
class TestBridgeSummary:
    def test_summary_all_pass(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["all_pass"] is True, s["failed_check_names"]

    def test_summary_checks_total(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["checks_total"] >= 200

    def test_summary_checks_passed_eq_total(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["checks_passed"] == s["checks_total"]

    def test_summary_part(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["part"] == "CCLXXXIV"

    def test_summary_W33_ramanujan(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["W33_is_ramanujan"] is True

    def test_summary_graph_RH(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["graph_RH_holds"] is True

    def test_summary_adj_eigenvalues(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["adj_eigenvalues"] == {"k": 12, "r": 2, "s": -4}

    def test_summary_multiplicities(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["multiplicities"] == {"k": 1, "r": 24, "s": 15}

    def test_summary_laplacian_eigenvalues(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["laplacian_eigenvalues"] == [0, PHI4, LAP_TOP]

    def test_summary_seidel_eigenvalues(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["seidel_eigenvalues"] == [15, -5, PHI6]

    def test_summary_spectral_gap_eq_E8_RANK(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["spectral_gap"] == E8_RANK

    def test_summary_alge_conn_eq_PHI4(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["algebraic_connectivity"] == PHI4

    def test_summary_ihara_euler_factor(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["ihara_euler_factor"] == 200

    def test_summary_K_minus_1(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["K_minus_1"] == 11

    def test_summary_hashimoto_modulus_sq(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["hashimoto_modulus_sq"] == K_MINUS_1

    def test_summary_hashimoto_im_from_r_eq_PHI4(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["hashimoto_im_sq_from_r"] == PHI4

    def test_summary_hashimoto_im_from_s_eq_PHI6(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["hashimoto_im_sq_from_s"] == PHI6

    def test_summary_has_sections(self):
        s = build_cclxxxiv_bridge_summary()
        assert len(s["sections"]) >= 20

    def test_summary_has_key_identities(self):
        s = build_cclxxxiv_bridge_summary()
        assert len(s["key_identities"]) >= 8

    def test_summary_zero_failed(self):
        s = build_cclxxxiv_bridge_summary()
        assert s["checks_failed"] == 0
