#!/usr/bin/env python3
"""Pass 4614 bonkers -- the PGSp outer action glues the multiplicity-two U6 nonsplit."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4614_OUTER_NONSPLIT_U6_EXTENSION.json'
def main():
    d=json.loads((ROOT/'data/PART_W33_PASS4609_OUTER_CANONICAL_U6_FACTOR.json').read_text())
    old=json.loads((ROOT/'data/PART_W33_PASS4583_WEDGE2_EXCEPTIONAL_SIX_BRIDGE.json').read_text())
    assert old['alternating_square']['quotient_dimension']==12 and old['alternating_square']['six_submodules']==3
    assert d['PSp']['six_submodules']==3 and d['PGSp_outer']['cycle_type']=='1+2' and d['PGSp_outer']['canonical_outer_stable_factor']
    out={'pass':4614,'module':'Q12=K27/K15','restriction_to_PSp':'U6 direct-sum U6','PSp_invariant_six_submodules':3,
      'outer_action_on_three':'one fixed, one transposed pair','PGSp_invariant_six_submodules':1,
      'exact_sequence':'0 -> U6_fixed -> Q12 -> Q12/U6_fixed (dim6) -> 0','splits_over_PSp':True,'splits_over_PGSp':False,
      'PGSp_equivariant_projection_onto_fixed_U6':False,
      'proof':'A splitting would give a second PGSp-stable six-dimensional complement. Every such complement is PSp-invariant, but the exhaustive PSp census has only three six-spaces and the outer involution fixes only one.',
      'bridge_consequence':'The orthogonal-pair wedge map is canonically PGSp-equivariant into Q12; projection to a single U6 necessarily drops to PSp equivariance or breaks outer symmetry.',
      'theorem':'Outer W33 symmetry turns the PSp multiplicity-two U6 module into a nonsplit 6|6 extension; the unique outer-stable U6 is a submodule, not an outer-equivariant direct summand.',
      'boundary':'Characteristic-two modular representation theorem only; no physical symmetry-breaking mechanism is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
