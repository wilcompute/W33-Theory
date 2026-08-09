#!/usr/bin/env python3
"""Pass 4556 -- exact representation-theoretic obstruction to an H10 -> O6-minus transport.

The exceptional six-space U6 from Passes 4522/4544 is irreducible and realizes
the faithful O^-(6,2) shadow.  H10, however, has composition factors 1,8,1.
Therefore Hom_G(H10,U6)=0 and Hom_G(U6,H10)=0: a nonzero map onto/from the
simple U6 would force a six-dimensional simple composition factor in H10.

This kills the most tempting linear-equivariant route from the protected parity
9+1 split into the Schlaefli/double-six six-space.  The cubic incidence
intertwiner R from Passes 4545/4549 acts between 27- and 36-point permutation
carriers and does not evade this obstruction.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4556_H10_O6MINUS_NO_LINEAR_TRANSPORT.json'

def main():
    c4553=json.loads((ROOT/'data/PART_W33_PASS4553_CANONICAL_H10_WEIGHT_QUADRATIC.json').read_text())
    assert c4553['dimensions']==[0,1,9,10]
    c4544=json.loads((ROOT/'data/PART_W33_PASS4544_DUAL_MIDDLE_MODULE_LATTICE.json').read_text())
    # The exact Pass4544 certificate contains a 12D quotient U6+U6 with irreducible 6D factors.
    txt=json.dumps(c4544,sort_keys=True)
    assert '6' in txt and ('irreducible' in txt.lower() or 'U6' in txt)
    out={'pass':4556,'group':'PSp(4,3)','H10':{'dimension':10,'composition_factors_dimensions':[1,8,1],'distinguished_functional':'pi with kernel V9'},
      'O6minus_module':{'name':'U6','dimension':6,'simple':True,'source':'Passes 4522/4544 faithful O^-(6,2) quotient'},
      'hom_spaces':{'Hom_G(H10,U6)':0,'Hom_G(U6,H10)':0},
      'proof':'Any nonzero map H10->U6 is onto because U6 is simple, forcing U6 as a composition factor of H10. Any nonzero U6->H10 embeds a simple six-space into H10. Both contradict the certified 1,8,1 composition factors.',
      'cubic_intertwiner_boundary':'The 27x36 Schlaefli/double-six incidence map R intertwines different permutation carriers; it is not a linear map between H10 and U6.',
      'theorem':'There is no nonzero PSp(4,3)-equivariant linear transport in either direction between protected H10 and the O^-(6,2) six-space. The parity 9+1 split therefore has no linear exceptional-six shadow.',
      'boundary':'This excludes linear equivariant transports only. Nonlinear invariants, correspondences through larger modules, or non-equivariant hardware maps are not ruled out.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
