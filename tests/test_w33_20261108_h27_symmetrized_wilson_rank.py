"""Exact H27 Wilson-loop orbit and forbidden singleton mass regressions."""
from __future__ import annotations
import importlib.util, os
from pathlib import Path
import pytest

SOURCE_ROOT=Path(__file__).resolve().parents[1]
ROOT=Path(os.environ.get("W33_REPO_ROOT",str(SOURCE_ROOT)))
sp=importlib.util.spec_from_file_location("h27_wilson_orbit",SOURCE_ROOT/"analysis/w33_20261108_h27_symmetrized_wilson_rank.py")
M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)

@pytest.fixture(scope="module")
def out():return M.reconstruct(ROOT)

def test_native_repository_data_and_group(out):
    assert out["native_holonomy_dimension"]==4
    assert out["native_H27_controller_elements"]==27
    assert out["distinct_matrices_in_four_real_dimensional_representation"]==9

def test_four_orbit_lengths_and_repetition(out):
    o=out["four_coordinate_orbits"]
    assert [x["distinct_symmetry_related_integer_wilson_charges"] for x in o]==[3,3,9,9]
    assert all(set(x["charge_multiplicities"])=={9 if x["selected_holonomy_index_zero_based"]<2 else 3} for x in o)

def test_symmetry_averaging_doubles_or_quadruples_rank(out):
    o=out["four_coordinate_orbits"]
    assert [x["symmetry_averaged_mass_hessian_rank"] for x in o]==[2,2,4,4]
    assert out["nonzero_H27_invariant_quadratic_mass_rank_choices"]==[2,4]

def test_primitive_wilson_integer_charge_lattice(out):
    o=out["four_coordinate_orbits"]
    assert [x["wilson_charge_smith_normal_form"] for x in o]==[[1,1],[1,1],[1,1,1,1],[1,1,1,1]]
    assert [x["cosine_potential_minimum_modulo_2pi"] for x in o]==[
        "continuous or discrete extra minima possible","continuous or discrete extra minima possible","unique","unique"]

def test_exact_e4_orbit_hessian_matrix(out):
    assert out["four_coordinate_orbits"][3]["mass_hessian_numerator_27"]==[
        [12,6,-9,0],[6,12,0,-9],[-9,0,18,-9],[0,-9,-9,18]]
    assert out["extra_combined_forms"]["native_fourth_holonomy_H27_average_hessian_determinant"]=="1/81"

def test_exact_e1_orbit_hessian_matrix(out):
    assert out["four_coordinate_orbits"][0]["mass_hessian_numerator_27"]==[
        [18,9,0,0],[9,18,0,0],[0,0,0,0],[0,0,0,0]]

def test_generalized_eigenvalues_are_two_doublets(out):
    eig=out["four_coordinate_orbits"][3]["generalized_mass_squared_eigenvalues"]
    assert eig=={"1/9":2,"2/27":2}
    assert out["four_coordinate_orbits"][0]["generalized_mass_squared_eigenvalues"]=={"0":2,"2/9":2}

def test_two_exact_real_character_projectors(out):
    import sympy as sym
    P=[sym.Matrix([[sym.Rational(y) for y in row] for row in x]) for x in out["real_character_plane_projectors"]]
    G=sym.Matrix([[sym.Rational(y) for y in row] for row in out["electric_metric_G"]])
    assert sum(P,sym.zeros(4))==sym.eye(4)
    assert P[0]*P[1]==sym.zeros(4)
    assert all(p*p==p and p.rank()==2 and p.T*G==G*p for p in P)

def test_h27_full_orbit_not_an_isolated_fourth_scalar(out):
    assert "never rank 1 or 3" in out["proof_rank"]
    assert "supplied equal-period" in out["physical_limit"]
    assert "might break H27" in out["physical_limit"]
