#!/usr/bin/env python3
"""Calibration-interval, finite-shot CCNR witness for the Horodecki family.

Ideal 10/11/12-setting W33/Q8 measurements; conditional accepted-detection
proportions; synthetic expected probabilities, NOT a performed experiment.
The fixed dual witness is valid even when chosen from the same data, because
the simultaneous probability intervals cover all 9*K unknown probabilities.
"""
import json, math, sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from w33_20261109_q8_ten_context_tomography import (
    select, projection_design, random_unitary
)
from w33_20261109_q8_12setting_completion import product_mub
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_horodecki_ccnr_exact import realign
from w33_20261109_q8_correlation_five import probabilities

def all_frames():
    ten,(Bell,U,V,ops,_)=select(return_components=True)
    bases10=[Bell[:,9*i:9*(i+1)] for i in range(8)]+[U,V]
    rng=np.random.default_rng(2026110944)
    best=None
    m10=np.vstack([projection_design(B,ops) for B in bases10])
    for ix in range(300):
        Q=random_unitary(rng)
        mat=np.vstack([m10,projection_design(Q,ops)])
        s=np.linalg.svd(mat,compute_uv=False)
        score=float(s[0]/s[-1])
        if best is None or score<best[0]:best=(score,Q,ix)
    assert best[0]<10
    product,_=product_mub()
    bases12=[*bases10[:8]]+[np.kron(U3,U3) for U3 in product]
    return {10:bases10,11:[*bases10,best[1]],12:bases12},ops,best[2]

def solve_basis_lp(c,q,lo,hi,eps):
    """Min c·p. Relax common PSD quantum state; constraints linear."""
    Aub=[];bub=[]
    for j in range(9):
        r=np.zeros(19);r[j]=-hi[j];r[9+j]=1;Aub.append(r);bub.append(0)
        r=np.zeros(19);r[j]=lo[j];r[9+j]=-1;Aub.append(r);bub.append(0)
        r=np.zeros(19);r[9+j]=1;r[18]=-min(1,q[j]+eps);Aub.append(r);bub.append(0)
        r=np.zeros(19);r[9+j]=-1;r[18]=max(0,q[j]-eps);Aub.append(r);bub.append(0)
    eq=np.zeros((2,19));eq[0,:9]=1;eq[1,9:18]=1;eq[1,18]=-1
    bounds=[(0,1)]*9+[(0,float(max(hi)))]*9+[(float(min(lo)),float(max(hi)))]
    sol=linprog(np.r_[c,np.zeros(10)],A_ub=np.array(Aub),b_ub=bub,
                A_eq=eq,b_eq=[1,0],bounds=bounds,method="highs")
    assert sol.success,sol.message
    return float(sol.fun)

def design_test(K,bases,ops,a=.236,relative_eff_uncertainty=.001):
    M=np.vstack([projection_design(B,ops) for B in bases])
    s=np.linalg.svd(M,compute_uv=False)
    condition=float(s[0]/s[-1])
    assert len(s)==80 and s[-1]>1e-7
    pinv=np.linalg.pinv(M,rcond=1e-13)
    rho=horodecki_state(a)
    R=realign(rho)
    u,_,vh=np.linalg.svd(R)
    W=u@vh
    assert np.linalg.norm(W,ord=2)<1+1e-12
    coeff=np.array([float(np.vdot(W,realign(h)).real) for h in ops])
    const=float(np.vdot(W,realign(np.eye(9)/9)).real)
    c=coeff@pinv
    truth=float(np.linalg.svd(R,compute_uv=False).sum())
    ideal=np.concatenate([probabilities(B,rho) for B in bases])
    est=const+float(c@(ideal-1/9))
    assert abs(est-truth)<3e-12,(K,est,truth)
    # Known outcome-dependent efficiency, outcome index j same calibration
    # envelope in all settings for this toy benchmark.
    eff=np.array([.63+.045*j for j in range(9)])
    lo=eff*(1-relative_eff_uncertainty)
    hi=eff*(1+relative_eff_uncertainty)
    q=np.array([ideal[9*i:9*(i+1)]*eff for i in range(K)])
    q=q/q.sum(axis=1)[:,None]
    # Model-free interval-radius bound for ideal full click detection.
    pilot_centered_c=np.array([c[9*i:9*(i+1)]-np.median(c[9*i:9*(i+1)])
                               for i in range(K)])
    coeff_l1=float(sum(np.sum(abs(v)) for v in pilot_centered_c))
    sample=[]
    for N in (100000,1000000,10000000,100000000,1000000000,10000000000):
        rad=math.sqrt(math.log(2*9*K/.05)/(2*N))
        lower=const+sum(solve_basis_lp(c[9*i:9*(i+1)],q[i],lo,hi,rad)
                        for i in range(K))-float(c.sum())/9
        # Optimistic expected counts, not finite Monte Carlo.
        no_loss_exact_minus_radius=truth-rad*coeff_l1
        sample.append({"accepted_shots_per_basis":N,
            "accepted_total":N*K,"simultaneous_95pct_Hoeffding_radius":rad,
            "calibrated_LP_lower":float(lower),
            "LP_certifies_entangled_on_expected_frequencies":bool(lower>1+1e-9),
            "perfect_efficiency_expected_rectangle_lower":no_loss_exact_minus_radius,
            "perfect_efficiency_certifies":bool(no_loss_exact_minus_radius>1)})
    return {"settings":K,"frame_rank":80,"min_singular":float(s[-1]),
            "condition":condition,"Horodecki_a":a,
            "true_realignment_norm":truth,
            "CCNR_excess":truth-1,
            "LP_efficiency_relative_envelope":relative_eff_uncertainty,
            "sample_count_sweep":sample,
            "coefficient_centered_l1":coeff_l1,
            "uncertainty_scope":"Conservative for IID accepted multinomial counts conditional on independent trusted efficiency intervals; no dark counts, crosstalk, preparation drift, calibration uncertainty beyond envelope, or adversarial detection selection.",
            "reporting_scope":"Observed q_j replaced by EXACT EXPECTED q_j for design-point resource estimation. A listed 95pct Hoeffding interval is a prospective coverage construction, NOT an observed 95pct successful experiment."}

def main(path=None):
    designs,ops,idx=all_frames()
    # 10,11,12 all from reproducible components. Test the a=0.236 hardest
    # interior witness and a=0.5 comparative control.
    tests={str(k):[design_test(k,bs,ops,a) for a in (.236,.5)]
           for k,bs in designs.items()}
    from w33_20261109_q8_ten_context_optimize import main as refined_frame
    _,(B,U,V,op)=refined_frame(return_components=True)
    refined_basis=[B[:,9*j:9*(j+1)] for j in range(8)]+[U,V]
    refined_tests=[design_test(10,refined_basis,op,a) for a in (.236,.5)]
    out={"status":"PASS_FINITE_SHOT_LOSS_AWARE_CCNR_PPT_SYNTHETIC_GATE",
         "best_eleventh_basis_candidate_index":idx,
         "tests":tests,
         "refined_ten_settings":refined_tests,
         "source":"known W33 Q8 eight-context Bell design; full tomography completed by 2/3/4 extra bases",
         "not_real_experiment":True}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS CCNR loss intervals",json.dumps({
      k:[{"a":u["Horodecki_a"],"margin":u["CCNR_excess"],
          "N_first_certificate":next((v["accepted_shots_per_basis"] for v in u["sample_count_sweep"]
                                     if v["LP_certifies_entangled_on_expected_frequencies"]),None)}
         for u in tests[k]]
      for k in tests}))
    return out

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
