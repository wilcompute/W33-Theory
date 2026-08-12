#!/usr/bin/env python3
"""Pass4957 — Q(4,3) ovoids in the corrected Steiner quotient are W33 spreads.

Pass4954 identifies the 40 Steiner fibers with the forty lines of W(3,3), so
its quotient graph is the line-intersection graph Q(4,3).  An independent set
of ten Q(4,3) vertices is therefore ten pairwise disjoint W33 lines covering
all forty W33 points: exactly a spread.

This verifier enumerates both sides independently and proves equality of the
36 maximum cocliques with the 36 W33 spreads.  Their pair intersections recover
the frozen Pass2000 census: 360 pairs meet in one line and 270 in four lines.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4957_Q43_OVOIDS_ARE_W33_SPREADS.json'

def canon3(v):
    v=np.array(v,dtype=int)%3
    j=next(i for i,x in enumerate(v) if x)
    return tuple((v*pow(int(v[j]),-1,3))%3)

def main()->int:
    pts=sorted({canon3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    assert len(pts)==40
    J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%3
    W=nx.Graph();W.add_nodes_from(range(40))
    for a,b in itertools.combinations(range(40),2):
        if int(np.array(pts[a])@J@np.array(pts[b]))%3==0:W.add_edge(a,b)
    assert W.number_of_edges()==240 and set(dict(W.degree()).values())=={12}
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4)
    assert len(lines)==40
    line_sets=[frozenset(L) for L in lines]

    # Q(4,3) point graph = intersection graph of W33 lines.
    Q=nx.Graph();Q.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if line_sets[i]&line_sets[j]:Q.add_edge(i,j)
    assert Q.number_of_edges()==240 and set(dict(Q.degree()).values())=={12}
    assert not nx.is_isomorphic(W,Q)

    # Enumerate every W33 spread by exact cover of the forty point set.
    point_to={p:[i for i,L in enumerate(line_sets) if p in L] for p in range(40)}
    spreads=[]
    def search(covered,chosen):
        if len(covered)==40:
            spreads.append(tuple(sorted(chosen)));return
        best=None
        for p in range(40):
            if p in covered:continue
            cands=[i for i in point_to[p] if not (line_sets[i]&covered)]
            if not cands:return
            if best is None or len(cands)<len(best):best=cands
        for i in best:search(covered|line_sets[i],chosen+[i])
    search(frozenset(),[])
    spread_sets={frozenset(S) for S in spreads}
    assert len(spread_sets)==36 and all(len(S)==10 for S in spread_sets)

    # Independently enumerate maximal cocliques of Q via maximal cliques of its complement.
    maximal_cocliques=[frozenset(c) for c in nx.find_cliques(nx.complement(Q))]
    size_census=Counter(map(len,maximal_cocliques))
    assert size_census==Counter({5:432,8:135,10:36})
    ovoids={C for C in maximal_cocliques if len(C)==10}
    assert len(ovoids)==36
    assert ovoids==spread_sets

    intersections=Counter(len(A&B) for A,B in itertools.combinations(sorted(spread_sets,key=lambda S:tuple(sorted(S))),2))
    assert intersections==Counter({1:360,4:270})

    # Basic incidence counts: each Q43 point/W33 line lies in nine ovoids/spreads.
    through=[sum(i in S for S in spread_sets) for i in range(40)]
    assert set(through)=={9}

    out={
      'pass':4957,
      'corrected_steiner_quotient':'Q(4,3) point graph = W(3,3) line-intersection graph',
      'maximum_coclique_number':10,
      'maximal_coclique_size_census':{str(k):v for k,v in sorted(size_census.items())},
      'maximum_cocliques':36,
      'W33_spreads':36,
      'set_equality_of_Q43_ovoids_and_W33_spreads':True,
      'incidence':{'lines_per_spread':10,'spreads_through_each_W33_line':9},
      'pair_intersection_census':{'1':360,'4':270},
      'repo_crosscheck':'Pass2000 independently froze the same 36-spread pair census 1^360,4^270.',
      'theorem':'The 36 maximum ten-cocliques of the corrected Steiner quotient Q(4,3) are exactly the 36 spreads of W(3,3), under the identification of Q(4,3) points with W33 lines. Their pair intersections are exactly 360 pairs sharing one line and 270 pairs sharing four lines.',
      'boundary':'This identifies Q43 ovoids with W33 spreads tautologically through point-line duality. It does not identify the 36 spreads with any other 36-element carrier such as the double-sixes without a separate equivariant map.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
