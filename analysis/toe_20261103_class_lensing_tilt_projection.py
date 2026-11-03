#!/usr/bin/env python3
"""One additional *actual* patched-CLASS run for primordial n_s response.
Project fixed-cosmology cprime response against lnAs and n_s nuisance using
same 6 CMB lensing multipoles. No real lensing covariance is assumed.
"""
from pathlib import Path
import sys,json,glob,shutil,re,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis/toe_uv'))
from class_cmb import run_class,titles
SRC='data/toe_20261103_class_lensing_growth_jacobian.json'
def main():
 old=json.loads((ROOT/SRC).read_text())
 p=dict(old['models'][0]['label'] and json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())['free_neg']['p'])
 p['ns']+=.005
 keep={}
 print('CLASS_NS_START',p['ns'],flush=True)
 _,_,_,_,info=run_class(p,'fading',extra='output=tCl,pCl,lCl,mPk\nnon_linear=none\nlensing=yes',keep=keep)
 try:
  f=keep['tag']+'/o_cl.dat';d=np.loadtxt(f);cols=titles(f)
  j=cols.index('phiphi');ls=d[:,0].astype(int)
  obs=old['observables'];ells=[x['ell'] for x in obs]
  ns_res=np.array([d[np.where(ls==ell)[0][0],j] for ell in ells])
  ref=np.array([old['models'][0]['C_phi_phi_proxy_native_CLASS_column'][str(ell)] for ell in ells])
  d_ns=np.log(ns_res/ref)/.005
  J=np.column_stack([np.array([z['derivative_logC_to_cp_finite'] for z in obs]),
                     np.ones(len(obs)),d_ns])
  F=J.T@J/.01**2
  eig=np.linalg.eigvalsh(F)
  # Project off two nuisance directions: lnAs and n_s, via orthogonal projector.
  nuisance=J[:,1:]
  ans=np.linalg.lstsq(nuisance,J[:,0],rcond=None)[0]
  residual=J[:,0]-nuisance@ans
  norm=float(np.linalg.norm(residual))
  error=1/(100*norm) if norm>1e-14 else math.inf
  rsignal=np.array([z['log_lens_coupling_ratio_fading_over_cpoff'] for z in obs])
  residual_full=rsignal-nuisance@np.linalg.lstsq(nuisance,rsignal,rcond=None)[0]
  print('CLASS_NS_RESULT',json.dumps({'ns_derivative':d_ns.tolist(),'fisher_eigen':eig.tolist(),
       'projected_cp_sig_1percent_indep':error,'fit_original_signal_residual_log':residual_full.tolist(),
       'fit_original_signal_residual_peak':float(max(abs(residual_full)))}),flush=True)
  out={'status':'PASS_REAL_CLASS_LENSING_CP_AS_NS_THREE_PARAMETER_PROJECTED_RESPONSE',
    'actual_runs':4,
    'parent_lensing_certificate':SRC,'new_ns_plus_delta':.005,
    'Cphi_ns_perturbed_values':ns_res.tolist(),'ell':ells,
    'finite_difference_logC_over_ns':d_ns.tolist(),
    'jacobian_columns':['cprime_secant','lnAs_exact_amplitude','ns_forward'],
    'Jacobian':J.tolist(),'independent_1pct_fisher':F.tolist(),
    'eigenvalues_1pct_fisher':eig.tolist(),
    'projected_cprime_response':residual.tolist(),
    'projected_Cprime_1sigma_illustrative':error,
    'lensing_response_removed_by_amplitude_and_tilt':(1-float(np.dot(residual_full,residual_full)/np.dot(rsignal,rsignal))),
    'full_cp_change_logC_residual_after_amplitude_and_ns_fit':residual_full.tolist(),
    'scope':'REAL patched CLASS linear lensing spectra from four full solver runs. 1% per multipole independent errors are illustrative, not a real survey covariance; no galaxy weak-lensing tomographic likelihood. n_s and lnAs response derivative at fitted model, cp response finite secant from zero to fitted cp, so linear Fisher forecast is only local approximate at cp~0.05. Fixes other cosmological parameters, not a full MCMC.'}
  (ROOT/'data/toe_20261103_class_lensing_tilt_projection.json').write_text(json.dumps(out,indent=2)+'\n')
 finally:shutil.rmtree(keep['tag'])
if __name__=='__main__':main()
