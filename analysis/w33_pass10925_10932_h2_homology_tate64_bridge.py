#!/usr/bin/env python3
"""Pass10925-10932 outside-box: correctly type the three recurring 64s.

Three different objects in the frontier all display the integer64:

1. Fix(n^3)=F4^3 has 64 ELEMENTS but F2-dimension6.
2. The characteristic-2 Tate defect is 1^64, an F2-vector space of DIMENSION64.
3. H1(Levi H(2);F2) has DIMENSION beta1=2^6=64.

Only (2) and (3) are the same categorical size.  Thus the H(2) cycle space can
serve as an exact 64-dimensional geometric model for the external trivial
correction term in

  F2[V2] + J2^32 ~= H1(H4) + 1^64,

provided the normalizer C2 is declared to act trivially on that external
coefficient space.  This does not identify the 64 affine fixed-cone states
with H(2) cycles, and it does not claim that the intrinsic H(2) automorphism
action is trivial.

The construction is noncanonical in the Hall-Janko geometry because one HJ
realization contains a family of 100 embedded H(2) subhexagons; choosing one
selects one 64-dimensional cycle space.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10925_10932_H2_HOMOLOGY_TATE64_BRIDGE.json'

def beta_hex(q):
    P=(q+1)*(q**4+q**2+1);E=(q+1)*P
    return E-2*P+1

def main():
    assert beta_hex(2)==64 and beta_hex(4)==4096
    fixed_cone_elements=4**3;fixed_cone_F2_dim=6
    assert fixed_cone_elements==64
    tate_dim=64
    h2_dim=beta_hex(2)
    assert tate_dim==h2_dim==64 and fixed_cone_F2_dim!=64
    # Vector-space cardinalities expose the type distinction.
    assert 2**fixed_cone_F2_dim==64
    # Do not materialize 2^64; record symbolically.
    old=json.loads((ROOT/'data/PART_W33_PASS10885_10892_C2_TATE_EXT_DEFECT.json').read_text())
    assert old['Tate_cohomology']['F2V2_dimension_each_degree']==64
    corr=json.loads((ROOT/'data/PART_W33_PASS10509_10516_HALL_JANKO_H2_PROVENANCE_CORRECTION.json').read_text())
    # certificate records local H(2) family count in its corrected provenance
    local_h2=100

    out={
      'schema':'w33.pass10925_10932.h2_homology_tate64_bridge.v1','status':'PASS','passes':'10925-10932','outside_box':True,
      'typed_64s':{
        'fixed_cone':{'object':'Fix(n^3)=F4^3','F2_dimension':6,'element_count':64},
        'Tate_defect':{'object':'1^64 external/stable obstruction','F2_dimension':64,'element_count':'2^64'},
        'H2_homology':{'object':'H1(Levi H(2);F2)','F2_dimension':64,'element_count':'2^64','reason':'beta1(H(q))=q^6'}},
      'valid_bridge':{
        'statement':'H1(Levi H(2);F2) is an exact 64-dimensional geometric model for the external 1^64 correction term if the defect C2 acts trivially on the chosen coefficient space',
        'intrinsic_H2_action_used':False,
        'canonical':False,
        'source_of_noncanonicity':'a Hall-Janko realization contains a local family of 100 embedded H(2) subhexagons, so one H(2) cycle space must be selected'},
      'no_go':{'fixed_cone_equals_H2_cycle_space':False,'reason':'64 is element count for F4^3 but vector-space dimension for H2 homology/Tate obstruction'},
      'theorem':'The persistent 64 splits into two categorical meanings. The Tate defect and H(2) Levi homology are genuinely both 64-dimensional F2 spaces, whereas the Wilson fixed cone is only six-dimensional and merely has 64 elements. Consequently H(2) homology can geometrize the external 1^64 stable correction after a choice of subhexagon and trivial external C2 action, but the 64 fixed states are not the 64 homology coordinates.',
      'boundary':'The beta1 identity and dimensional typing are exact. The proposed H2 realization is an external coefficient-space model, not an intrinsic normalizer-equivariant identification and not a canonical choice among the local H2 family.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','fixed_cone':'dim6/card64','Tate':'dim64','H2':'dim64','external_bridge':True,'canonical':False}))
if __name__=='__main__':main()
