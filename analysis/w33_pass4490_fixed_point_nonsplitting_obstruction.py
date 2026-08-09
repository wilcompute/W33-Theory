#!/usr/bin/env python3
"""Pass 4490 -- fixed-point obstruction behind the nonsplit apartment extension.

Pass 4488 proved by a 1660-equation affine system that

    0 -> K/J -> M/J -> M/K -> 0

has no PSp(4,3)-equivariant section.  The conceptual reason is much smaller.

M=F2^40 is the transitive line permutation module.  Its fixed space is exactly
J=<1>.  Therefore the quotient E=M/J has no fixed vector.  By contrast the
protected quotient V=M/K=H10 has a unique fixed line (Passes 187,4472).

An equivariant section s:V->E would have to send the nonzero fixed vector of V
to a nonzero fixed vector of E.  None exists.  Hence the extension is nonsplit.

Equivalently, in the long exact fixed-point/cohomology sequence, the connecting
map V^G -> H^1(G,K/J) is injective and sends the protected fixed class to a
nonzero extension cocycle.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry,transvection_matrix,build_line_perm,perm_group
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2,rref_rows

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
def main():
    pts,pidx,lines,lidx,A,Ast,*_=build_geometry();J=np.ones((1,40),dtype=np.uint8);K=rref_rows(nullspace_mod2(Ast))
    Ereps=extend(J);Vreps=extend(K);BE=np.vstack((J,Ereps));BV=np.vstack((K,Vreps));BEi=inv2(BE);BVi=inv2(BV)
    def cE(x):return ((x@BEi)%2)[1:]
    def cV(x):return ((x@BVi)%2)[30:]
    allg=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts];gens=[];G={tuple(range(40))}
    for p in allg:
        T=perm_group(gens+[p])
        if len(T)>len(G):gens.append(p);G=T
        if len(G)==25920:break
    GE=[];GV=[]
    for p in gens:
        P=pm(p);GE.append(np.column_stack([cE(P@e) for e in Ereps]));GV.append(np.column_stack([cV(P@v) for v in Vreps]))
    fixedE=nullspace_mod2(np.vstack([g^np.eye(39,dtype=np.uint8) for g in GE]));fixedV=nullspace_mod2(np.vstack([g^np.eye(10,dtype=np.uint8) for g in GV]))
    # Ambient M fixed space, and radical fixed space by injection into E.
    fixedM=nullspace_mod2(np.vstack([pm(p)^np.eye(40,dtype=np.uint8) for p in gens]))
    checks={'group_25920':len(G)==25920,'ambient_fixed_exactly_J':len(fixedM)==1 and np.array_equal(fixedM[0],np.ones(40,dtype=np.uint8)),
      'E_fixed_dimension_0':len(fixedE)==0,'V_fixed_dimension_1':len(fixedV)==1,'radical_fixed_dimension_0_by_injection':len(fixedE)==0,
      'fixed_point_dimension_mismatch':len(fixedE)<len(fixedV)}
    assert all(checks.values()),checks
    out={'pass':4490,'theorem':'W33 fixed-point nonsplitting obstruction theorem','group':'PSp(4,3)','sequence':'0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0',
      'fixed_dimensions':{'M':1,'K/J':0,'E=M/J':0,'V=H10':1},'obstruction':'An equivariant section would lift the unique nonzero fixed H10 class to a nonzero fixed E class, but E^G=0.',
      'cohomology':'The connecting map V^G -> H^1(G,K/J) is injective on the 1D fixed line, so the extension class is nonzero.',
      'relation_to_4488':'Explains conceptually the rank(A)=389, rank([A|b])=390 affine inconsistency.',
      'boundary':'Representation-theoretic fixed-point obstruction only; non-equivariant or symmetry-breaking decoders are not excluded.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4490_FIXED_POINT_NONSPLITTING_OBSTRUCTION.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
