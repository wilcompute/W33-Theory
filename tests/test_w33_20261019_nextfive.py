"""Reproduction checks for five October 19 follow-up W33 frontiers."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))

def load(name):
    path=ROOT/"analysis"/(name+".py")
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module

def test_negative_coupling_global_full120():
    r=load("w33_20261019_nextfive_gaussian_phase").test()
    assert r["all_checks_pass"]
    assert len(r["numerical_all_120_search"])==3
    assert all(x["global_singleton_sufficient_kappa_min"] < 0 for x in r["temperatures"])
    assert abs(r["Gaussian_max_abs_energy_residual"])<1e-12

def test_controlled_optics_and_standard_su9_intertwiner():
    r=load("w33_20261019_nextfive_optics_su9").tracks()
    assert r["all_checks_pass"]
    a=r["optics"]
    assert abs(a["ideal_trace_deficit_theta_pi_2"]-8/27)<1e-12
    assert a["synthetic_noise"]["effective_visibility"]<1
    assert r["su9_clifford_bridge"]["max_equivariance_residual"]<1e-10

def test_paper_evidence_resolution_and_echo_census():
    import json
    load("w33_20261019_nextfive_evidence_prediction")
    r=json.loads((ROOT/"data"/"w33_20261019_nextfive_evidence_prediction.json").read_text())
    assert r["all_checks_pass"]
    assert r["post_classification"]=={
        "PATH_MATCH":2,"COMMIT_MATCH":19,"MANUAL_OR_EXTERNAL":2}
    assert r["operational_parameter_free_test"]["correctly_classified_ideal_pairs"]==780


def test_intrinsic_fourth_order_gibbs_incidence():
    import json
    load("w33_20261019_nextfive_quartic_incidence")
    r=json.loads((ROOT/"data"/"w33_20261019_nextfive_quartic_incidence.json").read_text())
    assert r["all_checks_pass"]
    assert abs(r["moments"]["4"]["difference"]-1/12)<1e-12
    assert all(row["commuting_preferred_free_energy_gap"]>0
               for row in r["temperature_comparison"])
