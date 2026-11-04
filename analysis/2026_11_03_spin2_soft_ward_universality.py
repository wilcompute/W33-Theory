#!/usr/bin/env python3
"""Weinberg soft spin-2 mass-shell gauge Ward identity, exact toy 2->2.

Two species with non-universal soft-graviton couplings violate the
mass-shell polarization gauge identity for nontrivial scattering; a shared
universal coupling obeys it. Necessary condition, not a produced graviton.
"""
from pathlib import Path
import math,json
import numpy as np,sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_spin2_soft_ward_universality.json'
p1=sp.Matrix([1,0,0,1]);p2=sp.Matrix([1,0,0,-1])
p3=sp.Matrix([1,1,0,0]);p4=sp.Matrix([1,-1,0,0])
legs=[p1,p2,p3,p4]
eta=[-1,-1,1,1]
Metric=sp.diag(1,-1,-1,-1)
def dot(p,q):return (p.T*Metric*q)[0]
def run():
    assert sum((eta[i]*legs[i] for i in range(4)),sp.zeros(4,1))==sp.zeros(4,1)
    assert all(dot(p,p)==0 for p in legs)
    # A is the first incoming-to-outgoing species, B the other.
    PA=eta[0]*p1+eta[2]*p3
    PB=eta[1]*p2+eta[3]*p4
    J=sp.Matrix.hstack(PA,PB)
    assert J.rank()==1
    assert J.nullspace()==[sp.Matrix([1,1])]
    xi=sp.Matrix([sp.Rational(1,3),sp.Rational(2,5),sp.Rational(-1,7),sp.Rational(3,11)])
    # A soft null momentum q avoids collinear leg denominators.
    q=sp.Matrix([5,3,4,0])
    assert dot(q,q)==0
    assert all(dot(p,q)!=0 for p in legs)
    # Gauge shift on polarisation: eps_mu_nu -> eps_mu_nu
    # +q_mu xi_nu +xi_mu q_nu. Soft numerator transforms as
    # 2(p dot q)(p dot xi), leaving 2 sum eta kappa p dot xi.
    dx=sp.Matrix([[0]*4 for _ in range(4)])
    # Covariantized tensor components in Euclidean index notation:
    qc=Metric*q;xic=Metric*xi
    dx=qc*xic.T+xic*qc.T
    # p^T dx p / (p.q) = 2 (p.xi).
    factor=[sp.factor((p.T*dx*p)[0]/dot(p,q)) for p in legs]
    assert all(sp.simplify(factor[i]-2*dot(legs[i],xi))==0 for i in range(4))
    kA,kB=sp.symbols('kA kB',real=True)
    amplitude=sp.simplify(kA*(eta[0]*factor[0]+eta[2]*factor[2])
                          +kB*(eta[1]*factor[1]+eta[3]*factor[3]))
    expected=sp.factor(2*(kA-kB)*dot(PA,xi))
    assert sp.simplify(amplitude-expected)==0
    assert amplitude!=0
    assert sp.simplify(amplitude.subs({kA:1,kB:1}))==0
    numeric=[]
    for a,b in ((1.,1.),(1.,.9),(1.,1.01),(.7,1.)):
        result=float(amplitude.subs({kA:a,kB:b}))
        assert (abs(result)<1e-14)==(a==b)
        numeric.append({"species_A_coupling":a,"species_B_coupling":b,
            "soft_polarization_gauge_variation":result})
    out={"status":"PASS_SOFT_SPIN2_TWO_SPECIES_GAUGE_UNIVERSALITY",
      "input_kinematics":"Supplied flat Lorentzian 2->2 massless momenta p1=(1,0,0,1), p2=(1,0,0,-1), p3=(1,1,0,0), p4=(1,-1,0,0); incoming legs negative, outgoing positive; two distinct species A and B.",
      "universality_matrix":"J=[p3-p1, p4-p2], rank1; nullspace exactly span{(1,1)}. Two species' soft couplings must coincide to satisfy the gauge condition for this nonforward process.",
      "exact_polarization_gauge_shift":"delta S = 2 sum_i eta_i kappa_i (p_i dot xi) = 2(kA-kB)(p3-p1) dot xi",
      "polarization_q":[int(z) for z in q],
      "test_xi":[str(z) for z in xi],
      "symbolic_deltaS":str(amplitude),
      "nonuniversal_numeric_controls":numeric,
      "interpretation":"This is an exact check of a known necessary consistency condition from Weinberg soft-spin-2 theorem; it excludes universal soft-graviton gauge invariance for this specified scattering with species-dependent couplings.",
      "scope":"Does not generate a spin-2 field, supply a graviton propagator, prove the full theorem for arbitrary scattering, produce Einstein dynamics or measure a gravitational coupling.",
      "literature":["https://doi.org/10.1103/PhysRev.135.B1049","https://doi.org/10.1103/PhysRevD.96.084048"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("SOFT WARD",str(amplitude),"rank",J.rank(),"nullspace",J.nullspace(),flush=True)
if __name__=="__main__":run()
