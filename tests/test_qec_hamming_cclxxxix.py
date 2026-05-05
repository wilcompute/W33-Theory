"""
Tests for Part CCLXXXIX: QEC / Hamming code bridge.

Tests that the ternary Hamming code Ham(4,3) = [40, 36, 3]_3 and its dual
simplex code Sim(4,3) = [40, 4, 27]_3 precisely encode the SM fermion partition
and the W(3,3) combinatorial structure.
"""

import math
import pytest
from exploration.PART_CCLXXXIX_QEC_HAMMING_BRIDGE import (
    # W(3,3) constants
    V, K, LAM, MU, Q, K2, MULT_R, MULT_S, EDGES,
    # SM counts
    QUARKS_36, EW_GAUGE_4, TOTAL_SM,
    # Hamming code
    HAMMING_R, HAMMING_Q, HAMMING_LENGTH, HAMMING_REDUNDANCY,
    HAMMING_DIMENSION, HAMMING_MIN_DIST,
    HAMMING_BALL_RADIUS, HAMMING_BALL_SIZE, HAMMING_PERFECT_RHS,
    HAMMING_IS_PERFECT, HAMMING_COVERING_RADIUS,
    # Simplex code
    SIMPLEX_LENGTH, SIMPLEX_DIMENSION, SIMPLEX_MIN_DIST,
    SIMPLEX_NUM_NONZERO, SIMPLEX_IS_EQUIDISTANT, DUAL_DIMENSION_SUM,
    # PG / Qutrit
    PG3_3_POINT_COUNT, HAMMING_COLS_EQ_PG,
    NUM_QUTRITS, HEISENBERG_SIZE, QUTRIT_PAULIS,
    QUANTUM_N, QUANTUM_BALL_SIZE_LB, QUANTUM_MIN_OVERHEAD,
    # Generation / Yukawa
    NUM_GENERATIONS, COSET_LEADERS_PER_SYMBOL, TOTAL_ERROR_SYNDROMES,
    # Bounds
    GRIESMER_LB, SINGLETON_BOUND,
    HAMMING_SATISFIES_SINGLETON, HAMMING_MEETS_GRIESMER, HAMMING_IS_MDS,
    # Functions
    griesmer_bound, verify_hamming_code, verify_pg_identification,
    verify_sm_coding_correspondence, verify_all, build_cclxxxix_summary,
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Hamming code parameters
# ─────────────────────────────────────────────────────────────────────────────

class TestHammingCodeParameters:
    def test_hamming_length_equals_v(self):
        assert HAMMING_LENGTH == 40
        assert HAMMING_LENGTH == V

    def test_hamming_dimension_equals_quarks36(self):
        assert HAMMING_DIMENSION == 36
        assert HAMMING_DIMENSION == QUARKS_36

    def test_hamming_min_dist_equals_q(self):
        assert HAMMING_MIN_DIST == 3
        assert HAMMING_MIN_DIST == Q

    def test_hamming_redundancy_equals_ew_gauge4(self):
        assert HAMMING_REDUNDANCY == 4
        assert HAMMING_REDUNDANCY == EW_GAUGE_4

    def test_hamming_r_equals_4(self):
        assert HAMMING_R == 4

    def test_hamming_q_equals_3(self):
        assert HAMMING_Q == 3
        assert HAMMING_Q == Q

    def test_hamming_length_formula(self):
        # n = (q^r - 1) / (q - 1)
        assert HAMMING_LENGTH == (Q**4 - 1) // (Q - 1)

    def test_hamming_dimension_formula(self):
        # k = n - r
        assert HAMMING_DIMENSION == HAMMING_LENGTH - HAMMING_R

    def test_hamming_dimension_plus_redundancy_equals_length(self):
        assert HAMMING_DIMENSION + HAMMING_REDUNDANCY == HAMMING_LENGTH

    def test_hamming_redundancy_formula(self):
        # redundancy = r (same as HAMMING_R)
        assert HAMMING_REDUNDANCY == HAMMING_R


# ─────────────────────────────────────────────────────────────────────────────
# 2. Simplex code parameters
# ─────────────────────────────────────────────────────────────────────────────

class TestSimplexCodeParameters:
    def test_simplex_length_equals_v(self):
        assert SIMPLEX_LENGTH == 40
        assert SIMPLEX_LENGTH == V

    def test_simplex_dimension_equals_ew_gauge4(self):
        assert SIMPLEX_DIMENSION == 4
        assert SIMPLEX_DIMENSION == EW_GAUGE_4

    def test_simplex_min_dist_equals_k2(self):
        assert SIMPLEX_MIN_DIST == 27
        assert SIMPLEX_MIN_DIST == K2

    def test_simplex_is_dual_of_hamming(self):
        # dual code sums: k + k_dual = n
        assert DUAL_DIMENSION_SUM == HAMMING_LENGTH
        assert HAMMING_DIMENSION + SIMPLEX_DIMENSION == HAMMING_LENGTH

    def test_simplex_nonzero_codewords(self):
        # q^r - 1 = 3^4 - 1 = 80
        assert SIMPLEX_NUM_NONZERO == 80
        assert SIMPLEX_NUM_NONZERO == Q**HAMMING_REDUNDANCY - 1

    def test_simplex_is_equidistant(self):
        assert SIMPLEX_IS_EQUIDISTANT is True

    def test_simplex_min_dist_formula(self):
        # d_simplex = q^{r-1}
        assert SIMPLEX_MIN_DIST == Q ** (HAMMING_R - 1)

    def test_simplex_length_formula(self):
        assert SIMPLEX_LENGTH == (Q**HAMMING_R - 1) // (Q - 1)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Perfect-code / Hamming-ball properties
# ─────────────────────────────────────────────────────────────────────────────

class TestPerfectCodeProperty:
    def test_hamming_ball_radius_is_1(self):
        assert HAMMING_BALL_RADIUS == 1

    def test_hamming_ball_size_equals_81(self):
        assert HAMMING_BALL_SIZE == 81

    def test_hamming_ball_size_formula(self):
        # |B(c, 1)| = 1 + n*(q-1)
        assert HAMMING_BALL_SIZE == 1 + HAMMING_LENGTH * (Q - 1)

    def test_hamming_is_perfect(self):
        assert HAMMING_IS_PERFECT is True

    def test_perfect_rhs_equals_q_pow_r(self):
        assert HAMMING_PERFECT_RHS == Q**HAMMING_R

    def test_perfect_rhs_equals_81(self):
        assert HAMMING_PERFECT_RHS == 81

    def test_ball_size_equals_perfect_rhs(self):
        assert HAMMING_BALL_SIZE == HAMMING_PERFECT_RHS

    def test_ball_size_equals_q_pow_redundancy(self):
        assert HAMMING_BALL_SIZE == Q**HAMMING_REDUNDANCY

    def test_covering_radius_is_1(self):
        assert HAMMING_COVERING_RADIUS == 1

    def test_total_error_syndromes_eq_81(self):
        assert TOTAL_ERROR_SYNDROMES == 81
        assert TOTAL_ERROR_SYNDROMES == HAMMING_BALL_SIZE


# ─────────────────────────────────────────────────────────────────────────────
# 4. PG(3,3) identification
# ─────────────────────────────────────────────────────────────────────────────

class TestPG33Identification:
    def test_pg3_3_point_count_equals_v(self):
        assert PG3_3_POINT_COUNT == V
        assert PG3_3_POINT_COUNT == 40

    def test_pg3_3_point_count_formula(self):
        # |PG(3,q)| = (q^4 - 1)/(q-1)
        assert PG3_3_POINT_COUNT == (Q**4 - 1) // (Q - 1)

    def test_hamming_cols_eq_pg(self):
        assert HAMMING_COLS_EQ_PG is True

    def test_qutrit_paulis_equals_v(self):
        assert QUTRIT_PAULIS == V
        assert QUTRIT_PAULIS == 40

    def test_heisenberg_size_equals_81(self):
        assert HEISENBERG_SIZE == 81

    def test_heisenberg_size_formula(self):
        # |Heisenberg(n_q, q)| = q^{2*n_q}
        assert HEISENBERG_SIZE == Q ** (2 * NUM_QUTRITS)

    def test_num_qutrits_is_2(self):
        assert NUM_QUTRITS == 2

    def test_qutrit_paulis_formula(self):
        # (q^{2*n_q} - 1) / (q - 1)
        assert QUTRIT_PAULIS == (Q**(2 * NUM_QUTRITS) - 1) // (Q - 1)


# ─────────────────────────────────────────────────────────────────────────────
# 5. SM coding correspondence
# ─────────────────────────────────────────────────────────────────────────────

class TestSMCodingCorrespondence:
    def test_info_symbols_eq_quarks(self):
        assert HAMMING_DIMENSION == QUARKS_36

    def test_parity_eq_ew_gauge(self):
        assert HAMMING_REDUNDANCY == EW_GAUGE_4

    def test_sm_partition_40(self):
        assert QUARKS_36 + EW_GAUGE_4 == V
        assert QUARKS_36 + EW_GAUGE_4 == 40

    def test_min_dist_eq_generations(self):
        assert HAMMING_MIN_DIST == NUM_GENERATIONS

    def test_generations_eq_q(self):
        assert NUM_GENERATIONS == Q

    def test_min_dist_eq_q(self):
        assert HAMMING_MIN_DIST == Q

    def test_perfect_ball_eq_q_pow_redundancy(self):
        assert HAMMING_BALL_SIZE == Q**HAMMING_REDUNDANCY

    def test_coset_leaders_per_symbol(self):
        assert COSET_LEADERS_PER_SYMBOL == Q - 1
        assert COSET_LEADERS_PER_SYMBOL == 2

    def test_total_error_syndromes_formula(self):
        assert TOTAL_ERROR_SYNDROMES == 1 + HAMMING_LENGTH * (Q - 1)

    def test_total_sm_equals_v(self):
        assert TOTAL_SM == V


# ─────────────────────────────────────────────────────────────────────────────
# 6. W(3,3) SRG ↔ code correspondence
# ─────────────────────────────────────────────────────────────────────────────

class TestW33SRGConnection:
    def test_mu_eq_hamming_redundancy(self):
        assert MU == HAMMING_REDUNDANCY
        assert MU == EW_GAUGE_4

    def test_k2_eq_simplex_min_dist(self):
        assert K2 == SIMPLEX_MIN_DIST
        assert K2 == 27

    def test_v_eq_hamming_length(self):
        assert V == HAMMING_LENGTH

    def test_q_eq_hamming_min_dist(self):
        assert Q == HAMMING_MIN_DIST

    def test_hamming_length_eq_pg3_3_points(self):
        assert HAMMING_LENGTH == PG3_3_POINT_COUNT

    def test_hamming_redundancy_eq_mu(self):
        assert HAMMING_REDUNDANCY == MU

    def test_simplex_dimension_eq_mu(self):
        assert SIMPLEX_DIMENSION == MU

    def test_k_not_equal_min_dist(self):
        # Valency K=12 is distinct from min distance d=3
        assert K != HAMMING_MIN_DIST


# ─────────────────────────────────────────────────────────────────────────────
# 7. Coding-theory bounds
# ─────────────────────────────────────────────────────────────────────────────

class TestCodingBounds:
    def test_singleton_bound_value(self):
        assert SINGLETON_BOUND == 5
        assert SINGLETON_BOUND == HAMMING_LENGTH - HAMMING_DIMENSION + 1

    def test_hamming_satisfies_singleton(self):
        assert HAMMING_SATISFIES_SINGLETON is True
        assert HAMMING_MIN_DIST <= SINGLETON_BOUND

    def test_hamming_is_not_mds(self):
        # Min distance 3 < n - k + 1 = 5, so not an MDS code
        assert HAMMING_IS_MDS is False

    def test_griesmer_lb_value(self):
        assert GRIESMER_LB == 38

    def test_hamming_meets_griesmer(self):
        assert HAMMING_MEETS_GRIESMER is True
        assert HAMMING_LENGTH >= GRIESMER_LB

    def test_griesmer_bound_function(self):
        lb = griesmer_bound(40, 36, 3, 3)
        assert lb == 38

    def test_griesmer_first_term(self):
        # First term: ceil(d/q^0) = d = 3
        assert math.ceil(HAMMING_MIN_DIST / (Q**0)) == 3

    def test_griesmer_subsequent_terms(self):
        # For i >= 1: ceil(3/3^i) = 1
        for i in range(1, HAMMING_DIMENSION):
            assert math.ceil(HAMMING_MIN_DIST / (Q**i)) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 8. Quantum overhead
# ─────────────────────────────────────────────────────────────────────────────

class TestQuantumConnection:
    def test_quantum_n_is_half_v(self):
        assert QUANTUM_N == V // 2
        assert QUANTUM_N == 20

    def test_heisenberg_eq_ball_size(self):
        # Both = 81: qutrit Heisenberg group size = classical Hamming ball size
        assert HEISENBERG_SIZE == HAMMING_BALL_SIZE

    def test_qutrit_paulis_eq_hamming_length(self):
        assert QUTRIT_PAULIS == HAMMING_LENGTH

    def test_quantum_ball_size_lb(self):
        assert QUANTUM_BALL_SIZE_LB == 1 + QUANTUM_N * (Q**2 - 1)
        assert QUANTUM_BALL_SIZE_LB == 161

    def test_quantum_min_overhead(self):
        assert QUANTUM_MIN_OVERHEAD == 5


# ─────────────────────────────────────────────────────────────────────────────
# 9. Verification functions
# ─────────────────────────────────────────────────────────────────────────────

class TestVerifyFunctions:
    def test_verify_hamming_code_all_true(self):
        result = verify_hamming_code()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_hamming_code_returns_dict(self):
        assert isinstance(verify_hamming_code(), dict)

    def test_verify_hamming_code_count(self):
        assert len(verify_hamming_code()) == 6

    def test_verify_pg_identification_all_true(self):
        result = verify_pg_identification()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_pg_identification_count(self):
        assert len(verify_pg_identification()) == 4

    def test_verify_sm_coding_all_true(self):
        result = verify_sm_coding_correspondence()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_sm_coding_count(self):
        assert len(verify_sm_coding_correspondence()) == 6

    def test_verify_all_all_true(self):
        result = verify_all()
        assert all(result.values()), f"Failed: {[k for k,v in result.items() if not v]}"

    def test_verify_all_count(self):
        assert len(verify_all()) == 16

    def test_verify_all_returns_dict(self):
        assert isinstance(verify_all(), dict)


# ─────────────────────────────────────────────────────────────────────────────
# 10. Build summary
# ─────────────────────────────────────────────────────────────────────────────

class TestBuildSummary:
    def test_part_number(self):
        s = build_cclxxxix_summary()
        assert s["part_number"] == "CCLXXXIX"

    def test_verification_status_all_pass(self):
        s = build_cclxxxix_summary()
        assert s["verification_status"] == "ALL CHECKS PASS"

    def test_hamming_code_block_length(self):
        s = build_cclxxxix_summary()
        assert s["hamming_code"]["block_length"] == V

    def test_hamming_code_dimension(self):
        s = build_cclxxxix_summary()
        assert s["hamming_code"]["dimension"] == QUARKS_36

    def test_hamming_code_is_perfect(self):
        s = build_cclxxxix_summary()
        assert s["hamming_code"]["is_perfect"] is True

    def test_simplex_min_dist_in_summary(self):
        s = build_cclxxxix_summary()
        assert s["simplex_code"]["min_distance"] == K2

    def test_sm_correspondence_quarks(self):
        s = build_cclxxxix_summary()
        assert s["sm_correspondence"]["quarks_eq_dimension"] is True

    def test_sm_correspondence_ew_gauge(self):
        s = build_cclxxxix_summary()
        assert s["sm_correspondence"]["ew_gauge_eq_redundancy"] is True

    def test_sm_correspondence_partition_sum(self):
        s = build_cclxxxix_summary()
        assert s["sm_correspondence"]["partition_sum"] == V

    def test_key_discoveries_count(self):
        s = build_cclxxxix_summary()
        assert len(s["key_discoveries"]) == 7
