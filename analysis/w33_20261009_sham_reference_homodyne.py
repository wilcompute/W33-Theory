"""Matched sham/reference detector for independent S/G/R photonic
randomization. Uses blocked optical reference with common electronic
interaction (including S*G*R). Perfect common-mode artifact subtraction
restores conditional sharp route-null; small mismatch remains a confound.
This is an instrument model, not a manufactured CV gate.
"""
from pathlib import Path
import json
from math import sqrt,log
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def trial(seed,n=150000,mode='null',alpha=.01,mismatch=0):
    rg=np.random.default_rng(seed)
    S=rg.choice(np.array([-1.,1.]),n);G=rg.choice(np.array([-1.,1.]),n)
    R=rg.choice(np.array([-1.,1.]),n)
    z=rg.normal(0,sqrt(.5),n);x=rg.normal(0,sqrt(.5),n)
    py=z+rg.normal(0,.1,n);Q=py**2-.51
    drift=lfilter([1],[1,-.98],rg.normal(0,sqrt(.02*(1-.98**2)),n))
    electronic=.11*S*G*R*Q+.09*S*G*Q+.08*S*Q+.04*G*Q+drift
    ref=rg.normal(0,sqrt(.3),n)+electronic
    sample=rg.normal(0,sqrt(.5),n)+electronic+mismatch*S*G*R*Q
    if mode=='signal':
        theta=(39/20)**2*.05
        sample+=-.5*(G+1)*(R+1)*S*theta*(x+1/sqrt(39))*(z+1/sqrt(39))**2
    W=(sample-ref)*Q
    test=float((S*G*R)@W)
    cutoff=sqrt(2*log(2/alpha)*float(W@W))
    return int(abs(test)>=cutoff),4*test/n
def certificate():
    modes=[('uncorrelated_reference_null','null',0),
           ('genuine_gate','signal',0),
           ('mismatched_reference_null','null',.03)]
    trials=72;n=150000
    results={}
    for i,(label,mode,delta) in enumerate(modes):
        cases=[trial(seed=700000+i*1000+j,n=n,mode=mode,mismatch=delta) for j in range(trials)]
        results[label]=dict(rejections=sum(x[0] for x in cases),
             mean_4x_contrast=float(np.mean([x[1] for x in cases])),
             mismatch=delta)
        print(label,results[label],flush=True)
    assert results['uncorrelated_reference_null']['rejections']<=8
    assert results['genuine_gate']['rejections']>=45
    assert results['mismatched_reference_null']['rejections']>=45
    return dict(status='PASS',trials_each=trials,shots_per_trial=n,alpha=.01,arms=results,
      observable='4/N*sum_i S_i G_i R_i (Px_signal_i - Px_sham_i)*(Py_i^2-.51)',
      exactly_cancels_common_mode='any common additive electronic artifact at the Px readout, including terms proportional to S, SG, SGR and arbitrary time-correlated drift, provided synchronous reference response is identical',
      sharp_null_bound='After exact common-mode cancellation, for outcome differences invariant under randomized R, the conditional finite-N Hoeffding rejection probability is ≤alpha.',
      nonidentifiability='Residual mismatch δ*S*G*R*(Py²-.51) produces an indistinguishable third-order signal. Real devices require independent calibration constraints/bounds on δ; finite-N sharp null cannot cover δ≠0.',
      scope='Synthetic homodyne data, not an implementation or verified source/detector model.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_sham_reference_homodyne.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS')
