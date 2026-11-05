"""Recompute five TOE frontiers and two extra falsification controls.

Targeted:
  python -m pytest -q --noconftest tests/test_toe_20261105_nextfive_deeper.py

The fixture executes every producer again; stale saved JSON cannot pass tests.
"""
import importlib.util
import math
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
sys.path.insert(0,str(ROOT))

def execute(filename):
    path=ROOT/"analysis"/filename
    spec=importlib.util.spec_from_file_location(path.stem,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.main()

@pytest.fixture(scope="module")
def records():
    return {
      "s3":execute("toe_20261105_s3_exchange_mobile_obstruction.py"),
      "regge":execute("toe_20261105_regge_s4_nonlinear_hessian.py"),
      "optics":execute("toe_20261105_witting_memory_dual_frame.py"),
      "index":execute("toe_20261105_overlap_flux_chirality_index.py")
    }

def test_exact_27_exchange_even_odd_split(records):
    r=records["s3"]["27_exchange_obstruction"]
    assert r["rank_physical"]==27
    assert r["exchange_even"]==17 and r["exchange_odd"]==10
    assert r["exchange_trace_physical"]==7
    assert sum(r["burnside_trace_census"])==42

def test_no_full_Mat27_from_exchange_invariant_three_generators(records):
    r=records["s3"]["27_exchange_obstruction"]
    assert r["exchange_is_nontrivial_commutant_of_E_M_C"]
    assert r["exchange_even"] not in (0,27)

def test_parity_obstruction_is_conditional_not_universal(records):
    r=records["s3"]["27_exchange_obstruction"]
    assert r["gauge_invariant_loop_imbalance_breaks_exchange"]
    assert r["interparity_mixing_frobenius"]>1

def test_mobile_two_vertex_rank_changes(records):
    r=records["s3"]["mobile_two_vertex"]
    assert r["raw_reduced_dimension"]==144
    assert r["projected_dimension"]==18
    assert r["full_unfixed_raw_dimension"]==864
    assert r["full_unfixed_2vertex_projected_dimension_from_character"]==18
    assert sorted(r["Burnside_traces_sorted"])==[-18,-18,0,0,0,144]

def test_mobile_transport_gauss_and_nondynamical_scope(records):
    r=records["s3"]["mobile_two_vertex"]
    assert r["transport_covariant_and_noncommuting_with_electric"]
    assert all(x["gauss_max_residual"]<1e-11 for x in r["scans"])
    assert min(x["spectral_gap"] for x in r["scans"])>=-1e-10

def test_regge_closed_four_sphere_combinatorics(records):
    r=records["regge"]
    assert (r["edges"],r["triangle_hinges"],r["four_simplices"])==(15,20,6)
    assert abs(r["total_4_volume"]-math.sqrt(5)/16)<1e-12
    assert abs(r["regular_simplex_interior_dihedral"]-math.acos(.25))<1e-12

def test_regge_schlaefli_and_stationarity(records):
    r=records["regge"]
    assert r["max_schlaefli_gradient_mismatch"]<1e-7
    assert r["max_full_action_gradient_at_stationarity"]<2e-7

def test_regge_S6_hessian_1_5_9_no_gauge_zero(records):
    r=records["regge"]
    vals=r["hessian_eigenvalues"]
    assert len(vals)==15
    assert r["S6_edge_rep_irrep_multiplicities"]==[1,5,9]
    assert vals[0]<0<vals[1]
    assert r["hessian_min_abs_eigenvalue"]>5
    assert r["nonzero_linearized_gauge_modes"]==0
    assert max(vals[1:6])-min(vals[1:6])<.001
    assert max(vals[6:])-min(vals[6:])<.001

def test_local_ququart_dual_frame_Bell_witness(records):
    r=records["optics"]
    assert r["Witting_outcomes_per_site"]==40
    assert r["joint_outcome_count"]==1600
    assert abs(r["all_models"][2]["dual_estimator_mean"]-(1+8*.35)/9)<1e-12
    assert r["dual_weight_min"]<0<r["dual_weight_max"]

def test_Witting_local_readout_variance_penalty(records):
    r=records["optics"]
    assert r["all_models"][2]["Witting_vs_global_variance_ratio"]>6
    assert r["scaled_unconditional_variance_alt"]>2.6
    assert r["conservative_distribution_free_Hoeffding_shots_1pct_fpr_95pct_power"]>100000

def test_ideal_global_Bell_benchmark_not_assumed_hardware(records):
    r=records["optics"]
    g=r["ideal_global_entangling_Bell_measurement_binomial_benchmark"]
    assert g["shots"]<1000
    assert g["false_positive"]<=.01 and g["model_power"]>=.95
    assert r["joint_coincidence_efficiency"]==pytest.approx(.85**2)

def test_overlap_30_lattice_flux_index_tests(records):
    r=records["index"]
    assert len(r["records"])==30
    for x in r["records"]:
        expected=-x["topological_flux_Q"] if x["Wilson_regulator_mass"]<2 else x["topological_flux_Q"]
        assert x["index_minus_half_eta"]==expected

def test_overlap_ginsparg_wilson_finite_chirality(records):
    r=records["index"]
    selected=[x for x in r["records"] if "Ginsparg_Wilson_error" in x]
    assert len(selected)==6
    assert all(x["Ginsparg_Wilson_error"]<1e-12 for x in selected)
    assert all(x["minimum_abs_Wilson_eigenvalue"]>.1 for x in selected)

def test_chirality_selection_extra_input(records):
    r=records["index"]
    assert "neither sign of Q nor Wilson mass branch is selected" in r["limitation"]
    by={(z["L"],z["topological_flux_Q"],z["Wilson_regulator_mass"]):z["index_minus_half_eta"]
        for z in r["records"]}
    assert by[(6,1,1.)]==-1 and by[(6,1,2.5)]==1
    assert by[(6,-1,1.)]==1
