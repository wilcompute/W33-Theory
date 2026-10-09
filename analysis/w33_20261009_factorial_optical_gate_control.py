"""2x2 random factorial gate-enable x pump-sign CV homodyne protocol.

G=+/-1 random gate ON/OFF; S=+/-1 randomized pump sign.
W=Px*(Py^2-v). Contrast mean E[G*S*W] suppresses pump-sign
and gate-enable main effects, but not detector S*G interactions.
Under the sharp gate-null, G independent of all fixed outputs,
Hoeffding gives exact conditional finite-N alpha control.
"""
from pathlib import Path
from math import sqrt,log
import numpy as np,json
ROOT=Path(__file__).resolve().parents[1]
def run(seed,n,tau=.05,mode='null',alpha=.01):
    rng=np.random.default_rng(seed)
    s=rng.choice([-1.,1.],n);g=rng.choice([-1.,1.],n)
    z=rng.normal(0,sqrt(.5),n)
    x=rng.normal(0,sqrt(.5),n)
    px=rng.normal(0,sqrt(.5),n)
    py=z+rng.normal(0,.1,n)
    H=py*py-.51
    # temporal AR1 correlated independent of all randomized treatment
    eps=rng.normal(0,sqrt(.015*(1-.98**2)),n)
    drift=np.empty(n);drift[0]=eps[0]
    for i in range(1,n):drift[i]=.98*drift[i-1]+eps[i]
    # pump-sign-odd readout artifact -- cancels in factorial contrast
    readout=px+drift+.1*s*H+.05*H
    if mode in ('signal','interaction_artifact'):
        if mode=='signal':
            theta=(39/20)**2*tau
            readout+=-2*((g+1)/2)*s*theta*(x+1/sqrt(39))*(z+1/sqrt(39))**2
        else:readout+=.1*s*((g+1)/2)*H
    weight=s*readout*H
    T=float(g@weight);den=sqrt(2*log(2/alpha)*float(weight@weight))
    return bool(abs(T)>den),T/den,float(T/n)
def certificate():
    n=50000;ntrials=96
    none=[run(k,n,mode='null') for k in range(ntrials)]
    signal=[run(5000+k,n,mode='signal') for k in range(ntrials)]
    mimics=[run(10000+k,n,mode='interaction_artifact') for k in range(ntrials)]
    counts=[sum(v[0] for v in a) for a in (none,signal,mimics)]
    assert counts[0]<=6 and counts[1]>=60 and counts[2]>=50,counts
    return dict(status='PASS',n=n,trials_each=ntrials,
       no_gate_interaction_rejections=counts[0],
       true_quartic_signal_rejections=counts[1],
       gate_times_sign_detector_artifact_rejections=counts[2],
       contrast='mean(G*S*Px*(Py^2-.51)); S and G independent Rademacher signs',
       exact_null='If changing gate enable G leaves every shot output unaffected conditional on S, outcomes, then P(|T|>=sqrt(2 log(2/alpha)*sum(S W)^2))<=alpha for any finite N.',
       qualification='Main-effect pump sign artifacts disappear in expectation; gate*sign detector interactions remain indistinguishable. A gate-control bypass/reference channel is required for stronger causal attribution.',
       simulator='seeded AR1 drift rho=.98 and pump-sign detector cross-talk 0.1; 1% threshold',
       boundary='Monte Carlo evidence not a physical device demonstration; no finite-sample power guarantee under composite nuisance gate effects.')
if __name__=='__main__':
    d=certificate();(ROOT/'data/w33_20261009_factorial_optical_gate_control.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d)
