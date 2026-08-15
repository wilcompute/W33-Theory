#!/usr/bin/env python3
"""Pass5350b: odd-q footprint incidence gives a 2-periodic binary chain complex.

Let F be W-point x P-carrier incidence. A carrier is C_H=PG(H) union PG(H^perp)
for a nondegenerate 2-space H. Pass5267 gives FF^T=J mod2. This addendum proves
F^T F=0 mod2: the four projective intersections between H,H^perp and K,K^perp
occur in equal-size orthogonal-complement pairs, so every two carrier columns
have even intersection (and each carrier itself has even size 2(q+1)).

Every column has even weight, so F maps the P-carrier space U into the even point
module V0. Since J vanishes on V0, both composites vanish:
  U --F--> V0 --F^T--> U,
  V0 --F^T--> U --F--> V0.

Rank bookkeeping matters: if r=rank(F), then FF^T=J has rank1, so
rank(F^T|V0)=r-1, while rank(F:U->V0)=r. Thus
  dim H_point = v-2r,
  dim H_carrier = n_P-2r+1.
Pass5376 subsequently closes r=g and identifies im F=C_W^perp and ker F^T=C_W.
Therefore H_point is canonically C_W/C_W^perp, has dimension q^2+1, and is
exactly the logical quotient of the Pass5379 binary CSS family.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5350B_ALLODD_FOOTPRINT_CHAIN_COMPLEX.json'

def row(q):
    assert q%2==1
    v=(q+1)*(q*q+1);n=q*q*(q*q+1)//2;f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g and v-2*g==q*q+1
    return {'q':q,'point_dimension':v,'even_point_dimension':v-1,'carrier_dimension':n,
      'rank_F2':g,'rank_FT_on_even_points':g-1,
      'point_homology_dimension':v-2*g,'point_homology_expected':q*q+1,
      'carrier_homology_dimension':n-2*g+1}

def main():
    rows={str(q):row(q) for q in (3,5,7,9,11,13,17,19,25)}
    out={'pass':'5350b','status':'THEOREM_ALLODD_FOOTPRINT_CHAIN_COMPLEX_AND_CSS_LOGICAL_HOMOLOGY',
      'domain':'all odd prime powers q',
      'identities':['F^T F=0 over F2','F F^T=J over F2','FF^T vanishes on V0'],
      'complex':'U_Pcarriers --F--> V0_even_points --F^T--> U_Pcarriers, with both consecutive composites zero.',
      'rank_restriction':'rank(F)=g and rank(F^T|V0)=g-1; the latter loses the unique odd point-input mode detected by FF^T=J.',
      'point_homology':'H_V=ker(F^T|V0)/im(F)=C_W/C_W^perp, dimension q^2+1.',
      'carrier_homology':'H_U=ker(F)/im(F^T|V0), dimension n_P-2g+1.',
      'css_bridge':'Pass5379 uses C_W^perp as both binary X- and Z-check space. Its logical quotient C_W/C_W^perp is exactly this point-side homology, so the CSS logical dimension k=q^2+1 has a canonical chain-homology realization.',
      'geometric_parity_proof':'For C_H and C_K, dim(H∩K)=dim(H^perp∩K^perp) and dim(H∩K^perp)=dim(H^perp∩K); paired projective intersection sizes make |C_H∩C_K| even.',
      'rows':rows,
      'dependencies':'Uses Pass5267 FF^T identity and the later Pass5376 theorem im F=C_W^perp, ker F^T=C_W, rank F=g.',
      'boundary':'Exact binary homological/code statement. It does not identify the logical quotient with a physical topological phase or fault-tolerant hardware.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
