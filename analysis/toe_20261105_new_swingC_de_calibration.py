#!/usr/bin/env python3
"""Unrelated swing C: do supernova calibration drifts mimic evolving dark energy?

Use flat FLRW normalized H(z), CPL w(a)=w0+wa(1-a). Generate
*synthetic truth* at DES-Dovekie 2026 published central example
(Omega_m=.330, w0=-.803, wa=-.72), NOT a new fit to the data.
Show a smooth redshift-dependent SN magnitude calibration drift can
closely mimic its SN distance moduli; BAO radial+transverse data with
one common sound-horizon scaling break some degeneracy. Audit the
actual repo's 24-draw posterior-predictive likelihood-exception bias:
valid-only average vs failed draws treated as zero likelihood.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_swingC_cosmology_calibration_guard.json"
OM=.33
def E(z,w0,wa):
    z=np.asarray(z,dtype=float)
    rho=(1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z))
    return np.sqrt(OM*(1+z)**3+(1-OM)*rho)
def distances(z,w0,wa):
    z=np.asarray(z,dtype=float)
    grid=np.linspace(0,max(float(z.max()),.01),12001)
    Dc=cumulative_trapezoid(1/E(grid,w0,wa),grid,initial=0)
    d=np.interp(z,grid,Dc)
    return d,1/E(z,w0,wa)
def chi2_optimal_common_scale(reference,template,sigma):
    # Weighted least squares for shared alpha=c/(H0*rd), common to
    # radial and transverse BAO distances, not arbitrary per-redshift.
    w=1/np.asarray(sigma)**2
    a=float(np.dot(w*reference,template)/np.dot(w*template,template))
    return a,float(np.sum(((reference-a*template)/sigma)**2))
def synthetic():
    sn_z=np.linspace(.06,1.35,90)
    baoz=np.array([.3,.5,.7,.9,1.2,1.5,2.3])
    w0,wa=-.803,-.72
    d0,_=distances(sn_z,-1,0)
    d1,_=distances(sn_z,w0,wa)
    delta=5*np.log10(d1/d0)
    x=sn_z/(1+sn_z)
    # H0/SN absolute calibration degeneracy represented by intercept;
    # redshift drift is a single additional nuisance coefficient.
    X=np.c_[np.ones(len(sn_z)),x]
    coeff=np.linalg.lstsq(X,delta,rcond=None)[0]
    resid=delta-X@coeff
    sn_sigma=.10
    sn_chi2=float(np.sum((resid/sn_sigma)**2))
    # BAO predictions assuming a sound-horizon-free common scale:
    Dcl,Eil=distances(baoz,-1,0)
    Dcc,Eic=distances(baoz,w0,wa)
    # Assume a synthetic exact mean at alpha=1; choose 1% or 3% errors.
    obs=np.r_[Dcc,Eic]
    template=np.r_[Dcl,Eil]
    c1,s1=chi2_optimal_common_scale(obs,template,.01*obs)
    c3,s3=chi2_optimal_common_scale(obs,template,.03*obs)
    assert max(abs(resid))<.02
    assert s1>5*s3
    return {"synthetic_baseline":"Dovekie 2026 published illustrative central Omega_m=.33, CPL w0=-.803 wa=-.72, not refitted from observed SN/BAO",
     "SN_sample_redshift_count":len(sn_z),
     "SN_distance_modulus_CPL_minus_LCDM_mag_minmax":[float(min(delta)),float(max(delta))],
     "fitted_SN_calibration_offset_mag":float(coeff[0]),
     "fitted_SN_redshift_drift_per_z_over_1plusz_mag":float(coeff[1]),
     "max_abs_post_calibration_SN_residual_mag":float(max(abs(resid))),
     "synthetic_SN_chi2_difference_versus_CPL_for_drift_LCDM":sn_chi2,
     "BAO_redshift_points":baoz.tolist(),
     "BAO_radial_and_transverse_observations":len(obs),
     "BAO_one_percent_fractional_uncertainty_LCDM_vs_CPL_expected_chi2":s1,
     "BAO_three_percent_fractional_uncertainty_LCDM_vs_CPL_expected_chi2":s3,
     "BAO_scale_fit_1percent":c1,"BAO_scale_fit_3percent":c3,
     "interpretation":"SN-only CPL distances can be closely matched by a smooth calibration offset and drift. Independent BAO E(z),D_M(z) with common absolute scale can break the degeneracy at sufficiently small uncertainties; choice of adopted sound-horizon calibration and other parameters changes significance.",
     "limitations":"Purely synthetic ensemble and assumed homogeneous precision, no Planck likelihood, survey covariance, Pantheon/Dovekie redshift selection, selection biases, numerical BAO nuisance, perturbation data or joint posterior."}
def posterior_audit():
    bao=json.loads((ROOT/"analysis/toe_uv/class_ppd_dovekie_bao.json").read_text())
    sn=json.loads((ROOT/"analysis/toe_uv/class_ppd_dovekie_sn.json").read_text())
    rows=[]
    for name in sorted(set(bao["rows"])&set(sn["rows"])):
        parts=[]
        for hold,ds in (("bao",bao),("sn",sn)):
            z=ds["rows"][name]
            n=z["n"]
            if not 0<n<=24:raise ValueError("unexpected sample count")
            # If failures have zero likelihood, normalized over ALL 24
            # attempts, elpd shifts by ln(n_success/24).
            penalty=math.log(n/24)
            parts.append({"hold":hold,"n_valid":n,
                "reported_valid_only_elpd":z["elpd"],
                "zero_failed_draws_elpd":z["elpd"]+penalty,
                "missing_draw_log_correction":penalty})
        rows.append({"model":name,"folds":parts,
          "reported_total_elpd":sum(z["reported_valid_only_elpd"] for z in parts),
          "zero_failed_draws_total_elpd":sum(z["zero_failed_draws_elpd"] for z in parts)})
    exp=next(x for x in rows if x["model"]=="exp_infl1")
    assert sum(x["n_valid"] for x in exp["folds"])==32
    faded=next(x for x in rows if x["model"]=="free_neg_infl2")
    assert any(x["n_valid"]<15 for x in faded["folds"])
    return {"repo_parent_source":"analysis/toe_uv/class_ppd.py + class_ppd_dovekie_sn/bao.json (prior 24-draw attempted Fisher posterior predictive)",
        "assumed_attempts_per_fold":24,
        "rows":rows,
        "interpretation":"The parent code averages e^{-chi2/2} only over successful CLASS evaluations. If failed evaluations are assigned zero physical likelihood, use total attempted count instead, lowering elpd by ln(n_valid/24). If they are numerical failures of physically valid points, neither treatment resolves the missing predictive mass. Thus posterior model ranking needs convergence, failure accounting and robust sampling.",
        "not_a_new_data_fit":True}
def main():
    s=synthetic();r=posterior_audit()
    out={"status":"PASS_SYNTHETIC_DE_CPL_SN_DRIFT_AND_PPD_MISSING_DRAW_AUDIT",
      "synthetic_calibration":s,"repo_posterior_predictive_failure_audit":r,
      "source_literature":["DES-Dovekie 2026 updated photometry MNRAS548 2026 stag632","Turyshev PRD113 103540 2026 dark energy SN calibration sensitivity","DESI DR2 papers 2025-2026","repo PASS12616-12620 posterior predictive retraction"],
      "scientific_boundary":"No fresh statistical evidence for evolving dark energy; synthetic stress test is not posterior inference. PPD failure corrections are conditional interpretations, not unique corrected Bayes factors."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("DE_CALIBRATION_PASS",s["max_abs_post_calibration_SN_residual_mag"],
       "baochi2",s["BAO_one_percent_fractional_uncertainty_LCDM_vs_CPL_expected_chi2"],
       "elpdMissing",[(x["model"],round(x["zero_failed_draws_total_elpd"]-x["reported_total_elpd"],3)) for x in r["rows"]],flush=True)
    return out
if __name__=="__main__":main()
