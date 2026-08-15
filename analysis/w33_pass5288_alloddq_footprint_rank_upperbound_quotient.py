#!/usr/bin/env python3
"""Pass5288: all-odd-q footprint rank upper bound and exact quotient target.

Let V be the 4D symplectic space, L a totally isotropic 2-space (a W-line), and
H a nondegenerate 2-space. A P-component carrier is the projective point set of
H union H^perp. Since L=L^perp,

  (L + H^perp)^perp = L cap H,

so dimension counting gives

  dim(L cap H^perp) = dim(L cap H).

Because H is nondegenerate it cannot equal the totally isotropic L; these
intersection dimensions are 0 or 1. Thus every W-line meets every P carrier in
0 or 2 projective points. Over F2, every W-line incidence row therefore lies in
ker(F^T).

For odd q, Pass5130 gives the binary W point-line incidence rank
  1 + q(q+1)^2/2 = 1+f.
The point permutation space has dimension
  v=(q+1)(q^2+1)=1+f+g,
where g=q(q^2+1)/2. Hence
  rank_2(F) <= g.
At q=3,5,7,9 the exact repo ranks 15,65,175,369 equal g, so the footprint map
saturates this universal upper bound at four anchors.

The remaining all-odd-q equality theorem is precisely injectivity of the induced
map from the g-dimensional quotient of the point module by the W-line code.
The known modulo-2 Sp/O(5) rank-3 module literature is the correct framework for
identifying this quotient, but this pass does not silently import a theorem that
has not been matched objectwise to the footprint map.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5288_ALLODDQ_FOOTPRINT_RANK_UPPERBOUND_QUOTIENT.json'

def dims(q):
    v=(q+1)*(q*q+1)
    f=q*(q+1)**2//2
    g=q*(q*q+1)//2
    assert v==1+f+g
    return v,f,g

def main():
    anchors={3:15,5:65,7:175,9:369}
    rows={}
    for q in (3,5,7,9,11,13):
        v,f,g=dims(q)
        rows[str(q)]={'v':v,'line_code_dimension':1+f,'quotient_dimension_g':g}
        if q in anchors: assert anchors[q]==g
    out={
      'pass':5288,
      'status':'THEOREM_ALLODDQ_FOOTPRINT_RANK_UPPERBOUND_AND_QUOTIENT_REDUCTION',
      'domain':'odd prime powers q',
      'carrier_line_parity_theorem':'For every totally isotropic W-line L and every nondegenerate 2-space H, dim(L cap H)=dim(L cap H^perp), so L meets H union H^perp in 0 or 2 projective points.',
      'kernel_inclusion':'binary W-line incidence code is contained in ker(F^T)',
      'line_code_dimension':'1 + q(q+1)^2/2',
      'point_space_dimension':'(q+1)(q^2+1)',
      'rank_upper_bound':'rank_2(F) <= g = q(q^2+1)/2',
      'equality_anchors':{str(q):r for q,r in anchors.items()},
      'remaining_target':'Prove the induced footprint map on the g-dimensional point-module quotient by the W-line code is injective for every odd q.',
      'module_literature_context':['Lataille-Sin-Tiep (J. Algebra 268, 2003) determine the modulo-2 rank-3 permutation-module lattice for odd-characteristic symplectic groups and analogous O(5,q) modules.','Bagchi-Brouwer-Wilbrink (Geom. Dedicata 39, 1991) determine dimensions of related binary line/neighborhood codes for Sp(4,q) and dual O(5,q).'],
      'dimension_table':rows,
      'boundary':'The all-odd upper bound is proved. Equality rank_2(F)=g is exact only at q=3,5,7,9 here; no all-odd equality or footprint-distance theorem is promoted.'
    }
    OUT.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
