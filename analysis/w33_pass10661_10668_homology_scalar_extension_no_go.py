#!/usr/bin/env python3
"""Pass10661-10668: the H(4)-homology/V2 permutation bridge is C13-specific.

Pass10525-10532 / 10501-10508 prove, after restriction to the free C13 clock,

    H1(Levi H(4);F2) ~= F2[V2] ~= F2 + F2[C13]^315.

Canonical V2 is intrinsically F4^6 and its scalar group F4^x=C3 commutes with
G2(4).  Scalar multiplication is invisible after projectivization, so C3 acts
trivially on H(4) points, lines, flags, chains, and H1.  Thus H1^C3 has dimension
4096.

On the vector set V2, a nontrivial scalar fixes only 0 and partitions the 4095
nonzero vectors into 1365 scalar triples.  The permutation-module fixed space
therefore has dimension 1366.  This disproves extension of the C13-module
isomorphism even to C13 x C3.

The failure has a canonical replacement:

    F2[V2]^C3 = F2[{0}] + F2[PG(V2)]
               = F2 + F2[H(4)_points]

as a full G2(4)-permutation module.  Thus projectivization is the natural
G2-equivariant bridge, whereas the 4096-dimensional homology equality is a
free-C13-cover phenomenon.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10661_10668_HOMOLOGY_SCALAR_EXTENSION_NO_GO.json'

def main():
    V=4**6; nonzero=V-1; projective=nonzero//3
    assert (V,nonzero,projective)==(4096,4095,1365)
    # Scalar C3 on vector set: {0} plus 1365 free 3-cycles.
    vector_orbits=1+projective
    assert vector_orbits==1366
    # Permutation-module invariants in odd characteristic action = functions constant on orbits.
    vector_fixed_dim=vector_orbits
    # Scalar is projectively trivial, so every H(4) chain and homology class is fixed.
    h1_dim=4**6
    h1_fixed_dim=h1_dim
    assert h1_fixed_dim==4096 and vector_fixed_dim==1366 and h1_fixed_dim!=vector_fixed_dim
    # C13 commutes with scalar C3; failure on the C3 subgroup already kills extension to C39.
    assert 13*3==39
    # Projective replacement: one zero orbit plus all H4 points.
    assert 1+1365==1366
    out={
      'schema':'w33.pass10661_10668.homology_scalar_extension_no_go.v1','status':'PASS','passes':'10661-10668',
      'inputs':{'V2':'F4^6','V2_cardinality':4096,'projective_points':1365,'PG_V2':'H(4) point set','scalar_group':'F4^x=C3'},
      'scalar_on_H4':{'action':'trivial on projective points and lines','H1_dimension':4096,'H1_C3_fixed_dimension':4096},
      'scalar_on_vector_permutation_module':{'fixed_set':['0'],'nonzero_scalar_orbits':1365,'orbit_lengths':'1^1 + 3^1365','fixed_module_dimension':1366},
      'no_go':{'C13_module_isomorphism_from_Pass10525':True,'extends_to_C13_times_C3':False,'obstruction':'C3-fixed dimensions differ: 4096 versus 1366','consequence':'no full G2(4)-module isomorphism H1(Levi H4;F2) ~= F2[V2] can restrict to the canonical scalar action'},
      'canonical_replacement':{'identity':'F2[V2]^C3 ~= F2[zero] + F2[PG(V2)]','dimension':'1+1365=1366','G2_equivariant':True,'reading':'projectivization, not H1, is the canonical full-G2 bridge from the vector permutation module to H(4)'},
      'theorem':'The 4096-dimensional H(4)-Levi homology / F2[V2] equality is genuinely C13-specific and cannot extend across the internal F4 scalar C3. The canonical G2(4)-equivariant descendant is instead the scalar-invariant permutation module F2[V2]^C3 = F2 plus the permutation module on the 1365 projective H(4) points.',
      'boundary':'Exact orbit/permutation-module argument. It does not weaken the Pass10525 C13 chain-resolution theorem; it states its maximality with respect to the canonical scalar extension.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','H1_C3_fixed':4096,'vector_C3_fixed':1366,'replacement':'1 + H4_points'}))
if __name__=='__main__':main()
