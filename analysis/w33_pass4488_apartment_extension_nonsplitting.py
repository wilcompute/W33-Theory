#!/usr/bin/env python3
"""Pass 4488 -- the 39D apartment code is a nonsplit PSp(4,3)-extension.

Pass 4481 gives the exact sequence

    0 -> K/J (29) -> M/J (39) -> M/K (10) -> 0,

with M=F_2^40, J=<1>, K=ker(A*), and protected quotient M/K ~= H10.
Pass 4485 shows the same 8-core U/J occurs on both sides.  This pass asks the
stronger question: does the 39-space split equivariantly as 29 + 10?

Using four generators of PSp(4,3), write E=M/J and V=M/K in explicit quotient
bases.  Let Pi:E->V be the canonical quotient.  An equivariant section S would
satisfy

    Pi S = I_10,
    G_E S = S G_V

for every generator.  These are 1660 affine linear equations over F2 in the
390 entries of S.  The exact ranks are

    rank(A)=389,   rank([A|b])=390,

so no section exists: the extension is nonsplit.

The homogeneous intertwiner equations have nullity one.  Their unique nonzero
solution has rank 9, has Pi S=0, and is exactly the map

    T : M/K -> M/J,
    T([b]) = [A* b].

Its image is I/J (dimension 9) inside the radical K/J and its kernel is the
one-dimensional fixed line.  Thus symmetry allows only a 10->9 return channel
into the radical, not a protected 10-dimensional invariant complement.

Boundary: nonsplitting is a modular representation statement.  It does not
forbid non-equivariant software decoding or symmetry-breaking hardware; it says
there is no PSp-equivariant linear section of this exact sequence.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry, transvection_matrix, build_line_perm, perm_group
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows

ROOT=Path(__file__).resolve().parents[1]
def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def inv2(M):
    M=np.asarray(M,dtype=np.uint8); n=len(M); A=np.hstack((M.copy(),np.eye(n,dtype=np.uint8)))
    for c in range(n):
        r=next(i for i in range(c,n) if A[i,c]); A[[c,r]]=A[[r,c]]
        for i in range(n):
            if i!=c and A[i,c]:A[i]^=A[c]
    return A[:,n:]
def extend(small):
    cur=rref_rows(small); reps=[]; r=len(cur)
    for v in np.eye(40,dtype=np.uint8):
        trial=rref_rows(np.vstack((cur,v)))
        if len(trial)>r:reps.append(v.copy());cur=trial;r+=1
        if r==40:break
    return np.asarray(reps,dtype=np.uint8)
def perm_matrix(p):
    P=np.zeros((40,40),dtype=np.uint8)
    for i,j in enumerate(p):P[j,i]=1
    return P
def same_colspace(A,B): return rank2(A)==rank2(B)==rank2(np.hstack((A,B)))
def main():
    pts,pidx,lines,lidx,A,Ast,edge_line,apartments,H=build_geometry(); J=np.ones((1,40),dtype=np.uint8); K=rref_rows(nullspace_mod2(Ast)); I=rref_rows(Ast)
    Ereps=extend(J); Vreps=extend(K); BE=np.vstack((J,Ereps)); BV=np.vstack((K,Vreps)); BEi=inv2(BE); BVi=inv2(BV)
    def coordE(v):return ((v@BEi)%2)[1:]
    def coordV(v):return ((v@BVi)%2)[30:]
    # Deterministic PSp generators, then remove redundant ones.
    all_trans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]; gens=[]; group={tuple(range(40))}
    for p in all_trans:
        trial=perm_group(gens+[p])
        if len(trial)>len(group):gens.append(p);group=trial
        if len(group)==25920:break
    changed=True
    while changed:
        changed=False
        for i in range(len(gens)):
            trial=perm_group(gens[:i]+gens[i+1:])
            if len(trial)==25920:gens=gens[:i]+gens[i+1:];changed=True;break
    GEs=[];GVs=[]
    for p in gens:
        P=perm_matrix(p)
        GEs.append(np.column_stack([coordE(P@e) for e in Ereps]).astype(np.uint8))
        GVs.append(np.column_stack([coordV(P@v) for v in Vreps]).astype(np.uint8))
    Pi=np.column_stack([coordV(e) for e in Ereps]).astype(np.uint8)
    I10=np.eye(10,dtype=np.uint8); I39=np.eye(39,dtype=np.uint8)
    Hblocks=[(np.kron(I10,GE)^np.kron(GV.T,I39)).astype(np.uint8) for GE,GV in zip(GEs,GVs)]
    Hmat=np.vstack(Hblocks); Aaff=np.vstack((np.kron(I10,Pi).astype(np.uint8),Hmat)); baff=np.concatenate((I10.reshape(-1,order='F'),np.zeros(Hmat.shape[0],dtype=np.uint8)))
    rankA=rank2(Aaff); rankAug=rank2(np.column_stack((Aaff,baff))); hom_null=nullspace_mod2(Hmat)
    assert len(hom_null)==1
    S0=hom_null[0].reshape((39,10),order='F')
    # Canonical A* return map T([b])=[A*b].
    T=np.column_stack([coordE((Ast@v)%2) for v in Vreps]).astype(np.uint8)
    Icoords=np.column_stack([coordE(v) for v in I]).astype(np.uint8)
    checks={
      'dims':(len(K),len(Ereps),len(Vreps))==(30,39,10),'group_PSp25920':len(group)==25920,
      'quotient_projection_rank10':rank2(Pi)==10,'hom_nullity_one':len(hom_null)==1,
      'affine_section_inconsistent':rankA==389 and rankAug==390,'unique_nonzero_Hom_rank9':rank2(S0)==9,
      'unique_Hom_lands_in_radical':not np.any((Pi@S0)%2),'Astar_return_rank9':rank2(T)==9,
      'Astar_return_is_unique_Hom':np.array_equal(T,S0),'Astar_return_projection_zero':not np.any((Pi@T)%2),
      'image_is_I_mod_J':same_colspace(T,Icoords),'kernel_dimension_one':10-rank2(T)==1}
    for i,(GE,GV) in enumerate(zip(GEs,GVs)):checks[f'T_equivariant_gen{i}']=np.array_equal((GE@T)%2,(T@GV)%2)
    assert all(checks.values()),checks
    out={'pass':4488,'theorem':'W33 apartment-code nonsplit protected/radical extension theorem',
      'sequence':'0 -> K/J (29) -> M/J (39) -> M/K=H10 (10) -> 0','splits_PSp_equivariantly':False,
      'section_system':{'unknowns':390,'equations':int(Aaff.shape[0]),'rank_coefficient':rankA,'rank_augmented':rankAug},
      'Hom_PSp_H10_to_Cap':{'dimension':1,'unique_nonzero_rank':9,'formula':'T([b])=[A* b] mod J','image':'I/J inside radical','kernel_dimension':1,'projection_to_H10':'zero'},
      'interpretation':'The only nonzero equivariant return channel folds H10 into the radical and kills one fixed line; no invariant 10D complement exists.',
      'boundary':'Does not forbid non-equivariant decoding or symmetry-breaking hardware; it forbids a PSp-equivariant linear section only.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4488_APARTMENT_EXTENSION_NONSPLITTING.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
