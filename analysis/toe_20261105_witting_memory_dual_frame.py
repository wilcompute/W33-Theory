#!/usr/bin/env python3
"""Operational bridge: two local Witting-40 analyzers witness qutrit reset memory.

Use the exact ququart complex projective 2-design frame to reconstruct an
embedded qutrit Bell fidelity from product four-mode Witting readout.
Compute full 1600-outcome table, unbiased dual weights, finite sampling
variance, pair-loss model, and a uniform (conservative) Hoeffding bound.
Compare to an ideal *global entangling* Bell-projection benchmark.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays
OUT=ROOT/"data/toe_20261105_witting_qutrit_memory_product_dual.json"

def main():
    rays=np.asarray(construct_witting_40_rays(),complex)
    assert rays.shape==(40,4)
    P=np.einsum("ia,ib->iab",rays,rays.conj())
    assert np.max(abs(sum(P)-10*np.eye(4)))<1e-11
    F=5*P-np.eye(4)
    # The ququart Witting POVM is informationally complete:
    # rho=sum_i Tr(rho*P_i/10) * (5 P_i-I) for every 4x4 rho.
    for rho in (np.eye(4)/4,np.outer(rays[17],rays[17].conj()),
                np.diag([.1,.2,.3,.4])):
        p=np.real(np.einsum("iab,ba->i",P,rho))/10
        assert np.max(abs(sum(p[i]*F[i] for i in range(40))-rho))<1e-12
    phi=np.zeros(16,complex)
    for a in range(3):phi[5*a]=1/math.sqrt(3)
    Bell=np.outer(phi,phi.conj())
    norm3=np.sum(abs(rays[:,:3])**2,axis=1)
    inner=rays[:,:3]@rays[:,:3].T  # transpose, NOT Hermitian conjugation
    w=25*abs(inner)**2/3 -5*(norm3[:,None]+norm3[None,:])/3+1
    assert np.max(abs(w-w.T))<1e-12
    for i,j in ((0,0),(0,5),(14,32),(39,39)):
        direct=float(np.vdot(phi,np.kron(F[i],F[j])@phi).real)
        assert abs(w[i,j]-direct)<1e-12
    # Analytic full joint Witting-pair distributions for isotropic qutrit
    # states p|Phi3><Phi3|+(1-p) I_3 tensor I_3/9, embedded in 4x4.
    qpure=abs(inner)**2/(300)
    qmix=(norm3[:,None]*norm3[None,:])/900
    assert abs(qpure.sum()-1)<1e-12
    assert abs(qmix.sum()-1)<1e-12
    def dist(p):return p*qpure+(1-p)*qmix
    records=[]
    for p in (0,.25,.35,.6,1.):
        q=dist(p)
        f=(1+8*p)/9
        mean=float(np.sum(q*w))
        var=float(np.sum(q*(w-mean)**2))
        assert abs(q.sum()-1)<1e-12 and q.min()>-1e-13
        assert abs(mean-f)<1e-12
        records.append(dict(storage_survival_p=p,
             Bell_fidelity=f,dual_estimator_mean=mean,
             Witting_pair_single_sample_variance=var,
             Witting_single_sample_standard_deviation=math.sqrt(var),
             ideal_Global_Bell_projection_variance=f*(1-f),
             Witting_vs_global_variance_ratio=var/(f*(1-f)) if f<1 else None))
    # Independent loss on BOTH four-mode photon/ancilla analyzers.
    p=.35;eta=.85;pair_eff=eta**2
    F1=(1+8*p)/9;F0=1/3
    q1=dist(p); q0=dist(.25)
    var1=float(np.sum(q1*(w-F1)**2))
    var0=float(np.sum(q0*(w-F0)**2))
    var_no_click_scaled_alt=var1/pair_eff+F1*F1*(1/pair_eff-1)
    var_no_click_scaled_null=var0/pair_eff+F0*F0*(1/pair_eff-1)
    # Y=w/eta^2 for a coincidence; Y=0 for a failed pair.
    # This is unbiased only for state-independent, calibrated loss.
    delta=(F1-F0)/2
    range0=float(w.max()-w.min())
    required=int(math.ceil(math.log(1/.01)*range0**2/
                            (2*(pair_eff*delta)**2)))
    null_alpha=math.exp(-2*required*(pair_eff*delta)**2/range0**2)
    # Same bound under alternate must be <= beta=0.05.
    assert null_alpha<=.01+1e-12
    assert math.exp(-2*required*(pair_eff*delta)**2/range0**2)<.05
    # Ideal binary entangling Bell-projection benchmark: exact binomial,
    # rather than an assumed deterministic optical Bell measurement.
    optimal=None
    for n in range(1,5000):
        threshold=int(binom.isf(.01,n,F0))+1
        fpr=float(binom.sf(threshold-1,n,F0))
        pow=float(binom.sf(threshold-1,n,F1))
        if fpr<=.01 and pow>=.95:
            optimal=dict(shots=n,hit_threshold=threshold,false_positive=fpr,
                         model_power=pow)
            break
    assert optimal is not None
    bound={
       "status":"PASS_WITTING_LOCAL_PRODUCT_DUAL_QUTRIT_MEMORY_WITNESS",
       "Witting_outcomes_per_site":40,"joint_outcome_count":1600,
       "dual_frame_identity":"rho = sum_i p_i (5 P_i - I4)",
       "local_dual_weight_formula":"W_ij=25/3*|sum_a<3 r_i,a r_j,a|^2 - 5/3*(s_i+s_j)+1",
       "dual_weight_min":float(w.min()),"dual_weight_max":float(w.max()),
       "independent_analyzer_efficiency":eta,"joint_coincidence_efficiency":pair_eff,
       "alternative_storage_p":p,"alternative_Bell_fidelity":F1,
       "separable_upper_bound_Bell_fidelity":F0,
       "conservative_distribution_free_Hoeffding_shots_1pct_fpr_95pct_power":required,
       "Hoeffding_bound_at_shots":null_alpha,
       "ideal_global_entangling_Bell_measurement_binomial_benchmark":optimal,
       "scaled_unconditional_variance_alt":var_no_click_scaled_alt,
       "scaled_unconditional_variance_null_isotropic":var_no_click_scaled_null,
       "all_models":records,
       "scope":"Local product Witting tomography yields an unbiased Bell witness but a larger finite-sample variance than a global Bell projector. Hoeffding is conservative, not a realistic hardware forecast. Fixed eta and no outcome-dependent loss are essential. Global Bell projector not assumed available with passive four-port optics.",
       "known_prior_art":"Witting complex projective 2-design, linear-inversion dual frame, entanglement witness F<=1/3 for separable states, and Hoeffding/Bernstein concentration are standard."}
    OUT.write_text(json.dumps(bound,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS Witting POVM dual estimator",round(var_no_click_scaled_alt,5),"Hoeffding shots",required,"global Bell",optimal["shots"],flush=True)
    print("CERTIFICATE",OUT)
    return bound
if __name__=="__main__":main()
