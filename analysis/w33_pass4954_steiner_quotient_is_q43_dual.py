#!/usr/bin/env python3
"""Pass4954 — identify the Steiner 40-fiber quotient as Q(4,3), dual to W(3,3).

Pass4870 promoted the 40-fiber quotient to W(3,3) from SRG data plus an intended
isomorphism check.  Pass4947's 0/2 triad-center statistics conflict with the
standard symplectic W(3,3) point graph, whose statistics are 1/4.  This verifier
reconstructs the Steiner quotient from the 36-double-six geometry and compares it
directly with BOTH standard W(3,3) point and line-intersection graphs.

Result: the quotient is not the W(3,3) point graph.  It is exactly the
line-intersection graph of W(3,3), i.e. the point graph of the dual GQ Q(4,3).
"""
from __future__ import annotations
import itertools, json
from collections import Counter, deque
from pathlib import Path
import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4954_STEINER_QUOTIENT_IS_Q43_DUAL.json"


def Q6(v):
    a,c,d,e,f,g=v
    return (a*c+d*e+f+f*g+g)&1

def add2(a,b): return tuple(x^y for x,y in zip(a,b))
def polar(a,b): return Q6(add2(a,b))^Q6(a)^Q6(b)
def comp(p,q): return tuple(p[q[i]] for i in range(len(q)))

def closure(gens,n):
    I=tuple(range(n));S={I};D=deque([I])
    while D:
        a=D.popleft()
        for g in gens:
            z=comp(g,a)
            if z not in S:S.add(z);D.append(z)
    return S

def canon3(v):
    v=np.array(v,dtype=int)%3
    j=next(i for i,x in enumerate(v) if x)
    return tuple((v*pow(int(v[j]),-1,3))%3)

def srg_profile(G):
    adj=Counter();non=Counter()
    for a,b in itertools.combinations(G.nodes(),2):
        c=len(set(G[a])&set(G[b]))
        (adj if G.has_edge(a,b) else non)[c]+=1
    return set(dict(G.degree()).values()),dict(adj),dict(non)

def triad_centers(G):
    out=Counter()
    for t in itertools.combinations(G.nodes(),3):
        if any(G.has_edge(*e) for e in itertools.combinations(t,2)):continue
        c=len(set(G[t[0]])&set(G[t[1]])&set(G[t[2]]))
        out[c]+=1
    return dict(sorted(out.items()))

def spread_exists(G):
    lines=[frozenset(c) for c in nx.find_cliques(G) if len(c)==4]
    assert len(lines)==40
    point_to={p:[i for i,L in enumerate(lines) if p in L] for p in G.nodes()}
    def search(covered):
        if len(covered)==40:return True
        best=None
        for p in G.nodes():
            if p in covered:continue
            cands=[i for i in point_to[p] if not (lines[i]&covered)]
            if not cands:return False
            if best is None or len(cands)<len(best):best=cands
        for i in best:
            if search(covered|lines[i]):return True
        return False
    return search(frozenset())

def main()->int:
    # Reconstruct the Steiner quotient exactly as in Pass4870.
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
    G27=nx.Graph();G27.add_nodes_from(range(27))
    for i,j in itertools.combinations(range(27),2):
        if set(lines[i])&set(lines[j]):G27.add_edge(i,j)
    C6=[frozenset(c) for c in nx.find_cliques(nx.complement(G27)) if len(c)==6]
    DS=set()
    for A,B in itertools.combinations(C6,2):
        if A&B:continue
        H=G27.subgraph(A|B)
        if H.number_of_edges()==30 and set(dict(H.degree()).values())=={5} and nx.is_bipartite(H):DS.add(frozenset(A|B))
    DS=sorted(DS,key=lambda x:tuple(sorted(x)));assert len(DS)==36;di={S:i for i,S in enumerate(DS)}
    H36=nx.Graph();H36.add_nodes_from(range(36))
    for i,j in itertools.combinations(range(36),2):
        if len(DS[i]&DS[j])==6:H36.add_edge(i,j)
    st=sorted(t for t in itertools.combinations(range(36),3)
              if all(H36.has_edge(*e) for e in itertools.combinations(t,2))
              and len(DS[t[0]]&DS[t[1]]&DS[t[2]])==0)
    assert len(st)==120;sti={t:i for i,t in enumerate(st)}
    SP=[]
    for g in gp:
        dp=tuple(di[frozenset(g[x] for x in S)] for S in DS)
        SP.append(tuple(sti[tuple(sorted(dp[i] for i in t))] for t in st))
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
    R1,R2,R3,R4=sorted(orbits,key=len)
    assert list(map(len,(R1,R2,R3,R4)))==[120,1620,2160,3240]
    FG=nx.Graph();FG.add_nodes_from(range(120));FG.add_edges_from(R1)
    fibers=[set(c) for c in nx.connected_components(FG)];assert len(fibers)==40 and all(len(c)==3 for c in fibers)
    fi={x:i for i,c in enumerate(fibers) for x in c}
    SQ=nx.Graph();SQ.add_nodes_from(range(40))
    for a,b in R3:SQ.add_edge(fi[a],fi[b])
    assert srg_profile(SQ)==({12},{2:240},{4:540})

    # Standard symplectic W(3,3) point graph.
    wpts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(wpts[a])@J@np.array(wpts[b]))%3==0:W.add_edge(a,b)
    assert srg_profile(W)==({12},{2:240},{4:540})

    # Its 40 isotropic lines are the maximal K4s; intersecting lines define the dual point graph.
    Wlines=[frozenset(c) for c in nx.find_cliques(W) if len(c)==4]
    assert len(Wlines)==40
    L=nx.Graph();L.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if Wlines[i]&Wlines[j]:L.add_edge(i,j)
    assert srg_profile(L)==({12},{2:240},{4:540})

    sq_is_point=nx.is_isomorphic(SQ,W)
    sq_is_line=nx.is_isomorphic(SQ,L)
    assert not sq_is_point
    assert sq_is_line

    w_triad=triad_centers(W)
    l_triad=triad_centers(L)
    sq_triad=triad_centers(SQ)
    assert w_triad=={1:2880,4:360}
    assert l_triad==sq_triad=={0:1080,2:2160}

    sq_spread=spread_exists(SQ)
    assert sq_spread is False

    out={
      "pass":4954,
      "steiner_quotient":{"vertices":40,"srg":[40,12,2,4],"triad_centers":sq_triad,"spread_exists":sq_spread},
      "standard_W33_point_graph":{"triad_centers":w_triad,"isomorphic_to_steiner_quotient":sq_is_point},
      "standard_W33_line_intersection_graph":{"triad_centers":l_triad,"isomorphic_to_steiner_quotient":sq_is_line},
      "identification":"Steiner 40-fiber quotient = line-intersection graph of W(3,3) = point graph of dual Q(4,3)",
      "corrections":{
        "Pass4870_explicit_isomorphism_to_standard_W33":False,
        "Pass4947_0_2_center_counts":"correct for the Q(4,3) dual quotient, but incorrectly labeled as W(3,3) point-triad geometry",
        "Pass4953_1_4_counts":"correct for the standard W(3,3) point graph; not the Steiner quotient"
      },
      "repo_crosscheck":"Pass2869 already records that W(3,3) and Q(4,3) are the two GQ(3,3) candidates, nonisomorphic at odd q, and that a spread separates them.",
      "theorem":"The Steiner three-fiber quotient is not the standard W(3,3) point graph. It is exactly the intersection graph of the forty W(3,3) lines, hence the point graph of the dual generalized quadrangle Q(4,3). This resolves the apparent 1/4 versus 0/2 triad-center contradiction.",
      "boundary":"Both graphs share SRG(40,12,2,4); parameters alone never identify either graph. The identification here is by explicit graph isomorphism to the standard W33 line-intersection graph, not by SRG parameters."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
