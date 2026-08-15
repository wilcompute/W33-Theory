#!/usr/bin/env python3
"""Pass5380: q=5 distance-filtered apartment/footprint exact sequence.

This pass does not re-prove the heavy computations.  It composes three exact
certificates already on master:

  Pass5238/5262: apartment code C_A = [73125,625,625]_2, with exactly 936
                  minimum chamber stars, and footprint quotient C_F=[325,65,25]_2.
  Pass5260:      K0=ker(pi:C_A->C_F) has dimension 560.
  Pass5262:      d_block(K0)=25.
  Pass5259/5268: every nonzero even local P block has Hamming weight at least 40.
  Pass5284:      the bound is sharp; every block-minimum K0 word has 25 active
                  blocks of local weight 40, hence weight1000, and the complete
                  shell is 156*C(6,2)=2340 chamber-star pair differences.

Therefore K0 itself has exact binary parameters [73125,560,1000]_2 and we obtain
an exact distance-filtered extension

    0 -> K0 -> C_A -> C_F -> 0.

The striking point is that quotienting by K0 lowers the minimum from 1000 to 625:
the minimum chamber stars necessarily carry nonzero footprint.  The zero-footprint
sector is separated from the physical minimum shell by a factor 1000/625=8/5.
"""
from __future__ import annotations
import json
from math import comb
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5380_Q5_DISTANCE_FILTERED_CODE_EXTENSION.json'

def main():
    n=73125; dimA=625; dimF=65; dimK=560
    dA=625; dF=25; dK=1000
    assert dimK+dimF==dimA
    assert 25*40==dK
    minK=156*comb(6,2)
    assert minK==2340
    assert 156*6==936
    out={
      'pass':5380,
      'status':'THEOREM_Q5_DISTANCE_FILTERED_APARTMENT_FOOTPRINT_EXTENSION',
      'exact_sequence':'0 -> K0 -> C_A -> C_F -> 0',
      'apartment_code':{'parameters':'[73125,625,625]_2','minimum_words':936,
        'minimum_shell':'exactly the chamber stars'},
      'zero_footprint_kernel':{'parameters':'[73125,560,1000]_2','P_block_distance':25,
        'minimum_words':minK,'minimum_supports':156,'words_per_support':comb(6,2),
        'minimum_shell':'same-point pairwise differences of the six chamber stars; 25 active P blocks, local weight 40 in every block'},
      'footprint_quotient':{'parameters':'[325,65,25]_2','minimum_words':156,
        'minimum_shell':'exactly the W(3,5) point footprints'},
      'dimension_identity':'560+65=625',
      'kernel_distance_gap':'d(K0)/d(C_A)=1000/625=8/5',
      'structural_consequence':'Every apartment-code word of weight <1000 has nonzero P-footprint. In particular every minimum word lies outside K0.',
      'proof_dependencies':['Pass5238 footprint distance/minimum shell','Pass5259/5268 local even weight40','Pass5260 exact sequence dimensions','Pass5262 d_block(K0)=25 and full d(C_A)=625','Pass5284 complete K0 block-minimum word shell'],
      'boundary':'q=5 only. This is a synthesis theorem from exact prior certificates; it does not imply the all-q distance q^4 theorem.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
