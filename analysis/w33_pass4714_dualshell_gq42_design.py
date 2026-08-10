#!/usr/bin/env python3
"""Pass 4714 — the dual shells intrinsically reconstruct GQ(4,2).

Starting only from the selected [135,16,30]_2 code, obtain the 45 complements
of dual weight-132 words and project the 270 dual minimum triples to them.  The
resulting 45-point pair graph is SRG(45,12,3,3).  Its maximal cliques are exactly
27 K5s, and the 270 triples are precisely all C(5,3) triples inside those K5s.
Thus the dual shells reconstruct the point-line incidence of GQ(4,2) without
importing the historical protected-45 identification.  Integral ranks and Smith
forms are frozen as well.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,nullspace2
from w33_pass4587_w33_derived_d4_triality import rank_basis_int,span
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4714_DUALSHELL_GQ42_DESIGN_REGEN.json'

def rank_mod(A,p):
    A=np.asarray(A,dtype=np.int64).copy()%p;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]%p),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==A.shape[0]:break
    return r

def snf_nonzero(A):
    S=smith_normal_form(sp.Matrix(np.asarray(A,dtype=int)),domain=sp.ZZ)
    d=[abs(int(S[i,i])) for i in range(min(S.shape)) if S[i,i]]
    return Counter(d)

def main():
    _,_,_,_,_,Astar,_,apartments,_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    apartments=sorted(tuple(map(int,a)) for a in apartments);j=(1<<40)-1;cols=[]
    for c in range(40):
        m=0
        for r in np.flatnonzero(Astar[:,c]):m|=1<<int(r)
        cols.append(m)
    B9=rank_basis_int([cols[i]^cols[k] for i in range(40) for k in range(i+1,40) if Astar[i,k]])
    rep=lambda x:min(int(x),int(x)^j)
    def fib(ap):
        x=0
        for i in ap:x^=cols[i]
        return rep(x)
    def aline(ap):
        opp=[(a,b) for a,b in itertools.combinations(ap,2) if not Astar[a,b]]
        return tuple(sorted((rep(cols[opp[0][0]]^cols[opp[0][1]]),rep(cols[opp[1][0]]^cols[opp[1][1]]),fib(ap))))
    selected=sorted({aline(a) for a in apartments});sing=sorted(set().union(*(set(L) for L in selected)));sidx={x:i for i,x in enumerate(sing)}
    N=np.zeros((135,270),dtype=np.uint8)
    for c,L in enumerate(selected):
        for x in L:N[sidx[x],c]=1
    Cbasis=nullspace2(N.T);assert len(Cbasis)==16

    # A 3-subset T is the complement of a dual weight-132 word iff 1+1_T is
    # orthogonal to every basis vector of C.
    sig=[]
    for i in range(135):
        z=0
        for r,b in enumerate(Cbasis):
            if b[i]:z|=1<<r
        sig.append(z)
    parity=0
    for r,b in enumerate(Cbasis):
        if int(b.sum())&1:parity|=1<<r
    bysig=defaultdict(list)
    for i,z in enumerate(sig):bysig[z].append(i)
    packets=set()
    for i in range(135):
        for k in range(i+1,135):
            for l in bysig.get(parity^sig[i]^sig[k],()):
                if l>k:packets.add((i,k,l))
    packets=sorted(packets);assert len(packets)==45
    assert Counter(i for T in packets for i in T)==Counter({i:1 for i in range(135)})
    packet_of={i:t for t,T in enumerate(packets) for i in T}

    projected=[]
    for L in selected:
        T=tuple(sorted(packet_of[sidx[x]] for x in L));assert len(set(T))==3;projected.append(T)
    assert len(set(projected))==270
    pairmult=Counter()
    for T in projected:
        for a,b in itertools.combinations(T,2):pairmult[(a,b)]+=1
    assert Counter(pairmult.values())==Counter({3:270})
    G45=nx.Graph();G45.add_nodes_from(range(45));G45.add_edges_from(pairmult)
    assert set(dict(G45.degree()).values())=={12}
    for a,b in itertools.combinations(range(45),2):
        c=len(set(G45[a])&set(G45[b]));assert c==3

    K5=sorted((frozenset(c) for c in nx.find_cliques(G45) if len(c)==5),key=lambda x:tuple(sorted(x)))
    assert len(K5)==27 and all(len(c)==5 for c in K5)
    # Every projected triple lies in a unique K5 and every K5 contributes all ten triples.
    owner=[]
    for T in projected:
        hits=[i for i,S in enumerate(K5) if set(T)<=S];assert len(hits)==1;owner.append(hits[0])
    assert Counter(owner)==Counter({i:10 for i in range(27)})

    H=np.zeros((45,270),dtype=np.int64)
    for c,T in enumerate(projected):H[list(T),c]=1
    B=np.zeros((45,27),dtype=np.int64)
    for c,S in enumerate(K5):B[list(S),c]=1
    assert set(H.sum(1))=={18} and set(H.sum(0))=={3}
    assert set(B.sum(1))=={3} and set(B.sum(0))=={5}
    A45=nx.to_numpy_array(G45,dtype=np.int64)
    assert np.array_equal(H@H.T,18*np.eye(45,dtype=np.int64)+3*A45)
    assert np.array_equal(B@B.T,3*np.eye(45,dtype=np.int64)+A45)

    G27=nx.Graph();G27.add_nodes_from(range(27))
    for a,b in itertools.combinations(range(27),2):
        if K5[a]&K5[b]:G27.add_edge(a,b)
    assert set(dict(G27.degree()).values())=={10}
    lam=set();mu=set()
    for a,b in itertools.combinations(range(27),2):
        c=len(set(G27[a])&set(G27[b]));(lam if G27.has_edge(a,b) else mu).add(c)
    assert lam=={1} and mu=={5}

    sh=snf_nonzero(H); sb=snf_nonzero(B)
    assert sh==Counter({1:44,3:1}) and sb==Counter({1:21})
    ranksH={str(p):rank_mod(H,p) for p in (2,3,5,7)}
    ranksB={str(p):rank_mod(B,p) for p in (2,3,5,7)}
    assert ranksH=={'2':45,'3':44,'5':45,'7':45}
    assert ranksB=={'2':21,'3':21,'5':21,'7':21}

    # The dual 27-vertex graph is much faster to enumerate than the 45 graph;
    # its automorphism group is exactly the automorphism group of the reconstructed
    # point-line geometry because the 45 points are recovered as the 3-line pencils.
    aut=0
    for _ in nx.algorithms.isomorphism.GraphMatcher(G27,G27).isomorphisms_iter():aut+=1
    assert aut==51840

    out={'pass':4714,'packets':45,'projected_triples':270,
      'pair_graph':{'parameters':[45,12,3,3],'maximal_K5':27,'local_graph':'3 K4'},
      'hypergraph':{'description':'all 10 three-subsets of each of the 27 K5 lines','point_degree':18,'triple_size':3},
      'GQ':{'order':[4,2],'points':45,'lines':27,'point_lines':3,'line_points':5,'dual_point_graph':[27,10,1,5]},
      'triangle_incidence':{'shape':[45,270],'rank_Q':45,'ranks_mod':ranksH,'SNF_nonzero':{'1':44,'3':1},'gram':'18 I + 3 A45'},
      'point_line_incidence':{'shape':[45,27],'rank_Q':21,'ranks_mod':ranksB,'SNF_nonzero':{'1':21},'gram':'3 I + A45'},
      'automorphism_group_order':aut,
      'theorem':'The weight-132 packet shell plus the weight-3 dual minimum shell intrinsically reconstruct GQ(4,2): the 45-packet pair graph is SRG(45,12,3,3), its 27 maximal K5s are the GQ lines, and the 270 projected triples are exactly all three-subsets of those lines. The dual line graph is SRG(27,10,1,5).',
      'boundary':'Exact binary-code/design theorem; no protected-45 identification is used in the reconstruction.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
