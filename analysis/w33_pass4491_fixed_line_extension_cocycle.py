#!/usr/bin/env python3
"""Pass 4491 -- localize the nonsplitting cocycle inside the radical.

For the nonsplit sequence 0->K/J->E=M/J->V=M/K->0, let v be the unique
PSp-fixed class in V and choose the deterministic coordinate lift e in E.
The generator defects

    c_g = G_E(g)e - e

lie in the radical and represent the connecting H^1 class from Pass 4490.
Their PSp-module closure has dimension 23.  In ambient line coordinates it is
exactly

    (K intersect R^perp)/J,

where R=ker N is the 15-dimensional route code and R^perp=rowspace(N) has
dimension 25.  The ambient intersection has dimension 24 and invariant chain

    J < U < I < K intersect R^perp

with dimensions 1<9<10<24, hence cocycle-support profile

    8 | 1 | 14.

The same affine support test proves the cocycle cannot be gauged into I/J
(dim9): coefficient/augmented ranks differ by one there.  It can be represented
inside (K intersect R^perp)/J.  Thus the 6-dimensional route-side factor of the
full radical profile 8|(6+1)|14 is not needed by this fixed-line obstruction.

Boundary: this is support of one canonical/cohomologous extension cocycle and a
no-gauge-into-I/J certificate; it is not a physical error path or energy flow.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,transvection_matrix,build_line_perm,perm_group
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2,rref_rows
from w33_pass4481_apartment_radical_module_filtration import inter,contains

ROOT=Path(__file__).resolve().parents[1]
def rank2(M):return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def inv2(M):
    M=np.asarray(M,dtype=np.uint8);n=len(M);A=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if A[i,c]);A[[c,r]]=A[[r,c]]
        for i in range(n):
            if i!=c and A[i,c]:A[i]^=A[c]
    return A[:,n:]
def extend(B):
    cur=rref_rows(B);out=[];r=len(cur)
    for e in np.eye(40,dtype=np.uint8):
        t=rref_rows(np.vstack((cur,e)))
        if len(t)>r:out.append(e);cur=t;r+=1
    return np.asarray(out,dtype=np.uint8)
def pm(p):
    P=np.zeros((40,40),dtype=np.uint8)
    for i,j in enumerate(p):P[j,i]=1
    return P
def solve(M,b):
    A=np.hstack((np.asarray(M,dtype=np.uint8).copy(),np.asarray(b,dtype=np.uint8).reshape(-1,1)));m,n=M.shape;r=0;piv=[]
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(m):
            if i!=r and A[i,c]:A[i]^=A[r]
        piv.append(c);r+=1
    for i in range(r,m):
        if not A[i,:n].any() and A[i,n]:raise ValueError
    x=np.zeros(n,dtype=np.uint8)
    for rr,c in enumerate(piv):x[c]=A[rr,n]
    return x
def same(A,B):
    A=rref_rows(A);B=rref_rows(B)
    return len(A)==len(B) and contains(A,B) and contains(B,A)
def main():
    pts,pidx,lines,lidx,A,Ast,*_=build_geometry();N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    J=np.ones((1,40),dtype=np.uint8);K=rref_rows(nullspace_mod2(Ast));R=rref_rows(nullspace_mod2(N));Rp=rref_rows(N);I=rref_rows(Ast);U=inter(R,I);KRp=inter(K,Rp)
    Er=extend(J);Vr=extend(K);BE=np.vstack((J,Er));BV=np.vstack((K,Vr));BEi=inv2(BE);BVi=inv2(BV)
    def cE(x):return ((x@BEi)%2)[1:]
    def cV(x):return ((x@BVi)%2)[30:]
    allg=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];GG={tuple(range(40))}
    for p in allg:
        T=perm_group(gens+[p])
        if len(T)>len(GG):gens.append(p);GG=T
        if len(GG)==25920:break
    GE=[];GV=[]
    for p in gens:
        P=pm(p);GE.append(np.column_stack([cE(P@e) for e in Er]));GV.append(np.column_stack([cV(P@v) for v in Vr]))
    Pi=np.column_stack([cV(e) for e in Er]); fixed=nullspace_mod2(np.vstack([g^np.eye(10,dtype=np.uint8) for g in GV]));v=fixed[0];e=solve(Pi,v)
    defects=rref_rows(np.asarray([(g@e)^e for g in GE],dtype=np.uint8));closure=defects.copy();old=-1
    while len(closure)!=old:
        old=len(closure);closure=rref_rows(np.vstack((closure,*[(g@x)%2 for g in GE for x in closure])))
    Wamb=rref_rows(np.vstack((J,*[(x@Er)%2 for x in closure])))
    # Affine support feasibility: defects may be gauged into L iff there is lift e' over v fixed modulo L.
    def support_test(Lamb):
        LE=rref_rows(np.asarray([cE(x) for x in rref_rows(Lamb)],dtype=np.uint8));Ann=nullspace_mod2(LE)
        blocks=[Pi];rhs=[v]
        for g in GE:blocks.append((Ann@(g^np.eye(39,dtype=np.uint8)))%2);rhs.append(np.zeros(len(Ann),dtype=np.uint8))
        AA=np.vstack(blocks);bb=np.concatenate(rhs);return rank2(AA),rank2(np.column_stack((AA,bb))),len(LE)
    rI= support_test(I); rW=support_test(KRp)
    checks={'group25920':len(GG)==25920,'fixed_line_unique':len(fixed)==1,'defects_in_radical':all(not np.any((Pi@x)%2) for x in defects),
      'closure_dim23':len(closure)==23,'ambient_closure_dim24':len(Wamb)==24,'ambient_closure_is_KcapRperp':same(Wamb,KRp),
      'dims_J_U_I_KRp':(1,len(U),len(I),len(KRp))==(1,9,10,24),'support_profile_8_1_14':(len(U)-1,len(I)-len(U),len(KRp)-len(I))==(8,1,14),
      'cannot_gauge_into_IoverJ':rI[0]+1==rI[1],'can_gauge_into_KRp_over_J':rW[0]==rW[1]}
    assert all(checks.values()),checks
    out={'pass':4491,'theorem':'W33 fixed-line extension cocycle support theorem','cocycle':'c_g=G_E(g)e-e for a lift of the unique fixed v in H10',
      'support':{'module':'(K intersect R^perp)/J','dimension':23,'ambient_dimension':24,'profile':'8 | 1 | 14','full_radical_profile':'8 | (6+1) | 14'},
      'gauge_tests':{'I/J':{'dimension':9,'rank_coefficient':rI[0],'rank_augmented':rI[1],'possible':False},'KcapRperp/J':{'dimension':23,'rank_coefficient':rW[0],'rank_augmented':rW[1],'possible':True}},
      'interpretation':'The fixed-line nonsplitting cocycle needs the repeated 8-core, the trivial 1, and the 14-layer, but not the route-side 6-layer.',
      'boundary':'Cohomological/module support only; not a physical error current, transport energy, or hardware fault path.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4491_FIXED_LINE_EXTENSION_COCYCLE.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
