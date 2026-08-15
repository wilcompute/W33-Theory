#!/usr/bin/env python3
"""Pass5379: exact all-odd binary CSS family from the footprint/line-code sandwich.

Pass5376 identifies C_F=im_2(F)=C_W^perp.  Lataille--Sin--Tiep's complete
char-2 point-module lattice gives C_W^perp <= C_W for m=2.  Therefore C_F is
self-orthogonal and may be used as both the X- and Z-check row space of a CSS
stabilizer code.

Length:
    n=(q+1)(q^2+1).
Check rank:
    dim C_F=g=q(q^2+1)/2.
Logical dimension:
    k=n-2g=q^2+1.

Bagchi--Sastry prove for the regular generalized quadrangle W(3,q) that the
line code C_W has minimum distance q+1 and its minimum words are exactly line
incidence vectors.  A W-line is not in C_F=C_W^perp: choose any other W-line
meeting it in one point, giving odd inner product.  Hence

    d(C_W \ C_F)=q+1.

Since C_F^perp=C_W, the X and Z logical distances coincide, giving

    [[(q+1)(q^2+1), q^2+1, q+1]]_2

for every odd prime power q.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5379_ALLODD_BINARY_CSS_POINT_CODE.json'

def row(q:int)->dict[str,int]:
    n=(q+1)*(q*q+1); g=q*(q*q+1)//2; k=n-2*g; d=q+1
    assert k==q*q+1
    return {'q':q,'n':n,'stabilizer_rank_each':g,'k':k,'dX':d,'dZ':d,'d':d}

def main()->None:
    rows={str(q):row(q) for q in (3,5,7,9,11,13,17,19,25,27,49)}
    out={'pass':5379,'status':'THEOREM_ALLODD_BINARY_CSS_POINT_CODE_FAMILY',
      'domain':'all odd prime powers q',
      'css_parameters':'[[(q+1)(q^2+1), q^2+1, q+1]]_2',
      'construction':'Use C_F=C_W^perp as both X- and Z-check row spaces; LST gives C_W^perp<=C_W=(C_W^perp)^perp.',
      'distance_argument':'Bagchi--Sastry give d(C_W)=q+1 with minimum words exactly W-lines. Every W-line is outside C_W^perp because it has odd intersection with an intersecting W-line. Thus dX=dZ=q+1.',
      'samples':rows,
      'separation':'This is a binary point-code CSS family. It is distinct from the project ternary edge CSS [[240,81,3]]_3 and no equivalence between them is asserted.',
      'primary_sources':[
        'Lataille--Sin--Tiep, J. Algebra 268 (2003): complete characteristic-2 point-module lattice and C_W^perp<=C_W for m=2.',
        'Bagchi--Sastry, Geometriae Dedicata 27 (1988), DOI 10.1007/BF00181609: minimum weight q+1 of the regular generalized-polygon line code and minimum words are lines.'
      ],
      'boundary':'This determines the abstract CSS parameters. It does not supply a fault-tolerant circuit, decoding threshold, or hardware implementation for the binary family.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
