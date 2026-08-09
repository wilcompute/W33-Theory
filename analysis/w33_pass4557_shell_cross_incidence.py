#!/usr/bin/env python3
"""Pass 4557 (outside box) -- H10 shell distances recover vertex-edge incidence and pencils.

The odd minimum shell consists of forty line-stars s_i=A_*e_i.  The even
weight-20 shell consists of 240 edge vectors s_j+s_k for j~k.  Cross-shell
Hamming distance alone identifies the two endpoints of every edge (distance 12)
and the two other lines in its geometric K4 pencil (distance 28); all remaining
36 line-stars sit at distance 20.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4557_SHELL_CROSS_INCIDENCE.json'

def main():
    vals=build_geometry();A=vals[5]
    stars=[A[:,i].copy() for i in range(40)]
    edges=[(i,j) for i,j in itertools.combinations(range(40),2) if A[i,j]];assert len(edges)==240
    total=Counter()
    for j,k in edges:
        e=stars[j]^stars[k];prof=Counter()
        d12=[];d28=[]
        for i,s in enumerate(stars):
            d=int((s^e).sum());prof[d]+=1;total[d]+=1
            if d==12:d12.append(i)
            if d==28:d28.append(i)
        assert prof==Counter({20:36,12:2,28:2})
        assert set(d12)=={j,k}
        common={i for i in range(40) if A[i,j] and A[i,k]};assert set(d28)==common and len(common)==2
        pencil=set(d12+d28);assert len(pencil)==4 and all(A[a,b] for a,b in itertools.combinations(pencil,2))
    assert total==Counter({20:8640,12:480,28:480})
    out={'pass':4557,'shells':{'odd_line_stars':40,'even_edge_vectors':240},
      'per_edge_cross_distance_profile':{'12':2,'20':36,'28':2},'global_cross_distance_counts':{str(k):v for k,v in sorted(total.items())},
      'reconstruction':{'distance_12':'exactly the two endpoints of the W33 line-graph edge','distance_28':'exactly the two common neighbors of those endpoints','four_line_closure':'the 2 endpoints plus 2 distance-28 stars form the unique K4 pencil through their geometric intersection point'},
      'theorem':'The parity-refined H10 Hamming metric reconstructs not only W33 adjacency but the full vertex-edge incidence and each edge\'s four-line point pencil.',
      'boundary':'Finite Hamming-shell incidence only; no physical distance or spacetime metric is implied.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
