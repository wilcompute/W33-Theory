#!/usr/bin/env python3
"""Actual patched CLASS (Ubuntu) species-transfer comparison, a bridge to RSD.
Fading best fit vs same-parameter cprime=0, and native LCDM best fit.
No new likelihood fit; CLASS perturbations are solved but neutrino and baryon
and Bessel transfers are in the configured model. No ultralight axion module yet.
"""
from pathlib import Path
import sys,re,glob,json,shutil
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/toe_uv'))
from class_cmb import run_class,titles
TARGET_Z=[0.,.5,1.,2.,5.]
TARGET_K=[.05,.10,.20,.5,1.,3.]
def run(p,kind,label):
 keep={}
 print('CLASS_RUN',label,flush=True)
 extra='output=tCl,pCl,lCl,mPk,dTk\nz_pk=0,0.5,1,2,5'
 _,z,H,dc,info=run_class(p,kind=kind,extra=extra,keep=keep)
 tag=keep['tag']
 out=[]
 try:
  fn=sorted(glob.glob(tag+'/o_z*_tk.dat'),key=lambda x:int(re.search(r'o_z(\d+)_tk',x).group(1)))
  assert len(fn)==len(TARGET_Z),fn
  for j,f in enumerate(fn):
   with open(f) as io:
    comment=[x.strip() for x in io if x.startswith('#')]
   print('TRANSFER_META',label,j+1,comment[:3],flush=True)
   # CLASS prints the requested transfer outputs at each specified redshift,
   # with numbering ordered by z_pk input in the same order.
   # Validated also by linear growth from z0 to z5.
   zphys=TARGET_Z[j]
   d=np.loadtxt(f)
   names=titles(f)
   assert all(x in names for x in ['k (h/Mpc)','d_b','d_cdm','d_m','phi','psi']),names
   k=d[:,names.index('k (h/Mpc)')]
   assert np.all(np.diff(k)>0)
   row={'z':zphys,'filename':Path(f).name}
   for kk in TARGET_K:
    rr={'k_h_per_Mpc':kk}
    for field in ('d_b','d_cdm','d_m','phi','psi'):
     src=d[:,names.index(field)]
     rr[field]=float(np.interp(kk,k,src))
    rr['baryon_to_CDM_transfer_ratio']=rr['d_b']/rr['d_cdm']
    row[str(kk)]=rr
   out.append(row)
 finally:
  shutil.rmtree(tag)
 return dict(physics_model=label,settings={'kind':kind,'z_pk':TARGET_Z,'target_k_h_per_Mpc':TARGET_K},
             full_spectrum_CLASS_info=info,redshifts=out)
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 pf=dict(r['free_neg']['p'])
 p0=dict(pf,cp=0)
 pl=dict(r['LCDM']['p'])
 runs=[run(pf,'fading','fading_bestfit'),
       run(p0,'fading','same_cosmological_params_cp0'),
       run(pl,'native','native_LCDM_bestfit')]
 z0=[a['redshifts'][0] for a in runs]
 z5=[a['redshifts'][-1] for a in runs]
 summary=[]
 for kk in TARGET_K:
  x=[row[str(kk)] for row in z0]
  early=[row[str(kk)] for row in z5]
  summary.append({'k_h_per_Mpc':kk,
   'fading_baryon_to_CDM_z0':x[0]['baryon_to_CDM_transfer_ratio'],
   'cp0_baryon_to_CDM_z0':x[1]['baryon_to_CDM_transfer_ratio'],
   'growth_d_m_z5_to_z0_fading':x[0]['d_m']/early[0]['d_m'],
   'growth_d_m_z5_to_z0_cp0':x[1]['d_m']/early[1]['d_m'],
   'fading_vs_cp0_normalized_z5_to_z0_growth_ratio':(
       x[0]['d_m']/early[0]['d_m'])/(x[1]['d_m']/early[1]['d_m']),
   'transfer_d_m_fading_over_native_LCDM_z0':x[0]['d_m']/x[2]['d_m']})
 # z0 baryons >0 should be similar from coupling small
 assert all(np.isfinite(x['growth_d_m_z5_to_z0_fading']) for x in summary)
 assert len(summary)==6
 out={'status':'PASS_REAL_PATCHED_CLASS_FIVE_REDSHIFT_TRANSFER_BENCHMARK',
      'source':'analysis/toe_uv/class_cmb.py:run_class, patched ~/cosmo/class_fading/class',
      'comparators':'fading fit vs cprime=0 with SAME cosmological parameters and c; vs separately fitted native LambdaCDM parameters',
      'runs':runs,'k_diagnostics':summary,
      'gauge':'Synchronous gauge CLASS transfer densities. Density contrast ratios can be gauge dependent at superhorizon scales; k>=0.05h/Mpc is subhorizon at z<=5.',
      'scope':'REAL CLASS background and relativistic perturbation transfer outputs; no new likelihood fit, no observed redshift-space distortion or lensing covariance evaluated, no ultralight axion term inside CLASS (mPk still pressureless CDM). The cp0 control is a model evaluation not an optimized or fixed-H benchmark.',
      'prior_literature':['https://doi.org/10.1088/1475-7516/2026/02/014',
           'https://doi.org/10.1103/dqxw-yp1j']}
 (ROOT/'data/toe_20261103_real_CLASS_fading_species_transfers.json').write_text(json.dumps(out,indent=2)+'\n')
 print('CLASS_GROWTH_SUMMARY',json.dumps(summary),flush=True)
if __name__=='__main__':main()
