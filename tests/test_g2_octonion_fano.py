"""Tests for Pillar 116 (Part CCXVI): G2 Derivation Algebra and Octonion Fano Structure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXVI_G2_OCTONION_FANO import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: G2 derivation algebra
# ---------------------------------------------------------------------------

class TestT1G2DerivationAlgebra:
    """T1: dim(Der(O)) = 14 via linear constraints over GF(p); rank 50 of 64-var system."""

    def test_g2_dim_14(self, summary):
        """G2 has dimension 14."""
        assert summary["T1_deriv_dim"] == 14

    def test_64_variables(self, summary):
        """64 variables (8x8 derivation matrix)."""
        assert summary["T1_nvars"] == 64

    def test_512_equations(self, summary):
        """512 = 8^3 product constraint equations."""
        assert summary["T1_neq"] == 512

    def test_rank_50(self, summary):
        """Constraint system has rank 50."""
        assert summary["T1_rank"] == 50

    def test_nullity_14(self, summary):
        """Nullity = 64 - 50 = 14 = dim(G2)."""
        assert summary["T1_nullity"] == 14

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True

    def test_64_minus_50_equals_14(self, summary):
        """64 - 50 = 14."""
        assert summary["T1_nvars"] - summary["T1_rank"] == 14


# ---------------------------------------------------------------------------
# T2: sl3 subalgebra
# ---------------------------------------------------------------------------

class TestT2sl3Subalgebra:
    """T2: Fixing axis e7 gives sl3 of dim 8; rank 56 of 520-eq system."""

    def test_sl3_dim_8(self, summary):
        """sl3 subalgebra has dimension 8."""
        assert summary["T2_deriv_dim"] == 8

    def test_rank_56(self, summary):
        """Fixed-axis constraint system has rank 56."""
        assert summary["T2_rank"] == 56

    def test_nullity_8(self, summary):
        """Nullity = 64 - 56 = 8 = dim(sl3)."""
        assert summary["T2_nullity"] == 8

    def test_more_equations_than_full(self, summary):
        """Fixed-axis system has more equations than full system."""
        assert summary["T2_neq"] > summary["T1_neq"]

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True

    def test_64_minus_56_equals_8(self, summary):
        """64 - 56 = 8."""
        assert summary["T2_nvars"] - summary["T2_rank"] == 8


# ---------------------------------------------------------------------------
# T3: Fano plane
# ---------------------------------------------------------------------------

class TestT3FanoPlane:
    """T3: 7 Fano triples, each point in exactly 3 triples; Aut = PSL(2,7) order 168."""

    def test_7_triples(self, summary):
        """7 oriented triples of the Fano plane."""
        assert summary["T3_n_triples"] == 7

    def test_all_valid_triples(self, summary):
        """All triples have 3 distinct elements in {1,...,7}."""
        assert summary["T3_all_valid"] is True

    def test_all_7_points_used(self, summary):
        """All 7 Fano points appear in some triple."""
        assert summary["T3_all_7_points"] is True

    def test_each_point_in_3_triples(self, summary):
        """Each Fano point appears in exactly 3 triples (Fano regularity)."""
        assert summary["T3_each_pt_in_3"] is True

    def test_psl27_order_168(self, summary):
        """|PSL(2,7)| = |Aut(Fano)| = 168."""
        assert summary["T3_psl27_order"] == 168

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True


# ---------------------------------------------------------------------------
# T4: 480 octonion tables
# ---------------------------------------------------------------------------

class TestT4OctonionTables:
    """T4: 480 distinct octonion tables; stabilizer 1344 = 168*8; orbit-stabilizer."""

    def test_orbit_size_480(self, summary):
        """Orbit of distinct octonion tables has size 480."""
        assert summary["T4_orbit_size"] == 480

    def test_group_order_645120(self, summary):
        """Signed-permutation group has order 645120."""
        assert summary["T4_group_order"] == 645120

    def test_stabilizer_1344(self, summary):
        """Stabilizer of one table has order 1344."""
        assert summary["T4_stabilizer"] == 1344

    def test_orbit_times_stabilizer(self, summary):
        """480 * 1344 = 645120 (orbit-stabilizer theorem)."""
        assert summary["T4_orbit_stabilizer"] == 480

    def test_stabilizer_factored_168_times_8(self, summary):
        """1344 = 168 * 8 = |PSL(2,7)| * 8."""
        assert summary["T4_stabilizer_factored"] is True

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True

    def test_480_times_1344_equals_645120(self, summary):
        """480 * 1344 = 645120."""
        assert summary["T4_orbit_size"] * summary["T4_stabilizer"] == summary["T4_group_order"]


# ---------------------------------------------------------------------------
# T5: 540 W33 pockets
# ---------------------------------------------------------------------------

class TestT5W33Pockets:
    """T5: 540 pockets in SRG(36,20,10,12); each vertex silent in exactly 15."""

    def test_540_pockets(self, summary):
        """Exactly 540 canonical 7-element pockets."""
        assert summary["T5_num_pockets"] == 540

    def test_36_vertices(self, summary):
        """36 SRG vertices."""
        assert summary["T5_n_vertices"] == 36

    def test_all_15_pockets_per_vertex(self, summary):
        """Every vertex is silent in exactly 15 pockets."""
        assert summary["T5_all_15_per_vertex"] is True

    def test_36_times_15_equals_540(self, summary):
        """36 * 15 = 540."""
        assert summary["T5_total_check"] == 540

    def test_t5_correct(self, summary):
        """T5 overall correctness flag."""
        assert summary["T5_correct"] is True


# ---------------------------------------------------------------------------
# T6: G2 -> sl3 module decomposition
# ---------------------------------------------------------------------------

class TestT6ModuleDecomposition:
    """T6: Im(O) = 1 + 3 + 3bar under sl3; dim(G2) = dim(sl3) + 6."""

    def test_module_dim_7(self, summary):
        """Imaginary octonion module Im(O) has dimension 7."""
        assert summary["T6_module_dim"] == 7

    def test_1_silent_plus_6_active(self, summary):
        """Module splits as 1 (silent/axis) + 6 (active = 3+3bar)."""
        assert summary["T6_module_check"] is True

    def test_silent_part_is_1(self, summary):
        """Silent part has dimension 1."""
        assert summary["T6_silent_part"] == 1

    def test_active_part_is_6(self, summary):
        """Active part (3+3bar) has dimension 6."""
        assert summary["T6_active_part"] == 6

    def test_g2_equals_sl3_plus_6(self, summary):
        """dim(G2) = 14 = dim(sl3) + 6 = 8 + 6."""
        assert summary["T6_g2_from_sl3"] is True

    def test_15_pockets_per_vertex(self, summary):
        """540 / 36 = 15 pockets per vertex."""
        assert summary["T6_pockets_per_vertex"] == 15

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_g2_octonion_fano.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_g2_octonion_fano.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_deriv_dim", "T1_rank", "T1_nullity", "T1_correct",
            "T2_deriv_dim", "T2_rank", "T2_correct",
            "T3_n_triples", "T3_each_pt_in_3", "T3_correct",
            "T4_orbit_size", "T4_stabilizer", "T4_correct",
            "T5_num_pockets", "T5_all_15_per_vertex", "T5_correct",
            "T6_module_dim", "T6_g2_from_sl3", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
