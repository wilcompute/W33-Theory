"""
Regression tests for Part CCIV: Tropical Geometry Bridge (W(3,3)).

All constants are derived from the zero-parameter W(3,3) atoms:
  Q=3, V=40, K=12, LAM=2, MU=4, PHI3=13, EDGES=240.

Run:  pytest tests/test_tropical_geometry_bridge_cciv.py -v
"""

from __future__ import annotations

import sys
import math
from pathlib import Path

import pytest

# Make exploration/ importable regardless of invocation directory
_ROOT = Path(__file__).parent.parent
if str(_ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(_ROOT / "exploration"))

from PART_CCIV_TROPICAL_GEOMETRY_BRIDGE import (
    Q, V, K, LAM, MU, PHI3, PHI4, PHI6, EDGES,
    EIGENVALUES, LAPLACIAN_EIGENVALUES,
    TropicalGeometryBridge,
    build_tropical_geometry_bridge_summary,
    _verify_invariants,
)


# ──────────────────────────────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def bridge() -> TropicalGeometryBridge:
    return TropicalGeometryBridge()


@pytest.fixture(scope="module")
def summary() -> dict:
    return build_tropical_geometry_bridge_summary()


# ──────────────────────────────────────────────────────────────────────
# W(3,3) atom sanity
# ──────────────────────────────────────────────────────────────────────

class TestAtoms:
    def test_q(self):
        assert Q == 3

    def test_v(self):
        assert V == 40

    def test_k(self):
        assert K == 12

    def test_lam(self):
        assert LAM == 2

    def test_mu(self):
        assert MU == 4

    def test_phi3(self):
        assert PHI3 == 13

    def test_edges(self):
        assert EDGES == 240

    def test_eigenvalue_count(self):
        assert sum(m for _, m in EIGENVALUES) == V

    def test_eigenvalue_values(self):
        eigs = {lam for lam, _ in EIGENVALUES}
        assert eigs == {12, 2, -4}

    def test_laplacian_eigenvalue_sum(self):
        total = sum(mult for nu, mult in LAPLACIAN_EIGENVALUES)
        assert total == V

    def test_laplacian_nonzero_eigenvalues(self):
        nonzero = {nu for nu, _ in LAPLACIAN_EIGENVALUES if nu != 0}
        assert nonzero == {10, 16}  # K-2=10, K-(-4)=16

    def test_laplacian_zero_eigenvalue(self):
        zero_mults = [m for nu, m in LAPLACIAN_EIGENVALUES if nu == 0]
        assert zero_mults == [1]  # connected graph has exactly one 0


# ──────────────────────────────────────────────────────────────────────
# Tropical curve / graph invariants
# ──────────────────────────────────────────────────────────────────────

class TestTropicalCurve:
    def test_euler_characteristic(self, bridge):
        assert bridge.euler_characteristic == V - EDGES

    def test_euler_characteristic_value(self, bridge):
        assert bridge.euler_characteristic == -200

    def test_betti_1(self, bridge):
        assert bridge.betti_1 == EDGES - V + 1

    def test_betti_1_value(self, bridge):
        assert bridge.betti_1 == 201

    def test_tropical_genus_equals_betti_1(self, bridge):
        assert bridge.tropical_genus == bridge.betti_1

    def test_tropical_genus_value(self, bridge):
        assert bridge.tropical_genus == 201

    def test_euler_char_is_negative(self, bridge):
        assert bridge.euler_characteristic < 0

    def test_genus_positive(self, bridge):
        assert bridge.tropical_genus > 0


# ──────────────────────────────────────────────────────────────────────
# Tropical Grassmannian
# ──────────────────────────────────────────────────────────────────────

class TestTropicalGrassmannian:
    def test_grassmannian_dim(self, bridge):
        assert bridge.grassmannian_dim == Q * (V - Q)

    def test_grassmannian_dim_value(self, bridge):
        assert bridge.grassmannian_dim == 111

    def test_grassmannian_label(self, bridge):
        assert bridge.grassmannian_label == f"Gr_trop({Q},{V})"

    def test_grassmannian_label_content(self, bridge):
        assert "3" in bridge.grassmannian_label
        assert "40" in bridge.grassmannian_label

    def test_grassmannian_dim_formula(self, bridge):
        # Gr_trop(k,n) has dimension k(n-k)
        assert bridge.grassmannian_dim == Q * (V - Q)
        assert bridge.grassmannian_dim == 3 * 37


# ──────────────────────────────────────────────────────────────────────
# Tropical rank (perfect matching)
# ──────────────────────────────────────────────────────────────────────

class TestTropicalRank:
    def test_tropical_rank(self, bridge):
        assert bridge.tropical_rank == V // 2

    def test_tropical_rank_value(self, bridge):
        assert bridge.tropical_rank == 20

    def test_perfect_matching_exists(self):
        # SRG(40,12,2,4) has a perfect matching (V even, K>0, regular)
        assert V % 2 == 0

    def test_rank_is_half_vertices(self, bridge):
        assert 2 * bridge.tropical_rank == V


# ──────────────────────────────────────────────────────────────────────
# K-polygon lattice points = PHI3
# ──────────────────────────────────────────────────────────────────────

class TestKPolygonLattice:
    def test_lattice_points(self, bridge):
        assert bridge.k_polygon_lattice_pts == K + 1

    def test_lattice_points_equals_phi3(self, bridge):
        assert bridge.k_polygon_lattice_pts == PHI3

    def test_k_polygon_matches_phi3_flag(self, bridge):
        assert bridge.k_polygon_matches_phi3 is True

    def test_lattice_points_value(self, bridge):
        assert bridge.k_polygon_lattice_pts == 13


# ──────────────────────────────────────────────────────────────────────
# Tropical Satake parameters
# ──────────────────────────────────────────────────────────────────────

class TestTropicalSatake:
    def test_satake_eig_12(self, bridge):
        # floor(log_3(12)) = floor(2.261) = 2
        assert bridge.satake_tropical[12] == 2

    def test_satake_eig_2(self, bridge):
        # floor(log_3(2)) = floor(0.631) = 0
        assert bridge.satake_tropical[2] == 0

    def test_satake_eig_neg4(self, bridge):
        # floor(log_3(|-4|)) = floor(log_3(4)) = floor(1.261) = 1
        assert bridge.satake_tropical[-4] == 1

    def test_satake_values_distinct(self, bridge):
        vals = list(bridge.satake_tropical.values())
        assert len(set(vals)) == len(vals)  # all distinct: {0, 1, 2}

    def test_satake_range(self, bridge):
        for v in bridge.satake_tropical.values():
            assert 0 <= v <= 2

    def test_satake_uses_base_q(self):
        # The base is Q=3; check consistency
        assert int(math.log(12) / math.log(Q)) == 2
        assert int(math.log(2) / math.log(Q)) == 0
        assert int(math.log(4) / math.log(Q)) == 1


# ──────────────────────────────────────────────────────────────────────
# Spanning trees (tropical fan cone count)
# ──────────────────────────────────────────────────────────────────────

class TestSpanningTrees:
    def test_log_spanning_trees_positive(self, bridge):
        assert bridge.log_spanning_trees > 0

    def test_spanning_trees_log10_range(self, bridge):
        assert 39.0 < bridge.spanning_trees_log10 < 41.0

    def test_spanning_trees_log10_approx(self, bridge):
        # κ = (1/40)*10^27*16^12; log₁₀ ≈ 39.847
        assert abs(bridge.spanning_trees_log10 - 39.847) < 0.1

    def test_spanning_trees_formula(self, bridge):
        # Verify against manual calculation
        manual = (27 * math.log10(10) + 12 * math.log10(16)
                  - math.log10(40))
        assert abs(bridge.spanning_trees_log10 - manual) < 1e-6

    def test_spanning_trees_enormous(self, bridge):
        # The graph has fantastically many spanning trees
        assert bridge.spanning_trees_log10 > 35


# ──────────────────────────────────────────────────────────────────────
# Min-plus spectral radius
# ──────────────────────────────────────────────────────────────────────

class TestMinPlusSpectral:
    def test_minplus_spectral_radius(self, bridge):
        assert bridge.minplus_spectral_radius == K

    def test_minplus_spectral_radius_value(self, bridge):
        assert bridge.minplus_spectral_radius == 12

    def test_minplus_equals_degree(self, bridge):
        # For K-regular graph, tropical spectral radius = K
        assert bridge.minplus_spectral_radius == K


# ──────────────────────────────────────────────────────────────────────
# Dual tropical cell complex
# ──────────────────────────────────────────────────────────────────────

class TestDualCell:
    def test_dual_cell_dim(self, bridge):
        assert bridge.dual_cell_dim == K - 1

    def test_dual_cell_dim_value(self, bridge):
        assert bridge.dual_cell_dim == 11

    def test_dual_cell_formula(self, bridge):
        assert bridge.dual_cell_dim == K - 1


# ──────────────────────────────────────────────────────────────────────
# Tropical projective space
# ──────────────────────────────────────────────────────────────────────

class TestTropicalProjective:
    def test_tropical_proj_dim(self, bridge):
        assert bridge.tropical_proj_dim == V - 1

    def test_tropical_proj_dim_value(self, bridge):
        assert bridge.tropical_proj_dim == 39

    def test_tropical_lines_count(self, bridge):
        assert bridge.tropical_lines == PHI3

    def test_tropical_lines_value(self, bridge):
        assert bridge.tropical_lines == 13


# ──────────────────────────────────────────────────────────────────────
# Newton polytope
# ──────────────────────────────────────────────────────────────────────

class TestNewtonPolytope:
    def test_newton_degree(self, bridge):
        assert bridge.newton_degree == K

    def test_newton_degree_value(self, bridge):
        assert bridge.newton_degree == 12


# ──────────────────────────────────────────────────────────────────────
# Full summary / integration
# ──────────────────────────────────────────────────────────────────────

class TestFullSummary:
    def test_summary_verified(self, summary):
        assert summary["verified"] is True

    def test_summary_no_failures(self, summary):
        assert summary["failures"] == []

    def test_summary_all_keys_present(self, summary):
        required_keys = [
            "euler_characteristic", "betti_1", "tropical_genus",
            "grassmannian_label", "grassmannian_dim",
            "tropical_rank",
            "k_polygon_lattice_pts", "k_polygon_matches_phi3",
            "satake_tropical",
            "log_spanning_trees", "spanning_trees_log10",
            "minplus_spectral_radius",
            "dual_cell_dim",
            "tropical_proj_dim",
            "tropical_lines",
            "newton_degree",
            "verified", "failures", "w33_atoms",
        ]
        for key in required_keys:
            assert key in summary, f"Missing key: {key}"

    def test_summary_euler_char(self, summary):
        assert summary["euler_characteristic"] == -200

    def test_summary_betti_1(self, summary):
        assert summary["betti_1"] == 201

    def test_summary_grassmannian_dim(self, summary):
        assert summary["grassmannian_dim"] == 111

    def test_summary_tropical_rank(self, summary):
        assert summary["tropical_rank"] == 20

    def test_summary_k_polygon(self, summary):
        assert summary["k_polygon_lattice_pts"] == 13
        assert summary["k_polygon_matches_phi3"] is True

    def test_summary_satake_dict_keys(self, summary):
        keys = set(summary["satake_tropical"].keys())
        assert keys == {"12", "2", "-4"}

    def test_summary_spanning_trees_log10(self, summary):
        assert abs(summary["spanning_trees_log10"] - 39.847) < 0.1

    def test_summary_minplus_radius(self, summary):
        assert summary["minplus_spectral_radius"] == 12

    def test_summary_dual_cell_dim(self, summary):
        assert summary["dual_cell_dim"] == 11

    def test_summary_tropical_lines(self, summary):
        assert summary["tropical_lines"] == 13

    def test_summary_w33_atoms(self, summary):
        atoms = summary["w33_atoms"]
        assert atoms["Q"] == 3
        assert atoms["V"] == 40
        assert atoms["K"] == 12

    def test_verify_invariants_passes(self):
        b = TropicalGeometryBridge()
        failures = _verify_invariants(b)
        assert failures == []
