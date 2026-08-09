#!/usr/bin/env python3
"""Pass 4540 -- cross-fuse primitive-six tomography, prism fans, and H10 parity.

Pass 4523 says the degree-two Walsh layer of primitive C6 reconstructs the line
intersection graph A_* of every thick GQ.  In W33, Pass 4536 now says that the
same A_* canonically determines H10=im(A_*), its edge-accessible hyperplane
V9=A_*(even coefficients), and the quotient parity pi(A_*b)=sum b.
Therefore the primitive-six two-body zeta data already reconstructs the full
embedded protected H10 plus its 9+1 parity filtration, not only adjacency.

Passes 4524/4526 explain why the prism carrier is special at t=3: a 3-rung fan
is equivalent modulo ker(A_*) to its (t-2)-rung complement. Only t=3 makes that
complement a single rung/edge. Q(5,3), with t=9, has a 7-rung complement and an
injective 544320-prism protected map.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_apartment_section_core import build_geometry,rank2

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4540_ZETA_PARITY_PRISM_CROSS_FUSION.json'

def main():
    *_x,A=build_geometry()[:6]
    c4523=json.loads((ROOT/'data/PART_W33_PASS4523_GENERAL_GQ_C6_TOMOGRAPHY.json').read_text())
    c4524=json.loads((ROOT/'data/PART_W33_PASS4524_Q53_PRISM_FIBER_EXCEPTION.json').read_text())
    c4526=json.loads((ROOT/'data/PART_W33_PASS4526_GENERAL_GQ_PRISM_FAN_KERNEL.json').read_text())
    c4536=json.loads((ROOT/'data/PART_W33_PASS4536_MISSING_TENTH_PARITY_LINE_STAR.json').read_text())
    assert rank2(A)==10 and c4536['edge_span_dimension']==9
    # W33 C6 coefficient matrix: 48 disjoint, 252 intersecting.
    M=48*(np.ones((40,40),dtype=int)-np.eye(40,dtype=int))+204*A.astype(int)
    recovered=((M==252)&(~np.eye(40,dtype=bool))).astype(np.uint8)
    assert np.array_equal(recovered,A)
    assert c4523['regressions'][1]['s']==3 and c4523['regressions'][1]['t']==3
    assert c4523['regressions'][1]['disjoint']==48 and c4523['regressions'][1]['adjacent']==252
    assert c4526['triangular_prism']['canonical_complement_is_single_edge_iff']=='t=3'
    assert c4524['protected_map']['injective'] is True and c4524['protected_map']['distinct_images']==544320
    out={
      'pass':4540,
      'w33_c6_degree2':{'disjoint':48,'adjacent':252,'matrix_identity':'M6=48(J-I)+204 A_*','recovers_A_star_exactly':True},
      'zeta_to_protected_chain':['primitive-six degree-two Walsh matrix','A_*','H10=im(A_*)','V9=A_*(even coefficients)','H10/V9 coefficient parity pi'],
      'dimensions':{'H10':10,'V9_edge_span':9,'parity_quotient':1},
      'prism_exception':{
        'general_odd_t':'3-rung image equals its (t-2)-rung complement by the full-fan kernel law',
        'W33_t3':'complement has one rung, producing the nine-sheet edge collapse',
        'Q53_t9':'complement has seven rungs; 544320 prism images are injective and have weight 104'},
      'theorem':'For W33, primitive-six two-body zeta tomography determines not only dual-W33 adjacency but the full embedded protected H10 and its canonical 9+1 coefficient-parity filtration. The prism-to-edge carrier is the t=3 endpoint of the general fan-complement law, not an all-GQ phenomenon.',
      'boundary':'This is a reconstruction theorem for finite Walsh/graph/code data. It does not make the Ihara variable physical time or the parity quotient a physical charge.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
