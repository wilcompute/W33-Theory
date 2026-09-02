#!/usr/bin/env python3
"""Deterministically sparsify the explicit [[20,7,2]]_3 -> W33 edge symplectic map.

The base certificate fixes H A = T for the nine external code rows.  Each physical
column of A may therefore be shifted by any vector in ker(H) without changing
those code images.  We exploit that exact affine freedom with GF(3) coordinate
descent, accepting only support-reducing moves that preserve rank 20.  A fresh
right inverse B is then reconstructed so A B^T = I_20.

This is an algebraic sparsifier, not a claim of geometrically local/fault-tolerant
hardware.  It reports support and W33-edge footprint metrics explicitly.
"""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import numpy as np

import w33_qutrit_20_7_2_symplectic_embedding as base

ROOT=Path(__file__).resolve().parents[1]
EXT=ROOT/'data/w33_qutrit_20_7_2_external_code.json'
HX_PATH=ROOT/'matrices/w33_HX_40x240_GF3.mtx'
HZ_PATH=ROOT/'matrices/w33_HZ_160x240_GF3.mtx'


def build_base():
    hx,hz=base.mm(HX_PATH),base.mm(HZ_PATH)
    ext=json.loads(EXT.read_text())
    h1=np.array(ext['H1_logical_rows'],dtype=np.int64)%3
    h0=np.array(ext['H0_x_stabilizer_rows'],dtype=np.int64)%3
    h=np.vstack([h1,h0])
    hxb=base.row_basis(hx); ker=base.nullspace(hz)
    span=[x.copy() for x in hxb]; cur=base.rank(np.array(span)); logical=[]
    for v in ker:
        nr=base.rank(np.array(span+[v]))
        if nr>cur:
            logical.append(v.copy()); span.append(v.copy()); cur=nr
        if len(logical)==81: break
    targets9=np.array(logical[:7]+[hxb[0],hxb[1]],dtype=np.int64)%3
    m=base.extend_basis(list(h),20,20)
    targets20=base.extend_basis(list(targets9),240,20)
    A=(base.inv(m)@targets20)%3
    return hx,hz,h,targets9,A


def nnz(a): return int(np.count_nonzero(a%3))

def row_weights(a): return [int(np.count_nonzero(r%3)) for r in a]

def hash_matrix(a): return 'sha256:'+hashlib.sha256(bytes(int(x) for x in a.flatten())).hexdigest()


def rank_preserving_descent(A,h,passes=4):
    A=np.array(A,dtype=np.int64)%3
    null=base.nullspace(h)
    accepted=0
    before=nnz(A)
    # Independent affine columns; deterministic basis/order, strict improvement only.
    for _ in range(passes):
        changed=False
        for j in range(A.shape[1]):
            col=A[:,j].copy()
            current=int(np.count_nonzero(col))
            for n in null:
                best=col; bestw=current
                for alpha in (1,2):
                    cand=(col+alpha*n)%3
                    w=int(np.count_nonzero(cand))
                    if w<bestw:
                        old=A[:,j].copy(); A[:,j]=cand
                        if base.rank(A)==20:
                            best,bestw=cand,w
                        A[:,j]=old
                if bestw<current:
                    A[:,j]=best; col=best; current=bestw; accepted+=1; changed=True
        if not changed: break
    return A,{'before_nnz':before,'after_nnz':nnz(A),'accepted_moves':accepted,'passes':passes}


def right_inverse(A):
    # Pick pivot columns from row-RREF and solve using the invertible 20x20 minor.
    _,piv=base.rref(A); cols=piv[:20]
    if len(cols)!=20: raise RuntimeError('A lost full row rank')
    q=np.zeros((240,20),dtype=np.int64)
    q[cols,:]=base.inv(A[:,cols])
    B=q.T%3
    if not np.array_equal((A@B.T)%3,np.eye(20,dtype=np.int64)):
        raise RuntimeError('right inverse construction failed')
    return B,cols


def edge_endpoints(hx):
    out=[]
    for j in range(hx.shape[1]):
        vs=[i for i in range(hx.shape[0]) if hx[i,j]%3]
        if len(vs)!=2: raise RuntimeError('edge column does not have two endpoints')
        out.append(tuple(vs))
    return out


def footprint(A,hx):
    endpoints=edge_endpoints(hx); rows=[]
    for i,r in enumerate(A):
        supp=[j for j,x in enumerate(r) if x%3]
        verts=sorted({v for e in supp for v in endpoints[e]})
        # Connectivity of selected edges in the underlying 40-vertex graph.
        adj={v:set() for v in verts}
        for e in supp:
            u,v=endpoints[e]; adj[u].add(v); adj[v].add(u)
        comps=0; unseen=set(verts)
        while unseen:
            comps+=1; stack=[unseen.pop()]
            while stack:
                u=stack.pop()
                for v in adj[u]:
                    if v in unseen: unseen.remove(v); stack.append(v)
        rows.append({'row':i,'edge_weight':len(supp),'vertex_footprint':len(verts),'components':comps if verts else 0})
    return rows


def verify():
    hx,hz,h,targets9,A0=build_base()
    A,search=rank_preserving_descent(A0,h)
    B,cols=right_inverse(A)
    image=(h@A)%3
    fp=footprint(A,hx)
    checks={
      'constraints_preserved':np.array_equal(image,targets9),
      'A_rank_20':base.rank(A)==20,
      'B_rank_20':base.rank(B)==20,
      'symplectic_duality':np.array_equal((A@B.T)%3,np.eye(20,dtype=np.int64)),
      'support_never_worsened':nnz(A)<=nnz(A0),
      'strict_support_improvement':nnz(A)<nnz(A0),
      'H1_remains_parent_logical_X':np.all((hz@image[:7].T)%3==0),
      'H0_remains_parent_X_stabilizer':base.rank(np.vstack([base.row_basis(hx),image[7:9]]))==base.rank(hx),
    }
    return {
      'schema':'w33.qutrit-20-7-2-sparse-symplectic.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'checks':checks,
      'search':search,
      'A':{'sha256':hash_matrix(A),'row_weights':row_weights(A),'max_row_weight':max(row_weights(A)),'mean_row_weight':sum(row_weights(A))/20},
      'B':{'sha256':hash_matrix(B),'row_weights':row_weights(B),'pivot_columns_0_indexed':cols},
      'locality':{'rows':fp,'max_vertex_footprint':max(x['vertex_footprint'] for x in fp),'max_components':max(x['components'] for x in fp)},
      'interpretation':'The nonlocal symplectic witness has been moved within its exact affine solution class to a strictly lower-support representative while preserving all code-image and symplectic constraints.',
      'boundary':'Lower algebraic support is not yet a fault-tolerant locality theorem; optical routing depth and noise propagation require a compiled circuit.'
    }

if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
