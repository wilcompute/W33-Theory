#!/usr/bin/env python3
"""Pass5451: negative-Pell determinant squares force the split q-mod8 Weil branch.

Pass5450 proves that for odd q the unsigned apartment Gram determinant is a
square iff q^2-2m^2=-1.  Reducing this equation modulo16: m is odd, hence
2m^2=2 (mod16), so q^2=1 (mod16).  Therefore

  q = +/-1 (mod8).

Pass5361/5406 gives the independent characteristic-two logical Weil clock:
- q=+/-1 mod8: the two middle Weil factors are individually defined over F2;
- q=+/-3 mod8: they are Galois-fused over F2 and split only over F4.

Consequently every odd finite-field q for which the unsigned Gram determinant is
a square lies in the F2-split logical Weil branch.  The converse is false: q=9
is 1 mod8 but (q^2+1)/2=41 is not square.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5451_PELL_WEIL_CLOCK_COMPATIBILITY.json'

def pell_qs(n):
    x,y=1,1;out=[]
    for _ in range(n):out.append((x,y));x,y=3*x+4*y,2*x+3*y
    return out

def main():
    pell=pell_qs(10)
    for q,m in pell:
        assert q*q-2*m*m==-1
        assert q%8 in (1,7)
        assert m%2==1
    split_nonpell=[]
    for q in (9,17,23,25,31,47,49):
        if q%8 in (1,7):
            h=(q*q+1)//2;s=math.isqrt(h)
            if s*s!=h:split_nonpell.append(q)
    assert 9 in split_nonpell and 17 in split_nonpell
    out={
      'pass':5451,'status':'THEOREM_PELL_SQUARE_DETERMINANT_IMPLIES_SPLIT_BINARY_WEIL_CLOCK',
      'arithmetic_input':'Pass5450: for odd q, det(BB^T) square iff q^2-2m^2=-1.',
      'mod16_step':'Negative Pell implies m odd and q^2=1 mod16, hence q=+/-1 mod8.',
      'modular_input':'Pass5361/5406: q=+/-1 mod8 gives individually F2-defined logical Weil factors; q=+/-3 mod8 gives the F4/Galois-fused branch.',
      'theorem':'Odd-q square unsigned Gram determinant => binary logical Weil sector lies in the split F2 branch.',
      'first_Pell_q_coordinates':[q for q,m in pell],
      'converse_counterexamples':split_nonpell,
      'boundary':'One-way implication only. q=+/-1 mod8 does not imply the determinant is square, and no physical phase-transition interpretation is asserted.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
