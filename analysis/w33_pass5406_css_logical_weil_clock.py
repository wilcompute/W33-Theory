#!/usr/bin/env python3
"""Pass5406: the binary CSS logical module carries the q mod 8 Weil clock.

Pass5379 gives the CSS logical vector space

    L_q = C_W / C_W^perp,
    dim L_q = q^2+1.

In the proof of Theorem 2.13, Lataille--Sin--Tiep show

    C/(C cap C^perp) has composition factors k+k+W1+W2,

and then identify C^perp=U' and C=(U')^perp.  Thus for m=2,
C^perp <= C and the logical quotient C/C^perp has composition factors

    1, 1, W1, W2,

where dim W1=dim W2=(q^2-1)/2.

Remark 2.15 gives the F2 descent clock:
- q = +/-1 mod 8: W1,W2 are individually defined over F2;
- q = +/-3 mod 8: their smallest field is F4, so over F2 the middle pair
  appears as one irreducible Galois-fused module of dimension q^2-1.

This is a composition-factor/field-of-definition theorem.  It does not claim
that the two trivial factors split as direct summands of the logical module.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5406_CSS_LOGICAL_WEIL_CLOCK.json'

def row(q:int)->dict[str,object]:
    assert q%2==1
    w=(q*q-1)//2
    total=q*q+1
    assert 2+2*w==total
    split=q%8 in (1,7)
    return {'q':q,'q_mod_8':q%8,'logical_dimension':total,
      'algebraic_closure_composition_dimensions':[1,1,w,w],
      'weil_factor_dimension':w,
      'F2_middle_structure':f'two {w}-dimensional Weil factors' if split else f'one {2*w}-dimensional irreducible Galois fusion',
      'Weil_field_of_definition':'F2' if split else 'F4'}

def main()->None:
    samples={str(q):row(q) for q in (3,5,7,9,11,13,17,19,25,27)}
    out={'pass':5406,'status':'THEOREM_ALLODD_CSS_LOGICAL_WEIL_QMOD8_CLOCK',
      'logical_module':'L_q=C_W/C_W^perp',
      'dimension':'q^2+1',
      'composition_factors_over_alg_closure':'1, 1, W1, W2 with dim Wi=(q^2-1)/2',
      'F2_descent':'W1,W2 split over F2 for q=+-1 mod8; for q=+-3 mod8 they fuse to one irreducible F2 module of dimension q^2-1.',
      'source':'Lataille--Sin--Tiep, J. Algebra 268 (2003), proof/Theorem 2.13 and Remark 2.15.',
      'samples':samples,
      'boundary':'Composition factors and field-of-definition only. No direct-sum splitting of the two trivial logical factors is asserted.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
