"""Tests for Pillar 117 (Part CCXVII): Z2 Holonomy Obstruction in Edgepair Transport."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXVII_HOLONOMY_Z2_FLAT_Z3 import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Z3 flat on edgepairs
# ---------------------------------------------------------------------------

class TestT1Z3Flat:
    """T1: rot_Z3 = 0 for all 1200 generator-edgepair moves."""

    def test_all_rot_zero(self, summary):
        """Z3 rotation is zero in every generator-edgepair move."""
        assert summary["T1_all_rot_zero"] is True

    def test_1200_moves(self, summary):
        """Exactly 1200 = 10 gens * 120 edgepairs moves."""
        assert summary["T1_n_moves"] == 1200

    def test_only_zero_in_rot_values(self, summary):
        """Only rot value is 0."""
        assert summary["T1_rot_values"] == [0]

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True

    def test_10_times_120_equals_1200(self, summary):
        """10 * 120 = 1200."""
        assert summary["T1_n_moves"] == 10 * 120


# ---------------------------------------------------------------------------
# T2: Z2 nontrivial on edgepairs
# ---------------------------------------------------------------------------

class TestT2Z2Nontrivial:
    """T2: 184/1200 moves have flip_Z2 = 1; rot_Z3 always 0."""

    def test_1016_trivial(self, summary):
        """1016 trivial (flip=0, rot=0) moves."""
        assert summary["T2_trivial_count"] == 1016

    def test_184_flips(self, summary):
        """184 Z2-flip (flip=1, rot=0) moves."""
        assert summary["T2_flip_count"] == 184

    def test_all_z3_zero(self, summary):
        """All flip_Z2 moves still have rot_Z3 = 0."""
        assert summary["T2_all_z3_zero"] is True

    def test_g0_flips_60(self, summary):
        """Generator g0 flips exactly 60 edgepairs."""
        assert summary["T2_g0_flips"] == 60

    def test_g6_flips_60(self, summary):
        """Generator g6 flips exactly 60 edgepairs."""
        assert summary["T2_g6_flips"] == 60

    def test_g4_flips_54(self, summary):
        """Generator g4 flips exactly 54 edgepairs."""
        assert summary["T2_g4_flips"] == 54

    def test_4_gens_flip_nothing(self, summary):
        """Generators g2, g3, g8, g9 flip no edgepairs."""
        assert set(summary["T2_zero_flip_gens"]) == {2, 3, 8, 9}

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True

    def test_1016_plus_184_equals_1200(self, summary):
        """1016 + 184 = 1200."""
        assert summary["T2_trivial_count"] + summary["T2_flip_count"] == 1200


# ---------------------------------------------------------------------------
# T3: Generator-cycle holonomy trivial
# ---------------------------------------------------------------------------

class TestT3GeneratorCycleHolonomy:
    """T3: All 480 generator-cycle holonomy entries are (0,0)."""

    def test_all_trivial_holonomy(self, summary):
        """All generator cycle holonomies are (flip=0, rot=0)."""
        assert summary["T3_all_trivial"] is True

    def test_480_entries(self, summary):
        """480 holonomy entries (10 gens * ~48 cycles each on average)."""
        assert summary["T3_n_hol_entries"] == 480

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True


# ---------------------------------------------------------------------------
# T4: Commutator [g4, g5] is unique nontrivial
# ---------------------------------------------------------------------------

class TestT4CommutatorHolonomy:
    """T4: Exactly 1 of 45 commutators has nontrivial holonomy: [g4,g5]."""

    def test_45_commutator_pairs(self, summary):
        """C(10,2) = 45 commutator pairs checked."""
        assert summary["T4_n_comm_pairs"] == 45

    def test_exactly_1_nontrivial(self, summary):
        """Exactly 1 commutator pair has nontrivial holonomy."""
        assert summary["T4_n_nontrivial"] == 1

    def test_nontrivial_pair_is_g4_g5(self, summary):
        """The nontrivial commutator is [g4, g5]."""
        assert summary["T4_nontrivial_pair"] == [4, 5]

    def test_commutator_order_2(self, summary):
        """[g4, g5] has order 2."""
        assert summary["T4_comm_order"] == 2

    def test_8_fixed_reflections(self, summary):
        """[g4, g5] has 8 fixed edgepairs with Z2-flip holonomy."""
        assert summary["T4_fixed_reflections"] == 8

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True

    def test_unique_comm_flag(self, summary):
        """T4 unique_comm flag is True."""
        assert summary["T4_unique_comm"] is True


# ---------------------------------------------------------------------------
# T5: Internal flip of edgepairs
# ---------------------------------------------------------------------------

class TestT5InternalFlip:
    """T5: All 120 edgepairs have internal flip (1,0): opposite edge reflects."""

    def test_all_internal_flip_1(self, summary):
        """All internal edgepair flips are (flip=1, rot=0)."""
        assert summary["T5_all_flip1"] is True

    def test_120_internal_flips(self, summary):
        """All 120 edgepairs have internal flip recorded."""
        assert summary["T5_flip_count"] == 120

    def test_t5_correct(self, summary):
        """T5 overall correctness flag."""
        assert summary["T5_correct"] is True


# ---------------------------------------------------------------------------
# T6: Word length for nontrivial holonomy
# ---------------------------------------------------------------------------

class TestT6WordLengthHolonomy:
    """T6: Nontrivial Z2 holonomy requires word length >= 6."""

    def test_sample_exists(self, summary):
        """Sample of nontrivial holonomy elements is non-empty."""
        assert summary["T6_n_sample"] > 0

    def test_min_word_len_at_least_6(self, summary):
        """Shortest word with nontrivial holonomy has length >= 6."""
        assert summary["T6_min_len_at_least_6"] is True

    def test_min_word_len_6(self, summary):
        """Minimum sample word length is exactly 6."""
        assert summary["T6_min_word_len"] == 6

    def test_max_word_len_8(self, summary):
        """Maximum sample word length is 8."""
        assert summary["T6_max_word_len"] == 8

    def test_all_sample_nontrivial(self, summary):
        """All sample elements genuinely have nontrivial cycle holonomy."""
        assert summary["T6_all_nontrivial"] is True

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True

    def test_5_sample_elements(self, summary):
        """Exactly 5 sample elements provided."""
        assert summary["T6_n_sample"] == 5


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_holonomy_z2_flat_z3.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_holonomy_z2_flat_z3.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_all_rot_zero", "T1_n_moves", "T1_correct",
            "T2_trivial_count", "T2_flip_count", "T2_all_z3_zero", "T2_correct",
            "T3_all_trivial", "T3_n_hol_entries", "T3_correct",
            "T4_n_comm_pairs", "T4_n_nontrivial", "T4_nontrivial_pair",
            "T4_comm_order", "T4_fixed_reflections", "T4_correct",
            "T5_all_flip1", "T5_flip_count", "T5_correct",
            "T6_n_sample", "T6_min_word_len", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
