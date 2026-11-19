#!/usr/bin/env python3
"""BPS interpolation between H27 toy sextic SIC and MUB F-vacua.

For the real channel x in [0,1] with other two coordinates held at 1,
W=x^3-x^6/2 + constants. This is an isolated global-SUSY toy,
not a gauge-invariant/E8 domain wall or a cosmological prediction.
"""
import json
from pathlib import Path
import sympy as s
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261119_H27_SIC_MUB_BPS_wall_certificate.json"

def run():
    x=s.symbols("x",real=True)
    W=x**3-s.Rational(1,2)*x**6
    F=s.diff(W,x)
    assert F==3*x**2-3*x**5
    dw=s.simplify(W.subs(x,1)-W.subs(x,0))
    tension=s.simplify(2*s.integrate(F,(x,0,1)))
    assert dw==s.Rational(1,2) and tension==1
    assert s.limit(F/x**2,x,0,dir="+")==3
    assert s.diff(F,x).subs(x,1)==-9
    # Every stationary support sector has F=0, so V=sum_i|F_i|^2=0.
    # Distinct W values do not select a sector in unbroken global SUSY.
    energies=[0,0,0,0]
    Wlevels=[s.Rational(k,2) for k in range(4)]
    assert Wlevels[2]==1 and Wlevels[3]==s.Rational(3,2)
    # BPS wall slope x'=F(x), monotone for 0<x<1.
    # By integrating dx/dz near x=0, x(z)~ -1/(3 z) at z->-infty.
    # Near x=1, 1-x falls exponentially as e^(-9 z).
    # Cutoff integrals converge to exact wall tension 1.
    controls=[]
    for eps in [1e-2,1e-3,1e-4]:
        numeric=2*quad(lambda t: 3*t*t*(1-t**3),eps,1-eps,epsabs=1e-13)[0]
        analytic=float(2*(W.subs(x,1-eps)-W.subs(x,eps)))
        assert abs(numeric-analytic)<1e-12
        controls.append({"cutoff":eps,"integrated_tension":numeric,"missing_tail":1-numeric})
    result={"source":"H27 sextic W=sum_i(x_i^3-x_i^6/2), canonical global SUSY",
      "support_two_SIC_W":str(Wlevels[2]),
      "support_three_MUB_W":str(Wlevels[3]),
      "F_term_vacuum_energies_all_supports":energies,
      "delta_W":str(dw),"BPS_tension_dimensionless":str(tension),
      "interpolating_real_channel":"x_prime=3*x^2*(1-x^3); other two coordinates fixed at 1",
      "SIC_side_algebraic_tail":"x(z) asymptotic -1/(3z) as z->-infinity",
      "MUB_side_exponential_tail":"1-x(z) proportional to exp(-9z) as z->infinity",
      "cutoff_numerical_checks":controls,
      "limits":"BPS solution in ungauged canonical-Kähler global-SUSY toy; no E8 fields, gauge D-term, gravity backreaction, vacuum preference, or spacetime derivation"}
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
