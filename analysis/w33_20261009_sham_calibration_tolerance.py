"""Finite-shot nuisance-robust conditional randomization test for
calibrated gate/route/pump SHAM differences. EXACT worst-case allowed
per-shot systematic |delta_i|<=delta_max even if it follows treatment.

Given Wobs_i = W0_i + delta_i r_i Q_i^2, r_i=S_i G_i R_i,
w0 independent of randomized r, |delta_i|<=bound,
||W0||<=||Wobs||+bound||Q^2||.
Thus threshold bound*sum Q^2+sqrt(2ln(2/alpha))*
(||Wobs||+bound||Q^2||) is finite-N level alpha for sharp null.
"""
import json
from pathlib import Path
from math import sqrt,log
import numpy as np
from scipy.signal import lfilter
ROOT=Path(__file__).resolve().parents[1]
def critical(weights,q2,delta,alpha=.01):
    return (delta*float(q2.sum())+
        sqrt(2*log(2/alpha))*(float(np.linalg.norm(weights))+
                               delta*float(np.linalg.norm(q2))))
def trial(seed,n,delta_actual=0.,delta_bound=.003,signal=False):
    rng=np.random.default_rng(seed)
    sign=rng.choice([-1.,1.],n).astype(float)
    z=rng.normal(0,sqrt(.5),n)
    Q=(z+rng.normal(0,.1,n))**2-.51
    q2=Q*Q
    w0=rng.normal(0,sqrt(.8),n)*Q
    theta=(39/20)**2*.05
    if signal:
       # r correlated nonlinear interaction in full 3-way experiment
       x=rng.normal(0,sqrt(.5),n)
       # Design constant conditional mean with equivalent first-order 3-way
       # contrast; real gate full observable not simulated here.
       w0+=sign*(-theta/sqrt(39)/4)*q2/(2*.51**2)
    obs=w0+delta_actual*sign*q2
    T=float(sign@obs)
    cutoff=critical(obs,q2,delta_bound)
    return (abs(T)>cutoff,4*T/n,4*cutoff/n)
def certificate():
    theta=(39/20)**2*.05
    signal=theta/sqrt(39)
    qvar=2*.51**2
    artifact_slope=4*qvar
    equiv=signal/artifact_slope
    n=150000;alpha=.01
    variance_null=.8*qvar
    critical_gauss=4*sqrt(2*log(2/alpha)*variance_null/n)
    calibration_max=max(0.,(signal-critical_gauss)/artifact_slope)
    assert 0.003<calibration_max<0.006
    r0=[trial(5000+i,35000,delta_actual=+.003,delta_bound=.003) for i in range(80)]
    r1=[trial(7000+i,35000,delta_actual=-.003,delta_bound=.003) for i in range(80)]
    assert sum(x[0] for x in r0)<=7
    assert sum(x[0] for x in r1)<=7
    return dict(status='PASS',alpha=alpha,shots_for_illustrative_threshold=n,
      ideal_quartic_fourfold_signal=-signal,
      alternative_bias_per_unit_mismatch=artifact_slope,
      exactly_signal_equivalent_mismatch=equiv,
      expected_null_weight_variance=variance_null,
      idealized_hoeffding_critical_contrast=critical_gauss,
      idealized_max_mismatch_for_mean_above_threshold=calibration_max,
      worstcase_randomized_sharp_null_theorem='Conditional on all pump- and route-independent underlying W0,Q, assignment r are iid Rademacher. If |delta_i|<=d but otherwise arbitrary, Tobs=sum r_i Wobs_i. Using triangle inequalities, rejecting |Tobs|>d sum Q_i^2+c(||Wobs||2+d||Q^2||2) has P(reject)<=alpha exactly at every N. c=sqrt(2 log(2/alpha)).',
      trial_results=dict(trials_per_arm=80,n=35000,
         plus_boundary_null_rejections=sum(x[0] for x in r0),
         minus_boundary_null_rejections=sum(x[0] for x in r1)),
      caution='Idealized threshold in population moments is not the sample-wise robust threshold. The matched sham experiment may have sign-sensitive optical effects; the theorem requires an independently established bound |delta_i|<=d and the sharp-null independence of W0,Q from route randomization; calibration proof is external.')
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261009_sham_calibration_tolerance.json').write_text(json.dumps(d,indent=2)+'\n')
    print('CALIB',d['exactly_signal_equivalent_mismatch'],d['idealized_max_mismatch_for_mean_above_threshold'],d['trial_results'])
