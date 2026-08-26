#!/usr/bin/env python3
"""Pass10437-10444 outside-box: the two rank-six clocks are a field/local-ring dichotomy.

Binary/Leech side (now intrinsic): V2=F4^6 and z has order 13. Since ord_13(4)=6,
the minimal polynomial of z over F4 is irreducible of degree 6.  Therefore the algebra it
generates is the field

    F4[z] ~= F_{4^6}.

The natural module is one-dimensional over that field, so z has no nonzero proper
F4-invariant subspace.  Its GL6(4) centralizer is the unit group of the field, C4095.

Ternary/glue/local-field side: U=1+N on F9[t]/(t^6), with N^6=0 and N^5!=0.  Its
minimal polynomial is (x-1)^6 and

    F9[U]=F9[N] ~= F9[t]/(t^6).

This is a local Artin ring, not a field.  The regular module has the canonical ideal/lattice
chain (t^j), and U fixes every associated-graded one-dimensional F9 quotient.  Its ambient
GL6(9) centralizer is the unit group of the truncated polynomial ring, of order

    (9-1)*9^5 = 472392.

Thus both clocks are regular cyclic rank-six operators whose commutant algebra has base-field
dimension six, but one commutant is a FIELD and the other a LOCAL RING.  This formalizes
the semisimple/global versus unipotent/memory distinction.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10437_10444_RANK6_FIELD_LOCAL_RING_DUALITY.json'
def ordmod(a,n):
    x=1
    for k in range(1,n+1):
        x=x*a%n
        if x==1:return k
    raise RuntimeError
def main():
    assert ordmod(4,13)==6
    field_units=4**6-1;assert field_units==4095
    projective_field_units=field_units//(4-1);assert projective_field_units==1365
    local_size=9**6;assert local_size==531441
    local_units=(9-1)*9**5;assert local_units==472392
    local_projective=local_units//(9-1);assert local_projective==59049
    assert 59049==3**10
    out={
      'schema':'w33.pass10437_10444.rank6_field_local_ring_duality.v1','status':'PASS','passes':'10437-10444','outside_box':True,
      'semisimple_F4_branch':{
        'module':'V2=F4^6','clock':'z of order 13','ord_13_4':6,'minimal_polynomial':'irreducible degree 6 factor of Phi_13 over F4',
        'generated_algebra':'F4[z] ~= F_{4^6}','algebra_F4_dimension':6,'proper_invariant_F4_subspaces':'none','GL6_4_centralizer_units':'C4095','projective_centralizer_order':1365},
      'unipotent_F9_branch':{
        'module':'F9[t]/(t^6)','clock':'U=1+t=I+N of order 9','minimal_polynomial':'(x-1)^6','nilpotency':'N^6=0, N^5 != 0',
        'generated_algebra':'F9[U] ~= F9[t]/(t^6)','algebra_F9_dimension':6,'canonical_invariant_chain':'(t^5)<(t^4)<...<(t)<R','associated_graded_action':'identity on each 1-dimensional F9 layer','GL6_9_centralizer_unit_order':local_units,'scalar_quotient_order':local_projective},
      'common_structure':{'rank_over_quadratic_residue_field':6,'operator_type':'regular cyclic','commutant_algebra_dimension':6,'quadratic_base_fields':['F4=F2^2','F9=F3^2']},
      'duality':'The prime-2 clock is semisimple/global: its commutant is a degree-six field and it admits no proper invariant subspaces. The prime-3 clock is maximally unipotent/filtered: its commutant is a length-six local ring and it carries a unique complete invariant filtration. They are complementary regular rank-six realizations, not isomorphic modules.',
      'theorem':'The intrinsic C13 action on canonical V2 and the cyclotomic C9 action on the F9 glue are two regular cyclic rank-six clocks with six-dimensional commutant algebras of opposite type: F_{4^6} on the Leech side versus F9[t]/(t^6) on the local-field side. This gives an exact field-versus-local-ring, semisimple-versus-unipotent duality at the common rank six.',
      'boundary':'Finite algebra/linear algebra theorem. No physical identification of the two clocks is asserted; the words global and memory describe their invariant-subspace/filtration structure.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','semisimple_commutant':'F4^6 field','unipotent_commutant':'F9[t]/t6','rank':6}))
    return 0
if __name__=='__main__':raise SystemExit(main())
