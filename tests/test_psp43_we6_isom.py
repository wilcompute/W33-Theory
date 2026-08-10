"""Tests for Pillar 113 (Part CCXIII): PSp(4,3) = W(E6)+ Explicit Isomorphism."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXIII_PSP43_WE6_ISOM import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Group orders and isomorphism
# ---------------------------------------------------------------------------

class TestT1GroupOrders:
    """T1: |PSp(4,3)| = 25920 = |W(E6)+|; W(E6) has order 51840; index 2."""

    def test_sp43_order_25920(self, summary):
        """|PSp(4,3)| = 25920."""
        assert summary["T1_sp43_order"] == 25920

    def test_we6_even_order_25920(self, summary):
        """|W(E6)+| = 25920."""
        assert summary["T1_we6_even_order"] == 25920

    def test_orders_match(self, summary):
        """PSp(4,3) and W(E6)+ have equal order."""
        assert summary["T1_orders_match"] is True

    def test_we6_full_order_51840(self, summary):
        """|W(E6)| = 51840."""
        assert summary["T1_we6_full_order"] == 51840

    def test_index_2(self, summary):
        """|W(E6)| = 2 * |W(E6)+| (index-2 subgroup)."""
        assert summary["T1_index_2"] is True

    def test_order_spectrum_equal(self, summary):
        """Order spectra of PSp(4,3) and W(E6)+ are identical."""
        assert summary["T1_order_spectrum_equal"] is True

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True

    def test_51840_equals_2_times_25920(self, summary):
        """51840 = 2 * 25920."""
        assert summary["T1_we6_full_order"] == 2 * summary["T1_we6_even_order"]


# ---------------------------------------------------------------------------
# T2: Word map
# ---------------------------------------------------------------------------

class TestT2WordMap:
    """T2: 10 Sp(4,3) generators expressed as words of length 7-12 in W(E6)+ generators."""

    def test_10_gen_maps(self, summary):
        """Exactly 10 generator word maps."""
        assert summary["T2_num_gen_maps"] == 10

    def test_word_lengths_range(self, summary):
        """Word lengths are in range [7, 12]."""
        for length in summary["T2_word_lengths"]:
            assert 7 <= length <= 12

    def test_min_word_len_7(self, summary):
        """Shortest word has length 7."""
        assert summary["T2_min_word_len"] == 7

    def test_max_word_len_12(self, summary):
        """Longest word has length 12."""
        assert summary["T2_max_word_len"] == 12

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True


# ---------------------------------------------------------------------------
# T3: Root system isometry
# ---------------------------------------------------------------------------

class TestT3RootIsometry:
    """T3: Each mapped generator preserves E8 antipodes and dot products on 240 roots."""

    def test_all_antipode_preserved(self, summary):
        """All 10 generators preserve E8 antipode pairs."""
        assert summary["T3_all_antipode"] is True

    def test_all_dot_preserved(self, summary):
        """All 10 generators preserve E8 inner-product matrix."""
        assert summary["T3_all_dot"] is True

    def test_10_checks(self, summary):
        """Exactly 10 generators checked."""
        assert summary["T3_num_checks"] == 10

    def test_antipode_direct(self, summary):
        """Direct antipode check on gen 0: perm(r+120) = perm(r)+120 for r in 0..119."""
        assert summary["T3_antipode_direct"] is True

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True


# ---------------------------------------------------------------------------
# T4: Line permutation orders
# ---------------------------------------------------------------------------

class TestT4LinePermOrders:
    """T4: Induced line permutation orders are [3,3,3,3,3,3,4,4,2,2]."""

    def test_orders_match_bundle(self, summary):
        """Bundle-reported orders match expected [3,3,3,3,3,3,4,4,2,2]."""
        assert summary["T4_orders_match_bundle"] is True

    def test_orders_computed_match(self, summary):
        """Independently computed orders match expected."""
        assert summary["T4_orders_computed_match"] is True

    def test_six_order_3(self, summary):
        """6 generators of order 3."""
        assert summary["T4_six_order3"] is True

    def test_two_order_4(self, summary):
        """2 generators of order 4."""
        assert summary["T4_two_order4"] is True

    def test_two_order_2(self, summary):
        """2 generators of order 2."""
        assert summary["T4_two_order2"] is True

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True

    def test_line_orders_list(self, summary):
        """Line orders list is exactly [3,3,3,3,3,3,4,4,2,2]."""
        assert summary["T4_line_orders"] == [3, 3, 3, 3, 3, 3, 4, 4, 2, 2]


# ---------------------------------------------------------------------------
# T5: Sign cocycle triviality
# ---------------------------------------------------------------------------

class TestT5SignCocycle:
    """T5: Sign cocycle is trivial (0 non-trivial pairs); embedding is a genuine lift."""

    def test_cocycle_trivial(self, summary):
        """Sign cocycle is trivial."""
        assert summary["T5_cocycle_trivial"] is True

    def test_zero_nontrivial_pairs(self, summary):
        """Zero non-trivial sign pairs."""
        assert summary["T5_nontrivial_pairs"] == 0

    def test_eps_counts_match(self, summary):
        """Eps-minus counts from bundle match direct computation."""
        assert summary["T5_eps_counts_match"] is True

    def test_eps_counts_positive(self, summary):
        """Some eps-minus signs exist (non-zero total)."""
        assert summary["T5_total_eps_minus"] > 0

    def test_10_eps_counts(self, summary):
        """10 per-generator eps-minus counts."""
        assert len(summary["T5_eps_minus_counts"]) == 10


# ---------------------------------------------------------------------------
# T6: W(E6) generator structure
# ---------------------------------------------------------------------------

class TestT6WE6Structure:
    """T6: W(E6) has 6 Coxeter generators, 15 even generators; order 51840."""

    def test_we6_order_51840(self, summary):
        """|W(E6)| = 51840."""
        assert summary["T6_we6_order"] == 51840

    def test_we6_even_order_25920(self, summary):
        """|W(E6)+| = 25920."""
        assert summary["T6_we6_even_order"] == 25920

    def test_6_coxeter_generators(self, summary):
        """W(E6) has 6 Coxeter generators."""
        assert summary["T6_n_coxeter"] == 6

    def test_15_even_generators(self, summary):
        """W(E6)+ has 15 even generators."""
        assert summary["T6_n_even_gens"] == 15

    def test_order_ratio_2(self, summary):
        """|W(E6)| / |W(E6)+| = 2."""
        assert summary["T6_order_ratio"] == 2

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True

    def test_25920_times_2_is_51840(self, summary):
        """25920 * 2 = 51840."""
        assert summary["T6_we6_order"] == 2 * summary["T6_we6_even_order"]


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_psp43_we6_isom.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_psp43_we6_isom.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_sp43_order", "T1_we6_even_order", "T1_orders_match",
            "T1_order_spectrum_equal", "T1_correct",
            "T2_num_gen_maps", "T2_word_lengths", "T2_correct",
            "T3_all_antipode", "T3_all_dot", "T3_correct",
            "T4_line_orders", "T4_orders_computed_match", "T4_correct",
            "T5_cocycle_trivial", "T5_nontrivial_pairs",
            "T6_we6_order", "T6_n_coxeter", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
