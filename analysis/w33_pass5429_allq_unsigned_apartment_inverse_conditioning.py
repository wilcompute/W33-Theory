#!/usr/bin/env python3
"""Pass5429: exact inverse and condition number of unsigned apartment visibility.

Pass5404 gives K=B B^T on the N flag coordinates with primitive eigenvalues
  l0 = 8 q^4,
  l+ = 2 q^2(q-1)(q+1+sqrt(2q)),
  lm = 2 q^2(q-1)^2,
  l- = 2 q^2(q-1)(q+1-sqrt(2q)),
  lt = (q-1)^2(q^2+1).
All are positive.  The terminal eigenvalue lt is the smallest for every q>=2,
while l0 is the largest.  Therefore
  kappa(K)=8q^4/((q-1)^2(q^2+1))
and kappa(B)=sqrt(kappa(K)).
The inverse is the corresponding primitive-idempotent spectral sum, and
B^+=B^T K^{-1} gives canonical minimum-norm unsigned apartment tomography of
an arbitrary real flag signal.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5429_ALLQ_UNSIGNED_APARTMENT_INVERSE_CONDITIONING.json'
ANCHORS=(2,3,4,5,7,8,9,11,13)

def row(q:int)->dict:
    assert q>=2
    N=(q+1)**2*(q*q+1)
    l0=8*q**4
    lp=2*q*q*(q-1)*(q+1+math.sqrt(2*q))
    lm=2*q*q*(q-1)**2
    ln=2*q*q*(q-1)*(q+1-math.sqrt(2*q))
    lt=(q-1)**2*(q*q+1)
    # max: sqrt(2q)<=q for q>=2, so lp < 8q^4.  min terminal verified
    # algebraically by squaring the positive comparison:
    # (q^3+3q^2-q+1)^2-8q^5=(q^2+1)((q-1)^4+2q(q^2+1))>0.
    assert l0>=max(lp,lm,ln,lt)-1e-9
    assert lt<=min(lp,lm,ln)+1e-9
    kg=l0/lt
    return {'q':q,'flags':N,'lambda_max':l0,'lambda_min':lt,
      'gram_condition_number':kg,'incidence_condition_number':math.sqrt(kg)}

def main():
    rows={str(q):row(q) for q in ANCHORS}
    q3=rows['3'];assert q3['lambda_max']==648 and q3['lambda_min']==40
    out={
      'pass':5429,'status':'THEOREM_ALLQ_UNSIGNED_APARTMENT_CANONICAL_INVERSE_AND_CONDITIONING',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'input':'Pass5404 exact five-eigenvalue spectrum of K=B B^T.',
      'inverse':'K^{-1}=E0/l0 + E+/l+ + Em/lm + E-/l- + Et/lt; B^+=B^T K^{-1}.',
      'eigenvalues':[
        'l0=8q^4','l+=2q^2(q-1)(q+1+sqrt(2q))','lm=2q^2(q-1)^2',
        'l-=2q^2(q-1)(q+1-sqrt(2q))','lt=(q-1)^2(q^2+1)'],
      'extremes':'For every q>=2, l0 is largest and lt is smallest.',
      'minimum_proof':'After division by q-1, l- >= lt reduces to q^3+3q^2-q+1 >= 2q^2 sqrt(2q). Squaring is safe and the difference factors as (q^2+1)((q-1)^4+2q(q^2+1))>0.',
      'condition_number_gram':'8q^4/((q-1)^2(q^2+1))',
      'condition_number_B':'sqrt(8q^4/((q-1)^2(q^2+1)))',
      'tomography':'Because B has full row rank, every real flag signal x has canonical minimum-l2 apartment coefficients B^T K^{-1}x.',
      'anchors':rows,
      'boundary':'This is real linear inversion/conditioning, not a statement about binary decoding or robustness to a specified physical noise model.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
