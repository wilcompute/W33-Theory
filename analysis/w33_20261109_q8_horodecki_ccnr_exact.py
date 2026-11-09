#!/usr/bin/env python3
"""Exact CCNR realignment detection for the Horodecki two-qutrit PPT family.

Rudolph (2003), Chen and Wu (2003) already proved realignment/CCNR
separability tests and detected Horodecki bound entanglement. The project
integration is that our 10 W33/Q8 settings recover rho sufficiently to
evaluate CCNR, fixing the previous correlator-only blind spot.
"""
import json
import sys
import numpy as np
import sympy as sp
from pathlib import Path
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_ten_context_tomography import select

def realign(r):
    return r.reshape(3,3,3,3).transpose(0,2,1,3).reshape(9,9)

def exact_proof():
    a,b=sp.symbols("a b",real=True)
    z=sp.Symbol("z")
    d=8*a+1
    rho=sp.zeros(9)
    for i in (0,1,2,3,4,5,7):rho[i,i]=a
    rho[6,6]=rho[8,8]=(1+a)/2
    for i,j in ((0,4),(0,8),(4,8)):rho[i,j]=rho[j,i]=a
    rho[6,8]=rho[8,6]=b/2
    R=sp.Matrix(9,9,lambda i,j:rho[3*(i//3)+(j//3),
                                     3*(i%3)+(j%3)])
    characteristic=sp.factor((R*R.T).charpoly(z).as_expr())
    actual=sp.factor(characteristic.subs(b**2,1-a*a))
    e1=8*a*a+a+1
    e2=sp.Rational(1,2)*(11*a**4-2*a**3+9*a*a)
    e3=a**4*(1-a)**2
    expected=z*(z-a*a)**5*(z**3-e1*z*z+e2*z-e3)
    assert sp.factor(actual-expected)==0
    # Squared residual for sum S of the 3 remaining singular values.
    # If r_i=sqrt(root_i)>0, S=r1+r2+r3, then
    # F(S)=(S^2-e1)^2/4-e2-2*sqrt(e3)*S=0.
    S=sp.symbols("S",real=True)
    F=(S*S-e1)**2/4-e2-2*a*a*(1-a)*S
    S0=3*a+1
    F0=sp.factor(F.subs(S,S0))
    assert sp.factor(F0-a*a*(a-1)*(3*a+1)/4)==0
    deriv0=sp.factor(sp.diff(F,S).subs(S,S0))
    assert sp.factor(deriv0-a*(5*a*a+14*a+5))==0
    # For 0<a<1, F(sqrt(e1))<0, F''(S)=3S^2-e1>0 for
    # S>=sqrt(e1); one positive zero above sqrt(e1).
    # Since S0>sqrt(e1), F(S0)<0 => unique zero S>S0.
    # Thus 5a+S >8a+1 => realignment nuclear norm >1.
    return {
      "exact_scaled_Gram_characteristic":str(sp.factor(expected)),
      "three_remaining_squared_singular_elementary_symmetric":{
          "e1":str(e1),"e2":str(sp.factor(e2)),"e3":str(sp.factor(e3))},
      "root_sum_test_S0":"3*a+1",
      "F_at_S0":str(F0),
      "Fprime_at_S0":str(deriv0),
      "realignment_trace_norm_strict_gt_1_for_every_0_lt_a_lt_1":True,
      "proof":"Five nonzero isolated singular values a/(8a+1), one zero, three roots of displayed cubic. For S=sum sqrt(roots), F(S)=0 and F is strictly convex for S>=sqrt(e1). At S0=3a+1, F(S0)=a^2(a-1)(3a+1)/4<0, so S>S0. Therefore (5a+S)/(8a+1)>1.",
      "historical_prior_art":"Chen and Wu, Quantum Information and Computation 3:193-202 (2003), Example 2 explicitly detects this Horodecki family with realignment, doi:10.26421/QIC3.3-1."
    }

def main(path=None):
    exact=exact_proof()
    audit, (B,U,V,ops,inv)=select(return_components=True)
    scan=[]
    maxerr=0
    for a in (.001,.01,.05,.1,.2,.236,.3,.4,.5,.6,.7,.8,.9,.99,.999):
        rho=horodecki_state(a)
        spectra=np.linalg.eigvalsh(rho)
        gamma=rho.reshape(3,3,3,3).transpose(0,3,2,1).reshape(9,9)
        assert min(spectra)>-2e-12 and min(np.linalg.eigvalsh(gamma))>-2e-12
        p=np.concatenate([np.einsum("ij,ik,kj->j",e.conj(),rho,e).real
                          for e in (B,U,V)])
        coefficients=inv@(p-1/9)
        reconstructed=np.eye(9)/9+np.einsum("k,kij->ij",coefficients,ops)
        maxerr=max(maxerr,float(np.max(abs(reconstructed-rho))))
        detected=float(np.linalg.svd(realign(reconstructed),compute_uv=False).sum())
        ideal=float(np.linalg.svd(realign(rho),compute_uv=False).sum())
        assert detected>1+1e-6 and abs(detected-ideal)<4e-12
        scan.append({"a":a,"CCNR_from_10_measured_bases":detected,
                     "excess_above_separable_one":detected-1,
                     "PPT_minimum_eigenvalue":float(min(np.linalg.eigvalsh(gamma)))})
    assert maxerr<5e-12
    result={
      "status":"PASS_EXACT_CCNR_HORODECKI_ALL_0_A_1_FROM_TEN_W33_Q8_BASES",
      "analytic_certificate":exact,
      "sampled_Horodecki_family":scan,
      "reconstruction_max_abs_error":maxerr,
      "optimal_10_basis_rank":audit["ten_setting_design_rank"],
      "optimal_10_basis_condition_number":audit["combined_condition_number"],
      "physical_scope":"Ideal calibrated full tomography. CCNR can detect all ideal Horodecki a in (0,1), but the excess approaches zero near endpoints, so finite precision/noise can defeat certification.",
      "no_global_novelty_claim":True}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS Horodecki exact CCNR W33 10",json.dumps({
       "number_of_a_samples":len(scan),
       "minimum_sampled_excess":min(x["excess_above_separable_one"] for x in scan),
       "a0p236_excess":next(x["excess_above_separable_one"] for x in scan if x["a"]==.236),
       "max_reconstruction_error":maxerr}))
    return result

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
