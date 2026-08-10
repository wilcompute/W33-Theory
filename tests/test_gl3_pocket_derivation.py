"""Tests for Pillar 118 (Part CCXVIII): W33 7-Pocket Derivation Algebra is gl3."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXVIII_GL3_POCKET_DERIVATION import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Triangle product structure
# ---------------------------------------------------------------------------

class TestT1TriangleProductStructure:
    """T1: 36 vertices, 120 blocks, 720 defined ordered products."""

    def test_36_vertices(self, summary):
        """SRG has 36 vertices."""
        assert summary["T1_n_vertices"] == 36

    def test_120_blocks(self, summary):
        """120 oriented triangle blocks."""
        assert summary["T1_n_blocks"] == 120

    def test_720_products(self, summary):
        """720 defined ordered products (6 per block)."""
        assert summary["T1_defined_products"] == 720

    def test_120_times_6_equals_720(self, summary):
        """120 * 6 = 720."""
        assert summary["T1_products_from_blocks"] == 720

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True


# ---------------------------------------------------------------------------
# T2: 540 pockets from product closure
# ---------------------------------------------------------------------------

class TestT2PocketClosure:
    """T2: 540 pockets; 6 active + 1 silent = 7; orbit size 540, stab 96."""

    def test_540_pockets(self, summary):
        """Exactly 540 pockets from product closure."""
        assert summary["T2_n_pockets"] == 540

    def test_6_active_per_pocket(self, summary):
        """6 active elements per pocket."""
        assert summary["T2_active"] == 6

    def test_1_silent_per_pocket(self, summary):
        """1 silent element per pocket."""
        assert summary["T2_silent"] == 1

    def test_4_interior_triangles(self, summary):
        """4 interior triangle blocks per pocket."""
        assert summary["T2_n_interior"] == 4

    def test_orbit_transitive(self, summary):
        """540 pockets form a single transitive orbit under PSp(4,3)."""
        assert summary["T2_orbit_transitive"] is True

    def test_orbit_size_540(self, summary):
        """Orbit size = 540."""
        assert summary["T2_orbit_size"] == 540

    def test_stabilizer_96(self, summary):
        """Stabilizer order = 96."""
        assert summary["T2_stabilizer"] == 96

    def test_6_plus_1_equals_7(self, summary):
        """6 active + 1 silent = 7."""
        assert summary["T2_active"] + summary["T2_silent"] == 7

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True


# ---------------------------------------------------------------------------
# T3: Derivation algebra is gl3 (dim 9)
# ---------------------------------------------------------------------------

class TestT3DerivationAlgebra:
    """T3: Der(pocket) has dim 9 = sl3(8) + center(1) = gl3."""

    def test_dim_9(self, summary):
        """Der(pocket) has dimension 9."""
        assert summary["T3_der_dim"] == 9

    def test_9_matrices(self, summary):
        """9 linearly independent derivation matrices."""
        assert summary["T3_n_matrices"] == 9

    def test_center_dim_1(self, summary):
        """Center of Der(pocket) has dimension 1."""
        assert summary["T3_center_dim"] == 1

    def test_semisimple_dim_8(self, summary):
        """Semisimple part has dimension 8."""
        assert summary["T3_semisimple_dim"] == 8

    def test_center_plus_semisimple_equals_9(self, summary):
        """1 + 8 = 9."""
        assert summary["T3_center_dim"] + summary["T3_semisimple_dim"] == 9

    def test_field_Q(self, summary):
        """Computation over Q."""
        assert summary["T3_der_field"] == "Q"

    def test_center_index_8(self, summary):
        """Center basis vector has index 8."""
        assert summary["T3_center_index"] == 8

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True


# ---------------------------------------------------------------------------
# T4: Semisimple part is sl3
# ---------------------------------------------------------------------------

class TestT4SemisimplePartSl3:
    """T4: Semisimple part = sl3; 54 nonzero bracket pairs; 8-dim vectors."""

    def test_54_brackets(self, summary):
        """54 nonzero structure constant brackets."""
        assert summary["T4_n_brackets"] == 54

    def test_bracket_dim_8(self, summary):
        """Each bracket value is an 8-dimensional vector."""
        assert summary["T4_bracket_dim"] == 8

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True


# ---------------------------------------------------------------------------
# T5: Killing form rank 8
# ---------------------------------------------------------------------------

class TestT5KillingForm:
    """T5: Killing form has rank 8 (nondegenerate); diagonal = -12."""

    def test_killing_rank_8(self, summary):
        """Killing form has rank exactly 8 (nondegenerate)."""
        assert summary["T5_killing_rank"] == 8

    def test_all_diag_minus12(self, summary):
        """All diagonal entries of Killing form equal -12."""
        assert summary["T5_all_diag_minus12"] is True

    def test_8_diagonal_entries(self, summary):
        """Killing form has 8 diagonal entries."""
        assert len(summary["T5_killing_diag"]) == 8

    def test_exactly_2_offdiag_nonzero(self, summary):
        """Only 2 off-diagonal entries are nonzero (at (0,3) and (3,0))."""
        assert len(summary["T5_offdiag_nonzero"]) == 2

    def test_offdiag_at_0_3(self, summary):
        """Off-diagonal nonzero at positions (0,3) and (3,0)."""
        positions = {(e[0], e[1]) for e in summary["T5_offdiag_nonzero"]}
        assert positions == {(0, 3), (3, 0)}

    def test_offdiag_value_minus6(self, summary):
        """Off-diagonal nonzero values are -6."""
        values = {e[2] for e in summary["T5_offdiag_nonzero"]}
        assert values == {-6}

    def test_t5_correct(self, summary):
        """T5 overall correctness flag."""
        assert summary["T5_correct"] is True


# ---------------------------------------------------------------------------
# T6: Module decomposition 1 + 3 + 3-bar
# ---------------------------------------------------------------------------

class TestT6ModuleDecomposition:
    """T6: 7-pocket = 1 (silent) + 3 + 3-bar (active) under sl3."""

    def test_pocket_size_7(self, summary):
        """Pocket basis has 7 elements."""
        assert summary["T6_pocket_size"] == 7

    def test_silent_in_basis(self, summary):
        """Silent element (vertex 27) is in the pocket basis."""
        assert summary["T6_silent_in_basis"] is True

    def test_6_active_elements(self, summary):
        """6 active elements (3 + 3-bar under sl3)."""
        assert summary["T6_active_count"] == 6

    def test_1_silent_element(self, summary):
        """1 silent element."""
        assert summary["T6_silent_count"] == 1

    def test_total_7(self, summary):
        """6 active + 1 silent = 7 total."""
        assert summary["T6_total"] == 7

    def test_gl3_dim_9(self, summary):
        """gl3 = Der(pocket) has dimension 9."""
        assert summary["T6_gl3_dim"] == 9

    def test_sl3_dim_8(self, summary):
        """sl3 semisimple part has dimension 8."""
        assert summary["T6_sl3_dim"] == 8

    def test_matches_g2_pattern(self, summary):
        """dim(sl3) + active = 8 + 6 = 14 = dim(G2)."""
        assert summary["T6_matches_g2_pattern"] is True

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_gl3_pocket_derivation.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_gl3_pocket_derivation.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_n_vertices", "T1_n_blocks", "T1_defined_products", "T1_correct",
            "T2_n_pockets", "T2_active", "T2_silent", "T2_stabilizer", "T2_correct",
            "T3_der_dim", "T3_center_dim", "T3_semisimple_dim", "T3_correct",
            "T4_n_brackets", "T4_bracket_dim", "T4_correct",
            "T5_killing_rank", "T5_all_diag_minus12", "T5_correct",
            "T6_pocket_size", "T6_active_count", "T6_matches_g2_pattern", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
