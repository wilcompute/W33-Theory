#!/usr/bin/env python3
"""Pass9885-9892: exact symmetry obstruction to a single canonical plus R-Lagrangian.

Pass9765-9772 proves that the plus-type transverse Lagrangians for a fixed
symplectic complex structure R form U(6,3)/O+(6,3).  This pass asks whether the
Leech/Hall-Janko/G2(4) controllers can select ONE such Lagrangian while retaining
their full faithful symmetry.

If a finite controller H embeds faithfully in U(6,3) and fixes a point of the
plus orbit, H is contained in a conjugate of O+(6,3).  More generally its orbit
on a plus Lagrangian has size [H:H cap O+], so

    orbit_size >= |H| / gcd(|H|, |O+|).

For G2(4):2, J2:2 and the G2(4)-edge stabilizer these lower bounds are 560, 35,
and 7.  In particular no fully faithful controller can select a unique plus
polarization.  Extra datum / symmetry breaking is mathematically necessary.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9885_9892_PLUS_LAGRANGIAN_SYMMETRY_NO_GO.json'

U6=182699779456696320
OPLUS=24261120
PLUS_ORBIT=7530558336
CONTROLLERS={
    'G2(4):2':503193600,
    'J2:2':1209600,
    'G2(4) edge stabilizer':24192,
}

def main():
    assert U6//OPLUS==PLUS_ORBIT
    rows={}
    for name,h in CONTROLLERS.items():
        g=math.gcd(h,OPLUS)
        lower=h//g
        rows[name]={
            'order':h,
            'gcd_with_Oplus':g,
            'minimum_possible_orbit_size_under_faithful_embedding':lower,
            'unique_fixed_plus_lagrangian_possible':False,
        }
    assert rows['G2(4):2']['minimum_possible_orbit_size_under_faithful_embedding']==560
    assert rows['J2:2']['minimum_possible_orbit_size_under_faithful_embedding']==35
    assert rows['G2(4) edge stabilizer']['minimum_possible_orbit_size_under_faithful_embedding']==7

    out={
      'schema':'w33.pass9885_9892.plus_lagrangian_symmetry_no_go.v1',
      'status':'PASS','passes':'9885-9892',
      'plus_orbit':{'ambient':'U(6,3)','ambient_order':U6,'stabilizer':'O+(6,3)','stabilizer_order':OPLUS,'size':PLUS_ORBIT},
      'controller_bounds':rows,
      'theorem':('A single plus-type R-transverse Lagrangian cannot be selected while retaining a faithful full G2(4):2, J2:2, or G2(4)-edge-stabilizer action. Their possible orbits on U(6,3)/O+(6,3) have size at least 560, 35, and 7 respectively.'),
      'consequence':('The canonical-plus-polarization program must either break controller symmetry, select a nontrivial orbit/set of plus Lagrangians, or introduce extra structure whose stabilizer is smaller. The Witt-sign repair cannot be a hidden one-point invariant of the full Leech/Hall-Janko/G2 controller.'),
      'boundary':('The obstruction is conditional on a faithful embedding of the named controller into the fixed-R unitary group. It is pure orbit-stabilizer/divisibility and does not assert that such an embedding exists.'),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','orbit_lower_bounds':{k:v['minimum_possible_orbit_size_under_faithful_embedding'] for k,v in rows.items()}}))
    return 0
if __name__=='__main__': raise SystemExit(main())
