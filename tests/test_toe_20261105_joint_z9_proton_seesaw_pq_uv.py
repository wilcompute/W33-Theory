"""Independent replays of Z9 proton + seesaw + axion-quality + gauge UV cost.

Uses exactly source modules, recomputes JSON rather than trusting
certificates. The physics claimed is classical/algebraic and established
in prior literature; the new point is the cross-sector minimality test.
"""
from __future__ import annotations
import importlib,json,math,sys
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
@pytest.fixture(scope="module")
def data():
    a=importlib.import_module("toe_20261105_joint_flavor_u1_z9_seesaw_scalar_quality").main()
    b=importlib.import_module("toe_20261105_joint_flavor_u1_uv_coupling_cost").main()
    return a,b
def test_full_fermion_anomaly_cancel(data):
    a,b=data
    assert all(s=="0" for s in a["SM_three_family_polynomial_anomaly_tests"].values())
    assert len(a["SM_three_family_polynomial_anomaly_tests"])==6
    assert a["chiral_field_rows"]==18

def test_exact_discrete_after_two_vevs(data):
    a,_=data
    assert math.gcd(abs(a["scalar_X_charges"]["T"]),abs(a["scalar_X_charges"]["S"]))==9
    assert a["unbroken_discrete_gauge_group"]=="Z_9"

def test_family_nonuniversal_fixes_qqql(data):
    a,_=data
    x=a["proton_operators"]
    assert len(x)==3
    assert [z["lepton_charge"] for z in x]==[-9,0,0]
    assert [z["proton_decay_operator_X_charges"]["QQQL"] for z in x]==[-6,3,3]
    assert all(all(v%9 for v in z["proton_decay_operator_X_charges"].values()) for z in x)

def test_universal_generation_SU2_anomaly_proton_no_go(data):
    a,_=data
    z=a["generation_universal_no_go"]
    assert z["QQQL_X_charge_after_anomaly_cancellation"]=="0"
    assert z["if_only_SM_doublets_and_generation_universal_X_no_proton_selection"]

def test_seesaw_dirac_renormalizable_block_texture(data):
    a,_=data
    tex=a["generic_seesaw_renormalizable_textures"]
    assert tex["Ynu_renormalizable_allowed_3x3"]==[
       [True,False,False],[False,True,True],[False,True,True]]
    assert tex["Majorana_renormalizable_sources"]["00"]=="S"
    assert tex["Majorana_renormalizable_sources"]["01"]=="T"
    assert tex["Majorana_renormalizable_sources"]["12"]=="bare"

def test_neutrino_light_mass_fullrank_and_mixed(data):
    a,_=data
    z=a["generic_seesaw_renormalizable_textures"]
    M=np.array(z["light_mass_matrix"])
    assert z["light_mass_matrix_rank"]==3
    assert np.linalg.det(M)!=0
    assert abs(M[0,1])>1e-5 and abs(M[0,2])>1e-5
    assert np.max(abs(M-M.T))<1e-12
    assert z["not_a_mass_fit_or_PMNS_prediction"]

def test_cubic_scalar_pq_quality_failure(data):
    a,_=data
    s=a["scalar_phase_quality"]
    assert s["lowest_gauge_invariant_phase_sensitive_scalar_dimension"]==3
    assert {"T":2,"Tdag":0,"S":0,"Sdag":1} in s["primitive_degree3_monoms"]
    assert s["cannot_claim_PQ_quality_or_light_QCD_axion_from_this_scalar_inventory"]
    # Direct charge check: 2*(-9)+(+18)=0.
    assert 2*a["scalar_X_charges"]["T"]-a["scalar_X_charges"]["S"]==0

def test_cubic_breaks_relative_physical_phase_not_gauge_phase(data):
    a,_=data
    qT=a["scalar_X_charges"]["T"];qS=a["scalar_X_charges"]["S"]
    angleT=.3;angleS=.7;alpha=.153
    before=2*angleT-angleS
    after=2*(angleT+qT*alpha)-(angleS+qS*alpha)
    assert after==pytest.approx(before,abs=1e-12)
    # Relative shift alone changes this invariant and the potential.
    assert abs(math.cos(before)-math.cos(before+.1))>.001

def test_mixed_kinetic_matrix_beta_large_and_positive(data):
    _,b=data
    B=np.array(b["full_B_above_vectorlike_threshold"])
    assert B[0,1]==pytest.approx(52/3)
    assert B[1,1]==pytest.approx(383)
    assert B[0,0]==pytest.approx(127/18)
    assert min(np.linalg.eigvalsh(B))>0

def test_uv_pressure_and_counterexample_weak_coupling(data):
    _,b=data
    assert b["KXX_positive_necessary_coupling_upper_bound_at_initial_scale"]==pytest.approx(.132245228525,rel=1e-9)
    x=b["initial_X_coupling_scan"]
    assert x[1]["gX_at_1e10_GeV"]==.05 and x[1]["Kmatrix_positive_at_UV"]
    assert x[-1]["gX_at_1e10_GeV"]==.2 and not x[-1]["Kmatrix_positive_at_UV"]
    assert not x[-2]["Kmatrix_positive_at_UV"]

def test_charge_basis_covariance(data):
    _,b=data
    assert max(b["change_of_gauge_basis_invariant_current_errors"])<1e-11
    assert b["charge_normalization"].startswith("X=3(B-3Le)")

def test_independently_regenerated_certificates(data):
    for src,file in zip(data,[
     "toe_20261105_new_joint_symmetry_z9_seesaw_pq_obstruction.json",
     "toe_20261105_new_joint_flavor_u1_uv_gauge_cost.json"]):
        parsed=json.loads((ROOT/"data"/file).read_text(encoding="utf8"))
        assert parsed==json.loads(json.dumps(src))

def test_cubic_naturalness_threshold_is_extremely_tuned_if_asked_for_axion(data):
    a,_=data
    r=a["scalar_phase_quality"]["conditional_QCD_quality_example"]
    assert r["relative_phase_canonical_decay_constant_GeV"]==pytest.approx(1e11/math.sqrt(5),rel=1e-14)
    assert r["conditional_sufficient_phase_uniform_max_abs_cubic_coefficient_GeV"]==pytest.approx(4.619576674796773e-48,rel=1e-12)
    assert r["relative_phase_mass_if_cubic_coefficient_equals_vT_GeV"]>1e11
    assert "no axion solution" in r["critical_warning"]
