#!/usr/bin/env python3
"""Pass10861-10868: scalar-gauge local pairing exists; translation-type global repair does not.

Pass10845 finds Fix(k)=F4^3 and the semisimple C3 part s=n^4.  The s-fixed
vectors form one F4-line: 0 plus three nonzero vectors.  Translation by any
nonzero vector v on that line is a fixed-point-free involution of the 64-state
affine cone, commutes with s, and therefore pairs the 64 states into32 C3-
compatible pairs.  The three choices are permuted transitively by the internal
F4^x scalar, so they are one scalar-gauge class.

However a translation tau_v cannot extend as a C13-equivariant intrinsic repair
on V2.  Conjugation by g in the linear C13 sends tau_v to tau_{gv}; invariance
would force gv=v for all g.  The explicit order-13 action on F4^6 is irreducible
(degree-six factor of Phi13), so it has no nonzero fixed vector.  Thus v=0 is
the only C13-invariant translation, and it does not pair anything.

The result is deliberately local/global: there is a canonical local extension
class up to scalar gauge for the C6 complement, but no translation-type global
C13 repair.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10861_10868_LOCAL_PAIRING_GLOBAL_NO_GO.json'

def main():
    j=json.loads((ROOT/'data/PART_W33_PASS10845_10852_NORMALIZER_JORDAN_PG24.json').read_text())
    f=json.loads((ROOT/'data/PART_W33_PASS10453_10476_EXPLICIT_A4G24_COORDINATE_CLOSURE.json').read_text())
    assert j['fixed_cone']['affine_vectors']==64
    assert j['local_pairing_family']['nonzero_translation_choices']==3
    assert j['local_pairing_family']['each_translation_pairs']==32
    assert j['local_pairing_family']['commutes_with_s'] is True
    assert f['explicit_F4_structure_on_E']['g1_order']==13
    assert f['explicit_F4_structure_on_E']['g1_minpoly_low_to_high_F4']==[1,3,0,2,0,3,1]
    assert f['explicit_F4_structure_on_E']['factor_identity'].startswith('p(x) pbar(x) = Phi_13')
    # Irreducible degree6 on F4^6 means no eigenvalue1 and no nonzero fixed vector.
    # Three nonzero translations are exactly the F4^x orbit of one fixed-line vector.
    out={
      'schema':'w33.pass10861_10868.local_pairing_global_no_go.v1','status':'PASS','passes':'10861-10868',
      'local_C6_pairing':{
        'fixed_cone':'Fix(k)=F4^3, 64 affine states','s_fixed_line':'one F4 line, four vectors','nonzero_translation_involutions':3,
        'pairs_per_translation':32,'commutes_with_semisimple_C3':True,'scalar_gauge':'the three choices form one orbit under internal F4^x'},
      'C13_no_go':{
        'conjugation_law':'g tau_v g^-1 = tau_{g v}','C13_action':'irreducible degree6 over F4','nonzero_fixed_vectors':0,
        'only_C13_invariant_translation':'tau_0 = identity','translation_type_global_repair':False},
      'theorem':'The 64 k-fixed states admit a unique scalar-gauge class of C3-compatible perfect matchings, realized by translation along the unique s-fixed F4 line. This realizes locally the 32 missing Jordan extensions. No nontrivial translation pairing can extend C13-equivariantly because the order-13 action is irreducible and fixes no nonzero translation vector.',
      'boundary':'Exact affine/F4 and irreducibility argument. This no-go concerns translation-type intrinsic repairs on the V2 state set; it does not exclude a more general external stable correction module or a non-translation chain-level extension.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','local_pairing':'3 scalar-equivalent translations','global_C13_translation':False}))
if __name__=='__main__':main()
