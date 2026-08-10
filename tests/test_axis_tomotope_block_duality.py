"""Tests for Pillar 105 (Part CCV): Tomotope-Axis Complementary Block Duality."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCV_AXIS_TOMOTOPE_BLOCK_DUALITY import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Common skeleton
# ---------------------------------------------------------------------------

class TestT1CommonSkeleton:
    """T1: 48 <r0,r3>-blocks of size 4 are common to both models."""

    def test_num_blocks(self, summary):
        """Exactly 48 blocks."""
        assert summary["T1_num_blocks"] == 48

    def test_all_size_4(self, summary):
        """Every block has exactly 4 flags."""
        assert summary["T1_all_size_4"] is True

    def test_block_size_dist(self, summary):
        """Block size distribution is {4: 48}."""
        assert summary["T1_block_size_dist"] == {4: 48}

    def test_incidence_pairs_unique(self, summary):
        """Each block corresponds to a unique (tomotope-edge, tomotope-face) pair."""
        assert summary["T1_all_incidence_pairs_unique"] is True


# ---------------------------------------------------------------------------
# T2: Complementary duality
# ---------------------------------------------------------------------------

class TestT2ComplementaryDuality:
    """T2: (12,4,16,3) <-> (16,3,12,4) complementary partition numbers."""

    def test_complementary_duality_flag(self, summary):
        """Complementary duality flag is True."""
        assert summary["T2_complementary_duality"] is True

    def test_tomotope_fvec(self, summary):
        """Tomotope f-vector: V=4, E=12, F=16, C=8."""
        fv = summary["T2_tomotope_fvec"]
        assert fv["V"] == 4
        assert fv["E"] == 12
        assert fv["F"] == 16
        assert fv["C"] == 8

    def test_axis_fvec(self, summary):
        """Axis f-vector: V=1, E=16, F=12, C=4."""
        fv = summary["T2_axis_fvec"]
        assert fv["V"] == 1
        assert fv["E"] == 16
        assert fv["F"] == 12
        assert fv["C"] == 4

    def test_tomo_edges_times_blocks(self, summary):
        """12 tomotope edges x 4 blocks = 48."""
        assert summary["T2_tomo_edges_times_blocks"] == 48

    def test_tomo_faces_times_blocks(self, summary):
        """16 tomotope faces x 3 blocks = 48."""
        assert summary["T2_tomo_faces_times_blocks"] == 48

    def test_axis_edges_times_blocks(self, summary):
        """16 axis edges x 3 blocks = 48."""
        assert summary["T2_axis_edges_times_blocks"] == 48

    def test_axis_faces_times_blocks(self, summary):
        """12 axis faces x 4 blocks = 48."""
        assert summary["T2_axis_faces_times_blocks"] == 48

    def test_all_products_equal_48(self, summary):
        """All four products (n_features x blocks_per_feature) equal 48."""
        assert summary["T2_tomo_edges_times_blocks"] == 48
        assert summary["T2_tomo_faces_times_blocks"] == 48
        assert summary["T2_axis_edges_times_blocks"] == 48
        assert summary["T2_axis_faces_times_blocks"] == 48

    def test_edge_block_sizes_swap(self, summary):
        """Tomotope edges have 4 blocks each, axis edges have 3 — these swap."""
        t3 = summary["T3_tomotope_edge_partition"]
        t5 = summary["T5_axis_edge_partition"]
        assert t3["expected_size"] == 4
        assert t5["expected_size"] == 3
        assert t3["expected_size"] != t5["expected_size"]

    def test_face_block_sizes_swap(self, summary):
        """Tomotope faces have 3 blocks each, axis faces have 4 — these swap."""
        t4 = summary["T4_tomotope_face_partition"]
        t6 = summary["T6_axis_face_partition"]
        assert t4["expected_size"] == 3
        assert t6["expected_size"] == 4
        assert t4["expected_size"] != t6["expected_size"]


# ---------------------------------------------------------------------------
# T3: Tomotope-edge partition
# ---------------------------------------------------------------------------

class TestT3TomotopEdgePartition:
    """T3: 12 tomotope edges x 4 blocks each = exact partition."""

    def test_n_tomotope_edges(self, summary):
        """12 tomotope edges."""
        assert summary["T3_tomotope_edge_partition"]["n_parts"] == 12

    def test_exact_4_blocks_per_tomotope_edge(self, summary):
        """Each tomotope edge contains exactly 4 blocks."""
        assert summary["T3_tomotope_edge_partition"]["exact_size"] is True

    def test_tomotope_edge_partition_covers_all(self, summary):
        """Tomotope-edge partition covers all 48 blocks."""
        assert summary["T3_tomotope_edge_partition"]["covers_all_48"] is True

    def test_tomotope_edge_partition_disjoint(self, summary):
        """Tomotope-edge partition is disjoint."""
        assert summary["T3_tomotope_edge_partition"]["disjoint"] is True


# ---------------------------------------------------------------------------
# T4: Tomotope-face partition
# ---------------------------------------------------------------------------

class TestT4TomotopFacePartition:
    """T4: 16 tomotope faces x 3 blocks each = exact partition."""

    def test_n_tomotope_faces(self, summary):
        """16 tomotope faces."""
        assert summary["T4_tomotope_face_partition"]["n_parts"] == 16

    def test_exact_3_blocks_per_tomotope_face(self, summary):
        """Each tomotope face contains exactly 3 blocks."""
        assert summary["T4_tomotope_face_partition"]["exact_size"] is True

    def test_tomotope_face_partition_covers_all(self, summary):
        """Tomotope-face partition covers all 48 blocks."""
        assert summary["T4_tomotope_face_partition"]["covers_all_48"] is True

    def test_tomotope_face_partition_disjoint(self, summary):
        """Tomotope-face partition is disjoint."""
        assert summary["T4_tomotope_face_partition"]["disjoint"] is True


# ---------------------------------------------------------------------------
# T5: Axis-edge partition
# ---------------------------------------------------------------------------

class TestT5AxisEdgePartition:
    """T5: 16 axis edges x 3 blocks each = exact partition."""

    def test_n_axis_edges(self, summary):
        """16 axis edges."""
        assert summary["T5_axis_edge_partition"]["n_parts"] == 16

    def test_exact_3_blocks_per_axis_edge(self, summary):
        """Each axis edge contains exactly 3 blocks."""
        assert summary["T5_axis_edge_partition"]["exact_size"] is True

    def test_axis_edge_partition_covers_all(self, summary):
        """Axis-edge partition covers all 48 blocks."""
        assert summary["T5_axis_edge_partition"]["covers_all_48"] is True

    def test_axis_edge_partition_disjoint(self, summary):
        """Axis-edge partition is disjoint."""
        assert summary["T5_axis_edge_partition"]["disjoint"] is True


# ---------------------------------------------------------------------------
# T6: Axis-face partition
# ---------------------------------------------------------------------------

class TestT6AxisFacePartition:
    """T6: 12 axis faces x 4 blocks each = exact partition."""

    def test_n_axis_faces(self, summary):
        """12 axis faces."""
        assert summary["T6_axis_face_partition"]["n_parts"] == 12

    def test_exact_4_blocks_per_axis_face(self, summary):
        """Each axis face contains exactly 4 blocks."""
        assert summary["T6_axis_face_partition"]["exact_size"] is True

    def test_axis_face_partition_covers_all(self, summary):
        """Axis-face partition covers all 48 blocks."""
        assert summary["T6_axis_face_partition"]["covers_all_48"] is True

    def test_axis_face_partition_disjoint(self, summary):
        """Axis-face partition is disjoint."""
        assert summary["T6_axis_face_partition"]["disjoint"] is True


# ---------------------------------------------------------------------------
# Cross-checks
# ---------------------------------------------------------------------------

class TestCrossChecks:
    """Cross-checks: each block has a unique tomotope-edge and tomotope-face owner."""

    def test_unique_tomotope_edge_membership(self, summary):
        """Each block appears in exactly one tomotope edge."""
        assert summary["cross_check_te_membership_unique"] is True

    def test_unique_tomotope_face_membership(self, summary):
        """Each block appears in exactly one tomotope face."""
        assert summary["cross_check_tf_membership_unique"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_axis_tomotope_block_duality.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_axis_tomotope_block_duality.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_num_blocks", "T1_block_size_dist", "T1_all_size_4",
            "T2_complementary_duality", "T2_tomotope_fvec", "T2_axis_fvec",
            "T3_tomotope_edge_partition", "T4_tomotope_face_partition",
            "T5_axis_edge_partition", "T6_axis_face_partition",
            "cross_check_te_membership_unique", "cross_check_tf_membership_unique",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
