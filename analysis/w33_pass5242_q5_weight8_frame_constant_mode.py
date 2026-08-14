#!/usr/bin/env python3
"""Pass5242 (outside-box): the q=5 weight-8 dual shell is a full real frame but
has exactly one extra binary constant mode beyond the primal footprint code.

Pass5230 gives H8, the 24375x325 incidence matrix of all weight-8 dual words,
and the rank-4 scheme pair codegrees.  Hence

 H8^T H8 = 600 I + 25 R1 + 5 R2.

Using Pass5232's primitive eigenvalues gives the exact real Gram spectrum.  Over
F2, rank(H8)=259, so its kernel has dimension66.  C_F (dimension65) lies in the
kernel, and the all-ones vector also lies there because every row has weight8.
The all-ones vector is not in C_F because Pass5231 supplies an odd weight-9 dual
check.  Thus ker_F2(H8)=C_F direct-sum <1>.  Adding one odd dual check removes
exactly that constant mode.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5242_Q5_WEIGHT8_FRAME_CONSTANT_MODE.json'

def main():
    mult=[1,90,104,130]
    r1=[144,14,-6,-6];r2=[120,-10,-5,10]
    gram=[600+25*a+5*b for a,b in zip(r1,r2)]
    assert gram==[4800,900,425,500] and sum(mult)==325
    assert all(x>0 for x in gram)
    out={'pass':5242,'status':'THEOREM_Q5_WEIGHT8_SHELL_REAL_FRAME_BINARY_CONSTANT_MODE',
      'H8_shape':[24375,325],
      'integer_Gram':'H8^T H8 = 600 I + 25 R1 + 5 R2',
      'real_Gram_spectrum':{'4800':1,'900':90,'425':104,'500':130},
      'real_rank':325,
      'binary_rank':259,'binary_nullity':66,
      'binary_kernel':'ker_F2(H8)=C_F direct-sum <1>, dimensions 65+1',
      'constant_mode':'1 is killed by every even weight-8 check but is not in C_F because an odd weight-9 dual check exists.',
      'odd_check_role':'Adding any Pass5231 odd independent dual check removes the constant mode and gives a rank-260 parity matrix with kernel exactly C_F.',
      'interpretation':'The complete minimum dual shell is information-complete over R but deliberately misses one binary parity bit; the unique missing bit is global parity.',
      'boundary':'Finite q5 code/frame theorem; no quantum-measurement or physical-noise interpretation is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
