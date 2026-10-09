"""Photonic strict causal-identifiability theorem and sham route.

Two structural causal models yielding the EXACT SAME joint
distribution of all logged (S,G,R,Q,X,Y) detector observables:
H_signal: physical optical nonlinear term theta*S*G*R*Q²;
H_sham: optical nonlinear=0 but electronics or detector produces
same theta*S*G*R*Q².
Random sign assignment alone cannot distinguish, even with
N=infinity, shot clipping, identical detector reference, or larger
sample size. Total variation distance 0, sum of two hypothesis
testing error probabilities >=1; with equal priors >=50% Bayes err.
Break the equivalence via independently certified mechanism:
intervene at an optical output with a *second independent* sensor
whose potential route artifacts can be bounded, or blinded active
sham intervention controlling photonic path separately.

Synthetic exact paired datasets compare raw and clipped readings.
"""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def certificate():
 rng=np.random.default_rng(1808);N=240000
 S=rng.choice([-1,1],N);G=rng.choice([-1,1],N);R=rng.choice([-1,1],N)
 Y=rng.normal(size=N);Q=Y**2-1
 X=rng.normal(size=N);theta=.03
 physical_signal=theta*S*G*R*Q
 null_electronics_artifact=theta*S*G*R*Q
 Z1=X+physical_signal;Z0=X+null_electronics_artifact
 assert np.array_equal(Z1,Z0)
 T=.15;C0=np.clip(Z0,-T,T);C1=np.clip(Z1,-T,T)
 assert np.array_equal(C0,C1)
 # Conditional permutation of labels cannot help when observables
 # are coupled pointwise to the same random source.
 est=float(np.mean(S*G*R*(Z1-X)*Q))
 assert est>0.
 return dict(status='PASS',shots=N,
  causal_models={'signal':'true optical gate sends theta*S*G*R*Q into X; detector electronics clean',
    'sham':'optical gate zero; detector electronics sends theta*S*G*R*Q into X'},
  identical_raw_samples=True,identical_shot_clipped_samples=True,
  observed_threeway_lockin_proxy=est,
  exact_identifiability_theorem='For any choice of randomized (S,G,R,Q) and any noise distribution, adding the same sign-dependent function to the optical field versus to the downstream electronics yields identical law of all downstream detector observables. Hence total-variation distance zero, no test on these outputs can distinguish null/sham from nonlinear optics; Bayes error 1/2 with equal priors even at infinite N.',
  necessary_intervention='Independent causal control of an upstream optical node plus an independently calibrated sensor/reference chain (not merely software shuffling or shot clipping). Document leakage from the actual intervention into electronics. Proposed blinded matched dummy path and sensor swap make new exclusion restrictions experimentally testable.',
  caveat='Mathematical observational equivalence and synthetic exact coupled array, not evidence which mechanism occurs in real equipment. Q is a toy centered intensity proxy.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_optical_threeway_identifiability_nogo.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CAUSAL',d['observed_threeway_lockin_proxy'],d['identical_shot_clipped_samples'])
