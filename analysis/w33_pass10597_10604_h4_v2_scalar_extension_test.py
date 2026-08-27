#!/usr/bin/env python3
"""Pass10597-10604: test extension of H1(Levi H4) ~= F2[V2] across F4^x=C3.

The internal scalar C3 acts trivially on PG(V2), hence trivially on the H(4)
point/line incidence geometry and therefore on its graph homology.  On the
vector set V2=F4^6 it fixes 0 and acts freely on the 4095 nonzero vectors in
scalar triples.  Thus the permutation module F2[V2] has C3-fixed dimension
1+4095/3=1366, while H1 has fixed dimension 4096.  Fixed-space dimension is a
module-isomorphism invariant, so the Pass10525 C13 isomorphism cannot extend.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10597_10604_H4_V2_SCALAR_EXTENSION_TEST.json'

def main():
    V=4**6;nonzero=V-1;proj=nonzero//3
    assert (V,nonzero,proj)==(4096,4095,1365)
    h1_fixed=4096
    perm_fixed=1+proj
    assert perm_fixed==1366 and h1_fixed!=perm_fixed
    out={
      'schema':'w33.pass10597_10604.h4_v2_scalar_extension_test.v1','status':'PASS','passes':'10597-10604',
      'scalar':'F4^x=C3',
      'H4_homology':{'dimension':4096,'scalar_action':'trivial because projective points and lines are scalar orbits','C3_fixed_dimension':h1_fixed},
      'F2_V2_permutation_module':{'set_size':V,'set_orbits':'1 fixed zero + 1365 scalar triples','C3_fixed_dimension':perm_fixed},
      'extension_to_C3':False,
      'canonical_replacement':'F2[V2]^C3 = F2[0] + F2[PG(V2)], dimension 1366, G2(4)-equivariant',
      'theorem':'The C13-equivariant H(4)-Levi-homology/F2[V2] isomorphism cannot extend over the intrinsic F4 scalar C3, because their C3-fixed dimensions are 4096 and 1366. Projectivization is the canonical full-G2(4) descendant.',
      'parallel_note':'Later independently frozen Pass10661-10668 reaches the same obstruction from the independent harmonic-operator lane.',
      'boundary':'Exact orbit/fixed-space argument. It does not weaken the C13 chain-resolution theorem.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','fixed_dims':[4096,1366],'extends':False}))
if __name__=='__main__':main()
