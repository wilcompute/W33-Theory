#!/usr/bin/env python3
"""Complete nine-mode POVM calibration with 81 trusted probe states.

Each basis analyzer K has 9 click effects E_j=K†|j><j|K and an explicit
no-click effect I-K†K. The 81 probe states |j>, (|j>+|k>)/sqrt2,
(|j>+i|k>)/sqrt2 invert linearly to every 9x9 Hermitian E_j.

This is a calibration protocol for TRUSTED probe states / pulses and
unconditional no-click observations. A separate trusted source count and
stationarity are indispensable; no device-independence is claimed.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from w33_20261109_full_povm_calibration_bound import make_model
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_horodecki_ccnr_exact import realign

def probes():
    n=9;basis=np.eye(n,dtype=complex)
    P=[basis[:,i] for i in range(n)]
    plus={};iphi={}
    for j in range(n):
        for k in range(j+1,n):
            plus[j,k]=len(P);P.append((basis[:,j]+basis[:,k])/np.sqrt(2))
            iphi[j,k]=len(P);P.append((basis[:,j]+1j*basis[:,k])/np.sqrt(2))
    return np.stack(P),plus,iphi

def effects_from_probs(q,plus,iphi):
    # q is 81x9 unconditional click fractions (NOT normalized on clicks).
    n=9;out=np.zeros((9,n,n),complex)
    for j in range(n):
        for detector in range(n):
            out[detector,j,j]=q[j,detector]
    for j in range(n):
        for k in range(j+1,n):
            for detector in range(n):
                mean=(q[j,detector]+q[k,detector])/2
                re=q[plus[j,k],detector]-mean
                im=mean-q[iphi[j,k],detector]
                out[detector,j,k]=re+1j*im
                out[detector,k,j]=re-1j*im
    return out

def physical_prob(K,psi):
    p=np.abs(psi@K.T)**2
    noclick=1-p.sum(axis=1)
    assert np.min(noclick)>-1e-11,(np.min(noclick),np.linalg.norm(K,2))
    return np.column_stack((p,np.maximum(noclick,0)))

def main(path=None):
    mats,_,_,_=make_model()
    states,plus,iphi=probes()
    assert states.shape==(81,9)
    true=np.array([np.stack([np.outer(K[j].conj(),K[j]) for j in range(9)]) for K in mats])
    ps=np.array([physical_prob(K,states) for K in mats])
    assert ps.shape==(10,81,10)
    recon=np.array([effects_from_probs(q[:,:9],plus,iphi) for q in ps])
    exacterr=float(max(np.linalg.norm((recon-true).reshape(-1,9,9),ord=2,axis=(-2,-1))))
    assert exacterr<1e-12
    rng=np.random.default_rng(20261109195)
    finite={}
    for N in (1000,100000,1000000):
        qhat=np.array([[rng.multinomial(N,p)/N for p in context] for context in ps])
        assert qhat.shape==ps.shape
        Ehat=np.array([effects_from_probs(q[:,:9],plus,iphi) for q in qhat])
        errors=np.linalg.norm((Ehat-true).reshape(-1,9,9),ord=2,axis=(-2,-1))
        maxerr=float(max(errors))
        # Union bound over all 10 contexts, 81 trusted preparations, 10
        # exhaustive click / no-click outcomes. Hoeffding is deliberately
        # conservative, but valid for independently sampled pulse trials.
        eps=math.sqrt(math.log(2*10*81*10/.05)/(2*N))
        # 9 diagonal eps; 36 offdiagonals, both symmetric, each |complex
        # error|² <=(2eps)²+(2eps)²=8eps² -> 585 eps².
        delta=math.sqrt(585)*eps
        assert maxerr<=delta+1e-12
        finite[str(N)]={"pulses_per_probe_context":N,
             "total_trusted_calibration_pulses":10*81*N,
             "maximum_simulated_operator_norm_effect_error":maxerr,
             "simultaneous_95pct_elementary_frequency_radius":eps,
             "certified_each_POVM_effect_operator_norm_radius":delta,
             "true_error_below_conservative_bound":True}
    # Combined with the prior W33 ten-setting inverse and Horodecki
    # dual, this sample budget is overwhelmingly larger than the usable
    # CCNR gap. Give a lower bound on *necessary* pulses for this
    # particular worst-case certificate (measurement error set to zero).
    from w33_20261109_full_povm_calibration_bound import detected_q,certificate
    rho=horodecki_state(.236)
    q=detected_q(mats,rho)
    ideal=certificate(q,*make_model()[1:3],make_model()[3],N=10**30,delta=0)
    gap=ideal["measured_dual_witness"]-1
    L=ideal["dual_row_l1"]
    assert gap>0
    needed_delta=gap/L
    eps_req=needed_delta/math.sqrt(585)
    Nreq=math.floor(math.log(2*10*81*10/.05)/(2*eps_req**2))+1
    out={"status":"PASS_81_PROBE_ABSOLUTE_POVM_CALIBRATION_AND_RESOURCE_NO_GO",
         "independent_probe_states":81,"registered_click_outcomes_per_context":10,
         "actual_contexts":10,"Hilbert_space_dimension":9,
         "exact_expected_probability_reconstruction_operator_error":exacterr,
         "finite_calibration_trials":finite,
         "joint_95pct_coverage_formula":"eps=sqrt(log(2*10*81*10/0.05)/(2*N)); norm(Ehat_j-E_j)_op<=sqrt(585)*eps by Frobenius bound under all marginal concentration events",
         "formal_81_state_linear_inversion":"9 computational projectors plus 36 real and 36 imaginary pair-superposition probes; recover E_jk from unconditioned click probabilities, with no-click recorded",
         "Horodecki_a0p236_dual_margin":gap,
         "Horodecki_dual_l1":L,
         "needed_per_effect_calibration_radius_exclusive":needed_delta,
         "necessary_per_probe_calibration_pulses_for_this_worst_case_Hoeffding_cert_even_with_infinite_physics_shots":Nreq,
         "corresponding_total_calibration_pulses":10*81*Nreq,
         "critical_scope":"A sufficient radius for all effects under independent trusted probe preparations and all raw pulse outcomes. This is conservative and extremely costly: structured device calibration, lower-dimensional parameter fits, or sharper multivariate statistics may improve enormously. The calculation assumes absolute no-click counts and stationary source brightness/calibration and is not a demonstrated experiment."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("CALIBRATION",json.dumps({"exact_err":exacterr,"finite":{k:round(v["certified_each_POVM_effect_operator_norm_radius"],6) for k,v in finite.items()},"strict_required_N_per_probe":Nreq,"total_calibration_pulses":10*81*Nreq}))
    return out

if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
