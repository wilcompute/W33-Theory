"""Tests for Pillar 115 (Part CCXV): E8 Root Decomposition under E6 x A2."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXV_E8_E6A2_DECOMP import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Dot-pair invariant
# ---------------------------------------------------------------------------

class TestT1DotPairInvariant:
    """T1: 13 dot-pair classes totaling 240 E8 roots."""

    def test_13_classes(self, summary):
        """Exactly 13 dot-pair classes."""
        assert summary["T1_n_classes"] == 13

    def test_240_total_roots(self, summary):
        """All 240 E8 roots classified."""
        assert summary["T1_total_roots"] == 240

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True

    def test_largest_class_72(self, summary):
        """Largest class has 72 roots (E6)."""
        assert summary["T1_class_sizes"][0] == 72

    def test_class_sizes_sum_240(self, summary):
        """All class sizes sum to 240."""
        assert sum(summary["T1_class_sizes"]) == 240


# ---------------------------------------------------------------------------
# T2: E6 sector
# ---------------------------------------------------------------------------

class TestT2E6Sector:
    """T2: 72 roots with dot-pair (0,0) form the E6 root system."""

    def test_72_e6_roots(self, summary):
        """E6 sector contains exactly 72 roots."""
        assert summary["T2_e6_size"] == 72

    def test_e6_key_is_00(self, summary):
        """E6 sector key is [0, 0]."""
        assert summary["T2_e6_key"] == [0, 0]

    def test_t2_e6_correct(self, summary):
        """T2 E6 correctness flag."""
        assert summary["T2_e6_correct"] is True

    def test_72_equals_e6_nonzero_roots(self, summary):
        """72 = dim(E6) - rank(E6) = 78 - 6."""
        assert summary["T2_e6_size"] == 78 - 6


# ---------------------------------------------------------------------------
# T3: A2 sector
# ---------------------------------------------------------------------------

class TestT3A2Sector:
    """T3: 6 singleton roots forming the A2 root system."""

    def test_6_a2_roots(self, summary):
        """A2 sector has exactly 6 roots."""
        assert summary["T3_a2_total"] == 6

    def test_all_singletons(self, summary):
        """All A2 classes are singletons (size 1)."""
        assert summary["T3_all_singletons"] is True

    def test_6_singleton_classes(self, summary):
        """6 singleton dot-pair classes."""
        assert summary["T3_n_singleton_classes"] == 6

    def test_t3_a2_correct(self, summary):
        """T3 A2 correctness flag."""
        assert summary["T3_a2_correct"] is True

    def test_6_equals_2_times_3(self, summary):
        """6 = 2 * 3 (rank-2 A2 = SU(3) has 3 positive roots and 3 negative)."""
        assert summary["T3_a2_total"] == 2 * 3


# ---------------------------------------------------------------------------
# T4: Mixed sector
# ---------------------------------------------------------------------------

class TestT4MixedSector:
    """T4: 162 = 6 x 27 mixed (E6 x A2 fundamental representation) roots."""

    def test_162_mixed_roots(self, summary):
        """Mixed sector has exactly 162 roots."""
        assert summary["T4_mixed_total"] == 162

    def test_all_size_27(self, summary):
        """All 6 mixed-sector classes have size exactly 27."""
        assert summary["T4_all_27"] is True

    def test_6_mixed_classes(self, summary):
        """Exactly 6 mixed-sector dot-pair classes."""
        assert summary["T4_n_mixed_classes"] == 6

    def test_mixed_correct(self, summary):
        """T4 mixed correctness flag."""
        assert summary["T4_mixed_correct"] is True

    def test_total_check(self, summary):
        """72 + 6 + 162 = 240."""
        assert summary["T4_total_check"] is True

    def test_6_times_27_equals_162(self, summary):
        """6 * 27 = 162."""
        assert summary["T4_n_mixed_classes"] * summary["T4_mixed_total"] // summary["T4_n_mixed_classes"] == 162


# ---------------------------------------------------------------------------
# T5: Non-conjugate representations
# ---------------------------------------------------------------------------

class TestT5NonConjugate:
    """T5: Edgepair action transitive; line action intransitive; non-conjugate."""

    def test_edgepair_transitive(self, summary):
        """Edgepair action is transitive (one orbit of size 120)."""
        assert summary["T5_ep_transitive"] is True

    def test_edgepair_one_orbit_120(self, summary):
        """Edgepair orbit sizes = [120]."""
        assert summary["T5_ep_orbit_sizes"] == [120]

    def test_line_intransitive(self, summary):
        """Line action is intransitive (more than one orbit)."""
        assert summary["T5_line_intransitive"] is True

    def test_line_orbit_sizes(self, summary):
        """Line orbit sizes = [36, 27, 27, 27, 1, 1, 1]."""
        assert summary["T5_line_orbit_sizes"] == [36, 27, 27, 27, 1, 1, 1]

    def test_non_conjugate(self, summary):
        """The two degree-120 representations are non-conjugate."""
        assert summary["T5_non_conjugate"] is True

    def test_line_orbits_sum_120(self, summary):
        """36 + 27+27+27 + 1+1+1 = 120."""
        assert sum(summary["T5_line_orbit_sizes"]) == 120


# ---------------------------------------------------------------------------
# T6: Three-generation structure
# ---------------------------------------------------------------------------

class TestT6ThreeGenerations:
    """T6: Line orbits encode 36 E6 lines + 3x27 generations + 3 A2 color lines."""

    def test_36_e6_lines(self, summary):
        """36 E6 root lines (72 E6 roots / 2)."""
        assert summary["T6_e6_lines"] == 36

    def test_3_a2_lines(self, summary):
        """3 A2 root lines (6 A2 roots / 2)."""
        assert summary["T6_a2_lines"] == 3

    def test_27_per_generation(self, summary):
        """Each generation has 27 matter-field lines."""
        assert summary["T6_matter_lines_per_gen"] == 27

    def test_3_generations(self, summary):
        """Three matter-field generations."""
        assert summary["T6_n_generations"] == 3

    def test_total_120_lines(self, summary):
        """36 + 3*27 + 3 = 120 lines total."""
        assert summary["T6_total_lines_check"] == 120

    def test_one_orbit_of_36(self, summary):
        """Exactly 1 line orbit of size 36 (E6 sector)."""
        assert summary["T6_line_36_count"] == 1

    def test_three_orbits_of_27(self, summary):
        """Exactly 3 line orbits of size 27 (three generations)."""
        assert summary["T6_line_27_count"] == 3

    def test_three_singletons(self, summary):
        """Exactly 3 singleton line orbits (A2 color generators)."""
        assert summary["T6_line_1_count"] == 3

    def test_structure_correct(self, summary):
        """Three-generation structure correctness flag."""
        assert summary["T6_structure_correct"] is True

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_e8_e6a2_decomp.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_e8_e6a2_decomp.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_n_classes", "T1_total_roots", "T1_correct",
            "T2_e6_size", "T2_e6_correct",
            "T3_a2_total", "T3_a2_correct",
            "T4_mixed_total", "T4_all_27", "T4_total_check",
            "T5_ep_transitive", "T5_line_intransitive", "T5_non_conjugate",
            "T5_line_orbit_sizes",
            "T6_e6_lines", "T6_n_generations", "T6_structure_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
