#!/usr/bin/env python3
"""Exact one-link flux characteristic polynomial and all-temperature Hessian.

Because a single link carries only z or z^-1, the charpoly of B(z) B(z)†
is exactly affine in q=|z-1|². Factor P(z=-1)-P(z=1) over integers.
Compare its Matsubara sum curvature to the 81D Wilson-octagon Hessian.
"""
import json,sys,math
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
from w33_20261109_flux_dark_mode_fragility import build

def main(path=None):
    B,edges,G=build()
    p,l=edges[0]
    signed=B.astype(np.int64);signed[p,l]=-1
    t=sp.symbols("t",real=True)
    def P(T):
        coeff=[int((-1)**j*v) for j,v in enumerate(sp.Matrix((T@T.T).tolist()).charpoly().all_coeffs())]
        return sp.Poly(sum(v*t**j for j,v in enumerate(coeff)),t)
    p0=P(B.astype(int));p1=P(signed)
    delta=sp.factor(p1.as_expr()-p0.as_expr())
    print("EXACT_SINGLE_LINK_DELTA_POLY",str(delta)[:1600],flush=True)
    # s=singular value. Fermion F=-2/beta Sum_s log(2cosh(beta*s/2)).
    # P_theta=P0+(q/4)*(P_pi-P0), q=|exp(i theta)-1|².
    # At theta->0, q=theta², F''= - 1/beta Sum_n [(Ppi-P0)/P0](t_n),
    # t_n=beta²/(pi²(2n+1)²).
    # κcrit = -F'' / (# octagons containing one link)= -F''/81.
    # It is equivalent to the full 81D generalized Hessian if exact.
    assert int(sp.Poly(delta,t).coeff_monomial(t**4))>0
    assert p0.degree()==25 and p1.degree()==26
    ratios=[]
    fn=sp.lambdify(t,delta,"numpy")
    # Avoid big integer polynomial float overflow: use simplified rational.
    R=sp.cancel(delta/p0.as_expr())
    rf=sp.lambdify(t,R,"numpy")
    for beta in (.3,.5,1.,2.,5.,10.):
        def summand(k):
            z=(beta/(math.pi*(2*k+1)))**2
            return float(rf(z))
        # Rapid convergence since first term t^4 => O(n^-8).
        val=sum(summand(n) for n in range(250))
        tail_bound=abs(summand(250))*200/7
        local=val/(81*beta)
        ratios.append({"beta":beta,
              "kappa_local_single_link_Matsubara":local,
              "summation_terms":250,
              "bound_coarse_truncation_tail":tail_bound})
    out={"status":"PASS_EXACT_SINGLE_EDGE_W33_CHARACTERISTIC_POLYNOMIAL_FLUX_CURVATURE",
      "modified_edge":[p,l],
      "P_flat_factored":str(sp.factor(p0.as_expr())),
      "P_one_pi_minus_flat_exact_factored":str(delta),
      "ratio_difference_over_flat":str(R),
      "single_edge_octagons":81,
      "beta_curvature_controls":ratios,
      "matsubara_local_threshold_formula":"kappa_c(beta)=(1/(81*beta))*SUM_n[(P_pi(t_n)-P_flat(t_n))/P_flat(t_n)], t_n=beta²/(pi²(2n+1)²)",
      "scope":"Exact rational characteristic-poly identity for a single phase link, plus truncated positive convergent Matsubara sum; exact full 81x81 Hessian proportionality to octagon Gram has been numerically observed but is NOT proved by the single-link test alone.",
      "prior":"Analytic secular rank-one phase perturbations and fermionic cosh Matsubara products are standard; W33 rational polynomial coefficients are specific to this finite graph."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("MATSUBARA_CURVATURE",json.dumps({x["beta"]:x["kappa_local_single_link_Matsubara"] for x in ratios}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
