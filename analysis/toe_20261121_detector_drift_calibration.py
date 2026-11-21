"""Witting 24D chart tomography under heterogeneous efficiencies and temporal drift.

128 seeded multinomial trials per budget/layout, with no-click events retained.
Separates finite-shot stochastic error from systematic reference-target drift.
Provides exact local worst-case drift amplification from singular values of
the 24 resolved-ray response. This is not a CR-efficient joint MLE.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
import toe_20261121_relational_reference_pareto as source
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261121_detector_drift_calibration.json"
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]

def main():
    rays,H,A,(P1,P20,P24)=source.geometry()
    _,V=np.linalg.eigh(P24)
    V=V[:,-24:]
    D=(H.T@V)/8
    rng=np.random.default_rng(20261121)
    eta=rng.uniform(.65,.85,40)
    coeff=rng.normal(size=24)
    hidden=V@coeff
    hidden*=.003/np.linalg.norm(hidden)
    chart_w=np.full(45,1/45)+hidden
    assert min(chart_w)>0
    ideal=H.T@chart_w/8
    pref=eta/40
    ptarg=eta*ideal

    # Common drift patterns for comparable layouts
    drift_cases={}
    for d in (0,.001,.0025,.005,.01):
        draw=rng.normal(size=40)
        draw*=d/np.sqrt(np.mean(draw**2)) if d else 0.
        drift_cases[str(d)]=draw

    def estimate(labels,p0,p1):
        # Uses 24 individual ray ratios; for the full40 uses a least-squares
        # inverse. The 25-bin pooled label and no-click are observed but
        # do not enter this simple, not-statistically-optimal inverse.
        t=p1[labels]/(40*p0[labels])
        return V@np.linalg.lstsq(D[labels],t-1/40,rcond=None)[0]

    layouts=[]
    for name,labels in (("older_25",OLD),("newer_25",NEW),("full_40",list(range(40)))):
        responses=D[labels]
        singular=np.linalg.svd(responses,compute_uv=False)
        assert singular[-1]>1e-10
        drift_gain=math.sqrt(len(labels))/(40*singular[-1])
        shots=[]
        for N in (200_000,2_000_000,20_000_000):
            errors=[]
            for trial in range(128):
                ref=rng.multinomial(N,np.r_[pref,1-pref.sum()])[:40]/N
                target=rng.multinomial(N,np.r_[ptarg,1-ptarg.sum()])[:40]/N
                est=estimate(labels,ref,target)
                errors.append(float(np.linalg.norm(est-hidden)))
            shots.append({"reference_launches":N,"target_launches":N,
               "trials":128,"empirical_RMS_hidden_vector_error":float(np.sqrt(np.mean(np.square(errors))))})
        drifts=[]
        for label,delta in drift_cases.items():
            shifted=eta*(1+delta)*ideal
            assert shifted.sum()<1
            drifts.append({"RMS_fractional_efficiency_drift":float(label),
                "infinite_shot_bias_norm":float(np.linalg.norm(estimate(labels,pref,shifted)-hidden))})
        layouts.append({"name":name,"response_condition_number":float(singular[0]/singular[-1]),
           "worst_hidden_bias_gain_per_unit_RMS_fractional_drift_among_resolved_labels":drift_gain,
           "worst_hidden_bias_for_0p5pct_RMS_drift":drift_gain*.005,
           "finite_shot_simulation":shots,"stable_reference_target_drift":drifts})
    assert abs(layouts[0]["worst_hidden_bias_for_0p5pct_RMS_drift"]-.005063)<2e-5
    assert abs(layouts[1]["worst_hidden_bias_for_0p5pct_RMS_drift"]-.005987)<2e-5
    assert abs(layouts[2]["worst_hidden_bias_for_0p5pct_RMS_drift"]-.001826)<2e-5
    assert layouts[1]["worst_hidden_bias_for_0p5pct_RMS_drift"]>layouts[0]["worst_hidden_bias_for_0p5pct_RMS_drift"]
    record={"status":"PASS","date":"2026-11-21",
       "chart_hidden_signal_l2":float(np.linalg.norm(hidden)),
       "true_reference_detector_efficiency_min_max":[float(min(eta)),float(max(eta))],
       "all_40_raw_efficiencies_are_heterogeneous":True,
       "layouts":layouts,
       "worst_drift_formula":"sqrt(number_resolved)/(40*sigma_min(H_resolved.T*U24/8)) * RMS_fractional_detector_drift",
       "scope":"Finite-shot ratio-decoder simulations; this inverse is NOT profile-MLE or Cramer-Rao efficient and does NOT use aggregate pooled bin/no-click to improve estimation. Stable gain calibration alone cannot cancel unknown target-reference drift."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    print("PASS detector drift stress; new 25 nominal A gain can mean worse minimax drift bias")
    return record

if __name__=="__main__":main()
