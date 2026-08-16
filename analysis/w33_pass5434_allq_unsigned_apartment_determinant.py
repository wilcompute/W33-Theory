#!/usr/bin/env python3
"""Pass5434: exact determinant/volume invariant of unsigned apartment visibility.

Using the Pass5404 spectrum of K=B B^T, the conjugate radical eigenvalues occur
with equal multiplicity f. Their product is rational:

 l+ l- = 4 q^4 (q-1)^2 (q^2+1).

Writing P=(q+1)(q^2+1) for the number of W-points,
f=q(q+1)^2/2, g=q(q^2+1)/2, one obtains

 det(K)=2^(2P+1) q^(4P)
        (q-1)^(2f+4g+2q^4)
        (q^2+1)^(f+q^4).

Thus the irrational sqrt(2q) sectors cancel exactly from the global volume.
At q=3 this simplifies to 2^456 3^160 5^105.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5434_ALLQ_UNSIGNED_APARTMENT_DETERMINANT.json'
ANCHORS=(2,3,4,5,7,8,9,11,13)

def exponents(q:int)->dict:
    P=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert P==1+f+g
    return {'q':q,'W_points':P,'f':f,'g':g,
      'power_2':2*P+1,'power_q':4*P,
      'power_q_minus_1':2*f+4*g+2*q**4,
      'power_q2_plus_1':f+q**4}

def main():
    rows={str(q):exponents(q) for q in ANCHORS}
    q3=rows['3'];assert (q3['power_2'],q3['power_q'],q3['power_q_minus_1'],q3['power_q2_plus_1'])==(81,160,270,105)
    # q=3: q-1=2 and q^2+1=10 add another 270+105 powers of2 and 105 powers of5.
    assert 81+270+105==456
    q5=rows['5'];assert (q5['power_2'],q5['power_q'],q5['power_q_minus_1'],q5['power_q2_plus_1'])==(313,624,1690,715)
    out={
      'pass':5434,'status':'THEOREM_ALLQ_UNSIGNED_APARTMENT_GRAM_DETERMINANT',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'conjugate_pair_product':'l+ l-=4q^4(q-1)^2(q^2+1)',
      'closed_form':'det(BB^T)=2^(2P+1) q^(4P) (q-1)^(2f+4g+2q^4) (q^2+1)^(f+q^4), P=(q+1)(q^2+1).',
      'q3_factorization':'2^456 * 3^160 * 5^105',
      'q5_factorization':'2^4408 * 5^624 * 13^715',
      'interpretation':'The sqrt(2q) quadratic spectral pair contributes an integer norm factor because its two conjugate sectors have equal multiplicity f.',
      'anchors':rows,
      'boundary':'This determinant is a real/characteristic-zero Gram-volume invariant. It is not the binary determinant or a code weight enumerator.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
