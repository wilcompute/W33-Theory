#!/usr/bin/env python3
"""Pass 4510 -- outside-box: the optimized flag gauge is a radius-one W33 cell.

Pass 4504 exhausts all 64 sections of the canonical order-162 incident-flag
stabilizer and finds a minimum union support of 13 lines.  This pass asks what
those 13 lines ARE geometrically.

They are exactly the closed neighborhood N[l] of the fixed flag line l in the
W33 line-intersection graph:

    one center line + its twelve intersecting lines.

The induced graph is

    K1 join (4 K3).

The four triangles are the four pencils of three other lines through the four
points of l.  Thus the minimal equivariant gauge section is genuinely local in
W33: all ten representative columns can be supported inside one radius-one
line cell.  This is a construction theorem about the finite module, not a claim
about optical near-field locality or physical coupling range.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from w33_apartment_section_core import build_geometry

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4510_LOCAL_FLAG_GAUGE_CELL.json'


def components(A):
    unseen=set(range(len(A)));out=[]
    while unseen:
        s=min(unseen);cc={s};Q=[s]
        while Q:
            x=Q.pop()
            for y in np.flatnonzero(A[x]):
                y=int(y)
                if y not in cc:cc.add(y);Q.append(y)
        unseen-=cc;out.append(sorted(cc))
    return out


def main()->int:
    cert=json.loads((ROOT/'data/PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json').read_text())
    assert cert['pass']==4504 and cert['optimum']['score']==[42,9,13]
    support=cert['optimum']['union'];fixed_line=cert['flag']['line']
    pts,pidx,lines,lidx,A,Astar,*_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    closed=sorted({fixed_line}|set(np.flatnonzero(Astar[fixed_line]).tolist()))
    assert len(closed)==13 and support==closed

    G=Astar[np.ix_(support,support)]
    deg=list(map(int,G.sum(1)));center=support.index(fixed_line)
    assert deg[center]==12 and sorted(deg)==[3]*12+[12]
    rem=[i for i in range(13) if i!=center];H=G[np.ix_(rem,rem)]
    comps=components(H)
    assert sorted(map(len,comps))==[3,3,3,3]
    assert all(np.all(H[np.ix_(c,c)]==(np.ones((3,3),dtype=np.uint8)^np.eye(3,dtype=np.uint8))) for c in comps)

    # Each K3 is exactly the three other lines through one point of the fixed line.
    pencils=[]
    for p in sorted(lines[fixed_line]):
        neigh=sorted(li for li,L in enumerate(lines) if li!=fixed_line and p in L)
        assert len(neigh)==3 and set(neigh)<=set(support)
        pencils.append(neigh)
    assert sorted(map(tuple,pencils))==sorted(tuple(sorted(support[i] for i in c)) for c in comps)

    out={
      'pass':4510,
      'theorem':'the minimum-union flag-equivariant protected section is supported exactly on one closed line neighborhood',
      'fixed_flag_line':fixed_line,
      'support_size':13,
      'support_lines':support,
      'graph':'K1 join 4K3',
      'radius':1,
      'pencils_by_point_on_fixed_line':pencils,
      'relation_to_pass4504':{'sections_exhausted':64,'best_total_weight':42,'best_max_column_weight':9,'minimum_union_support':13},
      'architectural_reading':'A valid symmetry-broken representative register can be synthesized inside one W33 line cell after fixing an incident flag.',
      'boundary':'Graph locality in the finite line-intersection geometry is not automatically spatial, optical, or energetic locality in hardware.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
