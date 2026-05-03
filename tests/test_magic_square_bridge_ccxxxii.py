"""
Part CCXXXII — Freudenthal-Tits Magic Square from W(3,3)
Test suite: 74 tests across 11 classes.
"""

import pytest

from PART_CCXXXII_MAGIC_SQUARE_BRIDGE import (
    # SRG constants
    Q, V, K, LAM, MU, M_LAM, LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    # B0: Division algebra dims
    dim_R, dim_C, dim_H, dim_O, dim_H_srg, dim_O_srg,
    # B1: Exceptional 𝕆-row
    dim_F4, dim_E6, dim_E7, dim_E8, Phi3_Q,
    # B2: Rank sequence
    rank_F4, rank_E6, rank_E7, rank_E8,
    # B3: Albert algebra
    dim_Albert, dim_Albert_formula, Albert_rank,
    # B4: Key representations
    dim_27_E6, dim_56_E7, dim_248_E8, dim_26_F4,
    # B5: Row sums
    O_row_sum, H_row_sum, C_row_sum, R_row_sum,
    mersenne_9, mersenne_8,
    # B6: Total
    total_sum, fib_16,
    # B7: Diagonal
    diagonal_sum, diagonal_Q_factor,
    # B8: Coxeter numbers
    cox_F4, cox_E6, cox_E7, cox_E8,
    cox_exceptional_sum, cox_sum_from_K,
    # B9: Dual Coxeter
    dual_cox_F4, dual_cox_E6, dual_cox_E7, dual_cox_E8,
    # B10: Symmetry
    is_symmetric, O_row_equals_col,
    # Magic square table
    magic,
    # Column sums
    O_col_sum, H_col_sum, C_col_sum, R_col_sum,
    # Fine structure
    fine_structure_numerology,
    # Meta
    checks, Verified,
)


# ═══════════════════════════════════════════════════════════════
# T0: BRIDGE METADATA
# ═══════════════════════════════════════════════════════════════
class TestBridgeMetadata:
    def test_verified_flag(self):
        assert Verified is True

    def test_all_32_checks_pass(self):
        passed = sum(1 for _, v in checks if v)
        assert passed == 32

    def test_no_failed_checks(self):
        failed = [lbl for lbl, v in checks if not v]
        assert failed == [], f"Failed: {failed}"

    def test_check_count(self):
        assert len(checks) == 32


# ═══════════════════════════════════════════════════════════════
# T1: SRG PARAMETERS
# ═══════════════════════════════════════════════════════════════
class TestSRGParameters:
    def test_Q(self):
        assert Q == 3

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_EDGES(self):
        assert EDGES == 240


# ═══════════════════════════════════════════════════════════════
# T2: DIVISION ALGEBRA DIMENSIONS (Bridge B0)
# ═══════════════════════════════════════════════════════════════
class TestDivisionAlgebraDimensions:
    def test_dim_R(self):
        assert dim_R == 1

    def test_dim_C(self):
        assert dim_C == 2

    def test_dim_H(self):
        assert dim_H == 4

    def test_dim_O(self):
        assert dim_O == 8

    def test_dim_H_is_MU(self):
        """ℍ quaternion dimension = μ."""
        assert dim_H_srg == MU

    def test_dim_O_is_2MU(self):
        """𝕆 octonion dimension = 2μ."""
        assert dim_O_srg == 2 * MU

    def test_dim_algebra_doubling(self):
        """Cayley-Dickson: each step doubles dimension."""
        assert dim_C == 2 * dim_R
        assert dim_H == 2 * dim_C
        assert dim_O == 2 * dim_H


# ═══════════════════════════════════════════════════════════════
# T3: EXCEPTIONAL 𝕆-ROW (Bridge B1)
# ═══════════════════════════════════════════════════════════════
class TestExceptionalOctonionRow:
    def test_dim_F4_value(self):
        assert dim_F4 == 52

    def test_dim_F4_formula(self):
        assert dim_F4 == V + K

    def test_dim_E6_value(self):
        assert dim_E6 == 78

    def test_dim_E6_formula(self):
        assert dim_E6 == Q * (M_LAM - 1)

    def test_dim_E7_value(self):
        assert dim_E7 == 133

    def test_dim_E7_formula(self):
        assert dim_E7 == V * Q + Phi3_Q

    def test_Phi3_Q_value(self):
        assert Phi3_Q == 13

    def test_Phi3_Q_formula(self):
        assert Phi3_Q == Q**2 + Q + 1

    def test_dim_E8_value(self):
        assert dim_E8 == 248

    def test_dim_E8_formula(self):
        assert dim_E8 == EDGES + 2 * MU

    def test_magic_square_O_row(self):
        """Magic square 𝕆-row entries match bridge values."""
        assert magic[3] == [52, 78, 133, 248]


# ═══════════════════════════════════════════════════════════════
# T4: RANK SEQUENCE (Bridge B2)
# ═══════════════════════════════════════════════════════════════
class TestRankSequence:
    def test_rank_F4_is_MU(self):
        assert rank_F4 == MU

    def test_rank_F4_value(self):
        assert rank_F4 == 4

    def test_rank_E6_is_K_half(self):
        assert rank_E6 == K // 2

    def test_rank_E6_value(self):
        assert rank_E6 == 6

    def test_rank_E7_is_K_half_plus_1(self):
        assert rank_E7 == K // 2 + 1

    def test_rank_E7_value(self):
        assert rank_E7 == 7

    def test_rank_E8_is_2MU(self):
        assert rank_E8 == 2 * MU

    def test_rank_E8_value(self):
        assert rank_E8 == 8

    def test_rank_sequence_strictly_increasing(self):
        assert rank_F4 < rank_E6 < rank_E7 < rank_E8


# ═══════════════════════════════════════════════════════════════
# T5: ALBERT ALGEBRA J₃(O) (Bridge B3)
# ═══════════════════════════════════════════════════════════════
class TestAlbertAlgebra:
    def test_dim_Albert_is_M_LAM(self):
        assert dim_Albert == M_LAM

    def test_dim_Albert_value(self):
        assert dim_Albert == 27

    def test_Albert_formula_3O_plus_3R(self):
        """J₃(O) = 3 octonion off-diagonals + 3 real diagonals."""
        assert dim_Albert_formula == 3 * dim_O + 3 * dim_R

    def test_Albert_formula_value(self):
        assert dim_Albert_formula == 27

    def test_Albert_rank_is_Q(self):
        assert Albert_rank == Q

    def test_Albert_rank_value(self):
        assert Albert_rank == 3


# ═══════════════════════════════════════════════════════════════
# T6: KEY REPRESENTATIONS (Bridge B4)
# ═══════════════════════════════════════════════════════════════
class TestKeyRepresentations:
    def test_27_E6_is_M_LAM(self):
        assert dim_27_E6 == M_LAM

    def test_27_E6_value(self):
        assert dim_27_E6 == 27

    def test_56_E7_value(self):
        assert dim_56_E7 == 56

    def test_56_E7_formula(self):
        """56 = 2·M_λ + 2 = 2·27 + 2."""
        assert dim_56_E7 == 2 * M_LAM + 2

    def test_248_E8_is_dim_E8(self):
        assert dim_248_E8 == dim_E8

    def test_26_F4_value(self):
        assert dim_26_F4 == 26

    def test_26_F4_is_M_LAM_minus_1(self):
        assert dim_26_F4 == M_LAM - 1


# ═══════════════════════════════════════════════════════════════
# T7: ROW SUMS AND MERSENNE (Bridge B5)
# ═══════════════════════════════════════════════════════════════
class TestRowSums:
    def test_O_row_sum_value(self):
        assert O_row_sum == 511

    def test_O_row_sum_is_mersenne_9(self):
        assert O_row_sum == 2**9 - 1

    def test_mersenne_9_value(self):
        assert mersenne_9 == 511

    def test_H_row_sum_value(self):
        assert H_row_sum == 255

    def test_H_row_sum_is_mersenne_8(self):
        assert H_row_sum == 2**8 - 1

    def test_mersenne_8_value(self):
        assert mersenne_8 == 255

    def test_C_row_sum_value(self):
        assert C_row_sum == 137

    def test_R_row_sum_value(self):
        assert R_row_sum == 84

    def test_total_sum_is_fib16(self):
        """Sum of all 16 magic square entries = Fibonacci(16) = 987."""
        assert total_sum == fib_16

    def test_total_sum_value(self):
        assert total_sum == 987


# ═══════════════════════════════════════════════════════════════
# T8: DIAGONAL (Bridge B7)
# ═══════════════════════════════════════════════════════════════
class TestDiagonal:
    def test_diagonal_sum_value(self):
        assert diagonal_sum == 333

    def test_diagonal_Q_divisible(self):
        """Diagonal = Q × 111."""
        assert diagonal_sum % Q == 0

    def test_diagonal_Q_factor_value(self):
        assert diagonal_Q_factor == 111

    def test_diagonal_entries(self):
        """3, 16, 66, 248 are the four diagonal entries."""
        diag = [magic[i][i] for i in range(4)]
        assert diag == [3, 16, 66, 248]


# ═══════════════════════════════════════════════════════════════
# T9: COXETER NUMBERS (Bridge B8)
# ═══════════════════════════════════════════════════════════════
class TestCoxeterNumbers:
    def test_cox_F4_is_K(self):
        assert cox_F4 == K

    def test_cox_F4_value(self):
        assert cox_F4 == 12

    def test_cox_E6_is_K(self):
        assert cox_E6 == K

    def test_cox_E6_value(self):
        assert cox_E6 == 12

    def test_cox_E7_value(self):
        assert cox_E7 == 18

    def test_cox_E7_formula(self):
        assert cox_E7 == K + K // 2

    def test_cox_E8_value(self):
        assert cox_E8 == 30

    def test_cox_E8_formula(self):
        assert cox_E8 == V - LAP_MID

    def test_cox_sum_value(self):
        assert cox_exceptional_sum == 72

    def test_cox_sum_is_K_times_half_K(self):
        assert cox_exceptional_sum == cox_sum_from_K

    def test_dual_cox_F4_is_Q_squared(self):
        assert dual_cox_F4 == Q**2

    def test_dual_cox_F4_value(self):
        assert dual_cox_F4 == 9


# ═══════════════════════════════════════════════════════════════
# T10: SYMMETRY AND STRUCTURE (Bridge B10)
# ═══════════════════════════════════════════════════════════════
class TestSymmetry:
    def test_magic_square_is_symmetric(self):
        assert is_symmetric is True

    def test_O_row_equals_O_col(self):
        assert O_row_equals_col is True

    def test_row_equals_col_sums(self):
        """All row sums equal corresponding column sums (symmetry)."""
        assert O_row_sum == O_col_sum
        assert H_row_sum == H_col_sum
        assert C_row_sum == C_col_sum
        assert R_row_sum == R_col_sum

    def test_magic_square_dimensions(self):
        """4×4 table."""
        assert len(magic) == 4
        assert all(len(row) == 4 for row in magic)

    def test_fine_structure_137(self):
        """ℂ-row sum = 137 ≈ 1/α numerology."""
        assert fine_structure_numerology == 137
        assert C_row_sum == fine_structure_numerology
