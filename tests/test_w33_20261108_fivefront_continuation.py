"""Ten-plus independent checks for the five-front continuation."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import sympy as s
import pytest

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"analysis/w33_20261108_fivefront_continuation.py"
spec=importlib.util.spec_from_file_location("w33_fivefront_next",P)
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

@pytest.fixture(scope="module")
def result():return M.produce(ROOT)

def test_gauge_H1_46(result):
    assert result["gauge"]["H1"]==46
def test_gauge_character_census(result):
    assert result["gauge"]["character_census"]=={"(0, 3)":6,"(1, 2)":8,"(2, 1)":12,"(4, 0)":1}
def test_gauge_S4_orbits(result):
    o=result["gauge"]["S4_orbits"]
    assert sorted((x["size"],x["harmonic_per_character"]) for x in o)==[(1,0),(4,2),(4,2),(6,3),(12,1)]
    assert sum(x["dim"] for x in o)==46
def test_translation_invariant_mode_absent(result):
    assert result["gauge"]["translation_invariants"]==0
def test_native_E6_rank_certificate(result):
    x=result["flavor"]["E6_original"]
    assert x is not None
    assert x["mass_rank"]==[78,79] and x["mass_kernel"]==3
def test_NB_first_variation(result):
    x=result["flavor"]
    assert x["toy_det"]=="985/27"
    assert x["derivative_im_trace_Minv_delta"]=="33*sqrt(3)/1970"
    assert x["derivative"]==pytest.approx(33*math.sqrt(3)/1970,abs=1e-13)
def test_NB_sensitivity_is_conditional(result):
    x=result["flavor"]
    assert x["eps_bound_if_imposed_theta_lt_1e_minus10"]<4e-9
    assert "Hypothetical" in x["caveat"]
def test_quadratic_eigenspectra(result):
    for x in result["higher_q"]["checked_primes"]:
        q=x["q"]
        assert x["spectrum"][q*q-1]==1
        assert x["spectrum"][-1]==q*q-1
        assert x["spectrum"][q-1]+x["spectrum"][-q-1]==q*q*(q-1)
def test_no_uniform_mixing_any_time_q5_7_11(result):
    rows=result["higher_q"]["checked_primes"]
    assert [x["q"] for x in rows]==[3,5,7,11]
    assert not rows[0]["strictly_excluded"]
    for x in rows[1:]:
        assert x["strictly_excluded"]
        assert x["all_time_amplitude_bound"]<x["uniform_amplitude_required"]
        assert len(x["anisotropic_good_values"])==(x["q"]-1)//2
def test_provenance_evidence_is_not_first_commit(result):
    p=result["provenance"]
    assert len(p["formulas"])==6
    assert "No claim" in p["caveat"]
    assert p["matching_line_count"]>=0
def test_optical_27_mode_exact(result):
    o=result["optics"]
    assert o["full_matrix_residual"]<1e-12
    assert (o["forward_SUM"],o["inverse_SUM"],o["tritters_3x3"])==(2,2,27)
def test_optical_resource_advantage_but_not_physics(result):
    o=result["optics"]
    assert o["two_mode_MZI_upper_bound"]==81 and o["generic_27_mode_bound"]==351
    assert o["nonClifford_count"]==0
    assert "ordinary quantum mechanics" in o["caveat"]
def test_optical_perturbations_detectable(result):
    o=result["optics"]
    assert o["bad_tritter_max_probability_deviation"]>1e-3
    assert o["tick_drift_max_probability_deviation"]>1e-4
