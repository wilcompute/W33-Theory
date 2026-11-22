#!/usr/bin/env python3
"""W33 chordless-four-cycle causal orientation obstruction.

The exact same unoriented K2,2 graph supports inequivalent acyclic
Hasse orientations with different causal interval counts. Therefore
W33 graph adjacency alone cannot determine a Lorentzian causal set.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/"data/toe_20261122_causal_orientation_no_go.json"

def w33():
    pts=[]
    for lead in range(4):
        for tail in itertools.product(range(3),repeat=3-lead):
            pts.append((0,)*lead+(1,)+tail)
    assert len(pts)==40
    def s(a,b):
        return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%3
    E={tuple(sorted((i,j))) for i,j in itertools.combinations(range(40),2)
       if s(pts[i],pts[j])==0}
    assert len(E)==240
    return pts,E

def c4s(E):
    adj=[set() for _ in range(40)]
    for i,j in E:adj[i].add(j);adj[j].add(i)
    count_non=0; cycles=set()
    for a,b in itertools.combinations(range(40),2):
        if (a,b) in E:continue
        count_non+=1
        common=sorted(adj[a]&adj[b])
        assert len(common)==4
        for c,d in itertools.combinations(common,2):
            assert tuple(sorted((c,d))) not in E
            cycles.add(frozenset((a,b,c,d)))
    assert count_non==540 and len(cycles)==1620
    return cycles

def poset(edges):
    reach=[[False]*4 for _ in range(4)]
    for a,b in edges:reach[a][b]=True
    for k in range(4):
        for i in range(4):
            for j in range(4):
                reach[i][j]|=reach[i][k] and reach[k][j]
    assert not any(reach[i][i] for i in range(4))
    pairs=[(i,j) for i in range(4) for j in range(4) if reach[i][j]]
    intervals={f"{i}-{j}":sum(reach[i][k] and reach[k][j] for k in range(4))
               for i,j in pairs}
    histogram={str(k):sum(v==k for v in intervals.values())
               for k in sorted(set(intervals.values()))}
    chain_height=3 if any(v>=1 for v in intervals.values()) else 2
    return dict(comparable_pairs=len(pairs),proper_interval_interior_histogram=histogram,
                longest_chain_length=chain_height,intervals=intervals)

def verify():
    _,E=w33();cycles=c4s(E)
    diamond=poset([(0,1),(0,2),(1,3),(2,3)])
    opposite=poset([(0,1),(0,2),(3,1),(3,2)])
    assert diamond["comparable_pairs"]==5 and diamond["proper_interval_interior_histogram"]=={"0":4,"2":1}
    assert opposite["comparable_pairs"]==4 and opposite["proper_interval_interior_histogram"]=={"0":4}
    assert diamond["longest_chain_length"]==3 and opposite["longest_chain_length"]==2
    return dict(status="PASS_EXACT_GRAPH_ONLY_CAUSAL_ORIENTATION_OBSTRUCTION",
      date="2026-11-22",w33_vertices=40,w33_edges=240,
      nonadjacent_diagonal_pairs=540,induced_C4s=len(cycles),
      induced_C4_identity="540*choose(4,2)/2=1620",
      sample_C4_vertices=sorted(next(iter(cycles))),
      common_undirected_edges=[[0,1],[0,2],[1,3],[2,3]],
      diamond_edges=[[0,1],[0,2],[1,3],[2,3]],
      two_plus_two_edges=[[0,1],[0,2],[3,1],[3,2]],
      diamond_poset=diamond,two_plus_two_poset=opposite,
      theorem="Identical undirected W33-induced C4 skeletons admit different acyclic Hasse orientations, whose Alexandrov intervals and chain heights differ. Graph counts/eigenvalues alone cannot determine a Lorentzian causal order.",
      physical_boundary="No Einstein-Hilbert dynamics or continuum demonstrated; a dynamical causal orientation and metric/volume laws remain additional physical assumptions.")

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS 1620 W33 C4 witnesses, two non-isomorphic causal posets")
if __name__=="__main__":main()
