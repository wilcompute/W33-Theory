#!/usr/bin/env python3
"""Pass4857 — rational splitting of the 1080-minimum orbital algebras.

This is a cross-certificate over the exact Pass4850 center/block data.  The full
PGSp action is the already-certified W(E6) action.  Benard's classical theorem
on exceptional Weyl groups gives Schur index one for the rational W(E6)
characters, so the PGSp rational simple factors are split matrix algebras.

For the index-two PSp subgroup, restrict those rational W(E6) modules.  Whenever
a restriction has quadratic endomorphism field K=Q(sqrt(-3)), the same rational
module is explicitly a K-vector space of the required degree; hence the
corresponding central-simple component embeds in End_K(V) with equal dimension
and is M_n(K), not a division algebra.  Pass4850's generic-center factor
exponents then determine the full rational product uniquely.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/'data/PART_W33_PASS4850_LEVI_MINIMUM_ORBITAL_WEDDERBURN.json'
OUT=ROOT/'data/PART_W33_PASS4857_RATIONAL_ORBITAL_BLOCKS.json'

def main()->int:
    old=json.loads(IN.read_text())
    assert old['PSp']['orbital_dimension']==59 and old['PSp']['center_dimension']==15
    assert old['PGSp']['orbital_dimension']==49 and old['PGSp']['center_dimension']==13
    assert old['PSp']['complex_Wedderburn']=='C^7 x M2(C)^4 x M3(C)^4'
    assert old['PGSp']['complex_Wedderburn']=='C^6 x M2(C)^4 x M3(C)^3'
    assert old['PSp']['rational_center']=='Q^9 x Q(sqrt(-3))^3'
    assert old['PGSp']['rational_center']=='Q^13'
    # Dimension and center checks for the claimed rational products.
    pg_dim=6 + 4*4 + 3*9
    p_dim=3 + 2*2 + 2*4 + 2*4 + 4*9  # Q^3,K^2,M2(Q)^2,M2(K),M3(Q)^4; [K:Q]=2
    assert pg_dim==49 and p_dim==59
    out={
      'pass':4857,
      'PGSp':{
        'group':'PGSp(4,3) = W(E6) on the certified 36-root/double-six carrier',
        'rational_Wedderburn':'Q^6 x M2(Q)^4 x M3(Q)^3',
        'all_noncommutative_blocks_split':True,
        'splitting_certificate':'Benard Schur-index-one theorem for exceptional Weyl groups, applied to the certified W(E6) action; Pass4850 supplies the block multiplicities and Q^13 center.',
        'dimension_Q':pg_dim},
      'PSp':{
        'field_K':'Q(sqrt(-3))',
        'rational_Wedderburn':'Q^3 x K^2 x M2(Q)^2 x M2(K) x M3(Q)^4',
        'all_noncommutative_blocks_split_over_their_centers':True,
        'dimension_Q':p_dim,
        'center':'Q^9 x K^3',
        'quadratic_center_blocks':'two scalar K factors plus one M2(K) factor',
        'splitting_certificate':'Restrict the Q-realizable W(E6) modules to the index-two PSp subgroup. For each quadratic-central restriction the commuting field K acts on the same rational module, making it a K-vector space of the exact matrix degree. The central-simple image therefore has full dimension n^2 over K inside End_K(V), forcing M_n(K), not a division algebra.'},
      'complexification_check':{
        'PSp':'Q^3 + K^2 -> C^7; M2(Q)^2 + M2(K) -> M2(C)^4; M3(Q)^4 -> M3(C)^4',
        'PGSp':'Q^6 -> C^6; M2(Q)^4; M3(Q)^3'},
      'external_prior_art':{
        'Benard_1971':'M. Benard, On the Schur indices of characters of the exceptional Weyl groups, Annals of Mathematics 94 (1971), 89-107.',
        'scope':'Schur-index theorem is classical prior art; the new repo result is its application to the explicitly reconstructed Pass4850 orbital algebra and the exact PSp/PGSp block allocation.'},
      'theorem':'Every noncommutative rational simple factor of the Pass4850 orbital algebras is split over its center. PGSp gives Q^6 x M2(Q)^4 x M3(Q)^3. PSp gives Q^3 x Q(sqrt(-3))^2 x M2(Q)^2 x M2(Q(sqrt(-3))) x M3(Q)^4.',
      'boundary':'This is an exact rational-algebra decomposition using Pass4850 finite structure plus Benard Schur-index prior art. It is not a new proof of Benard’s Weyl-group theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
