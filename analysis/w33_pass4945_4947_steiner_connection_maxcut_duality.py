#!/usr/bin/env python3
"""Passes 4945--4947 — three outside-box probes of the Steiner three-cover.

4945: treat the canonical R2 perfect matchings over W33 nonedges as an S3
      connection and compute its gauge-invariant holonomy.
4946: cross the 120 maximum cuts with the 120 Steiner triangles; although
      Pass4877 forbids a 120<->120 equivariant bijection, their intrinsic
      triples recover the 40-line x 40-point incidence matrix of W33.
4947: classify triangle curvature of the S3 connection and identify it with
      acentric versus centric W33 triads.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT45=ROOT/'data/PART_W33_PASS4945_STEINER_NONEDGE_S3_HOLONOMY.json'
OUT46=ROOT/'data/PART_W33_PASS4946_MAXCUT_STEINER_DUAL_W33_INCIDENCE.json'
OUT47=ROOT/'data/PART_W33_PASS4947_W33_TRIAD_CURVATURE.json'

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

def compose_map(p,q):return tuple(q[p[i]] for i in range(len(p)))
def invperm(p):return tuple(p.index(i) for i in range(len(p)))
def canon_cut(S,n=36):
    S=frozenset(S);T=frozenset(set(range(n))-set(S));return min((S,T),key=lambda z:tuple(sorted(z)))

def main()->int:
    # Reconstruct the standard GQ(4,2), 36 double-sixes, 120 Steiner triangles, and PSp generators.
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
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36
    di={S:i for i,S in enumerate(DS)}
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
    # Pair orbit relations.
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
    fi={x:i for i,F in enumerate(fibers) for x in F};pos={x:i for F in fibers for i,x in enumerate(F)}
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for a,b in R3:Q.add_edge(fi[a],fi[b])
    assert Q.number_of_edges()==240 and set(dict(Q.degree()).values())=={12}
    r2=set(R2);Qbar=nx.complement(Q);Qbar.remove_edges_from(nx.selfloop_edges(Qbar));assert Qbar.number_of_edges()==540
    def edgeperm(u,v):
        p=[None]*3
        for x in fibers[u]:
            ys=[y for y in fibers[v] if tuple(sorted((x,y))) in r2];assert len(ys)==1;p[pos[x]]=pos[ys[0]]
        return tuple(p)
    transports={}
    for u,v in Qbar.edges():
        p=edgeperm(u,v);transports[(u,v)]=p;transports[(v,u)]=invperm(p)
    # 4945: fundamental-cycle holonomy from a BFS gauge.
    parent={0:None};tree_edges=[]
    for u,v in nx.bfs_edges(Qbar,0):parent[v]=u;tree_edges.append(tuple(sorted((u,v))))
    tree_edges=set(tree_edges);root_to={0:(0,1,2)}
    for v in nx.bfs_tree(Qbar,0):
        if v==0:continue
        u=parent[v];root_to[v]=compose_map(root_to[u],transports[(u,v)])
    hol=[]
    for u,v in Qbar.edges():
        if tuple(sorted((u,v))) in tree_edges:continue
        loop=compose_map(root_to[u],transports[(u,v)]);loop=compose_map(loop,invperm(root_to[v]));hol.append(loop)
    holset=set(hol);assert len(holset)==6
    # Find a four-cycle carrying order-three holonomy.
    cyc4=None
    for a in Qbar:
        if cyc4:break
        for b in Qbar[a]:
            for c in Qbar[b]:
                if c in (a,b):continue
                for d in Qbar[c]:
                    if d in (a,b,c) or not Qbar.has_edge(d,a):continue
                    p=transports[(a,b)];p=compose_map(p,transports[(b,c)]);p=compose_map(p,transports[(c,d)]);p=compose_map(p,transports[(d,a)])
                    if sum(i==p[i] for i in range(3))==0:cyc4=[a,b,c,d,list(p)];break
                if cyc4:break
            if cyc4:break
    assert cyc4 is not None
    out45={'pass':4945,'base_graph':'complement of W33 on the 40 Steiner fibers','edges':540,
      'connection':'each W33 nonedge carries the intrinsic R2 perfect matching, hence an S3 transport after local fiber labels are chosen',
      'fundamental_cycle_holonomy':{'group_order':6,'group':'S3','all_six_permutations_seen':True,
        'non_tree_cycle_count':len(hol),'order3_four_cycle_witness':cyc4},
      'theorem':'The canonical perfect matchings across W33 nonedges define a genuine non-flat S3 connection on the 40 Steiner fibers. After any local labeling of each three-element fiber, the fundamental-cycle transports generate all of S3. Consequently no global relabeling can trivialize all 540 nonedge matchings, and the connection does not reduce globally to C3 or C2.',
      'boundary':'The edge permutations depend on local labels, but the conjugacy class of the holonomy group and its order are gauge invariant.'}
    OUT45.write_text(json.dumps(out45,indent=2,sort_keys=True)+'\n')

    # 4946: build one exact maximum cut from the Pass4867 marked K6 chart, then exhaust its PSp orbit.
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
            Z=canon_cut(p[i] for i in C)
            if Z not in maxcuts:maxcuts.add(Z);D.append(Z)
    assert len(maxcuts)==120 and all(nx.cut_size(H36,C,set(range(36))-set(C))==216 for C in maxcuts)
    maxcuts=sorted(maxcuts,key=lambda C:tuple(sorted(C)))
    B=np.zeros((120,120),dtype=np.int8)
    for i,C in enumerate(maxcuts):
        for j,t in enumerate(st):
            n=sum(v in C for v in t);B[i,j]=int(n in (1,2))
    assert set(map(int,B.sum(1)))=={108} and set(map(int,B.sum(0)))=={108}
    rg={};cg={}
    for i in range(120):rg.setdefault(bytes(B[i].tolist()),[]).append(i)
    for j in range(120):cg.setdefault(bytes(B[:,j].tolist()),[]).append(j)
    assert len(rg)==len(cg)==40 and set(map(len,rg.values()))==set(map(len,cg.values()))=={3}
    assert {frozenset(v) for v in cg.values()}=={frozenset(F) for F in fibers}
    rgs=list(rg.values());cgs=list(cg.values());Cmat=np.array([[B[r[0],c[0]] for c in cgs] for r in rgs],dtype=np.int8);Z=1-Cmat
    assert set(map(int,Z.sum(1)))=={4} and set(map(int,Z.sum(0)))=={4}
    assert all(int(Z[i]@Z[j]) in (0,1) for i,j in itertools.combinations(range(40),2))
    Pcol=nx.Graph();Pcol.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if any(Z[r,a] and Z[r,b] for r in range(40)):Pcol.add_edge(a,b)
    assert Pcol.number_of_edges()==240 and set(dict(Pcol.degree()).values())=={12}
    assert all(len(set(Pcol[a])&set(Pcol[b]))==2 for a,b in Pcol.edges())
    assert all(len(set(Pcol[a])&set(Pcol[b]))==4 for a,b in itertools.combinations(range(40),2) if not Pcol.has_edge(a,b))
    assert nx.is_isomorphic(Pcol,Q)
    out46={'pass':4946,
      'shells':{'maximum_cuts':120,'Steiner_triangles':120,'Pass4877_equivariant_bijection_exists':False},
      'cross_incidence':{'definition':'B(C,T)=1 iff the maximum cut splits the three double-sixes of Steiner triangle T; zero iff T lies wholly on one side',
        'row_weight':108,'column_weight':108,'identical_row_classes':[40,3],'identical_column_classes':[40,3]},
      'quotient':{'maximum_cut_triples':'40 line classes','Steiner_triples':'the same 40 point fibers from Pass4870',
        'zero_matrix_row_weight':4,'zero_matrix_column_weight':4,
        'meaning':'Z=1-B on the 40x40 quotient is point-line incidence',
        'point_collinearity':'SRG(40,12,2,4)','explicit_isomorphism_to_Pass4870_W33':True},
      'theorem':'Although the 120 maximum cuts and 120 Steiner triangles are inequivalent PGSp G-sets, their cross-incidence has a canonical 3-to-1 collapse on both sides. The 120 maximum cuts form forty triples with identical Steiner-splitting profiles, while the Steiner columns collapse by exactly the classical forty Steiner triads. On the resulting 40x40 quotient, the NON-splitting relation has row and column weight four and is precisely a generalized-quadrangle point-line incidence matrix: two quotient points are collinear iff they share a zero block, and the resulting graph is W(3,3). Thus the two inequivalent 120-shells recover the dual 40-line and 40-point actions of W33 rather than a false 120-to-120 identification.',
      'boundary':'Finite incidence theorem. The quotient identifies GQ point/line actions; it does not restore an equivariant bijection between the original 120-element shells.'}
    OUT46.write_text(json.dumps(out46,indent=2,sort_keys=True)+'\n')

    # 4947: curvature on complement triangles = acentric/centric triad dichotomy.
    curv=Counter();by_centers=Counter();threecycles=0
    for clique in nx.enumerate_all_cliques(Qbar):
        if len(clique)<3:continue
        if len(clique)>3:break
        a,b,c=clique;p=transports[(a,b)];p=compose_map(p,transports[(b,c)]);p=compose_map(p,transports[(c,a)])
        fixed=sum(i==p[i] for i in range(3));typ='identity' if fixed==3 else ('transposition' if fixed==1 else '3cycle')
        centers=len(set(Q[a])&set(Q[b])&set(Q[c]));curv[typ]+=1;by_centers[(typ,centers)]+=1
        if typ=='3cycle':threecycles+=1
    assert curv==Counter({'transposition':2160,'identity':1080}) and threecycles==0
    assert by_centers==Counter({('transposition',2):2160,('identity',0):1080})
    out47={'pass':4947,'W33_independent_triads':3240,
      'curvature':{'flat_identity':1080,'reflection_transposition':2160,'order3':0},
      'geometric_classification':{'acentric_common_neighbors_0':1080,'centric_common_neighbors_2':2160,
        'equivalence':'matching holonomy is identity iff the W33 triad is acentric; it is a transposition iff the triad has two centers'},
      'theorem':'The S3 matching connection detects the intrinsic triad geometry of W33. Among the 3240 triples of pairwise noncollinear W33 points, exactly 1080 have no common neighbor and carry flat identity holonomy; exactly 2160 have two common neighbors and carry reflection holonomy. No complement triangle has order-three curvature. Hence the connection curvature is an exact finite detector of the acentric/centric triad dichotomy.',
      'boundary':'Finite holonomy/triad theorem. The numerical 1080 also occurs elsewhere in the repo (for example the even double-six triangle checks), but no identification with those 1080 objects is claimed here without an explicit equivariant map.'}
    OUT47.write_text(json.dumps(out47,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'4945':out45['fundamental_cycle_holonomy'],'4946':out46['quotient'],'4947':out47['curvature']},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
