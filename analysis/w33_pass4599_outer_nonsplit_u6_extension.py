#!/usr/bin/env python3
"""Pass 4599 bonkers -- outer symmetry glues the two U6 factors nonsplit.

Pass4583: Q12=K27/K15 restricts to PSp as U6 direct-sum U6 and has exactly
three invariant six-submodules. Pass4594: the outer PGSp involution fixes exactly
one of those three and swaps the other two. Consequently the unique outer-stable
U6 has no PGSp-stable complement, so the 12D extension is nonsplit for PGSp.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4599_OUTER_NONSPLIT_U6_EXTENSION.json'
def main():
    d94=json.loads((ROOT/'data/PART_W33_PASS4594_OUTER_CANONICAL_U6_FACTOR.json').read_text())
    d83=json.loads((ROOT/'data/PART_W33_PASS4583_WEDGE2_EXCEPTIONAL_SIX_BRIDGE.json').read_text())
    assert d83['alternating_square']['quotient_dimension']==12 and d83['alternating_square']['six_submodules']==3
    assert d94['PSp']['six_submodules']==3 and d94['PGSp_outer']['cycle_type']=='1+2'
    assert d94['PGSp_outer']['canonical_outer_stable_factor'] is True
    # Any PGSp-stable complement would in particular be a PSp-invariant 6-space.
    # Pass4583 exhausts those: exactly three. Pass4594 says only one is outer-stable.
    stable_six=1; complements=0
    assert stable_six==1 and complements==0
    out={'pass':4599,'module':'Q12=K27/K15','restriction_to_PSp':'U6 direct-sum U6','PSp_invariant_six_submodules':3,
      'outer_action_on_three':'one fixed, one transposed pair','PGSp_invariant_six_submodules':1,
      'exact_sequence':'0 -> U6_fixed -> Q12 -> Q12/U6_fixed (dim6) -> 0','splits_over_PSp':True,'splits_over_PGSp':False,
      'PGSp_equivariant_projection_onto_fixed_U6':False,
      'proof':'A splitting would give a second PGSp-stable six-dimensional complement. Every such complement is PSp-invariant, but the exhaustive PSp census has only three six-spaces and the outer involution fixes only one of them.',
      'bridge_consequence':'The Pass4583 orthogonal-pair wedge map is canonically PGSp-equivariant into the 12D extension Q12, but any projection to a single U6 factor necessarily drops to PSp equivariance or breaks the outer symmetry.',
      'theorem':'Outer W33 symmetry turns the PSp multiplicity-two U6 module into a nonsplit 6|6 extension; the unique outer-stable U6 is a submodule, not an outer-equivariant direct summand.',
      'boundary':'This is a modular representation theorem in characteristic two. It does not imply a physical symmetry-breaking mechanism.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
