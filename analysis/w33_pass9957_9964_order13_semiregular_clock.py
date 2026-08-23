#!/usr/bin/env python3
"""Pass9957-9964 outside-box: the surviving 13-state structure is a semiregular clock.

Pass9893-9900 rules out a full-G2(4):2 13-block quotient of the 416 vertices.
Nevertheless 13 is a genuine dynamical period.  The vertex stabilizer J2:2 and
the G2-edge stabilizer have orders not divisible by 13.  Therefore an element
of order 13 cannot fix a vertex or an edge: a fixed coset would conjugate that
element into the corresponding stabilizer, contradicting Lagrange.

Hence every C13 acts semiregularly:
  416 vertices = 32 cycles of length 13,
  20,800 edges = 1,600 cycles of length 13,
  41,600 incident flags = 3,200 cycles of length 13.

A regular C13 on 13 labels is the Singer-cycle size q^2+q+1 for PG(2,3), so a
chosen orbit can be given a 13-state projective-plane clock labeling.  Choosing
the C13/orbit is extra datum; this does not contradict the block no-go.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9957_9964_ORDER13_SEMIREGULAR_CLOCK.json'
G=503193600
V=416;E=20800;FLAGS=41600
VERT_STAB=1209600
EDGE_STAB=24192

def main():
    assert G%13==0 and V%13==E%13==FLAGS%13==0
    assert VERT_STAB%13!=0 and EDGE_STAB%13!=0
    cycles={'vertices':V//13,'edges':E//13,'incident_flags':FLAGS//13}
    assert cycles=={'vertices':32,'edges':1600,'incident_flags':3200}
    assert 3**2+3+1==13
    out={
      'schema':'w33.pass9957_9964.order13_semiregular_clock.v1','status':'PASS','passes':'9957-9964','outside_box':True,
      'group':{'G2(4):2_order':G,'order13_divides_group':True},
      'stabilizers':{'vertex_J2:2':VERT_STAB,'edge':EDGE_STAB,'both_prime_to_13':True},
      'semiregular_C13':{'vertex_cycles':32,'edge_cycles':1600,'flag_cycles':3200,'cycle_length':13},
      'projective_plane_reading':{'Phi3_at_q3':13,'PG(2,3)_points':13,'Singer_cycle_order':13,'interpretation':'each chosen C13 orbit is a natural 13-state clock after a Singer labeling'},
      'proof':'An order-13 element fixing a coset G/H is conjugate into H. Since neither relevant stabilizer order is divisible by 13, no nonidentity element of C13 fixes a vertex or edge; all orbits therefore have length13.',
      'theorem':'Although no full-G2 13-block quotient exists, every order-13 subgroup acts semiregularly on both the 416 Hall-Janko vertices and the 20,800 G2 edges, producing exactly 32 and 1,600 thirteen-cycles. The surviving 13-state object is a chosen cyclic clock, not a global quotient.',
      'boundary':'Exact group-action divisibility. Identifying a chosen 13-cycle with PG(2,3) uses the standard Singer-cycle model and requires a noncanonical choice of C13/orbit/labeling.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','cycles':cycles}));return 0
if __name__=='__main__':raise SystemExit(main())
