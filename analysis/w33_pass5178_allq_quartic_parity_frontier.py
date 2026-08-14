#!/usr/bin/env python3
"""Pass5178: all-q quartic chamber-star parity lower bound with exact dense remainder.

For a chamber leader Y, let r_A be the number of selected chamber stars that
contain apartment A.  Since an apartment has eight chamber edges, 0<=r_A<=8,
and the apartment-code coordinate is r_A mod 2.  The exact binomial parity
expansion begins

  1_{r odd}=r-2*C(r,2)+4*C(r,3)-8*C(r,4)+R_5(r).

For r=0..8 the remainder is nonnegative, vanishes through r=4, and equals
16,64,176,384 at r=5,6,7,8.  Summing apartmentwise gives

 wt >= S1-2S2+4S3-8S4,

with an additional certified +16 for every apartment containing at least five
selected leader chambers.  Pass5140 makes S3 an exact gallery-signature sum and
Pass5159/5177 make S4 an exact four-chamber six-distance-signature sum, so this
is an executable fourth-order frontier rather than a formal inclusion-exclusion
placeholder.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5178_ALLQ_QUARTIC_PARITY_FRONTIER.json'

def quartic(r):
    return r-2*math.comb(r,2)+4*math.comb(r,3)-8*math.comb(r,4)

def main():
    rows=[]
    for r in range(9):
        p=r&1;q4=quartic(r);rem=p-q4
        assert rem>=0
        rows.append({'occupancy':r,'parity':p,'quartic_truncation':q4,'remainder':rem})
    assert [x['remainder'] for x in rows]==[0,0,0,0,0,16,64,176,384]
    out={
      'pass':5178,
      'status':'THEOREM_ALL_Q_QUARTIC_CHAMBER_PARITY_FRONTIER',
      'pointwise_identity':'1_{r odd}=r-2*C(r,2)+4*C(r,3)-8*C(r,4)+R5(r), 0<=r<=8',
      'remainder_table':rows,
      'quartic_lower_bound':'wt(XOR chamber stars) >= S1-2 S2+4 S3-8 S4',
      'dense_remainder_bound':'wt >= S1-2S2+4S3-8S4+16*N_{r>=5}',
      'exact_sparse_sector':'If every apartment contains at most four selected leader chambers, the quartic formula is exact.',
      'moment_inputs':{
        'S1':'m q^4',
        'S2':'exact pair-intersection sum from chamber gallery distances',
        'S3':'exact triple-intersection sum from Pass5140',
        'S4':'exact quadruple-intersection sum from the seven-signature Pass5159/5177 law'
      },
      'connection':'This supplies a collision-safe fourth-order tool for the live leader>=31 q5 frontier. It is especially useful as a dichotomy: sparse apartment occupancy is exactly quartic; occupancy>=5 earns an explicit positive remainder rather than being hidden inside the cubic relaxation.',
      'boundary':'This theorem is an exact inequality/remainder identity. It does not by itself close the currently reserved leader-31 sector or prove q5/all-q minimum distance.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
