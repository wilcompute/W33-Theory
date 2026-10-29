#!/usr/bin/env python3
"""Klein-quadric bridge for the native two-commutator Maxwell completion.

Exact F2 reduction of all 15 Pfaffian-certified characteristic-zero
five-channel choices, with a complete 15 nonzero-momentum F2 census.
This identifies the 28 nondecomposable bivectors as the symplectic-form
GL4(2)/Sp4(2) coset, without inferring a physical particle.
"""
from __future__ import annotations
from itertools import combinations, product
from math import gcd
from pathlib import Path
import json
import sys

import sympy as sp

R=sp.Matrix([[1,0,5,-5,1,0],[0,1,-1,0,1,0],[0,0,5,-5,0,1]])
PAIRS=list(combinations(range(4),2))
BASE=sp.eye(6)


def pf(q):
    return int(q[0])*int(q[5])-int(q[1])*int(q[4])+int(q[2])*int(q[3])


def rank2(rows):
    piv={}
    for row in rows:
        z=sum((int(t)&1)<<i for i,t in enumerate(row))
        while z:
            j=z.bit_length()-1
            if j in piv:z^=piv[j]
            else:piv[j]=z;break
    return len(piv)


def c_of_d(d):
    return [[(d[a] if k==b else d[b] if k==a else 0) &1
             for k in range(4)] for a,b in PAIRS]


def pair_result(i,j):
    A=R.col_join(BASE.extract([i,j],range(6)))
    ker=A.nullspace()
    assert A.rank()==5 and len(ker)==1
    den=sp.ilcm(*[sp.denom(x) for x in ker[0]])
    vv=[int(den*x) for x in ker[0]]
    div=gcd(*[abs(t) for t in vv])
    vv=[t//div for t in vv]
    pfint=pf(vv)
    assert pfint in (1,25,30)
    assert rank2(A.tolist())==5
    bad=[]
    for d in product((0,1),repeat=4):
        if not any(d):continue
        C=c_of_d(d)
        AC=[[sum(int(A[r,t])*C[t][k] for t in range(6))&1
             for k in range(4)] for r in range(5)]
        rank=rank2(AC)
        assert rank in (2,3)
        if rank<3:bad.append(''.join(str(t) for t in d))
    assert bool(bad)==(pfint%2==0)
    if bad:assert bad==['0001','1110','1111']
    return {'indices':[i,j],
            'primitive_kernel':vv,
            'integer_pfaffian':pfint,
            'pfaffian_mod_2':pfint%2,
            'rank_A_mod_2':5,
            'bad_nonzero_momenta_F2':bad}


def analyze():
    points=[p for p in product((0,1),repeat=6) if any(p)]
    singular=[p for p in points if pf(p)%2==0]
    nonsingular=[p for p in points if pf(p)%2]
    assert len(points)==63 and len(singular)==35 and len(nonsingular)==28
    # Finite symplectic forms over F2: |GL4(2)|/|Sp4(2)| = 28.
    gl4=15*14*12*8
    sp4=2**4*(2**2-1)*(2**4-1)
    assert gl4==20160 and sp4==720 and gl4//sp4==28
    pairs=[pair_result(i,j) for i,j in combinations(range(6),2)]
    assert len(pairs)==15
    odd=[x for x in pairs if x['pfaffian_mod_2']==1]
    even=[x for x in pairs if x['pfaffian_mod_2']==0]
    assert len(odd)==12 and len(even)==3
    singular_points={tuple(x['primitive_kernel'][t]%2 for t in range(6)) for x in even}
    nonsingular_points={tuple(x['primitive_kernel'][t]%2 for t in range(6)) for x in odd}
    assert len(singular_points)==1 and len(nonsingular_points)==6
    return {'schema':'w33.native.klein_gauge_choices_f2.v1',
        'full_nonzero_bivectors':len(points),
        'Klein_quadric_decomposable':len(singular),
        'off_quadric_nondecomposable':len(nonsingular),
        'GL4_F2_order':gl4,
        'Sp4_F2_order':sp4,
        'symplectic_form_coset_count':gl4//sp4,
        'two_commutator_pairs':pairs,
        'pairs_surviving_full_F2_injectivity':len(odd),
        'pairs_losing_F2_injectivity':len(even),
        'distinct_good_F2_kernels':len(nonsingular_points),
        'distinct_bad_F2_kernels':len(singular_points),
        'optimized_pair':[0,5],
        'optimized_pair_primitive_kernel':[0,1,1,1,0,0],
        'optimized_pair_F2_is_one_of_28':True,
        'scope':'Finite-field algebra bridge: does not equate the 28 finite forms with physical photons, nor assert a canonical labeling by 8 Conwell heptads.'}


if __name__=="__main__":
    raw=json.dumps(analyze(),indent=2)+"\n"
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(raw,encoding="utf-8")
    else:print(raw,end="")
