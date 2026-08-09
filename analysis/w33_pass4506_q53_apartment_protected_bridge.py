#!/usr/bin/env python3
"""Pass 4506 -- concrete GQ(3,9) apartment-to-protected bridge and dual failure.

Pass 4471 proved the parity criterion H H^T=N^T N iff s=3 mod 4 and t odd.
This pass executes the theorem on the repo's independently constructed
Q(5,3)=GQ(3,9), rather than stopping at the formula.

For Q(5,3):

  112 points, 280 lines, 102060 apartments,
  rank(H)=279,
  rank(N)=91,
  rank(N^T N)=70,
  dim rad(C_ap)=279-70=209,
  dim C_ap/rad=70,
  dim im(N)/ker(N^T)=91-21=70.

The canonical map [b] -> [N b] therefore scales the W33 bridge from dimension
10 to dimension 70, with H H^T=N^T N checked entry-by-entry over F2.

For the dual GQ(9,3) orientation, using the SAME building apartments:

  rank(H_dual)=111,
  rank(H_dual H_dual^T)=1,
  rank(N N^T)=22,

and the two Gram matrices are unequal.  In fact the dual apartment Gram is the
all-ones matrix.  This is a sharp concrete witness that the bridge is genuinely
orientation-sensitive in characteristic two.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

from w33_pass4448_4450_q53_floquet_tanner import build_q53

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4506_Q53_APARTMENT_PROTECTED_BRIDGE.json"


def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows):continue
        rr=r+int(rows[0])
        if rr!=r:A[[r,rr]]=A[[rr,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
        if r==m:break
    return r


def nullspace2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows):continue
        rr=r+int(rows[0])
        if rr!=r:A[[r,rr]]=A[[rr,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,c in reversed(list(enumerate(piv))):x[c]=int(np.dot(A[i],x)%2)
        out.append(x)
    return np.asarray(out,dtype=np.uint8)


def rank_bit_rows(rows):
    piv={}
    for x in rows:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)


def main()->int:
    pts,lines=build_q53();P=len(pts);L=len(lines)
    assert (P,L)==(112,280)
    N=np.zeros((P,L),dtype=np.uint8)
    for j,line in enumerate(lines):N[list(line),j]=1
    assert rank2(N)==91

    # Line-intersection graph: the apartment supports are its induced C4s.
    A=np.zeros((L,L),dtype=np.uint8)
    for i,j in itertools.combinations(range(L),2):
        if lines[i]&lines[j]:A[i,j]=A[j,i]=1
    assert np.all(A.sum(1)==36)
    nb=[set(np.flatnonzero(A[i]).tolist()) for i in range(L)]
    apartments=set()
    for u,w in itertools.combinations(range(L),2):
        if A[u,w]:continue
        common=sorted(nb[u]&nb[w]);assert len(common)==4
        for a,b in itertools.combinations(common,2):
            if not A[a,b]:apartments.add(tuple(sorted((u,w,a,b))))
    apartments=sorted(apartments);assert len(apartments)==102060

    # Store H rows as Python bitsets: 280 x 102060 without a dense 28MB matrix.
    Hrows=[0]*L
    Gram=np.zeros((L,L),dtype=np.uint8)
    for j,ap in enumerate(apartments):
        bit=1<<j
        for x in ap:Hrows[x]|=bit
        for x in ap:
            for y in ap:Gram[x,y]^=1
    rH=rank_bit_rows(Hrows);assert rH==279
    Ast=(N.T@N)%2
    assert np.array_equal(Gram,Ast)
    rAst=rank2(Ast);assert rAst==70 and not np.any(np.diag(Ast))

    C=nullspace2(N.T);assert len(C)==21
    imN=N.T # rowspace(N.T) is the point-coordinate image of N
    assert rank2(np.vstack((imN,C)))==rank2(imN)==91
    protected_dim=91-21;assert protected_dim==70
    radical_dim=rH-rAst;assert radical_dim==209

    # Dual orientation: its lines are the 112 original points.  Each building
    # apartment supplies the four intersection points of its original four lines.
    Hdrows=[0]*P
    DGram=np.zeros((P,P),dtype=np.uint8)
    for j,ap in enumerate(apartments):
        ps=set()
        for a,b in itertools.combinations(ap,2):
            q=lines[a]&lines[b]
            if q:assert len(q)==1;ps|=set(q)
        assert len(ps)==4
        bit=1<<j
        for p in ps:Hdrows[p]|=bit
        for p in ps:
            for q in ps:DGram[p,q]^=1
    rHd=rank_bit_rows(Hdrows);assert rHd==111
    dual_incidence_gram=(N@N.T)%2
    assert rank2(DGram)==1 and rank2(dual_incidence_gram)==22
    assert np.array_equal(DGram,np.ones((P,P),dtype=np.uint8))
    assert not np.array_equal(DGram,dual_incidence_gram)

    out={
      "pass":4506,
      "theorem":"Q(5,3)=GQ(3,9) realizes a 70D apartment-protected quotient; the dual GQ(9,3) orientation fails the Gram bridge",
      "GQ_3_9":{"points":112,"lines":280,"apartments":102060,"rank_H":279,"rank_N":91,"rank_NtN":70,"apartment_radical_dimension":209,"protected_quotient_dimension":70,"sentinel_dimension":21,"gram_identity_HHt_eq_NtN":True,"canonical_map":"[b] -> [N b]"},
      "dual_GQ_9_3":{"lines_as_original_points":112,"rank_H_dual":111,"rank_apartment_gram":1,"rank_incidence_gram":22,"apartment_gram_is_all_ones":True,"gram_identity":False},
      "scaling_from_W33":"protected dimension 10 -> 70 while the same incidence-quotient construction remains exact in the passing orientation",
      "boundary":"This is an exact binary incidence/apartment theorem for the concrete Q(5,3) builder. It does not identify 70 with a physical state count or claim the same rank formula for every generalized quadrangle without separate computation."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=="__main__":raise SystemExit(main())
