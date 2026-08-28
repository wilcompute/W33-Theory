#!/usr/bin/env python3
"""Hall-Janko HJ10 versus the native S5 duad carrier.

The native W33 T(10) carrier has an exact transitive S5 action on ten duads.
HJ10, however, was constructed from one fixed C13 torus: take the 32 C13
cycles, quotient by the inner C6 in its C13:C12 normalizer, and obtain ten
states with residual outer C2.

Any ambient symmetry preserving that *specific construction* must preserve the
chosen C13 subgroup and therefore lie in N(C13)=C13:C12, of order 156.  Since
5 does not divide 156, no S5 can act provenance-preservingly on HJ10.

There is an independent obstruction from the canonical HJ10 fibre sizes.  The
ten weights inherited from the 32-cycle quotient are

    1,2,2,3,3,3,3,3,6,6.

The native S5 action is transitive on the ten duads, so every S5-invariant
weight function on that carrier is constant.  HJ10's canonical weights are
not.  Thus even forgetting the torus-normalizer order argument, the weighted
HJ10 object cannot carry the native transitive S5 while preserving its fibre
provenance.

This does not say J2:2 has no S5 subgroup.  It says no such S5 is compatible
with the fixed-C13 quotient that defines these ten HJ states.  The maximal
currently certified shared action remains the residual C2 of profile 1^2 2^4.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=json.loads((ROOT/'data/PART_W33_PASS10869_10876_HJ10_P1F9_TEST.json').read_text())
    w=json.loads((ROOT/'data/PART_W33_PASS10917_10924_HJ10_PROJECTIVE_WEIGHT_OBSTRUCTION.json').read_text())
    assert p['residual_outer_C2_on_10']['profile']=={'1':2,'2':4}
    weights=w['HJ10']['canonical_fibre_sizes_to_32']
    assert weights==[1,2,2,3,3,3,3,3,6,6]
    normalizer_order=13*12
    assert normalizer_order==156 and normalizer_order%5!=0
    assert len(set(weights))>1
    out={
      'status':'PASS',
      'HJ10_residual_C2':'1^2 2^4',
      'C13_normalizer':'C13:C12',
      'normalizer_order':normalizer_order,
      'contains_factor_5':False,
      'provenance_preserving_S5_possible':False,
      'canonical_weights':weights,
      'weights_constant':False,
      'native_transitive_S5_weight_compatible':False,
      'maximal_certified_shared_action':'C2'
    }
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
