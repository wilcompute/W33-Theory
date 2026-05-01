#!/usr/bin/env python3
"""Tests for Pillar 84 (Part CXC): Cocycle-Heisenberg-Tomotope Bridge.

Verifies six theorems proving that the Z3 cocycle on the K-Schreier graph,
the Heisenberg K27 twin-pair structure, and the tomotope triality element t4
form a single coherent bridge.
"""

from __future__ import annotations

import json
import os

import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(repo_root, "data", "w33_cocycle_heisenberg_bridge.json")


@pytest.fixture(scope="module")
def report():
    if not os.path.exists(DATA_FILE):
        pytest.skip(
            f"Missing data file: {DATA_FILE}; "
            "run THEORY_PART_CXC_COCYCLE_HEISENBERG_BRIDGE.py first"
        )
    with open(DATA_FILE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# T1: L-label distribution over 54 pockets
# ---------------------------------------------------------------------------


class TestT1LDistribution:
    def test_status_ok(self, report):
        assert report["status"] == "ok"

    def test_phase_0_count(self, report):
        assert report["T1_L_phase_0"] == 17

    def test_phase_1_count(self, report):
        assert report["T1_L_phase_1"] == 11

    def test_phase_2_count(self, report):
        assert report["T1_L_phase_2"] == 26

    def test_total_pockets(self, report):
        assert report["T1_L_total"] == 54

    def test_phases_sum_to_54(self, report):
        assert (
            report["T1_L_phase_0"] + report["T1_L_phase_1"] + report["T1_L_phase_2"]
        ) == 54

    def test_phase_2_dominant(self, report):
        """Phase 2 has the most pockets (26 > 17 > 11)."""
        assert report["T1_L_phase_2"] > report["T1_L_phase_0"] > report["T1_L_phase_1"]


# ---------------------------------------------------------------------------
# T2: Voltage reconstruction exact on all 270 edges
# ---------------------------------------------------------------------------


class TestT2VoltageReconstruction:
    def test_edges_total(self, report):
        assert report["T2_edges_total"] == 270

    def test_edges_ok(self, report):
        assert report["T2_edges_ok"] == 270

    def test_reconstruction_exact(self, report):
        assert report["T2_reconstruction_exact"] is True

    def test_all_edges_satisfied(self, report):
        assert report["T2_edges_ok"] == report["T2_edges_total"]


# ---------------------------------------------------------------------------
# T3: Only g3 carries nontrivial shift s_g = c^2
# ---------------------------------------------------------------------------


class TestT3OnlyG3Nontrivial:
    def test_g3_sg_is_c2(self, report):
        assert report["T3_g3_sg_is_c2"] is True

    def test_g3_nontrivial_edges(self, report):
        """Exactly 54 g3-edges (one per pocket) carry s_g=c^2."""
        assert report["T3_g3_nontrivial_edges"] == 54

    def test_others_sg_trivial(self, report):
        """g2, g5, g8, g9 all have s_g=id."""
        assert report["T3_others_sg_trivial"] is True

    def test_total_nontrivial_sg(self, report):
        assert report["T3_total_nontrivial_sg"] == 54


# ---------------------------------------------------------------------------
# T4: K27 stabilizer is C6
# ---------------------------------------------------------------------------


class TestT4K27StabilizerC6:
    def test_C6_size(self, report):
        assert report["T4_C6_size"] == 6

    def test_C6_abelian(self, report):
        assert report["T4_C6_abelian"] is True

    def test_C6_order_dist_has_order_6(self, report):
        """Order distribution includes order-6 elements."""
        assert "6" in report["T4_C6_order_dist"]
        assert report["T4_C6_order_dist"]["6"] == 2

    def test_C6_order_dist_has_order_1(self, report):
        assert report["T4_C6_order_dist"]["1"] == 1

    def test_C6_order_dist_has_order_2(self, report):
        assert report["T4_C6_order_dist"]["2"] == 1

    def test_C6_order_dist_has_order_3(self, report):
        assert report["T4_C6_order_dist"]["3"] == 2

    def test_C6_gen_order_on_27(self, report):
        assert report["T4_C6_gen_order_on_27"] == 6

    def test_q_xy_is_3x3(self, report):
        """q_xy table has exactly 9 entries (3x3)."""
        assert report["T4_q_xy_size"] == 9


# ---------------------------------------------------------------------------
# T5: Tomotope t4 element cycle structure
# ---------------------------------------------------------------------------


class TestT5TomotopT4:
    def test_t_order(self, report):
        """t = r1*r2 in tomotope has order 12."""
        assert report["T5_t_order"] == 12

    def test_t4_fixed_flags(self, report):
        """t4 fixes exactly 96 of 192 tomotope flags."""
        assert report["T5_t4_fixed_flags"] == 96

    def test_t4_3cycles(self, report):
        """t4 has exactly 32 three-cycles on flags."""
        assert report["T5_t4_3cycles"] == 32

    def test_t4_total_flags(self, report):
        """Total flags accounted: 96 + 32*3 = 192."""
        assert report["T5_t4_total_flags"] == 192

    def test_flags_account_correct(self, report):
        assert (report["T5_t4_fixed_flags"] + report["T5_t4_3cycles"] * 3) == 192

    def test_t4_order_3(self, report):
        """t4 = (t^4) has order 3 (since t has order 12 and gcd(4,12)=4, t^4 has order 3)."""
        # t has order 12, so t^12=id, t^4 has order 12/gcd(4,12) = 12/4 = 3
        assert report["T5_t_order"] % 4 == 0
        assert (report["T5_t_order"] // 4) == 3


# ---------------------------------------------------------------------------
# T6: Twin-phase consistency
# ---------------------------------------------------------------------------


class TestT6TwinPhaseConsistency:
    def test_twin_pairs_total(self, report):
        assert report["T6_twin_pairs_total"] == 27

    def test_same_phase_count(self, report):
        """Exactly 9 of 27 twin-pairs have identical L-phase for both pockets."""
        assert report["T6_same_phase_count"] == 9

    def test_diff_phase_count(self, report):
        assert report["T6_diff_phase_count"] == 18

    def test_same_diff_sum(self, report):
        assert (report["T6_same_phase_count"] + report["T6_diff_phase_count"]) == 27

    def test_q_xy_origin_zero(self, report):
        """q_xy(0,0) = 0: no z-shift at the origin."""
        assert report["T6_q_xy_origin_zero"] is True

    def test_q_xy_nontrivial_entries(self, report):
        """q_xy has nontrivial (non-zero) entries."""
        assert report["T6_q_xy_nontrivial_entries"] > 0


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestCocycleHeisenbergBridgeSummary:
    def test_summary_present(self, report):
        assert "summary" in report

    def test_summary_L_distribution(self, report):
        assert "17" in report["summary"]["L_distribution"]
        assert "54" in report["summary"]["L_distribution"]

    def test_summary_reconstruction(self, report):
        assert "270" in report["summary"]["reconstruction"]

    def test_summary_only_g3_nontrivial(self, report):
        assert "g3" in report["summary"]["only_g3_nontrivial"]
        assert "54" in report["summary"]["only_g3_nontrivial"]

    def test_summary_K27_stabilizer(self, report):
        assert "C6" in report["summary"]["K27_stabilizer"]
        assert "6" in report["summary"]["K27_stabilizer"]

    def test_summary_t4_cycle_struct(self, report):
        assert "96" in report["summary"]["t4_cycle_struct"]
        assert "32" in report["summary"]["t4_cycle_struct"]

    def test_summary_twin_phase(self, report):
        assert "9" in report["summary"]["twin_phase"]
        assert "27" in report["summary"]["twin_phase"]
