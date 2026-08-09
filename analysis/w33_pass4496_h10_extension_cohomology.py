#!/usr/bin/env python3
"""Pass 4496: exact cohomology class of the protected H10=1|8|1 module.

This refines Passes 4488 and 4490--4494.  Those passes prove nonsplitting and
localize a concrete cocycle.  Here we compute the complete relevant H^1:

  dim Z^1(PSp(4,3),V8)=10,
  dim B^1(PSp(4,3),V8)=8,
  dim H^1(PSp(4,3),V8)=2.

The outer PGSp involution swaps a chosen basis of H^1, so its unique nonzero
fixed class is their sum.  After the invariant symplectic identification
V8^* ~= V8, BOTH adjacent extension cocycles in H10=1|8|1 represent this same
outer-fixed nonzero class.

An exhaustive cyclic-submodule scan also proves the invariant-submodule lattice
of H10 is exactly 0 < 1 < 9 < 10: the module is genuinely uniserial.
"""
from __future__ import annotations
import json
from collections import deque, Counter
from pathlib import Path
import numpy as np

from w33_pass4495_4502_distance_prism_reconstruction import (
    geometry, transvection3, build_line_perm, perm_group, J3
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_PASS4496_H10_EXTENSION_COHOMOLOGY.json"

def rref2(M):
    A=np.array(M,dtype=np.uint8).copy();m,n=A.shape;piv=[];r=0
    for c in range(n):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows): continue
        rr=r+int(rows[0])
        if rr!=r: A[[r,rr]]=A[[rr,r]]
        for i in range(m):
            if i!=r and A[i,c]: A[i]^=A[r]
        piv.append(c);r+=1
        if r==m: break
    return A,piv
def rank2(M): return len(rref2(M)[1])
def nullspace2(M):
    R,piv=rref2(M);n=R.shape[1];free=[j for j in range(n) if j not in piv];out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8);x[f]=1
        for i,p in reversed(list(enumerate(piv))):
            x[p]=int(np.dot(R[i],x)%2)
        out.append(x)
    return out
def inv2(M):
    M=np.array(M,dtype=np.uint8);n=M.shape[0]
    A=np.concatenate([M.copy(),np.eye(n,dtype=np.uint8)],axis=1);r=0
    for c in range(n):
        rr=next(i for i in range(r,n) if A[i,c])
        if rr!=r: A[[r,rr]]=A[[rr,r]]
        for i in range(n):
            if i!=r and A[i,c]: A[i]^=A[r]
        r+=1
    return A[:,n:]
def permute_vector(v,p):
    out=np.zeros_like(v)
    for i,j in enumerate(p): out[j]=v[i]
    return out
def matrix_group(gens):
    n=gens[0].shape[0];I=np.eye(n,dtype=np.uint8);seen={I.tobytes():I};Q=deque([I])
    while Q:
        a=Q.popleft()
        for g in gens:
            c=(g@a)%2;k=c.tobytes()
            if k not in seen: seen[k]=c;Q.append(c)
    return list(seen.values())
def add_bitrow(piv,x):
    y=x
    while y:
        p=y.bit_length()-1
        if p in piv: y^=piv[p]
        else: piv[p]=y;return
def vals_to_bits(vals):
    m=0;n=len(vals[0])
    for gi,v in enumerate(vals):
        for j,b in enumerate(v):
            if b: m|=1<<(gi*n+j)
    return m

def h1_data(gens):
    """Cocycle relations from the full Cayley graph, without a presentation."""
    n=gens[0].shape[0];ng=len(gens);I=np.eye(n,dtype=np.uint8)
    genforms=[[1<<(gi*n+j) for j in range(n)] for gi in range(ng)]
    def symapply(M,forms):
        out=[]
        for i in range(n):
            z=0
            for j in np.flatnonzero(M[i]): z^=forms[int(j)]
            out.append(z)
        return out
    seen={I.tobytes():(I,[0]*n)};Q=deque([I]);eqpiv={}
    while Q:
        a=Q.popleft();fa=seen[a.tobytes()][1]
        for gi,g in enumerate(gens):
            c=(g@a)%2
            gf=symapply(g,fa)
            fc=[genforms[gi][i]^gf[i] for i in range(n)]
            k=c.tobytes()
            if k not in seen:
                seen[k]=(c,fc);Q.append(c)
            else:
                old=seen[k][1]
                for i in range(n):
                    e=old[i]^fc[i]
                    if e:add_bitrow(eqpiv,e)
    eqrows=list(eqpiv.values())
    E=np.array([[(x>>j)&1 for j in range(ng*n)] for x in eqrows],dtype=np.uint8)
    Z=nullspace2(E)
    cob=np.vstack([g^I for g in gens])
    Cob=[cob[:,j].copy() for j in range(n)]
    basis=Cob.copy();Qreps=[]
    for z in Z:
        if rank2(np.vstack(basis+[z]))==len(basis)+1:
            basis.append(z);Qreps.append(z)
    B=np.column_stack(basis);_,rp=rref2(B.T);rr=rp[:len(basis)];L=inv2(B[rr,:])
    def coords(v):
        v=np.array(v,dtype=np.uint8)
        c=(L@v[rr])%2
        assert np.array_equal((B@c)%2,v)
        return c
    return {"seen":seen,"eqrows":eqrows,"Z":Z,"Cob":Cob,"Qreps":Qreps,
            "basis":basis,"coords":coords,"dimZ":len(Z),
            "dimB":rank2(cob),"dimH":len(Qreps)}

def eval_forms(forms,assignment):
    return np.array([(m&assignment).bit_count()&1 for m in forms],dtype=np.uint8)

def cyclic_span_dim(v,gens):
    piv={};Q=[np.array(v,dtype=np.uint8)]
    while Q:
        x=Q.pop();m=sum(int(b)<<i for i,b in enumerate(x));y=m
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:
                piv[p]=y
                for g in gens:Q.append((g@x)%2)
                break
    return len(piv)

def main():
    pts,pidx,lines,Astar,apartments,masks,H=geometry()
    all_trans=[build_line_perm(transvection3(v),pts,pidx,lines) for v in pts]
    selected=[];Gperm={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(selected+[p])
        if len(trial)>len(Gperm):
            selected.append(p);Gperm=trial
        if len(Gperm)==25920:break
    assert len(selected)==5 and len(Gperm)==25920

    _,piv=rref2(Astar);piv=piv[:10];B10=Astar[:,piv]
    _,rp=rref2(B10.T);rows=rp[:10];left=inv2(B10[rows,:])
    def q10(p):
        cols=[]
        for j in range(10):
            y=permute_vector(B10[:,j],p);c=(left@y[rows])%2
            assert np.array_equal((B10@c)%2,y);cols.append(c)
        return np.column_stack(cols).astype(np.uint8)
    G10=[q10(p) for p in selected]
    assert len(matrix_group(G10))==25920
    F10=Astar[np.ix_(piv,piv)].astype(np.uint8);assert rank2(F10)==10

    I10=np.eye(10,dtype=np.uint8)
    fixed=nullspace2(np.vstack([g^I10 for g in G10]))
    assert len(fixed)==1;v=fixed[0]
    vperp=nullspace2((v.reshape(1,-1)@F10)%2)
    Ucols=[v.copy()]
    for x in vperp:
        if rank2(np.column_stack(Ucols+[x]))==len(Ucols)+1:Ucols.append(x)
        if len(Ucols)==9:break
    U=np.column_stack(Ucols);assert rank2(U)==9
    _,urp=rref2(U.T);ur=urp[:9];Uleft=inv2(U[ur,:])
    def q8(g):
        cols=[]
        for j in range(1,9):
            y=(g@U[:,j])%2;c=(Uleft@y[ur])%2
            assert np.array_equal((U@c)%2,y);cols.append(c[1:])
        return np.column_stack(cols).astype(np.uint8)
    G8=[q8(g) for g in G10]
    F8=((U.T@F10@U)%2)[1:,1:];assert rank2(F8)==8
    assert len(matrix_group(G8))==25920

    cyclic=Counter()
    for m in range(1,1<<10):
        x=np.array([(m>>i)&1 for i in range(10)],dtype=np.uint8)
        cyclic[cyclic_span_dim(x,G10)]+=1
    assert cyclic==Counter({10:512,9:510,1:1})

    hd=h1_data(G8)
    assert len(hd["seen"])==25920
    assert hd["dimZ"]==10 and hd["dimB"]==8 and hd["dimH"]==2

    tvec=None
    for e in np.eye(10,dtype=np.uint8).T:
        if rank2(np.column_stack([U,e]))==10:tvec=e;break
    P10=np.column_stack([v,U[:,1:9],tvec]);Pinv=inv2(P10)
    Mad=[(Pinv@g@P10)%2 for g in G10]
    assert all(np.array_equal(m[1:9,1:9],g) for m,g in zip(Mad,G8))

    topvals=[m[1:9,9].copy() for m in Mad]
    topvec=np.concatenate(topvals)
    topcls=hd["coords"](topvec)[-2:]
    assert topcls.any()

    FinvT=inv2(F8.T)
    bottomvals=[]
    for m,g in zip(Mad,G8):
        alpha=m[0,1:9].reshape(1,-1)
        d=(alpha@inv2(g)).reshape(-1)%2
        bottomvals.append((FinvT@d)%2)
    bottomvec=np.concatenate(bottomvals)
    bottomcls=hd["coords"](bottomvec)[-2:]
    assert bottomcls.any() and np.array_equal(bottomcls,topcls)

    outer3=np.diag([1,2,1,2])%3
    assert np.array_equal((outer3.T@J3@outer3)%3,(2*J3)%3)
    outerp=build_line_perm(outer3,pts,pidx,lines)
    O10=q10(outerp);O8=q8(O10);Oinv=inv2(O8)
    def outer_on_cocycle(vec):
        assignment=vals_to_bits([vec[i*8:(i+1)*8] for i in range(5)])
        vals=[]
        for g in G8:
            h=(Oinv@g@O8)%2
            forms=hd["seen"][h.tobytes()][1]
            vals.append((O8@eval_forms(forms,assignment))%2)
        return np.concatenate(vals)
    qactions=[]
    for qrep in hd["Qreps"]:
        qactions.append(hd["coords"](outer_on_cocycle(qrep))[-2:].tolist())
    assert sorted(qactions)==[[0,1],[1,0]]
    outer_top=hd["coords"](outer_on_cocycle(topvec))[-2:]
    assert np.array_equal(outer_top,topcls)
    assert topcls.tolist()==[1,1] and bottomcls.tolist()==[1,1]

    result={
      "pass":4496,
      "theorem":"exact H1 and outer-invariant extension class of H10=1|8|1",
      "group":{"inner":"PSp(4,3)","order":25920,"generators":5},
      "module":{"dimension":10,"fixed_dimension":1,"fixed_perp_dimension":9,
        "composition":"1|8|1","cyclic_generator_dimensions":{"1":1,"9":510,"10":512},
        "invariant_submodule_lattice":"0 < 1 < 9 < 10","uniserial":True},
      "cohomology":{"middle_module_dimension":8,"dim_Z1":10,"dim_B1":8,"dim_H1":2,
        "outer_action_on_chosen_H1_basis":["e1 -> e2","e2 -> e1"],
        "unique_nonzero_outer_fixed_class":[1,1],"top_adjacent_extension_class":[1,1],
        "bottom_adjacent_extension_class_after_symplectic_dual_identification":[1,1]},
      "relation_to_prior_passes":"Passes 4488 and 4490--4494 proved/localized nonsplitting cocycles. Pass 4496 computes the complete relevant H1, proves uniseriality, and classifies the outer action.",
      "boundary":"H1 is computed for the actual 8-dimensional PSp module in this H10 filtration. No claim is made about unrelated Ext groups or physical registers."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS 4496")
    print("  H10 invariant lattice: 0 < 1 < 9 < 10 (uniserial)")
    print("  dim Z1/B1 = 10-8 = 2")
    print("  outer swaps H1 basis; unique nonzero fixed class=(1,1)")
    print("  both adjacent extension classes map to that fixed class")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
