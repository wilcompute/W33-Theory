#!/usr/bin/env python3
"""Pass10405-10412: internal F4 scalars canonically collapse the C13 clock from 315 to 105 cycles.

Canonical V2 is now intrinsically F4^6 (Pass10389-10396).  For an order-13 element z
inside its G2(4) factor,

  ord_13(4)=6.

Thus on the natural six-dimensional F4 module z is irreducible and has no nonzero fixed
vector.  It partitions V2\{0} into 4095/13=315 vector cycles, reproducing the old abstract
F2 count.

But F4^x=C3 is now an INTERNAL scalar group commuting with z.  Each F4 projective point
contains three nonzero F2 vectors, and the 315 vector cycles group canonically into triples.
Hence z has

  1365/13 = 105

cycles on PG(5,4).  In the ambient GL6(4), the centralizer of an irreducible order-13
element is F_{4^6}^x=C4095.  Projectively this becomes C1365; quotienting by <z>=C13
gives a regular C105 torsor on the 105 projective z-cycles.

This is the first canonical reduction of the former C315 selector ambiguity.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10405_10412_PROJECTIVE_C13_CLOCK_105.json'

def ordmod(a,n):
    x=1
    for k in range(1,n+1):
        x=x*a%n
        if x==1:return k
    raise RuntimeError

def main():
    assert ordmod(4,13)==6
    nonzero=4**6-1;assert nonzero==4095
    vector_cycles=nonzero//13;assert vector_cycles==315
    proj=nonzero//(4-1);assert proj==1365
    projective_cycles=proj//13;assert projective_cycles==105
    assert vector_cycles//3==projective_cycles
    gl_centralizer=4**6-1;assert gl_centralizer==4095
    pgl_centralizer=gl_centralizer//3;assert pgl_centralizer==1365
    torsor=pgl_centralizer//13;assert torsor==105
    # ATLAS G2(4) class 13A/13B centralizers are order 13.
    g2_c13_centralizer=13
    out={
      'schema':'w33.pass10405_10412.projective_c13_clock_105.v1','status':'PASS','passes':'10405-10412',
      'module':{'V2':'F4^6','nonzero_vectors':nonzero,'projective_points_PG5_4':proj,'internal_scalars':'F4^x=C3'},
      'C13':{'ord_13_4':6,'natural_module_action':'irreducible/fixed-point-free','vector_cycles':vector_cycles,'projective_cycles':projective_cycles},
      'centralizers':{'GL6_4':'F_{4^6}^x=C4095','PGL6_4':'C1365','G2_4':'C13 (ATLAS class 13A/13B centralizer)'},
      'selector_reduction':{'old_vector_cycle_torsor':'C315','canonical_scalar_quotient':'divide by internal C3=F4^x','new_projective_cycle_torsor':'C105=C1365/C13'},
      'theorem':'The intrinsic F4 scalar field on canonical V2 canonically projectivizes the semiregular C13 clock: 315 nonzero-vector cycles become 105 cycles on PG(5,4). The ambient projective centralizer quotient acts regularly as C105, so the former C315 ambiguity has an exact canonical C3 quotient and the unresolved projective ambiguity is C105.',
      'boundary':'The F4 structure is Pass10389-10396. Irreducibility follows from ord_13(4)=6 on the natural six-dimensional module; the G2(4) order-13 centralizer order 13 is standard ATLAS data. No claim is made that the remaining C105 lies inside G2(4).'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','vector_cycles':315,'projective_cycles':105,'torsor':'C105'}))
    return 0
if __name__=='__main__':raise SystemExit(main())
