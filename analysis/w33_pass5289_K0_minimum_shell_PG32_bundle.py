#!/usr/bin/env python3
"""Pass5289 (outside-box): the q=5 K0 block-minimum shell is a PG(3,2) bundle over W points.

Pass5284 proves that over each W point p the 15 K0 block-minimum words are exactly
the pairwise differences of the six chamber stars (p,l) on the six W-lines through
p. There is a canonical 4-dimensional label space for this fiber.

Let E6 <= F2^6 be the even-weight coefficient space on the six chamber stars.
Every apartment through p contains exactly two of those six p-chambers, hence the
XOR of all six chamber stars is zero. Thus the difference map factors through

  E6 / <111111>,

which has dimension 5-1=4. Every nonzero quotient class has a unique weight-two
representative up to complement, hence is labeled by an unordered pair of the six
lines through p. There are C(6,2)=15 such classes. Over F2, the 15 nonzero vectors
of a 4-space are exactly the 15 projective points of PG(3,2).

Therefore the complete 2340-word block-minimum shell is a 156-point W(3,5) base
with a canonical PG(3,2) fiber over each point. This is finite code geometry, not
a physical-fiber assertion.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5289_K0_MINIMUM_SHELL_PG32_BUNDLE.json'

def main():
    ALL=(1<<6)-1
    even=[m for m in range(1<<6) if m.bit_count()%2==0]
    assert len(even)==32
    classes={min(m,m^ALL) for m in even}
    assert len(classes)==16
    nonzero=classes-{0}
    assert len(nonzero)==15
    reps2={m for m in nonzero if m.bit_count()==2}
    # Canonical min() need not always be the weight-two member, so identify each
    # class by whichever of m and its complement has weight two.
    pairs=[]
    for c in nonzero:
        a=c if c.bit_count()==2 else c^ALL
        assert a.bit_count()==2
        pairs.append(tuple(i for i in range(6) if (a>>i)&1))
    assert len(set(pairs))==15==len(list(itertools.combinations(range(6),2)))

    out={
      'pass':5289,
      'status':'THEOREM_Q5_K0_BLOCK_MINIMUM_SHELL_IS_PG32_BUNDLE_OVER_W_POINTS',
      'base_W_points':156,
      'fiber_chamber_stars':6,
      'coefficient_space':'E6 = even-weight subspace of F2^6, dimension 5',
      'fiber_relation':'111111 maps to zero because every apartment through p contains exactly two p-chambers',
      'fiber_vector_space':'E6/<111111>, dimension 4',
      'nonzero_fiber_vectors':15,
      'projective_identification':'Over F2 these 15 nonzero vectors are the 15 points of PG(3,2).',
      'pair_labels':'Each nonzero class is uniquely labeled by an unordered pair of the six W-lines through p (weight-two representative modulo complement).',
      'total_minimum_words':2340,
      'bundle_count':'156 * 15 = 2340',
      'boundary':'Exact q5 code-geometric bundle statement. It does not identify a physical fiber or imply a dynamical PG(3,2) degree of freedom.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
