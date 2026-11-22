"""Exact operator-entanglement extrema for phase-tunable Witting chart gates.

Separates three *different* special phases:
  - dominant operator-Schmidt singular-value crossing at a=2/3,
  - max linear operator entropy at a=10/13,
  - max von Neumann operator entropy at a=16/(15+3**(6/5)).
No statement about state entangling power or quantum gravity is made.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import sympy as sp

def verify():
    a=sp.symbols("a", real=True)
    p0=(16-15*a)/16
    p1=9*a/16
    p2=a/16
    assert sp.expand(p0+p1+6*p2)==1
    purity=sp.factor(p0**2+p1**2+6*p2**2)
    assert sp.simplify(purity-(39*a*a-60*a+32)/32)==0
    linear_stationary=sp.solve(sp.diff(purity,a),a)
    assert linear_stationary==[sp.Rational(10,13)]
    linear_min=sp.factor(purity.subs(a,sp.Rational(10,13)))
    assert linear_min==sp.Rational(29,104)
    # Shannon derivative vanishes when p0^15=p1^9*p2^6.
    # The unique positive solution is (16-15a)=3^(6/5)*a.
    shannon_optimum=sp.Integer(16)/(15+3**sp.Rational(6,5))
    assert sp.simplify(16-15*shannon_optimum-3**sp.Rational(6,5)*shannon_optimum)==0
    assert 0<float(shannon_optimum)<1
    # Strict concavity of Shannon entropy on 0<a<1:
    # H'' = -[(p0')²/p0 + (p1')²/p1 +6(p2')²/p2]/ln2 < 0.
    second_derivative=sp.factor(-(
        sp.Rational(225,256)/p0+
        sp.Rational(81,256)/p1+
        6*sp.Rational(1,256)/p2)/sp.log(2))
    assert float(second_derivative.subs(a,sp.Rational(1,2)))<0
    def entropy(x):
        weights=[(16-15*x)/16,9*x/16]+[x/16]*6
        return -sum(p*math.log2(p) for p in weights if p>0)
    shan=float(shannon_optimum)
    vals={str(k):entropy(v) for k,v in [
        ("crossing",2/3),("linear",10/13),("Shannon",shan),("pi",1)]}
    assert vals["Shannon"]>max(vals["linear"],vals["crossing"],vals["pi"])
    return dict(status="PASS_EXACT_ANALYTIC",date="2026-11-22",
        operator_entanglement_probabilities=["(16-15a)/16","9a/16"]+["a/16"]*6,
        purity_formula=str(purity),
        linear_entropy_maximum_a="10/13",
        linear_entropy_maximum="75/104",
        spectral_crossing_a="2/3",
        Shannon_entropy_maximum_a="16/(15+3^(6/5))",
        Shannon_entropy_optimal_theta_rad=2*math.asin(math.sqrt(shan)),
        Shannon_entropy_maximum_bits=vals["Shannon"],
        entropy_comparison_bits=vals,
        uniqueness="Shannon entropy strictly concave and linear entropy strictly concave as a function of a on 0<a<=1",
        caveat="Operator entanglement is Choi-vector Schmidt entropy, not generally the entangling power on product states; three critical phases differ.")

def main():
    output=Path(__file__).resolve().parents[1]/"data"/"toe_20261122_witting_operator_entropy_stationary_phase.json"
    result=verify()
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS exact operator-entropy stationary phases; Shannon a*=16/(15+3^(6/5))")

if __name__=="__main__":
    main()
