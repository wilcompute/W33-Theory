#!/usr/bin/env python3
"""Pass 4543 (outside box) -- the local Borel cell carries 108 full H10 bases.

The 13-line cell around line 0 is K1 join 4K3.  Its 12 neighbors lie in the
parity-even edge-accessible hyperplane V9; the center line-star is the parity-odd
direction from Pass 4536.

Choose nine of the twelve neighbors, equivalently omit a triple T.  The rank of
the nine corresponding A_* columns is determined exactly by the induced graph
on T inside 4K3:

  T a triangle             -> rank 7,  4 choices;
  T an edge plus isolated  -> rank 8, 108 choices;
  T independent            -> rank 9, 108 choices.

Thus precisely the 108 independent omitted triples give bases of V9. Adding the
center column gives 108 distinct ten-line local bases of all H10.  No ten-line
subset avoiding the center can span H10, because all twelve neighbor columns
have coefficient parity zero modulo the center/edge description.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4543_LOCAL_CELL_BASIS_MATROID.json'

def main():
    *_x,A=build_geometry()[:6]
    center=0; nbr=[int(x) for x in np.flatnonzero(A[center])];assert len(nbr)==12
    cell=[center]+nbr;assert rank2(A[:,cell])==10
    # K1 join 4K3 verification.
    induced=A[np.ix_(cell,cell)]
    assert int(induced[0].sum())==12
    assert sorted(map(int,induced.sum(1)))[1:]==[3]*12

    by_type=defaultdict(Counter); examples={}
    for chosen in itertools.combinations(nbr,9):
        omitted=tuple(sorted(set(nbr)-set(chosen)))
        e=sum(int(A[i,j]) for i,j in itertools.combinations(omitted,2))
        deg=tuple(sorted(sum(int(A[i,j]) for j in omitted if j!=i) for i in omitted))
        typ={(3,(2,2,2)):'triangle',(1,(0,1,1)):'edge_plus_isolated',(0,(0,0,0)):'independent'}[(e,deg)]
        r=rank2(A[:,chosen]);by_type[typ][r]+=1;examples.setdefault(typ,{'chosen':list(chosen),'omitted':list(omitted)})
    assert by_type['triangle']==Counter({7:4})
    assert by_type['edge_plus_isolated']==Counter({8:108})
    assert by_type['independent']==Counter({9:108})

    full=[]
    for chosen in itertools.combinations(nbr,9):
        if rank2(A[:,chosen])==9:
            B=[center]+list(chosen);assert rank2(A[:,B])==10;full.append(B)
    assert len(full)==108 and len({tuple(x) for x in full})==108
    assert all(center in B for B in full)
    # Any 10-line subset of the cell omitting the center stays within V9.
    assert all(rank2(A[:,sub])<=9 for sub in itertools.combinations(nbr,10))

    # The 108 count is structural: independent omitted triples select three of
    # the four K3 pencils and one vertex from each: C(4,3)*3^3=108.
    assert 4*27==108
    # Edge+isolated: choose pencil+edge, another pencil, then vertex = 4*3*3*3.
    assert 4*3*3*3==108

    out={
      'pass':4543,
      'cell':'K1 join 4K3 on 13 lines','center':center,'neighbors':nbr,
      'nine_neighbor_rank_by_omitted_triple':{
        'triangle':{'count':4,'rank':7,'count_formula':'4'},
        'edge_plus_isolated':{'count':108,'rank':8,'count_formula':'4*C(3,2)*3*3'},
        'independent':{'count':108,'rank':9,'count_formula':'C(4,3)*3^3'}},
      'full_local_H10_bases':108,
      'basis_rule':'center line-star plus nine neighbors whose omitted triple is independent across three distinct K3 pencils',
      'center_is_essential':'Every 10-line subset using only the 12 neighbors has rank at most 9; the center supplies the parity-odd tenth direction.',
      'example_full_basis':full[0],
      'examples':examples,
      'theorem':'The 13-line Borel gauge cell contains exactly 108 geometrically characterized ten-line bases of H10. Their V9 part is controlled purely by the omitted-triple type in 4K3.',
      'boundary':'This is a representable-matroid/local-incidence theorem. The 108 bases are not hardware layouts or independent physical encodings without additional constraints.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
