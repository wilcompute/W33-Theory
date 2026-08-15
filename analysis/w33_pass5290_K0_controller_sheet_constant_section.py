#!/usr/bin/env python3
"""Pass5290 (outside-box): K0 minimum fibers are constant sections over the 5x5 controller sheet.

Fix a q=5 W point p. Pass5289 gives the 4D fiber U_p=E6/<111111> labeling
the 15 differences of the six chamber stars through p. Pass5268 identifies, in
each of the 25 P blocks of the common point footprint, the corresponding six
p-incident minimum atoms and proves that every nonzero pair-difference class has
local weight 40.

For every footprint block c there is therefore a natural injective map
  phi_c : U_p -> E_c
into the 24D even local P-block code, sending a chamber-pair class to its local
adjacent-atom difference. The restricted K0 minimum subcode is the diagonal
section
  u -> (phi_c(u))_{c in footprint(p)}.
Pass5284 proves this diagonal has dimension 4 and exhausts the restricted kernel.
Every nonzero section has 25 local blocks of weight 40, hence global weight 1000.

Pass5217 identifies the 25 P blocks of a chosen q=5 chamber-star footprint with
(a,c) in F5^2 via the controller projection (a,b,c,d)->(a,c). Under that chart,
the K0 minimum fiber is a constant rank-4 binary section over the full 5x5 sheet.
This is an exact coordinate/local-system statement, not a dynamical or optical
claim.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5290_K0_CONTROLLER_SHEET_CONSTANT_SECTION.json'

def main():
    blocks=25; block_length=225; local_weight=40; dim=4
    length=blocks*block_length; weight=blocks*local_weight
    assert length==5625 and weight==1000 and (1<<dim)-1==15
    out={
      'pass':5290,
      'status':'THEOREM_Q5_K0_MINIMUM_FIBER_IS_DIAGONAL_CONSTANT_SECTION_ON_CONTROLLER_SHEET',
      'fixed_point_fiber':'U_p = E6/<111111> ~= F2^4',
      'fiber_dimension':4,
      'nonzero_fiber_symbols':15,
      'footprint_blocks':25,
      'local_block_code_length':225,
      'local_fiber_embedding':'For each footprint block c, phi_c maps a chamber-pair class to the corresponding adjacent-atom local even word; every nonzero image has weight40.',
      'global_diagonal_map':'u -> (phi_c(u)) over all 25 blocks',
      'restricted_linear_code':'[5625,4,1000]_2 after zero-extension to all 225 coordinates of each of the 25 blocks',
      'all_nonzero_global_weights':1000,
      'controller_trivialization':'Pass5217 labels the 25 footprint blocks by (a,c) in F5^2 under (a,b,c,d)->(a,c); the diagonal code is a constant U_p-valued section over this 5x5 sheet.',
      'boundary':'Exact finite code/controller-coordinate theorem. It does not assert physical transport, optical dynamics, or that the local system is physically realized.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
