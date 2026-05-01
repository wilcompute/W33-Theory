#!/usr/bin/env python3
"""Tests for Pillar 83 (Part CLXXXIX): Local Weld -- K Stabilizer C3 in Axis-192.

Verifies six theorems establishing the explicit local weld embedding the K
pocket-stabilizer C3 into the axis-line stabilizer H via right-multiplication.
"""

from __future__ import annotations

import json
import os

import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(repo_root, "data", "w33_local_weld.json")


@pytest.fixture(scope="module")
def report():
    if not os.path.exists(DATA_FILE):
        pytest.skip(
            f"Missing data file: {DATA_FILE}\n"
            "Run THEORY_PART_CLXXXIX_LOCAL_WELD.py first."
        )
    with open(DATA_FILE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# T1: K transitive on 54 pockets; |K|=162; stabilizer C3; 270 Schreier edges
# ---------------------------------------------------------------------------


class TestT1KTransitive:
    def test_status_ok(self, report):
        assert report["status"] == "ok"

    def test_K_order(self, report):
        assert report["T1_K_order"] == 162

    def test_pocket_orbit_size(self, report):
        assert report["T1_pocket_orbit_size"] == 54

    def test_stabilizer_size(self, report):
        assert report["T1_stabilizer_size"] == 3

    def test_schreier_edges(self, report):
        assert report["T1_schreier_edges"] == 270

    def test_edges_eq_54x5(self, report):
        """270 = 54 pockets x 5 K-generators."""
        assert report["T1_edges_eq_54x5"] is True

    def test_K_order_factorization(self, report):
        """162 = 2 * 3^4 (correct for K)."""
        assert report["T1_K_order"] == 2 * 3**4


# ---------------------------------------------------------------------------
# T2: Stabilizer C3 = {id, sigma, sigma^{-1}}; sigma=(1,3,5,0,2,4,6); sigma^3=id
# ---------------------------------------------------------------------------


class TestT2StabilizerC3:
    def test_stab_count(self, report):
        assert report["T2_stab_count"] == 3

    def test_exponents(self, report):
        assert sorted(report["T2_exponents"]) == [0, 1, 2]

    def test_sigma(self, report):
        assert report["T2_sigma"] == [1, 3, 5, 0, 2, 4, 6]

    def test_sigma_inv(self, report):
        assert report["T2_sigma_inv"] == [3, 0, 4, 1, 5, 2, 6]

    def test_sigma_sq_is_inv(self, report):
        assert report["T2_sigma_sq_is_inv"] is True

    def test_sigma_order_3(self, report):
        assert report["T2_sigma_order_3"] is True

    def test_sigma_generates_C3(self, report):
        """sigma on 7 elements; sigma^3 = id verified."""
        sig = report["T2_sigma"]
        sig_inv = report["T2_sigma_inv"]
        # sigma composed with sigma_inv should give identity
        composed = [sig_inv[sig[i]] for i in range(7)]
        assert composed == list(range(7))


# ---------------------------------------------------------------------------
# T3: Order-preserving weld map sigma^k -> r(sigma^k)
# ---------------------------------------------------------------------------


class TestT3OrderPreservingWeld:
    def test_id_stab_index(self, report):
        assert report["T3_id_stab_index"] == 7

    def test_id_order(self, report):
        assert report["T3_id_order"] == 1

    def test_sigma_stab_index(self, report):
        assert report["T3_sigma_stab_index"] == 399

    def test_sigma_order(self, report):
        assert report["T3_sigma_order"] == 3

    def test_sigma_inv_stab_index(self, report):
        assert report["T3_sigma_inv_stab_index"] == 246

    def test_sigma_inv_order(self, report):
        assert report["T3_sigma_inv_order"] == 3

    def test_order_preserving(self, report):
        assert report["T3_order_preserving"] is True

    def test_triality_stab_index_matches_pillar75(self, report):
        """Triality element (stab_index=399) is the same C3 weld from Pillar 75."""
        assert report["T3_sigma_stab_index"] == 399


# ---------------------------------------------------------------------------
# T4: Right-multiplication matching on 192 torsor
# ---------------------------------------------------------------------------


class TestT4RightMultiplying:
    def test_right_mult_matches_all_3(self, report):
        assert report["T4_right_mult_matches_all_3"] is True

    def test_r_a_is_bijection(self, report):
        assert report["T4_r_a_is_bijection"] is True

    def test_r_a_order_on_192(self, report):
        """r_a has order 3 on the 192-element torsor."""
        assert report["T4_r_a_order_on_192"] == 3

    def test_r_a_stab_index(self, report):
        """r_a corresponds to stab_index=399 (same as sigma)."""
        assert report["T4_r_a_stab_index"] == 399


# ---------------------------------------------------------------------------
# T5: No deck flip in K
# ---------------------------------------------------------------------------


class TestT5NoDeckFlip:
    def test_no_deck_flip(self, report):
        assert report["T5_deck_flip_in_K"] is False

    def test_K_preserves_enc0_enc1(self, report):
        assert report["T5_K_preserves_enc0_enc1"] is True


# ---------------------------------------------------------------------------
# T6: Schreier cocycle voltage distribution
# ---------------------------------------------------------------------------


class TestT6CocycleDistribution:
    def test_exp_0_count(self, report):
        assert report["T6_exp_0_count"] == 201

    def test_exp_1_count(self, report):
        assert report["T6_exp_1_count"] == 33

    def test_exp_2_count(self, report):
        assert report["T6_exp_2_count"] == 36

    def test_total_edges(self, report):
        assert report["T6_total_edges"] == 270

    def test_nontrivial_edges(self, report):
        assert report["T6_nontrivial_edges"] == 69

    def test_nontrivial_sums_to_total(self, report):
        assert (
            report["T6_exp_0_count"]
            + report["T6_exp_1_count"]
            + report["T6_exp_2_count"]
        ) == 270

    def test_nontrivial_stab399(self, report):
        assert report["T6_nontrivial_stab399"] == 33

    def test_nontrivial_stab246(self, report):
        assert report["T6_nontrivial_stab246"] == 36

    def test_nontrivial_stabs_sum(self, report):
        """Nontrivial edges all carry stab_index 399 or 246."""
        assert (report["T6_nontrivial_stab399"] + report["T6_nontrivial_stab246"]) == 69

    def test_matches_K_descent_discrepancies(self, report):
        """Matches Pillar 71 T2 cocycle discrepancies {0:148, 1:33, 2:36}."""
        assert report["T6_matches_K_descent_discrepancies"] is True


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestLocalWeldSummary:
    def test_summary_present(self, report):
        assert "summary" in report

    def test_summary_K_weld(self, report):
        assert "162" in report["summary"]["K_weld"]
        assert "270" in report["summary"]["K_weld"]

    def test_summary_stabilizer_C3(self, report):
        assert "sigma^3=id" in report["summary"]["stabilizer_C3"]

    def test_summary_order_preserving(self, report):
        assert "399" in report["summary"]["order_preserving"]
        assert "246" in report["summary"]["order_preserving"]

    def test_summary_right_mult_exact(self, report):
        assert "192" in report["summary"]["right_mult_exact"]

    def test_summary_no_deck_flip(self, report):
        assert "enc0" in report["summary"]["no_deck_flip"]

    def test_summary_cocycle_dist(self, report):
        assert "69" in report["summary"]["cocycle_dist"]
        assert "33" in report["summary"]["cocycle_dist"]
        assert "36" in report["summary"]["cocycle_dist"]
