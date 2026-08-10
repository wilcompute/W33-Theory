#!/usr/bin/env python3
"""Pass 4719 (outside box) — the S3 regular closure is a new 270 graph.

The selected135 three-cover has full S3 monodromy.  Form its regular six-sheet
(Galois) voltage cover on 45*6=270 vertices.  The parity of the S3 connection is
gauge-equivalent to the all-odd signing, so the regular closure is explicitly
the Kronecker/bipartite double cover of selected135.  It is therefore NOT the
270-vertex cold/base selected270 router: the former is bipartite, the latter is
not.  This freezes the tempting 270=270 identification closed while retaining a
canonical S3-deck graph.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,deque
from pathlib import Path
import networkx as nx
import numpy as np
from w33_pass4716_selected270_bundle_connection import build_bundle,compose,invperm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4719_S3_REGULAR_CLOSURE_REGEN.json'

def parity(p):return sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))&1

def spectrum(G):
    v=np.linalg.eigvalsh(nx.to_numpy_array(G,dtype=float));out=[]
    for z in v:
        if not out or abs(z-out[-1][0])>1e-7:out.append([float(z),1])
        else:out[-1][1]+=1
    return out

def main():
    X=build_bundle();B=X['G45'];sig=X['sig'];S3=list(itertools.permutations(range(3)));si={g:i for i,g in enumerate(S3)}
    # Three-cover itself.
    C=nx.Graph();C.add_nodes_from(range(45*3))
    for p,q in B.edges():
        s=sig[(p,q)]
        for i in range(3):C.add_edge(3*p+i,3*q+s[i])
    assert len(C)==135 and C.number_of_edges()==810 and set(dict(C.degree()).values())=={12} and nx.is_connected(C)

    # Regular S3 cover.
    R=nx.Graph();R.add_nodes_from(range(45*6))
    for p,q in B.edges():
        s=sig[(p,q)]
        for gi,g in enumerate(S3):R.add_edge(6*p+gi,6*q+si[compose(s,g)])
    assert len(R)==270 and R.number_of_edges()==1620 and set(dict(R.degree()).values())=={12} and nx.is_connected(R) and nx.is_bipartite(R)

    # Solve parity gauge h_q = 1 + sign(sigma_pq) + h_p, making every gauged
    # edge voltage odd.
    hp={0:0};Q=deque([0])
    while Q:
        p=Q.popleft()
        for q in B[p]:
            req=1^parity(sig[(p,q)])^hp[p]
            if q in hp:assert hp[q]==req
            else:hp[q]=req;Q.append(q)
    assert Counter(hp.values())==Counter({0:41,1:4})

    # Explicit isomorphism R -> bipartite double of C:
    # (p,g) |-> (p,g(0), sign(g)+h_p).
    D=nx.Graph();D.add_nodes_from(range(270))
    def did(p,i,e):return 6*p+2*i+e
    for u,v in C.edges():
        p,i=divmod(u,3);q,j=divmod(v,3)
        D.add_edge(did(p,i,0),did(q,j,1));D.add_edge(did(p,i,1),did(q,j,0))
    phi={6*p+gi:did(p,g[0],parity(g)^hp[p]) for p in range(45) for gi,g in enumerate(S3)}
    assert len(set(phi.values()))==270
    assert {tuple(sorted((phi[u],phi[v]))) for u,v in R.edges()}=={tuple(sorted(e)) for e in D.edges()}

    sr=spectrum(R)
    target=[(-12,1),(-6,30),(-3,44),(0,120),(3,44),(6,30),(12,1)]
    assert len(sr)==7 and all(abs(sr[i][0]-target[i][0])<1e-6 and sr[i][1]==target[i][1] for i in range(7))

    # Cold/base selected270 graph from Pass4716 is a different 270-vertex graph.
    K=nx.Graph();K.add_nodes_from(range(270));K.add_edges_from(X['cold']);assert K.number_of_edges()==1620 and not nx.is_bipartite(K)
    sk=spectrum(K);roots=[(-6,6),(-4,60),(1-math.sqrt(13),20),(-1,64),(2,84),(1+math.sqrt(13),20),(8,15),(12,1)]
    assert len(sk)==8 and all(abs(sk[i][0]-roots[i][0])<1e-6 and sk[i][1]==roots[i][1] for i in range(8))

    out={'pass':4719,
      'monodromy':'S3','regular_closure':{'vertices':270,'edges':1620,'degree':12,'connected':True,'deck_group':'S3','bipartite':True,'parity_gauge':{'0_packets':41,'1_packets':4},'identification':'Kronecker/bipartite double cover of selected135','spectrum':{'12':1,'6':30,'3':44,'0':120,'-3':44,'-6':30,'-12':1}},
      'selected270_base_nonidentification':{'vertices':270,'edges':1620,'bipartite':False,'spectrum':{'12':1,'8':15,'1+sqrt(13)':20,'2':84,'-1':64,'1-sqrt(13)':20,'-4':60,'-6':6}},
      'theorem':'The S3 connection of selected135 has a canonical connected six-sheet regular closure with deck group S3. A parity gauge makes every voltage odd, giving an explicit isomorphism to the bipartite double cover of selected135. Despite also having 270 vertices and 1620 edges, it is not the selected270 base router.',
      'boundary':'Exact finite voltage-cover theorem and explicit count-coincidence obstruction; no physical doubling is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
