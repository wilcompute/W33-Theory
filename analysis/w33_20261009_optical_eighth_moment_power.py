"""Exact eighth-moment analytic error bar for a quartic single-edge homodyne gate.

Pure Gaussian input with Var(X)Var(P_X)=1/4, independent Gaussian P_Y.
Pure loss, independent Gaussian electronics. This is an idealized gate
and assumes stable calibrated parameters: not a laboratory shot guarantee.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def dfact_odd(n):
    p=1
    for i in range(n,0,-2):p*=i
    return p
def raw_normal(k,variance):
    return sum(F(comb(k,2*j))*dfact_odd(2*j-1)*variance**j for j in range(k//2+1))
def raw_moments(theta,eta,sX2,sP2,sY2,noise):
    assert eta in [F(1),F(1,4),F(1,25),F(0)]
    root_eta={F(1):F(1),F(1,4):F(1,2),F(1,25):F(1,5),F(0):F(0)}[eta]
    assert sX2*sP2>=F(1,4)
    # Scale measured P_X by alpha^{-1}=sqrt(39) so all moments rational.
    A=-2*root_eta*theta/F(39)
    B0=F(39)*(eta*sP2+(1-eta)/2+noise)
    B1=F(4)*eta*theta*theta*sX2/F(39)
    vZ=F(39)*sY2
    moments=[]
    for k in range(9):
        val=F(0)
        for j in range(k//2+1):
            inside=sum(F(comb(j,h))*B0**(j-h)*B1**h *
                       raw_normal(2*(k-2*j)+4*h,vZ) for h in range(j+1))
            val+=F(comb(k,2*j))*dfact_odd(2*j-1)*A**(k-2*j)*inside
        moments.append(val)
    return moments
def power(theta,eta,sX2,sP2,sY2,noise):
    raw=raw_moments(theta,eta,sX2,sP2,sY2,noise)
    mu=raw[1]
    m=[sum(F(comb(n,k))*(-mu)**(n-k)*raw[k] for k in range(n+1)) for n in range(9)]
    m2,m3,m4=m[2:5]
    kap=m4-3*m2*m2
    gamma=kap/m2**2
    # Efficient influence function for the plug-in sample excess kurtosis.
    coefficients=[m4/m2**2,-4*m3/m2**2,-6/m2-2*kap/m2**3,F(0),F(1)/m2**2]
    assert sum(coefficients[i]*m[i] for i in range(5))==0
    vIF=sum(coefficients[i]*coefficients[j]*m[i+j] for i in range(5) for j in range(5))
    assert vIF>0
    return dict(excess_kurtosis=float(gamma),null_if_variance=24.,
        alternative_if_variance=float(vIF),
        optimistic_gaussian_null_N5=float(F(25)*F(24)/gamma**2) if gamma else None,
        alternative_asymptotic_N5=float(F(25)*vIF/gamma**2) if gamma else None,
        var_measured=float(m2/F(39)),
        kappa4_measured=float(kap/F(39)**2),
        relative_error_variance_ratio=float(vIF/F(24)),
        scope='Alternative asymptotic delta method, not validated 5-sigma power under time-correlated drift.')
def certificate():
    z=power(F(0),F(1),F(1,2),F(1,2),F(1,2),F(0))
    assert z['excess_kurtosis']==0 and z['alternative_if_variance']==24.
    t=F(1,20)*F(39,20)**2
    ideal=power(t,F(1),F(1,2),F(1,2),F(1,2),F(0))
    assert abs(ideal['var_measured']-(.5+float(F(5207,3042)*t*t)))<1e-12
    assert abs(ideal['kappa4_measured']-float(F(618440,6591)*t**4))<1e-12
    cases={'vacuum_ideal':ideal}
    for eta in [F(1),F(1,4),F(1,25)]:
        cases['squeezed_eta_'+str(eta)]=power(t,eta,F(1,4),F(1),F(1,2),F(1,100))
    return dict(status='PASS',input='Independent P_X and X minimum-uncertainty Gaussians; Z=P_Y+1/sqrt39.',
        method='Exact rational eighth moments and plug-in excess-kurtosis influence-function asymptotics.',
        cases=cases, warning='No photonic hardware gate, no Monte Carlo false-positive rate, no finite-N confidence interval.')
if __name__=='__main__':
    out=certificate()
    (ROOT/'data/w33_20261009_optical_eighth_moment_power.json').write_text(json.dumps(out,indent=2)+'\n')
    for k,v in out['cases'].items():print(k,v)
