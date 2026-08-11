#!/usr/bin/env python3
"""Pass4940 — exact distance of the Pass4859 covering-radius hard word.

Pass4859 certified d(x,K)>=124 and an automorphism g with g(x)=x+sigma,
which makes the distances from x to the two switching classes equal.  This
producer closes the remaining distance-to-cut subproblem by an exact,
deterministic 36-vertex bitset branch-and-bound.  The lower bound at each node
is the sum of independently unavoidable fixed-to-free mismatches, strengthened
near the root by a greedy packing of edge-disjoint odd signed triangles.  The
search is exhaustive; no external MIP/SAT solver or floating bound is used.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np,networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4940_EXACT_HARDWORD_COVER_DISTANCE.json'
WITNESS_HEX='4743dfaba7bb36874b9fcb5de87ed19c21ff7927d7754391d7d5d134b3bb04eefeccacde1ec769b98b7dffcf8'
WITNESS_AUT=(23,31,3,25,18,11,30,6,24,32,10,19,26,17,12,5,13,28,4,15,33,2,8,0,35,21,29,27,16,14,34,20,9,1,7,22)

def Q(x):
    b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1

def main()->int:
    qp=[x for x in range(1,64) if Q(x)==0]
    P=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,T in enumerate(P) if x in T) for x in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        J=G.subgraph(A|B)
        if J.number_of_edges()==30 and set(dict(J.degree()).values())=={5} and nx.is_bipartite(J):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda S:tuple(sorted(S)));assert len(DS)==36
    H=nx.Graph();H.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H.add_edge(i,j)
    E=sorted(tuple(sorted(e)) for e in H.edges());ei={e:i for i,e in enumerate(E)};assert len(E)==360
    xmask=int(WITNESS_HEX,16);x=[(xmask>>i)&1 for i in range(360)]

    # Reconstruct the E6 signing and recheck the exact Pass4859 twist certificate.
    C=np.eye(6,dtype=int)*2
    for a,b in ((0,1),(1,2),(2,3),(3,4),(2,5)):C[a,b]=C[b,a]=-1
    def ref(v,i):
        v=np.array(v,dtype=int);m=int(v@C[:,i]);w=v.copy();w[i]-=m;return tuple(map(int,w))
    roots={(1,0,0,0,0,0)};D=list(roots)
    while D:
        v=D.pop()
        for i in range(6):
            w=ref(v,i)
            if w not in roots:roots.add(w);D.append(w)
    pos=sorted(v for v in roots if all(z>=0 for z in v));assert len(pos)==36
    ER=nx.Graph();ER.add_nodes_from(range(36));ip={}
    for i,j in itertools.combinations(range(36),2):
        z=int(np.array(pos[i])@C@np.array(pos[j]));ip[(i,j)]=z
        if abs(z)==1:ER.add_edge(i,j)
    iso=next(nx.algorithms.isomorphism.GraphMatcher(H,ER).isomorphisms_iter())
    sigma=[0]*360
    for e,(a,b) in enumerate(E):
        i,j=sorted((iso[a],iso[b]));sigma[e]=int(ip[(i,j)]<0)
    ep=[ei[tuple(sorted((WITNESS_AUT[a],WITNESS_AUT[b])))] for a,b in E];gx=[0]*360
    for i,j in enumerate(ep):gx[j]=x[i]
    assert gx==[a^b for a,b in zip(x,sigma)]

    # Bitset exact branch-and-bound for min_y wt(x + delta y).
    n=36;ALL=(1<<n)-1;adj=[0]*n;n0=[0]*n;n1=[0]*n
    for e,(u,v) in enumerate(E):
        adj[u]|=1<<v;adj[v]|=1<<u
        target=n1 if x[e] else n0;target[u]|=1<<v;target[v]|=1<<u
    odd=[]
    for a,b,c in itertools.combinations(range(n),3):
        if H.has_edge(a,b) and H.has_edge(a,c) and H.has_edge(b,c):
            es=(ei[tuple(sorted((a,b)))],ei[tuple(sorted((a,c)))],ei[tuple(sorted((b,c)))])
            if x[es[0]]^x[es[1]]^x[es[2]]:
                odd.append(((1<<a)|(1<<b)|(1<<c),(1<<es[0])|(1<<es[1])|(1<<es[2])))
    assert len(odd)==700
    def costs(u,fixed,ymask):
        y1=fixed&ymask;y0=fixed&~ymask
        return ((n0[u]&y1).bit_count()+(n1[u]&y0).bit_count(),
                (n0[u]&y0).bit_count()+(n1[u]&y1).bit_count())
    # A deterministic feasible cut supplies the initial upper bound 134.
    best=134;bestmask=sum(1<<i for i in (6,7,8,9,10,11,13,14,16,17,18,19,20,21,23,26,30,35))
    nodes=prunes=0;stack=[(1,0,0,35)] # fix y_0=0, quotienting cut/complement symmetry
    while stack:
        fixed,ymask,cur,remain=stack.pop();nodes+=1
        if remain==0:
            if cur<best:best=cur;bestmask=ymask
            continue
        U=ALL^fixed;lb=cur;choice=-1;score=(-1,-1);cc=(0,0);um=U
        while um:
            bit=um&-um;u=bit.bit_length()-1;um^=bit;c0,c1=costs(u,fixed,ymask);lb+=min(c0,c1)
            sc=((adj[u]&fixed).bit_count(),abs(c0-c1))
            if sc>score:score=sc;choice=u;cc=(c0,c1)
        if lb>=best:prunes+=1;continue
        # Fully-unassigned odd triangles use only free-free edges, hence can be
        # added without double-counting the fixed-free unary bound.
        if remain>=22:
            used=0;pack=0
            for vm,em in odd:
                if not(vm&fixed) and not(em&used):used|=em;pack+=1
            if lb+pack>=best:prunes+=1;continue
        c0,c1=cc;bit=1<<choice;fixed2=fixed|bit;vals=(0,1) if c0<=c1 else (1,0)
        for val in reversed(vals):
            stack.append((fixed2,ymask|bit if val else ymask,cur+(c1 if val else c0),remain-1))
    assert best==134
    assignment=[(bestmask>>i)&1 for i in range(36)]
    cut=[assignment[u]^assignment[v] for u,v in E];assert sum(a^b for a,b in zip(x,cut))==best
    out={'pass':4940,'code':'K=[360,36,20]_2','witness_hex':WITNESS_HEX,
      'exact_search':{'method':'deterministic bitset branch-and-bound','status':'EXHAUSTED','Boolean_vertex_variables':36,
        'symmetry_fix':'y0=0','odd_signed_triangles':len(odd),'search_nodes':nodes,'pruned_nodes':prunes,
        'objective_distance':best},
      'exact_cut_representative_vertices':[i for i,b in enumerate(assignment) if b],
      'twist_cross_certificate':{'g_x_equals_x_plus_sigma':True,'therefore_two_switching_class_distances_equal':True},
      'covering_radius_update':{'certified_lower_bound':best,'previous_lower_bound':124,'upper_bound':179,'exact_radius_closed':False},
      'theorem':'The Pass4859 hard received word has exact distance 134 from the ordinary cut class by exhaustive integer branch-and-bound. Its certified twist automorphism sends x to x+sigma, so the switched class has the same distance. Hence d(x,K)=134 and the covering-radius lower bound rises from 124 to 134.',
      'boundary':'This closes the distance of one hard coset exactly, not the global covering radius. The current rigorous interval is 134<=rho(K)<=179.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
