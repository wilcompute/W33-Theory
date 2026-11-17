"""Curvature invariant firewall for M-theory eight-derivative corrections.

On AdS5(L) x S2(L/sqrt(k1)) x S2(L/sqrt(k2)) x T2,
k1=4(1+eta), k2=4(2-eta), the constant-curvature
Riemann invariants are exact. Pontryagin curvature 4-form traces
vanish pointwise on EACH constant-sectional-curvature block,
hence X8(background)=0, but scalar Riem^4 contractions are nonzero.
This does NOT calculate t8t8R4 nor the G4 supersymmetric completion.
"""
import json,math
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_11D_R4_curvature_nonzero_vs_X8.json"

def invariants(eta):
    e=S.sympify(eta)
    k1=4*(1+e);k2=4*(2-e)
    R=S.expand(-5*4+2*k1+2*k2)
    Ric2=S.expand(5*4**2+2*k1**2+2*k2**2)
    Riem2=S.expand(2*5*4+4*k1**2+4*k2**2)
    return {"eta":str(eta),"k1":str(k1),"k2":str(k2),
            "R_L2":str(R),"Ricci_squared_L4":str(Ric2),
            "Riemann_squared_L4":str(Riem2),
            "Riemann_squared_squared_L8":str(S.expand(Riem2**2)),
            "pointwise_pontryagin_trR2":"0",
            "pointwise_pontryagin_trR4":"0",
            "pointwise_X8":"0"}

def derivation():
    x=S.symbols("x",real=True)
    e=S.Rational(1,2)+x
    k1=4*(1+e);k2=4*(2-e)
    R=-20+2*(k1+k2)
    Ric2=S.expand(80+2*k1**2+2*k2**2)
    Riem2=S.expand(40+4*k1**2+4*k2**2)
    assert S.simplify(R-4)==0
    assert S.simplify(Ric2-(224+64*x*x))==0
    assert S.simplify(Riem2-(328+128*x*x))==0
    # On each constant-K factor R^a_b=K e^a wedge e_b, every
    # term in tr R^(2j) has a repeated one-form and vanishes.
    # A zero Pontryagin density does not make scalar R4 zero.
    return {"shape_offset":"x=eta-1/2",
      "scalar_R_L2":"4",
      "Ricci_squared_L4":"224+64*x^2",
      "Riemann_squared_L4":"328+128*x^2",
      "example_nonzero_quartic_scalar_at_equal":"(Rabcd Rabcd)^2 L^8=107584",
      "pointwise_tr_R_wedge_R":"0",
      "pointwise_tr_R_wedge_R_wedge_R_wedge_R":"0",
      "pointwise_X8":"0",
      "not_computed":"Actual t8t8R4, epsilon11epsilon11R4 and complete supersymmetric flux-dependent eight-derivative operator; X8 variations can affect fluctuation equations even when X8 of background is zero."}

def verify():
    law=derivation()
    rows=[invariants(v) for v in (S.Rational(1,4),S.Rational(1,2),S.Rational(3,4))]
    assert rows[1]["Riemann_squared_squared_L8"]=="107584"
    assert rows[0]["R_L2"]==rows[1]["R_L2"]==rows[2]["R_L2"]=="4"
    assert rows[0]["Riemann_squared_L4"]==rows[2]["Riemann_squared_L4"]
    assert rows[0]["Riemann_squared_L4"]!="328"
    return {"status":"PASS_NONZERO_SCALAR_R4_INVARIANT_DESPITE_X8_ZERO",
      "exact_invariants":law,"samples":rows,
      "no_physical_eight_derivative_coefficient_computed":True}
if __name__=="__main__":
    o=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(o["status"],o["exact_invariants"]["Riemann_squared_L4"])
