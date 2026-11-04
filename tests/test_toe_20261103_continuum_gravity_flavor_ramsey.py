"""Regression checks for continuum, gravitational, flavor, and Ramsey falsifiers."""
from pathlib import Path
import importlib.util
import math
import pytest

ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("fronts",ROOT/"analysis"/"toe_20261103_continuum_gravity_flavor_ramsey.py")
mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)

@pytest.fixture(scope="module")
def r():
    return mod.main()

def test_refinement_keeps_topology_but_not_dimension(r):
    records=r["continuum"]["subdivision"]
    assert [a["subdivision_length"] for a in records]==[1,2,3,4,6,8,16,32]
    assert all(a["betti1"]==81 for a in records)
    assert all(a["edges"]-a["vertices"]+1==81 for a in records)
    predicted=r["continuum"]["metric_graph_predicted_first_eigenvalue"]
    assert math.isclose(predicted,0.8312667112181387,rel_tol=1e-10)
    assert abs(records[-1]["rescaled_gap"]-predicted)<.014

def test_4d_null_control_is_imposed(r):
    row=r["continuum"]["imposed_4torus_times_W33_heat"][-1]
    assert 4.0<row["product_spectral_dimension"]<4.02
    assert row["w33_internal"]<1e-20

def test_local_gauss_is_not_gravity_constraint_closure(r):
    row=r["gravity"]
    assert row["Gauss_zero"]
    assert row["overlap"]==1 and abs(row["signed_intersection"])==1
    assert abs(row["poisson_bracket_at_gauss_zero"])==7

def test_one_spurion_fails_and_two_spurions_allow_cp(r):
    row=r["flavor"]
    assert row["one_27_contains_one_SU5_chiral_generation_plus_vectorlike_5_5bar"]
    assert row["single_flavor_spurion_proportional_Yu_Yd_CP_invariant"]==0
    assert row["exact_two_spurion_CP_trace"]=="-97200"

def test_ramsey_flux_detection_with_probability_blindness(r):
    rows=r["hardware"]["Ramsey_reference_phase_contrast"]
    assert all(a["site_probability_max_gap"]<1e-14 for a in rows)
    assert math.isclose(rows[1]["coherent_reference_imaginary_contrast"],0.04098706247851882,rel_tol=1e-12)
    assert r["hardware"]["cubed_return_matrix_difference_exact"]=="4"
    assert r["hardware"]["contrast_positive_fraction"]==1.0
    assert r["hardware"]["contrast_minimum"]>0.037
    assert r["hardware"]["robust_perturbation_sample_size"]==500
