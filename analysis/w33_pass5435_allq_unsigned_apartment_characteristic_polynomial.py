#!/usr/bin/env python3
"""Pass5435: integral characteristic polynomial for unsigned apartment visibility.

Pass5404's only irrational eigenvalues are
  l±=2q^2(q-1)(q+1±sqrt(2q)),
with equal multiplicity f=q(q+1)^2/2.  They are the two roots of

 Q_q(x)=x^2-4q^2(q-1)(q+1)x+4q^4(q-1)^2(q^2+1).

Hence the full characteristic polynomial of K=B B^T is

 (x-8q^4)
 Q_q(x)^f
 (x-2q^2(q-1)^2)^(2g)
 (x-(q-1)^2(q^2+1))^(q^4),

g=q(q^2+1)/2.  Thus the apparent quadratic field is paired exactly into an
integral polynomial.  For even prime powers q=2^e, the radical sqrt(2q) is
rational iff e is odd; for odd prime powers it is always irrational.
"""
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5435_ALLQ_UNSIGNED_APARTMENT_CHARACTERISTIC_POLYNOMIAL.json'
ANCHORS=(2,3,4,5,7,8,9,11,13,16,32)

def row(q:int)->dict:
    f=q*(q+1)**2//2;g=q*(q*q+1)//2;N=(q+1)**2*(q*q+1)
    s=4*q*q*(q-1)*(q+1);p=4*q**4*(q-1)**2*(q*q+1)
    total=1+2*f+2*g+q**4
    assert total==N
    radical=2*q;root=int(math.isqrt(radical));rational=(root*root==radical)
    return {'q':q,'flags':N,'f':f,'g':g,
      'quadratic_trace':s,'quadratic_norm':p,
      'sqrt_2q_rational':rational}

def main():
    rows={str(q):row(q) for q in ANCHORS}
    assert rows['3']['flags']==160 and not rows['3']['sqrt_2q_rational']
    assert rows['8']['sqrt_2q_rational'] and rows['32']['sqrt_2q_rational']
    assert not rows['4']['sqrt_2q_rational'] and not rows['16']['sqrt_2q_rational']
    out={
      'pass':5435,'status':'THEOREM_ALLQ_UNSIGNED_APARTMENT_INTEGRAL_CHARACTERISTIC_POLYNOMIAL',
      'domain':'finite generalized quadrangles GQ(q,q), q>1',
      'quadratic_factor':'Q_q(x)=x^2-4q^2(q-1)(q+1)x+4q^4(q-1)^2(q^2+1)',
      'characteristic_polynomial':'(x-8q^4) Q_q(x)^f (x-2q^2(q-1)^2)^(2g) (x-(q-1)^2(q^2+1))^(q^4)',
      'multiplicities':'f=q(q+1)^2/2, g=q(q^2+1)/2; total degree equals N=(q+1)^2(q^2+1).',
      'field_classification':'For q=2^e, sqrt(2q) is rational exactly when e is odd. For odd prime powers q, sqrt(2q) is irrational because its 2-adic valuation is odd.',
      'relation_to_Pass5434':'The determinant is the constant-term norm of this integral factorization; equal multiplicities of the conjugate roots force radical cancellation.',
      'anchors':rows,
      'boundary':'Characteristic-zero spectral polynomial of the unsigned Gram operator; no modular semisimplicity claim is made.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
