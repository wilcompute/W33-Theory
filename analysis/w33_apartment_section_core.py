#!/usr/bin/env python3
"""Shared exact GF(2) apartment-extension section machinery.

Factored from Pass 4493 during the Pass-4503/4507 erratum so historical and new
section tests use one implementation without importing stale numerical claims.
"""
from __future__ import annotations

import itertools
from collections import deque
import numpy as np

from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import (
    build_geometry, build_line_perm, transvection_matrix,
)
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows


def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))


def inv2(M):
    M=np.asarray(M,dtype=np.uint8);n=M.shape[0]
    A=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if A[i,c])
        if r!=c:A[[c,r]]=A[[r,c]]
        for i in range(n):
            if i!=c and A[i,c]:A[i]^=A[c]
    return A[:,n:]


def extend(subspace):
    current=rref_rows(subspace);out=[];r=len(current);n=subspace.shape[1]
    for e in np.eye(n,dtype=np.uint8):
        trial=rref_rows(np.vstack((current,e)))
        if len(trial)>r:out.append(e.copy());current=trial;r+=1
        if r==n:break
    return np.asarray(out,dtype=np.uint8)


def normalize_projective(v):
    w=[int(x)%3 for x in v]
    for x in w:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in w)
    raise ValueError("zero projective vector")


def point_perm_from_matrix(M,pts,pidx):
    out=[]
    for x in pts:
        y=(M@np.asarray(x,dtype=int))%3
        out.append(pidx[normalize_projective(y)])
    return tuple(out)


def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))


def perm_group(gens,n=40):
    ident=tuple(range(n));seen={ident};Q=deque([ident])
    while Q:
        g=Q.popleft()
        for h in gens:
            for k in (compose(g,h),compose(h,g)):
                if k not in seen:seen.add(k);Q.append(k)
    return seen


def small_generating_set(group,n=40):
    ident=tuple(range(n));target=len(group);gens=[];current={ident}
    for g in sorted(group):
        if g in current:continue
        trial=perm_group(gens+[g],n)
        if len(trial)>len(current):gens.append(g);current=trial
        if len(current)==target:break
    assert len(current)==target
    changed=True
    while changed:
        changed=False
        for i in range(len(gens)):
            trial=gens[:i]+gens[i+1:]
            if len(perm_group(trial,n))==target:
                gens=trial;changed=True;break
    return gens


def line_perm_from_point_perm(p,lines,lidx):
    return tuple(lidx[frozenset(p[x] for x in L)] for L in lines)


def perm_matrix(p):
    n=len(p);P=np.zeros((n,n),dtype=np.uint8)
    for i,j in enumerate(p):P[j,i]=1
    return P


def quotient_model(Astar):
    J=np.ones((1,40),dtype=np.uint8);K=rref_rows(nullspace_mod2(Astar))
    Ereps=extend(J);Vreps=extend(K)
    BE=np.vstack((J,Ereps));BV=np.vstack((K,Vreps));BEi=inv2(BE);BVi=inv2(BV)
    def coordE(v):return ((np.asarray(v,dtype=np.uint8)@BEi)%2)[1:]
    def coordV(v):return ((np.asarray(v,dtype=np.uint8)@BVi)%2)[30:]
    Pi=np.column_stack([coordV(e) for e in Ereps]).astype(np.uint8)
    return K,Ereps,Vreps,coordE,coordV,Pi


def actions_from_line_gens(line_gens,Ereps,Vreps,coordE,coordV):
    GE=[];GV=[]
    for p in line_gens:
        P=perm_matrix(p)
        GE.append(np.column_stack([coordE(P@e) for e in Ereps]).astype(np.uint8))
        GV.append(np.column_stack([coordV(P@v) for v in Vreps]).astype(np.uint8))
    return GE,GV


def section_system(Pi,GE,GV):
    I10=np.eye(10,dtype=np.uint8);I39=np.eye(39,dtype=np.uint8)
    blocks=[np.kron(I10,Pi).astype(np.uint8)];rhs=[I10.reshape(-1,order="F")]
    for e,v in zip(GE,GV):
        blocks.append((np.kron(I10,e)^np.kron(v.T,I39)).astype(np.uint8))
        rhs.append(np.zeros(390,dtype=np.uint8))
    A=np.vstack(blocks);b=np.concatenate(rhs);r=rank2(A);ra=rank2(np.column_stack((A,b)))
    return {"rank_coefficient":r,"rank_augmented":ra,"consistent":r==ra,
            "affine_dimension":390-r if r==ra else None,"equations":int(A.shape[0]),"unknowns":390}


def fixed_dimension(actions,n):
    if not actions:return n
    I=np.eye(n,dtype=np.uint8)
    return n-rank2(np.vstack([g^I for g in actions]))


def first_apartment(Astar):
    for C in itertools.combinations(range(40),4):
        deg=[sum(int(Astar[x,y]) for y in C if y!=x) for x in C]
        if deg==[2,2,2,2]:return frozenset(C)
    raise AssertionError("no apartment")
