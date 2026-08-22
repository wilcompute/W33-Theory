#!/usr/bin/env python3
"""Pass7213: canonical signed 45-tritangent frame from the 90 selected E8 D4s."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass7163_7170_e8_hexagonal_lift as e8
import w33_pass7182_d4_glue_spread_code as d4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7213_D4_SIGNED_TRITANGENT_FRAME.json'

def main():
    _,_,_,_,adj,_,_,_=e8.e8_fibers()
    Q,partner=d4.cqs(adj)
    pairs=d4.pairs(partner); assert len(Q)==90 and len(pairs)==45
    reps=[a for a,b in pairs]
    B=np.zeros((45,45),dtype=np.int64)
    rel_hist={}
    for i,j in __import__('itertools').combinations(range(45),2):
        r=d4.relation(Q,adj,reps[i],reps[j]); rel_hist[str(r)]=rel_hist.get(str(r),0)+1
        if r==(1,3): s=1
        elif r==(0,7): s=-1
        elif r==(0,4): s=0
        else: raise AssertionError((i,j,r))
        B[i,j]=B[j,i]=s
    A=np.abs(B)
    assert np.all(A.sum(1)==32)
    for i in range(45):
        for j in range(i+1,45):
            c=int(A[i]@A[j])
            assert c==(22 if A[i,j] else 24)
    I=np.eye(45,dtype=np.int64)
    assert np.array_equal(B@B,4*B+32*I)
    # Minimal polynomial has roots 8,-4. Trace=0 fixes multiplicities 15,30.
    assert np.trace(B)==0
    m8,m4=15,30
    assert m8+m4==45 and 8*m8-4*m4==0
    # G=I+B/4; equivalently H=4G=4I+B satisfies H^2=12H.
    H=4*I+B
    assert np.array_equal(H@H,12*H)
    assert np.all(np.diag(H)==4)
    off=H.copy();np.fill_diagonal(off,0)
    assert set(np.unique(off))=={-1,0,1}
    # The switching class is independent of choosing the other D4 in any antipodal pair:
    # replacing one representative conjugates B by a diagonal sign switch.
    out={
      'schema':'w33.pass7213.d4_signed_tritangent_frame.v1','status':'PASS',
      'vertices':45,'source':'90 selected D4 subsystems modulo D4 <-> D4^perp',
      'unsigned_support':'srg(45,32,22,24) tritangent overlap graph',
      'signed_relation':'+1 for selected relation (1,3), -1 for (0,7), 0 for (0,4)',
      'switching_class_canonical':True,
      'signed_adjacency_identity':'B^2 = 4 B + 32 I',
      'signed_spectrum':{'8':15,'-4':30},
      'gram':'G = I + B/4',
      'gram_identity':'G^2 = 3 G',
      'tight_frame':'45 unit vectors in R^15 with frame bound 3',
      'pairwise_inner_products':['0','+1/4','-1/4'],
      'rank':15,'zero_neighbors_per_vector':12,'nonzero_neighbors_per_vector':32,
      'relation_histogram_for_chosen_section':rel_hist,
      'boundary':'Exact finite signed-frame statement. A different D4/D4-perp section only performs Seidel switching; no physical state-space interpretation is inferred.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','spectrum':out['signed_spectrum'],'rank':15}))
if __name__=='__main__': main()
