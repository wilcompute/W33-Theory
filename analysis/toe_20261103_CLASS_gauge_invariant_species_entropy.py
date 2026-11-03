#!/usr/bin/env python3
"""Actual CLASS gauge-invariant relative-entropy test for interacting DM.

S_bc=3(zeta_b-zeta_c)=3(delta_c/r_c-delta_b/r_b),
r_i = d ln(rho_i)/d ln a. For mass-varying CDM r_c != -3, so
delta_b-delta_c is NOT gauge invariant even at linear order.
"""
from pathlib import Path
import numpy as np,sys,json,shutil,glob,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis/toe_uv'))
from class_cmb import run_class,titles
KS=[.05,.1,.2,1.]
ZS=[0.,1.]
def run(p,kind,label):
 keep={}
 _,z,H,dc,info=run_class(p,kind=kind,extra='output=tCl,pCl,lCl,mPk,dTk\nz_pk=0,1\nnon_linear=none',keep=keep)
 try:
  bc=keep['cols']
  raw=keep['raw']
  assert 'phi_scf' in bc if kind=='fading' else True
  row_z=raw[:,bc.index('z')][::-1]
  rho_b=raw[:,bc.index('(.)rho_b')][::-1]
  rho_c=raw[:,bc.index('(.)rho_cdm')][::-1]
  assert len(row_z)>200
  N=-np.log1p(row_z)
  rb=np.gradient(np.log(rho_b),N,edge_order=2)
  rc=np.gradient(np.log(rho_c),N,edge_order=2)
  phi=raw[:,bc.index('phi_scf')][::-1] if 'phi_scf' in bc else None
  v=np.gradient(phi,N,edge_order=2) if phi is not None else None
  fns=sorted(glob.glob(keep['tag']+'/o_z*_tk.dat'),key=lambda f:int(re.search(r'_z(\d+)_tk',f).group(1)))
  assert len(fns)==2
  results=[]
  for i,znow in enumerate(ZS):
   # Headers show redshift; enumerate CLASS order corresponding z_pk order
   cols=titles(fns[i]);dat=np.loadtxt(fns[i]);k=dat[:,cols.index('k (h/Mpc)')]
   db=dat[:,cols.index('d_b')];dc=dat[:,cols.index('d_cdm')]
   rbi=float(np.interp(znow,row_z,rb));rci=float(np.interp(znow,row_z,rc))
   vi=float(np.interp(znow,row_z,v)) if v is not None else None
   mass_rate=float(-3-rci)
   logmass_from_phi=(float(p['cp'])*vi) if 'cp' in p and kind=='fading' else 0.
   for K in KS:
    valb=float(np.interp(K,k,db));valc=float(np.interp(K,k,dc))
    rawdiff=valb-valc
    S=3*(valc/rci-valb/rbi)
    # Explicit gauge-shift: delta_i -> delta_i + r_i epsilon
    eps=.04*valc
    delta_S=3*((valc+rci*eps)/rci-(valb+rbi*eps)/rbi)
    delta_raw=(valb+rbi*eps)-(valc+rci*eps)
    assert abs(delta_S-S)<1e-11*max(1,abs(S))
    results.append({'z':znow,'k_hMpc':K,'delta_b_over_delta_c':valb/valc,
      'delta_b_minus_delta_c_over_delta_c':rawdiff/valc,
      'gauge_invariant_Sbc_over_delta_c':S/valc,
      'difference_Sbc_minus_raw_over_delta_c':(S-rawdiff)/valc,
      'baryon_rho_log_derivative':rbi,'CDM_rho_log_derivative':rci,
      'effective_mass_log_derivative_minus_dlnm_over_dN':mass_rate,
      'beta_times_phi_N_if_fading':logmass_from_phi,
      'raw_diff_under_gauge_shift_relative_change':(delta_raw-rawdiff)/valc,
      'Sbc_gauge_transform_absolute_error':abs(delta_S-S)})
  return {'label':label,'info':info,'results':results,
   'background_phi_scf_field_present':phi is not None,
   'background_fields_for_derivative':{'z':row_z[:5].tolist(),'rho_cdm':rho_c[:5].tolist()}}
 finally:shutil.rmtree(keep['tag'])
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 p=dict(r['free_neg']['p'])
 runs=[run(p,'fading','fading_fit'),
       run(dict(p,cp=0.),'fading','fixed_params_no_mass_coupling')]
 for runx in runs:
  for res in runx['results']:
   assert abs(res['baryon_rho_log_derivative']+3)<.003
   if runx['label']=='fading_fit':
    assert abs(res['effective_mass_log_derivative_minus_dlnm_over_dN']-
               res['beta_times_phi_N_if_fading'])<.003
 summary=[{'model':rx['label'],'z0_k0p1':next(x for x in rx['results'] if x['z']==0 and x['k_hMpc']==.1)}for rx in runs]
 out={'status':'PASS_REAL_CLASS_RELATIVE_ENTROPY_GAUGE_INVARIANT_DIAGNOSTIC',
 'runs':runs,'summary':summary,
 'definition':'For baryon and interacting CDM background r_i=dln rho_i/dln a, S_bc=3(zeta_b-zeta_c)=3[delta_c/r_c-delta_b/r_b]. This is invariant under common infinitesimal slicing change delta_i->delta_i+r_i epsilon. In a CDM mass-varying background r_c=-3-beta phi_N, r_b=-3. For cp=0, S_bc=delta_b-delta_c.',
 'scope':'Real patched CLASS source density transfer functions in its synchronous gauge, and background from CLASS. Does not construct an experimentally accessible isolated S_bc, a survey likelihood, or galaxy bias. Ratios S_bc/delta_c are NOT themselves gauge invariant, only S_bc is; the normalizing delta_c is gauge dependent. No full ultralight scalar wave included. Finite differencing the background rho fields can be numerically unstable at high redshift; only z=0 and1 tested.',
 'prior_literature':['https://doi.org/10.1103/PhysRevD.82.083515',
  'https://doi.org/10.1103/PhysRevD.68.063505']}
 (ROOT/'data/toe_20261103_CLASS_gauge_invariant_species_entropy.json').write_text(json.dumps(out,indent=2)+'\n')
 print('CLASS_GI_ENTROPY',json.dumps(summary),flush=True)
if __name__=='__main__':main()
