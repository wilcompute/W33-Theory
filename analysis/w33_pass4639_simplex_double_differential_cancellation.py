#!/usr/bin/env python3
"""Pass 4639 -- two square-zero 63-point differentials cancel to the simplex/Hamming CSS code.

On the 63 nonzero vectors of the natural six-space U6, let D be the polar matrix
D[x,y]=B(x,y).  Split the coordinates into 27 singular and 36 anisotropic points.
Then

  D0 = [[0,R],[R^T,0]]        (cross-shell differential),
  Delta = diag(S27,A36)       (within-shell differential),
  D = D0 + Delta.

Over F2 all three square to zero.  D0 and Delta each have rank 12 and in fact the
same 12-dimensional image; they commute.  Their sum D has rank only 6.  Hence
homology jumps from 63-2*12=39 to 63-2*6=51.  The row code of D is exactly the
[63,6,32] simplex code, so the final CSS code is [[63,51,3]].
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4592_paired_axes_simplex_hexacode_golay as p4592
import w33_pass4575_cubic_incidence_binary_code as p4575
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4639_SIMPLEX_DOUBLE_DIFFERENTIAL_CANCELLATION.json'

def main()->int:
    allv=list(range(1,64));sing=[x for x in allv if p4592.qminus_f4_message(x)==0];anis=[x for x in allv if p4592.qminus_f4_message(x)==1]
    assert (len(sing),len(anis))==(27,36)
    B=lambda x,y:p4592.polar(x,y)
    R=np.array([[B(s,a) for a in anis] for s in sing],dtype=np.uint8)
    S=np.array([[B(x,y) for y in sing] for x in sing],dtype=np.uint8);A=np.array([[B(x,y) for y in anis] for x in anis],dtype=np.uint8)
    D0=np.block([[np.zeros((27,27),dtype=np.uint8),R],[R.T,np.zeros((36,36),dtype=np.uint8)]])
    Delta=np.block([[S,np.zeros((27,36),dtype=np.uint8)],[np.zeros((36,27),dtype=np.uint8),A]])
    D=(D0^Delta).astype(np.uint8);Full=np.array([[B(x,y) for y in allv] for x in allv],dtype=np.uint8)
    assert np.array_equal(D,Full)
    r0=p4575.rank2(D0);rd=p4575.rank2(Delta);r=p4575.rank2(D);assert (r0,rd,r)==(12,12,6)
    assert not np.any((D0@D0)%2) and not np.any((Delta@Delta)%2) and not np.any((D@D)%2)
    assert np.array_equal((D0@Delta)%2,(Delta@D0)%2)
    assert p4575.rank2(np.concatenate([D0,Delta],axis=0))==12
    h0=63-2*r0;hd=63-2*rd;h=63-2*r;assert (h0,hd,h)==(39,39,51)
    rb=p4575.independent_rows(D);W=p4575.code_enumerator(rb);assert W=={0:1,32:63} or dict(W)=={0:1,32:63}
    low=p4575.low_kernel_counts(D,3);assert low[1]==low[2]==0 and low[3]>0
    out={'pass':4639,'operators':{'D0_cross':{'rank':r0,'square_zero':True,'homology_dimension':h0},'Delta_within':{'rank':rd,'square_zero':True,'homology_dimension':hd},'D_full_polar':{'rank':r,'square_zero':True,'homology_dimension':h}},'cancellation':{'cross_and_within_images_equal':True,'commute':True,'rank_12_plus_rank_12_to_rank_6':True,'homology_jump':12},'simplex_CSS':{'row_code':'[63,6,32] simplex','dual':'[63,57,3] Hamming','CSS':'[[63,51,3]]'},'theorem':'The singular/anisotropic split of the 63-point polar matrix yields two commuting square-zero rank-12 differentials with the same image. Their characteristic-two sum cancels to rank 6, raising homology from 39 to 51 and producing the fused simplex/Hamming [[63,51,3]] CSS code.','boundary':'Exact F2 chain-complex/code theorem. The cancellation is algebraic in characteristic two and is not by itself a dynamical or physical interference mechanism.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
