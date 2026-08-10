#!/usr/bin/env python3
"""Pass 4694 -- the faithful Golay sextet translation module is not the cubic O^-(6,2) six-space.

Pass4690 produces a normal regular N=C2^6 translation group and a faithful
order-2160 point stabilizer K acting linearly on N by conjugation.  Equal
six-dimensional cardinality tempts an identification with the natural cubic
minus-type U6.  This verifier solves the complete invariance equations instead.

For quadratic functions q:F2^6->F2 with q(0)=0 there are 21 coefficients (six
linear plus fifteen square-free cross terms).  K-invariance on all 64 vectors
has nullity zero.  For arbitrary bilinear forms there are 36 coefficients;
G^T B G=B likewise has nullity zero.  Thus this faithful K-module has no nonzero
invariant quadratic or bilinear form at all and cannot be the orthogonal U6
module.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4632_periodic_homology_module_separation as lin
import w33_pass4633_m24_sextet_section_stabilizer as p
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4694_GOLAY_AFFINE_U6_FORM_NOGO.json'
I=bytes(range(24))

def order(g):
    x=I
    for n in range(1,25):
        x=p.comp(g,x)
        if x==I:return n
    raise AssertionError
def conj(g,n):return p.comp(p.comp(g,n),p.inv(g))
def monomials(x):
    b=[(x>>i)&1 for i in range(6)];out=b[:]
    for i in range(6):
        for j in range(i+1,6):out.append(b[i]&b[j])
    return out
def apply(M,x):
    y=0
    for j in range(6):
        if (x>>j)&1:
            for i in range(6):y^=(int(M[i,j])&1)<<i
    return y

def main()->int:
    d=p.build();H=d['H'];K=d['K'];Kgens=d['Kgens'];tetrads=[frozenset(x) for x in d['sextet']]
    M={g for g in H if all(p.act_set(T,g)==T for T in tetrads)}
    N={g for g in M if order(g)<=2};assert len(N)==64
    basis=[];span={I:0}
    for n in N:
        if n in span:continue
        bit=1<<len(basis);basis.append(n)
        for g,c in list(span.items()):span[p.comp(n,g)]=c|bit
        if len(span)==64:break
    assert len(basis)==6 and len(span)==64
    mats=[]
    for k in Kgens:
        A=np.zeros((6,6),dtype=np.uint8)
        for j,n in enumerate(basis):
            c=span[conj(k,n)]
            for i in range(6):A[i,j]=(c>>i)&1
        mats.append(A)
    # Quadratic invariants: linear + square-free degree-two monomials.
    eq=[]
    for A in mats:
        for x in range(64):
            mx=monomials(x);my=monomials(apply(A,x));r=sum((mx[i]^my[i])<<i for i in range(21))
            if r:eq.append(r)
    qnull=len(lin.nullspace(eq,21));assert qnull==0
    # Arbitrary invariant bilinear forms.
    eq=[]
    for A in mats:
        for a in range(6):
            for b in range(6):
                r=1<<(6*a+b)
                for i in range(6):
                    if A[i,a]:
                        for j in range(6):
                            if A[j,b]:r^=1<<(6*i+j)
                if r:eq.append(r)
    bnull=len(lin.nullspace(eq,36));assert bnull==0
    out={'pass':4694,'module':'faithful 6D F2 translation module N of the Golay sextet section stabilizer K','K_order':2160,'invariant_quadratic_space_dimension':qnull,'invariant_bilinear_space_dimension':bnull,'theorem':'The faithful Golay sextet translation module has no nonzero K-invariant quadratic form and no nonzero K-invariant bilinear form.  It is therefore not an orthogonal six-space and cannot be identified with the cubic O^-(6,2) module U6.','boundary':'Exact negative representation theorem.  It does not exclude more indirect functors, subquotients, or nonlinear relations between the Golay and cubic six-dimensional constructions.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
