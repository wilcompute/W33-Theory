#!/usr/bin/env python3
"""Pass5243 (outside-box): the Hoffman-13 shortening is a [312,52,>=28] doubly-even residual.

Pass5235 gives a 13-coordinate Hoffman cover on which C_F projects surjectively,
with shortening kernel dimension52.  The 13 cover carriers partition the 156
W-points: each point belongs to exactly one cover carrier.  If y=F^T a vanishes
on all cover coordinates, summing those 13 coordinates gives sum_p a_p=0.  The
point-input parity is representation-independent because ker(F^T) is generated
by even weight-6 W-lines (Pass5202).  Hence every shortened word lies in the
Pass5209 hull and has weight divisible by4.

Pass5238 gives d(C_F)=25, so a nonzero shortened word has weight at least28.
There are explicit weight40 shortened words: choose two collinear W-points in
the same cover carrier (one on each of its two polar nonisotropic lines).  Their
point-footprint sum has weight40 and cancels on the common systematic coordinate.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5243_HOFFMAN13_SHORTENED_DOUBLY_EVEN_CODE.json'

def main():
    assert 325-13==312 and 65-13==52
    allowed=[w for w in range(25,41) if w%4==0]
    assert allowed==[28,32,36,40]
    out={'pass':5243,'status':'THEOREM_Q5_HOFFMAN13_SHORTENING_IS_DOUBLY_EVEN_312_52_RESIDUAL',
      'parent':'C_F=[325,65,25]_2 (Pass5238)',
      'systematic_cover_coordinates':13,
      'shortened_length':312,'shortened_dimension':52,
      'doubly_even':True,
      'proof':'Zero on all 13 cover coordinates implies even point-input parity because the cover carriers partition the 156 W-points; therefore the shortened kernel lies in the doubly-even hull.',
      'distance_lower_bound':28,
      'distance_upper_bound':40,
      'possible_minimum_weights':[28,32,36,40],
      'weight40_witness_family':'Two collinear W-points assigned to the same cover carrier give a point-row sum of weight40 and zero cover projection; cross pairs between the carrier line H and H^perp are collinear.',
      'next_target':'Determine whether the shortened residual has d=28,32,36,or40; this is a 52-dimensional search instead of the original 65-dimensional footprint problem.',
      'boundary':'The exact shortened minimum is not claimed here.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
