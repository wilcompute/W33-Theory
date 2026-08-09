#!/usr/bin/env python3
"""Pass 4505 -- H^1 of the full 29D apartment radical and its three charges.

Pass 4496 computes H^1 on the irreducible middle 8-space of H10.  This pass
answers the different question naturally exposed by the nonsplit apartment
extension: first cohomology of the entire radical R29=K/J.

Exact Cayley-graph cocycle computation gives

    dim Z^1(PSp(4,3),R29) = 31,
    dim B^1(PSp(4,3),R29) = 29,
    dim H^1(PSp(4,3),R29) = 2.

Hence there are three nonzero cohomology classes.  The Pass-4491 fixed-line
connecting cocycle is one of them.  A second independent class exists, but the
surprise is that all three nonzero classes have the SAME PSp-module support:

    W/J = (K intersect rowspace(N))/J,

of dimension 23, exactly the Pass-4492 route-hull/sentinel support
8 | (1 | 14).  The missing 6-dimensional radical factor is not activated by
any nonzero H^1 class.

This is H^1(G,R29), not the full Ext^1_G(H10,R29) group.  The nonsplitting of
the full 39->10 extension remains owned by Pass 4488.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from w33_pass4493_symmetry_breaking_section_threshold import (
    actions_from_line_gens, build_geometry, build_line_perm, perm_group,
    point_perm_from_matrix, quotient_model, small_generating_set,
    transvection_matrix,
)
from w33_pass4496_h10_extension_cohomology import h1_data, nullspace2, rank2
from w33_pass4469_apartment_css_h10_intertwiner import rref_rows
from w33_pass4481_apartment_radical_module_filtration import inter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_PASS4505_RADICAL_H1_THREE_CHARGES.json"


def inv2(M):
    M=np.asarray(M,dtype=np.uint8);n=M.shape[0]
    A=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if A[i,c])
        if r!=c:A[[c,r]]=A[[r,c]]
        for i in range(n):
            if i!=c and A[i,c]:A[i]^=A[c]
    return A[:,n:]


def solve2(A,b):
    A=np.asarray(A,dtype=np.uint8);b=np.asarray(b,dtype=np.uint8)
    M=np.column_stack((A.copy(),b.copy()));m,n=A.shape;r=0;piv=[]
    for c in range(n):
        rows=np.flatnonzero(M[r:,c])
        if not len(rows):continue
        rr=r+int(rows[0])
        if rr!=r:M[[r,rr]]=M[[rr,r]]
        for i in range(m):
            if i!=r and M[i,c]:M[i]^=M[r]
        piv.append(c);r+=1
    for i in range(r,m):
        if not M[i,:n].any() and M[i,n]:raise ValueError("inconsistent")
    x=np.zeros(n,dtype=np.uint8)
    for i,c in reversed(list(enumerate(piv))):
        x[c]=int(M[i,n]^(np.dot(M[i,:n],x)%2))
    return x


def coords_for_column_basis(B,y):
    """B is d x r, full column rank; solve B c = y by pivot rows."""
    _,piv=rref_rows(B.T),None
    # Pivot columns of B.T are independent rows of B.
    R=np.asarray(B.T,dtype=np.uint8).copy();m,n=R.shape;r=0;rows=[]
    for c in range(n):
        rr=next((i for i in range(r,m) if R[i,c]),None)
        if rr is None:continue
        if rr!=r:R[[r,rr]]=R[[rr,r]]
        for i in range(m):
            if i!=r and R[i,c]:R[i]^=R[r]
        rows.append(c);r+=1
        if r==m:break
    S=B[rows,:]
    c=(inv2(S)@np.asarray(y,dtype=np.uint8)[rows])%2
    assert np.array_equal((B@c)%2,np.asarray(y,dtype=np.uint8)%2)
    return c


def module_closure(seed,rho):
    cur=rref_rows(np.asarray([v for v in seed if np.any(v)],dtype=np.uint8))
    while True:
        old=len(cur)
        images=[(g@v)%2 for g in rho for v in cur]
        cur=rref_rows(np.vstack((cur,np.asarray(images,dtype=np.uint8)))) if images else cur
        if len(cur)==old:return cur


def same_rowspace(A,B):
    A=rref_rows(A);B=rref_rows(B)
    return len(A)==len(B)==len(rref_rows(np.vstack((A,B))))


def main()->int:
    pts,pidx,lines,lidx,_,Astar,*_=build_geometry()
    Astar=np.asarray(Astar,dtype=np.uint8)
    K,Ereps,Vreps,coordE,coordV,Pi=quotient_model(Astar)
    matrices=[transvection_matrix(v) for v in pts]
    point_trans=[point_perm_from_matrix(M,pts,pidx) for M in matrices]
    line_trans=[build_line_perm(M,pts,pidx,lines,lidx) for M in matrices]
    selected=[];full={tuple(range(40))}
    for i,p in enumerate(line_trans):
        trial=perm_group([line_trans[j] for j in selected]+[p],40)
        if len(trial)>len(full):selected.append(i);full=trial
        if len(full)==25920:break
    assert len(full)==25920 and len(selected)==5
    gens=[line_trans[i] for i in selected]
    GE,GV=actions_from_line_gens(gens,Ereps,Vreps,coordE,coordV)

    # R29 = ker Pi in E coordinates.
    Rrows=rref_rows(np.asarray(nullspace2(Pi),dtype=np.uint8))
    assert len(Rrows)==29
    B=Rrows.T # 39 x 29 column basis
    rho=[]
    for ge in GE:
        cols=[]
        for j in range(29):
            y=(ge@B[:,j])%2
            cols.append(coords_for_column_basis(B,y))
        rho.append(np.column_stack(cols).astype(np.uint8))
    assert all(rank2(g)==29 for g in rho)

    hd=h1_data(rho)
    assert hd["dimZ"]==31 and hd["dimB"]==29 and hd["dimH"]==2
    assert len(hd["seen"])==25920 and len(hd["Qreps"])==2

    # Pass-4491 connecting cocycle from the unique globally fixed vector in V10.
    I10=np.eye(10,dtype=np.uint8)
    fixed=nullspace2(np.vstack([g^I10 for g in GV]));assert len(fixed)==1
    v=np.asarray(fixed[0],dtype=np.uint8);e=solve2(Pi,v)
    fixed_vals=[]
    for ge in GE:
        c=((ge@e)%2)^e
        assert not np.any((Pi@c)%2)
        fixed_vals.append(coords_for_column_basis(B,c))
    fixed_vec=np.concatenate(fixed_vals)
    fixed_coords=hd["coords"](fixed_vec)[-2:]
    assert fixed_coords.any()

    # Three nonzero quotient classes: the fixed class, one independent class,
    # and their sum.  Select an H1 representative independent of fixed_vec.
    basis=np.asarray(hd["Cob"],dtype=np.uint8)
    span=rref_rows(np.vstack((basis,fixed_vec)))
    second=None
    for q in hd["Qreps"]:
        if rank2(np.vstack((span,q)))>len(span):second=np.asarray(q,dtype=np.uint8);break
    assert second is not None
    reps={"fixed_line":fixed_vec,"second":second,"sum":fixed_vec^second}

    closures={}
    for name,z in reps.items():
        vals=[z[i*29:(i+1)*29] for i in range(5)]
        closures[name]=module_closure(vals,rho)
        assert len(closures[name])==23
    assert same_rowspace(closures["fixed_line"],closures["second"])
    assert same_rowspace(closures["fixed_line"],closures["sum"])

    # Identify that common 23-space with the Pass-4492 W/J support.
    N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    Rroute=rref_rows(np.asarray(nullspace2(N),dtype=np.uint8))
    Rp=rref_rows(N)
    W=inter(rref_rows(np.asarray(K,dtype=np.uint8)),Rp)
    assert len(W)==24
    J=np.ones((1,40),dtype=np.uint8)
    Wcomp=[];cur=rref_rows(J)
    for w in W:
        trial=rref_rows(np.vstack((cur,w)))
        if len(trial)>len(cur):Wcomp.append(w);cur=trial
    assert len(Wcomp)==23
    Wrad=[]
    for w in Wcomp:
        ew=np.asarray(coordE(w),dtype=np.uint8)
        assert not np.any((Pi@ew)%2)
        Wrad.append(coords_for_column_basis(B,ew))
    Wrad=rref_rows(np.asarray(Wrad,dtype=np.uint8))
    assert len(Wrad)==23 and same_rowspace(Wrad,closures["fixed_line"])

    out={
      "pass":4505,
      "theorem":"H1(PSp(4,3), apartment radical K/J) is F2^2 with three nonzero classes on one common 23D support",
      "cohomology":{"module_dimension":29,"dim_Z1":31,"dim_B1":29,"dim_H1":2,"nonzero_classes":3,"fixed_line_class_coordinates_in_computed_basis":fixed_coords.tolist()},
      "support":{"dimension":23,"all_three_nonzero_classes_same_support":True,"identified_as":"W/J = (K intersect rowspace(N))/J","profile":"8 | (1 | 14)","relation":"exactly Pass-4492 route-hull/sentinel support"},
      "negative_result":"The 6-dimensional radical composition factor is absent from the module closure of every nonzero H1 class.",
      "relation_to_pass4496":"Pass 4496 independently computes dim H1=2 on the irreducible middle 8-space. Pass 4505 computes the different cohomology H1(G,K/J) of the full 29D apartment radical.",
      "boundary":"This is H1(G,K/J), including the fixed-line connecting obstruction. It is not a computation of the full Ext^1_G(H10,K/J) group, whose particular apartment extension is already proved nonsplit in Pass 4488."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=="__main__":raise SystemExit(main())
