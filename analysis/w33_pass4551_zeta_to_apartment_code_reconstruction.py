#!/usr/bin/env python3
"""Pass 4551 -- primitive C8 zeta data reconstructs the apartment code.

Pass 4548 proves that among degree-four Walsh supports of the primitive signed
length-eight Ihara coefficient, coefficient 712 occurs on exactly 1620 supports
and those supports are exactly the W33 building apartments.

This pass turns that tomography statement into a coding theorem. Treat the 40
Walsh variables as row labels and each coefficient-712 support as a binary
column. The resulting 40 x 1620 matrix H_zeta is exactly the apartment-incidence
matrix H. Therefore zeta data alone recovers rank_F2(H_zeta)=39 and
H_zeta H_zeta^T=A_* mod 2. The [1620,39,162] distance theorem and intrinsic-W33
minimum-shell reconstruction remain inherited independent certificates.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

import w33_pass4548_c7_c8_higher_body_tomography as p4548
from w33_pass4495_4502_distance_prism_reconstruction import geometry
import w33_pass4511_4514_dual_even_prism_ihara as p4514

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS4551_ZETA_TO_APARTMENT_CODE.json'


def rank2(M):
    A=np.asarray(M,dtype=np.uint8).copy();m,n=A.shape;r=0
    for c in range(n):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows):continue
        rr=r+int(rows[0])
        if rr!=r:A[[r,rr]]=A[[rr,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        r+=1
        if r==m:break
    return r


def main()->int:
    pts,pidx,lines,Astar,apartments,apmasks,H=geometry();apset=set(apmasks)
    selected,psp,outer,pgsp=p4514.build_groups(pts,pidx,lines)
    p8,Apoint=p4548.compute_prime_orbits(8,pts,pidx,lines,Astar,selected)
    zeta_masks=set()
    for orb,c,rep in p8:
        inv=p4514.graph_inv(rep,Astar)
        if inv['support_size']==4 and c==712:zeta_masks|=set(orb)
    assert len(zeta_masks)==1620 and zeta_masks==apset

    cols=sorted(zeta_masks);Hz=np.zeros((40,1620),dtype=np.uint8)
    for j,m in enumerate(cols):
        for i in range(40):Hz[i,j]=(m>>i)&1
    original_cols={sum(int(H[i,j])<<i for i in range(40)) for j in range(1620)}
    assert set(cols)==original_cols
    rank=rank2(Hz);assert rank==39
    gram=(Hz@Hz.T)%2;assert np.array_equal(gram,Astar)
    row_weights=sorted(set(map(int,Hz.sum(1))));assert row_weights==[162]

    out={
      'pass':4551,
      'C8_selector':{'Walsh_degree':4,'primitive_length':8,'apartment_coefficient':712,'selected_supports':1620},
      'reconstructed_matrix':{'shape':[40,1620],'rank_F2':39,'row_weight':162,'column_weight':4,
                              'Gram_mod2':'A_* (dual-W33 line adjacency)'},
      'identity':'the coefficient-712 support set equals the 1620 apartment C4 column supports exactly',
      'inherited_certified_consequences':{
        'apartment_code':'[1620,39,162] (Pass 4495)','minimum_words':40,
        'code_reconstructs_dual_W33':'Pass 4500'},
      'boundary':'The new exact statement is C8 degree-four zeta tensor -> apartment incidence matrix. Distance 162 and Aut(C) are inherited from earlier independent certificates; no physical zeta observable is asserted.'}
    OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
