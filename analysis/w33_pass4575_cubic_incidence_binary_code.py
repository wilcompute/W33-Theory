#!/usr/bin/env python3
"""Pass 4575 -- the 27x36 cubic line/double-six incidence is the natural O^-(6,2) bilinear code.

Passes 4525/4527 explicitly identified the 27 cubic-surface lines with the 27
nonzero singular vectors and the 36 double-sixes with the 36 anisotropic vectors
of the faithful six-dimensional minus-type module U6. Passes 4545/4549 then built
the integer incidence matrix R (line belongs to double-six), with rational rank 21.

This pass reduces that *same* incidence matrix modulo two and proves a much sharper
statement. After the frozen 4525/4527 conjugations,

    R[s,a] = B(s,a)

for every nonzero singular s and anisotropic a in U6, where B is the invariant
alternating polar form. Consequently rank_2(R)=6. The row and column images are
the natural six-dimensional O^-(6,2) module in two coordinate realizations:

    row code    [36,6,16], W=1+27 z^16+36 z^20,
    column code [27,6,12], W=1+36 z^12+27 z^16.

Both are self-orthogonal because RR^T=R^TR=0 mod 2. The dual kernels have
parameters [36,30,3] and [27,21,3]; the exact low-weight relation counts are
A3=120,A4=945 and A3=45,A4=270 respectively.

This is finite binary representation/coding geometry. It is not a physical
six-bit subsystem or particle identification.
"""
from __future__ import annotations

import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np

import w33_pass4522_4525_4527_dual_orthogonal_schlafli as p4522
import w33_pass4545_4549_schlafli_double_six_incidence_intertwiner as p4549

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4575_CUBIC_INCIDENCE_BINARY_CODE.json'
ISO27=[0,6,7,12,25,3,17,13,24,14,22,26,4,19,5,8,23,20,9,2,16,11,15,21,10,18,1]
ISO36=[0,21,5,14,13,31,34,6,22,20,12,8,18,4,26,30,1,32,35,24,10,25,16,2,15,28,33,19,23,7,17,9,11,29,27,3]


def rank2(A):
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


def build_actual_R():
    mod=p4549.load_cds();roots=mod.construct_e8_roots();orbits=mod.compute_we6_orbits(roots)
    orb27=[o for o in orbits if len(o)==27][0]
    r=roots[orb27];gram=np.rint(r@r.T).astype(int)
    skew=(gram==1);np.fill_diagonal(skew,False)
    k6=mod.find_k_cliques(skew,6);assert len(k6)==72
    ds=[]
    for ai,A in enumerate(k6):
        SA=set(A)
        for bi in range(ai+1,len(k6)):
            B=k6[bi];SB=set(B)
            if SA&SB:continue
            if all(sum(bool(skew[a,b]) for b in B)==1 for a in A) and all(sum(bool(skew[a,b]) for a in A)==1 for b in B):
                ds.append((tuple(A),tuple(B)))
    assert len(ds)==36
    supp=[frozenset(A)|frozenset(B) for A,B in ds]
    R=np.zeros((27,36),dtype=np.uint8)
    for j,S in enumerate(supp):
        for i in S:R[i,j]=1
    return R


def code_enumerator(rows):
    rows=np.asarray(rows,dtype=np.uint8);k=len(rows);C=Counter()
    for mask in range(1<<k):
        v=np.zeros(rows.shape[1],dtype=np.uint8)
        for i in range(k):
            if (mask>>i)&1:v^=rows[i]
        C[int(v.sum())]+=1
    return C


def independent_rows(A):
    A=np.asarray(A,dtype=np.uint8);basis=[];r=0
    for row in A:
        if rank2(np.asarray(basis+[row],dtype=np.uint8))>r:
            basis.append(row.copy());r+=1
    return basis


def low_kernel_counts(A,maxw=4):
    A=np.asarray(A,dtype=np.uint8);n=A.shape[1];out={}
    for w in range(1,maxw+1):
        c=0
        for S in itertools.combinations(range(n),w):
            if not np.any(np.bitwise_xor.reduce(A[:,S],axis=1)):c+=1
        out[w]=c
    return out


def main()->int:
    R=build_actual_R();assert R.shape==(27,36)
    d=p4522.build_module();F=d['F'];sing=d['singular'];anis=d['anis']
    # Orthogonal coordinates -> existing repository carriers, frozen in Pass4525/4527.
    Rc=R[np.asarray(ISO27),:][:,np.asarray(ISO36)]
    P=np.zeros((27,36),dtype=np.uint8)
    for i,s in enumerate(sing):
        sv=p4522.intvec(s,6)
        for j,a in enumerate(anis):
            av=p4522.intvec(a,6);P[i,j]=int(sv@F@av%2)
    assert np.array_equal(Rc,P)
    r=rank2(R);assert r==6
    assert not np.any((R@R.T)%2) and not np.any((R.T@R)%2)

    rb=independent_rows(R);cb=independent_rows(R.T)
    assert len(rb)==len(cb)==6
    Wr=code_enumerator(rb);Wc=code_enumerator(cb)
    assert Wr==Counter({20:36,16:27,0:1})
    assert Wc==Counter({12:36,16:27,0:1})
    kr=low_kernel_counts(R,4);kc=low_kernel_counts(R.T,4)
    assert kr=={1:0,2:0,3:120,4:945}
    assert kc=={1:0,2:0,3:45,4:270}

    out={
      'pass':4575,
      'incidence_identity':{
        'matrix':'the actual 27x36 cubic-line/double-six incidence from Pass4549',
        'orthogonal_coordinates':'R[s,a]=B(s,a) for the 27 nonzero singular and 36 anisotropic vectors of U6',
        'entrywise_verified_through_frozen_4525_4527_isomorphisms':True},
      'binary_rank':6,
      'row_code':{'parameters':'[36,6,16]','weight_enumerator':{'0':1,'16':27,'20':36},'self_orthogonal':True,
                  'dual_kernel':{'parameters':'[36,30,3]','A3':120,'A4':945}},
      'column_code':{'parameters':'[27,6,12]','weight_enumerator':{'0':1,'12':36,'16':27},'self_orthogonal':True,
                     'dual_kernel':{'parameters':'[27,21,3]','A3':45,'A4':270}},
      'quadratic_reading':'the two nonzero weight shells are exactly the singular/anisotropic split of the natural O^-(6,2) module',
      'boundary':'Exact finite GF(2) coding/orthogonal geometry. No physical six-bit carrier is inferred.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
