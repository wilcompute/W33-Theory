#!/usr/bin/env python3
"""Pass5387: each q=5 minimum-support K0 fiber contains a (16,6,2) difference set.

Pass5284 proves that on a fixed W-point footprint the restricted zero-footprint
kernel is a 4-dimensional F2-space V, and its 15 nonzero vectors are exactly the
15 pairwise differences of the six chamber stars based at that point.

Choose one chamber-star restriction s0 as affine origin and set
  D={s_i+s0 : i=0,...,5} subset V,
so |D|=6 and 0 in D.  There are C(6,2)=15 unordered pair differences, and Pass5284
says they are exactly the 15 nonzero vectors of V.  Therefore every nonzero group
element occurs exactly twice among ordered differences d-d' (the two orders are
equal in characteristic two but are counted as ordered pairs).  Thus D is a
(16,6,2) difference set in the additive group V~=F2^4.

Equivalently, translating D by all 16 elements of V gives a symmetric
2-(16,6,2) design.  For every nontrivial character chi of V,
|sum_{d in D} chi(d)|^2 = k-lambda = 4, so the character magnitude is exactly2.
This structure was implicit in the six-star/15-difference shell but had not been
named in the repo.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5387_Q5_LOCAL_K0_DIFFERENCE_SET.json'

def main():
    v=16;k=6;lam=2
    assert k*(k-1)==lam*(v-1)==30
    unordered=15;ordered=30
    assert unordered==v-1 and ordered==lam*(v-1)
    out={'pass':5387,'status':'THEOREM_Q5_LOCAL_K0_16_6_2_DIFFERENCE_SET',
      'ambient_group':'additive F2^4, the 4-dimensional restricted K0 kernel on one W-point footprint',
      'difference_set_parameters':'(v,k,lambda)=(16,6,2)',
      'construction':'Choose one of the six chamber-star restrictions as affine origin. The six translated star restrictions form D; their 15 unordered pair differences are exactly all 15 nonzero vectors of F2^4.',
      'ordered_difference_law':'Every nonzero group element occurs exactly lambda=2 times among the 6*5=30 ordered differences.',
      'development':'The 16 translates of D form a symmetric 2-(16,6,2) design.',
      'character_law':'For every nontrivial additive character chi, |sum_{d in D} chi(d)|^2=k-lambda=4, hence magnitude2.',
      'global_multiplicity':'There is one such local affine difference-set structure over each of the 156 W(3,5) point footprints.',
      'connection':'The 15 minimum K0 words over a point are not merely a shell of size15: they are the complete nonzero additive group of the local F2^4 kernel, generated as the difference table of six chamber-star affine points.',
      'dependency':'Pass5284 restricted-kernel dimension4 and exact identification of all 15 nonzero words with the 15 chamber-star pair differences.',
      'boundary':'The theorem is local to each q5 minimum block support. No canonical identification between the 156 affine F2^4 fibers is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
