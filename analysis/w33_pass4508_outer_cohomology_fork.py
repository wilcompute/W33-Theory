#!/usr/bin/env python3
"""Pass 4508 -- outside-box: a cohomological outer-action fork.

Two coefficient modules now independently have 2-dimensional first cohomology:

  Pass 4496: H^1(PSp(4,3), V8)  = F2^2, where V8 is the protected irreducible
             middle factor of H10=1|8|1.  PGSp's outer involution swaps a chosen
             H1 basis, so only one nonzero class is outer-fixed.

  Pass 4505: H^1(PSp(4,3), R29) = F2^2, where R29=K/J is the apartment radical.

This pass computes the outer action on the SECOND H1 directly.  It is the
identity.  Therefore every one of the three nonzero radical obstruction classes
is PGSp-outer-fixed, while the protected V8 cohomology has only one nonzero
outer-fixed class.

Same dimension does NOT mean same outer module.  This is a useful negative
identification: the two F2^2 cohomology spaces must not be silently conflated.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from w33_apartment_section_core import (
    actions_from_line_gens, build_geometry, build_line_perm, inv2, perm_group,
    perm_matrix, point_perm_from_matrix, quotient_model, transvection_matrix,
)
from w33_pass4496_h10_extension_cohomology import h1_data, eval_forms, vals_to_bits, nullspace2, rank2
from w33_pass4469_apartment_css_h10_intertwiner import rref_rows

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4508_OUTER_COHOMOLOGY_FORK.json'


def coords_for_column_basis(B,y):
    T=B.T.copy();m,n=T.shape;r=0;rows=[]
    for c in range(n):
        rr=next((i for i in range(r,m) if T[i,c]),None)
        if rr is None:continue
        if rr!=r:T[[r,rr]]=T[[rr,r]]
        for i in range(m):
            if i!=r and T[i,c]:T[i]^=T[r]
        rows.append(c);r+=1
        if r==m:break
    S=B[rows,:];c=(inv2(S)@np.asarray(y,dtype=np.uint8)[rows])%2
    assert np.array_equal((B@c)%2,np.asarray(y,dtype=np.uint8)%2);return c


def line_perm_from_matrix(M,pts,pidx,lines,lidx):
    pp=[]
    for p in pts:
        y=(np.asarray(M,dtype=int)@np.asarray(p,dtype=int))%3
        for x in y:
            if x:
                inv=1 if x==1 else 2;y=(inv*y)%3;break
        pp.append(pidx[tuple(int(z) for z in y)])
    return tuple(lidx[tuple(sorted(pp[i] for i in L))] for L in lines)


def main()->int:
    pts,pidx,lines,lidx,_,Astar,*_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    _,Ereps,Vreps,coordE,coordV,Pi=quotient_model(Astar)
    matrices=[transvection_matrix(v) for v in pts]
    line_trans=[build_line_perm(M,pts,pidx,lines,lidx) for M in matrices]
    selected=[];full={tuple(range(40))}
    for i,p in enumerate(line_trans):
        trial=perm_group([line_trans[j] for j in selected]+[p],40)
        if len(trial)>len(full):selected.append(i);full=trial
        if len(full)==25920:break
    gens=[line_trans[i] for i in selected];assert len(gens)==5 and len(full)==25920
    GE,GV=actions_from_line_gens(gens,Ereps,Vreps,coordE,coordV)

    Rrows=rref_rows(np.asarray(nullspace2(Pi),dtype=np.uint8));B=Rrows.T;assert B.shape==(39,29)
    rho=[]
    for ge in GE:
        rho.append(np.column_stack([coords_for_column_basis(B,(ge@B[:,j])%2) for j in range(29)]).astype(np.uint8))
    hd=h1_data(rho);assert (hd['dimZ'],hd['dimB'],hd['dimH'])==(31,29,2)

    # Outer PGSp similitude used independently in Pass 4496.
    outer3=np.diag([1,2,1,2])%3
    outerp=line_perm_from_matrix(outer3,pts,pidx,lines,lidx)
    OE=np.column_stack([coordE(perm_matrix(outerp)@e) for e in Ereps]).astype(np.uint8)
    OR=np.column_stack([coords_for_column_basis(B,(OE@B[:,j])%2) for j in range(29)]).astype(np.uint8)
    assert rank2(OR)==29 and np.array_equal((OR@OR)%2,np.eye(29,dtype=np.uint8))
    ORinv=inv2(OR)

    def outer_on_cocycle(vec):
        assignment=vals_to_bits([vec[i*29:(i+1)*29] for i in range(5)])
        vals=[]
        for g in rho:
            h=(ORinv@g@OR)%2
            forms=hd['seen'][h.tobytes()][1]
            vals.append((OR@eval_forms(forms,assignment))%2)
        return np.concatenate(vals)

    qactions=[]
    for qrep in hd['Qreps']:
        qactions.append(hd['coords'](outer_on_cocycle(np.asarray(qrep,dtype=np.uint8)))[-2:].tolist())
    assert qactions==[[1,0],[0,1]],qactions

    p4496=json.loads((ROOT/'data/PART_W33_PASS4496_H10_EXTENSION_COHOMOLOGY.json').read_text())
    middle=p4496['cohomology']['outer_action_on_chosen_H1_basis']
    assert middle==['e1 -> e2','e2 -> e1']

    out={
      'pass':4508,
      'theorem':'outer-action fork between two dimension-2 PSp(4,3) cohomology spaces',
      'radical_H1':{'coefficient_module':'R29=K/J','dimension':2,'PGSp_outer_action':'identity','nonzero_outer_fixed_classes':3},
      'protected_middle_H1':{'coefficient_module':'V8 middle factor of H10=1|8|1','dimension':2,'PGSp_outer_action':'basis swap','nonzero_outer_fixed_classes':1,'owner':'Pass 4496'},
      'negative_identification':'The equal F2^2 dimensions do not define the same PGSp outer module; the two H1 spaces must not be identified by dimension alone.',
      'boundary':'This compares exact outer actions on two different coefficient-module cohomology groups. It does not assert a canonical map between those H1 spaces.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
