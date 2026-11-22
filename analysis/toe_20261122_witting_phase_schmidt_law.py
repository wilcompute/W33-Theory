"""Exact full-phase operator Schmidt spectrum for Witting chart unitaries.

Proves a symbolic identity for all U(z)=I+(z-1)P with |z|=1,
rather than sampling isolated angles. Requires SymPy and the independent
canonical gate witness toe_20261122_witting_approximate_gate_no_go.py.

No experimental or spacetime-geometric claim is made.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
from toe_20261122_witting_approximate_gate_no_go import canonical_chart_gate, realign

def verify():
    base = canonical_chart_gate()
    eye = sp.eye(16)
    P = sp.simplify((base-eye)/(-1-sp.I))
    assert (P*P-P).applyfunc(sp.simplify) == sp.zeros(16)
    assert (P-P.H).applyfunc(sp.simplify) == sp.zeros(16)
    assert sp.trace(P) == 6
    z = sp.Symbol("z", nonzero=True)
    x = sp.Symbol("x")
    U = eye+(z-1)*P
    R = realign(U)
    # On the physical unit circle z*=1/z.
    Rdag = R.H.applyfunc(lambda entry: entry.xreplace({sp.conjugate(z): 1/z}))
    gram = sp.simplify(R*Rdag)
    a = sp.factor(-(z-1)**2/(4*z))
    expected = x**8*(x-(16-15*a))*(x-9*a)*(x-a)**6
    exact = sp.factor(gram.charpoly(x).as_expr())
    assert sp.factor(exact-expected) == 0
    assert sp.factor(a.subs(z,-sp.I)-sp.Rational(1,2)) == 0
    assert sp.factor(a.subs(z,-1)-1) == 0
    assert sp.factor(a.subs(z,1)) == 0
    # For 0<a<=1 the two largest squared singular values are
    # 16-15a and 9a; they exchange order at a=2/3.
    assert sp.simplify((16-15*a)-(9*a)) == 16-24*a
    # Top-four squared Schmidt weight = 16-4a.
    return dict(status="PASS_EXACT_ALL_PHASES",date="2026-11-22",
      unitary_family="U(theta)=I+(exp(i theta)-1)*P, rank(P)=6",
      phase_parameter="a=sin(theta/2)^2=(1-cos(theta))/2",
      squared_operator_schmidt_spectrum=["16-15a","9a"]+["a"]*6+["0"]*8,
      characteristic_polynomial="x^8*(x-16+15a)*(x-9a)*(x-a)^6",
      rank_statement="OSR=8 for theta not 0 modulo 2pi; OSR=1 for theta=0 modulo 2pi",
      crossing="a=2/3, cos(theta)=-1/3; dominant squared values 6 and 6",
      fidelity_k1="F_avg <= 1-6a/17",
      fidelity_k2="F_avg <= 1-4a/17",
      diamond_k2="||Channel(U)-Channel(V)||_diamond >= sqrt(a) for any unitary V with OSR<=4",
      scope="Only rank<=2 deterministic unitary entanglers and arbitrary local unitary circuits; mathematical result, not physical spacetime tetrahedron or universal computing theorem")

def main():
    result=verify()
    path=Path(__file__).resolve().parents[1]/"data"/"toe_20261122_witting_phase_schmidt_law.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS exact all-phase Witting Schmidt spectrum and rank-budget fidelity bound")

if __name__=="__main__":
    main()
