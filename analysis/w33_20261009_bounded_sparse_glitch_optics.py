"""Finite-N robust Rademacher optical-sham null against BOTH:
(a) all good detector mismatches |delta_i|<=d, AND
(b) up to m arbitrary, potentially unbounded, treatment-adaptive glitches.
Clip each weighted homodyne statistic at +/-T, then pay an exact worst
case 2*m*T score penalty and 2*T*sqrt(m) norm penalty.
Actual detector independent clipping is essential; result is conditional
on at most m glitches AND a bounded mismatch for other shots.
"""
from pathlib import Path
from math import sqrt,log
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def robust_test(r,q2,Wobs,alpha=.01,T=2.,d=.001,m=40):
  z=np.clip(Wobs,-T,T)
  score=abs(float(r@z))
  # For good indices, |clip(W0)-clip(Wobs)|<=d*q2.
  # On bad indices, at most 2T. Thus a deterministic bound
  # |S0|>=|Sobs|-d Σq2-2mT.
  # ||clip(W0)||2 <= ||z||2 +d||q2||2+2T sqrt(m).
  cutoff=d*float(q2.sum())+2*m*T+sqrt(2*log(2/alpha))*(
      float(np.linalg.norm(z))+d*float(np.linalg.norm(q2))+2*T*sqrt(m))
  return dict(reject=bool(score>cutoff),score=score,cutoff=cutoff,
              observed_fourfold=4*float(r@z)/len(r),threshold_fourfold=4*cutoff/len(r))
def sample(seed,n=240000,signal=False,glitches=40):
  rng=np.random.default_rng(seed)
  r=rng.choice(np.array([-1.,1.]),n)
  py=rng.normal(0,sqrt(.51),n)
  q2=(py*py-.51)**2
  W0=rng.normal(0,sqrt(.8),n)*(py*py-.51)
  theta=(39/20)**2*.05
  if signal:W0+=r*(-theta/sqrt(39))/4
  # Route-dependent bounded mismatch on good shots
  observed=W0+.001*r*q2
  inds=rng.choice(n,glitches,replace=False)
  observed[inds]=100000*r[inds]  # arbitrarily large adversarial false signal
  return robust_test(r,q2,observed,m=glitches)
def certificate():
  seeds=range(24)
  tests={arm:[sample(seed+i*10000,signal=bool(i)) for seed in seeds]
         for i,arm in enumerate(['null_with_arbitrary_sign_glitches','quartic_signal_with_glitches'])}
  counts={name:sum(x['reject'] for x in arr) for name,arr in tests.items()}
  assert counts['null_with_arbitrary_sign_glitches']<=4,counts
  assert counts['quartic_signal_with_glitches']>=12,counts
  stat={k:dict(rejects=counts[k],replicates=len(v),
       median_significance_ratio=float(np.median([x['score']/x['cutoff'] for x in v])),
       first_trial={key:val for key,val in v[0].items()}) for k,v in tests.items()}
  return dict(status='PASS',samples_per_trial=240000,alpha=.01,clipping_T=2,
    bounded_good_shots_delta=.001,max_unbounded_glitches=40,
    fraction_unbounded=40/240000,simulation=stat,
    robust_null_rejection='Let r_i be independent Rademacher assignments and W0_i/Q_i independent of assignments under the sharp optical null. Good observed weighted W_i=W0_i+delta_i*r_i*q2_i, |delta_i|<=d, with at most m otherwise arbitrary/outcome-adaptive contaminated observations. Define z_i=clip(W_i,-T,T). Reject when |Σr_i z_i|>d Σq2_i+2mT+c*(||z||2+d||q2||2+2T sqrt(m)), c=sqrt(2ln(2/alpha)). This controls Type-I error <=alpha for every N, conditional on the stated bounded-contamination assumptions.',
    adversarial_caveat='Guarantee FAILS if more than m glitches, if untrusted q2 values were also altered, or if good W0 depends on randomized signs. Robustness to a bounded number of outliers is not absolute hardware certification.',
    physics_scope='The signal data uses an injected idealized 4-fold mean contrast from prior quartic model, not Maxwell/quantum-optical device simulation or real hardware.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_bounded_sparse_glitch_optics.json').write_text(json.dumps(d,indent=2)+'\n')
  print('CLIP',[(k,v['rejects']) for k,v in d['simulation'].items()])
