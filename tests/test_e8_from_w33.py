"""Tests for Pillar 107 (Part CCVII): E8 Root System from W(3,3) GF(2) Homology."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCVII_E8_FROM_W33 import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: GF(2) homology space
# ---------------------------------------------------------------------------

class TestT1GF2Homology:
    """T1: H = ker(A)/im(A) has dimension 8, giving 256 elements."""

    def test_dimension_8(self, summary):
        """H has dimension 8 over GF(2)."""
        assert summary["T1_dim_H"] == 8

    def test_size_256(self, summary):
        """H has 2^8 = 256 elements."""
        assert summary["T1_size_H"] == 256

    def test_from_w33_adjacency(self, summary):
        """H is derived from the W33 adjacency matrix."""
        assert summary["T1_H_from_W33_adjacency"] is True

    def test_256_equals_2_to_8(self, summary):
        """256 = 2^dim(H)."""
        assert summary["T1_size_H"] == 2 ** summary["T1_dim_H"]


# ---------------------------------------------------------------------------
# T2: Quadratic form orbits
# ---------------------------------------------------------------------------

class TestT2QuadraticFormOrbits:
    """T2: q partitions H into {0} (1), singular nonzero (135), nonsingular (120)."""

    def test_zero_orbit_size_1(self, summary):
        """The zero orbit has exactly 1 element."""
        assert summary["T2_orbit_zero_size"] == 1

    def test_singular_orbit_size_135(self, summary):
        """The singular nonzero orbit has 135 elements."""
        assert summary["T2_orbit_singular_size"] == 135

    def test_nonsingular_orbit_size_120(self, summary):
        """The nonsingular orbit has 120 elements."""
        assert summary["T2_orbit_nonsingular_size"] == 120

    def test_total_256(self, summary):
        """1 + 135 + 120 = 256."""
        assert summary["T2_total_256"] == 256

    def test_partition_correct(self, summary):
        """Partition correctness flag is True."""
        assert summary["T2_partition_correct"] is True

    def test_parts_sum_to_total(self, summary):
        """Parts sum to |H|."""
        total = (summary["T2_orbit_zero_size"]
                 + summary["T2_orbit_singular_size"]
                 + summary["T2_orbit_nonsingular_size"])
        assert total == summary["T1_size_H"]


# ---------------------------------------------------------------------------
# T3: E8 Dynkin embedding
# ---------------------------------------------------------------------------

class TestT3E8DynkinEmbedding:
    """T3: 8 simple roots in SRG(120,56,28,24) form the E8 Dynkin diagram."""

    def test_is_E8_dynkin(self, summary):
        """E8 Dynkin embedding flag is True."""
        assert summary["T3_is_E8_Dynkin"] is True

    def test_num_dynkin_edges(self, summary):
        """E8 Dynkin diagram has exactly 7 edges."""
        assert summary["T3_num_dynkin_edges"] == 7

    def test_branching_node_is_2(self, summary):
        """Branching node (degree 3) is node 2."""
        assert summary["T3_branching_node"] == 2

    def test_branching_node_degree_3(self, summary):
        """Branching node has degree 3."""
        assert summary["T3_branch_node_degree"] == 3

    def test_dynkin_edges_contain_branch(self, summary):
        """Branch edge (2,7) is in the Dynkin edge list."""
        edges = summary["T3_dynkin_edges"]
        assert [2, 7] in edges or (2, 7) in edges

    def test_simple_root_H_ints(self, summary):
        """Simple root H-integers are [4,64,1,2,23,102,31,177]."""
        assert summary["T3_simple_root_H_ints"] == [4, 64, 1, 2, 23, 102, 31, 177]

    def test_8_simple_roots(self, summary):
        """Exactly 8 simple roots."""
        assert len(summary["T3_simple_root_H_ints"]) == 8

    def test_all_simple_roots_nonsingular(self, summary):
        """All 8 simple roots are nonsingular (q=1)."""
        assert summary["T3_all_simple_roots_nonsingular"] is True

    def test_srg_vertex_ids_present(self, summary):
        """SRG vertex IDs are provided for all 8 nodes."""
        assert len(summary["T3_srg_vertex_ids"]) == 8


# ---------------------------------------------------------------------------
# T4: Coxeter relations
# ---------------------------------------------------------------------------

class TestT4CoxeterRelations:
    """T4: 8 GF(2) reflections satisfy E8 Coxeter relations."""

    def test_all_involutions(self, summary):
        """All 8 reflections have order 2."""
        assert summary["T4_all_involutions"] is True

    def test_s_orders_all_2(self, summary):
        """Each reflection order is exactly 2."""
        assert summary["T4_s_orders"] == [2, 2, 2, 2, 2, 2, 2, 2]

    def test_all_coxeter_correct(self, summary):
        """All 28 pair orders match precomputed Coxeter table."""
        assert summary["T4_all_coxeter_correct"] is True

    def test_adj_order_3(self, summary):
        """All adjacent pairs have ord(s_i*s_j) = 3."""
        assert summary["T4_all_adj_order_3"] is True

    def test_nonadj_order_2(self, summary):
        """All non-adjacent pairs have ord(s_i*s_j) = 2."""
        assert summary["T4_all_nonadj_order_2"] is True

    def test_adj_order_distribution(self, summary):
        """All 7 adjacent pairs give order 3."""
        assert summary["T4_adj_order_dist"] == {3: 7}

    def test_nonadj_order_distribution(self, summary):
        """All 21 non-adjacent pairs give order 2."""
        assert summary["T4_nonadj_order_dist"] == {2: 21}

    def test_28_pairs_checked(self, summary):
        """All C(8,2) = 28 pairs are checked."""
        assert summary["T4_num_pairs_checked"] == 28


# ---------------------------------------------------------------------------
# T5: Cartan matrix
# ---------------------------------------------------------------------------

class TestT5CartanMatrix:
    """T5: The 8x8 Cartan matrix is the standard E8 Cartan matrix."""

    def test_cartan_correct(self, summary):
        """Cartan matrix matches standard E8 Cartan matrix."""
        assert summary["T5_cartan_correct"] is True

    def test_bilinear_matches_dynkin(self, summary):
        """Bilinear form b(r_i,r_j)=1 iff i~j in Dynkin diagram."""
        assert summary["T5_bilinear_matches_dynkin"] is True


# ---------------------------------------------------------------------------
# T6: Spanning and orbit structure
# ---------------------------------------------------------------------------

class TestT6SpanningOrbits:
    """T6: Simple roots span H; reflections have 3 orbits matching quadratic form."""

    def test_spans_H(self, summary):
        """8 simple roots span all of H (rank 8)."""
        assert summary["T6_spans_H"] is True

    def test_span_dim_8(self, summary):
        """Spanning dimension is 8."""
        assert summary["T6_simple_roots_span_dim"] == 8

    def test_coxeter_satisfied(self, summary):
        """Coxeter relations satisfied flag from summary."""
        assert summary["T6_coxeter_satisfied"] is True

    def test_three_orbits(self, summary):
        """Reflection group has exactly 3 orbits on H."""
        assert summary["T6_three_orbits"] is True

    def test_orbit_sizes(self, summary):
        """Orbit sizes are [1, 135, 120]."""
        sizes = sorted(summary["T6_orbit_sizes"])
        assert sizes == [1, 120, 135]

    def test_orbit_sizes_sum_256(self, summary):
        """Orbit sizes sum to |H| = 256."""
        assert sum(summary["T6_orbit_sizes"]) == 256


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_e8_from_w33.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_e8_from_w33.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_dim_H", "T1_size_H",
            "T2_orbit_zero_size", "T2_orbit_singular_size",
            "T2_orbit_nonsingular_size", "T2_partition_correct",
            "T3_is_E8_Dynkin", "T3_num_dynkin_edges",
            "T3_simple_root_H_ints", "T3_all_simple_roots_nonsingular",
            "T4_all_involutions", "T4_all_coxeter_correct",
            "T4_adj_order_dist", "T4_nonadj_order_dist",
            "T5_cartan_correct", "T5_bilinear_matches_dynkin",
            "T6_spans_H", "T6_three_orbits", "T6_orbit_sizes",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
