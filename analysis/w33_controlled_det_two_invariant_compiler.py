#!/usr/bin/env python3
"""Two-invariant compiler for the controlled determinant gate.

For X in sp4(F3), eigenvalues occur in +/- pairs and the characteristic
polynomial is even. Newton identities for a traceless 4x4 matrix with tr X^3=0
give
    det X = ((tr X^2)^2 - 2 tr X^4)/8.
Over F3, 8=2 and 1/2=2, hence
    det X = 2 * ((tr X^2)^2 + tr X^4)  mod 3.

The identity is exhaustively verified on all 3^10 controller states in the
repo's fixed coordinate basis.

Therefore, in a richer invariant-phase library with primitives
    P_q2sq : |X,r> -> omega^(r (tr X^2)^2) |X,r>
    P_q4   : |X,r> -> omega^(r tr X^4) |X,r>,
the exact controlled determinant gate is
    U_det = P_q2sq^2 P_q4^2.
This is two commuting nonlinear invariant-phase primitives, versus the proven
17-primitive optimum in the native reduced-monomial library.

The result is a compiler theorem, not a hardware claim: the current photonic
stack has not yet demonstrated direct q2^2 or tr(X^4) phase interactions.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_controlled_det_two_invariant_compiler.json'

def mat(x):
    return [[2*x[4]%3,2*x[8]%3,x[0],x[1]],
            [2*x[5]%3,2*x[9]%3,x[1],x[2]],
            [x[3],x[6],x[4],x[5]],
            [x[6],x[7],x[8],x[9]]]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(4))%3 for j in range(4)] for i in range(4)]
def tr(A):return sum(A[i][i] for i in range(4))%3
def det4(A):
    A=[row[:] for row in A];d=1
    for c in range(4):
        p=next((i for i in range(c,4) if A[i][c]%3),None)
        if p is None:return 0
        if p!=c:A[c],A[p]=A[p],A[c];d=(-d)%3
        pv=A[c][c]%3;d=d*pv%3;iv=pow(pv,-1,3)
        for i in range(c+1,4):
            if A[i][c]%3:
                f=A[i][c]*iv%3
                A[i]=[(A[i][j]-f*A[c][j])%3 for j in range(4)]
    return d%3
def main(write=True):
    census={}
    for x in itertools.product(range(3),repeat=10):
        X=mat(x);X2=mm(X,X);X4=mm(X2,X2)
        p2=tr(X2);p4=tr(X4)
        rhs=2*((p2*p2+p4)%3)%3
        lhs=det4(X)
        assert lhs==rhs
        census[(p2,p4,lhs)]=census.get((p2,p4,lhs),0)+1
    parent=json.loads((ROOT/'data/w33_controlled_det_17term_optimality.json').read_text())
    assert parent['status']=='PASS_LIBRARY_OPTIMUM'
    out={'schema':'w33.controlled_det_two_invariant_compiler.v1','status':'PASS_TWO_PRIMITIVE_RICH_LIBRARY',
      'identity':'det(X)=2*((tr X^2)^2 + tr X^4) mod 3 for X in sp4(F3)',
      'derivation':'Newton identity e4=((p2)^2-2p4)/8 plus the even characteristic polynomial of sp4 elements; reduce coefficients mod3',
      'exhaustive_controller_states':3**10,
      'all_states_verified':True,
      'compiler':{
        'primitive_1':'P_q2sq: exponent (tr X^2)^2',
        'primitive_2':'P_q4: exponent tr X^4',
        'formula':'U_det = P_q2sq^2 * P_q4^2',
        'commuting':True,
        'primitive_count':2},
      'comparison':{'native_reduced_monomial_optimum':17,'rich_invariant_library':2,'compression_factor':'17/2=8.5 in primitive count'},
      'physical_boundary':'No present Holonet certificate implements direct q2^2 or tr(X^4) phase Hamiltonians. This result specifies the two nonlinear observables a richer device would need.',
      'checks':{'parent_17_optimum_loaded':True,'newton_identity_exhaustive':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
