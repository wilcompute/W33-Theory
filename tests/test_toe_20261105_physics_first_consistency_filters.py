"""Independent physics-first TOE consistency checks, runnable without repo conftest."""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261105_physics_first_consistency_filters as p

@pytest.fixture(scope="module")
def result():return p.main()

def test_qutrit_or_W33_not_necessary(result):
    assert result["status"]=="PASS_FIVE_INDEPENDENT_TOE_CONSISTENCY_FRONTS"
    assert all(k not in str(result.keys()).lower() for k in ("w33","h27","e8"))

def test_hypercharge_with_N_two_free_parameters(result):
    a=result["anomaly_and_hypercharge"]
    assert a["one_generation_anomaly_free_integer_grid_cases"]==49
    assert a["no_unique_hypercharge_with_N_without_extra_input"]
    assert a["Witten_anomaly_cancelled"]
    assert a["SU2_doublets"]==4

def test_hypercharge_neutrino_removed_breaks_family(result):
    a=result["anomaly_and_hypercharge"]
    assert a["without_N_gravity_anomaly"]=="h - 3*q"
    from sympy import sympify,symbols,expand
    q,h=symbols("q h")
    assert expand(sympify(a["without_N_cubic_anomaly"])-(h-3*q)**3)==0

def test_one_generation_sm_charge_basis(result):
    a=result["anomaly_and_hypercharge"]
    assert a["SM_Y_basis"]==["1/6","-2/3","1/3","-1/2","1","0"]
    assert a["BL_basis"]==["1/3","-1/3","-1/3","-1","1","1"]

def test_minimal_five_chiral_charge_certificate(result):
    a=result["minimal_chiral_u1"]
    assert a["primitive_chiral_five_fermion_solutions_maxabs_le9"]==[(-9,-5,-1,7,8)]
    assert sum([-9,-5,-1,7,8])==0
    assert sum(x**3 for x in (-9,-5,-1,7,8))==0

@pytest.mark.parametrize("dimension,expected",[(2,.5),(3,8/35),(4,.1)])
def test_myrheim_meyer_recovery(result,dimension,expected):
    row=next(x for x in result["causal_set_dimension"]["data"] if x["dimension_input"]==dimension)
    assert row["predicted_order_fraction"]==pytest.approx(expected,abs=1e-13)
    assert abs(row["reconstructed_dimension_from_mean"]-dimension)<.16
    assert row["replicates"]==16

def test_one_photon_does_not_give_two_local_clicks(result):
    x=result["one_photon_locality"]
    assert x["number_conserved_one_excitation"]==1
    assert x["A_occupancy"]+x["B_occupancy"]==pytest.approx(1,abs=1e-13)
    assert x["A_and_B_coincidence"]==0
    assert x["two_excitation_A_and_B_coincidence"]==1

def test_locality_does_not_force_universal_c(result):
    s=result["universal_speed_guard"]["species"]
    assert s[0]["group_speed_at_k_2pi_over19"]==pytest.approx(1,abs=4e-5)
    assert s[1]["group_speed_at_k_2pi_over19"]==pytest.approx(1.2,abs=4e-5)

def test_sm_one_loop_couplings_do_not_unify(result):
    x=result["gauge_running_nonunification"]
    c=x["pairwise_crossings"]
    assert len(c)==3 and x["no_one_loop_triple_unification"]
    assert c[0]["crossing_GeV"]==pytest.approx(1.0317136647571e13,rel=1e-8)
    assert c[1]["crossing_GeV"]==pytest.approx(2.43264314534e14,rel=1e-8)
    assert c[2]["crossing_GeV"]==pytest.approx(9.72517562388e16,rel=1e-8)
    assert all(v["remaining_inverse_coupling_mismatch"]>3 for v in c)

def test_replay_written_certificate_is_consistent(result):
    x=json.loads((ROOT/"data/toe_20261105_physics_first_consistency_filters.json").read_text())
    assert x==json.loads(json.dumps(result))
