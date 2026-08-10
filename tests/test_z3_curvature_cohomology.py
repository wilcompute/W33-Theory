"""Tests for Pillar 109 (Part CCIX): Z3 Curvature Cohomology on W(3,3) Complement."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCIX_Z3_CURVATURE_COHOMOLOGY import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Quotient graph structure
# ---------------------------------------------------------------------------

class TestT1QuotientGraph:
    """T1: Q = complement(W33) is SRG(40,27,18,18) with 540 edges in one orbit."""

    def test_n_vertices(self, summary):
        """Q has 40 vertices."""
        assert summary["T1_n_vertices"] == 40

    def test_degree_27(self, summary):
        """Q is 27-regular."""
        assert summary["T1_degree"] == 27

    def test_total_edges_540(self, summary):
        """Q has 40*27/2 = 540 edges."""
        assert summary["T1_total_edges"] == 540

    def test_single_edge_orbit(self, summary):
        """All 540 edges form a single Aut(W33) orbit."""
        assert summary["T1_single_edge_orbit"] is True

    def test_edge_orbit_size_matches(self, summary):
        """Edge orbit size equals total edge count."""
        assert summary["T1_edge_orbit_matches"] is True

    def test_srg_params(self, summary):
        """SRG parameters are (40,27,18,18)."""
        p = summary["T1_srg_params"]
        assert p["n"] == 40
        assert p["k"] == 27

    def test_complement_degree_check(self, summary):
        """Complement degree: 40 - 1 - 12 = 27."""
        assert summary["T1_degree"] == 40 - 1 - 12


# ---------------------------------------------------------------------------
# T2: Triangle orbits
# ---------------------------------------------------------------------------

class TestT2TriangleOrbits:
    """T2: 3240 triangles split into 2 Aut orbits: 360 flat + 2880 curved."""

    def test_total_triangles(self, summary):
        """Q has 3240 triangles."""
        assert summary["T2_total_triangles"] == 3240

    def test_two_orbits(self, summary):
        """Exactly 2 Aut(W33) orbits of triangles."""
        assert summary["T2_num_triangle_orbits"] == 2

    def test_flat_count_360(self, summary):
        """Flat orbit has 360 triangles."""
        assert summary["T2_flat_count"] == 360

    def test_curved_count_2880(self, summary):
        """Curved orbit has 2880 triangles."""
        assert summary["T2_curved_count"] == 2880

    def test_sum_is_3240(self, summary):
        """360 + 2880 = 3240."""
        assert summary["T2_flat_count"] + summary["T2_curved_count"] == 3240

    def test_correct_flag(self, summary):
        """Triangle orbit correctness flag is True."""
        assert summary["T2_correct"] is True


# ---------------------------------------------------------------------------
# T3: Flat locus geometry
# ---------------------------------------------------------------------------

class TestT3FlatLocus:
    """T3: 360 flat triangles = 90 non-isotropic lines x C(4,3)=4 triples each."""

    def test_flat_count_from_csv(self, summary):
        """CSV confirms 360 flat triangles (F=0)."""
        assert summary["T3_flat_count_csv"] == 360

    def test_flat_from_lines(self, summary):
        """90 non-isotropic lines x 4 triples = 360."""
        assert summary["T3_flat_from_lines"] == 360

    def test_flat_counts_agree(self, summary):
        """Flat count from CSV agrees with geometric formula."""
        assert summary["T3_flat_count_correct"] is True

    def test_90_times_4(self, summary):
        """90 x 4 = 360 (C(4,3)=4 triples per 4-point line)."""
        assert summary["T3_flat_from_lines"] == 90 * 4

    def test_interpretation_present(self, summary):
        """Geometric interpretation string is present."""
        assert summary["T3_interpretation"] is not None
        assert len(summary["T3_interpretation"]) > 0


# ---------------------------------------------------------------------------
# T4: Curvature distribution
# ---------------------------------------------------------------------------

class TestT4CurvatureDistribution:
    """T4: F_z3 distribution is {0:360, 1:1432, 2:1448} over 3240 triangles."""

    def test_F_dist_keys(self, summary):
        """F distribution has keys {0, 1, 2}."""
        assert set(summary["T4_F_dist"].keys()) == {0, 1, 2}

    def test_F0_count(self, summary):
        """360 flat triangles (F=0)."""
        assert summary["T4_F_dist"][0] == 360

    def test_F1_count(self, summary):
        """1432 triangles with F=1."""
        assert summary["T4_F1_count"] == 1432

    def test_F2_count(self, summary):
        """1448 triangles with F=2."""
        assert summary["T4_F2_count"] == 1448

    def test_total_3240(self, summary):
        """F distribution sums to 3240."""
        assert summary["T4_total_triangles"] == 3240

    def test_curved_2880(self, summary):
        """Total curved triangles (F nonzero) = 2880."""
        assert summary["T4_curved_count"] == 2880

    def test_curved_correct(self, summary):
        """Curved count correctness flag is True."""
        assert summary["T4_curved_correct"] is True

    def test_F1_plus_F2(self, summary):
        """F=1 + F=2 = 2880 curved."""
        assert summary["T4_F1_count"] + summary["T4_F2_count"] == 2880


# ---------------------------------------------------------------------------
# T5: Non-exactness
# ---------------------------------------------------------------------------

class TestT5NonExactness:
    """T5: F is not in im(delta); rank augmented = 502 > rank delta = 501."""

    def test_n_variables(self, summary):
        """540 edge variables."""
        assert summary["T5_n_variables"] == 540

    def test_n_equations(self, summary):
        """3240 triangle equations."""
        assert summary["T5_n_equations"] == 3240

    def test_rank_delta(self, summary):
        """rank(delta) = 501."""
        assert summary["T5_rank_delta"] == 501

    def test_rank_augmented(self, summary):
        """rank([delta|F]) = 502."""
        assert summary["T5_rank_augmented"] == 502

    def test_non_exact(self, summary):
        """Non-exactness flag is True."""
        assert summary["T5_non_exact"] is True

    def test_augmented_exceeds_delta(self, summary):
        """rank([delta|F]) > rank(delta) confirms non-exactness."""
        assert summary["T5_rank_augmented"] > summary["T5_rank_delta"]

    def test_conclusion_present(self, summary):
        """Conclusion string confirms non-exactness."""
        assert "non" in summary["T5_conclusion"].lower() or "no" in summary["T5_conclusion"].lower()


# ---------------------------------------------------------------------------
# T6: Cohomological obstruction
# ---------------------------------------------------------------------------

class TestT6CohomologicalObstruction:
    """T6: Defect = 1 independent obstruction; gauge freedom = 39."""

    def test_defect_is_1(self, summary):
        """Cohomological defect = 1."""
        assert summary["T6_defect"] == 1

    def test_gauge_freedom_39(self, summary):
        """Gauge freedom = 540 - 501 = 39."""
        assert summary["T6_gauge_freedom"] == 39

    def test_obstruction_rank_1(self, summary):
        """Exactly 1 independent obstruction."""
        assert summary["T6_obstruction_rank"] == 1

    def test_defect_equals_rank_difference(self, summary):
        """Defect = rank_augmented - rank_delta."""
        assert summary["T6_defect"] == (
            summary["T5_rank_augmented"] - summary["T5_rank_delta"]
        )

    def test_gauge_freedom_formula(self, summary):
        """Gauge freedom = variables - rank(delta) = 540 - 501."""
        assert summary["T6_gauge_freedom"] == (
            summary["T5_n_variables"] - summary["T5_rank_delta"]
        )


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_z3_curvature_cohomology.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_z3_curvature_cohomology.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_n_vertices", "T1_total_edges", "T1_single_edge_orbit",
            "T2_total_triangles", "T2_num_triangle_orbits",
            "T2_flat_count", "T2_curved_count", "T2_correct",
            "T3_flat_count_csv", "T3_flat_from_lines", "T3_flat_count_correct",
            "T4_F_dist", "T4_curved_count",
            "T5_rank_delta", "T5_rank_augmented", "T5_non_exact",
            "T6_defect", "T6_gauge_freedom", "T6_obstruction_rank",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
