"""Exact one-loop SU5 shape-selection test from softly split messenger pairs.

This is an EFFECTIVE SU5 threshold calculation after E6 has already
broken to SU5. It is NOT a renormalizable invariant of a single E6
adjoint, nor a completed supersymmetric E6 vacuum.

W = (M+y Phi) F+ Fbar+ + (M-y Phi) F- Fbar-
with one equal scalar soft mass-squared Delta in EACH vectorlike pair.
The two opposite Yukawa signs cancel all odd Phi powers.
For one 5+5bar pair: one-loop supertrace / (16*pi^2)
of f(m_s^2)-f(m_f^2), f(s)=s^2(log(s/Q^2)-3/2).
An EXACT SUSY pair at Delta=0 cancels. The quartic coefficient of
the mirror TWO-pair threshold is y^4/(8*pi^2)*F(Delta/M^2),
F(t)=log(1+t)-4t(2t+1)/(3(1+t)^2).

For t=-1/10 (all scalar m^2=0.9 M^2 positive), F>0 and
the quartic favors 3+2. t=+1/10 gives F<0 and instead
favors 4+1 near the origin. The effect needs nonzero SUSY breaking.
"""
from __future__ import annotations
from pathlib import Path
import json, math
import mpmath as mp
import scipy.optimize as so
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_SU5_mirror_messenger_Coleman_Weinberg_threshold.json"

def F(t):
    assert t>-1
    return math.log1p(t)-4*t*(2*t+1)/(3*(1+t)**2)

def exact_identity():
    z,D,scale=sp.symbols("z D scale",positive=True)
    f=lambda s:s*s*(sp.log(s/scale**2)-sp.Rational(3,2))
    g=f(z*z+D)-f(z*z)
    quartic=sp.factor(sp.diff(g,z,4)/sp.factorial(4))
    expected=sp.log(1+D/z**2)-4*D*(2*D+z*z)/(3*(D+z*z)**2)
    assert sp.simplify(quartic-expected)==0
    assert sp.simplify(expected.subs(D,0))==0
    # Two mirror messengers (m + y phi) and (m - y phi)
    # add even coefficients, and cancel odd coefficients exactly.
    a,x,y=sp.symbols("a x y",real=True)
    assert sp.expand((a+y*x)**3+(a-y*x)**3).coeff(x,3)==0
    assert sp.expand((a+y*x)**5+(a-y*x)**5).coeff(x,5)==0
    series=sp.series(sp.log(1+sp.Symbol("t"))-
        4*sp.Symbol("t")*(2*sp.Symbol("t")+1)/(3*(1+sp.Symbol("t"))**2),
        sp.Symbol("t"),0,4)
    assert sp.expand(series.removeO()).coeff(sp.Symbol("t"),1)==-sp.Rational(1,3)
    return {"quartic_mirror_coefficient":"kappa_eff=y^4/(8*pi^2) F(Delta/M^2)",
       "F(t)":"log(1+t)-4*t*(2*t+1)/(3*(1+t)^2)",
       "first_small_soft_term":"F(t)=-t/3+O(t^2)",
       "scalar_stability":"Require M^2+Delta>0 for all 5 messenger scalar components at Phi=0; also require |y phi_i| small enough to keep all mass squares positive.",
       "holomorphic_messenger_symmetry":"Opposite Yukawa signs (+y,-y) and equal soft splittings are ASSUMED; no UV symmetry enforcing their equality established.",
       "exact_one_loop_prefactor":"1/(16*pi^2) per vectorlike 5+5bar chiral pair (two complex scalars and one Dirac fermion)."}

def calc_potential(phi,delta,scale=1):
    """Two 5+5bar mirror pairs at M=y=1, with high precision."""
    mp.mp.dps=55
    D=mp.mpf(str(delta)); M=mp.mpf(1);Y=mp.mpf(1)
    Q=mp.mpf(str(scale))
    def h(z):
        s=z*z
        assert s+D>0
        return (s+D)**2*(mp.log((s+D)/(Q*Q))-mp.mpf("1.5")) - s*s*(mp.log(s/(Q*Q))-mp.mpf("1.5"))
    return sum(h(M+Y*xi)+h(M-Y*xi) for xi in phi)/(16*mp.pi**2)

def numerical():
    root=so.brentq(F,-.3,-.2,xtol=1e-14)
    assert -.27<root<-.26
    data=[]
    for t in (-.5,-.3,-.25,-.1,0,.1,.5,1):
        data.append({"soft_mass2_over_M2":t,
                     "F":F(t),
                     "quartic_sign":"positive_3plus2" if F(t)>1e-12 else
                                    ("negative_4plus1" if F(t)<-1e-12 else "zero_SUSY")})
    assert F(-.1)>0 and F(.1)<0 and F(0)==0
    diffs=[]
    for rstr in (".01",".02",".05",".1",".2"):
        r=mp.mpf(rstr)
        # normalized 3+2 and 4+1 eigenvalues at common norm r:
        a=[2*r/mp.sqrt(30)]*3+[-3*r/mp.sqrt(30)]*2
        b=[r/mp.sqrt(20)]*4+[-4*r/mp.sqrt(20)]
        gap=calc_potential(b,-.1)-calc_potential(a,-.1)
        leading=mp.mpf(str(F(-.1)))/(8*mp.pi**2)*(mp.mpf(13)/20-mp.mpf(7)/30)*r**4
        assert gap>0
        assert abs(gap/leading-1)<.001
        diffs.append({"Phi_norm":rstr,
                      "V_SU4_minus_V_SM":str(gap),
                      "leading_order_prediction":str(leading),
                      "relative_discrepancy":float(gap/leading-1)})
    # The quartic is a LOCAL effective expansion: no claim about
    # global minimum at arbitrary high VEV where heavy modes become light.
    return {"critical_negative_soft_t":root,
       "sample_soft_sign_scan":data,
       "benchmark_Delta_over_M2":-.1,
       "benchmark_F":F(-.1),
       "benchmark_kappa_eff_at_y1":F(-.1)/(8*math.pi**2),
       "fixed_norm_3plus2_vs_4plus1":diffs,
       "gauge_threshold":"The messenger-induced quartic is a legitimate SU5 effective invariant only after E6 is already broken. If all heavy fields form mass-degenerate complete E6 multiplets, the E6 single-adjoint quartic obstruction persists.",
       "renormalization_warning":"Quadratic radial terms, gauge-loop potentials, counterterms, and higher powers of Phi need matching; the quartic coefficient alone is not a global vacuum proof.",
       "SUSY_warning":"Delta=0 gives exact boson-fermion cancellation; negative scalar Delta is allowed only if physical scalar mass^2 remains positive. This entails high-scale soft SUSY breaking and may conflict with naturalness."}

def verify():
    a=exact_identity();b=numerical()
    return {"status":"PASS_SOFT_SUSY_MIRROR_MESSENGER_INDUCED_3PLUS2_QUARTIC",
            "analytic_one_loop":a,"numerical_controls":b,
            "scope":"Original controlled one-loop effective-field-theory example, NOT an E6 UV completion, a prediction of measured scales, or a complete Coleman-Weinberg vacuum analysis."}
if __name__=="__main__":
    v=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(v["status"],v["numerical_controls"]["critical_negative_soft_t"],
          v["numerical_controls"]["benchmark_kappa_eff_at_y1"])
