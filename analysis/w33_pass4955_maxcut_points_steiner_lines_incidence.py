#!/usr/bin/env python3
"""Pass4955 — correct the Pass4946 quotient labels: max-cut triples are W33 points,
Steiner fibers are W33 lines, and non-splitting is literal point-line incidence.

This verifier rebuilds the Pass4946 120x120 cross-incidence, collapses its identical
row/column triples, and compares the two quotient collinearity graphs with the
standard symplectic W(3,3) point graph and its line-intersection graph Q(4,3).
"""
from __future__ import annotations
import itertools, json
from collections import deque
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4955_MAXCUT_POINTS_STEINER_LINES_INCIDENCE.json'

def Q6(v):
    a,c,d,e,f,g=v;return (a*c+d*e+f+f*g+g)&1
def add2(a,b):return tuple(x^y for x,y in zip(a,b))
def polar(a,b):return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q):return tuple(p[q[i]] for i in range(len(q)))
def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S
def canon_cut(S,n=36):
    S=frozenset(S);T=frozenset(set(range(n))-set(S));return min((S,T),key=lambda z:tuple(sorted(z)))
def canon3(v):
    v=np.array(v,dtype=int)%3;j=next(i for i,x in enumerate(v) if x)
    return tuple((v*pow(int(v[j]),-1,3))%3)

def main()->int:
    # 36 double-sixes, Steiner triangles, and PSp action.
    vecs=[v for v in itertools.product((0,1),repeat=6) if any(v)]
    sing=[v for v in vecs if Q6(v)==0];nons=[v for v in vecs if Q6(v)==1];si={v:i for i,v in enumerate(sing)}
    trans=[tuple(si[add2(x,v) if polar(x,v) else x] for x in sing) for v in nons]
    gp=[];S={tuple(range(27))}
    for g in [comp(trans[0],t) for t in trans[1:]]:
        T=closure(gp+[g],27)
        if len(T)>len(S):gp.append(g);S=T
        if len(S)==25920:break
    assert len(S)==25920
    qp=[sum(bit<<i for i,bit in enumerate(v)) for v in sing]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36;di={S:i for i,S in enumerate(DS)}
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    st=sorted(t for t in itertools.combinations(range(36),3)
      if all(H36.has_edge(*e) for e in itertools.combinations(t,2))
      and len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert len(st)==120;sti={t:i for i,t in enumerate(st)}
    SP=[];DP=[]
    for g in gp:
        dp=tuple(di[frozenset(g[x] for x in S)] for S in DS);DP.append(dp)
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st))

    # Steiner pair orbit fibers and quotient.
    seen=set();orbits=[]
    for p in itertools.combinations(range(120),2):
        if p in seen:continue
        O={p};seen.add(p);D=deque([p])
        while D:
            a=D.popleft()
            for op in SP:
                b=tuple(sorted((op[a[0]],op[a[1]])))
                if b not in O:O.add(b);seen.add(b);D.append(b)
        orbits.append(sorted(O))
    R1,R2,R3,R4=sorted(orbits,key=len);assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=[sorted(c) for c in nx.connected_components(FG)];assert len(fibers)==40 and all(len(F)==3 for F in fibers)

    # One exact maximum cut and its PSp orbit (Pass4867/4946 seed).
    base=0;D0=DS[base];J0=G.subgraph(D0);A0,B0=nx.algorithms.bipartite.sets(J0);A0=sorted(A0);B0=set(B0)
    columns=[]
    for a in A0:
        miss=[b for b in B0 if not G.has_edge(a,b)];assert len(miss)==1;columns.append((a,miss[0]))
    N=sorted(H36.neighbors(base));F=sorted(set(range(36))-{base}-set(N))
    def pattern(S):return tuple((1 if a in S else 0)+(2 if b in S else 0) for a,b in columns)
    duad={j:tuple(i for i,z in enumerate(pattern(DS[j]&D0)) if z==3) for j in F}
    triad={j:tuple(i for i,z in enumerate(pattern(DS[j]&D0)) if z==1) for j in N}
    d2v={d:v for v,d in duad.items()};t2v={t:v for v,t in triad.items()}
    duads=list(itertools.combinations(range(6),2));triads6=list(itertools.combinations(range(6),3));di6={d:i for i,d in enumerate(duads)}
    cycle_edges=((0,1),(1,2),(2,3),(3,4),(4,5),(0,5));dmask=sum(1<<di6[tuple(sorted(e))] for e in cycle_edges);tmask=0xb8ecb
    seed=set()
    for i,d in enumerate(duads):
        if dmask>>i&1:seed.add(d2v[d])
    for i,t in enumerate(triads6):
        if tmask>>i&1:seed.add(t2v[t])
    seed=canon_cut(seed);assert nx.cut_size(H36,seed,set(range(36))-set(seed))==216
    maxcuts={seed};D=deque([seed])
    while D:
        C=D.popleft()
        for p in DP:
            Zc=canon_cut(p[i] for i in C)
            if Zc not in maxcuts:maxcuts.add(Zc);D.append(Zc)
    assert len(maxcuts)==120;maxcuts=sorted(maxcuts,key=lambda C:tuple(sorted(C)))

    B=np.zeros((120,120),dtype=np.int8)
    for i,C in enumerate(maxcuts):
        for j,t in enumerate(st):
            n=sum(v in C for v in t);B[i,j]=int(n in (1,2))
    rg={};cg={}
    for i in range(120):rg.setdefault(bytes(B[i].tolist()),[]).append(i)
    for j in range(120):cg.setdefault(bytes(B[:,j].tolist()),[]).append(j)
    assert len(rg)==len(cg)==40 and set(map(len,rg.values()))==set(map(len,cg.values()))=={3}
    assert {frozenset(v) for v in cg.values()}=={frozenset(F) for F in fibers}
    rgs=list(rg.values());cgs=list(cg.values())
    split=np.array([[B[r[0],c[0]] for c in cgs] for r in rgs],dtype=np.int8)
    Z=1-split
    assert set(map(int,Z.sum(1)))=={4} and set(map(int,Z.sum(0)))=={4}

    # Collinearity graphs induced by common incidence.
    Grow=nx.Graph();Grow.add_nodes_from(range(40));Gcol=nx.Graph();Gcol.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if any(Z[a,j] and Z[b,j] for j in range(40)):Grow.add_edge(a,b)
        if any(Z[i,a] and Z[i,b] for i in range(40)):Gcol.add_edge(a,b)

    # Standard W33 point graph and line-intersection graph.
    wpts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(wpts[a])@J@np.array(wpts[b]))%3==0:W.add_edge(a,b)
    Wlines=[frozenset(c) for c in nx.find_cliques(W) if len(c)==4];assert len(Wlines)==40
    L=nx.Graph();L.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if Wlines[i]&Wlines[j]:L.add_edge(i,j)

    assert nx.is_isomorphic(Grow,W) and not nx.is_isomorphic(Grow,L)
    assert nx.is_isomorphic(Gcol,L) and not nx.is_isomorphic(Gcol,W)

    # Incidence Gram spectra follow immediately.
    evals=np.linalg.eigvalsh(Z@Z.T)
    rounded=Counter(int(round(x)) for x in evals)
    assert rounded==Counter({0:15,6:24,16:1})
    assert np.linalg.matrix_rank(Z)==25

    out={
      'pass':4955,
      'original_shells':{'maximum_cuts':120,'Steiner_triangles':120},
      'triple_collapses':{'maximum_cut_identical_profile_classes':[40,3],'Steiner_fibers':[40,3]},
      'quotient_non_splitting_matrix':{'shape':[40,40],'row_weight':4,'column_weight':4,'rank_Q':25,'gram_spectrum':{'16':1,'6':24,'0':15}},
      'row_side':{'source':'maximum-cut triples','identified_as':'points of standard W(3,3)','collinearity_graph':'W(3,3)'},
      'column_side':{'source':'Steiner three-fibers','identified_as':'lines of standard W(3,3)','collinearity_graph':'line-intersection graph = Q(4,3)'},
      'incidence':'Z is literal W(3,3) point-line incidence after the two 3-to-1 collapses',
      'correction_to_Pass4946':{'maximum_cut_triples':'points, not line classes','Steiner_fibers':'lines, not a second W33 point copy'},
      'theorem':'The 120 maximum cuts are a threefold refinement of the forty W(3,3) points, while the 120 Steiner triangles are a threefold refinement of the forty W(3,3) lines. Their quotient non-splitting relation is exactly point-line incidence. The row graph is W(3,3); the column graph is its nonisomorphic odd-q dual Q(4,3).',
      'boundary':'The original 120-element G-sets remain inequivalent. The 40x40 incidence bridge appears only after the canonical identical-profile triple collapses.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
