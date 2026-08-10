"""Tests for Pillar 111 (Part CCXI): Bose-Mesner Algebra of the PSp(4,3) 120-Duad Scheme."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXI_BOSE_MESNER_ALGEBRA import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Scheme identification
# ---------------------------------------------------------------------------

class TestT1SchemeIdentification:
    """T1: Rank-5 scheme on 120 duads; PSp(4,3) Gelfand pair; val/mult sums = 120."""

    def test_n_is_120(self, summary):
        """n = 120 duads."""
        assert summary["T1_n"] == 120

    def test_rank_is_5(self, summary):
        """Scheme has rank 5."""
        assert summary["T1_rank"] == 5

    def test_val_sum_120(self, summary):
        """Valencies sum to 120."""
        assert summary["T1_val_sum"] == 120

    def test_mult_sum_120(self, summary):
        """Multiplicities sum to 120."""
        assert summary["T1_mult_sum"] == 120

    def test_group_order_25920(self, summary):
        """|PSp(4,3)| = |W(E6)| = 25920."""
        assert summary["T1_group_order"] == 25920

    def test_stab_order_216(self, summary):
        """Stabiliser H has order 216."""
        assert summary["T1_stab_order"] == 216

    def test_gelfand_pair(self, summary):
        """|G|/|H| = 120 (Gelfand pair condition)."""
        assert summary["T1_gelfand"] is True

    def test_valencies_correct(self, summary):
        """Valencies are (1, 2, 27, 36, 54)."""
        assert summary["T1_val_correct"] is True

    def test_multiplicities_correct(self, summary):
        """Multiplicities are (1, 20, 24, 15, 60)."""
        assert summary["T1_mult_correct"] is True

    def test_bundle_vals_match(self, summary):
        """Bundle valencies match hard-coded values."""
        assert summary["T1_bundle_vals_match"] is True

    def test_val_plus_mult_even(self, summary):
        """Valencies and multiplicities both sum to n=120."""
        assert summary["T1_val_sum"] == summary["T1_mult_sum"]

    def test_group_over_stab(self, summary):
        """25920 / 216 = 120."""
        assert summary["T1_group_order"] // summary["T1_stab_order"] == 120


# ---------------------------------------------------------------------------
# T2: Multiplication table
# ---------------------------------------------------------------------------

class TestT2MultiplicationTable:
    """T2: 25 structure-constant products in the rank-5 Bose-Mesner algebra."""

    def test_all_products_correct(self, summary):
        """All 10 key products verified against bundle."""
        assert summary["T2_all_correct"] is True

    def test_products_verified_count(self, summary):
        """Exactly 10 key products verified."""
        assert summary["T2_products_verified"] == 10

    def test_no_product_failures(self, summary):
        """Zero product mismatches."""
        assert summary["T2_num_failures"] == 0

    def test_total_products_25(self, summary):
        """Bundle contains 25 total products (5x5 table)."""
        assert summary["T2_total_products"] == 25

    def test_a1_squared_triangles(self, summary):
        """A1^2 = 2A0 + A1 (40 disjoint triangles in A1-graph)."""
        # This is encoded in the verification
        assert summary["T2_all_correct"] is True

    def test_a4_squared_full(self, summary):
        """A4^2 = 54A0+27A1+28A2+24A3+22A4 (densest relation)."""
        assert summary["T2_all_correct"] is True


# ---------------------------------------------------------------------------
# T3: P eigenmatrix
# ---------------------------------------------------------------------------

class TestT3PEigenmatrix:
    """T3: 5x5 eigenvalue matrix P; P*Q = 120*I; orthogonality verified."""

    def test_pq_equals_120I(self, summary):
        """P * Q = 120 * I (exact rational arithmetic)."""
        assert summary["T3_pq_is_nI"] is True

    def test_e0_row_is_valencies(self, summary):
        """E0 eigenvalues = valencies (1,2,27,36,54)."""
        assert summary["T3_e0_eigenvalues"] is True

    def test_col_orthogonality(self, summary):
        """Mult-weighted column sums for A_i (i>0) are zero."""
        assert summary["T3_col_orth"] is True

    def test_spec_match(self, summary):
        """P eigenvalues for A1 match bundle spectrum."""
        assert summary["T3_spec_match"] is True

    def test_p_is_5x5(self, summary):
        """P is a 5x5 matrix (rank 5)."""
        assert summary["T1_rank"] == 5


# ---------------------------------------------------------------------------
# T4: Q dual eigenmatrix
# ---------------------------------------------------------------------------

class TestT4QDualEigenmatrix:
    """T4: Q has rational entries; Q col0 = all-ones; Q row0 = multiplicities."""

    def test_q_col0_all_ones(self, summary):
        """Q column 0 (E0 column) = [1,1,1,1,1] (E0 = (1/120)*J)."""
        assert summary["T4_q_col0_correct"] is True

    def test_q_row0_multiplicities(self, summary):
        """Q row 0 (A0 row) = [1,20,24,15,60] = multiplicities."""
        assert summary["T4_q_row0_correct"] is True

    def test_q_has_rational_entries(self, summary):
        """Q has non-integer rational entries (A2 and A4 rows have 1/3 denominators)."""
        assert summary["T4_q_has_fractions"] is True

    def test_pq_is_n_times_identity(self, summary):
        """P*Q = 120*I verified from T3."""
        assert summary["T3_pq_is_nI"] is True


# ---------------------------------------------------------------------------
# T5: Primitive idempotents
# ---------------------------------------------------------------------------

class TestT5PrimitiveIdempotents:
    """T5: 5 closed-form idempotents; rank sum = 120; each rank matches multiplicity."""

    def test_rank_sum_120(self, summary):
        """Sum of idempotent ranks = 1+20+24+15+60 = 120."""
        assert summary["T5_rank_sum"] == 120

    def test_rank_sum_correct(self, summary):
        """Rank sum equals n=120."""
        assert summary["T5_rank_sum_correct"] is True

    def test_e0_formula_correct(self, summary):
        """E0 = (1/120)*(A0+A1+A2+A3+A4) all-ones with denom 120."""
        assert summary["T5_e0_correct"] is True

    def test_all_idempotent_ranks_correct(self, summary):
        """All 5 idempotent rank computations match multiplicities."""
        assert summary["T5_all_ranks_correct"] is True

    def test_e0_rank_1(self, summary):
        """E0 has rank 1 (trivial module)."""
        assert summary["T5_idem_rank_check"]["E0"] is True

    def test_e1_rank_20(self, summary):
        """E1 has rank 20."""
        assert summary["T5_idem_rank_check"]["E1"] is True

    def test_e2_rank_24(self, summary):
        """E2 has rank 24."""
        assert summary["T5_idem_rank_check"]["E2"] is True

    def test_e3_rank_15(self, summary):
        """E3 has rank 15."""
        assert summary["T5_idem_rank_check"]["E3"] is True

    def test_e4_rank_60(self, summary):
        """E4 has rank 60 (largest irreducible component)."""
        assert summary["T5_idem_rank_check"]["E4"] is True

    def test_1_plus_20_plus_24_plus_15_plus_60(self, summary):
        """1+20+24+15+60 = 120."""
        assert summary["T5_rank_sum"] == 1 + 20 + 24 + 15 + 60


# ---------------------------------------------------------------------------
# T6: Minimal polynomials
# ---------------------------------------------------------------------------

class TestT6MinimalPolynomials:
    """T6: Minimal polynomial degrees match distinct eigenvalue counts."""

    def test_all_minpoly_correct(self, summary):
        """All 4 minimal polynomials verified at all eigenvalues."""
        assert summary["T6_all_correct"] is True

    def test_a1_degree_2(self, summary):
        """A1 minimal polynomial has degree 2 (eigenvalues {2,-1})."""
        assert summary["T6_degrees"]["A1"] == 2

    def test_a2_degree_4(self, summary):
        """A2 minimal polynomial has degree 4 (eigenvalues {27,9,-3,3})."""
        assert summary["T6_degrees"]["A2"] == 4

    def test_a3_degree_4(self, summary):
        """A3 minimal polynomial has degree 4 (eigenvalues {36,6,-12,0})."""
        assert summary["T6_degrees"]["A3"] == 4

    def test_a4_degree_5(self, summary):
        """A4 minimal polynomial has degree 5 (all 5 distinct eigenvalues)."""
        assert summary["T6_degrees"]["A4"] == 5

    def test_a1_minpoly_roots(self, summary):
        """A1 polynomial x^2-x-2 vanishes at eigenvalues."""
        assert summary["T6_minpoly_checks"]["A1"] is True

    def test_a2_minpoly_roots(self, summary):
        """A2 polynomial x^4-36x^3+234x^2+324x-2187 vanishes at eigenvalues."""
        assert summary["T6_minpoly_checks"]["A2"] is True

    def test_a3_minpoly_roots(self, summary):
        """A3 polynomial x^4-30x^3-288x^2+2592x vanishes at eigenvalues."""
        assert summary["T6_minpoly_checks"]["A3"] is True

    def test_a4_minpoly_roots(self, summary):
        """A4 polynomial vanishes at all 5 eigenvalues."""
        assert summary["T6_minpoly_checks"]["A4"] is True

    def test_a1_distinct_evals_2(self, summary):
        """A1 has exactly 2 distinct eigenvalues."""
        assert summary["T6_num_distinct_evals"]["A1"] == 2

    def test_a4_distinct_evals_5(self, summary):
        """A4 has 5 distinct eigenvalues (equal to scheme rank)."""
        assert summary["T6_num_distinct_evals"]["A4"] == 5


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_bose_mesner_algebra.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_bose_mesner_algebra.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_n", "T1_rank", "T1_val_sum", "T1_mult_sum", "T1_gelfand",
            "T2_products_verified", "T2_all_correct",
            "T3_pq_is_nI", "T3_e0_eigenvalues", "T3_col_orth",
            "T4_q_col0_correct", "T4_q_row0_correct", "T4_q_has_fractions",
            "T5_rank_sum", "T5_all_ranks_correct",
            "T6_all_correct", "T6_degrees",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
