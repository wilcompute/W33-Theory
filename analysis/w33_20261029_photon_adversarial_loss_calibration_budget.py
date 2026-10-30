#!/usr/bin/env python3
"""Conservative W33/dual optical hypothesis test under bounded independent
adversarial complex photon Gram, full-threefold survival, optical transfer
matrix error and hypothesis-dependent spurious event probability.
No mode-dependent loss, correlated trials, or arbitrary detector process claim.
"""
import json
import numpy as np
from scipy.stats import binom
DEN=15**6
WMIN=17496/DEN
DMAX=6752/DEN
ALPHA=.001

def model(eta,eps,beta):
 r=eta**3
 wlow=r*(WMIN-3*eps)
 dhigh=DMAX+3*eps+beta
 assert 0<=eps and 0<=beta and 0<eta<=1
 return wlow,dhigh

def min_trials(pw,pd,limit=400000):
 if not (0<=pd<pw<=1):return dict(status="NO_WORST_CASE_SEPARATION")
 N=np.arange(1,limit+1)
 k=np.asarray(binom.isf(ALPHA,N,pd),np.int64)+1
 fp=binom.sf(k-1,N,pd)
 k+=(fp>=ALPHA)
 fp=binom.sf(k-1,N,pd)
 fn=binom.cdf(k-1,N,pw)
 valid=(k<=N)&(fp<ALPHA)&(fn<ALPHA)
 if not valid.any():return dict(status="NO_CERTIFIED_N_WITHIN_LIMIT",limit=limit)
 i=int(np.flatnonzero(valid)[0])
 assert not valid[:i].any()
 return dict(status="PASS",emitted_trials=int(N[i]),minimum_count_cutoff=int(k[i]),
   false_positive=float(fp[i]),false_negative=float(fn[i]),
   exhaustive_range=[1,int(N[i])],per_hypothesis_error_strictly_below=ALPHA)

def verify():
 cases=[(1.,0.,0.,43047,43),
        (.95,1e-5,5e-5,95513,91),
        (.9,0.,1e-4,187342,167),
        (.98,2e-5,1e-4,98767,103)]
 rows=[]
 for eta,eps,beta,n,k in cases:
  w,d=model(eta,eps,beta)
  r=min_trials(w,d)
  assert (r["emitted_trials"],r["minimum_count_cutoff"])==(n,k)
  rows.append(dict(eta_min=eta,device_opnorm_error_max=eps,
    upper_spurious_event_prob=beta,
    guaranteed_W_event_lower=w,guaranteed_dual_event_upper=d,stats=r))
 threshold_eta=(DMAX/WMIN)**(1/3)
 assert .7<threshold_eta<.8
 return dict(status="PASS",W33_ideal_event_lower=WMIN,
    dual_ideal_event_upper=DMAX,
    source="independently chosen arbitrary complex photon Gram states for W33 vs dual, independent photons",
    conservative_model="W success >= eta^3*(WMIN-3 eps); dual success <= DMAX+3 eps+beta",
    separation_criterion="eta^3*(WMIN-3 eps)>DMAX+3 eps+beta",
    eta_threshold_if_eps_beta_zero=threshold_eta,
    epsilon_threshold_for_eta_given_beta="(eta^3*WMIN-DMAX-beta)/(3*(1+eta^3))",
    backgrounds="beta bounds false event probability additively only; no event-loss coupling and independent trials",
    independent_nonidentically_distributed_trials=True,
    proof_of_error_control="independent Poisson-binomial tails bounded by the two binomial endpoint tails via coordinatewise stochastic monotonicity",
    cases=rows,
    caveats="No correlated trials, arbitrary mode-specific postselection, unknown loss calibration, hypothesis-dependent unbounded dark events, multipair sources, or physical TOE prediction.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
