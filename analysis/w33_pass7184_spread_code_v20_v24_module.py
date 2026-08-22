#!/usr/bin/env python3
"""Pass7184: identify the 27-spread [45,21,5] code as 1 + V20 and its dual as V24.

The 45 coordinates are the selected orthogonal D4+D4 / tritangent supports.  The
27 ten-D4 spreads generate C21.  Pass7182 proved C21^perp is the 120-Steiner
K3,3 circuit code [45,24,6].  Here we additionally identify the even subcode of
C21 equivariantly with the previously certified binary tritangent selector V20.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
from collections import deque
import numpy as np
import networkx as nx
import w33_pass7163_7170_e8_hexagonal_lift as e8
from w33_pass4992_4999_common import build_base,build_group,gf2_rank_int

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7184_SPREAD_CODE_V20_V24_MODULE.json'

def piv_basis(rows):
    P={}
    for x0 in rows:
        x=int(x0)
        while x:
            k=x.bit_length()-1
            if k in P:x^=P[k]
            else:P[k]=x;break
    return [P[k] for k in sorted(P,reverse=True)]

def coord_basis(rows):
    piv={};basis=[]
    for x0 in rows:
        x=int(x0);c=0
        for p in sorted(piv,reverse=True):
            if (x>>p)&1:x^=piv[p][0];c^=piv[p][1]
        if x:
            i=len(basis);p=x.bit_length()-1;piv[p]=(x,1<<i);basis.append(x)
    def express(x):
        x=int(x);c=0
        for p in sorted(piv,reverse=True):
            if (x>>p)&1:x^=piv[p][0];c^=piv[p][1]
        return x,c
    return basis,express

def vbits(mask,n):return np.array([(int(mask)>>i)&1 for i in range(n)],dtype=np.uint8)
def maskbits(v):return sum((int(x)&1)<<i for i,x in enumerate(v))

def nullspace(A):
    R=np.array(A,dtype=np.uint8)%2;m,n=R.shape;r=0;piv=[]
    for c in range(n):
        k=next((i for i in range(r,m) if R[i,c]),None)
        if k is None:continue
        if k!=r:R[[r,k]]=R[[k,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        piv.append(c);r+=1
        if r==m:break
    free=[c for c in range(n) if c not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for rr,c in enumerate(piv):
            if R[rr,f]:x[c]=1
        out.append(x)
    return np.array(out,dtype=np.uint8)

def perm_mask(mask,p):
    y=0;x=int(mask)
    while x:
        lb=x&-x;i=lb.bit_length()-1;y|=1<<p[i];x^=lb
    return y

def center_data(adj):
    Q=set()
    for a,b,c in itertools.combinations(range(40),3):
        if b in adj[a] or c in adj[a] or c in adj[b]:continue
        X=frozenset(adj[a]&adj[b]&adj[c])
        if len(X)==4:Q.add(X)
    Q=sorted(Q,key=lambda z:tuple(sorted(z)));qi={q:i for i,q in enumerate(Q)};partner={}
    for i,q in enumerate(Q):partner[i]=qi[frozenset(set.intersection(*(adj[x] for x in q)))]
    pairs=sorted({tuple(sorted((i,j))) for i,j in partner.items()});assert len(Q)==90 and len(pairs)==45
    supports=[frozenset(Q[i]|Q[j]) for i,j in pairs]
    packs=[]
    for C in itertools.combinations(range(45),5):
        U=set();ok=True
        for z in C:
            if U&supports[z]:ok=False;break
            U|=supports[z]
        if ok and len(U)==40:packs.append(C)
    assert len(packs)==27
    return Q,pairs,supports,packs

def action_on_basis(basis,express,p,n):
    d=len(basis);A=np.zeros((d,d),dtype=np.uint8)
    for j,x in enumerate(basis):
        rem,c=express(perm_mask(x,p));assert rem==0;A[:,j]=vbits(c,d)
    return A

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=e8.e8_fibers();Q,pairs,supports,packs=center_data(adj)
    rows=[sum(1<<z for z in C) for C in packs];B21=piv_basis(rows);assert len(B21)==21
    ones=(1<<45)-1
    # all-ones is in C21; parity is nonzero, so the even kernel is dimension 20.
    fullbasis,fullexpr=coord_basis(B21);rem,_=fullexpr(ones);assert rem==0
    odd=next(x for x in B21 if x.bit_count()&1)
    evenrows=[]
    for x in B21:
        y=x if x.bit_count()%2==0 else x^odd
        if y:evenrows.append(y)
    B20=piv_basis(evenrows);assert len(B20)==20 and all(x.bit_count()%2==0 for x in B20)
    evenbasis,evenexpr=coord_basis(B20)
    # Match our intrinsic 45 supports to the canonical cubic-surface tritangent indexing.
    base=build_base();grp=build_group(base);T=base['tritangents']
    Gs=nx.Graph();Gs.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if supports[i].isdisjoint(supports[j]):Gs.add_edge(i,j)
    Gt=nx.Graph();Gt.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if set(T[i])&set(T[j]):Gt.add_edge(i,j)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(Gs,Gt).isomorphisms_iter())
    p_s_to_t=tuple(iso[i] for i in range(45));inv=[0]*45
    for i,j in enumerate(p_s_to_t):inv[j]=i
    # Rewrite C20 basis on canonical tritangent coordinates.
    C20=[perm_mask(x,p_s_to_t) for x in B20];cbasis,cexpr=coord_basis(C20);assert len(cbasis)==20
    # Canonical V20 selector code = row span of the 45x36 tritangent/double-six selector M mod 2.
    Vrows=[maskbits(row) for row in (base['M']%2)];vbasis,vexpr=coord_basis(Vrows);assert len(vbasis)==20
    tri_index={tuple(t):i for i,t in enumerate(T)}
    def tperm(g):return tuple(tri_index[tuple(sorted(g[x] for x in t))] for t in T)
    tp=[tperm(g) for g in grp['gp']];td=tperm(grp['trans'][0])
    CA=[action_on_basis(cbasis,cexpr,p,45) for p in tp]
    VA=[action_on_basis(vbasis,vexpr,p,36) for p in grp['DPp']]
    # Solve X*CA = VA*X for X: C20 -> V20. Unique Hom line, nonzero map invertible.
    eq=[]
    for Ac,Av in zip(CA,VA):
        for a in range(20):
            for c in range(20):
                row=np.zeros(400,dtype=np.uint8)
                for j in range(20):
                    if Av[a,j]:row[j*20+c]^=1
                    if Ac[j,c]:row[a*20+j]^=1
                if row.any():eq.append(row)
    H=nullspace(np.array(eq,dtype=np.uint8));assert H.shape[0]==1
    X=H[0].reshape(20,20);assert gf2_rank_int(maskbits(r) for r in X)==20
    Co=action_on_basis(cbasis,cexpr,td,45);Vo=action_on_basis(vbasis,vexpr,grp['DPf'][-1],36)
    assert np.array_equal((Vo@X)%2,(X@Co)%2)
    # Build the 120 K3,3 circuit supports and verify exact orthogonal complement.
    independent=[frozenset(x) for x in itertools.combinations(range(45),3) if all(not Gt.has_edge(a,b) for a,b in itertools.combinations(x,2))]
    IS=set(independent);K=set()
    for A in independent:
        N=set(range(45))
        for a in A:N&=set(Gt[a])
        for z in itertools.combinations(sorted(N),3):
            B=frozenset(z)
            if B in IS and len(A|B)==6:K.add(frozenset(A|B))
    assert len(K)==120
    Krows=[sum(1<<i for i in s) for s in K];assert len(piv_basis(Krows))==24
    # coordinate reorder spread rows before orthogonality test
    spreadT=[perm_mask(x,p_s_to_t) for x in rows]
    assert all((x&y).bit_count()%2==0 for x in spreadT for y in Krows)
    out={
      'schema':'w33.pass7184.spread_code_v20_v24_module.v1','status':'PASS',
      'spread_code':'[45,21,5]_2','spread_generators':27,'all_ones_in_spread_code':True,
      'even_subcode_dimension':20,'direct_sum':'C_spread = <1_45> direct_sum C_even over F2',
      'V20_identification':{'target':'Pass5001 binary tritangent-selector V20','PSp_Hom_dimension':1,'unique_nonzero_intertwiner_rank':20,'outer_PGSp_generator_intertwined':True,'full_group_equivariant_isomorphism':True},
      'dual_code':'[45,24,6]_2','dual_minimum_K3,3_words':120,'spread_times_circuit_transpose_zero':True,
      'module_dictionary':'[45,21,5] = 1 + V20_trit and [45,24,6] = V24 (binary full-group modules, with the displayed explicit intertwiner for V20).',
      'repo_bridge':'Pass5001 owns V20_trit; Pass5019 owns the 120-Steiner/K3,3 V24. This pass identifies the 27 E8 ten-D4 spread code as their 1+20 orthogonal complement.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Hom':1,'spread':'[45,21,5]','dual':'[45,24,6]'}))
if __name__=='__main__':main()
