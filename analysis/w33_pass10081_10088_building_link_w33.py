#!/usr/bin/env python3
"""Pass10081-10088: W33 is the canonical symplectic refinement of the middle F9 chamber residue.

The full chamber from Pass10041 lives in the affine building of PGL6(Q3(i)).
Its spherical link at a vertex is the A5 building over F9, with a complete flag
F1<F2<F3<F4<F5 in F9^6.  The explicit Hermitian Gram from Pass10009 makes the
regular-unipotent flag self-dual:

    F_j^perp = F_{6-j}.

Hence F4 is coisotropic with radical F2, and the middle quotient

    Q = F4/F2

is a canonical nondegenerate 2-dimensional Hermitian space over F9.  On the
underlying F3-vector space Q_F3 (dimension 4), the imaginary part of the
Hermitian form is a nondegenerate alternating form.  Its polar space is W(3,3).

This is a REFINEMENT of the middle F9 residue, not literally an A5(F9)
subbuilding: F3-lines are finer objects than F9-lines.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10081_10088_BUILDING_LINK_W33.json'
P=3
A=np.array([
 [0,0,0,0,0,1],
 [0,0,0,0,2,2],
 [0,0,0,1,2,1],
 [0,0,2,0,0,0],
 [0,1,1,0,0,0],
 [2,1,2,0,0,0]],dtype=np.int64)%P

def rankp(M):
    R=np.array(M,dtype=np.int64)%P;m,n=R.shape;r=0
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]]
        R[r]=(R[r]*pow(int(R[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and R[i,c]:R[i]=(R[i]-R[i,c]*R[r])%P
        r+=1
    return r

def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            u=pow(x,-1,P);return tuple(u*y%P for y in v)
    raise ValueError

def perp_basis(F):
    M=(F.T@A)%P
    # nullspace
    R=M.copy();m,n=R.shape;r=0;piv=[]
    for c in range(n):
        q=next((i for i in range(r,m) if R[i,c]),None)
        if q is None:continue
        R[[r,q]]=R[[q,r]];R[r]=(R[r]*pow(int(R[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and R[i,c]:R[i]=(R[i]-R[i,c]*R[r])%P
        piv.append(c);r+=1
    free=[c for c in range(n) if c not in piv];cols=[]
    for f in free:
        v=np.zeros(n,dtype=np.int64);v[f]=1
        for i,pv in enumerate(piv):v[pv]=(-R[i,f])%P
        cols.append(v)
    return np.column_stack(cols)
def same(A1,A2):return rankp(np.column_stack([A1,A2]))==rankp(A1)==rankp(A2)

def all_2spaces_F3_4():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    S=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            R=np.array([pts[i],pts[j]],dtype=np.int64)%3
            # rref rows
            rr=R.copy();r=0
            for c in range(4):
                q=next((k for k in range(r,2) if rr[k,c]),None)
                if q is None:continue
                rr[[r,q]]=rr[[q,r]];rr[r]=(rr[r]*pow(int(rr[r,c]),-1,3))%3
                for k in range(2):
                    if k!=r and rr[k,c]:rr[k]=(rr[k]-rr[k,c]*rr[r])%3
                r+=1
                if r==2:break
            if r==2:S.add(tuple(tuple(int(x) for x in row) for row in rr))
    return pts,sorted(S)

def main():
    # Flag F_j = span e0,...,e_{j-1}; verify exact self-duality.
    E=np.eye(6,dtype=np.int64)
    dual={}
    for j in range(1,6):
        F=E[:,:j];Fp=perp_basis(F);want=E[:,:6-j]
        ok=same(Fp,want);assert ok;dual[str(j)]=6-j
    # Middle quotient F4/F2 represented by e2,e3. A is the i-coefficient of H=iA.
    Amid=A[2:4,2:4]%3
    assert np.array_equal(Amid,np.array([[0,1],[2,0]],dtype=np.int64))
    assert rankp(Amid)==2
    # F9 = F3[i], i^2=2.  For x=a+i b, y=c+i d in F9^2 and H=i*A,
    # compute imaginary coefficient of x H conjugate(y)^T.  Derivation gives a 4x4 K.
    # Coordinates ordered (a0,a1,b0,b1). h = (a+i b) iA (c-i d)^T.
    # Imaginary part = a A c^T + b A d^T.
    K=np.block([[Amid,np.zeros((2,2),dtype=np.int64)],[np.zeros((2,2),dtype=np.int64),Amid]])%3
    assert np.array_equal(K.T%3,(-K)%3) and rankp(K)==4
    pts,spaces=all_2spaces_F3_4();assert len(pts)==40 and len(spaces)==130
    lag=[]
    for U in spaces:
        B=np.array(U,dtype=np.int64).T%3
        if not np.any(B.T@K@B%3):lag.append(U)
    assert len(lag)==40
    # incidence regularity: each lagrangian line has 4 projective points; each point lies on 4.
    pidx={p:i for i,p in enumerate(pts)};deg=[0]*len(pts)
    for U in lag:
        R=np.array(U,dtype=np.int64)%3
        lpts={canon((a*R[0]+b*R[1])%3) for a,b in ((1,0),(0,1),(1,1),(1,2))}
        assert len(lpts)==4
        for p in lpts:deg[pidx[p]]+=1
    assert set(deg)=={4}
    out={
      'schema':'w33.pass10081_10088.building_link_w33.v1','status':'PASS','passes':'10081-10088',
      'spherical_link':{'ambient':'A5 building over F9 = flags of proper nonzero subspaces of F9^6','chamber_flag':'F1<F2<F3<F4<F5'},
      'Hermitian_self_duality':{'relation':'F_j^perp=F_{6-j}','verified':dual,'middle':'F4^perp=F2, so F4/F2 is nondegenerate Hermitian dimension 2 over F9'},
      'middle_quotient':{'F9_dimension':2,'F3_dimension':4,'Hermitian_i_coefficient_matrix':Amid.tolist(),'underlying_alternating_matrix':K.tolist(),'alternating_rank':4},
      'W33_census':{'points':40,'lagrangian_lines':40,'points_per_line':4,'lines_per_point':4,'ambient_2spaces':130},
      'theorem':'The self-dual cyclotomic chamber canonically selects the middle quotient F4/F2. Its underlying F3^4 space carries the nondegenerate alternating imaginary part of the F9-Hermitian form, and its polar geometry is exactly W(3,3): 40 points, 40 Lagrangian lines, 4 points/line and 4 lines/point.',
      'precision':'W33 is a canonical symplectic F3 refinement of the middle F9 residue. It is not literally a subbuilding of the A5(F9) spherical link, because its F3 projective points refine the F9-subspace structure.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','middle':'F4/F2','W33':[40,40,4,4]}))
    return 0
if __name__=='__main__':raise SystemExit(main())
