"""Invert a finite-sample randomized sign test into a confidence interval
for a CONSTANT sham-transfer mismatch delta. Arbitrary temporal
correlations in noise are permitted if independent of random route signs.
This cannot certify a per-shot sup-norm mismatch without assumptions.
"""
from pathlib import Path
import json
from math import sqrt,log
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def one(seed,n,delta=.003,alpha=.01):
  rng=np.random.default_rng(seed)
  r=rng.choice([-1.,1.],n).astype(float)
  z=rng.normal(0,sqrt(.5),n)
  Q=(z+rng.normal(0,.1,n))**2-.51
  # detector fluctuations correlated across time; independent assignment
  eps=lfilter([1],[1,-.98],rng.normal(0,sqrt(.8*(1-.98**2)),n))
  Y=delta*r*Q+eps
  U=r*Q
  A=float(Q@Q);B=float(U@Y)
  C=float((Q*Y)@(Q*Y))
  D=float((r*Q*Q*Q)@Y)
  E=float((Q*Q)@(Q*Q))
  c2=2*log(2/alpha)
  aa=A*A-c2*E;bb=-2*(A*B-c2*D);cc=B*B-c2*C
  disc=bb*bb-4*aa*cc
  assert aa>0 and disc>=0
  lo=(-bb-sqrt(disc))/(2*aa);hi=(-bb+sqrt(disc))/(2*aa)
  assert lo<delta<hi
  return dict(n=n,true_delta=delta,point_estimate=B/A,
        confidence_interval=[lo,hi],width=hi-lo,
        calibration_sign_rademacher=True)
def certificate():
  samples=[one(1234+i,n) for i,n in enumerate((50000,200000,1000000))]
  theta=(39/20)**2*.05
  optical_signal=theta/sqrt(39)
  slope=4*(2*(.51**2))
  nuisance_limit=optical_signal/slope
  hypothetical=[dict(shots=N,prob_zero_spikes=(1-1/(10*N))**N,
           possible_unobserved_outlier_magnitude='unbounded') for N in (50000,200000,1000000)]
  return dict(status='PASS',alpha=.01,
       samples=samples,
       matched_sham_criterion='constant delta confidence inversion; test any delta0 using |sum r_i Q_i(Y_i-delta0*r_i*Q_i)| <= sqrt(2log(2/alpha)*sum Q_i^2(Y_i-delta0*r_i Q_i)^2). Invert the quadratic, endpoints given.',
       finite_sample_guarantee='For deterministic fixed Q, epsilon independent of assigned Rademacher r (temporal correlation permitted), inversion has >=1-alpha coverage of common delta.',
       exactly_signal_equivalent_mismatch=nuisance_limit,
       mismatch_threshold_referenced_to_prior='Idealized optical signal divided by 4 E[(P_Y^2-.51)^2]',
       important_impossibility='No finite randomized calibration dataset can, without a boundedness or regularity assumption on delta_i, certify a deterministic worst-case per-shot |delta_i|<=d. An arbitrarily rare, arbitrarily large route-sensitive detector outlier can remain unobserved.',
       rare_outlier_counterexamples=hypothetical,
       scope='Seeded Gaussian AR1 illustrative calibration. Common parameter delta is an assumption. The earlier robust detector null requires per-shot bound, not merely this confidence interval.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_randomized_sham_CI.json').write_text(json.dumps(d,indent=2)+'\n')
  print('SHAMCI',[(a['n'],a['confidence_interval']) for a in d['samples']])
