"""A 100% EXACT RATIONAL certificate: global singleton CANNOT be optimal
at the two-tick local-stability threshold for T=1.

This builds 18x18 rational representations of 9x9 Q(omega) projectors,
uses rational Taylor lower bound on Tr(exp Q), rational upper bound
on e and exp(kappa*C) to certify E(Q)<E(single).
No floating optimizer/eigen solver needed for the inequality!
"""
from __future__ import annotations
import math,json,itertools
from pathlib import Path
import sympy as S
from w33_20261019_tick_operator_frame_majorization import points,symp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round12_exact_rational_heptad_counterexample.json"
M=S.Matrix([[0,-1],[1,-1]])  # multiplication by omega, omega^2+omega+1=0
I2=S.eye(2);I18=S.eye(18)
O=S.kronecker_product(S.eye(9),M)
def W18(p):
    a,b,c,d=p
    W=S.zeros(18)
    for i,j in itertools.product(range(3),repeat=2):
        row=3*((i+a)%3)+(j+b)%3;col=3*i+j
        v=M**((c*i+d*j)%3)
        for r in range(2):
            for s in range(2):W[2*row+r,2*col+s]=v[r,s]
    assert W**3==I18
    return W
def P18(p,k):
    W=W18(p)
    return (I18+(O**((-k)%3))*W+(O**((-2*k)%3))*(W**2))/3
def run():
    pt=points()
    ids=[0,23,27,28,34,36,39]
    ks=[2,2,2,1,2,0,1]
    weights=[S.Rational(1473,10000)]*6+[S.Rational(1162,10000)]
    assert sum(weights)==1
    assert all(symp(pt[i],pt[j])!=0 for i,j in itertools.combinations(ids,2))
    Q=sum((w*P18(pt[i],k) for i,k,w in zip(ids,ks,weights)),S.zeros(18))
    assert S.trace(Q)==6
    # Ordinary field trace of Q^n equals twice the real matrix trace
    # in the original nine-dimensional Hermitian physical Hilbert space.
    qpow=I18
    terms=[]
    Zlower=S.Integer(0)
    m=12
    for n in range(m+1):
        term=(S.trace(qpow)/2)/math.factorial(n)
        assert term.is_Rational and term>=0
        terms.append(term)
        Zlower+=term
        qpow=qpow*Q
    # All eigenvalues of physical Q lie in [0,1]; all omitted terms
    # in Tr exp Q = sum trace(Q^n)/n! are NONNEGATIVE.
    eL=sum((S.Rational(1,math.factorial(n)) for n in range(13)),S.Rational(0))
    eU=eL+S.Rational(14,13*math.factorial(13))
    # exp(1) lies strictly between these rational bounds.
    # kappa_loc(T=1) = -(e-1)/(2(e+2)).
    # Since this function strictly DECREASES in e,
    # kappa_true < kappa_upper computed at e_L.
    kup=-(eL-1)/(2*(eL+2))
    C=S.Rational(4,3)*sum((x*y for x,y in itertools.combinations(weights,2)),S.Rational(0))
    assert C>0
    x=kup*C
    assert -S.Rational(1,2)<x<0
    # For negative x, 4th Taylor polynomial of e^x is UPPER
    # by Lagrange's signed fifth remainder.
    expUpper=sum((x**n/math.factorial(n) for n in range(5)),S.Rational(0))
    RHS=(3*eU+6)*expUpper
    rationalMargin=Zlower-RHS
    assert rationalMargin>0, "No rigorous counterexample found"
    # This proves Z(Q) > (3e+6)*exp(kappa_true C), equivalently
    # F(Q)+kappa_true C < F(single), without numerical approximations.
    checks={"all_seven_direction_pairs_noncommuting":True,
      "exact_Q_field_trace_6":S.trace(Q)==6,
      "all_13_Taylor_terms_rational_nonnegative":all(t.is_Rational and t>=0 for t in terms),
      "rational_e_bounds_valid":eU>eL and eU-eL<S.Rational(1,100000000),
      "strict_certified_gap_in_partition_inequality":rationalMargin>0,
      "simplex_weights_rational_positive":sum(weights)==1 and all(w>0 for w in weights)}
    out={"schema":"w33.round12.rigorous_rational_T1_heptad_global_boundary_counterexample.v1",
     "theorem":"At T=1, kappa_two_tick_local=-(e-1)/(2(e+2)), the proposed full-120-rate singleton global stability is FALSE. Explicit rational seven-tick mixture supported on seven pairwise noncommuting Pauli directions, with rational masses six times 1473/10000 plus 1162/10000, has F_1(Q)+kappa*C < F_1(single). Proof uses exact rational 18x18 Q(omega) matrix representation, finite Taylor lower bound for Z(Q)=Tr exp Q, rational bounds eL<e<eU, and degree-4 alternating-Taylor upper bound on exp(kappa_upper*C); all comparisons are exact rational inequalities. Thus the global transition may be FIRST ORDER at T=1, preceding local singleton instability.",
     "prior_art":"Earlier numerical Round3/Round7 recorded equal-weight heptad versus singleton crossing around kappa=-0.181113 at T=1, already above local threshold ≈-0.182088. The phenomenon was known numerically; NEW contribution is an exact rational proof for one explicit seven-point state, and explicit correction to any all-T conjecture of equality.",
     "T":1,"outcome_indices_120":[3*i+k for i,k in zip(ids,ks)],
     "point_indices":ids,"outcome_labels":ks,
     "weights":[str(w) for w in weights],
     "C_exact":str(C),
     "kappa_upper_exact":str(kup),
     "e_bounds":{"lower":str(eL),"upper":str(eU)},
     "taylor_order":m,"trace_exp_Q_lower_exact":str(Zlower),
     "strict_partition_gap_lower_exact":str(rationalMargin),
     "strict_partition_gap_lower_float":float(rationalMargin),
     "numerical_energy_gap_estimate":float(-S.log(Zlower/(3*eU+6))+kup*C),
     "interpretation":"At kappa_local the SINGLE TICK is locally stable along EVERY two-tick direction, but this seven-tick configuration is lower energy. It proves a nontrivial metastability/first-order pre-emption possibility for this finite-dimensional engineered functional; not a thermodynamic singular phase transition or physical fundamental coupling prediction.",
     "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"margin":float(rationalMargin),"gap_energy_upper_bound":out["numerical_energy_gap_estimate"]},indent=2))
    return out
if __name__=="__main__":run()
