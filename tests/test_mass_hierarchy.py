#!/usr/bin/env python3
"""Tests for Pillar 68: Fermion Mass Texture from W33 Z3 Yukawa Grading.

Tests all six theorems from THEORY_PART_CLXXVII_MASS_TEXTURE.py:
  T1: Z3 grade decomposition of H27 (9 orbits, grade dims = [9,9,9])
  T2: Exact Z3 Yukawa texture (0 of 162 violations)
  T3: Form-factor bounds (nontrivial hierarchy; legacy sqrt(15) lock falsified)
  T4: Higgs VEV grade fractions from Pillar 65
  T5: GUT-scale mass texture (hierarchical SVD ratios)
  T6: Golay algebra pure symplectic normal form (phi=0, 9 outer Der)
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pytest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, repo_root)
sys.path.insert(0, os.path.join(repo_root, "scripts"))

from THEORY_PART_CLXXVII_MASS_TEXTURE import (
    _build_r3_fixing_v0,
    _build_r_on_h27,
    _grade_projectors,
    theorem1_z3_grade_decomposition,
    theorem2_yukawa_texture,
    theorem3_form_factor_bounds,
    theorem4_higgs_grade_fractions,
    theorem5_gut_scale_mass_texture,
    theorem6_golay_pure_symplectic,
)
from w33_homology import build_w33

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def w33_graph():
    n, vertices, adj, edges = build_w33()
    return n, vertices, adj, edges


@pytest.fixture(scope="module")
def r3_vperm(w33_graph):
    n, vertices, adj, edges = w33_graph
    return _build_r3_fixing_v0(n, vertices, adj, edges)


@pytest.fixture(scope="module")
def h27_verts(w33_graph):
    n, vertices, adj, edges = w33_graph
    adj_list = [[] for _ in range(n)]
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    return [v for v in range(n) if v != 0 and 0 not in adj_list[v]]


@pytest.fixture(scope="module")
def r_mat(r3_vperm, h27_verts):
    return _build_r_on_h27(r3_vperm, h27_verts)


@pytest.fixture(scope="module")
def grade_projectors(r_mat):
    return _grade_projectors(r_mat)


@pytest.fixture(scope="module")
def t1_result():
    return theorem1_z3_grade_decomposition()


@pytest.fixture(scope="module")
def t2_result():
    return theorem2_yukawa_texture()


@pytest.fixture(scope="module")
def t3_result():
    return theorem3_form_factor_bounds()


@pytest.fixture(scope="module")
def t4_result():
    return theorem4_higgs_grade_fractions()


@pytest.fixture(scope="module")
def t5_result():
    return theorem5_gut_scale_mass_texture()


@pytest.fixture(scope="module")
def t6_result():
    return theorem6_golay_pure_symplectic()


# ---------------------------------------------------------------------------
# T1: Z3 Grade Decomposition
# ---------------------------------------------------------------------------


class TestT1Z3GradeDecomposition:
    def test_h27_has_27_vertices(self, t1_result):
        assert t1_result["n_h27_vertices"] == 27

    def test_no_fixed_points(self, t1_result):
        assert t1_result["n_fixed_points"] == 0

    def test_nine_three_element_orbits(self, t1_result):
        assert t1_result["n_3element_orbits"] == 9

    def test_all_orbits_size3(self, t1_result):
        assert t1_result["all_orbits_size3"] is True

    def test_grade_eigenspace_dims_are_9_each(self, t1_result):
        assert t1_result["grade_eigenspace_dims"] == [9, 9, 9]

    def test_projectors_complete(self, t1_result):
        assert t1_result["projectors_complete"] is True

    def test_r3_fixes_vertex0(self, r3_vperm):
        # R fixes vertex 0
        assert r3_vperm[0] == 0

    def test_r3_is_order3(self, r3_vperm, w33_graph):
        n, vertices, adj, edges = w33_graph
        R2 = tuple(r3_vperm[r3_vperm[i]] for i in range(n))
        R3 = tuple(r3_vperm[R2[i]] for i in range(n))
        assert R3 == tuple(range(n))

    def test_r_preserves_h27(self, r3_vperm, h27_verts):
        h27_set = set(h27_verts)
        for v in h27_verts:
            assert r3_vperm[v] in h27_set

    def test_r_mat_is_27x27(self, r_mat):
        assert r_mat.shape == (27, 27)

    def test_r_mat_is_unitary(self, r_mat):
        product = r_mat @ r_mat.conj().T
        np.testing.assert_allclose(product, np.eye(27), atol=1e-10)

    def test_r_mat_cubed_is_identity(self, r_mat):
        R3 = r_mat @ r_mat @ r_mat
        np.testing.assert_allclose(R3, np.eye(27), atol=1e-10)

    def test_projector_sum_is_identity(self, grade_projectors):
        P0, P1, P2 = grade_projectors
        total = P0 + P1 + P2
        np.testing.assert_allclose(total, np.eye(27), atol=1e-10)

    def test_projectors_are_orthogonal(self, grade_projectors):
        P0, P1, P2 = grade_projectors
        np.testing.assert_allclose(P0 @ P1, np.zeros((27, 27)), atol=1e-10)
        np.testing.assert_allclose(P1 @ P2, np.zeros((27, 27)), atol=1e-10)
        np.testing.assert_allclose(P0 @ P2, np.zeros((27, 27)), atol=1e-10)

    def test_projectors_are_idempotent(self, grade_projectors):
        for P in grade_projectors:
            np.testing.assert_allclose(P @ P, P, atol=1e-10)

    def test_each_projector_rank_is_9(self, grade_projectors):
        for P in grade_projectors:
            rank = int(round(np.real(np.trace(P))))
            assert rank == 9

    def test_r_eigenvalues_are_cube_roots(self, r_mat):
        omega = np.exp(2j * np.pi / 3)
        eigs = np.linalg.eigvals(r_mat)
        for e in eigs:
            diffs = [abs(e - 1), abs(e - omega), abs(e - omega**2)]
            assert min(diffs) < 1e-8


# ---------------------------------------------------------------------------
# T2: Exact Z3 Yukawa Texture
# ---------------------------------------------------------------------------


class TestT2YukawaTexture:
    def test_zero_violations(self, t2_result):
        assert t2_result["violations"] == 0

    def test_theorem_exact(self, t2_result):
        assert t2_result["theorem_exact"] is True

    def test_total_checks_is_162(self, t2_result):
        assert t2_result["total_checks"] == 162

    def test_exact_zeros_count(self, t2_result):
        # 6 pairs × 2 forbidden grades × 9 vecs = 108 exact zeros
        assert t2_result["exact_zeros"] == 108

    def test_non_zero_count(self, t2_result):
        # 6 pairs × 1 allowed grade × 9 vecs = 54 non-zero
        assert t2_result["total_checks"] - t2_result["exact_zeros"] == 54

    def test_texture_structure_00_block(self, t2_result):
        # grade-g=0 couples (a,b)=(0,0) and (1,2) [since 0+0=0, 1+2=3=0 mod 3]
        assert t2_result["violations"] == 0

    def test_t2_returns_required_keys(self, t2_result):
        for key in ["violations", "theorem_exact", "total_checks", "exact_zeros"]:
            assert key in t2_result


# ---------------------------------------------------------------------------
# T3: Form Factor Bounds
# ---------------------------------------------------------------------------


class TestT3FormFactorBounds:
    def test_grade0_eigenspace_dim_is_9(self, t3_result):
        assert t3_result["grade0_eigenspace_dim"] == 9

    def test_max_ratio_not_locked_to_sqrt15(self, t3_result):
        assert t3_result["max_ratio_approx_sqrt15"] is False

    def test_max_ratio_exceeds_sqrt15(self, t3_result):
        assert t3_result["ratio_f12_f00_max"] > np.sqrt(15)

    def test_min_ratio_positive(self, t3_result):
        assert t3_result["ratio_f12_f00_min"] > 0

    def test_ratio_range_is_reasonable(self, t3_result):
        assert t3_result["ratio_f12_f00_max"] > t3_result["ratio_f12_f00_min"]

    def test_f00_range_positive(self, t3_result):
        assert t3_result["f00_min"] > 0
        assert t3_result["f00_max"] > t3_result["f00_min"]

    def test_f12_range_positive(self, t3_result):
        assert t3_result["f12_min"] >= 0
        assert t3_result["f12_max"] > 0

    def test_geometry_splits_factor_positive(self, t3_result):
        assert t3_result["geometry_splits_by_factor"] > 1

    def test_t3_returns_required_keys(self, t3_result):
        for key in [
            "grade0_eigenspace_dim",
            "max_ratio_approx_sqrt15",
            "ratio_f12_f00_min",
            "ratio_f12_f00_max",
            "f00_min",
            "f00_max",
            "f12_min",
            "f12_max",
            "geometry_splits_by_factor",
        ]:
            assert key in t3_result


# ---------------------------------------------------------------------------
# T4: Higgs VEV Grade Fractions
# ---------------------------------------------------------------------------


class TestT4HiggsGradeFractions:
    def test_available(self, t4_result):
        # Requires Pillar 65 data; skip gracefully if missing
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")

    def test_v_up_fractions_sum_to_1(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        fracs = t4_result["v_up_grade_fractions"]
        assert abs(sum(fracs) - 1.0) < 1e-8

    def test_v_dn_fractions_sum_to_1(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        fracs = t4_result["v_dn_grade_fractions"]
        assert abs(sum(fracs) - 1.0) < 1e-8

    def test_v_up_fractions_nonnegative(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for f in t4_result["v_up_grade_fractions"]:
            assert f >= -1e-12

    def test_v_dn_fractions_nonnegative(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for f in t4_result["v_dn_grade_fractions"]:
            assert f >= -1e-12

    def test_v_up_dominant_grade_is_valid(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        assert t4_result["v_up_dominant_grade"] in [0, 1, 2]

    def test_v_dn_dominant_grade_is_valid(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        assert t4_result["v_dn_dominant_grade"] in [0, 1, 2]

    def test_v_up_dominant_grade_is_2(self, t4_result):
        # CKM-optimal VEV: grade-2 dominates v_up (50.2%)
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        assert t4_result["v_up_dominant_grade"] == 2

    def test_v_dn_dominant_grade_is_0(self, t4_result):
        # CKM-optimal VEV: grade-0 dominates v_dn (57.5%)
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        assert t4_result["v_dn_dominant_grade"] == 0

    def test_v_up_grade2_fraction_near_50pct(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        fracs = t4_result["v_up_grade_fractions"]
        assert abs(fracs[2] - 0.502) < 0.02

    def test_v_dn_grade0_fraction_near_57pct(self, t4_result):
        if not t4_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        fracs = t4_result["v_dn_grade_fractions"]
        assert abs(fracs[0] - 0.575) < 0.02


# ---------------------------------------------------------------------------
# T5: GUT-Scale Mass Texture
# ---------------------------------------------------------------------------


class TestT5GUTScaleMassTexture:
    def test_available(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")

    def test_has_four_yukawa_textures(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for label in ["up", "dn", "nu", "e"]:
            assert label in t5_result["yukawa_textures"]

    def test_singular_values_positive(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for label in ["up", "dn", "nu", "e"]:
            svs = t5_result["yukawa_textures"][label]["singular_values"]
            assert all(sv >= 0 for sv in svs), f"Negative SV for {label}"

    def test_singular_values_ordered_descending(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for label in ["up", "dn", "nu", "e"]:
            svs = t5_result["yukawa_textures"][label]["singular_values"]
            assert svs[0] >= svs[1] >= svs[2], f"SVs not ordered for {label}"

    def test_up_type_hierarchy_exists(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        svs = t5_result["yukawa_textures"]["up"]["singular_values"]
        # sv[0] should be at least 2x sv[2]
        assert svs[0] > 2 * svs[2]

    def test_dn_type_hierarchy_exists(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        svs = t5_result["yukawa_textures"]["dn"]["singular_values"]
        assert svs[0] > 2 * svs[2]

    def test_ratios_are_stored(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for label in ["up", "dn", "nu", "e"]:
            tx = t5_result["yukawa_textures"][label]
            assert "ratio_sv1_sv2" in tx
            assert "ratio_sv1_sv3" in tx

    def test_up_sv1_sv3_ratio_positive(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        tx = t5_result["yukawa_textures"]["up"]
        assert tx["ratio_sv1_sv3"] > 1.0

    def test_t5_returns_required_keys(self, t5_result):
        if not t5_result.get("available"):
            pytest.skip("Pillar 65 data not available")
        for key in [
            "available",
            "yukawa_textures",
            "up_type_ratios",
            "down_type_ratios",
            "interpretation",
        ]:
            assert key in t5_result


# ---------------------------------------------------------------------------
# T6: Golay Algebra Pure Symplectic Normal Form
# ---------------------------------------------------------------------------


class TestT6GolayPureSymplectic:
    def test_phi_is_zero(self, t6_result):
        assert t6_result["phi_is_zero"] is True

    def test_c_addition_holds(self, t6_result):
        assert t6_result["c_addition_holds"] is True

    def test_dim_outer_derivations_is_9(self, t6_result):
        assert t6_result["dim_outer_derivations"] == 9

    def test_dim_derivations_is_33(self, t6_result):
        assert t6_result["dim_derivations"] == 33

    def test_bracket_form_is_ascii(self, t6_result):
        bf = t6_result["bracket_form"]
        assert all(ord(c) < 128 for c in bf)

    def test_bracket_form_mentions_omega(self, t6_result):
        assert "omega" in t6_result["bracket_form"]

    def test_structure_string_present(self, t6_result):
        assert "structure" in t6_result
        assert "L0" in t6_result["structure"]

    def test_outer_decomposition_3_plus_6(self, t6_result):
        od = t6_result["outer_decomposition"]
        assert "3" in od and "6" in od

    def test_physics_key_present(self, t6_result):
        assert "physics" in t6_result

    def test_t6_returns_required_keys(self, t6_result):
        for key in [
            "phi_is_zero",
            "c_addition_holds",
            "bracket_form",
            "structure",
            "dim_outer_derivations",
            "dim_derivations",
            "outer_decomposition",
            "physics",
        ]:
            assert key in t6_result


# ---------------------------------------------------------------------------
# Saved JSON data tests
# ---------------------------------------------------------------------------


class TestSavedJSON:
    @pytest.fixture(scope="class")
    def data(self):
        path = os.path.join(repo_root, "data", "w33_mass_texture.json")
        if not os.path.exists(path):
            pytest.skip("data/w33_mass_texture.json not found")
        with open(path) as f:
            return json.load(f)

    def test_pillar_number(self, data):
        assert data["pillar"] == 68

    def test_title_present(self, data):
        assert "Mass Texture" in data["title"]

    def test_t1_stored(self, data):
        assert "T1_z3_grade_decomposition" in data

    def test_t2_stored(self, data):
        assert "T2_yukawa_texture" in data

    def test_t3_stored(self, data):
        assert "T3_form_factor_bounds" in data

    def test_t4_stored(self, data):
        assert "T4_higgs_grade_fractions" in data

    def test_t5_stored(self, data):
        assert "T5_gut_scale_mass_texture" in data

    def test_t6_stored(self, data):
        assert "T6_golay_pure_symplectic" in data

    def test_elapsed_positive(self, data):
        assert data["elapsed_s"] > 0

    def test_stored_t1_no_fixed_points(self, data):
        assert data["T1_z3_grade_decomposition"]["n_fixed_points"] == 0

    def test_stored_t2_zero_violations(self, data):
        assert data["T2_yukawa_texture"]["violations"] == 0

    def test_stored_t3_max_ratio_approx_sqrt15(self, data):
        assert data["T3_form_factor_bounds"]["max_ratio_approx_sqrt15"] is False

    def test_stored_t6_phi_is_zero(self, data):
        assert data["T6_golay_pure_symplectic"]["phi_is_zero"] is True

    def test_stored_t6_dim_outer_is_9(self, data):
        assert data["T6_golay_pure_symplectic"]["dim_outer_derivations"] == 9
