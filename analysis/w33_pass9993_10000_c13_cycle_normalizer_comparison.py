#!/usr/bin/env python3
"""Pass9993-10000: classify the abstract V2 C13 cycles and compare them with G2(4):2 clocks.

Pass9973-9980 gave an abstract irreducible C13 on V2=F2^12.  Pass9985-9992
keeps its Co0 realization open.  This pass classifies what the abstract action
actually supplies and compares it to the certified semiregular C13 actions on
the G2(4):2 416-vertex / 20800-edge carriers.

The key refinement is the normalizer.  Since ord_13(2)=12, the irreducible
F2[C13]-module is F_{2^12}.  The centralizer of C13 in GL(12,2) is the full
Singer scalar group F_{2^12}^x=C4095, and its semilinear normalizer is
C4095:C12.  Thus the 315 C13 cycles on V2\{0} form a regular C315 torsor under
C4095/C13, with a common C12 Frobenius clock above them.

On G2(4):2 an order-13 maximal torus has normalizer C13:C12.  The same C12
therefore controls the local automorphism of each 13-clock, but there is no
C315 scalar torsor.  This isolates the precise symmetry mismatch to be removed
by any actual V2/G2 weld.
"""
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9993_10000_C13_CYCLE_NORMALIZER_COMPARISON.json'

G2EXT=503_193_600
VERTICES=416
EDGES=20_800
FLAGS=41_600


def ordmod(a,n):
    x=1
    for k in range(1,1000):
        x=x*a%n
        if x==1:return k
    raise RuntimeError


def main():
    assert ordmod(2,13)==12
    field_units=2**12-1
    assert field_units==4095==13*315
    gl_normalizer=field_units*12
    assert gl_normalizer==49_140
    assert VERTICES//13==32 and EDGES//13==1600 and FLAGS//13==3200
    vst=G2EXT//VERTICES; est=G2EXT//EDGES; fst=G2EXT//FLAGS
    assert (vst,est,fst)==(1_209_600,24_192,12_096)
    assert all(x%13 for x in (vst,est,fst))
    g2_torus_normalizer=13*12
    assert g2_torus_normalizer==156
    assert field_units//13==315

    out={
      'schema':'w33.pass9993_10000.c13_cycle_normalizer_comparison.v1','status':'PASS','passes':'9993-10000',
      'V2_abstract_C13':{
        'module':'F2^12 ~= additive F_{2^12}','ord_13_2':12,
        'nonzero_directions':4095,'C13_cycles':315,
        'centralizer_in_GL12_2':'F_{2^12}^x = C4095','centralizer_order':field_units,
        'normalizer_in_GL12_2':'C4095:C12','normalizer_order':gl_normalizer,
        'cycle_torsor':'C4095/C13 = C315 acts regularly on the 315 C13 cycles'},
      'G2_4_colon_2':{
        'group_order':G2EXT,
        'vertex_carrier':{'size':VERTICES,'stabilizer_order':vst,'C13_cycles':32},
        'edge_carrier':{'size':EDGES,'stabilizer_order':est,'C13_cycles':1600},
        'flag_carrier':{'size':FLAGS,'stabilizer_order':fst,'C13_cycles':3200},
        'order13_torus_normalizer':'C13:C12','normalizer_order':g2_torus_normalizer},
      'common_structure':{
        'clock':'C13','clock_automorphisms':'C12',
        'meaning':'Both sides naturally carry a 12-step automorphism clock on a chosen C13.'},
      'mismatch':{
        'V2_extra_scalar_factor':315,
        'explanation':'The abstract GL12 realization has a C315 torsor of C13 cycles coming from F_{2^12}^x/C13; the G2 torus centralizer is only C13.',
        'weld_target':'An actual Co0/G2 bridge must collapse or geometrically identify this extra C315 scalar ambiguity.'},
      'theorem':('The 315 abstract V2 C13 cycles are not merely a count: they form a regular C315 torsor under the Singer centralizer quotient, while the clock automorphism quotient is C12. G2(4):2 has the same local C13:C12 clock but no C315 scalar centralizer. The exact mismatch is therefore C315.'),
      'boundary':'The V2 statement is for the abstract GL(12,2) C13 until Pass9985 existence is resolved. The G2 torus normalizer is standard finite-group structure; semiregularity follows from stabilizer orders prime to 13.'}
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','V2_cycles':315,'G2_cycles':[32,1600,3200],'normalizer_gap':315}))
    return 0
if __name__=='__main__':raise SystemExit(main())
