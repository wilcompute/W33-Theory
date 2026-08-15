#!/usr/bin/env python3
"""Pass5335: exact kernel identification at all currently verified odd-q anchors.

Pass5288 proves the binary W-line code C_W lies in ker(F^T) and has dimension
1+f, where f=q(q+1)^2/2. Pass5334 records v=1+f+g and rank_2(F)=g at
q=3,5,7,9,11,13. Therefore at each anchor

    dim ker(F^T)=v-g=1+f=dim C_W,

so the inclusion is equality. The all-odd rank conjecture is equivalently the
kernel theorem ker(F^T)=C_W for every odd q.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5335_ALLODD_KERNEL_EQUALS_LINECODE_ANCHORS.json'

def row(q,r):
    v=(q+1)*(q*q+1);f=q*(q+1)**2//2;g=q*(q*q+1)//2
    assert v==1+f+g and r==g and v-r==1+f
    return {'q':q,'v':v,'rank_F2':r,'kernel_dimension':v-r,'W_line_code_dimension':1+f,'equality':True}

def main():
    anchors={3:15,5:65,7:175,9:369,11:671,13:1105}
    A={str(q):row(q,r) for q,r in anchors.items()}
    out={'pass':5335,'status':'THEOREM_BINARY_FOOTPRINT_KERNEL_EQUALS_W_LINE_CODE_AT_Q3_TO_Q13_ANCHORS',
      'general_inclusion':'C_W <= ker(F^T), dim C_W=1+q(q+1)^2/2.',
      'equivalence':'rank_2(F)=g iff ker(F^T)=C_W, where g=q(q^2+1)/2.',
      'verified_anchor_equality':A,
      'proof':'At each rank-equality anchor, nullity(F^T)=v-g=1+f, exactly the already-proved dimension of the included W-line code.',
      'boundary':'This identifies the full binary kernel at q=3,5,7,9,11,13. The equality ker(F^T)=C_W remains open for arbitrary odd q and is equivalent to the all-odd rank conjecture.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
