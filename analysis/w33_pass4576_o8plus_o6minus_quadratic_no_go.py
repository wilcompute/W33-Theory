#!/usr/bin/env python3
"""Pass 4576 -- no equivariant Boolean map of degree <=2 between protected O+(8,2) and cubic O-(6,2).

Pass4556 proved Hom_G(H10,U6)=Hom_G(U6,H10)=0 for G=PSp(4,3), so no linear
protected-to-exceptional-six transport exists. Pass4575 identifies the cubic
line/double-six incidence code itself with the natural six-dimensional U6.
This pass asks whether the nonlinear bridge can already appear quadratically.

It cannot. Reconstruct the protected V8=V9/<j> action from the H10 line-star
module and the cubic U6 action from Pass4522, with the same five PSp generators.
Represent every Boolean polynomial function of degree <=2 by the square-free
monomial basis {1,x_i,x_i x_j}; dimensions are 37 for eight input bits and 22 for
six. Exact GF(2) equivariance equations

    C Phi(gx) = g C Phi(x)

have full ranks 222 and 176 respectively. Hence the only degree<=2 equivariant
polynomial maps V8->U6 and U6->V8 are zero.
"""
from __future__ import annotations

import json,itertools
from pathlib import Path
import numpy as np

import w33_pass4522_4525_4527_dual_orthogonal_schlafli as p4522
import w33_pass4511_4514_dual_even_prism_ihara as p4514
from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4576_O8PLUS_O6MINUS_QUADRATIC_NO_GO.json'
COLS=[0,1,2,3,4,5,7,8,10,11]


def perm_mask(m,p):
    out=0
    while m:
        b=m&-m;i=b.bit_length()-1;out|=1<<p[i];m-=b
    return out


def apply_cols(cols,x):
    out=0
    while x:
        b=x&-x;i=b.bit_length()-1;out^=cols[i];x-=b
    return out


def cols_to_np(cols,d):return p4522.cols_to_np(cols,d).astype(np.uint8)


def gf2_rank(A):
    A=np.asarray(A,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
        if r==m:break
    return r


def protected_v8_generators():
    pts,pidx,lines,A,apartments,apmasks,H=geometry();selected,psp,outer,pgsp=p4514.build_groups(pts,pidx,lines)
    hcols=[sum(int(A[i,c])<<i for i in range(40) if A[i,c]) for c in COLS]
    HC=p4522.CoordBasis()
    for x in hcols:assert HC.add(x)
    Hgens=[]
    for _,lp in selected:
        Hgens.append([HC.coords(perm_mask(x,lp)) for x in hcols])
        assert None not in Hgens[-1]
    j=(1<<40)-1;jc=HC.coords(j);assert jc is not None and jc.bit_count()%2==0
    V9=p4522.CoordBasis();V9.add(jc)
    for i in range(9):V9.add((1<<i)^(1<<9))
    assert len(V9.orig)==9
    V9g=[]
    for g in Hgens:
        cols=[]
        for x in V9.orig:
            z=V9.coords(apply_cols(g,x));assert z is not None;cols.append(z)
        V9g.append(cols)
    V8g=[[g[j]>>1 for j in range(1,9)] for g in V9g]
    return [cols_to_np(g,8) for g in V8g]


def monomial_transform(M):
    d=M.shape[0];pairs=[(i,j) for i in range(d) for j in range(i+1,d)]
    qdim=1+d+len(pairs);idx={p:1+d+k for k,p in enumerate(pairs)}
    Q=np.zeros((qdim,qdim),dtype=np.uint8);Q[0,0]=1
    for i in range(d):
        for a in range(d):
            if M[i,a]:Q[1+i,1+a]^=1
    r=1+d
    for i,j in pairs:
        for a in range(d):
            if M[i,a]:
                for b in range(d):
                    if M[j,b]:
                        if a==b:Q[r,1+a]^=1
                        else:Q[r,idx[tuple(sorted((a,b)))]]^=1
        r+=1
    return Q


def equivariance_rank(input_gens,output_gens):
    din=input_gens[0].shape[0];dout=output_gens[0].shape[0];qdim=1+din+din*(din-1)//2
    eq=[]
    for G,H in zip(input_gens,output_gens):
        Q=monomial_transform(G)
        for r in range(dout):
            for j in range(qdim):
                row=np.zeros(dout*qdim,dtype=np.uint8)
                for k in range(qdim):
                    if Q[k,j]:row[r*qdim+k]^=1
                for s in range(dout):
                    if H[r,s]:row[s*qdim+j]^=1
                eq.append(row)
    rank=gf2_rank(np.asarray(eq,dtype=np.uint8));return rank,dout*qdim


def main()->int:
    V8=protected_v8_generators();d=p4522.build_module();U6=[np.asarray(g,dtype=np.uint8) for g in d['G6']]
    assert len(V8)==len(U6)==5
    r86,n86=equivariance_rank(V8,U6);r68,n68=equivariance_rank(U6,V8)
    assert (r86,n86)==(222,222) and (r68,n68)==(176,176)
    out={'pass':4576,'group':'PSp(4,3)','source_modules':{'protected':'V8=O+(8,2) middle protected factor','cubic':'U6=O-(6,2) cubic incidence factor'},
      'boolean_degree_le2':{
        'V8_to_U6':{'unknown_coefficients':222,'equation_rank':222,'solution_dimension':0},
        'U6_to_V8':{'unknown_coefficients':176,'equation_rank':176,'solution_dimension':0}},
      'theorem':'No nonzero PSp(4,3)-equivariant Boolean polynomial map of degree <=2 exists in either direction between V8 and U6.',
      'next_possible_bridge':'degree >=3, a larger intermediate/permutation module, or explicit symmetry breaking',
      'boundary':'Finite modular-representation obstruction. It does not exclude non-polynomial physical maps or maps after enlarging/breaking symmetry.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
