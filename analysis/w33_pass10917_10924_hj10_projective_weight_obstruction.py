#!/usr/bin/env python3
"""Pass10917-10924: the HJ10 split-C2 match does not extend to D16/C4 projective structure.

The ten Hall-Janko states are inner-C6 orbits on the 32 C13 cycles.  Their
canonical fibre sizes are forced by the parent C12 cycle profile:

  fixed under residual C2: 1,3;
  four exchanged pairs:   2,3,3,6  (each size occurs on both states of a pair).

On P1(F9), j:z->-z has centralizer D16=C8:C2 in PGL2(9).  That D16 acts
transitively on the two poles {0,infinity} and transitively on F9^x.  Hence any
D16-invariant weight function is constant on the 2-point pole orbit and on the
8-point moving orbit.  The HJ fibre-size function is not.

After quotienting by j, the four moving antipodal classes form the canonical
C4=F9^x/{+/-1}; its rotation is transitive.  But the HJ moving-pair fibre
weights are {2,3,3,6}, so no C4 rotation can preserve them either.

Thus the exact projective-line bridge stops at the residual C2-set unless one
forgets the canonical C6 fibre sizes or supplies new non-normalizer structure.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10917_10924_HJ10_PROJECTIVE_WEIGHT_OBSTRUCTION.json'

def main():
    old=json.loads((ROOT/'data/PART_W33_PASS10869_10876_HJ10_P1F9_TEST.json').read_text())
    prof={int(k):int(v) for k,v in old['C12_on_32_C13_cycles']['cycle_profile'].items()}
    # Odd C12 cycles give residual-C2 fixed C6-orbits; even cycles split into paired C6-orbits.
    fixed=[];pairs=[]
    import math
    for d,m in prof.items():
      if d%2:
        fixed += [d]*m
      else:
        # each C12 cycle splits into two C6 cycles of size d/2, exchanged by residual C2
        pairs += [d//2]*m
    assert sorted(fixed)==[1,3]
    assert sorted(pairs)==[2,3,3,6]
    # Ten-state fibre weights: each moving pair contributes two states of the same size.
    ten_weights=sorted(fixed+[x for x in pairs for _ in (0,1)])
    assert ten_weights==[1,2,2,3,3,3,3,3,6,6]
    assert sum(ten_weights)==32

    # D16 orbits on P1(F9) under the split involution centralizer are 2 poles + 8 moving points.
    p1_orbits=[2,8]
    # A D16-invariant fibre-size function must be constant on each orbit; HJ is not.
    pole_constant=(fixed[0]==fixed[1])
    moving_values=Counter([x for x in pairs for _ in (0,1)])
    moving_constant=(len(moving_values)==1)
    assert not pole_constant and not moving_constant
    # C4 quotient rotates the four antipodal moving classes transitively; pair weights are nonconstant.
    c4_pair_weights=sorted(pairs)
    assert c4_pair_weights==[2,3,3,6] and len(set(c4_pair_weights))>1

    out={
      'schema':'w33.pass10917_10924.hj10_projective_weight_obstruction.v1','status':'PASS','passes':'10917-10924',
      'HJ10':{
        'canonical_fibre_sizes_to_32':[1,2,2,3,3,3,3,3,6,6],
        'residual_C2_fixed_state_weights':[1,3],
        'residual_C2_moving_pair_weights':[2,3,3,6]},
      'P1F9_split_model':{
        'D16_orbits_on_10_points':[2,8],
        'j_quotient':'2 poles + C4','C4_moving_classes':4,
        'weight_preserving_D16_extension':False,
        'weight_preserving_C4_rotation':False},
      'theorem':'The HJ10 residual involution is isomorphic to the split involution z->-z on P1(F9) only as a C2-set. The canonical Hall-Janko fibre sizes obstruct every extension to the natural projective centralizer D16 and already obstruct the C4 rotation on the four antipodal moving classes: the two fixed-state weights are 1 and3 and the moving-pair weights are 2,3,3,6. Therefore cross-ratio/C4 structure is not inherited from the torus-normalizer quotient.',
      'boundary':'Exact consequence of the certified C12 cycle profile and the explicit P1(F9) split-involution centralizer. A projective-line structure could still be imposed after forgetting fibre sizes or by adding external geometry; this pass rules out a canonical lift preserving the normalizer quotient data.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','D16_extension':False,'C4_extension':False,'fixed_weights':[1,3],'moving_pair_weights':[2,3,3,6]}))
if __name__=='__main__':main()
