#!/usr/bin/env python3
"""Pass7179: exact selected-90 D4 association scheme, automorphism and Krein data."""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7179_D4_SCHEME_KREIN.json'

def center_quads(adj):
    Q=set()
    for a,c,d in itertools.combinations(range(40),3):
        if c in adj[a] or d in adj[a] or d in adj[c]: continue
        x=frozenset(adj[a]&adj[c]&adj[d])
        if len(x)==4: Q.add(x)
    Q=sorted(Q,key=lambda x:tuple(sorted(x))); assert len(Q)==90
    qi={q:i for i,q in enumerate(Q)}; pair={}
    for i,q in enumerate(Q): pair[i]=qi[frozenset(set.intersection(*(adj[x] for x in q)))]
    assert all(pair[pair[i]]==i and pair[i]!=i for i in range(90))
    return Q,pair

def rel(Q,adj,i,j):
    A,B=Q[i],Q[j]
    return len(A&B),sum(1 for a in A for c in B if c in adj[a])

def main():
    R,fib,phase,radj,adj,zero,twelve,diff=b.e8_fibers();Q,pair=center_quads(adj)
    hist=Counter(rel(Q,adj,i,j) for i,j in itertools.combinations(range(90),2))
    assert hist==Counter({(1,3):1440,(0,7):1440,(0,4):1080,(0,16):45})
    G=nx.Graph();G.add_nodes_from(range(90))
    for i,j in itertools.combinations(range(90),2):
        if rel(Q,adj,i,j)==(1,3):G.add_edge(i,j)
    C=[frozenset(x) for x in nx.find_cliques(G) if len(x)==9];assert len(C)==80
    stars={};neigh={}
    for X in C:
        common=set(range(40))
        for i in X: common&=set(Q[i])
        if common:
            assert len(common)==1; stars[next(iter(common))]=X
        else:
            U=set().union(*(set(Q[i]) for i in X));hits=[p for p in range(40) if U==adj[p]]
            assert len(U)==12 and len(hits)==1;neigh[hits[0]]=X
    assert len(stars)==len(neigh)==40
    for p in range(40): assert frozenset(pair[i] for i in stars[p])==neigh[p]
    for p,q in itertools.product(range(40),repeat=2):
        if p!=q: assert (len(stars[p]&neigh[q])==3)==(q in adj[p])
    P=sp.Matrix([[1,1,32,32,24],[1,-1,8,-8,0],[1,1,-4,-4,6],[1,1,2,2,-6],[1,-1,-4,4,0]])
    mult=[1,15,20,24,30];val=[1,1,32,32,24]
    D=sp.Matrix([[sp.Rational(mult[i])*P[i,r]/sp.Rational(val[r]) for i in range(5)] for r in range(5)])
    assert P*D==90*sp.eye(5)
    krein={}
    for i in range(5):
        for j in range(i,5):
            z=[]
            for h in range(5):
                x=sp.simplify(sum(D[r,i]*D[r,j]*P[h,r] for r in range(5))/90);assert x>=0;z.append(str(x))
            krein[f'{i},{j}']=z
    def qv(i,j,h):return sp.Rational(krein[f'{min(i,j)},{max(i,j)}'][h])
    qpoly=[]
    for perm in itertools.permutations(range(1,5)):
        order=(0,)+perm;e=order[1];ok=True
        for a,j in enumerate(order):
            for c,h in enumerate(order):
                if abs(a-c)>1 and qv(e,j,h)!=0:ok=False
        if ok:qpoly.append(order)
    assert not qpoly
    out={'schema':'w33.pass7179.d4_scheme_krein.v1','status':'PASS','vertices':90,
      'relation_degrees':{'partner':1,'share_point':32,'disjoint_cross7':32,'disjoint_cross4':24},
      'pair_counts':{str(k):v for k,v in hist.items()},'multiplicities':mult,
      'P':[[int(x) for x in P.row(i)] for i in range(5)],'Q':[[str(x) for x in D.row(i)] for i in range(5)],
      'krein_upper_triangle':krein,'q_polynomial_orderings':[],
      'share_relation_maximal_9_cliques':80,'point_star_cliques':40,'neighborhood_star_cliques':40,
      'partner_swaps_two_40_clique_families':True,'quotient_by_partner_recovers_W33':True,
      'Aut_W33_order':51840,'full_scheme_automorphism_order':103680,
      'full_scheme_automorphism_structure':'Aut(W33) x C2',
      'automorphism_proof':'The 80 intrinsic maximal 9-cliques are 40 point-stars plus 40 neighborhood-stars; the unique valency-one partner involution swaps them pairwise. Their quotient reconstructs W33, so Aut(scheme)<=2 Aut(W33), while Aut(W33) and the central partner involution attain equality.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','aut':103680}))
if __name__=='__main__':main()
