"""Regression tests for Part CCVI: Intersection Theory Bridge."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
if str(_ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(_ROOT / "exploration"))

from PART_CCVI_INTERSECTION_THEORY_BRIDGE import (
    Q, V, K, LAM, MU, PHI3, EDGES, MULT_K2,
    EIGENVALUES,
    IntersectionTheoryBridge,
    build_intersection_theory_bridge_summary,
    _verify_invariants,
)


@pytest.fixture(scope="module")
def bridge() -> IntersectionTheoryBridge:
    return IntersectionTheoryBridge()


@pytest.fixture(scope="module")
def summary() -> dict:
    return build_intersection_theory_bridge_summary()


class TestAtoms:
    def test_core_atoms(self):
        assert (Q, V, K, LAM, MU, PHI3, EDGES) == (3, 40, 12, 2, 4, 13, 240)

    def test_eigen_multiplicity_sum(self):
        assert sum(m for _, m in EIGENVALUES) == V


class TestIntersectionInvariants:
    def test_chow_ring_dim(self, bridge):
        assert bridge.chow_ring_dim == 40

    def test_self_intersection(self, bridge):
        assert bridge.self_intersection_K == K == 12

    def test_degree_map_image(self, bridge):
        assert bridge.degree_map_image == EDGES == 240

    def test_divisor_degree(self, bridge):
        assert bridge.divisor_class_degree == K

    def test_intersection_mult_lambda(self, bridge):
        assert bridge.intersection_mult_lam == LAM == 2

    def test_excess_intersection(self, bridge):
        assert bridge.excess_intersection == MU - LAM == 2

    def test_chern_chars(self, bridge):
        assert bridge.chern_char_0 == 1
        assert bridge.chern_char_1 == 12
        assert bridge.chern_char_2 == 70

    def test_todd_class(self, bridge):
        assert bridge.todd_1 == MULT_K2 == 6

    def test_riemann_roch(self, bridge):
        assert bridge.riemann_roch_chi == 20

    def test_projection_formula(self, bridge):
        assert bridge.projection_formula_value == LAM * EDGES == 480

    def test_blowup_excess(self, bridge):
        assert bridge.blowup_excess_class == -K == -12

    def test_generator_degrees(self, bridge):
        assert bridge.generator_degree_h == K
        assert bridge.generator_degree_c == LAM

    def test_pontryagin(self, bridge):
        assert bridge.pontryagin_p1 == -140


class TestSummary:
    def test_summary_verified(self, summary):
        assert summary["verified"] is True
        assert summary["failures"] == []

    def test_summary_keys(self, summary):
        keys = {
            "chow_ring_dim", "self_intersection_K", "degree_map_image",
            "divisor_class_degree", "intersection_mult_lam", "excess_intersection",
            "chern_char_0", "chern_char_1", "chern_char_2", "todd_1",
            "riemann_roch_chi", "projection_formula_value", "blowup_excess_class",
            "generator_degree_h", "generator_degree_c", "pontryagin_p1",
            "verified", "failures", "w33_atoms",
        }
        assert keys.issubset(summary.keys())

    def test_summary_values(self, summary):
        assert summary["chow_ring_dim"] == 40
        assert summary["degree_map_image"] == 240
        assert summary["todd_1"] == 6
        assert summary["projection_formula_value"] == 480


class TestVerifier:
    def test_verify_no_failures(self):
        b = IntersectionTheoryBridge()
        assert _verify_invariants(b) == []
