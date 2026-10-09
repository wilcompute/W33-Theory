"""Finite-N conditional random-sign test for two-mode nonlinear homodyne.

Under the sharp null that the preassigned pump-sign s_i cannot change
the measured readouts, conditioned on arbitrary noisy outcome weights w_i
(including temporally correlated classical drift), Hoeffding gives
P(|sum s_i w_i|>=t | w) <=2 exp(-t²/(2 sum w_i²)).
This is exact finite-N type-I control, not asymptotic Gaussian tails.
"""
from pathlib import Path
import json
from math import sqrt,log
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def stat(s,px,py,alpha=.01):
    yvar=.51
    weights=px*(py*py-yvar)
    t=float(s@weights)
    cutoff=sqrt(2*log(2/alpha)*float(weights@weights))
    return abs(t)>=cutoff,t/cutoff
def trial(seed,n,theta,detector_odd=0.):
    rng=np.random.default_rng(seed)
    sign=rng.choice(np.array([-1.,1.]),n)
    z=rng.normal(0,sqrt(.5),n)
    x=rng.normal(0,sqrt(.5),n)
    px=rng.normal(0,sqrt(.5),n)
    noise=rng.normal(0,sqrt(.01),n)
    # Correlated pump-independent electronics: AR(1), rho=.98
    eps=rng.normal(0,sqrt(.02*(1-.98**2)),n)
    drift=np.empty(n);drift[0]=eps[0]
    for i in range(1,n):drift[i]=.98*drift[i-1]+eps[i]
    py=z+rng.normal(0,sqrt(.01),n)
    q=py*py-.51
    out=px+noise+drift+.08*q-2*sign*theta*(x+1/sqrt(39))*(z+1/sqrt(39))**2+detector_odd*sign*q
    return stat(sign,out,py,alpha=.01)
def certificate():
    tau=.05;theta=(39/20)**2*tau
    nnull=400;nalt=160;N0=3000;N1=24000
    null=[trial(i,N0,0.) for i in range(nnull)]
    alt=[trial(10000+i,N1,theta) for i in range(nalt)]
    bad=[trial(30000+i,N1,0.,.08) for i in range(nalt)]
    false=sum(a for a,b in null);power=sum(a for a,b in alt)
    confound=sum(a for a,b in bad)
    assert false<=15,(false,nnull)
    assert power>=int(.65*nalt),(power,nalt)
    assert confound>=int(.5*nalt),(confound,nalt)
    return dict(status='PASS',null_trials=nnull,null_N=N0,
         null_rejections=false,null_empirical_rate=false/nnull,
         alternative_trials=nalt,alternative_N=N1,
         alternative_rejections=power,alternative_empirical_power=power/nalt,
         pump_odd_detector_confound_rejections=confound,
         alpha=.01,seed='null 0..399, alt 10000..10159, confound 30000..30159',
         drift='Independent of sign, AR(1) rho=.98, stationary variance=.02',
         systematic='Pump-even quadratic detector crosstalk 0.08; pump-odd confound 0.08 additionally tested',
         theorem='Under sharp randomization null s independent of every readout, conditional type-I error <= alpha exactly at any N even under arbitrarily temporally correlated readouts.',
         limits='Toy simulated power, no hardware, no general composite null with sign-dependent instruments, no physical gate demonstration. Monte Carlo counts are not certified exact power probabilities.')
if __name__=='__main__':
    out=certificate()
    (ROOT/'data/w33_20261009_finite_shot_homodyne_randomization.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS',out['null_rejections'],out['alternative_rejections'],out['pump_odd_detector_confound_rejections'])
