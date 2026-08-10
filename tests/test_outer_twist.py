"""Tests for Pillar 108 (Part CCVIII): Outer Twist on E8 Roots and PG(3,3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCVIII_OUTER_TWIST import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Outer twist order 8
# ---------------------------------------------------------------------------

class TestT1OuterTwistOrder:
    """T1: N4 induces a permutation of order 8; N4 is NOT symplectic."""

    def test_order_p_is_8(self, summary):
        """Outer permutation p has order 8."""
        assert summary["T1_order_p"] == 8

    def test_computed_order_matches(self, summary):
        """Independently computed order matches summary value."""
        assert summary["T1_order_p_matches"] is True

    def test_not_symplectic(self, summary):
        """N4 is NOT symplectic: Omega' ≠ Omega."""
        assert summary["T1_not_symplectic"] is True

    def test_twisted_form_computed_correctly(self, summary):
        """Twisted form Omega' = N4^T Omega N4 verified."""
        assert summary["T1_twisted_form_correct"] is True


# ---------------------------------------------------------------------------
# T2: Inner residual order 6
# ---------------------------------------------------------------------------

class TestT2InnerResidual:
    """T2: Inner residual a = Q * N4^{-1} has order 6; Q is symplectic w.r.t. Omega'."""

    def test_order_a_is_6(self, summary):
        """Inner residual a has order 6."""
        assert summary["T2_order_a"] == 6

    def test_Q_isomorphism_correct(self, summary):
        """Q^T Omega Q = Omega' verified."""
        assert summary["T2_Q_isomorphism_correct"] is True

    def test_order_a_divides_order_p_lcm(self, summary):
        """Orders 8 (p) and 6 (a) are distinct, showing non-trivial structure."""
        assert summary["T1_order_p"] != summary["T2_order_a"]


# ---------------------------------------------------------------------------
# T3: Vertex cycle structure
# ---------------------------------------------------------------------------

class TestT3VertexCycleStructure:
    """T3: a acts on 40 PG(3,3) points with cycle structure {1:2, 2:1, 3:2, 6:5}."""

    def test_cycle_struct_correct(self, summary):
        """Cycle structure correctness flag is True."""
        assert summary["T3_correct"] is True

    def test_total_pts_40(self, summary):
        """Cycle structure accounts for all 40 PG(3,3) points."""
        assert summary["T3_total_pts"] == 40

    def test_two_fixed_points(self, summary):
        """Exactly 2 fixed points."""
        assert summary["T3_fixed_count"] == 2

    def test_six_cycles(self, summary):
        """5 six-cycles (30 points)."""
        assert summary["T3_vertex_cycle_struct"].get(6) == 5

    def test_three_cycles(self, summary):
        """2 three-cycles (6 points)."""
        assert summary["T3_vertex_cycle_struct"].get(3) == 2

    def test_one_transposition(self, summary):
        """1 transposition (2-cycle)."""
        assert summary["T3_vertex_cycle_struct"].get(2) == 1

    def test_fixed_vertex_count_matches(self, summary):
        """2 fixed vertices identified."""
        assert len(summary["T3_fixed_vertices"]) == 2

    def test_one_two_cycle_pair(self, summary):
        """1 two-cycle pair identified."""
        assert len(summary["T3_two_cycle_vertices"]) == 1

    def test_cycle_total_check(self, summary):
        """2+2+6+30 = 42 -- wait, 2*1+1*2+2*3+5*6 = 2+2+6+30 = 40."""
        cs = summary["T3_vertex_cycle_struct"]
        total = sum(length * count for length, count in cs.items())
        assert total == 40


# ---------------------------------------------------------------------------
# T4: E8 root cycle structure
# ---------------------------------------------------------------------------

class TestT4RootCycleStructure:
    """T4: a acts on 240 E8 roots with cycle structure {1:2, 2:2, 3:10, 6:34}."""

    def test_root_cycle_correct(self, summary):
        """Root cycle structure correctness flag is True."""
        assert summary["T4_correct"] is True

    def test_total_roots_240(self, summary):
        """Cycle structure accounts for all 240 E8 roots."""
        assert summary["T4_total_roots"] == 240

    def test_two_fixed_roots(self, summary):
        """Exactly 2 fixed roots."""
        assert summary["T4_fixed_root_count"] == 2

    def test_34_six_cycles(self, summary):
        """34 six-cycles (204 roots)."""
        assert summary["T4_root_cycle_struct"].get(6) == 34

    def test_10_three_cycles(self, summary):
        """10 three-cycles (30 roots)."""
        assert summary["T4_root_cycle_struct"].get(3) == 10

    def test_2_transpositions(self, summary):
        """2 transpositions (4 roots)."""
        assert summary["T4_root_cycle_struct"].get(2) == 2

    def test_fixed_root_vectors_present(self, summary):
        """2 fixed root vectors identified."""
        assert len(summary["T4_fixed_root_vectors"]) == 2

    def test_root_total_check(self, summary):
        """2+4+30+204 = 240."""
        cs = summary["T4_root_cycle_struct"]
        total = sum(length * count for length, count in cs.items())
        assert total == 240


# ---------------------------------------------------------------------------
# T5: Affine Heisenberg orbits
# ---------------------------------------------------------------------------

class TestT5AffineHeisenbergOrbits:
    """T5: Outer twist on AG(3,3) = 27 affine points gives 5 orbits {1:1,2:1,8:3}."""

    def test_five_affine_orbits(self, summary):
        """Exactly 5 affine orbits."""
        assert summary["T5_num_affine_orbits"] == 5

    def test_total_affine_27(self, summary):
        """Total affine points = 27."""
        assert summary["T5_total_affine_pts"] == 27

    def test_affine_orbit_size_dist(self, summary):
        """Orbit size distribution is {1:1, 2:1, 8:3}."""
        assert summary["T5_affine_orbit_size_dist"] == {1: 1, 2: 1, 8: 3}

    def test_affine_correct(self, summary):
        """Affine orbit correctness flag is True."""
        assert summary["T5_correct"] is True

    def test_three_orbits_of_8(self, summary):
        """3 large orbits of size 8 (covering 24 of 27 affine points)."""
        assert summary["T5_affine_orbit_size_dist"][8] == 3

    def test_one_fixed_affine_point(self, summary):
        """1 fixed affine point (orbit of size 1)."""
        assert summary["T5_affine_orbit_size_dist"][1] == 1


# ---------------------------------------------------------------------------
# T6: Edge orbit structure
# ---------------------------------------------------------------------------

class TestT6EdgeOrbits:
    """T6: Outer twist has 34 orbits on 240 W(3,3) collinearity edges."""

    def test_34_edge_orbits(self, summary):
        """Exactly 34 edge orbits."""
        assert summary["T6_num_edge_orbits"] == 34

    def test_total_edges_240(self, summary):
        """Total edges = 240 = |SRG(40,12)| edges."""
        assert summary["T6_total_edges"] == 240

    def test_edge_size_dist(self, summary):
        """All edge orbits have size 4 or 8: {4:8, 8:26}."""
        assert summary["T6_edge_size_dist"] == {4: 8, 8: 26}

    def test_edge_correct(self, summary):
        """Edge orbit correctness flag is True."""
        assert summary["T6_correct"] is True

    def test_8_size_4_orbits(self, summary):
        """8 orbits of size 4 covering 32 edges."""
        assert summary["T6_edge_size_dist"][4] == 8

    def test_26_size_8_orbits(self, summary):
        """26 orbits of size 8 covering 208 edges."""
        assert summary["T6_edge_size_dist"][8] == 26

    def test_edge_total_check(self, summary):
        """8*4 + 26*8 = 32 + 208 = 240."""
        dist = summary["T6_edge_size_dist"]
        total = sum(size * count for size, count in dist.items())
        assert total == 240


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_outer_twist.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_outer_twist.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_order_p", "T1_not_symplectic", "T1_twisted_form_correct",
            "T2_order_a", "T2_Q_isomorphism_correct",
            "T3_vertex_cycle_struct", "T3_total_pts", "T3_correct",
            "T4_root_cycle_struct", "T4_total_roots", "T4_correct",
            "T5_num_affine_orbits", "T5_affine_orbit_size_dist", "T5_correct",
            "T6_num_edge_orbits", "T6_edge_size_dist", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
