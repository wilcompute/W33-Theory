"""tests/test_mass_texture.py
Pillar 68: Fermion Mass Texture from W33 Z3 Yukawa Grading.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "pillars"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


@pytest.fixture(scope="module")
def results():
    from THEORY_PART_CLXXVII_MASS_TEXTURE import (
        theorem1_z3_grade_decomposition,
        theorem2_yukawa_texture,
        theorem3_form_factor_bounds,
        theorem6_golay_pure_symplectic,
    )

    return {
        "pillar": 68,
        "T1_z3_grade_decomposition": theorem1_z3_grade_decomposition(),
        "T2_yukawa_texture": theorem2_yukawa_texture(),
        "T3_form_factor_bounds": theorem3_form_factor_bounds(),
        "T6_golay_pure_symplectic": theorem6_golay_pure_symplectic(),
    }


def test_pillar_is_68(results):
    assert results["pillar"] == 68


def test_t1_z3_grade_decomposition(results):
    t1 = results["T1_z3_grade_decomposition"]
    assert t1["n_h27_vertices"] == 27
    assert t1["n_fixed_points"] == 0
    assert t1["n_3element_orbits"] == 9
    assert t1["grade_eigenspace_dims"] == [9, 9, 9]
    assert t1["projectors_complete"] is True
    assert t1["all_orbits_size3"] is True
    assert t1["n_local_triangles"] == 36


def test_t2_exact_yukawa_texture(results):
    t2 = results["T2_yukawa_texture"]
    assert t2["total_checks"] == 162
    assert t2["violations"] == 0
    assert t2["exact_zeros"] == 108
    assert t2["theorem_exact"] is True


def test_t3_form_factor_bounds(results):
    t3 = results["T3_form_factor_bounds"]
    assert t3["grade0_eigenspace_dim"] == 9
    assert t3["max_ratio_approx_sqrt15"] is False
    assert float(t3["ratio_f12_f00_max"]) > float(t3["ratio_f12_f00_min"])
    assert float(t3["ratio_f12_f00_min"]) > 0.0


def test_t6_golay_pure_symplectic_normal_form(results):
    t6 = results["T6_golay_pure_symplectic"]
    assert t6["phi_is_zero"] is True
    assert t6["c_addition_holds"] is True
    assert int(t6["dim_outer_derivations"]) == 9
    assert int(t6["dim_derivations"]) == 33
