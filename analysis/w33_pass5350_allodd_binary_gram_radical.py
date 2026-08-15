#!/usr/bin/env python3
"""Pass5350: all-odd binary Gram/radical theorem for the footprint image.

Pass5267 proves over Z that
  F F^T = (q^2-1)I + (q-1)A_W + J.
For odd q both q^2-1 and q-1 are even, hence over F2
  F F^T = J.
This tiny reduction has strong consequences that were not previously frozen:
(1) ker(F^T) contains no odd-weight vector;
(2) for footprint code C=im(F^T), the induced dot product has rank exactly1;
(3) the radical C cap C^perp is precisely F^T(M_even), of dimension rank(F)-1;
(4) C is therefore a one-dimensional nonsingular extension of a totally
    self-orthogonal code, uniformly for every odd q.
Combined with C_W <= ker(F^T), the all-odd rank target says the *entire* even
kernel is exactly the W-line code. This is a sharper modular formulation of the
characteristic rank-complement law.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5350_ALLODD_BINARY_GRAM_RADICAL.json'

def row(q,rank=None):
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g and q%2==1
    rec={'q':q,'v':v,'f':f,'g':g,'binary_gram':'J_v','kernel_is_even':True}
    if rank is not None:
        rec.update(rank_F2=rank,footprint_code_dimension=rank,
                   radical_dimension=rank-1,nonsingular_quotient_dimension=1,
                   kernel_dimension=v-rank,
                   rank_equality=(rank==g),
                   line_code_dimension=1+f)
        if rank==g:assert v-rank==1+f
    return rec

def main():
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    A={str(q):row(q,r) for q,r in anchors.items()}
    # symbolic parity checks behind FF^T=J
    for q in range(3,32,2):
        assert (q*q-1)%2==0 and (q-1)%2==0 and q*q%2==1
    out={'pass':5350,'status':'THEOREM_ALLODD_BINARY_FOOTPRINT_GRAM_HAS_RANK_ONE_AND_IMAGE_HAS_CODIMENSION_ONE_RADICAL',
      'domain':'all odd prime powers q',
      'integer_gram':'FF^T=(q^2-1)I+(q-1)A_W+J',
      'binary_gram':'FF^T=J',
      'pairing_formula':'For point coefficient vectors x,y, <F^T x,F^T y> = parity(x) parity(y).',
      'kernel_parity':'If F^T x=0 then Jx=0, hence x has even Hamming weight. Thus ker(F^T) lies inside the even-weight point module.',
      'image_radical':'Let C=im(F^T) and M0 be the even-weight point module. Then Rad(C)=C cap C^perp=F^T(M0), with dim Rad(C)=rank(F)-1; C/Rad(C) is one-dimensional and nonsingular.',
      'allodd_target':'Since the binary W-line code C_W is already contained in ker(F^T), rank_2(F)=g is equivalent to ker(F^T)=C_W; Pass5350 adds that this sought kernel is necessarily an even submodule and the image is always an almost-self-orthogonal rank-one extension.',
      'anchors':A,
      'boundary':'This is an all-odd structural theorem but does not by itself prove rank_2(F)=g. Equality with the W-line code remains open for general odd q.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
