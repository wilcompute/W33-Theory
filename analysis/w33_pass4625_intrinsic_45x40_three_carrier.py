#!/usr/bin/env python3
"""Pass 4625 -- the 45x40 incidence intrinsically contains three carriers.

The matrix T is the center-quad 8-point support incidence from Pass4617.  This
pass studies T without using its construction labels.  Its integer Smith form is
1^15 2^10 0^15.  Row intersections reconstruct the 45 center-quad/E6 graph;
column intersections reconstruct the point-side W33 graph; and the 40 minimum
weight-four words of ker_F2(T) reconstruct the line-side W33 carrier.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ
from exploration.w33_center_quad_gq42_e6_bridge import quotient_points, w33_lines

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4625_INTRINSIC_45X40_THREE_CARRIER.json'

def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        r+=1
        if r==m:break
    return r

def nullspace2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
        z=np.flatnonzero(A[r:,c])
        if not len(z):continue
        k=r+int(z[0]);A[[r,k]]=A[[k,r]]
        for i in np.flatnonzero(A[:,c]):
            if i!=r:A[i]^=A[r]
        piv.append(c);r+=1
        if r==m:break
    out=[]
    for f in [c for c in range(n) if c not in piv]:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,c in reversed(list(enumerate(piv))):x[c]=int(np.dot(A[i],x)%2)
        out.append(x)
    return out

def span_words(B):
    C=[np.zeros_like(B[0])]
    for b in B:C += [x^b for x in list(C)]
    return C

def srg(A):
    A=np.asarray(A,dtype=np.uint8);v=len(A);ks=set(map(int,A.sum(1)));la=set();mu=set()
    for i,j in itertools.combinations(range(v),2):
        c=int(A[i].astype(int)@A[j].astype(int));(la if A[i,j] else mu).add(c)
    assert len(ks)==len(la)==len(mu)==1
    return [v,next(iter(ks)),next(iter(la)),next(iter(mu))]

def main()->int:
    points=quotient_points();assert len(points)==45
    T=np.zeros((45,40),dtype=np.int64)
    for i,p in enumerate(points):T[i,list(p.support_vertices)]=1
    assert set(map(int,T.sum(1)))=={8} and set(map(int,T.sum(0)))=={9}

    D=smith_normal_form(sp.Matrix(T),domain=ZZ)
    diag=[abs(int(D[i,i])) for i in range(min(D.shape))]
    snf=Counter(diag);assert snf==Counter({1:15,2:10,0:15})
    assert int(sp.Matrix(T).rank())==25 and rank2(T)==15

    RR=T@T.T;CC=T.T@T
    A45=np.zeros((45,45),dtype=np.uint8)
    for i,j in itertools.combinations(range(45),2):
        z=int(RR[i,j]);assert z in (0,2)
        if z==2:A45[i,j]=A45[j,i]=1
    Apoint=np.zeros((40,40),dtype=np.uint8)
    for i,j in itertools.combinations(range(40),2):
        z=int(CC[i,j]);assert z in (1,3)
        if z==3:Apoint[i,j]=Apoint[j,i]=1
    assert srg(A45)==[45,32,22,24] and srg(Apoint)==[40,12,2,4]
    assert np.array_equal(RR,8*np.eye(45,dtype=int)+2*A45.astype(int))
    assert np.array_equal(CC,8*np.eye(40,dtype=int)+2*Apoint.astype(int)+np.ones((40,40),dtype=int))

    # Binary kernel: the complete weight-four minimum shell is exactly the W33 lines.
    K=nullspace2(T);assert len(K)==25
    lines=w33_lines();assert len(lines)==40
    linewords=[]
    for L in lines:
        x=np.zeros(40,dtype=np.uint8);x[list(L)]=1
        assert not np.any((T@x)%2);linewords.append(x)
    assert len({bytes(x) for x in linewords})==40
    # The exact context-code enumerator already proves there are exactly 40
    # weight-four kernel words; verify the frozen certificate and hence completeness.
    old=json.loads((ROOT/'data/w33_pass228_sentinel_weight_enumerator.json').read_text())
    assert old['context_40_25_4_via_macwilliams']['low_weight_spectrum']['4']==40
    # The line-side graph is recovered from intersections among those 40 words.
    Aline=np.zeros((40,40),dtype=np.uint8)
    for i,j in itertools.combinations(range(40),2):
        z=int(linewords[i]@linewords[j]);assert z in (0,1)
        if z==1:Aline[i,j]=Aline[j,i]=1
    assert srg(Aline)==[40,12,2,4]

    # Because TT^T=0 mod2, im(T^T)=row(T) lies in ker(T); the middle homology is 10D.
    assert not np.any((T@T.T)%2)
    hdim=len(K)-rank2(T);assert hdim==10

    out={
      'pass':4625,
      'matrix':{'shape':[45,40],'row_weight':8,'column_weight':9,'rank_Q':25,'rank_F2':15,
        'smith_normal_form':{'1':15,'2':10,'0':15},'rank_over_every_odd_characteristic':25},
      'row_carrier':{'rule':'join rows iff support intersection is 2','graph':'SRG(45,32,22,24)','identity':'TT^T=8I+2A45'},
      'point_carrier':{'rule':'join columns iff co-occurrence is 3','graph':'point-side W33 SRG(40,12,2,4)','identity':'T^TT=8I+2A_point+J'},
      'line_carrier':{'binary_kernel_dimension':25,'minimum_weight':4,'minimum_words':40,'minimum_words_are_exactly_W33_lines':True,'intersection_graph':'line-side W33 SRG(40,12,2,4)'},
      'binary_complex':{'TTt_zero':True,'im_Tt_dimension':15,'ker_T_dimension':25,'middle_homology_dimension':10},
      'bipartite_spectrum':{'nonzero':'(+/-6 sqrt(2))^1, (+/-2 sqrt(3))^24','zero_multiplicity':35},
      'theorem':'The unlabeled 45x40 support incidence intrinsically reconstructs the E6/center-quad 45, the point-side W33 40, and the inequivalent line-side W33 40. Its Smith form is 1^15 2^10 0^15, so characteristic two is the unique rank-drop prime and the resulting middle binary homology has dimension ten.',
      'boundary':'The incidence determines the three finite carriers. A full automorphism-group equality is not claimed here without a separate exact automorphism computation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
