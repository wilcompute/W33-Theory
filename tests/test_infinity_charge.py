"""Tests for Pillar 114 (Part CCXIV): Infinity Neighbor Charge Table for AG(3,3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCXIV_INFINITY_CHARGE import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: PG(3,3) geometry
# ---------------------------------------------------------------------------

class TestT1PG33Geometry:
    """T1: PG(3,3) has 40 points, 240 W(3,3) edges, 12-regular."""

    def test_40_points(self, summary):
        """PG(3,3) has 40 points."""
        assert summary["T1_n_pg33"] == 40

    def test_27_affine(self, summary):
        """27 affine AG(3,3) points."""
        assert summary["T1_n_affine"] == 27

    def test_13_infinity(self, summary):
        """13 infinity PG(2,3) points."""
        assert summary["T1_n_infinity"] == 13

    def test_240_edges(self, summary):
        """W(3,3) has 240 collinearity edges."""
        assert summary["T1_n_edges"] == 240

    def test_all_degree_12(self, summary):
        """Every vertex has degree 12."""
        assert summary["T1_all_degree_12"] is True

    def test_single_degree_value(self, summary):
        """Degree distribution contains only 12."""
        assert set(summary["T1_degree_dist"].keys()) == {12}

    def test_t1_correct(self, summary):
        """T1 overall correctness flag."""
        assert summary["T1_correct"] is True

    def test_27_plus_13_equals_40(self, summary):
        """27 affine + 13 infinity = 40 total."""
        assert summary["T1_n_affine"] + summary["T1_n_infinity"] == 40


# ---------------------------------------------------------------------------
# T2: Infinity neighbor map
# ---------------------------------------------------------------------------

class TestT2InfinityNeighborMap:
    """T2: Each affine point has exactly 4 distinct infinity neighbors."""

    def test_27_affine_rows(self, summary):
        """27 affine points in the neighbor table."""
        assert summary["T2_n_affine_rows"] == 27

    def test_all_have_4_neighbors(self, summary):
        """Every affine point has exactly 4 distinct infinity neighbors."""
        assert summary["T2_all_4_neighbors"] is True

    def test_all_in_infinity_range(self, summary):
        """All infinity neighbors are in {0,...,12}."""
        assert summary["T2_all_in_infinity"] is True

    def test_total_incidences_108(self, summary):
        """Total incidences = 27 * 4 = 108."""
        assert summary["T2_total_incidences"] == 108

    def test_t2_correct(self, summary):
        """T2 overall correctness flag."""
        assert summary["T2_correct"] is True

    def test_27_times_4_equals_108(self, summary):
        """27 * 4 = 108."""
        assert summary["T2_total_incidences"] == 27 * 4


# ---------------------------------------------------------------------------
# T3: Charge distribution
# ---------------------------------------------------------------------------

class TestT3ChargeDistribution:
    """T3: 12 infinity pts have charge 9; 1 has charge 0 (the special pt 4)."""

    def test_12_charged_pts(self, summary):
        """Exactly 12 infinity points have nonzero charge."""
        assert summary["T3_num_charged"] == 12

    def test_1_zero_charge_pt(self, summary):
        """Exactly 1 infinity point has charge 0."""
        assert summary["T3_num_zero"] == 1

    def test_all_nonzero_charges_9(self, summary):
        """All charged infinity points have charge exactly 9."""
        assert summary["T3_all_charge_9"] is True

    def test_total_charge_108(self, summary):
        """Total charge = 12 * 9 = 108 = 27 * 4."""
        assert summary["T3_total_charge"] == 108

    def test_one_zero_charge(self, summary):
        """Exactly one zero-charge infinity point."""
        assert summary["T3_one_zero"] is True

    def test_special_point_is_4(self, summary):
        """The special (charge-0) infinity point has pg_id = 4."""
        assert summary["T3_special_pt"] == 4

    def test_t3_correct(self, summary):
        """T3 overall correctness flag."""
        assert summary["T3_correct"] is True

    def test_12_times_9_equals_108(self, summary):
        """12 * 9 = 108."""
        assert 12 * 9 == 108

    def test_zero_charge_list_length_1(self, summary):
        """Exactly one point in zero-charge list."""
        assert len(summary["T3_zero_charge_pts"]) == 1


# ---------------------------------------------------------------------------
# T4: NP orbit structure
# ---------------------------------------------------------------------------

class TestT4NPOrbits:
    """T4: NP gives 2 orbits of sizes 12 and 27 on 39 non-origin PG(3,3) points."""

    def test_two_np_orbits(self, summary):
        """Exactly 2 NP orbits."""
        assert summary["T4_np_two_orbits"] is True

    def test_orbit_sizes_12_and_27(self, summary):
        """Orbit sizes are 12 and 27."""
        assert sorted(summary["T4_np_orbit_sizes"]) == [12, 27]

    def test_orbit_12_exists(self, summary):
        """Orbit of size 12 exists."""
        assert summary["T4_np_orbit12_exists"] is True

    def test_orbit_27_exists(self, summary):
        """Orbit of size 27 exists."""
        assert summary["T4_np_orbit27_exists"] is True

    def test_np_total_39(self, summary):
        """NP orbits cover 39 = 40 - 1 points."""
        assert summary["T4_np_total"] == 39

    def test_t4_correct(self, summary):
        """T4 overall correctness flag."""
        assert summary["T4_correct"] is True

    def test_12_plus_27_equals_39(self, summary):
        """12 + 27 = 39."""
        assert sum(summary["T4_np_orbit_sizes"]) == 39


# ---------------------------------------------------------------------------
# T5: Outer twist orbits
# ---------------------------------------------------------------------------

class TestT5OuterTwistOrbits:
    """T5: Outer twist gives 5 orbits on 27 affine pts with size dist {1:1, 2:1, 8:3}."""

    def test_5_orbits(self, summary):
        """Exactly 5 outer-twist orbits on affine points."""
        assert summary["T5_num_orbits"] == 5

    def test_total_affine_27(self, summary):
        """Orbits cover all 27 affine points."""
        assert summary["T5_total_affine"] == 27

    def test_size_dist_correct(self, summary):
        """Size distribution = {1:1, 2:1, 8:3}."""
        assert summary["T5_size_dist_correct"] is True

    def test_one_fixed_point(self, summary):
        """Exactly 1 fixed affine point (orbit size 1)."""
        assert summary["T5_one_fixed"] is True

    def test_one_pair_orbit(self, summary):
        """Exactly 1 orbit of size 2."""
        assert summary["T5_one_pair"] is True

    def test_three_size8_orbits(self, summary):
        """Exactly 3 orbits of size 8 (covering 24 affine pts)."""
        assert summary["T5_three_8orbits"] is True

    def test_t5_correct(self, summary):
        """T5 overall correctness flag."""
        assert summary["T5_correct"] is True

    def test_1_plus_2_plus_24_equals_27(self, summary):
        """1 + 2 + 3*8 = 1 + 2 + 24 = 27."""
        dist = summary["T5_outer_size_dist"]
        assert sum(k * v for k, v in dist.items()) == 27


# ---------------------------------------------------------------------------
# T6: Affine coordinate structure
# ---------------------------------------------------------------------------

class TestT6AffineCoordinates:
    """T6: NP orbit-0 has 9 affine points; each (x,y) appears with all 3 t-values."""

    def test_orbit0_affine_count_9(self, summary):
        """NP orbit-0 contains exactly 9 affine points."""
        assert summary["T6_orbit0_affine_count"] == 9

    def test_each_xy_has_3_t_values(self, summary):
        """Each (x,y) pair in orbit-0 affine appears with t=0,1,2."""
        assert summary["T6_orbit0_each_xy_has_3_t"] is True

    def test_J_is_4x4(self, summary):
        """Symplectic form J is a 4x4 matrix."""
        assert summary["T6_J_is_4x4"] is True

    def test_N4_is_4x4(self, summary):
        """Outer twist N4 is a 4x4 matrix."""
        assert summary["T6_N4_is_4x4"] is True

    def test_t6_correct(self, summary):
        """T6 overall correctness flag."""
        assert summary["T6_correct"] is True


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_infinity_charge.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_infinity_charge.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_n_pg33", "T1_n_affine", "T1_n_infinity", "T1_n_edges", "T1_correct",
            "T2_all_4_neighbors", "T2_total_incidences", "T2_correct",
            "T3_num_charged", "T3_all_charge_9", "T3_special_pt", "T3_correct",
            "T4_np_orbit_sizes", "T4_correct",
            "T5_num_orbits", "T5_size_dist_correct", "T5_correct",
            "T6_orbit0_affine_count", "T6_correct",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
