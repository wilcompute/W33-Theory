#!/usr/bin/env python3
"""Tests for Pillar 85 (Part CXCI): Tomotope Matched-Pair Push.

Verifies six theorems synthesizing the Zappa-Szep decomposition Gamma=N*P0,
the 12-step rotation t=r1*r2, triality bridge, and H vs N order spectra.
"""

from __future__ import annotations

import json
import os

import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(repo_root, "data", "w33_matched_pair_push.json")


@pytest.fixture(scope="module")
def report():
    if not os.path.exists(DATA_FILE):
        pytest.skip(
            f"optional matched-pair report missing: {DATA_FILE}; "
            "requires the tomotope matched-pair bundle and "
            "THEORY_PART_CXCI_MATCHED_PAIR_PUSH.py"
        )
    with open(DATA_FILE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# T1: Gamma = N * P0 (Zappa-Szep)
# ---------------------------------------------------------------------------


class TestT1GammaFactorization:
    def test_status_ok(self, report):
        assert report["status"] == "ok"

    def test_N_order(self, report):
        assert report["T1_N_order"] == 192

    def test_P0_order(self, report):
        assert report["T1_P0_order"] == 96

    def test_Gamma_order(self, report):
        assert report["T1_Gamma_order"] == 18432

    def test_Gamma_is_N_times_P0(self, report):
        assert report["T1_Gamma_is_N_times_P0"] is True

    def test_Gamma_order_product(self, report):
        assert report["T1_N_order"] * report["T1_P0_order"] == 18432

    def test_V4_image_P0_size(self, report):
        """P0 acts on V4 with image size 2 (not all of Aut(V4)=S3)."""
        assert report["T1_V4_image_P0_size"] == 2


# ---------------------------------------------------------------------------
# T2: t^k factorization; N-component period 4; t^12=id
# ---------------------------------------------------------------------------


class TestT2RotationFactorization:
    def test_rotation_steps(self, report):
        assert report["T2_rotation_steps"] == 12

    def test_t12_n_is_id(self, report):
        assert report["T2_t12_n_is_id"] is True

    def test_t12_p_is_id(self, report):
        assert report["T2_t12_p_is_id"] is True

    def test_N_component_distinct_values(self, report):
        """N-component of t^k takes exactly 4 distinct values."""
        assert sorted(report["T2_N_component_distinct_values"]) == [0, 101, 160, 180]

    def test_N_component_period(self, report):
        """N-component repeats with period 4."""
        assert report["T2_N_component_period"] == 4

    def test_N_component_count(self, report):
        """Exactly 4 distinct N-component values."""
        assert len(report["T2_N_component_distinct_values"]) == 4


# ---------------------------------------------------------------------------
# T3: t4 lies purely in P0 with order 3
# ---------------------------------------------------------------------------


class TestT3T4InP0:
    def test_t4_n_is_id(self, report):
        """t4 N-component is identity (n_idx=0)."""
        assert report["T3_t4_n_is_id"] is True

    def test_t4_p_idx(self, report):
        """t4 P0-index = 13."""
        assert report["T3_t4_p_idx"] == 13

    def test_t4_order(self, report):
        assert report["T3_t4_order"] == 3

    def test_t4_purely_in_P0(self, report):
        assert report["T3_t4_purely_in_P0"] is True

    def test_t4_order_divides_t_order(self, report):
        """Order of t4 divides order of t (12)."""
        assert 12 % report["T3_t4_order"] == 0


# ---------------------------------------------------------------------------
# T4: t4 action on N: cycle structure {1:96, 3:32}
# ---------------------------------------------------------------------------


class TestT4T4CycleStructure:
    def test_t4_fixed_N(self, report):
        assert report["T4_t4_fixed_N"] == 96

    def test_t4_3cycles_N(self, report):
        assert report["T4_t4_3cycles_N"] == 32

    def test_t4_total_N(self, report):
        assert report["T4_t4_total_N"] == 192

    def test_flags_account_correct(self, report):
        assert report["T4_t4_fixed_N"] + report["T4_t4_3cycles_N"] * 3 == 192

    def test_p_coaction_size(self, report):
        """P0 coaction has exactly 32 entries (one per 3-cycle)."""
        assert report["T4_p_coaction_size"] == 32


# ---------------------------------------------------------------------------
# T5: N has 3 Sylow-2 subgroups of order 64
# ---------------------------------------------------------------------------


class TestT5NSylow2Triality:
    def test_sylow2_order(self, report):
        assert report["T5_sylow2_order"] == 64

    def test_sylow2_count(self, report):
        assert report["T5_sylow2_count"] == 3

    def test_conjugating_element_order(self, report):
        assert report["T5_conjugating_element_order"] == 3

    def test_N_triality_decomp(self, report):
        assert report["T5_N_triality_192_eq_3x64"] is True

    def test_N_order_check(self, report):
        """192 = 3 * 64 (3 Sylow-2 sectors)."""
        assert report["T5_sylow2_count"] * report["T5_sylow2_order"] == 192


# ---------------------------------------------------------------------------
# T6: H vs N order spectra; Z3 cocycle sanity
# ---------------------------------------------------------------------------


class TestT6HvsNSpectra:
    def test_H_order8_count(self, report):
        assert report["T6_H_order8_count"] == 48

    def test_N_order8_count(self, report):
        assert report["T6_N_order8_count"] == 0

    def test_N_extra_order4(self, report):
        """N has exactly 48 more order-4 elements than H."""
        assert report["T6_N_extra_order4"] == 48

    def test_shared_orders_match(self, report):
        assert report["T6_shared_orders_match"] is True

    def test_Z3_cocycle_sanity_ok(self, report):
        assert report["T6_Z3_cocycle_sanity_ok"] == 200

    def test_Z3_cocycle_sanity_tested(self, report):
        assert report["T6_Z3_cocycle_sanity_tested"] == 200

    def test_cocycle_sanity_all_pass(self, report):
        assert (
            report["T6_Z3_cocycle_sanity_ok"] == report["T6_Z3_cocycle_sanity_tested"]
        )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestMatchedPairPushSummary:
    def test_summary_present(self, report):
        assert "summary" in report

    def test_summary_Gamma_factorization(self, report):
        assert "18432" in report["summary"]["Gamma_factorization"]
        assert "192" in report["summary"]["Gamma_factorization"]

    def test_summary_t12_rotation(self, report):
        assert "12" in report["summary"]["t12_rotation"]
        assert "period 4" in report["summary"]["t12_rotation"]

    def test_summary_t4_in_P0(self, report):
        assert "P0" in report["summary"]["t4_in_P0"]
        assert "3" in report["summary"]["t4_in_P0"]

    def test_summary_t4_cycle_struct(self, report):
        assert "96" in report["summary"]["t4_cycle_struct"]
        assert "32" in report["summary"]["t4_cycle_struct"]

    def test_summary_N_triality(self, report):
        assert "3" in report["summary"]["N_triality"]
        assert "64" in report["summary"]["N_triality"]

    def test_summary_H_vs_N(self, report):
        assert "48" in report["summary"]["H_vs_N"]
