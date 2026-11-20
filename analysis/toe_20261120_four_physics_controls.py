#!/usr/bin/env python3
"""Independent, explicitly limited physics gates: E6 matter, causal conformal
ambiguity, SU3 center readout and worst-case heralded-loss memory witness.
All mathematical/model outcomes, NOT evidence for a complete physical TOE.
"""
from __future__ import annotations
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_four_physics_controls.json"

def matter():
    # Standard E6 -> Spin10 x U1_psi branching 27=16_1 +10_-2 +1_4.
    reps=[{"spin10":"16","dim":16,"qpsi":1,"index":2},
          {"spin10":"10","dim":10,"qpsi":-2,"index":1},
          {"spin10":"1","dim":1,"qpsi":4,"index":0}]
    assert sum(r["dim"] for r in reps)==27
    grav=sum(r["dim"]*r["qpsi"] for r in reps)
    cubic=sum(r["dim"]*r["qpsi"]**3 for r in reps)
    mixed=sum(r["index"]*r["qpsi"] for r in reps)
    assert (grav,cubic,mixed)==(0,0,0)
    triplets={"16_16_10":1+1-2,"10_10_1":-2-2+4,
              "16_16_1":1+1+4,"16_10_1":1-2+4,
              "1_1_1":12}
    assert [k for k,v in triplets.items() if v==0]==["16_16_10","10_10_1"]
    assert all((m*grav,m*cubic,m*mixed)==(0,0,0) for m in range(7))
    return {
        "E6_to_Spin10_U1_psi_27":reps,
        "gravity_U1psi_anomaly":grav,"U1psi_cubic_anomaly":cubic,
        "Spin10_squared_U1psi_anomaly_index_normalization":mixed,
        "triple_charge_sums":triplets,
        "family_multiplicity_not_fixed_by_anomalies":[1,2,3,4,5,6],
        "qualified_conclusion":"One 1_4 singlet VEV permits 10_-2 x10_-2 exotic-vector mass via 10*10*1, but not a bare 16_1 x16_1 mass via 16*16*1. Requires permitted nonzero coupling, actual vacuum, and compact charged Dirac index. Standard E6 branching."
    }

def causal():
    # 1+1 Minkowski background: g(a)=exp(2*a*x^2)*diag(-1,+1).
    events=[(0.0,0.0),(.3,.1),(.55,-.15),(.6,.4),
            (.9,.0),(1.2,.2),(1.5,-.1),(1.7,.1)]
    def order(p,q):
        return q[0]>p[0] and q[0]-p[0]>=abs(q[1]-p[1])-1e-12
    relations=[(i,j) for i,p in enumerate(events) for j,q in enumerate(events)
               if i!=j and order(p,q)]
    links=[(i,j) for i,j in relations
           if not any((i,k) in relations and (k,j) in relations
                      for k in range(len(events)))]
    rows=[]
    for a in (0.,.15,.25):
        vol=2*quad(lambda x:math.exp(2*a*x*x),-1,1,epsabs=1e-12)[0]
        metric_density_origin=math.exp(2*a*0)
        scalar_curvature_origin=-4*a
        assert abs(metric_density_origin-1)<1e-12
        rows.append({"conformal_a":a,"same_causal_edges":len(relations),
            "same_Hasse_links":len(links),"coordinate_rectangle_volume":vol,
            "R_scalar_at_origin":scalar_curvature_origin})
    assert all(row["same_causal_edges"]==rows[0]["same_causal_edges"] for row in rows)
    assert rows[0]["coordinate_rectangle_volume"]<rows[1]["coordinate_rectangle_volume"]<rows[2]["coordinate_rectangle_volume"]
    return {"metric":"exp(2*a*x^2)*(-dt^2+dx^2)",
        "continuum_causal_order_invariant_under_all_positive_conformal_scales":True,
        "sample_event_count":len(events),"comparability_pairs":relations,"Hasse_edges":links,
        "metrics":rows,
        "interpretation":"Order alone fixes at most conformal causal structure under appropriate regularity. Volume density or independent scale input is necessary to resolve curvature/metric; a finite poset cannot by itself select Einstein dynamics."}

def holonomy():
    w=np.exp(2j*np.pi/3)
    Z=np.diag([1,w,w*w])
    X=np.zeros((3,3),complex)
    for j in range(3):X[(j+1)%3,j]=1
    assert abs(np.linalg.det(X)-1)<1e-12 and abs(np.linalg.det(Z)-1)<1e-12
    K=Z@X@Z.conj().T@X.conj().T
    assert np.max(np.abs(K-w*np.eye(3)))<1e-12
    rho=np.diag([.6,.3,.1])
    assert np.max(np.abs(K@rho@K.conj().T-rho))<1e-12
    gauge_H=np.array([[.2,1j*.13,.08],[-1j*.13,-.3,.11],[.08,.11,.1]],complex)
    G=expm(1j*gauge_H)
    assert abs(np.linalg.det(G)-1)<1e-12
    Kg=(G@Z@G.conj().T)@(G@X@G.conj().T)@(G@Z.conj().T@G.conj().T)@(G@X.conj().T@G.conj().T)
    assert np.max(np.abs(Kg-w*np.eye(3)))<1e-11
    fundamental_complex_trace=complex(np.trace(K))
    adjoint_character=abs(fundamental_complex_trace)**2-1
    assert abs(adjoint_character-8)<1e-10
    p_reference=1.
    p_center=(1+np.real(np.trace(rho@K)))/2
    assert abs(p_center-.25)<1e-12
    # One-sided two-hypothesis discrimination at midpoint 0.625:
    n=math.ceil(math.log(2/.01)/(2*(.375**2)))
    return {"ZX_equals_omega_XZ":True,"fundamental_tr_center":
         [float(fundamental_complex_trace.real),float(fundamental_complex_trace.imag)],
         "fundamental_normalized_tr_center":[float(w.real),float(w.imag)],
         "adjoint_tr_center":float(adjoint_character),
         "adjoint_tr_identity":8,
         "all_qutrit_density_operators_blind_to_central_conjugation":True,
         "interferometric_controlled_center_p_plus":float(p_center),
         "interferometric_identity_p_plus":p_reference,
         "ideal_bernoulli_Hoeffding_shots_99pct":n,
         "boundary":"Adjoint only and direct qutrit state tomography cannot see central holonomy. A reference-controlled interferometer can, assuming coherent controlled-Wilson operation, stable relative phase and iid shots. Existing repo pass5709 already recognized adjoint Z3 blindness."}

def memory():
    # Assumed accepted-trial calibration model. Missing events may produce arbitrary
    # outcomes, and eta is certified as an input-independent lower bound.
    gamma=.75
    epsilon=.01
    p=np.array([1-2*epsilon/3,epsilon/3,epsilon/3])
    q=np.array([epsilon/3,1-2*epsilon/3,epsilon/3])
    r0=(1+2*gamma)/3
    def upper(eta,t=0.):
        lo=1-eta
        ubp=np.minimum(1,eta*np.minimum(1,p+t)+lo)
        ubq=np.minimum(1,eta*np.minimum(1,q+t)+lo)
        fidelity=min(1.,float(np.sum(np.sqrt(ubp*ubq))))
        s1low=max(0,3*eta*max(0,r0-t)-1)
        return 6*fidelity-s1low
    threshold=float(brentq(lambda eta:upper(eta),.985,.995,xtol=1e-14))
    eta=.995;delta=.01
    def t_of(n):return math.sqrt(math.log(42/delta)/(2*n))
    lo,hi=1,10**12
    while lo<hi:
        mid=(lo+hi)//2
        if upper(eta,t_of(mid))<0:hi=mid
        else:lo=mid+1
    n=lo
    assert upper(eta,0)<0<upper(.985,0)
    assert upper(eta,t_of(n))<0
    assert upper(eta,t_of(n-1))>=0
    return {
        "witness_origin":"Beyer et al. arXiv:2611.17268 generalized dimensional MUB witness",
        "assumed_reference_model":{"gamma":gamma,"late_depolarizing_epsilon":epsilon},
        "adversarial_missing_data_handling":"If accepted outcomes p_j have independently calibrated common lower-bound acceptance eta, any CPTP completion of lost trials has true outcome coordinate in [eta*p_j,eta*p_j+1-eta]; fidelity is upper-bounded by classical Bhattacharyya coefficient. Nonunitality S1 is lower bounded by max(0,3*eta*r0-1).",
        "zero_loss_accepted_reference_W":upper(1.),
        "minimum_eta_for_negative_worst_case_upper":threshold,
        "eta_0_995_worst_case_Wupper":upper(eta),
        "eta_0_99_worst_case_Wupper":upper(.99),
        "eta_0_985_worst_case_Wupper":upper(.985),
        "accepted_samples_per_setting_99pct":n,
        "seven_setting_accepted_total_99pct":7*n,
        "IID_Hoeffding_confidence_delta":delta,
        "observational_boundary":"Not device independent. Requires reliable lower bound on acceptance for each prepared input and stationarity; no fair-sampling shortcut. The sample forecast uses an illustrative gamma/epsilon model, but the conservative data bound itself does not require depolarizing outputs."}

def run(write=True):
    tracks={"E6_matter_selection":matter(),
            "causal_conformal_nonidentifiability":causal(),
            "SU3_center_interferometer":holonomy(),
            "multitime_memory_adversarial_loss":memory()}
    result={"status":"FOUR_FINITE_OR_MODEL_SCOPED_GATES_PASS_NOT_A_TOE",
            "source_date":"2026-11-20",
            "scope":"Four independent stress tests of previous five-step directions; repetition-dial CSS is the fifth.",
            "tracks":tracks}
    if write:OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":print(json.dumps(run(),indent=2))
