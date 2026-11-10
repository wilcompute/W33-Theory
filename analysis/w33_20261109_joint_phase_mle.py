#!/usr/bin/env python3
"""Joint multinomial phase calibration on W33-Q8 lossy analyzers.

Model restricted to fully known K_cal plus unknown input diagonal phases,
one unobservable gauge phase per support component. Simultaneous fit to
all 9 click and 1 no-click outcomes and all coherent probes; numerical
Fisher and empirical seed controls, NOT a rigorous coverage certificate.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2
from w33_20261109_full_povm_calibration_bound import make_model
from w33_20261109_phase25_structured_calibration import forest,probes,effects
from w33_20261109_phase_fisher_information import all_pairs

def probs_jac(K,S,theta):
    KD=K*np.exp(1j*theta)[None,:]
    amp=S@KD.T
    click=abs(amp)**2
    p=np.column_stack([click,1-click.sum(axis=1)])
    jac=2*np.real(np.conj(amp)[:,:,None]*(1j*S[:,None,:]*KD[None,:,:]))
    jac=np.concatenate([jac,-jac.sum(axis=1,keepdims=True)],axis=1)
    assert p.shape==(len(S),10)
    assert np.min(p)>-1e-10
    return np.maximum(p,0),jac

def fisher(K,S,theta,free):
    p,dp=probs_jac(K,S,theta)
    jp=dp[:,:,free]
    F=np.einsum('ijk,ijl,ij->kl',jp,jp,1/np.maximum(p,1e-13))/len(S)
    eig=np.linalg.eigvalsh(F)
    assert np.min(eig)>1e-9
    return F

def fit(K,S,counts,free):
    def loss(z):
        theta=np.zeros(9);theta[free]=z
        p,dp=probs_jac(K,S,theta)
        C=counts/np.maximum(p,1e-12)
        score=-np.einsum("ij,ijk->k",C,dp[:,:,free])
        nll=-np.sum(counts*np.log(np.maximum(p,1e-12)))
        return float(nll),score
    sol=minimize(loss,np.zeros(len(free)),jac=True,
         method="L-BFGS-B",bounds=[(-.3,.3)]*len(free),
         options={"maxiter":160,"ftol":1e-12,"gtol":1e-5})
    theta=np.zeros(9);theta[free]=sol.x
    return theta,float(sol.fun),bool(sol.success)

def experiment(K,index,M=640000,reps=12,seed=20261109200):
    rng=np.random.default_rng(seed+index)
    roots,tree=forest(K)
    free=[j for j in range(9) if j not in roots]
    phase=np.zeros(9);phase[free]=rng.uniform(-.07,.07,size=len(free))
    true=K*np.exp(1j*phase)[None,:]
    designs={"forest_phase_only":tree,"all_observable_phase_pairs":all_pairs(K)}
    rows={}
    all_errors={}
    for name,edges in designs.items():
        # The 9 number inputs are exactly phase-insensitive when K_cal is
        # trusted; we reserve them separately for model validation.
        S=probes(edges)[9:]
        N=max(1,int(M/len(S)))
        pp,_=probs_jac(K,S,phase)
        F=fisher(K,S,phase,free)
        lam=np.linalg.eigvalsh(F)
        records=[]
        for rep in range(reps):
            counts=np.array([rng.multinomial(N,row) for row in pp])
            hat,nll,conv=fit(K,S,counts,free)
            Eerror=effects(K*np.exp(1j*hat)[None,:])-effects(true)
            effecterr=float(np.max(np.linalg.norm(Eerror,ord=2,axis=(-2,-1))))
            delta=hat[free]-phase[free]
            quadratic=float((N*len(S))*(delta@F@delta))
            records.append({"max_effect_operator_error":effecterr,
                        "phase_rmse":float(np.linalg.norm(delta)/math.sqrt(len(free))),
                        "asymptotic_fisher_ellipsoid_chi2":quadratic,
                        "chi_square_95pct_threshold":float(chi2.ppf(.95,len(free))),
                        "falls_inside_nominal_asymptotic_95pct_ellipsoid":quadratic<=chi2.ppf(.95,len(free)),
                        "optimizer_converged":conv})
        errors=np.array([x["max_effect_operator_error"] for x in records])
        rows[name]={"phase_probe_configuration_count":len(S),
             "independent_model_check_number_probe_configs":9,
             "launched_photons_per_coherent_probe":N,
             "total_launched_phase_calibration_photons":N*len(S),
             "phase_dim":len(free),
             "full_multinomial_Fisher_min_eig_per_launched_trial":float(min(lam)),
             "local_CR_trace_per_launched_trial":float(np.trace(np.linalg.inv(F))),
             "replications":reps,
             "effect_opnorm_error_mean":float(np.mean(errors)),
             "effect_opnorm_error_max":float(np.max(errors)),
             "empirical_nominal_95pct_ellipsoid_fraction":float(np.mean([x["falls_inside_nominal_asymptotic_95pct_ellipsoid"] for x in records])),
             "optimizer_converged_count":sum(x["optimizer_converged"] for x in records)}
        all_errors[name]=errors
    return {"setting_index":index,"component_count":len(roots),
        "two_designs":rows,
        "mean_error_forest_over_all_pairs":float(np.mean(all_errors["forest_phase_only"])/np.mean(all_errors["all_observable_phase_pairs"]))}

def main(path=None):
    K,_,_,_=make_model()
    idx=(0,2,8)
    rows=[experiment(K[i],i,reps=12) for i in idx]
    assert all(x["two_designs"]["forest_phase_only"]["phase_dim"]==9-x["component_count"] for x in rows)
    assert all(x["two_designs"]["all_observable_phase_pairs"]["local_CR_trace_per_launched_trial"]<
               x["two_designs"]["forest_phase_only"]["local_CR_trace_per_launched_trial"] for x in rows)
    out={"status":"PASS_JOINT_MULTINOMIAL_PHASE_MLE_3_CONTEXTS_FINITE_TRIALS",
         "contexts_evaluated":list(idx),
         "each_design_fixed_phase_calibration_launch_budget_target":640000,
         "number_replications_each":12,
         "designs":rows,
         "mean_empirical_forest_over_all_pairs_effect_error":float(np.mean([r["mean_error_forest_over_all_pairs"] for r in rows])),
         "model_assumptions":"Known complete stationary lossy 9x9 Kcal, only unknown diagonal input phases. One gauge root per disjoint interferometric component. All 9 clicks and no-click used jointly. Input basis preparations cannot infer phase and are reserved for separate model-falsifier acquisitions, NOT included in quoted phase-only photons.",
         "statistical_scope":"Optimization and Monte Carlo coverage are empirical and local-asymptotic only; 12 replicates/context cannot establish 95% confidence coverage. No rigorous nonasymptotic effect error guarantee or PPT witness certificate. Full physical calibration would also estimate Kcal amplitudes, losses, detector effects, drifts and source state deviations.",
         "prior_art":"Multinomial MLE, Fisher information and optimal experimental design are standard; W33-specific geometry and observed gauge-identifiability are the application."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PHASE_MLE",json.dumps({"mean_ratio":out["mean_empirical_forest_over_all_pairs_effect_error"],
      "per_setting":[(x["setting_index"],x["mean_error_forest_over_all_pairs"]) for x in rows]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
