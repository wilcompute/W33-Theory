#!/usr/bin/env python3
"""Pass5603: symbolic closure of the PSL2(q) fixed-point fusion scheme.

For odd prime powers q>3, let G=PSL(2,q) act on P1(q).  Fuse nonidentity
relative projectivities according to 0,1,2 fixed points.  Pass5599 measured
polynomial intersection numbers.  Here we package the exact first eigenmatrix,
multiplicities, and reconstruct every structure constant from character
orthogonality.  This converts the finite interpolation packet into a symbolic
Bose--Mesner closure certificate.

The representation-theoretic input is the standard projective-line character
table: the permutation character is 1+Steinberg and the remaining principal /
cuspidal families aggregate by fixed-point type.  The executable part below
checks the resulting orthogonality and all structure constants identically in q.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5603_PSL2_FIXEDPOINT_FUSION_SYMBOLIC.json'


def symbolic_packet():
    q=sp.symbols('q', integer=True, positive=True, odd=True)
    v=q*(q*q-1)/2
    k0=q*(q-1)**2/4
    k1=q*q-1
    k2=q*(q+1)*(q-3)/4
    ks=[sp.Integer(1),k0,k1,k2]
    P=sp.Matrix([
      [1,k0,k1,k2],
      [1,0,q-1,-q],
      [1,-(q-1)**2/4,0,(q-3)*(q+1)/4],
      [1,q,-(q+1),0],
    ])
    ms=[
      sp.Integer(1),
      (q-3)*(q+1)**2/4,
      q*q,
      (q-1)**3/4,
    ]
    assert sp.factor(P.det()) == -q**2*(q-1)**2*(q+1)**2/4
    lhs=sp.simplify(P.T*sp.diag(*ms)*P)
    rhs=sp.diag(*[sp.simplify(v*k) for k in ks])
    assert sp.simplify(lhs-rhs)==sp.zeros(4)
    assert sp.factor(sum(ms)-v)==0

    # p_ij^k = 1/(v k_k) sum_h m_h P_hi P_hj P_hk for a symmetric scheme.
    p={}
    for i in range(4):
      for j in range(4):
        for k in range(4):
          p[(i,j,k)]=sp.factor(sum(ms[h]*P[h,i]*P[h,j]*P[h,k] for h in range(4))/(v*ks[k]))

    # Identity laws and symmetry.
    for j in range(4):
      for k in range(4):
        assert sp.simplify(p[(0,j,k)]-(1 if j==k else 0))==0
        assert sp.simplify(p[(j,0,k)]-(1 if j==k else 0))==0
    for i in range(4):
      for j in range(4):
        for k in range(4):
          assert sp.simplify(p[(i,j,k)]-p[(j,i,k)])==0

    mats={}
    for k in range(1,4):
      mats[str(k-1)]=[[str(p[(i,j,k)]) for j in range(1,4)] for i in range(1,4)]

    # q=3 degeneration: the 2-fixed-point relation and one primitive idempotent vanish.
    subs3={str(expr):int(sp.simplify(expr.subs(q,3))) for expr in (v,k0,k1,k2,*ms)}
    assert sp.simplify(k2.subs(q,3))==0
    assert sp.simplify(ms[1].subs(q,3))==0

    return {
      'status':'THEOREM_SYMBOLIC_BOSE_MESNER_CLOSURE',
      'domain':'odd prime powers q>3, with q=3 the degenerate two-class limit',
      'group_order':'q(q^2-1)/2',
      'valencies':['1','q(q-1)^2/4','q^2-1','q(q+1)(q-3)/4'],
      'first_eigenmatrix':[[str(sp.factor(x)) for x in P.row(i)] for i in range(4)],
      'multiplicities':['1','(q-3)(q+1)^2/4','q^2','(q-1)^3/4'],
      'orthogonality':'P^T diag(m) P = |G| diag(k) identically in q',
      'intersection_matrices_nontrivial':mats,
      'q3_structural_collapse':{
        'two_fixed_relation_valency':0,
        'vanishing_primitive_multiplicity':0,
        'remaining_relation_graphs':'3K4 and K4,4,4 from Pass5599/5596',
        'meaning':'q=3 loses both one adjacency relation and one primitive idempotent; this is an algebra degeneration, not only a count coincidence.'
      },
      'proof_boundary':(
        'The standard PSL2/PGL2 projective-line character classification is the representation-theoretic input. '
        'This file certifies the resulting character-aggregated eigenmatrix, multiplicities, orthogonality and every structure constant symbolically.'
      ),
      'primary_reference':'Long-Plaza-Sin-Xiang, Characterization of intersecting families of maximum size in PSL(2,q), arXiv:1608.07304, Section 2 character-table background.'
    }


def main():
    out=symbolic_packet()
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__': main()
