#!/usr/bin/env python3
"""Real patched CLASS lensing transfer and amplitude-degeneracy Jacobian.

Three runs: fading best fit, identical inputs cp=0 and lnAs increased by 0.01.
Compute CMB lensing C_L^{phiphi} directly, not measured WL tomographic shear.
The output observable is illustrative, with NO survey covariance.
"""
from pathlib import Path
import sys,math,json,glob,re,shutil
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/toe_uv'))
from class_cmb import run_class,titles
LVAL=[40,100,200,400,700,1000]
def run(p,label):
 keep={}
 _,_,_,_,info=run_class(p,kind='fading',
   extra='output=tCl,pCl,lCl,mPk\nnon_linear=none\nlensing=yes',keep=keep)
 tag=keep['tag']
 try:
  files=sorted(glob.glob(tag+'/o*cl*.dat'))
  lens=next((f for f in files if f.endswith('o_cl.dat')),None)
  assert lens,files
  cols=titles(lens)
  d=np.loadtxt(lens)
  # CLASS o_cl.dat usually gives 'phiphi' as a named column.
  candidates=[(j,name) for j,name in enumerate(cols) if 'phi' in name.lower() and
    ('phi' in name.lower().replace('phi','',1) or 'pp' in name.lower())]
  assert candidates,dict(cols=cols,files=files)
  j=candidates[0][0]
  lines=d[:,0].astype(int)
  chosen={}
  for ell in LVAL:
   ii=np.argmin(abs(lines-ell))
   assert lines[ii]==ell
   chosen[str(ell)]=float(d[ii,j])
  assert all(v>0 for v in chosen.values())
  print('CLASS_LENS',label,'COLS',cols,'PHI_COL',j,'VALUES',chosen,flush=True)
  return {'label':label,'C_phi_phi_proxy_native_CLASS_column':chosen,
          'file_header_column':cols[j],
          'units':'As CLASS o_cl.dat writes the lensing potential column, its ell prefactor is common and cancels in ratios at fixed ell.',
          'sigma8':info['s8'],'Omega_m':info['om']}
 finally:shutil.rmtree(tag)
def main():
 src=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 x=dict(src['free_neg']['p'])
 xs=[run(x,'fading_fit'),run(dict(x,cp=0),'zero_coupling_fixed_cosmology'),
    run(dict(x,lnA=x['lnA']+.01),'fading_lnAs_plus_0p01')]
 f,zero,amp=xs
 cp=x['cp']
 vals=[]
 for ell in LVAL:
  name=str(ell)
  y_f=f['C_phi_phi_proxy_native_CLASS_column'][name]
  y_0=zero['C_phi_phi_proxy_native_CLASS_column'][name]
  y_amp=amp['C_phi_phi_proxy_native_CLASS_column'][name]
  dcp=math.log(y_f/y_0)/cp
  dlnA=math.log(y_amp/y_f)/.01
  vals.append({'ell':ell,'log_lens_coupling_ratio_fading_over_cpoff':math.log(y_f/y_0),
     'lens_relative_coupling_effect_percent':(y_f/y_0-1)*100,
     'derivative_logC_to_cp_finite':dcp,
     'derivative_logC_to_lnAs_finite':dlnA})
 J=np.array([[t['derivative_logC_to_cp_finite'],t['derivative_logC_to_lnAs_finite']] for t in vals])
 assert np.isfinite(J).all()
 # Fisher for 1% independent bins, model-independent cosmic variance NOT included.
 F=(J.T@J)/.01**2
 eig=np.linalg.eigvalsh(F)
 corr=-F[0,1]/math.sqrt(F[0,0]*F[1,1])
 sig_cp_cond=1/math.sqrt(F[0,0]);sig_cp_marg=math.sqrt(np.linalg.inv(F)[0,0]) if eig.min()>1e-14 else math.inf
 assert np.max(abs(J[:,1]-1))<.2
 out={'status':'PASS_REAL_CLASS_LENSING_AND_PARAMETER_IDENTIFIABILITY_SENSITIVITY',
 'source':'analysis/toe_uv/class_cmb.py patched binary ~/cosmo/class_fading/class',
 'models':xs,'observables':vals,
 'jacobian_columns':['c_prime','lnAs'],
 'Fisher_1pct_uncorrelated_ell_bins':F.tolist(),
 'Fisher_eigenvalues':eig.tolist(),
 'fisher_correlation_cp_lnAs':corr,
 'idealized_cp_sigma_if_lnAs_fixed':sig_cp_cond,
 'idealized_cp_sigma_after_marginal_lnAs':sig_cp_marg,
 'modeled_cp_bestfit':cp,
 'scope':'Real full CLASS CMB lensing potential spectra; NOT galaxy shear or tomographic weak-lensing data, not an actual survey likelihood or a robust posterior. Six multipoles are correlated by cosmic variance and lensing reconstruction; independent 1% per bin is an invented sensitivity thought experiment. cp derivative uses 0 vs fitted cp and hence is secant, not differential derivative at cp=.053.',
 'prior_literature':['https://doi.org/10.1088/1475-7516/2026/02/014']}
 (ROOT/'data/toe_20261103_class_lensing_growth_jacobian.json').write_text(json.dumps(out,indent=2)+'\n')
 print('CLASS_LENS_RESULT',json.dumps({'rows':vals,'sigma_cp_marg':sig_cp_marg,'corr':corr}),flush=True)
if __name__=='__main__':main()
