"""Tests for Pillar 106 (Part CCVI): Klein Correspondence W(3,3) <-> Q(4,3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCVI_KLEIN_CORRESPONDENCE import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: W(3,3) geometry
# ---------------------------------------------------------------------------

class TestT1W33Geometry:
    """T1: W(3,3) has exactly 40 points, 40 lines, 4 pts/line, 4 lines/pt."""

    def test_num_points(self, summary):
        """Exactly 40 points in W(3,3)."""
        assert summary["T1_num_W33_points"] == 40

    def test_num_lines(self, summary):
        """Exactly 40 totally isotropic lines."""
        assert summary["T1_num_W33_lines"] == 40

    def test_pts_per_line(self, summary):
        """Every line contains exactly 4 points."""
        assert summary["T1_pts_per_line"] == {4: 40}

    def test_lines_per_pt(self, summary):
        """Every point lies on exactly 4 lines."""
        assert summary["T1_lines_per_pt"] == {4: 40}

    def test_symmetric_parameters(self, summary):
        """W(3,3) has the same number of points and lines (40)."""
        assert summary["T1_num_W33_points"] == summary["T1_num_W33_lines"]


# ---------------------------------------------------------------------------
# T2: Q(4,3) quadric
# ---------------------------------------------------------------------------

class TestT2Q43Quadric:
    """T2: All 40 Klein images lie on the parabolic quadric Q(4,3)."""

    def test_all_on_quadric(self, summary):
        """All 40 Q-points satisfy the quadric equation."""
        assert summary["T2_all_on_quadric"] is True

    def test_quadric_count(self, summary):
        """Exactly 40 points on the quadric."""
        assert summary["T2_quadric_satisfied_count"] == 40

    def test_quadric_equation_present(self, summary):
        """Quadric equation metadata is present."""
        assert summary["T2_quadric_equation"] is not None


# ---------------------------------------------------------------------------
# T3: Klein bijectivity
# ---------------------------------------------------------------------------

class TestT3KleinBijectivity:
    """T3: The Klein map is a bijection from 40 W-lines to 40 Q-points."""

    def test_map_length(self, summary):
        """Klein map has 40 entries."""
        assert summary["T3_klein_map_length"] == 40

    def test_bijective(self, summary):
        """Klein map is bijective (every Q-point hit exactly once)."""
        assert summary["T3_klein_bijective"] is True

    def test_40_equals_40(self, summary):
        """40 lines map to 40 distinct Q-points."""
        assert summary["T3_klein_map_length"] == summary["T1_num_W33_lines"]


# ---------------------------------------------------------------------------
# T4: Duality isomorphism
# ---------------------------------------------------------------------------

class TestT4DualityIsomorphism:
    """T4: W-points map to Q-lines giving incidence-preserving isomorphism W(3,3)~=Q(4,3)^dual."""

    def test_num_q_lines(self, summary):
        """Exactly 40 Q-lines."""
        assert summary["T4_num_Q_lines"] == 40

    def test_q_line_sizes(self, summary):
        """Every Q-line has exactly 4 points."""
        assert summary["T4_Q_line_sizes"] == {4: 40}

    def test_qlines_per_qpt(self, summary):
        """Every Q-point lies on exactly 4 Q-lines."""
        assert summary["T4_Qlines_per_Qpt"] == {4: 40}

    def test_isomorphism_holds(self, summary):
        """Duality isomorphism flag is True."""
        assert summary["T4_duality_isomorphism"] is True


# ---------------------------------------------------------------------------
# T5: Sp(4,3) induces SO(5,3)
# ---------------------------------------------------------------------------

class TestT5GroupInduction:
    """T5: The 6 Sp(4,3) generators induce SO(5,3) matrices preserving the quadratic form."""

    def test_num_generators(self, summary):
        """Exactly 6 generators (T_e1, T_e2, T_e3, T_e4, A, B)."""
        assert summary["T5_num_generators"] == 6

    def test_generator_names_present(self, summary):
        """Generator names are provided."""
        names = summary["T5_generator_names"]
        assert len(names) == 6

    def test_sp43_all_preserve_omega(self, summary):
        """All 6 Sp(4,3) generators preserve the symplectic form omega."""
        assert summary["T5_Sp43_all_preserve_omega"] is True

    def test_so53_all_preserve_S(self, summary):
        """All 6 induced SO(5,3) matrices preserve the quadratic form S."""
        assert summary["T5_SO53_all_preserve_S"] is True

    def test_sp43_individual_all_true(self, summary):
        """Each individual Sp(4,3) generator preserves omega."""
        for name, result in summary["T5_Sp43_individual"].items():
            assert result is True, f"Sp(4,3) generator {name} fails omega preservation"

    def test_so53_individual_all_true(self, summary):
        """Each individual SO(5,3) generator preserves S."""
        for name, result in summary["T5_SO53_individual"].items():
            assert result is True, f"SO(5,3) generator {name} fails S preservation"


# ---------------------------------------------------------------------------
# T6: Parameter symmetry
# ---------------------------------------------------------------------------

class TestT6ParameterSymmetry:
    """T6: W(3,3) and Q(4,3) share identical parameters (40, 40, 4, 4)."""

    def test_parameter_symmetry(self, summary):
        """Parameter symmetry flag is True."""
        assert summary["T6_parameter_symmetry"] is True

    def test_shared_points(self, summary):
        """Both spaces have 40 points."""
        assert summary["T6_shared_params"]["points"] == 40

    def test_shared_lines(self, summary):
        """Both spaces have 40 lines."""
        assert summary["T6_shared_params"]["lines"] == 40

    def test_shared_pts_per_line(self, summary):
        """Both spaces have 4 points per line."""
        assert summary["T6_shared_params"]["pts_per_line"] == 4

    def test_shared_lines_per_pt(self, summary):
        """Both spaces have 4 lines per point."""
        assert summary["T6_shared_params"]["lines_per_pt"] == 4

    def test_w33_params_match_shared(self, summary):
        """W(3,3) parameters match shared parameters."""
        shared = summary["T6_shared_params"]
        assert summary["T1_num_W33_points"] == shared["points"]
        assert summary["T1_num_W33_lines"] == shared["lines"]

    def test_q43_params_match_shared(self, summary):
        """Q(4,3) parameters match shared parameters."""
        shared = summary["T6_shared_params"]
        assert summary["T4_num_Q_lines"] == shared["lines"]
        assert summary["T2_quadric_satisfied_count"] == shared["points"]


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_klein_correspondence.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_klein_correspondence.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_num_W33_points", "T1_num_W33_lines",
            "T1_pts_per_line", "T1_lines_per_pt",
            "T2_quadric_satisfied_count", "T2_all_on_quadric",
            "T3_klein_map_length", "T3_klein_bijective",
            "T4_num_Q_lines", "T4_Q_line_sizes",
            "T4_Qlines_per_Qpt", "T4_duality_isomorphism",
            "T5_num_generators", "T5_Sp43_all_preserve_omega",
            "T5_SO53_all_preserve_S",
            "T6_parameter_symmetry", "T6_shared_params",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
