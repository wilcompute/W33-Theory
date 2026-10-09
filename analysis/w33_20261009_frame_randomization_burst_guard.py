"""Burst-resistant photonic randomization at the FRAME level.

Rademacher route/pump sign independently assigned to each FRAME, not
each temporally correlated shot. Arbitrary within-frame and between-
frame noise correlation allowed under sharp null, independent of signs.

Detector transfer mismatch |delta_frame|<=d on all good frames,
and <=m entirely compromised frames (any amplitude, adaptive sign).
Clip each frame-AVERAGED weighted statistic at +/-T, apply exact
finite sample conditional Rademacher bound plus 2mT adversarial cost.

Synthetic optical signal is an injected quartic-contrast proxy, not
a real device or full quantum-optical wave simulation.
"""
from pathlib import Path
import json
import numpy as np
from scipy.signal import lfilter
from math import sqrt,log
ROOT=Path(__file__).resolve().parents[1]
def decision(r,Q2,W,d=.001,m=1,T=.15,alpha=.01):
 z=np.clip(W,-T,T)
 c=sqrt(2*log(2/alpha))
 score=abs(float(r@z))
 cutoff=d*float(sum(Q2))+2*m*T+c*(float(np.linalg.norm(z))+
      d*float(np.linalg.norm(Q2))+2*T*sqrt(m))
 return dict(rejected=bool(score>cutoff),score=score,cutoff=cutoff,
   ratio=score/cutoff)
def trial(seed,signal=False,frames=1200,shots=200,glitches=1):
 rng=np.random.default_rng(seed)
 signs=rng.choice(np.array([-1.,1.]),frames)
 N=frames*shots
 py=rng.normal(0,sqrt(.51),N)
 q=py*py-.51
 # Strong serial correlations across all samples, within and across
 # adjacent frame boundaries; no IID noise assumption.
 eps=lfilter([1.], [1.,-.85],rng.normal(0,.2*sqrt(1-.85**2),N))
 raw=eps*q
 w0=np.mean(raw.reshape(frames,shots),axis=1)
 q2=np.mean((q*q).reshape(frames,shots),axis=1)
 theta=(39/20)**2*.05/sqrt(39)
 if signal:w0+=signs*(-theta/4)
 obs=w0+signs*.001*q2
 chosen=rng.choice(frames,glitches,replace=False)
 obs[chosen]=100000*signs[chosen]
 return decision(signs,q2,obs,m=glitches)
def certificate():
 counts={}
 rows={}
 for key,alt in [('null_adversarial_single_bad_frame',False),
                 ('quartic_proxy_single_bad_frame',True)]:
  trials=[trial(200000*i+12345+z,signal=alt) for z in range(24) for i in [int(alt)]]
  n=sum(x['rejected'] for x in trials)
  counts[key]=n
  rows[key]=dict(rejects=n,replicates=len(trials),
    median_score_over_cutoff=float(np.median([x['ratio'] for x in trials])),
    first_trial=trials[0])
 assert counts['null_adversarial_single_bad_frame']<=3
 # Do not force an optimistic power claim; record observed power honestly.
 return dict(status='PASS',independent_randomized_frames=1200,
    shots_per_frame=200,total_shots=240000,
    temporal_ar1_rho=.85,uncorrupted_noise_amplitude=.2,
    frame_clip_T=.15,allow_adaptive_fully_corrupted_frames=1,
    good_frame_mismatch_bound=.001,nominal_alpha=.01,
    simulation=rows,
    finiteN_theorem='Under a sharp null independent of all Rademacher frame assignment signs, arbitrary temporally correlated clean frame weights W0 and trusted Q2, and at most m adaptively altered frame weights with |delta_i|<=d for all others, clip W at +/-T and reject iff |sum r_i clip(Wobs_i)|>d sum Q2_i+2mT+sqrt(2log(2/alpha))*(||clip(Wobs)||2+d||Q2||2+2T sqrt(m)). This has conditional Type-I rate <= alpha at every number of frames.',
    distinction='Frame-level randomization tolerates correlations within shots and across frames, but protects only a certified COUNT of compromised frames. Cluster randomization lowers effective number of independent signs and may reduce power compared to independently sign-randomizing shots.',
    failure_modes='An unmonitored burst spanning more than m frames, randomization-dependent clean drift, corrupted Q2, unbounded good-frame mismatch, or an adversary predicting sign assignments invalidates the guarantee. This is a synthetic implementation test, NOT photonic hardware.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_frame_randomization_burst_guard.json').write_text(json.dumps(d,indent=2)+'\n')
 print('BURST GUARD',[(k,v['rejects'],v['median_score_over_cutoff']) for k,v in d['simulation'].items()])
