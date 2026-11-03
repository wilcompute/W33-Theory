#!/usr/bin/env python3
"""Real CLASS linear sigma8(z), growth and one public 2026 DR1 PV RSD point.

Uses the available patched CLASS+Planck environment; computes sigma8 from
the linear mPk outputs at five redshifts instead of using f~Omega^0.55.
Data point from 2026 DESI DR1 Peculiar Velocity Survey consensus at z=.07,
f sigma8=0.450 +/- 0.055. This is ONE Gaussian diagnostic, not survey likelihood.
"""
from pathlib import Path
import json,re,glob,shutil,sys,math
import numpy as np
from scipy.integrate import simpson
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/toe_uv'))
from class_cmb import run_class
ZS=[0.0,0.04,0.06,0.07,0.08,0.10,0.15]
K=[.05,.10,.20,.35]
def sigma8(pk):
 k=pk[:,0];P=pk[:,1]
 z=8*k
 W=np.ones_like(z)
 m=z>1e-4
 W[m]=3*(np.sin(z[m])-z[m]*np.cos(z[m]))/z[m]**3
 W[~m]=1-z[~m]**2/10+z[~m]**4/280
 return math.sqrt(float(simpson((k**3)*P*W*W/(2*math.pi**2),x=np.log(k))))
def run(p,kind,label):
 keep={}
 print('START_RSD_CLASS',label,flush=True)
 extra='output=tCl,pCl,lCl,mPk,dTk\nz_pk='+','.join(str(z) for z in ZS)+'\nnon_linear=none'
 _,z,H,dc,info=run_class(p,kind=kind,extra=extra,keep=keep)
 root=keep['tag']
 records=[]
 try:
  pf=sorted(glob.glob(root+'/o_z*_pk.dat'),key=lambda f:int(re.search(r'_z(\d+)_pk',f).group(1)))
  tf=sorted(glob.glob(root+'/o_z*_tk.dat'),key=lambda f:int(re.search(r'_z(\d+)_tk',f).group(1)))
  assert len(pf)==len(tf)==len(ZS),(pf,tf)
  for i,(fp,ft) in enumerate(zip(pf,tf)):
   with open(fp) as t: h=[s.strip() for s in t if s.startswith('#')]
   print('PK_HEADER',label,i+1,h[:2],flush=True)
   pk=np.loadtxt(fp)
   transfer=np.loadtxt(ft)
   # CLASS tk convention col: k,d_g,d_b,d_cdm,d_ur,d_ncdm,d_scf,d_m
   k=transfer[:,0]
   delta=np.interp(K,k,transfer[:,7])
   records.append({'z':ZS[i],'sigma8_linear_from_integral':sigma8(pk),
                   'matter_delta_k':{str(w):float(v) for w,v in zip(K,delta)}})
 finally:
  shutil.rmtree(root)
 sig=[r['sigma8_linear_from_integral'] for r in records]
 # sciPy integrate log-k should reproduce CLASS's sigma8 at z0
 calib=(sig[0]-info['s8'])/info['s8']
 print('SIGMA8_CHECK',label,sig[0],info['s8'],calib,flush=True)
 assert abs(calib)<.01,(label,calib)
 smap={r['z']:r['sigma8_linear_from_integral'] for r in records}
 z0=.07;step=.01
 # z=.06/.08 central derivative of sigma8, which is sigma8-weighted
 # growth rate fsigma8 if linear D(k,z).
 fs8=-(1+z0)*(smap[.08]-smap[.06])/(.08-.06)
 fs8_central=-(1+z0)*(smap[.08]-smap[.06])/(.08-.06)
 # Single public PV observation, reported symmetric consensus width.
 obs=.450;std=.055
 diagnostics={'f_sigma8_at_z0p07':fs8,
  'observed_DESI_DR1_PV_z0p07':obs,'reported_consensus_sigma':std,
  'Gaussian_single_point_chi2':((fs8-obs)/std)**2,
  'sigma8_z0p07':smap[.07],
  'calibrated_sigma8_z0_vs_CLASS_info_relative_error':calib}
 return {'label':label,'parameters':p,'info':info,'spectrum':records,'diagnostics':diagnostics}
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 fading=dict(r['free_neg']['p'])
 off=dict(fading,cp=0.)
 native=dict(r['LCDM']['p'])
 models=[run(fading,'fading','fading_fit'),
         run(off,'fading','fixed_params_cprime_zero'),
         run(native,'native','native_LCDM_independently_fitted')]
 rr=[m['diagnostics']['f_sigma8_at_z0p07'] for m in models]
 out={'status':'PASS_REAL_CLASS_LINEAR_SIGMA8_AND_SINGLE_POINT_DR1_PV_CHECK',
 'source': 'Existing analysis/toe_uv/class_cmb.py : run_class using patched CLASS under Ubuntu',
 'models':models,'public_RSD_reference':'DESI DR1 Peculiar Velocity Survey consensus f sigma8 (z_eff=.07)=.450 +/- .055, Astronomy & Astrophysics 2026 A&A doi 10.1051/0004-6361/202558368',
 'fading_vs_same_params_zero_cprime_delta_fsigma8':rr[0]-rr[1],
 'fading_vs_native_LCDM_different_fit_delta_fsigma8':rr[0]-rr[2],
 'precision_required_for_one_sigma_distinguishing_coupling_with_single_fsigma8_point':abs(rr[0]-rr[1]),
 'real_likelihood_evaluated':'NO: uses one Gaussian consensus datum without survey window/AP corrections, non-Gaussian posterior, nuisance or full public covariance',
 'physics_scope':'Linear pressureless CDM CLASS model. Does NOT include coupled ultralight axion in CLASS. The signed delta between separately fitted LCDM and fading mixes cosmological background shifts. The fixed-parameter zero-coupling control is not refitted; observed PV datum may have priors and overlaps with previously used observations.',
 'external_reference':'https://doi.org/10.1051/0004-6361/202558368'}
 (ROOT/'data/toe_20261103_class_PV_real_RSD_singlepoint.json').write_text(json.dumps(out,indent=2)+'\n')
 print('RSD_RESULT',json.dumps([{'model':m['label'],**m['diagnostics']} for m in models]),flush=True)
if __name__=='__main__':main()
