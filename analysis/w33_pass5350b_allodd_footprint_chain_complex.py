#!/usr/bin/env python3
"""Pass5350b: the odd-q footprint incidence matrix is a 2-periodic binary chain complex.

Let F be W-point x P-carrier incidence. A carrier is C_H=PG(H) union PG(H^perp)
for a nondegenerate 2-space H. Pass5267 gives FF^T=J mod2. This addendum proves
the complementary identity F^T F=0 mod2.

Indeed C_H cap C_K is the disjoint union of projective intersections
H cap K, H cap K^perp, H^perp cap K, H^perp cap K^perp. Orthogonal
complementation gives equal dimensions in the first/fourth pair and in the
second/third pair, so the total number of projective points is even (the H=K
diagonal has 2(q+1), also even).

Every carrier column has even weight, hence F maps the P-space U into the even
point module V0. On V0, J=0, so both composites vanish:
  U --F--> V0 --F^T--> U,   F^T F=0,
  V0 --F^T--> U --F--> V0, FF^T|V0=0.
If r=rank_2(F), the point-side homology has dimension v-2r. Since r<=g,
  dim H_point >= v-2g = q^2+1,
and equality is equivalent to the all-odd rank theorem r=g.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5350B_ALLODD_FOOTPRINT_CHAIN_COMPLEX.json'

def row(q,r=None):
    assert q%2==1
    v=(q+1)*(q*q+1);n=q*q*(q*q+1)//2;f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g and v-2*g==q*q+1
    x={'q':q,'point_dimension':v,'even_point_dimension':v-1,'carrier_dimension':n,
       'rank_upper_bound_g':g,'minimal_point_homology_dimension':q*q+1,
       'minimal_carrier_homology_dimension':n-2*g}
    if r is not None:
        x.update(rank_F2=r,point_homology_dimension=v-2*r,carrier_homology_dimension=n-2*r,
                 rank_equality=(r==g))
        if r==g:assert v-2*r==q*q+1
    return x

def main():
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    rows={str(q):row(q,anchors.get(q)) for q in (3,5,7,9,11,13,17,19,25)}
    out={'pass':'5350b','status':'THEOREM_ALLODD_BINARY_FOOTPRINT_TWO_PERIODIC_CHAIN_COMPLEX',
      'domain':'all odd prime powers q',
      'identities':['F^T F=0 over F2','F F^T=J over F2','FF^T vanishes on the even point module V0'],
      'complex':'U_Pcarriers --F--> V0_even_points --F^T--> U_Pcarriers, with both consecutive composites zero.',
      'point_homology_dimension':'dim H_V = v - 2 rank_2(F)',
      'carrier_homology_dimension':'dim H_U = n_P - 2 rank_2(F)',
      'allodd_lower_bound':'dim H_V >= q^2+1 because rank_2(F)<=g=q(q^2+1)/2.',
      'rank_equivalence':'rank_2(F)=g iff dim H_V=q^2+1.',
      'geometric_parity_proof':'For carriers C_H and C_K, dimensions of H∩K and H^perp∩K^perp agree, as do H∩K^perp and H^perp∩K; paired projective intersection sizes make |C_H∩C_K| even.',
      'anchors':rows,
      'boundary':'This reframes but does not prove the all-odd rank theorem. Identifying the q^2+1-dimensional minimal homology module remains the key modular target.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
