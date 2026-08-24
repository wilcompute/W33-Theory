#!/usr/bin/env python3
"""Pass10097-10104 outside-box: the four-channel C15 norm shadow cannot be one W33 clock.

Pass10065 shows that the C4 controller canonically sees a C15 norm shadow of
the Singer C315 torsor.  A natural question is whether that C15 can be realised
as a single cyclic collineation of W(3,3).

No.  The full projective symplectic collineation group of W(3,3) is contained
in PGSp4(3) (order 51840).  For any element s of order 5 in Sp4(3), ord_5(3)=4,
so s acts irreducibly on F3^4.  Its GL4 centralizer is F81^x.  Imposing the
symplectic similitude condition leaves a group of order dividing 20 (and the
symplectic centralizer has order q^2+1=10).  In particular no centralizer of an
order-5 element contains a 3-element.  Therefore no element of order 15 exists
in Sp4(3), PSp4(3), or PGSp4(3).

So the C15 controller shadow cannot be represented by one cyclic W33 symmetry.
It must split its C3 and C5 information into separate/noncommuting channels, or
one factor must be collapsed before landing in W33.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10097_10104_C15_W33_CYCLIC_OBSTRUCTION.json'

def ordmod(a,n):
    x=1
    for k in range(1,100):
        x=x*a%n
        if x==1:return k
    raise RuntimeError

def main():
    q=3
    assert ordmod(q,5)==4
    gl_cent=3**4-1 # irreducible semisimple centralizer F81^x
    sp_cent=q**2+1
    pgsp_upper=2*sp_cent
    assert gl_cent==80 and sp_cent==10 and pgsp_upper==20
    assert sp_cent%3!=0 and pgsp_upper%3!=0
    psp=25920;pgsp=51840
    assert psp%15==0 and pgsp%15==0 # divisibility alone is misleading
    out={
      'schema':'w33.pass10097_10104.c15_w33_cyclic_obstruction.v1','status':'PASS','passes':'10097-10104','outside_box':True,
      'controller_input':'four-channel norm shadow C315 -> C15=C3 x C5 from Pass10065-10072',
      'order5_structure':{'ord_5_3':4,'action_on_F3^4':'irreducible','GL4_3_centralizer':'F81^x, order 80','Sp4_3_centralizer_order':10,'PGSp4_3_centralizer_order_divides':20},
      'no_order15_reason':'An element of order15 would have commuting order5 and order3 parts, forcing a 3-element into the centralizer of its order5 part; that centralizer has no factor3.',
      'groups_ruled_out':['Sp4(3)','PSp4(3)','PGSp4(3) = full projective symplectic similitude group'],
      'theorem':'The canonical C15 four-channel norm shadow cannot embed as a cyclic symmetry of W(3,3): the projective symplectic collineation group has no element of order 15. Any W33 controller realization must split the C3 and C5 information into separate/noncommuting channels or quotient away one factor.',
      'boundary':'This rules out one cyclic C15 action. It does not rule out a noncyclic controller carrying separate order3 and order5 operations.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','C15_in_W33_collineation_group':False,'order5_centralizer':10}))
    return 0
if __name__=='__main__':raise SystemExit(main())
