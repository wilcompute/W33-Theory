"""Shot-level clipping + frame-level Rademacher optical test. This
improves previous one-bad-FRAME rule by converting arbitrarily high
raw spikes into a finite score budget per corrupted SHOT.

Frames r_b independently randomized. y0_{bi} sharp-null clean
pre-clip weights independent of ALL r. For good shots:
yobs=y0 + r_b*delta_b*Q², |delta_b|<=d. Up to M bad raw
observations arbitrary even AFTER learning sign, Q² trusted.
Clip each yobs to [-T,T] BEFORE averaging L shots per frame.
Then |sum r_b(zobs_b-z0_b)| <= e1=d sum_b mean Q²+2TM/L,
||zobs-z0||2<=e2=d||mean Q²||2+2TM/L.
A Rademacher bound on z0 gives valid level-alpha rejection:
|r.zobs| > e1+sqrt(2 log(2/alpha)) (||zobs||2+e2).
Arbitrary serial correlation of y0 allowed because sign-blocks are
randomized independently of clean data, not sampled IID.

This is mathematical/simulation, not optical chip demonstration.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def decision(r,clipped_frame_means,frame_Q2,bad_shots,d=.001,T=.15,L=200,alpha=.01):
 e1=d*float(frame_Q2.sum())+2*T*bad_shots/L
 e2=d*float(np.linalg.norm(frame_Q2))+2*T*bad_shots/L
 score=abs(float(r@clipped_frame_means))
 cutoff=e1+math.sqrt(2*math.log(2/alpha))*(float(np.linalg.norm(clipped_frame_means))+e2)
 return dict(reject=bool(score>cutoff),score=score,threshold=cutoff,ratio=score/cutoff)
def trial(seed,alt=False,frames=1200,shots=200,bad_shots=40,T=.15):
 rng=np.random.default_rng(seed);N=frames*shots
 r=rng.choice(np.array([-1.,1.]),size=frames)
 py=rng.normal(0,math.sqrt(.51),N);q=py*py-.51;Q2=q*q
 eps=lfilter([1.],[1.,-.85],rng.normal(0,.2*math.sqrt(1-.85**2),N))
 clean=eps*q
 obs=clean + .001*np.repeat(r,shots)*Q2
 theta=(39/20)**2*.05/math.sqrt(39)
 if alt:obs=obs-np.repeat(r,shots)*theta/4
 bad=rng.choice(N,bad_shots,replace=False)
 obs[bad]=1e8*np.repeat(r,shots)[bad]
 clip=np.clip(obs,-T,T).reshape(frames,shots).mean(axis=1)
 return decision(r,clip,Q2.reshape(frames,shots).mean(axis=1),bad_shots,L=shots,T=T)
def certificate():
 rows={}
 for alt in (False,True):
  rs=[trial(134911+j+100000*int(alt),alt=alt) for j in range(36)]
  rows['signal_proxy' if alt else 'no_optical_signal']=dict(n=len(rs),rejections=sum(z['reject'] for z in rs),
    median_ratio=float(np.median([z['ratio'] for z in rs])),first=rs[0])
 assert rows['no_optical_signal']['rejections']<=3
 return dict(status='PASS',frames=1200,shots_per_frame=200,
  corrupted_shots_arbitrary=40,total_shots=240000,clip_per_shot_T=.15,
  seeded_runs=rows,
  adversary_spike_value='1e8 times randomized frame sign, chosen after randomization',
  theory='For clean clip-frame-vector z0 independent of randomized r, with at most M arbitrary bad raw shots and |good detector mismatch|<=dQ2, the fully clipped frame vector zobs obeys ||zobs-z0||1<=d sum Q2bar+2TM/L and ||zobs-z0||2<=d||Q2bar||2+2TM/L. Hoeffding on r.z0 gives unconditional sharp-null Type-I <=alpha with data-adaptive safe cutoff e1+sqrt(2ln(2/alpha))*(||zobs||2+e2). No independent glitches or noise samples are needed.',
  hardware_requirements='Requires trusted every-shot clipping before frame means, trusted Q2, a credible bound M on total arbitrary shot corruption OR a physical upper amplitude cap. Without a certified bound, effective false positive protection is not claimed. Strongly correlated clean detector drift is allowed only if independent of randomized signs.',
  signal_boundary='Synthetic quartic proxy injected in detector observations; no observed optical nonlinearity, gate or self-entangled photon.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_shot_clipped_frame_optics.json').write_text(json.dumps(d,indent=2)+'\n')
 print('CLIPPED OPTICS',[(k,v['rejections'],v['n'],v['median_ratio']) for k,v in d['seeded_runs'].items()])
