#!/usr/bin/env python3
"""Pass5212 (bonkers): an exact 13-dual-grid partition / Hoffman coclique at q=5.

Pass5211 identifies the 325 P components with the NO_5^+(5) vertices, and
Pass5187 identifies each vertex with a 12-point dual grid H union H^perp in
W(3,5).  This producer reconstructs the 325 grids canonically and verifies an
explicit set of 13 that partitions all 156 W-points.

Two P-component blocks are adjacent in Pass5203 exactly when they meet in two
points.  The 13 partition blocks are disjoint, hence form a coclique.  For
SRG(325,144,68,60) with least eigenvalue -6, Hoffman's bound is

  alpha <= 325*6/(144+6)=13,

so the coclique is maximum.  Every W-point footprint is a distinguished maximum
25-clique and a point belongs to exactly one partition block, so every such
25-clique meets the 13-coclique exactly once.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5212_Q5_DUALGRID_HOFFMAN_13_COVER.json'
SELECTED=[6,30,73,111,128,140,157,189,193,226,254,277,320]

def geometry(q=5):
    def norm(v):
        for a in v:
            if a%q:
                z=pow(a,-1,q);return tuple((z*x)%q for x in v)
        raise ValueError
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)}
    def s(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%q
    def span(x,y):
        S={norm(tuple((x[i]+t*y[i])%q for i in range(4))) for t in range(q)}
        S.add(norm(y));return frozenset(pi[z] for z in S)
    H=set()
    for i,j in itertools.combinations(range(len(pts)),2):
        if s(pts[i],pts[j])!=0:H.add(span(pts[i],pts[j]))
    pairs=set()
    for h in H:
        a,b=sorted(h)[:2]
        hp=frozenset(i for i,y in enumerate(pts) if s(pts[a],y)==0 and s(pts[b],y)==0)
        pairs.add(frozenset((h,hp)))
    blocks=sorted((frozenset().union(*p) for p in pairs),key=lambda B:tuple(sorted(B)))
    assert len(pts)==156 and len(blocks)==325 and {len(B) for B in blocks}=={12}
    return pts,blocks

def main():
    pts,B=geometry();C=[B[i] for i in SELECTED]
    assert len(set().union(*C))==156
    assert sum(len(x) for x in C)==156
    assert all(not (C[i]&C[j]) for i,j in itertools.combinations(range(13),2))
    # Hoffman bound for Pass5203 q5 block SRG.
    n,k,s=325,144,-6
    hoff=n*(-s)//(k-s);assert hoff==13
    # Every W point lies in 25 dual grids and exactly one chosen cover grid.
    point_degrees=[];cover_degrees=[]
    for p in range(156):
        point_degrees.append(sum(p in X for X in B))
        cover_degrees.append(sum(p in X for X in C))
    assert set(point_degrees)=={25} and set(cover_degrees)=={1}
    out={'pass':5212,'status':'THEOREM_Q5_DUALGRID_HOFFMAN_13_COVER',
      'block_graph':'NO_5^+(5)=SRG(325,144,68,60)','least_eigenvalue':-6,
      'Hoffman_coclique_bound':13,'selected_canonical_block_indices':SELECTED,
      'dual_grid_block_size':12,'selected_blocks':13,'covered_W_points':156,
      'pairwise_intersection':'0 for every selected pair',
      'partition':'The 13 selected dual grids partition the 156 W-points.',
      'clique_transversal':'Every distinguished W-point footprint clique of size25 meets the 13-coclique in exactly one P component.',
      'conclusion':'The q5 P-component graph contains a maximum Hoffman coclique that is simultaneously an exact dual-grid resolution of W(3,5) points.',
      'boundary':'Existence theorem/certificate at q=5; no uniqueness or all-q existence classification is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
