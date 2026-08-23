#!/usr/bin/env python3
"""Pass9893-9900: test the proposed 13-state common quotient on the 416 G2(4) vertices.

The Pass9773-9780 information-budget observation only said that a *uniform*
common quotient of 4095 Leech frames, 416 Hall-Janko vertices and 20800 G2 edges
could have nontrivial size only 13.  Divisibility is necessary, not sufficient.

The 416-point G2(4):2 action is rank 3.  A vertex stabilizer has suborbits
1, 100, 315 (the vertex, its graph neighbors, and its nonneighbors).  Any block
of imprimitivity containing that vertex is fixed setwise by the vertex
stabilizer, hence is a union of these suborbits.  Its size must therefore be
one of 1, 101, 316, 416.  A 13-block quotient would require block size 32.
Impossible.
"""
from __future__ import annotations
import json,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9893_9900_THIRTEEN_STATE_RANK3_BLOCK_NO_GO.json'

V=416
SUBDEGREES=(1,100,315)
TARGET_STATES=13
TARGET_BLOCK=V//TARGET_STATES

def main():
    assert V%TARGET_STATES==0 and TARGET_BLOCK==32
    sizes=sorted({sum(SUBDEGREES[i] for i in range(3) if mask>>i&1)
                  for mask in range(1,1<<3) if mask&1})
    # A block containing the base vertex must include the 1-suborbit.
    assert sizes==[1,101,316,416]
    assert TARGET_BLOCK not in sizes
    out={
      'schema':'w33.pass9893_9900.thirteen_state_rank3_block_no_go.v1',
      'status':'PASS','passes':'9893-9900',
      'action':{'group':'G2(4):2','degree':416,'rank':3,'point_stabilizer':'J2:2','subdegrees':list(SUBDEGREES)},
      'proposed_13_state_quotient':{'number_of_blocks':13,'required_block_size':TARGET_BLOCK,'allowed_block_sizes_containing_basepoint':sizes,'exists_as_G2_equivariant_block_system':False},
      'proof':('If B is a block containing alpha and h fixes alpha, then hB is another block containing alpha, hence hB=B. Thus B is a union of G_alpha-suborbits. Rank 3 gives only subdegrees 1,100,315, so a basepoint block has size 1,101,316,or416, never32.'),
      'theorem':('The numerical gcd=13 from Pass9773-9780 does not lift to a full-G2(4):2-equivariant 13-state quotient of the 416 Hall-Janko/G2 vertices. The rank-3 action has no 32-point block.'),
      'consequence':('Any genuine 13-state selector must break full G2(4):2 symmetry, live on a different derived object, or use extra structure rather than a block system of the rank-3 vertex action.'),
      'boundary':'Exact permutation-action block argument using the repo-certified rank-3 subdegrees 1+100+315=416.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','allowed_block_sizes':sizes,'target':TARGET_BLOCK}))
    return 0
if __name__=='__main__':raise SystemExit(main())
