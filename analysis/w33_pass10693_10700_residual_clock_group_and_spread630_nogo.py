#!/usr/bin/env python3
"""Pass10693-10700 outside-box: exact residual clock group decomposition and the W33 630 no-go.

The residual arithmetic controller is G=C105:C6, with the C6 generator acting
by 79 mod105.  CRT gives

  79 mod3 = 1,
  79 mod5 = -1,
  79 mod7 = 2.

Because C6 ~= C2 x C3, with the C2 part acting only on C5 and the C3 part only
on C7,

  G ~= C3 x (C5:C2) x (C7:C3)
    ~= C3 x D10 x (C7:C3).

This has a canonical regular 3 x 10 x 21 combinatorial carrier:
  * C3 on three phase states;
  * D10 on the ten directed edges of a pentagon;
  * C7:C3 on the 21 flags of the Fano plane.
The last action is sharp: write Fano lines as b+D with D={1,2,4}; translation
chooses b and multiplier 2 chooses the incident offset d in D.

W33 independently has 630 unordered pairs of spreads.  That equality is NOT a
W33-equivariant identification: |PSp4(3)|=25920 and |PGSp4(3)|=51840 have no
factor 7, so neither contains G of order 630.  The W33 spread pairs also split
into two intrinsic orbits 360+270.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10693_10700_RESIDUAL_CLOCK_GROUP_AND_SPREAD630_NOGO.json'

def main():
    assert (79%3,79%5,79%7)==(1,4,2)
    assert pow(4,2,5)==1 and pow(2,3,7)==1
    order=105*6; assert order==630==3*10*21

    # Fano flags from the Singer difference set D.
    D=(1,2,4)
    lines=[tuple(sorted((b+d)%7 for d in D)) for b in range(7)]
    flags=[(p,b) for b,L in enumerate(lines) for p in L]
    assert len(flags)==21
    # Affine Singer normalizer action (a,k): x -> a + 2^k x.
    # Line b+D maps to a+2^k b + D because 2D=D.
    def act(flag,a,k):
      p,b=flag;m=pow(2,k,7)
      return ((a+m*p)%7,(a+m*b)%7)
    base=(1,0)
    orbit={(act(base,a,k)) for a in range(7) for k in range(3)}
    assert len(orbit)==21 and orbit==set(flags)
    # Sharpness: group size equals orbit size.
    assert 7*3==len(flags)

    # D10 acts sharply transitively on directed pentagon edges.
    arcs=[(i,(i+s)%5) for i in range(5) for s in (1,-1)]
    assert len(arcs)==10
    # rotations r and reflections s of C5; enumerate images of (0,1).
    d10orbit=set()
    for a in range(5):
      for eps in (1,-1):
        d10orbit.add((a%5,(a+eps)%5))
    assert d10orbit==set(arcs)

    spread=json.loads((ROOT/'data/w33_pass2013_rank_three_spread_association_scheme.json').read_text())
    assert spread['objects']['unordered_spread_pairs']==630
    assert spread['objects']['one_line_pairs']==360 and spread['objects']['four_line_pairs']==270
    psp=25920; pgsp=51840
    assert psp%7!=0 and pgsp%7!=0 and psp%630!=0 and pgsp%630!=0

    out={
      'schema':'w33.pass10693_10700.residual_clock_group_and_spread630_nogo.v1','status':'PASS','passes':'10693-10700','outside_box':True,
      'clock_group':{
        'presentation':'C105 :_<79> C6','order':630,
        'CRT_action':'79 -> (1,-1,2) on C3 x C5 x C7',
        'direct_product_isomorphism':'C3 x D10 x (C7:C3)',
        'factor_orders':[3,10,21]},
      'regular_product_carrier':{
        'C3':'3 qutrit/phase states',
        'D10':'10 directed edges of the pentagon, sharp transitive action',
        'C7:C3':'21 Fano flags, sharp Singer-normalizer action',
        'product_size':'3*10*21=630'},
      'Fano_flag_action':{'difference_set':[1,2,4],'flags':21,'Singer_normalizer_order':21,'regular':True,'ambient_Fano_automorphism_group':'GL(3,2), order 168','Singer_normalizer_index':8},
      'W33_spread_pair_count':{'unordered_pairs':630,'intersection_1_orbit':360,'intersection_4_orbit':270},
      'equivariant_no_go':{
        'PSp4_3_order':25920,'PGSp4_3_order':51840,
        'factor7_absent':True,'C105_C6_subgroup_of_W33_collineation_group':False,
        'additional_obstruction':'the 630 spread pairs are not one W33 orbit; they split 360+270'},
      'theorem':'The residual 105:6 clock controller is exactly C3 x D10 x (C7:C3) and acts regularly on the product of three phase states, ten directed pentagon edges, and twenty-one Fano flags. Although W33 also has 630 unordered spread pairs, there is no W33-collineation-equivariant identification: the collineation groups have no factor 7 and the spread-pair carrier already splits into 360 and 270 orbits.',
      'boundary':'The 3x10x21 product carrier is exact. The equality 630=630 with W33 spread pairs is explicitly retained only as a count after the equivariant no-go.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','group':'C3 x D10 x (C7:C3)','regular_carrier':[3,10,21],'spread630_equivariant':False}))
if __name__=='__main__': main()
