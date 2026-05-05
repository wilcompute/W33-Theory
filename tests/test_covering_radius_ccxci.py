"""Tests for Part CCXCI: Covering Radius and Packing-Covering Duality."""

import pytest
from fractions import Fraction
from exploration.PART_CCXCI_COVERING_RADIUS_BRIDGE import (
    # Constants
    V, K, LAM, MU, Q, K2, MULT_R, MULT_S, EDGES,
    QUARKS_36, EW_GAUGE_4, TOTAL_SM,
    HAM_N, HAM_K, HAM_D, HAM_Q, HAM_R,
    PACKING_RADIUS, COVERING_RADIUS,
    BALL_VOL_T, CODE_SIZE, AMBIENT_SIZE,
    PERFECT_CODE_EXACT, PERFECT_CODE_PRODUCT,
    PACKING_COVERING_EQUAL, COVERING_DENSITY, PERFECT_DENSITY,
    NUM_COSETS, COSET_LEADERS_WT0, COSET_LEADERS_WT1, TOTAL_COSET_LEADERS,
    COSET_STRUCTURE_CORRECT,
    SYNDROME_SPACE_SIZE, ZERO_SYNDROME, NONZERO_SYNDROMES,
    SYNDROMES_PER_POSITION, NUM_CORRECTABLE_POSITIONS,
    SYNDROME_COVERS_ALL_POSITIONS,
    PG3_3_POINTS, PCM_COLUMNS_EQ_PG,
    REDUNDANCY, REDUNDANCY_EQ_EW,
    HAMMING_BOUND, HAMMING_BOUND_EQ_CODE_SIZE, HAMMING_BOUND_TIGHT,
    PARTITION_COSET_COUNT, PARTITION_COSET_SIZE,
    PARTITION_TOTAL, PARTITION_COMPLETE,
    SM_VALID_STATES, SM_ERROR_NEIGHBORHOOD,
    SM_ERROR_ALPHABET_SIZE, SM_SYNDROME_BITS,
    # Functions
    hamming_ball_volume, verify_perfect_code, verify_coset_structure,
    verify_parity_check_matrix, verify_hamming_bound,
    verify_all, build_ccxci_summary,
)


class TestSRGConstants:
    """Verify SRG(40,12,2,4) constants are correct."""

    def test_v_is_40(self):
        assert V == 40

    def test_k_is_12(self):
        assert K == 12

    def test_lam_is_2(self):
        assert LAM == 2

    def test_mu_is_4(self):
        assert MU == 4

    def test_q_is_3(self):
        assert Q == 3

    def test_k2_is_27(self):
        assert K2 == 27

    def test_mult_r_is_24(self):
        assert MULT_R == 24

    def test_mult_s_is_15(self):
        assert MULT_S == 15

    def test_edges_is_240(self):
        assert EDGES == 240

    def test_k_plus_k2_plus_1_eq_v(self):
        assert K + K2 + 1 == V


class TestSMConstants:
    """Verify Standard Model dimension constants."""

    def test_quarks_36(self):
        assert QUARKS_36 == 36

    def test_ew_gauge_4(self):
        assert EW_GAUGE_4 == 4

    def test_total_sm_40(self):
        assert TOTAL_SM == 40

    def test_quarks_plus_ew_eq_total(self):
        assert QUARKS_36 + EW_GAUGE_4 == TOTAL_SM


class TestCodeParameters:
    """Verify Ham(4,3) code parameters."""

    def test_n_is_40(self):
        assert HAM_N == 40

    def test_k_is_36(self):
        assert HAM_K == 36

    def test_d_is_3(self):
        assert HAM_D == 3

    def test_q_is_3(self):
        assert HAM_Q == 3

    def test_r_is_4(self):
        assert HAM_R == 4

    def test_n_eq_v(self):
        assert HAM_N == V

    def test_k_eq_quarks(self):
        assert HAM_K == QUARKS_36

    def test_r_eq_ew(self):
        assert HAM_R == EW_GAUGE_4

    def test_n_minus_k_eq_r(self):
        assert HAM_N - HAM_K == HAM_R


class TestPackingCoveringRadii:
    """Verify packing and covering radii for Ham(4,3)."""

    def test_packing_radius_is_1(self):
        assert PACKING_RADIUS == 1

    def test_packing_radius_formula(self):
        assert PACKING_RADIUS == (HAM_D - 1) // 2

    def test_covering_radius_is_1(self):
        assert COVERING_RADIUS == 1

    def test_packing_equals_covering(self):
        assert PACKING_COVERING_EQUAL

    def test_packing_eq_covering_value(self):
        assert PACKING_RADIUS == COVERING_RADIUS


class TestHammingBallVolume:
    """Test hamming_ball_volume function and ball volume constant."""

    def test_ball_vol_radius_0(self):
        assert hamming_ball_volume(40, 0, 3) == 1

    def test_ball_vol_radius_1(self):
        assert hamming_ball_volume(40, 1, 3) == 81

    def test_ball_vol_t_is_81(self):
        assert BALL_VOL_T == 81

    def test_ball_vol_is_q_pow_r(self):
        assert BALL_VOL_T == HAM_Q ** HAM_R

    def test_ball_vol_formula(self):
        # 1 + 40*2 = 81
        assert BALL_VOL_T == 1 + HAM_N * (HAM_Q - 1)

    def test_ball_vol_small(self):
        # Ball of radius 1 in GF(3)^4: size = 1 + 4*2 = 9
        assert hamming_ball_volume(4, 1, 3) == 9

    def test_ball_vol_general(self):
        # Ball of radius 2 in GF(3)^40
        expected = 1 + 40 * 2 + (40 * 39 // 2) * 4
        assert hamming_ball_volume(40, 2, 3) == expected


class TestPerfectCodeCondition:
    """Verify Ham(4,3) satisfies the perfect code condition."""

    def test_perfect_code_exact(self):
        assert PERFECT_CODE_EXACT

    def test_perfect_product_eq_ambient(self):
        assert PERFECT_CODE_PRODUCT == AMBIENT_SIZE

    def test_code_times_ball_eq_ambient(self):
        assert CODE_SIZE * BALL_VOL_T == AMBIENT_SIZE

    def test_covering_density_is_1(self):
        assert COVERING_DENSITY == Fraction(1)

    def test_perfect_density_flag(self):
        assert PERFECT_DENSITY

    def test_hamming_bound_tight(self):
        assert HAMMING_BOUND_TIGHT

    def test_hamming_bound_eq_code_size(self):
        assert HAMMING_BOUND_EQ_CODE_SIZE

    def test_hamming_bound_value(self):
        assert HAMMING_BOUND == CODE_SIZE

    def test_ambient_is_q_pow_n(self):
        assert AMBIENT_SIZE == HAM_Q ** HAM_N

    def test_code_size_is_q_pow_k(self):
        assert CODE_SIZE == HAM_Q ** HAM_K


class TestCosetStructure:
    """Test coset decomposition and coset leaders."""

    def test_num_cosets_is_81(self):
        assert NUM_COSETS == 81

    def test_num_cosets_is_q_pow_r(self):
        assert NUM_COSETS == HAM_Q ** HAM_R

    def test_coset_size_eq_ball_vol(self):
        assert NUM_COSETS == BALL_VOL_T

    def test_leaders_wt0_is_1(self):
        assert COSET_LEADERS_WT0 == 1

    def test_leaders_wt1_is_80(self):
        assert COSET_LEADERS_WT1 == 80

    def test_leaders_wt1_formula(self):
        assert COSET_LEADERS_WT1 == HAM_N * (HAM_Q - 1)

    def test_total_leaders_is_81(self):
        assert TOTAL_COSET_LEADERS == 81

    def test_coset_structure_correct(self):
        assert COSET_STRUCTURE_CORRECT

    def test_leaders_sum_to_cosets(self):
        assert COSET_LEADERS_WT0 + COSET_LEADERS_WT1 == NUM_COSETS


class TestSyndromeDecoding:
    """Test syndrome space and decoding correctness."""

    def test_syndrome_space_is_81(self):
        assert SYNDROME_SPACE_SIZE == 81

    def test_zero_syndrome_count_is_1(self):
        assert ZERO_SYNDROME == 1

    def test_nonzero_syndromes_is_80(self):
        assert NONZERO_SYNDROMES == 80

    def test_nonzero_plus_zero_eq_total(self):
        assert ZERO_SYNDROME + NONZERO_SYNDROMES == SYNDROME_SPACE_SIZE

    def test_syndromes_per_position_is_2(self):
        assert SYNDROMES_PER_POSITION == 2

    def test_syndromes_per_position_formula(self):
        assert SYNDROMES_PER_POSITION == HAM_Q - 1

    def test_correctable_positions_is_40(self):
        assert NUM_CORRECTABLE_POSITIONS == 40

    def test_syndrome_covers_all_positions(self):
        assert SYNDROME_COVERS_ALL_POSITIONS

    def test_nonzero_syndromes_eq_leaders_wt1(self):
        assert NONZERO_SYNDROMES == COSET_LEADERS_WT1


class TestParityCheckMatrix:
    """Test parity check matrix column count and PG(3,3) identification."""

    def test_pg33_points_is_40(self):
        assert PG3_3_POINTS == 40

    def test_pg33_formula(self):
        assert PG3_3_POINTS == (HAM_Q ** HAM_R - 1) // (HAM_Q - 1)

    def test_pg33_eq_v(self):
        assert PG3_3_POINTS == V

    def test_pg33_eq_ham_n(self):
        assert PG3_3_POINTS == HAM_N

    def test_pcm_columns_eq_pg(self):
        assert PCM_COLUMNS_EQ_PG

    def test_redundancy_is_4(self):
        assert REDUNDANCY == 4

    def test_redundancy_eq_ew(self):
        assert REDUNDANCY_EQ_EW

    def test_redundancy_eq_ham_r(self):
        assert REDUNDANCY == HAM_R


class TestPerfectPartition:
    """Test the perfect partition of the ambient space."""

    def test_partition_complete(self):
        assert PARTITION_COMPLETE

    def test_partition_total_eq_ambient(self):
        assert PARTITION_TOTAL == AMBIENT_SIZE

    def test_partition_count_is_q_pow_k(self):
        assert PARTITION_COSET_COUNT == HAM_Q ** HAM_K

    def test_partition_size_is_81(self):
        assert PARTITION_COSET_SIZE == 81

    def test_partition_size_eq_ball_vol(self):
        assert PARTITION_COSET_SIZE == BALL_VOL_T


class TestSMInterpretation:
    """Test SM physical interpretation of the coding structure."""

    def test_valid_states_is_q_pow_k(self):
        assert SM_VALID_STATES == HAM_Q ** HAM_K

    def test_error_neighborhood_is_81(self):
        assert SM_ERROR_NEIGHBORHOOD == 81

    def test_error_alphabet_is_81(self):
        assert SM_ERROR_ALPHABET_SIZE == 81

    def test_syndrome_bits_is_4(self):
        assert SM_SYNDROME_BITS == 4

    def test_syndrome_bits_eq_ew(self):
        assert SM_SYNDROME_BITS == EW_GAUGE_4

    def test_error_neighborhood_eq_alphabet(self):
        assert SM_ERROR_NEIGHBORHOOD == SM_ERROR_ALPHABET_SIZE


class TestVerifyFunctions:
    """Test the verify_* functions return correct dicts."""

    def test_verify_perfect_code_all_pass(self):
        result = verify_perfect_code()
        assert all(result.values()), [k for k, v in result.items() if not v]

    def test_verify_perfect_code_keys(self):
        result = verify_perfect_code()
        assert "packing_radius_is_1" in result
        assert "covering_radius_is_1" in result
        assert "perfect_code_exact" in result

    def test_verify_coset_structure_all_pass(self):
        result = verify_coset_structure()
        assert all(result.values()), [k for k, v in result.items() if not v]

    def test_verify_coset_structure_keys(self):
        result = verify_coset_structure()
        assert "num_cosets_is_81" in result
        assert "coset_structure_correct" in result

    def test_verify_parity_check_matrix_all_pass(self):
        result = verify_parity_check_matrix()
        assert all(result.values()), [k for k, v in result.items() if not v]

    def test_verify_parity_check_matrix_keys(self):
        result = verify_parity_check_matrix()
        assert "pg33_points_is_40" in result
        assert "redundancy_eq_ew" in result

    def test_verify_hamming_bound_all_pass(self):
        result = verify_hamming_bound()
        assert all(result.values()), [k for k, v in result.items() if not v]

    def test_verify_hamming_bound_keys(self):
        result = verify_hamming_bound()
        assert "hamming_bound_tight" in result
        assert "partition_complete" in result

    def test_verify_all_22_pass(self):
        result = verify_all()
        assert len(result) == 22

    def test_verify_all_pass(self):
        result = verify_all()
        assert all(result.values()), [k for k, v in result.items() if not v]


class TestBuildSummary:
    """Test the summary dictionary structure and values."""

    def test_summary_part_number(self):
        s = build_ccxci_summary()
        assert s["part_number"] == "CCXCI"

    def test_summary_checks_pass_22(self):
        s = build_ccxci_summary()
        assert s["checks_pass"] == 22

    def test_summary_checks_total_22(self):
        s = build_ccxci_summary()
        assert s["checks_total"] == 22

    def test_summary_all_pass(self):
        s = build_ccxci_summary()
        assert s["verification_status"] == "ALL CHECKS PASS"

    def test_summary_code_params(self):
        s = build_ccxci_summary()
        p = s["code_parameters"]
        assert p["n"] == 40
        assert p["k"] == 36
        assert p["d"] == 3
        assert p["q"] == 3
        assert p["r"] == 4

    def test_summary_perfect_code(self):
        s = build_ccxci_summary()
        pc = s["perfect_code"]
        assert pc["packing_radius"] == 1
        assert pc["covering_radius"] == 1
        assert pc["ball_volume"] == 81

    def test_summary_coset_structure(self):
        s = build_ccxci_summary()
        cs = s["coset_structure"]
        assert cs["num_cosets"] == 81
        assert cs["leaders_wt0"] == 1
        assert cs["leaders_wt1"] == 80
        assert cs["total_leaders"] == 81

    def test_summary_key_discoveries_nonempty(self):
        s = build_ccxci_summary()
        assert len(s["key_discoveries"]) >= 5
