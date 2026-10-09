"""Exact rational two-mode optical cumulant for ONE W33 current square.

This is not a simulation of all 160 currents or of a finite qutrit register.
"""
from fractions import Fraction as F
from math import comb, factorial
import json
from pathlib import Path

def gaussian_even(n, alpha_squared):
    return sum(F(comb(2*n,2*k)*factorial(2*k), 2**k*factorial(k))
               *F(1,2)**k*alpha_squared**(n-k) for k in range(n+1))

def certificate(alpha_squared=F(1,39)):
    m1,m2,m3,m4=[gaussian_even(k,alpha_squared) for k in range(1,5)]
    variance_Z2=m2-m1*m1
    kappa_Z2=m4-4*m3*m1+6*m2*m1*m1-3*m1**4-3*variance_Z2**2
    covariance=m4-2*m1*m3+m1*m1*m2-variance_Z2*m2
    coeff=16*alpha_squared**2*kappa_Z2+48*alpha_squared*covariance+12*(m4-m2*m2)
    variance_coefficient=2*m2+4*alpha_squared*variance_Z2
    assert coeff==F(618440,6591)
    assert variance_coefficient==F(5207,3042)
    return dict(status="PASS",alpha_squared=str(alpha_squared),
                exact_kappa4_coefficient=str(coeff),
                exact_variance_coefficient=str(variance_coefficient),
                theta_from_edge_time="theta=(39/20)^2*tau",
                scope="Single current-square CV two-mode vacuum; no full 160-current gate or detector model.")

if __name__=="__main__":
    result=certificate()
    path=Path(__file__).resolve().parents[1]/"data/w33_20261008_single_edge_photonic_kurtosis.json"
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(result)
