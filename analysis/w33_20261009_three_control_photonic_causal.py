"""Three-way randomized photonic control: pump S, gate G, bypass R.

Under a sharp route null, independently randomized route bits R yield an
exact conditional Hoeffding finite-N type-I bound despite arbitrary
correlated W=SG Px(Py²-vy). A GS electronics artifact is canceled in
expectation by R; a GSR electronic artifact remains a false positive.
"""
from pathlib import Path
from math import sqrt,log
import numpy as np,json
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def trial(seed,n=90000,mode='null',alpha=.01):
    rg=np.random.default_rng(seed)
    S=rg.choice(np.array([-1.,1.]),n);G=rg.choice(np.array([-1.,1.]),n)
    R=rg.choice(np.array([-1.,1.]),n)
    z=rg.normal(0,sqrt(.5),n);x=rg.normal(0,sqrt(.5),n)
    py=z+rg.normal(0,.1,n);Q=py*py-.51
    drift=lfilter([1],[1,-.98],rg.normal(0,sqrt(.02*(1-.98**2)),n))
    p=rg.normal(0,sqrt(.5),n)+drift+.1*S*G*Q+.08*S*Q+.04*G*Q
    if mode=='signal':
        theta=(39/20)**2*.05
        p+= -2*.25*(G+1)*(R+1)*S*theta*(x+1/sqrt(39))*(z+1/sqrt(39))**2
    if mode=='route_dependent_detector':
        p+=.11*S*G*R*Q
    weight=S*G*p*Q
    numerator=float(R@weight)
    critical=sqrt(2*log(2/alpha)*float(weight@weight))
    return dict(reject=abs(numerator)>=critical,z_score=numerator/critical,
                estimand_fourfold=4*numerator/n)
def certificate():
    reps=72;n=90000
    modes=('null','signal','route_dependent_detector')
    all_results={mode:[trial(11000*i+7*j,n,mode) for j in range(reps)]
                 for i,mode in enumerate(modes)}
    rejection={mode:sum(x['reject'] for x in vals) for mode,vals in all_results.items()}
    mean_est={mode:float(np.mean([x['estimand_fourfold'] for x in vals])) for mode,vals in all_results.items()}
    assert rejection['null']<=8,rejection
    assert rejection['signal']>=40,rejection
    assert rejection['route_dependent_detector']>=50,rejection
    theta=(39/20)**2*.05;analytic=-theta/sqrt(39)
    assert abs(mean_est['signal']-analytic)<.01,mean_est
    return dict(status='PASS',shots_per_trial=n,trials_per_arm=reps,alpha=.01,
        rejection_counts=rejection,mean_4x_GSR_score=mean_est,
        predicted_4x_GSR_signal=analytic,
        theorem='Under sharp route-null that R cannot change any measured output, for fixed S,G,weights, the independent Rademacher randomized R yields exact finite-N two-sided type-I probability <= alpha.',
        scope='Simulated single-edge ideal quartic CV gate and artificial detector responses. Genuine gate-and-route-dependent detector coupling can still fake a signal. Physical bypass must be calibrated; no actual device or photon source demonstrated.')
if __name__=='__main__':
    result=certificate()
    (ROOT/'data/w33_20261009_three_control_photonic_causal.json').write_text(json.dumps(result,indent=2)+'\n')
    print('THREE-WAY',result['rejection_counts'],result['mean_4x_GSR_score'])
