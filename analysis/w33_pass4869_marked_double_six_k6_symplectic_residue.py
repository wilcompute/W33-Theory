#!/usr/bin/env python3
"""Pass4869 — marked double-six residue as an exact K6 subset-shell symplectic chart.

Mark one of the 36 double-sixes. Its twelve lines canonically form six opposite
columns in K6,6 minus a perfect matching. The other 35 double-sixes then acquire
literal subset labels of that six-set:

  * the 15 non-neighbors are the 15 duads (two complete columns);
  * the 20 neighbors are the 20 triads (one chosen line in each column, 3+3).

The induced graph is recovered by one nondegenerate alternating form on F2^6:
B(x,y)=x.y + wt(x)wt(y) (mod 2), restricted to weights 2 and 3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np,networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS4869_MARKED_DOUBLE_SIX_K6_SYMPLECTIC_RESIDUE.json"

def Q(x):
    b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b
    return (a*c+d*e+f+f*g+g)&1

def rref2(M):
    A=np.array(M,dtype=np.uint8);r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
    return r

def main()->int:
    qp=[x for x in range(1,64) if Q(x)==0]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        J=G.subgraph(A|B)
        if len(A|B)==12 and J.number_of_edges()==30 and set(dict(J.degree()).values())=={5} and nx.is_bipartite(J):
            DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda S:tuple(sorted(S)));assert len(DS)==36
    H=nx.Graph();H.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H.add_edge(i,j)
    assert H.number_of_edges()==360 and set(dict(H.degree()).values())=={20}

    base=0;D0=DS[base];J0=G.subgraph(D0)
    A0,B0=nx.algorithms.bipartite.sets(J0);A0=sorted(A0);B0=set(B0)
    columns=[]
    for a in A0:
        miss=[b for b in B0 if not G.has_edge(a,b)]
        assert len(miss)==1
        columns.append((a,miss[0]))
    assert len(columns)==6 and len({b for _,b in columns})==6

    N=sorted(H.neighbors(base));F=sorted(set(range(36))-{base}-set(N))
    assert (len(N),len(F))==(20,15)
    def pattern(S):
        return tuple((1 if a in S else 0)+(2 if b in S else 0) for a,b in columns)
    duad={};triad={}
    for j in F:
        p=pattern(DS[j]&D0)
        assert Counter(p)==Counter({0:4,3:2})
        duad[j]=tuple(i for i,z in enumerate(p) if z==3)
    for j in N:
        p=pattern(DS[j]&D0)
        assert Counter(p)==Counter({1:3,2:3})
        triad[j]=tuple(i for i,z in enumerate(p) if z==1)
    assert set(duad.values())==set(itertools.combinations(range(6),2))
    assert set(triad.values())==set(itertools.combinations(range(6),3))

    for i,j in itertools.combinations(F,2):
        assert H.has_edge(i,j)==(len(set(duad[i])&set(duad[j]))==1)
    for i,j in itertools.combinations(N,2):
        r=len(set(triad[i])&set(triad[j]))
        assert H.has_edge(i,j)==(r in (0,2))
    for i in F:
        for j in N:
            assert H.has_edge(i,j)==(len(set(duad[i])&set(triad[j]))==1)

    BF=(np.eye(6,dtype=np.uint8)+np.ones((6,6),dtype=np.uint8))%2
    assert np.all(np.diag(BF)==0) and np.array_equal(BF,BF.T) and rref2(BF.copy())==6
    vec={}
    for j,s in duad.items():
        x=np.zeros(6,dtype=np.uint8);x[list(s)]=1;vec[j]=x
    for j,s in triad.items():
        x=np.zeros(6,dtype=np.uint8);x[list(s)]=1;vec[j]=x
    R=F+N
    for i,j in itertools.combinations(R,2):
        assert H.has_edge(i,j)==bool(int(vec[i]@BF@vec[j])&1)

    labels=[("d",s) for s in itertools.combinations(range(6),2)]+[("t",s) for s in itertools.combinations(range(6),3)]
    M=nx.Graph();M.add_nodes_from(labels)
    def bv(s):
        x=np.zeros(6,dtype=np.uint8);x[list(s)]=1;return x
    for a,b in itertools.combinations(labels,2):
        if int(bv(a[1])@BF@bv(b[1]))&1:M.add_edge(a,b)
    assert nx.is_isomorphic(H.subgraph(R),M)
    aut_count=sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(M,M).isomorphisms_iter())
    assert aut_count==1440

    labs={x:i for i,x in enumerate(labels)};perms=set()
    for s6 in itertools.permutations(range(6)):
        for flip in (0,1):
            p=[]
            for typ,S in labels:
                T=tuple(sorted(s6[i] for i in S))
                if flip and typ=="t":T=tuple(i for i in range(6) if i not in T)
                p.append(labs[(typ,T)])
            perms.add(tuple(p))
    assert len(perms)==1440

    HF=H.subgraph(F);HN=H.subgraph(N)
    assert set(dict(HF.degree()).values())=={8}
    assert set(dict(HN.degree()).values())=={10}

    out={
      "pass":4869,
      "marked_double_six":{"columns":6,"residue_vertices":35,"neighbor_orbit":20,"nonneighbor_orbit":15},
      "canonical_labels":{
        "15_non_neighbors":"duads C(6,2): intersection with the marked double-six is two complete opposite columns",
        "20_neighbors":"triads C(6,3): intersection takes exactly one line from each column, with a 3+3 side split"},
      "adjacency_laws":{
        "duad_duad":"adjacent iff intersection size 1 (T(6)=L(K6))",
        "triad_triad":"adjacent iff intersection size 0 or 2",
        "duad_triad":"adjacent iff intersection size 1",
        "unified":"adjacent iff B(x,y)=1 for B(x,y)=x.y+wt(x)wt(y) mod 2"},
      "symplectic_chart":{"matrix":"I_6+J_6 over F2","alternating":True,"nondegenerate_rank":6,
        "ambient":"35-vertex weight-{2,3} shell inside F2^6 under a nondegenerate symplectic form"},
      "residue_automorphism_group":{"order":1440,"explicit_model":"S6 x C2","S6":"permutes six marked double-six columns",
        "C2":"fixes duads and complements each triad","full_by_exhaustive_graph_automorphism_count":True},
      "repo_bridge":{"BT632_duad_carrier":"The formerly model-level 15 K6-duad carrier is now canonically realized after marking one double-six.",
        "boundary":"The marking is extra data; there is no globally preferred double-six, so this does not canonically label the unmarked 36-carrier."},
      "theorem":"Marking one double-six canonically coordinatizes the other 35 double-sixes by the 15 duads and 20 triads of its six opposite columns. The entire marked residue adjacency is the restriction of the nondegenerate alternating form I+J on F2^6 to weights 2 and 3, and the residue automorphism group is exactly S6 x C2 of order 1440. This upgrades the repo's earlier K6-duad carrier from a model to an incidence-derived chart relative to a marked double-six.",
      "boundary":"Finite marked-residue theorem. The 35-shell is not the whole 63-point W(5,2), and the marked double-six is additional structure."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
