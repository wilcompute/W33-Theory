"""Tests for Pillar 119 (Part CCXIX): SRG36 Triangle Fibration over W33 Lines."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXIX_SRG36_TRIANGLE_FIBRATION import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: 1200 triangles split as 120 + 240 + 840
# ---------------------------------------------------------------------------

class TestT1TriangleSplit:
    """T1: 1200 = 120 faces + 240 odd-nonface + 840 even-nonface."""

    def test_1200_triangles(self, summary):
        """SRG(36,20,10,12) has 1200 triangles."""
        assert summary["T1_triangles_total"] == 1200

    def test_120_faces(self, summary):
        """120 faces chosen (holonomy 1)."""
        assert summary["T1_faces_chosen"] == 120

    def test_240_odd_nonfaces(self, summary):
        """240 odd non-face triangles (holonomy 1)."""
        assert summary["T1_nonface_hol1"] == 240

    def test_840_even_nonfaces(self, summary):
        """840 even non-face triangles (holonomy 0)."""
        assert summary["T1_nonface_hol0"] == 840

    def test_120_chosen_hol1(self, summary):
        """All 120 chosen faces have holonomy 1."""
        assert summary["T1_chosen_hol1"] == 120

    def test_sum_equals_1200(self, summary):
        """120 + 240 + 840 = 1200."""
        assert (summary["T1_faces_chosen"] +
                summary["T1_nonface_hol1"] +
                summary["T1_nonface_hol0"]) == 1200

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True


# ---------------------------------------------------------------------------
# T2: 240 odd non-faces fiber over 40 special faces
# ---------------------------------------------------------------------------

class TestT2OddNonfaceFibration:
    """T2: 240 odd non-faces / 40 special faces = fiber size 6."""

    def test_240_odd_nonfaces(self, summary):
        """240 odd non-face triangles."""
        assert summary["T2_n_odd"] == 240

    def test_40_special_faces(self, summary):
        """40 distinct special faces (fiber base)."""
        assert summary["T2_n_special"] == 40

    def test_fiber_size_6(self, summary):
        """Each special face has exactly 6 odd non-face preimages."""
        assert summary["T2_fiber_size"] == 6

    def test_all_fibers_size_6(self, summary):
        """All 40 fibers have exactly 6 elements."""
        assert summary["T2_all_fiber_size_6"] is True

    def test_240_equals_40_times_6(self, summary):
        """240 = 40 * 6."""
        assert summary["T2_n_odd"] == summary["T2_n_special"] * summary["T2_fiber_size"]

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True


# ---------------------------------------------------------------------------
# T3: 40 special faces = 40 W33 lines
# ---------------------------------------------------------------------------

class TestT3SpecialFacesLines:
    """T3: 40 special faces correspond bijectively to 40 W33 lines."""

    def test_40_special_faces(self, summary):
        """40 special faces in the list."""
        assert summary["T3_n_special"] == 40

    def test_line_ids_unique(self, summary):
        """Each special face has a unique line_id."""
        assert summary["T3_line_ids_unique"] is True

    def test_all_40_lines_covered(self, summary):
        """All 40 W33 line ids appear (0 through 39)."""
        assert summary["T3_all_lines_covered"] is True

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True


# ---------------------------------------------------------------------------
# T4: Face preimage map has degree 10
# ---------------------------------------------------------------------------

class TestT4PreimageDegree:
    """T4: Every face has exactly 10 preimages."""

    def test_120_faces(self, summary):
        """120 faces in the preimage map."""
        assert summary["T4_n_faces"] == 120

    def test_all_degree_10(self, summary):
        """Every face has total_preimages = 10."""
        assert summary["T4_all_degree_10"] is True

    def test_only_10_in_distribution(self, summary):
        """Preimage count distribution has only value 10."""
        assert list(summary["T4_preimage_dist"].keys()) == [10]

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True


# ---------------------------------------------------------------------------
# T5: Special face profile (6+3+1=10)
# ---------------------------------------------------------------------------

class TestT5SpecialFaceProfile:
    """T5: Each special face: 6 odd + 3 even + 1 self = 10 preimages."""

    def test_40_special_faces(self, summary):
        """40 special faces in profile check."""
        assert summary["T5_n_special"] == 40

    def test_all_odd_6(self, summary):
        """All special faces have exactly 6 odd non-face preimages."""
        assert summary["T5_all_odd_6"] is True

    def test_all_even_3(self, summary):
        """All special faces have exactly 3 even non-face preimages."""
        assert summary["T5_all_even_3"] is True

    def test_6_plus_3_plus_1_equals_10(self, summary):
        """6 odd + 3 even + 1 self = 10."""
        assert summary["T5_all_total_10"] is True

    def test_t5_correct(self, summary):
        """T5 overall correctness flag."""
        assert summary["T5_correct"] is True


# ---------------------------------------------------------------------------
# T6: Ordinary face profile (0+9+1=10)
# ---------------------------------------------------------------------------

class TestT6OrdinaryFaceProfile:
    """T6: Each ordinary face: 0 odd + 9 even + 1 self = 10 preimages."""

    def test_80_ordinary_faces(self, summary):
        """80 ordinary faces."""
        assert summary["T6_n_ordinary"] == 80

    def test_all_odd_0(self, summary):
        """All ordinary faces have 0 odd non-face preimages."""
        assert summary["T6_all_odd_0"] is True

    def test_all_even_9(self, summary):
        """All ordinary faces have exactly 9 even non-face preimages."""
        assert summary["T6_all_even_9"] is True

    def test_0_plus_9_plus_1_equals_10(self, summary):
        """0 odd + 9 even + 1 self = 10."""
        assert summary["T6_all_total_10"] is True

    def test_40_plus_80_equals_120(self, summary):
        """40 special + 80 ordinary = 120 faces total."""
        assert summary["T6_special_plus_ordinary"] == 120

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_srg36_triangle_fibration.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_srg36_triangle_fibration.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_triangles_total", "T1_faces_chosen", "T1_nonface_hol1",
            "T1_nonface_hol0", "T1_correct",
            "T2_n_odd", "T2_n_special", "T2_fiber_size", "T2_correct",
            "T3_n_special", "T3_all_lines_covered", "T3_correct",
            "T4_n_faces", "T4_all_degree_10", "T4_correct",
            "T5_n_special", "T5_all_odd_6", "T5_all_even_3", "T5_correct",
            "T6_n_ordinary", "T6_all_odd_0", "T6_all_even_9", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
