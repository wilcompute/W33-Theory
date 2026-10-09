"""Distribution-free *effect size confidence interval* for paired
blinded active/sham path randomization, not only previous null test.

Let Y_j1(a),Y_j2(a) be fixed clipped potential detector outcomes
at optical switch state a=0,1 independently of z_j, with |Y|<=T.
Let r_j be a fixed randomized pump/gate/route sign independent of z.
When z=+1 activate slot1, when z=-1 activate slot2. Then
S=sum_j r_j*z_j*(Y_j1(obs)-Y_j2(obs))
is unbiased for the finite-pair signed clipped causal contrast
M*tau = 1/2 sum_j r_j[(Y_j1(1)-Y_j1(0))+
                      (Y_j2(1)-Y_j2(0))].
Each summand conditioned on potential outcomes has bounded
range [-2T,2T], so Hoeffding:
P(|S/M-tau| > 2T sqrt(2 log(2/alpha)/M))<=alpha.

Bound arbitrary after-randomization fault K shots by +2TK/M
and independently calibrated setting-to-electronics leakage
eta per reading by +2eta. Invert for a simultaneous two-sided
CI on the PHYSICALLY CLIPPED, SIGNED PATH effect tau.
This CI cannot isolate quartic nonlinear optics from other
path-correlated optical effects, cannot estimate unclipped
phase without calibration, and fails without credible eta,K.

Use Round14 seeded stress tests; record lower effect CI.
"""
import math,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_round14_paired_optical_intervention as P
def CI(score,M,T,eta,K,alpha):
 margin=2*eta+2*T*K/M+2*T*math.sqrt(2*math.log(2/alpha)/M)
 return [score/M-margin,score/M+margin]
def certificate():
 M=8000;T=.15;eta=.0004;K=14;alpha=.01
 reports={}
 for mode in ('null','optical','electronics_only'):
  rawmode='optical' if mode=='optical' else 'null'
  seedshift=10000*(mode=='optical')+20000*(mode=='electronics_only')
  dat=[P.trial(234900+i+seedshift,M=M,T=T,eta=eta,K=K,alpha=alpha,mode=rawmode) for i in range(30)]
  intervals=[CI(x['score'],M,T,eta,K,alpha) for x in dat]
  reports[mode]=dict(runs=30,intervals_excluding_zero=sum((lo>0 or hi<0) for lo,hi in intervals),
      median_center=float(np.median([x['score']/M for x in dat])),
      median_lower=float(np.median([p[0] for p in intervals])),
      worst_lower=float(min(p[0] for p in intervals)),
      two_sided_CI_first_run=intervals[0])
 assert reports['optical']['intervals_excluding_zero']==30
 assert reports['null']['intervals_excluding_zero']==0
 assert reports['electronics_only']['intervals_excluding_zero']==0
 margin=2*eta+2*T*K/M+2*T*math.sqrt(2*math.log(2/alpha)/M)
 return dict(status='PASS',M=M,clip_T=T,assumed_max_electronic_leakage_per_reading_eta=eta,
  assumed_max_adversarial_corrupted_raw_shots_K=K,alpha=alpha,
  certified_conservative_two_sided_halfwidth=margin,
  synthetic_sham_and_optical_effect_CIs=reports,
  estimand='Finite-population average r-weighted causal effect of active path on clipped detector outputs, averaged across BOTH possible slot positions; not unclipped optical phase or a specific quartic coefficient.',
  theorem='With baseline clipped potential outcomes fixed independent of random z_j, independent fair z_j, and r_j fixed independently of z_j, E[S]=M tau. Each centered signed contribution is bounded by 2T. Hoeffding gives a two-sided 1-alpha CI S/M +/- 2T sqrt(2log(2/alpha)/M). Unknown post-assignment corruption up to K raw shots adds 2TK/M worst-case bias. Direct switch-correlated electronics up to eta per reading adds 2eta; the resulting enlarged interval contains tau with probability >=1-alpha.',
  physical_falsifiers='A path-specific optical alteration other than the desired nonlinearity can still cause a positive causal effect. If switch leakage or detector corruption count assumptions fail, coverage guarantee fails. Real calibration, blinded sham, path-swapped sensors, and independent optical reference needed before experimental claim.')
if __name__=='__main__':
 d=certificate();(ROOT/'data/w33_20261009_round15_optical_causal_effect_CI.json').write_text(json.dumps(d,indent=2)+'\n')
 print('OPTICAL CIs',d['certified_conservative_two_sided_halfwidth'],[(m,v['intervals_excluding_zero'],v['median_lower']) for m,v in d['synthetic_sham_and_optical_effect_CIs'].items()])
