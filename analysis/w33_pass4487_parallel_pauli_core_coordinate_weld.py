#!/usr/bin/env python3
"""Pass 4487 -- literal coordinate weld to the parallel Pass-4477/4478 8-core.

The parallel 4472--4479 verifier constructs H10 as I=im(A*) in a 10-coordinate
basis, finds its unique fixed line v, takes v^perp/<v>, and on that 8-space
builds the invariant plus-type quadratic form used in the E8/2E8 and four-Pauli
interpretations.

Passes 4485--4486 identify the repeated core intrinsically as U/J, where
U=ker(N) cap im(A*) and J=<1> in the 40-line module.

This verifier puts the two constructions in the same ambient line coordinates:

  * B10 v = j (the all-ones fixed vector),
  * B10(v^perp) = U exactly,
  * the parallel eight basis vectors map to a basis of U/J,
  * the parallel F8 Gram matrix equals the lift-defined protected Gram matrix,
  * the parallel invariant q8 equals q([A*b])=wt(Nb)/2 mod2 on all 256 classes.

Therefore the Pass-4477/4478 E8/Pauli 8-core is literally the same U/J quotient
that Pass 4485 found inside the apartment radical, not merely an abstract
isomorphic 8-dimensional representation.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import w33_pass4472_4479_apartment_module_thermo_ihara_pauli as par
from w33_pass4469_apartment_css_h10_intertwiner import nullspace_mod2, rref_rows
from w33_pass4470_apartment_h10_quadratic_fixed_layer import q_half_weight, solve_mod2
from w33_pass4481_apartment_radical_module_filtration import inter, contains

ROOT=Path(__file__).resolve().parents[1]
def rank2(M): return len(rref_rows(np.asarray(M,dtype=np.uint8)))
def same(A,B):
    A=rref_rows(A);B=rref_rows(B)
    return len(A)==len(B) and contains(A,B) and contains(B,A)
def main():
    pts,pidx,lines,lidx,A,Ast,edge_line,apartments,H=par.build_geometry()
    N=np.zeros((40,40),dtype=np.uint8)
    for li,L in enumerate(lines):N[list(L),li]=1
    I=rref_rows(Ast); R=rref_rows(nullspace_mod2(N)); Uamb=inter(R,I); Jamb=np.ones((1,40),dtype=np.uint8)

    # Rebuild the parallel 10D action/fixed-line construction exactly.
    all_trans=[par.build_line_perm(par.transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    selected=[]; group={tuple(range(40))}
    for p in all_trans:
        trial=par.perm_group(selected+[p])
        if len(trial)>len(group):selected.append(p);group=trial
        if len(group)==25920:break
    _,piv=par.rref2(Ast); piv=piv[:10]; B10=Ast[:,piv]
    _,rowp=par.rref2(B10.T); rows=rowp[:10]; left=par.inv2(B10[rows,:])
    def q10_matrix(p):
        cols=[]
        for j in range(10):
            y=par.permute_vector(B10[:,j],p); c=(left@y[rows])%2; cols.append(c)
        return np.column_stack(cols).astype(np.uint8)
    G10=[q10_matrix(p) for p in selected]
    F10=Ast[np.ix_(piv,piv)].astype(np.uint8)
    fixed=par.nullspace2(np.vstack([g^np.eye(10,dtype=np.uint8) for g in G10])); assert len(fixed)==1
    v=fixed[0]; vperp=par.nullspace2((v.reshape(1,-1)@F10)%2)
    Ucols=[v.copy()]
    for x in vperp:
        if par.rank2(np.column_stack(Ucols+[x]))==len(Ucols)+1:Ucols.append(x)
        if len(Ucols)==9:break
    U10=np.column_stack(Ucols)
    ambient=np.asarray([(B10@U10[:,j])%2 for j in range(9)],dtype=np.uint8)
    ambient_fixed=ambient[0]; ambient8=ambient[1:]

    # Parallel F8 and q8.
    F8par=((U10.T@F10@U10)%2)[1:,1:]
    _,urp=par.rref2(U10.T); ur=urp[:9]; Uleft=par.inv2(U10[ur,:])
    def q8_matrix(g):
        cols=[]
        for j in range(1,9):
            y=(g@U10[:,j])%2; c=(Uleft@y[ur])%2; cols.append(c[1:])
        return np.column_stack(cols).astype(np.uint8)
    G8=[q8_matrix(g) for g in G10]
    def q0(x):
        s=0
        for i in range(8):
            for j in range(i+1,8):
                if F8par[i,j]:s^=int(x[i]&x[j])
        return s
    eqs=[];rhs=[]
    for g in G8:
        for m in range(256):
            x=par.maskvec(m); gx=(g@x)%2; eqs.append(gx^x);rhs.append(q0(gx)^q0(x))
    ell,free=par.solve2(eqs,rhs); assert free==[]
    def qpar(c):return q0(c)^int(np.dot(ell,c)%2)

    # Independent lift-defined protected form/q on the same ambient8 basis.
    lifts=np.asarray([solve_mod2(Ast,y) for y in ambient8],dtype=np.uint8)
    F8ours=(lifts@Ast@lifts.T)%2
    qours=[];qparallel=[]
    for m in range(256):
        c=par.maskvec(m); b=(c@lifts)%2
        qours.append(q_half_weight((N@b)%2)); qparallel.append(qpar(c))

    checks={
      'PSp_group_25920':len(group)==25920,'fixed_line_unique':len(fixed)==1,
      'ambient_fixed_is_all_ones':np.array_equal(ambient_fixed,np.ones(40,dtype=np.uint8)),
      'ambient_vperp_is_U':same(ambient,Uamb),'ambient8_gives_UmodJ':rank2(np.vstack((Jamb,ambient8)))==9,
      'parallel_F8_rank8':rank2(F8par)==8,'F8_exact_coordinate_equality':np.array_equal(F8par,F8ours),
      'quadratic_exact_all256':qours==qparallel,'quadratic_counts':qours.count(0)==136 and qours.count(1)==120}
    assert all(checks.values()),checks
    out={'pass':4487,'theorem':'literal U/J to parallel E8/Pauli core coordinate weld',
      'identities':['B10*v = j','B10*vperp = U','parallel F8 = lift-defined protected F8','parallel q8 = wt(Nb)/2 on all 256 classes'],
      'core':{'literal_space':'U/J','dimension':8,'quadratic':'O+(8,2)','singular_nonzero':135,'anisotropic':120},
      'connection':'Parallel Passes 4477/4478 and Passes 4485/4486 use the same ambient U/J quotient in explicit coordinates.',
      'boundary':'This weld identifies finite representation/quadratic data only; it does not turn the radical copy into Pauli hardware or imply E8 dynamics.',
      'checks':{'passed':sum(checks.values()),'total':len(checks)}}
    p=ROOT/'data/PART_W33_PASS4487_PARALLEL_PAULI_CORE_COORDINATE_WELD.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
