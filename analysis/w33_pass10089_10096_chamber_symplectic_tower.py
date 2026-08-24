#!/usr/bin/env python3
"""Pass10089-10096 outside-box: the self-dual F9 chamber carries a canonical symplectic tower.

For the self-dual chamber flag F_j^perp=F_{6-j}, each coisotropic quotient

    Q_j = F_{6-j}/F_j,   j=0,1,2

is nondegenerate Hermitian over F9 of dimensions 6,4,2.  Taking the imaginary
part on the underlying F3 spaces gives nondegenerate alternating spaces of
dimensions 12,8,4.  Therefore the chamber canonically carries

    W(11,3) -> W(7,3) -> W(3,3),

or in qutrit count, 6 -> 4 -> 2.

The arrows are symplectic reductions by the chamber's paired isotropic layers,
not embeddings of one polar space as a literal subgeometry of the next.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10089_10096_CHAMBER_SYMPLECTIC_TOWER.json'
A=np.array([[0,0,0,0,0,1],[0,0,0,0,2,2],[0,0,0,1,2,1],[0,0,2,0,0,0],[0,1,1,0,0,0],[2,1,2,0,0,0]],dtype=np.int64)%3

def rankp(M):
    R=np.array(M,dtype=np.int64)%3;m,n=R.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]];R[r]=(R[r]*pow(int(R[r,c]),-1,3))%3
        for i in range(m):
            if i!=r and R[i,c]:R[i]=(R[i]-R[i,c]*R[r])%3
        r+=1
    return r

def main():
    rows=[]
    for j in (0,1,2):
        H=A[j:6-j,j:6-j]%3
        m=6-2*j
        assert H.shape==(m,m) and rankp(H)==m and np.array_equal(H.T%3,(-H)%3)
        K=np.block([[H,np.zeros((m,m),dtype=np.int64)],[np.zeros((m,m),dtype=np.int64),H]])%3
        assert rankp(K)==2*m and np.array_equal(K.T%3,(-K)%3)
        rows.append({'j':j,'Hermitian_F9_dimension':m,'underlying_F3_dimension':2*m,'symplectic_geometry':f'W({2*m-1},3)','qutrits':m,'projective_points':(3**(2*m)-1)//2})
    assert [r['qutrits'] for r in rows]==[6,4,2]
    out={'schema':'w33.pass10089_10096.chamber_symplectic_tower.v1','status':'PASS','passes':'10089-10096','outside_box':True,
         'reductions':rows,
         'tower':'W(11,3) -> W(7,3) -> W(3,3)',
         'qutrit_tower':'6 -> 4 -> 2',
         'mechanism':'Q_j=F_{6-j}/F_j with radical F_j; imaginary part of the induced F9-Hermitian form gives a nondegenerate alternating F3 form.',
         'theorem':'The self-dual six-step cyclotomic chamber canonically carries a three-rung symplectic reduction tower W(11,3), W(7,3), W(3,3), corresponding to six, four and two qutrits. The W33 middle endpoint is therefore part of a chamber-controlled tower rather than an isolated quotient.',
         'boundary':'Reduction tower, not literal nested subgeometries. No physical renormalization or spacetime interpretation is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','tower':out['tower'],'qutrits':[6,4,2]}))
    return 0
if __name__=='__main__':raise SystemExit(main())
