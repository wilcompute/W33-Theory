#!/usr/bin/env python3
"""Frozen S9 Gaussian likelihood harness validated on SYNTHETIC DES-like shear.

It never scores S9 from a conditional S8 posterior or search-indexed URL.
Checks exact preregistration frozen date and cuts, covariance order, nuisance
profiling versus independent optimizer, permutation invariance, and refusal
to process absent/unauthenticated full data/theory/covariance.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from w33_20261109_des_y6_live_frozen_gate import probe
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"analysis/toe_uv/prereg_noshear.json"
FROZEN=json.loads(P.read_text())["S9_shear_no_split"]
assert FROZEN["frozen"]=="2026-11-08"

def profile_chi2(data,theory,cov,nuisance,prior_precision):
    data=np.asarray(data,dtype=float)
    theory=np.asarray(theory,dtype=float)
    C=np.asarray(cov,float);A=np.asarray(nuisance,float)
    N=len(data)
    assert theory.shape==(N,) and C.shape==(N,N) and A.shape[0]==N
    assert np.max(abs(C-C.T))<1e-12
    assert min(np.linalg.eigvalsh(C))>0
    assert prior_precision.shape==(A.shape[1],A.shape[1])
    inv=np.linalg.inv(C)
    x=data-theory
    normal=A.T@inv@A+prior_precision
    beta=np.linalg.solve(normal,A.T@inv@x)
    residual=x-A@beta
    chi=float(residual@inv@residual+beta@prior_precision@beta)
    assert chi>=-1e-9
    return chi,beta

def validate_ids(data_ids,model_ids,cov_ids):
    if list(data_ids)!=list(model_ids) or list(data_ids)!=list(cov_ids):
        raise ValueError("FATAL: data-vector, covariance and theory bin IDs differ")
    if len(set(data_ids))!=len(data_ids):
        raise ValueError("FATAL: duplicated bin IDs")
    return True

def make_synthetic():
    ids=[f"xip_{i}" for i in range(4)]+[f"xim_{i}" for i in range(4)]
    angles=np.array([5,12,20,60,30,70,100,110],float)
    cuts=np.r_[(angles[:4]>10),(angles[4:]>60)]
    assert list(np.where(cuts)[0])==[1,2,3,5,6,7]
    i=np.arange(8)
    C=.0004*(.27**abs(i[:,None]-i[None,:]))
    rng=np.random.default_rng(202611091902)
    bases=np.array([.12,.16,.20,.24,.03,.06,.08,.10])
    # Every model is *synthetic*, not an actual scalar-field CLASS/Halofit
    # prediction. Nuisance columns have a Gaussian prior.
    theories={
       "synthetic_LCDM":bases,
       "synthetic_CPL":bases+.013*np.cos(np.arange(8)),
       "synthetic_fading_cneg":bases+.010*np.sin(np.arange(8)),
       "synthetic_fading_cpos":bases-.012*np.sin(np.arange(8))}
    A=np.column_stack((np.linspace(-.02,.025,8),np.array([.012]*4+[-.015]*4)))
    precision=np.diag([1.5,2.])
    noise=rng.multivariate_normal(np.zeros(8),C)
    true=theories["synthetic_fading_cneg"]+A@np.array([.3,-.4])+noise
    return ids,angles,cuts,C,A,precision,theories,true

def main(path=None):
    ids,ang,mask,C,A,P,models,data=make_synthetic()
    selected=np.where(mask)[0]
    selected_ids=[ids[i] for i in selected]
    Cov=C[np.ix_(selected,selected)]
    Am=A[selected]
    scores={}
    for name,t in models.items():
        validate_ids(selected_ids,selected_ids,selected_ids)
        exact,beta=profile_chi2(data[selected],t[selected],Cov,Am,P)
        def f(v):
            residual=data[selected]-t[selected]-Am@v
            return float(residual@np.linalg.solve(Cov,residual)+v@P@v)
        numerical=minimize(f,np.zeros(2),method="BFGS",tol=1e-10)
        assert abs(exact-numerical.fun)<1e-7
        scores[name]={"synthetic_profile_chi2":exact,
                      "best_synthetic_nuisance":beta.tolist()}
    rng=np.random.default_rng(202611091903)
    perm=rng.permutation(len(selected))
    perr=0.
    for name,t in models.items():
        chi,_=profile_chi2(data[selected],t[selected],Cov,Am,P)
        cp,_=profile_chi2(data[selected][perm],t[selected][perm],
                    Cov[np.ix_(perm,perm)],Am[perm],P)
        perr=max(perr,abs(chi-cp))
    assert perr<1e-9
    refused=[]
    try:validate_ids(selected_ids,list(reversed(selected_ids)),selected_ids)
    except ValueError:refused.append("permuted theory bin labels")
    try:validate_ids(selected_ids,selected_ids,list(reversed(selected_ids)))
    except ValueError:refused.append("permuted covariance bin labels")
    try:
        bad=Cov.copy();bad[0,0]=-1
        profile_chi2(data[selected],models["synthetic_CPL"][selected],bad,Am,P)
    except AssertionError:refused.append("indefinite covariance")
    assert len(refused)==3
    # Actual survey availability: status 200 HTML is never valid data.
    official="https://des.ncsa.illinois.edu/releases/y6a2/"
    missing="https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6key_products/final_version/3x2pt_2025-07-28-20h_UNBLINDED_wmask_nob2.fits"
    statuses={"official_release_app":probe(official),
              "former_unblinded_FITS":probe(missing)}
    out={"status":"PASS_S9_PREREG_GAUSSIAN_LIKELIHOOD_SYNTHETIC_VALIDATION_ONLY",
         "frozen_S9_date":FROZEN["frozen"],
         "frozen_claim_sha256":hashlib.sha256(FROZEN["claim"].encode()).hexdigest(),
         "frozen_scale_cuts":{"xi_plus_arcmin_strict_gt":10,"xi_minus_arcmin_strict_gt":60},
         "synthetic_source":{"all_bins":len(ids),"kept_bins":len(selected),"kept_indices":selected.tolist(),
                             "independent_test_models":list(models.keys()),
                             "nuisance_prior":"2D Gaussian synthetic, NOT calibrated DES NLA"},
         "synthetic_profile_scores_NOT_DES":scores,
         "analytic_nuisance_profile_vs_BFGS_max_difference_less_than":1e-7,
         "synthetic_bin_covariance_joint_permutation_invariance_error":perr,
         "negative_controls_rejected":refused,
         "live_endpoint_get":statuses,
         "unblinded_DES_Y6_real_fits_complete_and_verified":False,
         "matched_real_covariance_and_nz_acquired":False,
         "patched_CLASS_Halofit_model_predictions_and_nuisance_refits_executed":False,
         "S9_real_survey_chi2_scored":False,
         "fail_closed_conditions":["verified unblinded full Y6 FITS actual bytes & official hash",
           "covariance/correlation function bin order, photometric redshift and exact cuts",
           "corrected nonlinear predictions for each frozen model",
           "matched nuisance priors and refitted likelihood for CPL,fading c<0,c>0,LCDM"],
         "scope":"This is only a statistical pipeline unit test against a synthetic data vector; the preregistered S9 comparison is not evaluated. An official web HTML page or a conditional LambdaCDM S8 posterior is not valid substitute data."}
    assert not out["S9_real_survey_chi2_scored"]
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PASS S9 synthetic pipeline",json.dumps({
        "kept_bins":len(selected),"matched_profiles":True,
        "perm_err":perr,"negatives":len(refused),
        "DES_endpoint":statuses["former_unblinded_FITS"]["status_code"],
        "S9_real_scored":False}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
