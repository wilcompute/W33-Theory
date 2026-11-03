#!/usr/bin/env python3
"""Phase resolution and condition-number falsifier for the fixed W33 216-port POVM.
Research provenance: Nov 3 three-setting complex IC and failed three 2-bit trials.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.linalg import eigvalsh
from contextlib import nullcontext

def threadpool_limits(limits):
 return nullcontext()  # set OPENBLAS_NUM_THREADS in process environment instead
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261103_three_setting_ic_povm import embed_effects
def main():
 Z,_=route_frame();w,Q=np.linalg.eigh((Z.T@Z).astype(float))
 V=Z@Q[:,16:]/math.sqrt(360)
 for j in range(24):
  if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
 assert np.linalg.norm(V.T@V-np.eye(24))<1e-9
 rng=np.random.default_rng(20261105);F0=embed_effects(V,np.eye(24))
 out=[]
 with threadpool_limits(limits=2):
  for bits in (2,3,4,6,10,0):
   best=None
   for tr in range(5 if bits in (2,3,4) else 2):
    if bits:
     m1=rng.integers(0,2**bits,24);m2=rng.integers(0,2**bits,24)
     a=2*np.pi*m1/(2**bits);b=2*np.pi*m2/(2**bits)
    else:a=rng.uniform(0,2*np.pi,24);b=rng.uniform(0,2*np.pi,24)
    F=np.vstack((F0,embed_effects(V,np.diag(np.exp(1j*a))),
          embed_effects(V,np.diag(np.exp(1j*b)))))
    gram=F.T@F
    eig=eigvalsh(gram,overwrite_a=True,check_finite=False)
    # eigen threshold relative to max eigen; condition of FRAME itself sqrt().
    rank=int(np.sum(eig>max(eig[-1]*1e-11,1e-15)))
    cond=float(np.sqrt(eig[-1]/eig[0])) if eig[0]>0 else None
    rec={'bits':bits,'trial':tr,'rank':rank,'frame_condition':cond,
       'min_eigenvalue':float(eig[0]),'max_eigenvalue':float(eig[-1]),
       'phase_exponents_1':m1.tolist() if bits else None,
       'phase_exponents_2':m2.tolist() if bits else None}
    if best is None or (rank, eig[0])>(best['rank'],best['min_eigenvalue']):best=rec
    print('PHASE_DEPTH',bits,tr,rank,cond,flush=True)
   out.append(best)
  # Numerical Monte Carlo with selected best discrete complete design.
  good=[r for r in out if r['rank']==576 and r['bits']>0]
  if good:
   best=min(good,key=lambda z:z['frame_condition'])
   b=best['bits'];a=2*np.pi*np.array(best['phase_exponents_1'])/(2**b)
   t=2*np.pi*np.array(best['phase_exponents_2'])/(2**b)
   f=np.vstack((F0,embed_effects(V,np.diag(np.exp(1j*a))),embed_effects(V,np.diag(np.exp(1j*t)))))
   gram=f.T@f
   # Local Fisher at maximally mixed, each setting 1/216 for each outcome;
   # multinomial Fisher on traceless subspace is 216*N*f.T*f for N shots/setting.
   # Using orthonormal Hermitian-coordinate basis, the trace/identity direction
   # is constrained. Here give unconstrained Gram condition, not CRB.
   l=eigvalsh(gram,overwrite_a=True,check_finite=False)
   assert l[0]>1e-12
   bestpick={k:v for k,v in best.items()}
  else:bestpick=None
 result={'status':'PASS_EXPLORATORY_BITDEPTH_RANK_SWEEP',
 'source_216_effects_rank':201,'Hermitian_space_dimension':576,
 'settings':3,'sampled_best_per_bitdepth':out,'best_complete_discrete_design':bestpick,
 'numeric_rank_tolerance':'Gram eigenvalue > max(1e-11*maxGramEig,1e-15)',
 'scope':'Seeded finite sample of phase masks, not an exhaustive 2-bit impossibility proof; incomplete designs have no finite frame condition. Deterministic optical mode basis chosen by numpy.eigh; calibration and detector losses still unmodeled.'}
 (ROOT/'data/w33_20261103_phase_bitdepth_condition.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PHASE_BITDEPTH_DONE',json.dumps([{k:v for k,v in a.items() if not k.startswith('phase_exponents')} for a in out]),flush=True)
 return result
if __name__=='__main__':main()
