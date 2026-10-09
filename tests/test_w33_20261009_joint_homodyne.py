"""Independent Gaussian-quadrature check of the exact mixed cumulant variance."""
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_joint_homodyne_cumulant as m

def test_exact_mixed_cumulant_and_eighth_moment_influence():
    a=1/np.sqrt(39)
    v=.5
    theta=(39/20)**2*.05
    z,w=np.polynomial.hermite_e.hermegauss(13)
    z*=np.sqrt(v)
    w/=np.sqrt(2*np.pi)
    mu=-2*theta*a*(z+a)**2
    mean=float(np.sum(w*mu))
    c1=float(np.sum(w*(mu-mean)*z))
    h2=z*z-v
    kappa=float(np.sum(w*(mu-mean)*h2))
    assert abs(kappa+theta*a)<2e-14
    given_var=v+4*theta*theta*v*(z+a)**4
    if_mean=(mu-mean)*h2-kappa-2*c1*z
    var_if=float(w@(given_var*h2*h2+if_mean*if_mean))
    from fractions import Fraction as F
    exact=m.certificate(F(1,20))
    assert abs(var_if-float(F(exact['exact_influence_variance'])))<2e-11
    assert 16000<exact['alternative_asymptotic_5sigma_N']<18000

def test_local_efficiency():
    from fractions import Fraction as F
    assert m.certificate()['locally_efficient_gaussian_nuisance_score_fisher']=='4/39'
    # For theta->0 the joint H2 score has null asymptotic variance 1/4
    # and covariance slope -1/sqrt(39): Fisher information 4/39.
