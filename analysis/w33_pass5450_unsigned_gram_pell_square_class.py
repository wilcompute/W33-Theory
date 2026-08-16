#!/usr/bin/env python3
"""Pass5450: arithmetic square class of the all-q unsigned apartment Gram determinant.

Pass5434 gives
 det K = 2^(2P+1) q^(4P) (q-1)^(2f+4g+2q^4) (q^2+1)^(f+q^4).
All factors except the leading 2 and possibly q^2+1 occur to even powers.

For odd q, f=q(q+1)^2/2 is even and q^4 is odd, so f+q^4 is odd.  Since
q^2+1=2h with h=(q^2+1)/2,

  det K has square class 2(q^2+1)=4h ~ h.

Hence det K is an integer square iff h is a square, equivalently

  q^2 - 2m^2 = -1.

Thus odd-q square determinants are controlled exactly by the negative Pell
equation.  The first q>1 Pell coordinates are 7,41,239,1393,8119,...; only
those that are prime powers are geometrically admissible q.

For even finite fields q=2^e: q=2 has square class10; every q>=4 has square
class2.  Hence no even-q unsigned Gram determinant is a square.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5450_UNSIGNED_GRAM_PELL_SQUARE_CLASS.json'

def pell_qs(n):
    x,y=1,1;out=[]
    for _ in range(n):
        out.append((x,y));x,y=3*x+4*y,2*x+3*y
    return out

def odd_square_class(q):
    assert q%2==1
    return (q*q+1)//2

def main():
    pell=pell_qs(8)
    assert pell[:6]==[(1,1),(7,5),(41,29),(239,169),(1393,985),(8119,5741)]
    for q,m in pell:
        assert q*q-2*m*m==-1
        assert odd_square_class(q)==m*m
    anchors={}
    for q in (3,5,7,9,11,13,17,19,23,25,41,239):
        h=odd_square_class(q);s=math.isqrt(h)
        anchors[str(q)]={'square_class_representative':h,'determinant_is_square':s*s==h,'pell_m':s if s*s==h else None}
    assert anchors['7']['determinant_is_square'] and anchors['41']['determinant_is_square'] and anchors['239']['determinant_is_square']
    assert not anchors['3']['determinant_is_square'] and not anchors['5']['determinant_is_square']
    out={
      'pass':5450,'status':'THEOREM_ALLQ_UNSIGNED_GRAM_SQUARE_CLASS_AND_NEGATIVE_PELL_LAW',
      'odd_q_square_class':'det(BB^T) ~ (q^2+1)/2 in Q*/(Q*)^2.',
      'odd_q_square_criterion':'det(BB^T) is a perfect integer square iff q^2-2m^2=-1 for some integer m.',
      'negative_Pell_q_coordinates':[q for q,m in pell],
      'prime_power_firewall':'The Pell equation is arithmetic; the GQ(q,q) theorem only applies at Pell q that are finite-field prime powers.',
      'even_q':'For q=2 the square class is10; for q=2^e with e>=2 the square class is2. Therefore no even-q determinant is a square.',
      'anchors':anchors,
      'boundary':'This is an arithmetic corollary of Pass5434. It does not attach physical meaning to Pell solutions or claim every Pell q is a prime power.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
