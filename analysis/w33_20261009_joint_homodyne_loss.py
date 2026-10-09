"""Exact-polynomial Gaussian-quadrature signal variance for joint homodyne.

Both output quadratures pass through independent pure-loss channels; Gaussian
electronics are independent. All moments here are degree<=8, 11/12 GH nodes
are independent precision controls, not sampling. Real optical drift remains.
"""
from pathlib import Path
from math import sqrt
import json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def power(tau=.05,eta=1.,noise_p=0.,noise_y=0.,order=11):
    assert 0<eta<=1 and noise_p>=0 and noise_y>=0
    theta=(39/20)**2*tau
    alpha=1/sqrt(39)
    v=.5
    x,w=np.polynomial.hermite_e.hermegauss(order);w/=sqrt(2*np.pi)
    z=sqrt(v)*x[:,None]
    var_Ynoise=(1-eta)*v+noise_y
    yy=sqrt(eta)*z+sqrt(var_Ynoise)*x[None,:]
    weights=w[:,None]*w[None,:]
    yvar=v+noise_y
    H2=yy**2-yvar
    delta_mu=-2*sqrt(eta)*theta*alpha*((z+alpha)**2-(v+alpha**2))
    var_P=v+noise_p+2*eta*theta**2*(z+alpha)**4
    cov=-4*eta*theta*alpha**2*v
    kappa=-4*sqrt(eta)*eta*theta*alpha*v*v
    conditional_IF_mean=delta_mu*H2-kappa-2*cov*yy
    assert abs(np.sum(weights*conditional_IF_mean))<1e-10
    variance=float(np.sum(weights*(var_P*H2**2+conditional_IF_mean**2)))
    n=25*variance/kappa**2
    return dict(tau=tau,eta=eta,noise_p=noise_p,noise_y=noise_y,
        cross_cumulant=kappa,influence_variance=variance,
        alternative_approx_5sigma_N=n,
        order=order,
        matched_gaussian_null_N=25*2*(v+noise_p)*(v+noise_y)**2/kappa**2)
def certificate():
    rows=[]
    for eta in (1.,.8,.5,.2):
        for npower in (0.,.01):
            a=power(eta=eta,noise_p=npower,noise_y=npower,order=11)
            b=power(eta=eta,noise_p=npower,noise_y=npower,order=12)
            assert abs(a['influence_variance']-b['influence_variance'])<1e-9
            rows.append(a)
    ideal=rows[0]
    assert abs(ideal['alternative_approx_5sigma_N']-16982.78534280753)<1e-7
    return dict(status='PASS',signal='kappa(Px_out,Py_out,Py_out)=-eta^(3/2)*theta/sqrt(39)',
        samples=rows,boundary='Only a single two-mode quartic CV current square; idealized pure loss and independent Gaussian electronics, no time-correlated noise, imperfect nonlinear gate or finite-N power.')
if __name__=='__main__':
    result=certificate()
    (ROOT/'data/w33_20261009_joint_homodyne_loss.json').write_text(json.dumps(result,indent=2)+'\n')
    for s in result['samples']:print(s)
