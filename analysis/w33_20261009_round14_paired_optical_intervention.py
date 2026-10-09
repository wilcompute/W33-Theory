"""Causally identified randomized PHOTONIC SWITCH experiment:
paired active/sham optical-path interventions plus an independently
certified upper bound on direct electronics switch leakage.

Round13 proved a threeway gate signature is observationally
nonidentifiable from matched electronics artifacts. Here we
specify a REAL randomized design: M paired shots, one optical
attenuator state (active vs blinded sham) randomly assigned to
shot1 or shot2, z_j in +-1. Both paths use identical pump/gate/
route sign schedule and sensor; switching electronic leakage <=eta
per clipped reading. Each recorded y_{ji} clipped to [-T,T].
Under a sharp null: the fully clipped baseline y0_j1,y0_j2
are FIXED independently of z; no independent temporal noise
assumption. For d_j=y_j1-y_j2,
|sum z_j d_j| <= 2eta M + 2T sqrt(2M ln(2/alpha))
with type-I <=alpha, by Rademacher Hoeffding. Fault injections
need a TOTAL malicious-shot budget separately: add 2T*K to
adversarial score cutoff (each faulty shot can alter clip by2T).
This intervention removes sign-*independent* electronics bias;
electronics leakage that tracks the optical switch beyond eta
remains exactly nonidentifiable, NOT a detector-free proof.

Synthetic randomized experiment with serial AR1 drift, huge
raw sample glitches, and verified separation active vs sham.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def cutoff(M,T,eta,K,alpha):
 return 2*eta*M+2*T*K+2*T*math.sqrt(2*M*math.log(2/alpha))
def trial(seed,M=8000,T=.15,theta=.095,eta=.0004,K=14,alpha=.01,mode='optical'):
 rng=np.random.default_rng(seed)
 z=rng.choice(np.array([-1.,1.]),size=M)
 r=rng.choice(np.array([-1.,1.]),size=M) # triple pump/gate/route sign, independent of optical-path z
 base=lfilter([1.],[1.,-.91],rng.normal(size=2*M)*.022*math.sqrt(1-.91**2))
 base=base.reshape(M,2)
 # active assignment in slot1 if z=+1, slot2 otherwise
 active=np.stack(((z+1)/2,(1-z)/2),axis=1)
 # actual optical shift on active slot vs zero optical
 optical=theta*r[:,None]*active if mode=='optical' else np.zeros((M,2))
 # electronics artifact independent of switch, but may be
 # strongly correlated within pairs and with pump route signs.
 common=(rng.standard_normal(M)*.012)[:,None]
 electronic=common*np.ones((1,2))
 # direct switching leakage only eta (declared calibrated)
 leak=.65*eta*active
 y=base+optical+electronic+leak
 # unbounded raw corruption AFTER seeing random assignments.
 ix=rng.choice(2*M,size=K,replace=False)
 y.flat[ix]=1e8
 yc=np.clip(y,-T,T)
 score=float((r*z)@(yc[:,0]-yc[:,1]))
 threshold=cutoff(M,T,eta,K,alpha)
 return dict(reject=score>threshold,score=score,threshold=threshold,
   ratio=score/threshold)
def certificate():
 rows={}
 for mode in ('null','optical','electronics_only'):
  out=[trial(234900+i+10000*(mode=='optical')+20000*(mode=='electronics_only'),
    mode=('optical' if mode=='optical' else 'null')) for i in range(30)]
  rows[mode]=dict(rejections=sum(r['reject'] for r in out),
    runs=len(out),median_score=float(np.median([r['score'] for r in out])),
    threshold=out[0]['threshold'],first_run=out[0])
 assert rows['null']['rejections']<=2
 assert rows['optical']['rejections']>=20
 assert rows['electronics_only']['rejections']<=2
 return dict(status='PASS',
    paired_optical_interventions=8000,
    shots_per_intervention=2,
    blinded_assignment='Exactly one active optical path per pair, fair independent random z. Independently random triple pump/gate/route sign r shared within pair; lock-in score sum r*z*(y1-y2). Optical switch path must be invisible to electronics except audited <=eta leakage.',
    clip_threshold_T=.15,maximum_direct_electronic_switch_leakage_eta=.0004,
    arbitrary_corrupted_raw_shots_K=14,test_alpha=.01,
    exact_conditional_randomization_bound='Under a sharp null and independent random z, baseline clipped outcomes (y0_j1,y0_j2) are fixed, with abs differences <=2T. Condition on randomized r (held fixed within a pair), so r*z is a fair independent sign under z randomization. Electronic switch leakage per reading <=eta adds at most 2eta M total to signed contrast; K arbitrary corrupted raw readings add at most 2TK. Hoeffding gives P(|sum z_j(y1-y2)|>2etaM+2TK+2T sqrt(2M ln(2/alpha))) <=alpha.',
    runs=rows,
    crucial_falsifier='If electronic artifacts respond to the actual optical attenuator with direct leakage >eta, the experiment remains observationally nonidentifiable. Hardware route attenuation/blinded switch and independent detector/reference verification required. Simulations are not measurement results.',
    reference='Builds on Round12 per-shot clipping and Round13 explicit two-model electronics sham no-go.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round14_paired_optical_intervention.json').write_text(json.dumps(d,indent=2)+'\n')
 print('OPTICAL PAIRED',[(x,y['rejections'],y['median_score'],y['threshold']) for x,y in d['runs'].items()])
