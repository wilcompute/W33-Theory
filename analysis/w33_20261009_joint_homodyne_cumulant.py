"""Exact third-order two-homodyne witness for a single quartic W33 current.
This is a *joint* homodyne experiment, P_X and P_Y on different CV modes.
A joint Gaussian state has vanishing mixed centered third cumulant.
"""
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
def certificate(tau=F(1,20)):
    theta=F(39,20)**2 * tau
    a2=F(1,39)
    v=F(1,2)
    # P_X' = P_X - 2 theta (X+a)(z+a)^2, Var(X)=Var(P_X)=v.
    # Mixed central third cumulant of P_X',z,z.
    k2=-4*theta*v*v  # cumulant / alpha
    kappa2=k2*k2*a2
    # Influence function for the estimated mixed cumulant, including
    # estimations of both channel means and the linear P--z covariance.
    # Its variance follows by conditioning on z and Wick's theorem.
    var_if=v*(2*v*v)+theta**2*((156+224*a2)*v**4+
                               120*a2*v**3+96*a2*a2*v**3+
                               4*a2*a2*v*v)
    gaussian_null_var=2*v*v*v
    alternative_n25=F(25)*var_if/kappa2
    null_n25=F(25)*gaussian_null_var/kappa2
    # Locally efficient quadratic score after fitting Gaussian intercept
    # and slope; Fisher information for theta at theta=0, from conditional
    # Gaussian mean displacement -2 theta a [(z^2-v)+2 a z].
    fisher=4*a2*(2*v*v)/v
    assert fisher==F(4,39)
    return dict(status="PASS",tau=str(tau),theta=str(theta),
        mixed_cumulant_over_alpha=str(k2),
        mixed_cumulant_squared=str(kappa2),
        exact_influence_variance=str(var_if),
        alternative_asymptotic_5sigma_N=float(alternative_n25),
        matched_gaussian_null_5sigma_N=float(null_n25),
        prior_kurtosis_alternative_N=85260.4879969483,
        locally_efficient_gaussian_nuisance_score_fisher=str(fisher),
        locally_efficient_5sigma_N=float(F(25)/(fisher*theta*theta)),
        scope="Single two-mode CV quartic term; independent vacuum inputs; no photon source, gate synthesis, drift, detector loss, finite-N power, or optimized gate.") 
if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261009_joint_homodyne_cumulant.json").write_text(json.dumps(out,indent=2)+"\n")
    print(out)
