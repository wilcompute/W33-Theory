#!/usr/bin/env python3
"""2-bit-only phase tomography and an imaginary-coherence witness."""
import sys,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import svdvals
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_five_deeper_fronts import route_frame
from w33_20261103_three_setting_ic_povm import embed_effects
def main():
 Z,_=route_frame();e,Q=np.linalg.eigh((Z.T@Z).astype(float))
 V=Z@Q[:,16:]/math.sqrt(360)
 for j in range(24):
  if V[np.argmax(abs(V[:,j])),j]<0:V[:,j]*=-1
 rng=np.random.default_rng(20261104)
 base=embed_effects(V,np.eye(24,dtype=complex))
 trials=[];winner=None
 for k in range(3):
  a=rng.integers(0,4,24);b=rng.integers(0,4,24)
  rows=np.vstack((base,embed_effects(V,np.diag(1j**a)),
                       embed_effects(V,np.diag(1j**b))))
  s=svdvals(rows,check_finite=False)
  rk=int(np.sum(s>1e-9))
  trials.append({'trial':k,'real_Hermitian_span_rank':rk,
    'condition_number':float(s[0]/s[-1]) if s[-1]>1e-12 else None})
  if rk==576 and winner is None:winner=[a.tolist(),b.tolist()]
  print('TWO_BIT',trials[-1],flush=True)
 # Real POVM E has zero sensitivity to imaginary coherences;
 # a single 90-degree prephase unlocks one explicit witness.
 B=np.zeros((24,24),complex);B[0,1]=1j;B[1,0]=-1j
 eps=1/48
 rp=np.eye(24)/24+eps*B;rm=np.eye(24)/24-eps*B
 assert min(np.linalg.eigvalsh(rp))>0
 def pr(D,rho):
  W=V@D
  return np.einsum('si,ij,sj->s',W.conj(),rho,W).real
 p0=pr(np.eye(24),rp);q0=pr(np.eye(24),rm)
 phases=np.ones(24,complex);phases[1]=1j
 p1=pr(np.diag(phases),rp);q1=pr(np.diag(phases),rm)
 tv0=float(np.abs(p0-q0).sum()/2)
 tv1=float(np.abs(p1-q1).sum()/2)
 assert tv0<1e-12 and tv1>0.02
 out={'status':'PASS_IMAGINARY_WITNESS_QUANTIZED_PHASE_LIMITED_TRIALS',
      'two_bit_phase_trials':trials,
      'three_settings_complete_with_two_bit_phases':winner is not None,
      'winning_phase_exponents_for_settings_2_3':winner,
      'imaginary_coherence_witness_no_phase_TV':tv0,
      'imaginary_coherence_witness_with_one_90deg_phase_TV':tv1,
      'states':'rho±=I24/24 ±(i/48)(|0><1|-|1><0|)',
      'scope':'Numerical rank and a basis-dependent imaginary coherence pair; not physical CP parity violation, not a calibrated or loss-tolerant optical experiment.'}
 (ROOT/'data/w33_20261103_two_bit_phase_witness.json').write_text(json.dumps(out,indent=2)+'\n')
 print('TWO_BIT_FINAL',json.dumps(out)[:3300],flush=True)
 return out
if __name__=='__main__':main()
