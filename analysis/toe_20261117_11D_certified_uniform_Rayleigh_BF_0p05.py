"""EXACT uniform AdS5 BF-deficit >1/20 for all fixed-area
flat torus shapes and all |d|<=1 in the physical gauge-constrained
two-derivative sphere-singlet metric-C3 five-scalar pencil.

Take the zero-vector v(d) of Q=M+4K at lambda=12 (from the parallel
exact scalar-operator work). At ANY l in (0,12), its Rayleigh BF
deficit has a simple factored closed form. Let x=sqrt(l), t=d².
  D= ((189+31t)x² +567-207t)
  A= 189*(x-2sqrt3/7)*(x²+3)
  C= 20*(11x³-10sqrt3*x²+42x-12sqrt3).
Then  -(v^T Q v)/(v^T K v) =
  (2sqrt3-x)*[(1-t)*A +t*C]/D.
The flat-T2 Hermite shortest-vector bound l0<=L=2pi sqrt3,
combined with n=floor(sqrt(L/l0)), selects l=n²l0 in [L/4,L].
For x=sqrt(l) in this entire compact interval:
  1.64 < x <3.302; 2sqrt3 -x>.162;
  A> 189*(1.64-2*1.733/7)*5.7 > 1233;
  C>20*(42*1.64-12*1.733) = 961.68;
  D<220*10.9+567 =2965.
Thus deficit >.162*961.68/2965 > .05.
These are conservative rational inequalities using classical bounds
3.14<pi<22/7 and 1.72<sqrt3<1.733.
Because v is an admissible positive-norm 5-vector, Courant-Fischer
guarantees the full five-scalar lowest eigenvalue has at least this
BF deficit. NO interval arithmetic or optimizer premises required.

This is strictly a TWO-DERIVATIVE classical result; higher
derivatives, full 11D modulated branches and other sectors are outside.
"""
import json,math,sys
from fractions import Fraction
from pathlib import Path
import sympy as s
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_11D_unequal_flux_scalar_operator import pencil
from toe_20261117_11D_modular_harmonic_uniform_BF import L,numeric_pencil
OUT=ROOT/"data"/"toe_20261117_11D_uniform_analytic_Rayleigh_gap_over_0p05.json"
def analytic():
    l=s.symbols("l",positive=True)
    x=s.symbols("x",positive=True)
    d=s.symbols("d",real=True)
    K,M=pencil(l,d)
    v=s.Matrix([1,(d-9)/(d+9),4*d/(d+9),
        -s.sqrt(3*(1+d)),s.sqrt(3*(1-d))*(9-d)/(d+9)])
    q=s.factor((v.T*(M+4*K)*v)[0])
    kn=s.factor((v.T*K*v)[0])
    A=189*(x-2*s.sqrt(3)/7)*(x*x+3)
    C=20*(11*x**3-10*s.sqrt(3)*x*x+42*x-12*s.sqrt(3))
    D=(189+31*d*d)*x*x+567-207*d*d
    prediction=(2*s.sqrt(3)-x)*((1-d*d)*A+d*d*C)/D
    # SymPy knows x=sqrt(l)>0. Check numerator and denominator
    # as exact polynomials after substituting l=x².
    substituted=s.factor((-q/kn).subs(l,x*x))
    assert s.simplify(substituted-prediction)==0
    assert s.simplify(s.factor(kn).subs(l,x*x)
        -6*D/((d+9)**2*(x*x+3)))==0
    assert s.simplify((M+4*K).subs(l,12)*v)==s.zeros(5,1)
    # Pure rational lower bound. We use elementary true enclosures:
    # 10.8<L<10.9, 1.64<sqrt(L/4), sqrt(L)<3.302.
    # 1.732<sqrt3<1.733, 3.464<2sqrt3, etc.
    sqrt3=s.sqrt(3)
    assert s.Rational(172,100)<sqrt3<s.Rational(1733,1000)
    assert s.Rational(3464,1000)<2*sqrt3
    assert s.Rational(314,100)<s.pi<s.Rational(22,7)
    assert s.Rational(108,10)<2*s.pi*sqrt3<s.Rational(109,10)
    assert s.Rational(164,100)**2<s.Rational(108,10)/4
    assert s.Rational(109,10)<s.Rational(3302,1000)**2
    amin=189*(s.Rational(164,100)-2*s.Rational(1733,1000)/7)*s.Rational(57,10)
    cmin=20*(42*s.Rational(164,100)-12*s.Rational(1733,1000))
    assert amin>cmin
    uniform=s.factor(s.Rational(162,1000)*cmin/(220*s.Rational(109,10)+567))
    assert uniform>s.Rational(1,20)
    return {"K_normalized_threshold_eigenvector":[str(z) for z in v],
       "exact_Rayleigh_negative_gap_factorization":str(prediction),
       "rational_interval_brackets":{"L":"10.8 < L=2*pi*sqrt3 <10.9",
          "x":"1.64<sqrt(lambda)<3.302",
          "2sqrt3_minus_x":">0.162",
          "A":">"+str(amin),
          "C":">"+str(cmin),
          "D":"<2965"},
       "certified_rational_BF_gap_lower":str(uniform),
       "certified_decimal_BF_gap_lower":float(uniform),
       "claimed_strict_simple_BF_gap_lower":"1/20 = 0.05",
       "proof":"On compact harmonic band x in [sqrt(L/4),sqrt(L)], t=d² in [0,1], A,C positive and bounded below. Numerator is (2sqrt3-x)[(1-t)A+tC], denominator bounded above. Min-max on positive-norm physical K proves lowest eigen below -4.05."}
def numeric():
    gmin=1e99;diffmax=0;num=0
    for d in np.linspace(0,1,19):
      for lam in np.linspace(L/4,L,27):
        K,M=numeric_pencil(lam,d)
        v=np.array([1,(d-9)/(d+9),4*d/(d+9),
          -math.sqrt(3*(1+d)),math.sqrt(3*(1-d))*(9-d)/(d+9)])
        ray=-float(v@(M+4*K)@v/(v@K@v))
        exact=-4-eigh(M,K,eigvals_only=True,subset_by_index=(0,0))[0]
        assert exact>=ray-1e-10
        assert ray>.05
        gmin=min(gmin,ray)
        diffmax=max(diffmax,abs(exact-ray))
        num+=1
    return {"independent_samples":num,"smallest_sample_Rayleigh_gap":gmin,
        "largest_exact_lowest_eigen_gap_minus_Rayleigh":diffmax,
        "scope":"Numerical regression only; analytic rational inequalities are the real mathematical certificate."}
def verify():
    return {"status":"PASS_EXACT_GLOBAL_11D_TWO_DERIVATIVE_BF_DEFICIT_GT_0P05",
       "analytic_certificate":analytic(),
       "numerical_crosschecks":numeric(),
       "physical_scope":"Gauge-constrained physical five scalar sphere-singlet model, positive 5x5 kinetic pencil and fixed-area flat torus, classical two-derivative geometry only. No full 11D corrected action or stable nonlinear branch."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["analytic_certificate"]["certified_decimal_BF_gap_lower"],
          z["numerical_crosschecks"]["smallest_sample_Rayleigh_gap"])
