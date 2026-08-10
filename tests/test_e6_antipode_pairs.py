"""Tests for Pillar 112 (Part CCXII): E6 Antipode Pairs and SRG Triangle Decomposition."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXII_E6_ANTIPODE_PAIRS import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Antipode pairs
# ---------------------------------------------------------------------------

class TestT1AntipodePairs:
    """T1: 36 antipode pairs from 72 E6 roots; each pair is {r, r+120}."""

    def test_36_pairs(self, summary):
        """Exactly 36 antipode pairs."""
        assert summary["T1_num_pairs"] == 36

    def test_all_roots_distinct(self, summary):
        """All 72 roots in pairs are distinct."""
        assert summary["T1_all_roots_distinct"] is True

    def test_pairs_antipodal(self, summary):
        """Each pair satisfies |pair[1] - pair[0]| = 120."""
        assert summary["T1_pairs_antipodal"] is True

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True


# ---------------------------------------------------------------------------
# T2: SRG(36,20,10,12)
# ---------------------------------------------------------------------------

class TestT2SRG:
    """T2: Strongly regular graph SRG(36,20,10,12) on 36 antipode-pair vertices."""

    def test_360_edges(self, summary):
        """SRG has 360 edges (36*20/2)."""
        assert summary["T2_num_edges"] == 360

    def test_degree_20(self, summary):
        """Every vertex has degree 20."""
        assert summary["T2_all_degrees_20"] is True

    def test_lambda_10(self, summary):
        """Adjacent pairs share exactly 10 common neighbors."""
        assert summary["T2_all_lambda_correct"] is True

    def test_srg_correct(self, summary):
        """SRG verification flag."""
        assert summary["T2_srg_correct"] is True

    def test_36_times_20_div_2(self, summary):
        """360 = 36 * 20 / 2."""
        assert summary["T2_num_edges"] == 36 * 20 // 2

    def test_mu_12(self, summary):
        """Non-adjacent pairs share exactly 12 common neighbors (sample)."""
        assert summary["T2_mu_correct"] is True


# ---------------------------------------------------------------------------
# T3: Triangle partition
# ---------------------------------------------------------------------------

class TestT3TrianglePartition:
    """T3: 120 triangles exactly partition all 360 SRG edges."""

    def test_120_triangles(self, summary):
        """Exactly 120 triangles."""
        assert summary["T3_num_triangles"] == 120

    def test_all_cliques(self, summary):
        """Every triangle is a clique (all 3 edges present in SRG)."""
        assert summary["T3_all_cliques"] is True

    def test_each_edge_once(self, summary):
        """Every SRG edge appears in exactly one triangle."""
        assert summary["T3_each_edge_once"] is True

    def test_all_edges_covered(self, summary):
        """All 360 SRG edges are covered by the triangle partition."""
        assert summary["T3_all_edges_covered"] is True

    def test_partition_correct(self, summary):
        """Full partition correctness flag."""
        assert summary["T3_partition_correct"] is True

    def test_120_times_3_is_360(self, summary):
        """120 triangles * 3 edges each = 360 SRG edges."""
        assert summary["T3_edge_times_3"] is True


# ---------------------------------------------------------------------------
# T4: W(3,3) line geometry
# ---------------------------------------------------------------------------

class TestT4W33LineGeometry:
    """T4: 40 W(3,3) lines, each contributing 3 triangles = 120 total."""

    def test_40_lines(self, summary):
        """W(3,3) has 40 lines."""
        assert summary["T4_num_lines"] == 40

    def test_3_triangles_per_line(self, summary):
        """Each line contributes exactly 3 triangles."""
        assert summary["T4_all_3_per_line"] is True

    def test_40_times_3_equals_120(self, summary):
        """40 lines * 3 triangles = 120 triangles."""
        assert summary["T4_40_times_3"] is True

    def test_total_from_lines_120(self, summary):
        """Total triangles from W(3,3) lines = 120."""
        assert summary["T4_total_from_lines"] == 120

    def test_coverage_complete(self, summary):
        """Line triangles cover all 120 triangle blocks."""
        assert summary["T4_coverage_complete"] is True

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True


# ---------------------------------------------------------------------------
# T5: PSp(4,3) generator action
# ---------------------------------------------------------------------------

class TestT5GeneratorAction:
    """T5: 10 Sp(4,3) generators act on 36 vertices; transitive; orders in {2,3,4}."""

    def test_10_generators(self, summary):
        """Exactly 10 generators."""
        assert summary["T5_num_gens"] == 10

    def test_transitive(self, summary):
        """Generators act transitively (orbit = all 36 vertices)."""
        assert summary["T5_transitive"] is True

    def test_orbit_size_36(self, summary):
        """Orbit of any vertex under all generators = 36."""
        assert summary["T5_orbit_size"] == 36

    def test_generator_orders(self, summary):
        """Generator orders are all in {2, 3, 4}."""
        for order in summary["T5_gen_orders"]:
            assert order in {2, 3, 4}

    def test_six_order_3_gens(self, summary):
        """6 generators of order 3."""
        assert summary["T5_gen_orders"].count(3) == 6

    def test_two_order_4_gens(self, summary):
        """2 generators of order 4."""
        assert summary["T5_gen_orders"].count(4) == 2

    def test_two_order_2_gens(self, summary):
        """2 generators of order 2."""
        assert summary["T5_gen_orders"].count(2) == 2


# ---------------------------------------------------------------------------
# T6: Transport cocycles
# ---------------------------------------------------------------------------

class TestT6TransportCocycles:
    """T6: Z3 rotation and Z2 flip transport on 240 W(3,3) edges x 10 generators."""

    def test_z3_total_2400(self, summary):
        """Total Z3 transport entries = 240 * 10 = 2400."""
        assert summary["T6_z3_total"] == 2400

    def test_z2_total_2400(self, summary):
        """Total Z2 transport entries = 240 * 10 = 2400."""
        assert summary["T6_z2_total"] == 2400

    def test_z3_correct(self, summary):
        """Z3 total matches expected 2400."""
        assert summary["T6_z3_correct"] is True

    def test_z2_correct(self, summary):
        """Z2 total matches expected 2400."""
        assert summary["T6_z2_correct"] is True

    def test_pure_noflip_gens(self, summary):
        """Exactly 4 generators are purely non-flipping (Z2=0 for all edges)."""
        assert summary["T6_pure_noflip_gens"] == 4

    def test_z3_expected(self, summary):
        """Z3 expected = 10 * 240 = 2400."""
        assert summary["T6_z3_total_expected"] == 2400

    def test_z2_expected(self, summary):
        """Z2 expected = 10 * 240 = 2400."""
        assert summary["T6_z2_total_expected"] == 2400


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_e6_antipode_pairs.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_e6_antipode_pairs.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_num_pairs", "T1_pairs_antipodal", "T1_correct",
            "T2_num_edges", "T2_all_degrees_20", "T2_srg_correct",
            "T3_num_triangles", "T3_partition_correct",
            "T4_num_lines", "T4_coverage_complete", "T4_correct",
            "T5_num_gens", "T5_transitive", "T5_gen_orders",
            "T6_z3_total", "T6_z2_total", "T6_z3_correct", "T6_z2_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
