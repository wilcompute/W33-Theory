"""Pump-sign-randomized homodyne lock-in for the W33 single-edge CV gate.

Observable R=s P_X^out ((P_Y^out)^2-vY), where s=+/- pump sign
assigned uniformly independently of each shot. Pump-even additive
readout offsets and background mixed cumulants cancel IN EXPECTATION.
Variance is integrated by two independent GH orders, with optional
Gaussian common drifts in the P readout.
"""
import json
from pathlib import Path
from math import sqrt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def lockin(tau=.05,eta=.8,noise_p=.01,noise_y=.01,drift_p=.0,n=11):
    theta=(39/20)**2*tau;a=1/sqrt(39);v=.5
    nodes,w=np.polynomial.hermite_e.hermegauss(n)
    nodes*=sqrt(v);w/=sqrt(2*np.pi)
    z=nodes[:,None];noise=np.sqrt(2*((1-eta)*v+noise_y))*nodes[None,:]
    # nodes have variance v=1/2, so sqrt(2*v_noise) gives desired variance
    Y=sqrt(eta)*z+noise
    vy=v+noise_y
    Q=Y*Y-vy
    mean=-2*sqrt(eta)*theta*a*(z+a)**2
    varP=v+noise_p+drift_p+2*eta*theta**2*(z+a)**4
    prob=w[:,None]*w[None,:]
    E_R=float(np.sum(prob*mean*Q))
    analytic=-(eta**1.5)*theta*a
    assert abs(E_R-analytic)<1e-12
    variance=float(np.sum(prob*(varP+mean*mean)*Q*Q))-E_R**2
    assert variance>0
    n5=25*variance/E_R**2
    return dict(eta=eta,noise_p=noise_p,noise_y=noise_y,drift_p=drift_p,
         mean=E_R,variance=variance,approx_5sigma_samples=n5)
def certificate():
    rows=[]
    for eta in (1.,.8,.5,.2):
        for drift in (0.,.05):
            a=lockin(eta=eta,drift_p=drift,n=11)
            b=lockin(eta=eta,drift_p=drift,n=12)
            assert abs(a['variance']-b['variance'])<1e-11
            rows.append(a)
    return dict(status='PASS',pump_sign='independently randomized +/- on each shot',
      observable='s * P_X_out * (P_Y_out^2 - E[P_Y_out^2])',
      mean='-eta^(3/2)*theta/sqrt39 under independent symmetric Gaussian inputs',
      rows=rows,
      boundary='Pump-even drift canceled in mean only if independently randomized, uncorrelated with sign. A phase-locked pump-odd detector bias still can fake it; finite-N power, hardware and nonlinear gate not certified.')
if __name__=='__main__':
    x=certificate()
    (ROOT/'data/w33_20261009_pump_sign_lockin.json').write_text(json.dumps(x,indent=2)+'\n')
    for r in x['rows']:print(r)
