#!/usr/bin/env python3
"""Full-POVM calibration-uncertainty + finite-shot realignment certificates.

Given actual POVM effects E_j and calibrated Ehat_j with
||E_j-Ehat_j||op<=delta, and simultaneous observed click-frequency errors
|q_bj-qhat_bj|<=epsilon, derive a *data-adaptive* dual certificate

 CCNR(rho) >= Tr[W^dag R(rho_hat)] - (delta+epsilon)*||v||_1,
 Mhat(qhat)^T v = (coefficients(W),0_K).

Proof uses state positivity/tr(rho)=1 and 0<=s_b<=1, not purity or
brightness. Works even if W chosen from same data as the reconstruction.
Synthetic frequencies and calibration radii, no observed hardware.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from w33_20261109_q8_ten_context_optimize import main as optimal
from w33_20261109_q8_full_povm_selfnormalize import calibrated_inverse
from w33_20261109_q8_horodecki_ccnr_exact import realign
from w33_20261109_q8_five_extensions import horodecki_state

def make_model():
    _,(B,U,V,ops)=optimal(return_components=True)
    mats,A,b=calibrated_inverse(B,U,V,ops,.995,.003,
                                       np.random.default_rng(2026110920))
    return mats,A,b,ops

def detected_q(mats,rho):
    p=[]
    for K in mats:
        x=np.real(np.diag(K@rho@K.conj().T))
        p.append(x/x.sum())
    return np.array(p)

def certificate(qhat,A,b,ops,alpha=.05,N=10**10,delta=0.):
    K=len(qhat)
    # 9K independent scalar outcomes; Hoeffding simultaneous 1-alpha event
    eps=math.sqrt(math.log(2*9*K/alpha)/(2*N))
    Q=np.zeros((9*K,K))
    for i in range(K):Q[9*i:9*(i+1),i]=qhat[i]
    M=np.column_stack((A,-Q))
    assert M.shape==(90,90)
    pars=np.linalg.solve(M,-b)
    coeff=pars[:80]
    rhohat=np.eye(9)/9+np.einsum('k,kij->ij',coeff,ops)
    r=realign(rhohat)
    u,s,vh=np.linalg.svd(r)
    W=u@vh
    # nuclear-norm subgradient at the reconstructed matrix, no
    # assumption that rhohat is positive.
    h=np.array([float(np.vdot(W,realign(op)).real) for op in ops])
    w0=float(np.vdot(W,realign(np.eye(9)/9)).real)
    measured_witness=w0+h@coeff
    dual=np.linalg.solve(M.T,np.r_[h,np.zeros(K)])
    L=float(np.abs(dual).sum())
    lower=float(measured_witness-(delta+eps)*L)
    return {"measured_dual_witness":float(measured_witness),
            "trace_norm_of_reconstruction":float(s.sum()),
            "dual_row_l1":L,
            "simultaneous_95pct_Hoeffding_epsilon":eps,
            "max_operator_effect_calibration_error_assumed":delta,
            "CCNR_lower":lower,
            "certifies_entanglement":bool(lower>1),
            "min_estimated_survival":float(min(pars[80:])),
            "max_estimated_survival":float(max(pars[80:])),
            "measurement_matrix_min_singular":float(np.linalg.svd(M,compute_uv=False)[-1])}

def controlled_calibration_perturbation(mats,kappa,seed=2026110945):
    rng=np.random.default_rng(seed)
    matsactual=[]
    maxK=0.;maxE=0.
    for K in mats:
        X=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
        H=(X+X.conj().T)/2
        H/=np.linalg.norm(H,2)
        U=expm(1j*kappa*H)
        Ka=K@U
        maxK=max(maxK,np.linalg.norm(Ka-K,2))
        for j in range(9):
            z=Ka[j,:].conj()[:,None]@Ka[j,:][None,:]-K[j,:].conj()[:,None]@K[j,:][None,:]
            maxE=max(maxE,np.linalg.norm(z,2))
        matsactual.append(Ka)
    assert maxK<=kappa*1.001 and maxE<=2*kappa+1e-12
    return matsactual,maxK,maxE

def main(path=None):
    mats,A,b,ops=make_model()
    rng=np.random.default_rng(2026110937)
    v=rng.normal(size=3)+1j*rng.normal(size=3)
    w=rng.normal(size=3)+1j*rng.normal(size=3)
    v/=np.linalg.norm(v);w/=np.linalg.norm(w)
    psi=np.kron(v,w)
    sources={"Horodecki_a0p236":horodecki_state(.236),
             "separable_pure_product":np.outer(psi,psi.conj()),
             "maximally_mixed":np.eye(9)/9}
    report={}
    for state,rho in sources.items():
        actualnorm=float(np.linalg.svd(realign(rho),compute_uv=False).sum())
        q=detected_q(mats,rho)
        tests=[]
        for kappa in (0.,1e-7,1e-6,1e-5):
            actualK,maxK,maxE=controlled_calibration_perturbation(mats,kappa)
            qtrue=detected_q(actualK,rho)
            # conservative worst-case certificate even at EXACT expected
            # observed conditional q. Calibrator only promises ||K-Khat||<=kappa.
            guard=2*kappa+kappa*kappa
            assert maxE<=guard+1e-11
            row=[]
            for N in (10**6,10**8,10**10,10**12,10**14):
                c=certificate(qtrue,A,b,ops,N=N,delta=guard)
                assert c["CCNR_lower"]<=actualnorm+1e-7
                row.append({"accepted_shots_per_setting":N,
                            "CCNR_lower":c["CCNR_lower"],
                            "prospective_certifies":c["certifies_entanglement"],
                            "simultaneous_radius":c["simultaneous_95pct_Hoeffding_epsilon"]})
            tests.append({"kappa_operator_analyzer_calibration":kappa,
                          "actual_max_K_difference":maxK,
                          "actual_max_POVM_effect_difference":maxE,
                          "conservative_effect_guard":guard,
                          "dual_l1":certificate(qtrue,A,b,ops,N=10**10,delta=guard)["dual_row_l1"],
                          "shot_grid":row})
        report[state]={"true_CCNR":actualnorm,"calibration_tests":tests}
    # Finite-shot random check (honest conditioning on the Hoeffding event),
    # not an assertion of actual laboratory confidence.
    rho=sources["Horodecki_a0p236"]
    q=detected_q(mats,rho)
    N=10**11
    counts=np.array([rng.multinomial(N,vector) for vector in q])
    qhat=counts/N
    eps=math.sqrt(math.log(180/.05)/(2*N))
    assert np.max(abs(qhat-q))<=eps
    c=certificate(qhat,A,b,ops,N=N,delta=0)
    assert c["CCNR_lower"]<=report["Horodecki_a0p236"]["true_CCNR"]+1e-7
    out={"status":"PASS_FULL_POVM_EFFECT_NORM_AND_FINITE_SHOT_DUAL_CERTIFICATE",
         "analytic_theorem":"For calibrated normalized POVM Ehat and ||E-Ehat||op<=delta per outcome, |q-qhat|<=epsilon simultaneously, 0<=survival<=1, and trace-one positive rho: nuclear norm R(rho)>=w(rhohat)-(delta+epsilon)*||v||1, v=M(qhat)^(-T)[h;0], with h_k=Re Tr W†R(Hk), ||W||op<=1. W can depend on observed data.",
         "confidence_scope":"Simultaneous scalar Hoeffding event for independent accepted counts, conditional on trusted per-POVM-effect operator bounds and stable state preparation. No device-independent or adversarial-source claim.",
         "per_setting_accepted_idealized_counts_grid":[10**6,10**8,10**10,10**12,10**14],
         "source_controls":report,
         "one_realized_simulated_multinomial":{"N_per_setting":N,
                  "maximum_frequency_error":float(np.max(abs(qhat-q))),
                  "simultaneous_Hoeffding_epsilon":eps,
                  "CCNR_lower":c["CCNR_lower"],
                  "certifies":c["certifies_entanglement"]},
         "true_full_POVM_effects_are_assumed_calibratable":True,
         "no_empirical_photonic_experiment":True}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS full POVM effect uncertainty",json.dumps({
         "source_summary":{k:[{"kappa":t["kappa_operator_analyzer_calibration"],
                        "first_grid_N":next((x["accepted_shots_per_setting"]
                            for x in t["shot_grid"] if x["prospective_certifies"]),None),
                        "L":t["dual_l1"]} for t in v["calibration_tests"]]
                    for k,v in report.items()},
         "one_realized_multinomial_certifies":c["certifies_entanglement"]}))
    return out

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
