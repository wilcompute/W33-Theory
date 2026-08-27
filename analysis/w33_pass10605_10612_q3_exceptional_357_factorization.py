#!/usr/bin/env python3
"""Pass10605-10612: prove the 3*5*7 harmonic factorization is exceptional at q=3.

For the binary F4^6 clock one may write 4=q+1 at the W33 value q=3.  Removing
one scalar factor q=3 and the C13=Phi3(q) clock from (q+1)^6-1 suggests the
symbolic quotient

  ((q+1)^6-1)/(q Phi3(q)) = (q+2)(q^2+3q+3).

At q=3 this is 5*21=105.  The repo harmonic reading is

  q * (Phi4(q)/2) * Phi6(q),

which also equals 3*5*7=105.  We prove symbolically that the equality is
exceptional: the difference has a factor (q-3) and no polynomial identity is
being asserted away from q=3.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10605_10612_Q3_EXCEPTIONAL_357_FACTORIZATION.json'

def phi3(q): return q*q+q+1
def phi4(q): return q*q+1
def phi6(q): return q*q-q+1

def main():
    q=3
    assert 4**6-1==4095
    assert (4**6-1)//q//phi3(q)==105
    assert phi3(q)==13 and phi4(q)==10 and phi6(q)==7
    assert q*(phi4(q)//2)*phi6(q)==105
    # General factorization verified by coefficient expansion.
    # (q+1)^6-1 = q(q+2)Phi3(q)(q^2+3q+3).
    for x in range(-9,10):
      lhs=(x+1)**6-1
      rhs=x*(x+2)*phi3(x)*(x*x+3*x+3)
      assert lhs==rhs
    # Twice the difference, avoiding fractions:
    # 2[(q+2)(q^2+3q+3) - q Phi4 Phi6/2]
    # = -(q-3)(q^4+2q^3+6q^2+7q+4).
    for x in range(-9,10):
      left=2*(x+2)*(x*x+3*x+3)-x*phi4(x)*phi6(x)
      right=-(x-3)*(x**4+2*x**3+6*x*x+7*x+4)
      assert left==right
    out={
      'schema':'w33.pass10605_10612.q3_exceptional_357_factorization.v1','status':'PASS','passes':'10605-10612',
      'general_identity':'((q+1)^6-1)/(q Phi3(q)) = (q+2)(q^2+3q+3)',
      'W33_q3':{'Phi3':13,'Phi4':10,'Phi6':7,'F4^6_nonzero':4095,'after_scalar_and_C13':105,'harmonic':'3*5*7'},
      'exceptional_identity_at_q3':'105 = q*(Phi4(q)/2)*Phi6(q) at q=3',
      'difference_identity':'2[(q+2)(q^2+3q+3)] - q Phi4(q) Phi6(q) = -(q-3)(q^4+2q^3+6q^2+7q+4)',
      'interpretation':'Phi3=13 is the removed C13 clock; Phi6=7 survives intact; Phi4=10 contributes its odd half 5; the residual 3 is q itself after one F4^x scalar factor 3 was already projectivized away.',
      'theorem':'The residual 105=3*5*7 harmonic factorization is an arithmetic fingerprint of q=3. The general post-scalar/post-Phi3 quotient is (q+2)(q^2+3q+3), and its equality with q*(Phi4/2)*Phi6 has an explicit q-3 factor.',
      'boundary':'Exact integer polynomial identity. No universal 3-5-7 cyclotomic factorization away from q=3 is claimed.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','q3':105,'exceptional_factor':'q-3'}))
if __name__=='__main__':main()
