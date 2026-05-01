#!/usr/bin/env python3
"""Tests for Pillar 78 (Part CLXXXVI): 192-Flag Maniplex Model Inside H.

Verifies the six theorems establishing that the axis-line stabilizer H (order 192)
carries an explicit rank-4 maniplex structure on its 192 elements, with generators
r0..r3 satisfying commutation axioms but FAILING the intersection/C-group condition.
"""

from __future__ import annotations

import json
import os

import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_FILE = os.path.join(repo_root, "data", "w33_flag_model_conjugacy.json")


@pytest.fixture(scope="module")
def report():
    if not os.path.exists(DATA_FILE):
        pytest.skip(
            f"Missing data file: {DATA_FILE}\n"
            "Run THEORY_PART_CLXXXVI_FLAG_MODEL_CONJUGACY.py first."
        )
    with open(DATA_FILE) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# T1: Generators r0..r3 are involutions satisfying commutation axioms
# ---------------------------------------------------------------------------


class TestT1CommutationAxioms:
    def test_status_ok(self, report):
        assert report["status"] == "ok"

    def test_r0_involution(self, report):
        assert report["T1_r0_involution"] is True

    def test_r1_involution(self, report):
        assert report["T1_r1_involution"] is True

    def test_r2_involution(self, report):
        assert report["T1_r2_involution"] is True

    def test_r3_involution(self, report):
        assert report["T1_r3_involution"] is True

    def test_r0_commutes_r2(self, report):
        assert report["T1_r0_commutes_r2"] is True

    def test_r0_commutes_r3(self, report):
        assert report["T1_r0_commutes_r3"] is True

    def test_r1_commutes_r3(self, report):
        assert report["T1_r1_commutes_r3"] is True


# ---------------------------------------------------------------------------
# T2: Intersection condition FAILS (non-C-group)
# ---------------------------------------------------------------------------


class TestT2IntersectionFails:
    def test_size_r0r1r2(self, report):
        assert report["T2_size_r0r1r2"] == 48

    def test_size_r1r2r3(self, report):
        assert report["T2_size_r1r2r3"] == 192

    def test_size_r1r2(self, report):
        assert report["T2_size_r1r2"] == 12

    def test_intersection_size(self, report):
        assert report["T2_intersection"] == 48

    def test_intersection_ratio(self, report):
        """Ratio = 48/12 = 4 (expected 1 for a C-group)."""
        assert report["T2_intersection_ratio"] == 4

    def test_C_group_condition_fails(self, report):
        assert report["T2_C_group_condition_fails"] is True

    def test_ratio_not_one(self, report):
        """Ratio must be > 1 to confirm non-C-group."""
        assert report["T2_intersection_ratio"] > 1

    def test_r1r2r3_is_full_H(self, report):
        """<r1,r2,r3> generates all 192 H-elements."""
        assert report["T2_size_r1r2r3"] == 192


# ---------------------------------------------------------------------------
# T3: f-vector (1, 16, 12, 4) — axis maniplex geometry
# ---------------------------------------------------------------------------


class TestT3AxisFVector:
    def test_fvector_vertices(self, report):
        assert report["T3_fvector"]["V"] == 1

    def test_fvector_edges(self, report):
        assert report["T3_fvector"]["E"] == 16

    def test_fvector_faces(self, report):
        assert report["T3_fvector"]["F"] == 12

    def test_fvector_cells(self, report):
        assert report["T3_fvector"]["C"] == 4

    def test_is_axis_fvector(self, report):
        assert report["T3_is_axis_fvector"] is True

    def test_not_tomotope_fvector(self, report):
        """f-vector is NOT the tomotope (4,12,16,8)."""
        assert report["T3_not_tomotope_fvector"] is True

    def test_fvector_complete(self, report):
        """All four f-vector components present."""
        fv = report["T3_fvector"]
        assert set(fv.keys()) == {"V", "E", "F", "C"}

    def test_fvector_sum(self, report):
        """V + E + F + C = 33 (Euler-related count)."""
        fv = report["T3_fvector"]
        assert fv["V"] + fv["E"] + fv["F"] + fv["C"] == 33


# ---------------------------------------------------------------------------
# T4: H+ has 2 flag orbits of size 96 each
# ---------------------------------------------------------------------------


class TestT4HPlusFlagOrbits:
    def test_num_orbits(self, report):
        assert report["T4_hplus_flag_orbits"] == 2

    def test_orbit_sizes(self, report):
        assert sorted(report["T4_orbit_sizes"]) == [96, 96]

    def test_orbit_total(self, report):
        """Both orbits together cover all 192 flags."""
        assert sum(report["T4_orbit_sizes"]) == 192

    def test_tomotope_signature_match(self, report):
        """Matches tomotope metadata: symmetry=96, flag orbits=2."""
        assert report["T4_tomotope_signature_match"] is True

    def test_each_orbit_size_96(self, report):
        """Each orbit has exactly 96 elements (= order of H+)."""
        for s in report["T4_orbit_sizes"]:
            assert s == 96


# ---------------------------------------------------------------------------
# T5: Triality element t (stab_index=399, order 3) in H-maniplex
# ---------------------------------------------------------------------------


class TestT5TrialityElement:
    def test_stab_index(self, report):
        assert report["T5_triality_stab_index"] == 399

    def test_order_3(self, report):
        assert report["T5_triality_order"] == 3

    def test_flag_idx_in_range(self, report):
        assert 0 <= report["T5_triality_flag_idx"] < 192

    def test_flag_idx_is_71(self, report):
        """Triality element t is at flag_idx=71 (matches Pillar 72 H-index 71)."""
        assert report["T5_triality_flag_idx"] == 71

    def test_matches_pillar75(self, report):
        assert report["T5_triality_matches_Pillar75"] is True


# ---------------------------------------------------------------------------
# T6: Inversion conjugator — left -> right regular action
# ---------------------------------------------------------------------------


class TestT6InversionConjugator:
    def test_torsor_to_flag_is_identity(self, report):
        assert report["T6_torsor_to_flag_is_identity"] is True

    def test_inv_conjugator_is_bijection(self, report):
        assert report["T6_inv_conjugator_is_bijection"] is True

    def test_inv_conjugator_not_identity(self, report):
        """Inversion conjugator is a non-trivial deck map."""
        assert report["T6_inv_conjugator_is_identity"] is False


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------


class TestFlagModelConjugacySummary:
    def test_summary_present(self, report):
        assert "summary" in report

    def test_summary_generators(self, report):
        assert "involutions" in report["summary"]["generators"]

    def test_summary_C_group_fails(self, report):
        assert "48" in report["summary"]["C_group_fails"]
        assert "12" in report["summary"]["C_group_fails"]
        assert "ratio=4" in report["summary"]["C_group_fails"]

    def test_summary_fvector(self, report):
        assert "(1,16,12,4)" in report["summary"]["fvector"]
        assert "axis" in report["summary"]["fvector"]

    def test_summary_H_plus_orbits(self, report):
        assert "96" in report["summary"]["H_plus_orbits"]

    def test_summary_triality(self, report):
        assert "399" in report["summary"]["triality"]
        assert "3" in report["summary"]["triality"]

    def test_summary_inversion_conj(self, report):
        assert (
            "right" in report["summary"]["inversion_conj"].lower()
            or "left" in report["summary"]["inversion_conj"].lower()
        )
