"""TOE94 exact cyclotomic-field certificate of TOE93 central obstruction.

Recognize each U4 transvection generator in Q(sqrt(3),i)=Q(zeta_12),
with rational coefficients bounded by denominator 12; use SymPy exact
field arithmetic to prove commuting projective permutations have
anticommuting unitary lifts. No floating tolerance in final identity.
"""
from __future__ import annotations
import json
import numpy as np
import sympy as S
from fractions import Fraction
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_central_extension import V
from analysis.w33_20261015_toe91_symplectic_phase_audit import transvection
from analysis.w33_20261015_toe91_symplectic_unitary_lift import lift
from analysis.w33_20261015_toe92_full_symplectic_4mode import comp
SQ=S.sqrt(3)
COEFF=[S.Rational(k,d) for d in (1,2,3,4,6,12) for k in range(-12,13)]
COEFF=list(dict.fromkeys(COEFF))
CANDIDATES=sorted(set((float(a+b*SQ),a+b*SQ) for a in COEFF for b in COEFF
                       if abs(float(a+b*SQ))<=1.01),key=lambda q:q[0])
def recognized(x):
    possibles=[(abs(v-x),z) for v,z in CANDIDATES if abs(v-x)<1e-9]
    if not possibles:raise AssertionError(('unrecognized',x))
    return min(possibles,key=lambda y:(y[0],len(str(y[1]))))[1]
def gens():
    exact=[];errs=[]
    for v in V:
        u,_,_=lift(tuple(transvection(v)))
        z=S.Matrix(4,4,lambda i,j:recognized(u[i,j].real)+S.I*recognized(u[i,j].imag))
        errs.append(max(abs(complex(z[i,j].evalf())-u[i,j]) for i in range(4) for j in range(4)))
        assert errs[-1]<1e-9
        assert matzero(z.conjugate().T*z-S.eye(4))
        exact.append(z)
    return exact,errs
def matzero(M):
    return all(S.expand(z)==0 for z in M)
def word_product(ws,us):
    P=S.eye(4)
    for i in ws:
        P=(us[i]*P).applyfunc(S.expand)
    return P
def perm_product(ws,gs):
    P=tuple(range(40))
    for i in ws:P=comp(gs[i],P)
    return P
def certificate():
    from analysis.w33_20261015_toe93_central_extension import certificate as previous
    w=previous()['gauge_invariant_nontrivial_multiplier_witness']
    A=w['projective_order_two_permutation_A_word']
    B=w['projective_order_two_permutation_B_word']
    unit,errs=gens()
    X=word_product(A,unit);Y=word_product(B,unit)
    P=[tuple(transvection(v)) for v in V]
    assert perm_product(A,P)!=perm_product(B,P)
    assert comp(perm_product(A,P),perm_product(B,P))==comp(perm_product(B,P),perm_product(A,P))
    assert matzero(X*Y+Y*X)
    assert matzero(X.conjugate().T*X-S.eye(4))
    assert matzero(Y.conjugate().T*Y-S.eye(4))
    assert matzero(X*Y*X.conjugate().T*Y.conjugate().T+S.eye(4))
    print('EXACT-CENTRAL',len(A),len(B),'U_A U_B=-U_B U_A over Q(zeta12)',flush=True)
    return {'number_of_generators':len(V),
      'coefficient_field':'Q(sqrt(3),i)=Q(zeta_12)',
      'max_rational_reconstruction_residual':round(float(max(errs)),12),
      'word_A':A,'word_B':B,
      'permutation_commutator':'identity',
      'exact_matrix_product_XY_plus_YX':'zero 4x4 over Q(zeta12)',
      'exact_lifted_commutator':'-I4',
      'linearization_impossible_on_projective_25920_group':True,
      'central_cover_caveat':'Exact projective multiplier obstruction on two commuting elements. This certifies nontrivial central extension, but not the full presentation/group order of the generated unitary extension or uniqueness of Sp(4,3) as a lift.'}
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261015_toe94_exact_central.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
