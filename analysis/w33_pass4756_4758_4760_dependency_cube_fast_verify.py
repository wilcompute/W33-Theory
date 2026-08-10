#!/usr/bin/env python3
"""Fast regression verifier for Passes 4756, 4758 and 4760.

The full theorem builder retains the explicit PSp-equivariant reconstruction.
This CI verifier rederives the structural counts, 135 Q3 decomposition, and the
[40,24,6] binary intersection without the redundant C(40,6) scan.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4495_4502_distance_prism_reconstruction import geometry

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_W33_PASS4756_4758_4760_DEPENDENCY_CUBES.json'

def mask(S):return sum(1<<i for i in S)
def gf2_basis(vals):
    piv={};out=[]
    for x in vals:
        y=int(x)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;out.append(y);break
    return out
def reduce(x,basis):
    piv={}
    for b in basis:
        y=int(b)
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    y=int(x)
    while y:
        p=y.bit_length()-1
        if p in piv:y^=piv[p]
        else:break
    return y
def nullspace(rows,n=40):
    R=[int(x) for x in rows if x];rr=0;piv=[]
    for col in reversed(range(n)):
        k=next((i for i in range(rr,len(R)) if (R[i]>>col)&1),None)
        if k is None:continue
        R[rr],R[k]=R[k],R[rr]
        for i in range(len(R)):
            if i!=rr and ((R[i]>>col)&1):R[i]^=R[rr]
        piv.append(col);rr+=1
        if rr==len(R):break
    R=R[:rr];free=[c for c in range(n) if c not in set(piv)];out=[]
    for f in free:
        x=1<<f
        for row,p in zip(R,piv):
            if (row&x).bit_count()&1:x|=1<<p
        out.append(x)
    return out
def span(B):
    S={0}
    for b in B:S|={x^b for x in list(S)}
    return S
def kraw(n,j,i):
    from math import comb
    return sum((-1)**s*comb(i,s)*comb(n-i,j-s) for s in range(max(0,j-(n-i)),min(j,i)+1))

def main():
    pts,pidx,lines,A,apartments,_,_=geometry();A=np.asarray(A,dtype=np.uint8)
    residues=[]
    for C in itertools.combinations(range(40),4):
        if not np.any(np.sum(A[:,C],axis=1)&1):residues.append(tuple(C))
    assert len(residues)==270
    rm=[mask(r) for r in residues]
    cold=[set() for _ in range(270)]
    for i,j in itertools.combinations(range(270),2):
        if (rm[i]&rm[j]).bit_count()==2:cold[i].add(j);cold[j].add(i)
    assert sum(map(len,cold))//2==1620 and {len(x) for x in cold}=={12}

    tris=[]
    for a in range(270):
        for b in (x for x in cold[a] if x>a):
            for c in cold[a]&cold[b]:
                if c>b:tris.append((a,b,c))
    cir=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]==0]
    non=[t for t in tris if rm[t[0]]^rm[t[1]]^rm[t[2]]!=0]
    assert (len(tris),len(cir),len(non))==(1080,540,540)
    ec={tuple(sorted(e)):i for i,t in enumerate(cir) for e in itertools.combinations(t,2)}
    en={tuple(sorted(e)):i for i,t in enumerate(non) for e in itertools.combinations(t,2)}
    assert len(ec)==len(en)==1620 and set(ec)==set(en)
    B=nx.Graph();B.add_nodes_from(range(1080))
    for e in ec:B.add_edge(ec[e],540+en[e])
    comps=list(nx.connected_components(B));assert len(comps)==135
    assert all(len(C)==8 and nx.is_isomorphic(B.subgraph(C),nx.cubical_graph()) for C in comps)

    unions=[]
    for C in comps:
        R=set()
        for x in C:R.update(cir[x] if x<540 else non[x-540])
        assert len(R)==6
        H=nx.Graph();H.add_nodes_from(R)
        H.add_edges_from((a,b) for a,b in itertools.combinations(R,2) if b in cold[a])
        assert H.number_of_edges()==12 and set(dict(H.degree()).values())=={4}
        u=0
        for r in R:u|=rm[r]
        assert u.bit_count()==8
        v=np.array([(u>>i)&1 for i in range(40)],dtype=np.uint8)
        assert not np.any((A@v)&1)
        unions.append(u)
    U=sorted(set(unions));assert len(U)==135

    # C_star and H10^perp intersection.
    stars=[mask(i for i,L in enumerate(lines) if p in L) for p in range(40)]
    sb=gf2_basis(stars);rb=gf2_basis(rm);ub=gf2_basis(U)
    assert (len(sb),len(rb),len(ub),len(gf2_basis(sb+rb)))==(25,30,24,31)
    assert all(reduce(u,sb)==0 and reduce(u,rb)==0 for u in U)

    dual=nullspace(ub,40);assert len(dual)==16
    Wd=Counter(x.bit_count() for x in span(dual));assert sum(Wd.values())==2**16
    W={}
    for j in range(41):
        z=sum(c*kraw(40,j,i) for i,c in Wd.items())//(2**16)
        if z:W[j]=z
    assert W[0]==1 and W[6]==240 and W[8]==1485 and sum(W.values())==2**24

    # Construct all 240 claimed weight-6 words; W[6]=240 proves completeness.
    colpairs=set()
    for p,q in itertools.combinations(range(40),2):
        if any(p in L and q in L for L in lines):colpairs.add(stars[p]^stars[q])
    assert len(colpairs)==240
    for m in colpairs:
        assert m.bit_count()==6 and reduce(m,ub)==0
    cert=json.loads(CERT.read_text())
    assert cert['4756_dependency_geometry']['cold_triangles']==1080
    assert cert['4758_cube_reconstruction']['cube_union_words']==135
    assert cert['4760_binary_intersection_code']['parameters']=='[40,24,6]'
    print(json.dumps({'PASS':True,'triangles':[1080,540,540],'cubes':135,'intersection_rank':24,'A6':240,'A8':1485},sort_keys=True))
    return 0
if __name__=='__main__':raise SystemExit(main())
