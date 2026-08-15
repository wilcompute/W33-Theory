#!/usr/bin/env python3
"""Pass5378: the all-odd footprint image is a classical minimum-word-generated code.

Pass5376 identifies the binary footprint image with the dual of the W(3,q)
point-line incidence code:

    C_F := im_2(F) = C_W^perp,
    dim C_F = g=q(q^2+1)/2.

Kim--Mellinger--Storme, Designs Codes Cryptogr. 42 (2007), record that the
binary LDPC code defined by W(q), i.e. the kernel of its line-point incidence
matrix, has minimum distance 2(q+1). This LDPC code is exactly C_W^perp.

Each footprint column is the indicator of a P-component block H union H^perp
and has weight 2(q+1). Hence every footprint column is a minimum codeword.
Since the columns span C_F by definition and Pass5376 proves that span is all
of C_W^perp, one PSp4(q)-orbit of minimum words generates the full code.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5378_FOOTPRINT_CODE_MINIMUM_ORBIT.json'

def row(q:int)->dict[str,int]:
    assert q%2==1 and q>=3
    n=(q+1)*(q*q+1);k=q*(q*q+1)//2;d=2*(q+1)
    b=q*q*(q*q+1)//2
    assert d<n and 0<k<n
    return {'q':q,'length':n,'dimension':k,'minimum_distance':d,
      'minimum_generator_orbit_size':b,'minimum_generator_weight':d}

def main()->None:
    rows={str(q):row(q) for q in (3,5,7,9,11,13,17,19,25,27,49)}
    out={'pass':5378,'status':'THEOREM_ALLODD_FOOTPRINT_CODE_PARAMETERS_AND_MINIMUM_ORBIT',
      'domain':'all odd prime powers q',
      'code':'C_F=im_2(F)=C_W^perp',
      'parameters':'[(q+1)(q^2+1), q(q^2+1)/2, 2(q+1)]_2',
      'minimum_orbit':'The q^2(q^2+1)/2 footprint/P-component columns each have weight 2(q+1), hence are minimum codewords; their span is the entire code.',
      'primary_distance_source':{
        'authors':'Jon-Lark Kim, Keith E. Mellinger, Leo Storme',
        'title':'Small weight codewords in LDPC codes defined by (dual) classical generalized quadrangles',
        'journal':'Designs, Codes and Cryptography 42 (2007), 73--92',
        'doi':'10.1007/s10623-006-9017-6',
        'result_used':'The binary LDPC code defined by W(q) has minimum distance 2(q+1).'
      },
      'sample_parameters':rows,
      'boundary':'This proves the exact footprint-image minimum distance and that the P-component orbit is a generating orbit of minimum words. It does not assert that these are all minimum codewords unless a separate classification is invoked.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
