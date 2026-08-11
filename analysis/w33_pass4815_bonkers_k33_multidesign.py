#!/usr/bin/env python3
"""Pass 4815 bonkers — the complete 360 K3,3 homology shell is a multidesign.

Starting only from the 27-line GQ(4,2) intersection graph, enumerate every
induced K3,3.  Pass4809 proves these are exactly the projective minimum nonlocal
logical classes.  This producer records their simultaneous incidence with:
  * 27 line/fiber vertices;
  * 45 GQ points (graph edges);
  * 270 physical triangle coordinates.

It also proves two completion properties: every independent triple of the
27-line graph is one bipartition side of a unique K3,3, and every induced K1,3
is contained in a unique K3,3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4815_K33_MULTIDESIGN.json'

def Qm(v):
    x1,x2,x3,x4,x5,x6=v
    return (x1*x2+x3*x4+x5+x5*x6+x6)&1

def bits(x):return tuple((x>>i)&1 for i in range(6))
def geom():
    qp=[x for x in range(1,64) if Qm(bits(x))==0]
    pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp})
    lines=[tuple(i for i,P in enumerate(pts) if p in P) for p in qp]
    G=nx.Graph();G.add_nodes_from(range(27))
    edgepoint={}
    for i,j in itertools.combinations(range(27),2):
        z=set(lines[i])&set(lines[j])
        if z:
            assert len(z)==1;G.add_edge(i,j);edgepoint[(i,j)]=next(iter(z))
    tris=sorted({tuple(sorted(t)) for L in lines for t in itertools.combinations(L,3)});assert len(tris)==270
    tidx={t:i for i,t in enumerate(tris)}
    return lines,G,edgepoint,tidx

def k33s(G):
    out=[]
    for S in itertools.combinations(range(27),6):
        H=G.subgraph(S)
        if H.number_of_edges()!=9 or not nx.is_bipartite(H):continue
        if set(dict(H.degree()).values())!={3}:continue
        A,B=nx.algorithms.bipartite.sets(H);assert len(A)==len(B)==3
        out.append((frozenset(S),tuple(sorted((tuple(sorted(A)),tuple(sorted(B)))))))
    assert len(out)==360
    return out

def main():
    lines,G,edgepoint,tidx=geom();shell=k33s(G)
    rline=Counter();rpoint=Counter();rtri=Counter();sides=Counter();stars=Counter();adjpair=Counter();nonpair=Counter();p3=Counter()
    for S,(A,B) in shell:
        rline.update(S);sides[A]+=1;sides[B]+=1
        for u,v in itertools.combinations(sorted(S),2):
            (adjpair if G.has_edge(u,v) else nonpair)[(u,v)]+=1
        ps=set()
        for u in A:
            for v in B:
                e=tuple(sorted((u,v)));p=edgepoint[e];ps.add(p);rpoint[p]+=1
        assert len(ps)==9
        # one physical triangle coordinate per active line: its three cross-part intersection points
        for u in S:
            opp=B if u in A else A
            t=tuple(sorted(edgepoint[tuple(sorted((u,v)))] for v in opp));assert t in tidx;rtri[tidx[t]]+=1
        # six induced stars and eighteen P3 triples per K3,3
        for c in S:
            leaves=tuple(sorted(v for v in S if G.has_edge(c,v)));assert len(leaves)==3;stars[(c,leaves)]+=1
        for c in S:
            nbr=[v for v in S if G.has_edge(c,v)]
            for a,b in itertools.combinations(nbr,2):p3[tuple(sorted((a,c,b)))]+=1
    assert Counter(rline.values())==Counter({80:27})
    assert Counter(rpoint.values())==Counter({72:45})
    assert Counter(rtri.values())==Counter({8:270})
    assert Counter(adjpair.values())==Counter({24:135})
    assert Counter(nonpair.values())==Counter({10:216})
    # Ambient independent triples: exactly the 720 sides, each once.
    indep=[T for T in itertools.combinations(range(27),3) if G.subgraph(T).number_of_edges()==0]
    assert len(indep)==720 and set(indep)==set(sides) and set(sides.values())=={1}
    # Ambient induced P3 count 1080, each appears in six K3,3.
    P3=[]
    for T in itertools.combinations(range(27),3):
        H=G.subgraph(T)
        if H.number_of_edges()==2:P3.append(T)
    assert len(P3)==1080 and set(P3)==set(p3) and set(p3.values())=={6}
    # Every induced K1,3 occurs once.
    allstars=[]
    for c in range(27):
        N=list(G.neighbors(c))
        for L in itertools.combinations(N,3):
            if G.subgraph(L).number_of_edges()==0:allstars.append((c,tuple(sorted(L))))
    assert len(allstars)==2160 and set(allstars)==set(stars) and set(stars.values())=={1}
    out={'pass':4815,'projective_K33_minima':360,
      'line_fibers':{'points':27,'block_size':6,'replication':80},
      'GQ_points':{'points':45,'block_size':9,'replication':72},
      'physical_triangles':{'points':270,'block_size':6,'replication':8},
      'adjacent_line_pair_replication':24,'nonadjacent_line_pair_replication':10,
      'independent_triples':720,'K33_sides_per_independent_triple':1,
      'induced_P3_triples':1080,'K33_per_induced_P3':6,
      'induced_K13_stars':2160,'K33_per_induced_K13':1,
      'theorem':'The complete 360-class K3,3 homology shell is simultaneously regular on the 27 line fibers, 45 GQ points, and 270 physical triangle coordinates, with replications 80,72,8. Every independent triple is a unique K3,3 side and every induced K1,3 has a unique K3,3 completion.',
      'boundary':'These are exact incidence/completion statements in the GQ(4,2) line graph; no external design name is inferred from parameters alone.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
