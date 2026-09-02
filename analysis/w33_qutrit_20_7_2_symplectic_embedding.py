#!/usr/bin/env python3
"""Construct a nonlocal symplectic embedding of the external [[20,7,2]]_3 code
into the canonical W33 [[240,81,3]]_3 edge CSS carrier.

The previous no-go excludes only monomial 20-edge selectors. Here physical X
coordinates are allowed to mix linearly. We construct A,B in F_3^(20x240) with
A B^T = I_20, so (x,z) -> (xA,zB) is an injective symplectic Pauli embedding.
The seven H1 rows are sent to independent parent logical-X classes and the two
H0 rows to parent X stabilizers.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
HX_PATH=ROOT/'matrices/w33_HX_40x240_GF3.mtx'
HZ_PATH=ROOT/'matrices/w33_HZ_160x240_GF3.mtx'
EXT=ROOT/'data/w33_qutrit_20_7_2_external_code.json'

def mm(path):
    lines=[x.strip() for x in path.read_text().splitlines() if x.strip() and not x.startswith('%')]
    m,n,nnz=map(int,lines[0].split()); a=np.zeros((m,n),dtype=np.int64)
    for row in lines[1:]:
        i,j,v=map(int,row.split()); a[i-1,j-1]=v%3
    assert np.count_nonzero(a)==nnz
    return a%3

def rref(a):
    a=np.array(a,dtype=np.int64)%3; m,n=a.shape; piv=[]; r=0
    for c in range(n):
        p=next((i for i in range(r,m) if a[i,c]),None)
        if p is None: continue
        a[[r,p]]=a[[p,r]]
        if a[r,c]==2: a[r]=(2*a[r])%3
        for i in range(m):
            if i!=r and a[i,c]: a[i]=(a[i]-a[i,c]*a[r])%3
        piv.append(c); r+=1
        if r==m: break
    return a,piv

def rank(a): return len(rref(a)[1])

def row_basis(a):
    rr,p=rref(a); return rr[:len(p)]

def nullspace(a):
    rr,piv=rref(a); n=a.shape[1]; free=[c for c in range(n) if c not in piv]; out=[]
    for f in free:
        x=np.zeros(n,dtype=np.int64); x[f]=1
        for i,p in enumerate(piv): x[p]=(-rr[i,f])%3
        out.append(x)
    return np.array(out,dtype=np.int64)%3

def inv(a):
    a=np.array(a,dtype=np.int64)%3; n=a.shape[0]; aug=np.concatenate([a,np.eye(n,dtype=np.int64)],axis=1); r=0
    for c in range(n):
        p=next(i for i in range(r,n) if aug[i,c]); aug[[r,p]]=aug[[p,r]]
        if aug[r,c]==2: aug[r]=(2*aug[r])%3
        for i in range(n):
            if i!=r and aug[i,c]: aug[i]=(aug[i]-aug[i,c]*aug[r])%3
        r+=1
    return aug[:,n:]%3

def extend_basis(rows,width,target):
    out=[np.array(x,dtype=np.int64)%3 for x in rows]; cur=rank(np.array(out)) if out else 0
    for j in range(width):
        e=np.zeros(width,dtype=np.int64); e[j]=1
        if rank(np.array(out+[e]))>cur: out.append(e); cur+=1
        if cur==target: break
    if cur!=target: raise RuntimeError('failed to extend basis')
    return np.array(out,dtype=np.int64)%3

def hash_matrix(a):
    return 'sha256:'+hashlib.sha256(bytes(int(x) for x in a.flatten())).hexdigest()

def verify():
    hx,hz=mm(HX_PATH),mm(HZ_PATH)
    ext=json.loads(EXT.read_text())
    h1=np.array(ext['H1_logical_rows'],dtype=np.int64)%3
    h0=np.array(ext['H0_x_stabilizer_rows'],dtype=np.int64)%3
    h=np.vstack([h1,h0])
    hxb=row_basis(hx)
    ker=nullspace(hz)
    span=[x.copy() for x in hxb]; cur=rank(np.array(span)); logical=[]
    for v in ker:
        nr=rank(np.array(span+[v]))
        if nr>cur: logical.append(v.copy()); span.append(v.copy()); cur=nr
        if len(logical)==81: break
    targets9=np.array(logical[:7]+[hxb[0],hxb[1]],dtype=np.int64)%3
    m=extend_basis(list(h),20,20)
    targets20=extend_basis(list(targets9),240,20)
    A=(inv(m)@targets20)%3
    _,piv=rref(A); cols=piv[:20]
    q=np.zeros((240,20),dtype=np.int64); q[cols,:]=inv(A[:,cols]); B=q.T%3
    image=(h@A)%3
    sym=(A@B.T)%3
    checks={
      'parent_shapes':hx.shape==(40,240) and hz.shape==(160,240),
      'parent_css_commutes':np.all((hx@hz.T)%3==0),
      'parent_ranks':rank(hx)==39 and rank(hz)==120,
      'parent_has_81_logical_x_classes':len(logical)==81,
      'A_rank_20':rank(A)==20,
      'B_rank_20':rank(B)==20,
      'ABt_identity':np.array_equal(sym,np.eye(20,dtype=np.int64)),
      'H1_maps_to_kernel_HZ':np.all((hz@image[:7].T)%3==0),
      'H1_independent_mod_X_stabilizers':rank(np.vstack([hxb,image[:7]]))==46,
      'H0_maps_to_row_HX':np.array_equal(image[7:9],targets9[7:9]),
      'nine_constraints_exact':np.array_equal(image,targets9),
    }
    return {
      'schema':'w33.qutrit-20-7-2-symplectic-embedding.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'checks':checks,
      'construction':{'A_shape':[20,240],'B_shape':[20,240],'A_sha256':hash_matrix(A),'B_sha256':hash_matrix(B),'right_inverse_pivot_columns_0_indexed':cols},
      'theorem':'The external 20-qutrit Pauli space admits an explicit nonlocal CSS-linear symplectic embedding into the W33 240-edge Pauli space with H0 sent into parent X stabilizers and H1 into seven independent parent logical-X classes.',
      'interpretation':'The earlier weight-6 vs weight-12 no-go is a locality/monomial obstruction, not an obstruction to general Clifford embedding.',
      'boundary':'This algebraic Pauli/Clifford embedding is nonlocal and does not yet provide a low-weight optical circuit, decoder, magic-state threshold, or fault-tolerant locality bound.'
    }
if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
