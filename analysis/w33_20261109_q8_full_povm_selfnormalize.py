#!/usr/bin/env python3
"""Correct simulated optical-loss CCNR false positives using full calibrated POVMs.

All 10 contexts need known effects E_{bj}=K_b^dag|j><j|K_b; with
postselected q_{bj}=p_click_{bj}/s_b, the unknown positive s_b may be
included as ten extra linear variables. 90 observed q values then solve
a 90x90 real system for 80 traceless rho components and 10 s_b factors.
This is a detector-calibrated toy model, not device-independent.
"""
import json,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_optical_loss_povm import givens_network
from w33_20261109_q8_ten_context_optimize import main as optimize
from w33_20261109_q8_horodecki_ccnr_exact import realign
from w33_20261109_q8_five_extensions import horodecki_state

def effects_design(K,ops):
    A=np.einsum("ji,kil,jl->jk",K,ops,K.conj()).real
    b=np.sum(abs(K)**2,axis=1)/9
    return A,b

def calibrated_inverse(B,U,V,ops,t,phase,rng):
    mats=[B[:,9*i:9*(i+1)].conj().T for i in range(8)]
    K1,_=givens_network(U,t,phase,rng)
    K2,_=givens_network(V,t,phase,rng)
    mats.extend([K1,K2])
    a=[];b=[]
    for K in mats:
        X,y=effects_design(K,ops)
        a.append(X);b.extend(y)
    A=np.vstack(a)
    baseline=np.array(b)
    return mats,A,baseline

def solve_conditional(mats,A,b,rho,ops):
    q=[];survival=[]
    for K in mats:
        v=np.diag(K@rho@K.conj().T).real
        si=float(sum(v))
        q.extend(v/si)
        survival.append(si)
    q=np.array(q)
    N=len(mats)
    Q=np.zeros((9*N,N))
    for k in range(N):Q[9*k:9*(k+1),k]=q[9*k:9*(k+1)]
    aug=np.column_stack((A,-Q))
    cond=float(np.linalg.cond(aug))
    assert np.linalg.matrix_rank(aug,tol=1e-9)==80+N
    params=np.linalg.solve(aug,-b)
    theta=params[:80]
    inferred_s=params[80:]
    restored=np.eye(9)/9+np.einsum("k,kij->ij",theta,ops)
    err=float(np.max(abs(restored-rho)))
    serr=float(max(abs(inferred_s-np.array(survival))))
    assert err<5e-10,(err,cond)
    assert serr<5e-10
    return {"reconstruction_error":err,
            "inferred_survival_error":serr,
            "augmented_condition":cond,
            "min_inferred_click_survival":float(min(inferred_s)),
            "restored_CCNR":float(np.linalg.svd(realign(restored),compute_uv=False).sum()),
            "true_CCNR":float(np.linalg.svd(realign(rho),compute_uv=False).sum())}

def main(path=None):
    o,(B,U,V,ops)=optimize(return_components=True)
    rngstates=np.random.default_rng(20261109255)
    sources={"Horodecki_a0p236":horodecki_state(.236),
             "maximally_mixed":np.eye(9)/9}
    for i in range(12):
        x=rngstates.normal(size=3)+1j*rngstates.normal(size=3)
        y=rngstates.normal(size=3)+1j*rngstates.normal(size=3)
        x/=np.linalg.norm(x);y/=np.linalg.norm(y)
        psi=np.kron(x,y)
        sources[f"separable_{i}"]=np.outer(psi,psi.conj())
    rows=[]
    for t,phase in ((1.,0.),(.999,0.),(.995,0.),(.99,0.),(.995,.003)):
        mats,A,b=calibrated_inverse(B,U,V,ops,t,phase,
                            np.random.default_rng(2026110920))
        vals={k:solve_conditional(mats,A,b,rho,ops) for k,rho in sources.items()}
        maxerr=max(v["reconstruction_error"] for v in vals.values())
        false=sum(v["restored_CCNR"]>1+1e-7 for k,v in vals.items() if k.startswith("separable"))
        assert false==0 and maxerr<1e-9
        rows.append({"intensity_transmission_per_coupled_rail":t,
                     "phase_rms_rad":phase,
                     "max_corrected_rho_error":maxerr,
                     "corrected_false_positives":false,
                     "tested_product_states":12,
                     "worst_augmented_condition":max(v["augmented_condition"] for v in vals.values()),
                     "states":vals})
    out={"status":"PASS_FULL_POVM_SELF_NORMALIZING_CALIBRATED_Q8_CCNR_TOY",
         "10_contexts_with_90_conditional_probabilities":True,
         "80_unknown_traceless_state_components":True,
         "10_unknown_click_survival_factors":True,
         "normalization_augmented_system":"[A_effects, -blockdiag(q_basis)] @ [theta, s_0,...,s_9] = -b_effects; trace rho=1",
         "tested_loss_models":rows,
         "all_product_controls_correct_after_full_POVM_calibration":True,
         "hardware_limit":"Requires exact full POVM effects including internal noncommuting losses and drifts; no finite-shot confidence or POVM-calibration uncertainty included. Conditional click-rate normalization alone does not provide device-independence.",
         "novelty_scope":"Linear calibrated-POVM tomography is standard. This explicitly repairs the false positives of the repo's 10-setting Givens loss toy."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS calibrated POVM correction",[(r["intensity_transmission_per_coupled_rail"],
                                           r["corrected_false_positives"],
                                           r["max_corrected_rho_error"]) for r in rows])
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
