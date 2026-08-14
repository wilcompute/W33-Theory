#!/usr/bin/env python3
"""Pass5213 (bonkers): exact dual of the q=5 footprint code is [325,260,8]_2.

Let F be the 156x325 point/dual-grid incidence matrix.  The dual of the footprint
row code C_F is ker(F): selected P components such that every W-point lies in an
even number of selected dual grids.  Pass5202 gives rank(F)=65, hence
C_F^perp has dimension 260.

Lower bound.  For a nonzero dual word X of t blocks, let r_p be the number of
selected blocks through W-point p and E the number of adjacent selected pairs in
the Pass5203 block graph.  Every r_p is even and

  sum r_p = 12t,
  sum C(r_p,2) = 2E,

because an adjacent block pair intersects in exactly two points.  For positive
even r, C(r,2)>=r/2, so E>=3t.  Since E<=C(t,2), t>=7.

If t=7 then equality is forced everywhere: the seven blocks form K7 in the block
graph and every covered point has r_p=2.  By transitivity fix one base block.
Its six partners must meet it in six disjoint 2-point edges partitioning its 12
points.  In the canonical q=5 geometry the base has 36 possible intersection
edges and exactly four other blocks over each edge.  A deterministic exact
backtrack enforces pairwise 2-point intersections and point multiplicity <=2;
it exhausts the search in 265 recursion nodes and finds no completion.
Therefore d>=8.

Finally the hard-coded canonical 8-block support below is verified to give point
degrees 0 or 2, so it is a dual codeword of weight 8.  Its induced block graph is
6-regular on 8 vertices, i.e. K8 minus a perfect matching.
"""
from __future__ import annotations
import itertools,json
from collections import defaultdict,Counter
from pathlib import Path
from analysis.w33_pass5212_q5_dualgrid_Hoffman_13_cover import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5213_Q5_FOOTPRINT_DUAL_325_260_8.json'
W8=[119,124,183,188,209,302,317,318]

def rank_bits(rows):
    P={}
    for r0 in rows:
        r=r0
        while r:
            p=r.bit_length()-1
            if p in P:r^=P[p]
            else:P[p]=r;break
    return len(P)

def main():
    pts,B=geometry();assert len(B)==325
    # Point-row rank of F.
    rows=[]
    for p in range(156):
        z=0
        for i,X in enumerate(B):
            if p in X:z|=1<<i
        rows.append(z)
    rank=rank_bits(rows);assert rank==65

    # Lower bound t>=7 from even point degrees and the block graph.
    # Exclude the equality t=7 exactly, fixing block 0 by transitivity.
    base=0;B0=B[base]
    neighbors=[j for j,X in enumerate(B) if j!=base and len(B0&X)==2]
    assert len(neighbors)==144
    groups=defaultdict(list)
    for j in neighbors:groups[tuple(sorted(B0&B[j]))].append(j)
    assert len(groups)==36 and set(map(len,groups.values()))=={4}
    bypoint=defaultdict(list)
    for e in groups:
        for p in e:bypoint[p].append(e)
    nodes=0;found=False
    def bt(uncovered,chosen,mult):
        nonlocal nodes,found
        nodes+=1
        if not uncovered:found=True;return
        p=min(uncovered)
        for e in bypoint[p]:
            if not set(e)<=uncovered:continue
            for j in groups[e]:
                if any(len(B[j]&B[k])!=2 for k in chosen):continue
                M=mult.copy();ok=True
                for x in B[j]:
                    M[x]=M.get(x,0)+1
                    if M[x]>2:ok=False;break
                if ok:bt(uncovered-set(e),chosen+[j],M)
                if found:return
    bt(set(B0),[],{p:1 for p in B0})
    assert not found and nodes==265

    # Explicit weight-eight word.
    C=[B[i] for i in W8]
    deg=Counter(p for X in C for p in X)
    assert Counter(deg.values())=={2:48}
    assert len(deg)==48
    iadj=[]
    for i,j in itertools.combinations(range(8),2):
        z=len(C[i]&C[j]);assert z in (0,2)
        if z==2:iadj.append((i,j))
    dd=Counter()
    for i,j in iadj:dd[i]+=1;dd[j]+=1
    assert len(iadj)==24 and set(dd.values())=={6}

    out={'pass':5213,'status':'THEOREM_Q5_FOOTPRINT_DUAL_CODE_325_260_8',
      'primal':'C_F=im(F^T) has length325 and dimension65.',
      'dual':'C_F^perp=ker(F) has dimension260.',
      'lower_bound':'Even point degrees give E>=3t for a t-block dual word, hence t>=7.',
      'weight7_exclusion':{'fixed_base_by_transitivity':0,'base_neighbors':144,
        'intersection_edge_groups':36,'other_blocks_per_edge':4,
        'exact_backtrack_nodes':nodes,'solutions':0},
      'weight8_support_canonical_indices':W8,
      'weight8_geometry':'48 W-points, each covered exactly twice; induced block graph K8 minus a perfect matching.',
      'code_parameters':'[325,260,8]_2',
      'connection':'The d=25 primal footprint problem now has an exact dual minimum and an explicit weight-8 dual shell available for MacWilliams/LP/local-check attacks.',
      'boundary':'This proves the dual distance, not the primal footprint distance25.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
