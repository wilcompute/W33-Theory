#!/usr/bin/env python3
"""Pass 4509 -- outside-box: restriction barcode of the two-bit radical obstruction.

Pass 4505 gives H^1(G,R29)=F2^2 with three nonzero classes.  Pass 4503 says
all five maximal subgroup types retain the full 39->10 nonsplitting, while an
incident flag stabilizer of order 162 splits.  This pass computes the actual
restriction behavior of the radical H1 classes.

Result, expressed as kernel dimensions of res_H:H1(G,R29)->H1(H,R29):

  maximal 2^4:A5, order 960              0
  maximal spread S6, order 720           0
  maximal line stabilizer, order 648     1
  maximal point stabilizer, order 648    1
  maximal class45 centralizer, order576  0
  incident flag = point cap line, 162    2

The point and line kernels are DISTINCT one-dimensional subspaces.  The canonical
Pass-4491 fixed-line class dies on the point stabilizer; a different nonzero
class dies on the line stabilizer.  Their incident intersection kills the entire
2D H1.  This gives a cohomological explanation of the corrected geometric
threshold: a point or line removes one obstruction charge, while a flag removes
both.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
import numpy as np

from w33_apartment_section_core import (
    actions_from_line_gens, build_geometry, build_line_perm, compose,
    line_perm_from_point_perm, perm_group, perm_matrix, point_perm_from_matrix,
    quotient_model, small_generating_set, transvection_matrix,
)
from w33_pass4503_maximal_subgroup_splitting_erratum import enumerate_spreads, generated_limited
from w33_pass4505_radical_h1_three_charges import coords_for_column_basis, solve2
from w33_pass4496_h10_extension_cohomology import h1_data, eval_forms, vals_to_bits, nullspace2, rank2
from w33_pass4469_apartment_css_h10_intertwiner import rref_rows

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4509_COHOMOLOGY_RESTRICTION_BARCODE.json'


def main()->int:
    pts,pidx,lines,lidx,_,Astar,*_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    _,Ereps,Vreps,coordE,coordV,Pi=quotient_model(Astar)
    matrices=[transvection_matrix(v) for v in pts]
    point_trans=[point_perm_from_matrix(M,pts,pidx) for M in matrices]
    line_trans=[build_line_perm(M,pts,pidx,lines,lidx) for M in matrices]
    selected=[];full={tuple(range(40))}
    for i,p in enumerate(line_trans):
        trial=perm_group([line_trans[j] for j in selected]+[p],40)
        if len(trial)>len(full):selected.append(i);full=trial
        if len(full)==25920:break
    full_point=perm_group([point_trans[i] for i in selected],40)
    assert len(full)==len(full_point)==25920
    gens=[line_trans[i] for i in selected]
    GE,GV=actions_from_line_gens(gens,Ereps,Vreps,coordE,coordV)

    Rrows=rref_rows(np.asarray(nullspace2(Pi),dtype=np.uint8));B=Rrows.T;assert B.shape==(39,29)
    def radical_action(p):
        P=perm_matrix(p)
        ge=np.column_stack([coordE(P@e) for e in Ereps]).astype(np.uint8)
        return np.column_stack([coords_for_column_basis(B,(ge@B[:,j])%2) for j in range(29)]).astype(np.uint8)
    rho=[radical_action(p) for p in gens]
    hd=h1_data(rho);assert hd['dimH']==2 and hd['dimZ']==31 and hd['dimB']==29

    # Canonical fixed-line connecting class.
    I10=np.eye(10,dtype=np.uint8)
    fixed=nullspace2(np.vstack([g^I10 for g in GV]));assert len(fixed)==1
    v=np.asarray(fixed[0],dtype=np.uint8);e=solve2(Pi,v)
    fixed_vals=[]
    for ge in GE:
        c=((ge@e)%2)^e;fixed_vals.append(coords_for_column_basis(B,c))
    fixed_vec=np.concatenate(fixed_vals)
    assert hd['coords'](fixed_vec)[-2:].any()

    span=rref_rows(np.vstack((np.asarray(hd['Cob'],dtype=np.uint8),fixed_vec)))
    second=None
    for q in hd['Qreps']:
        q=np.asarray(q,dtype=np.uint8)
        if rank2(np.vstack((span,q)))>len(span):second=q;break
    assert second is not None
    reps={'fixed_line':fixed_vec,'second':second,'sum':fixed_vec^second}

    # Canonical maximal/natural subgroup representatives, exactly as Pass 4503.
    line_stab={g for g in full if g[0]==0}
    point_stab_point={g for g in full_point if g[0]==0}
    point_stab={line_perm_from_point_perm(g,lines,lidx) for g in point_stab_point}
    fp,fl=min((p,li) for li,L in enumerate(lines) for p in L)
    flag_point={g for g in full_point if g[fp]==fp and line_perm_from_point_perm(g,lines,lidx)[fl]==fl}
    flag={line_perm_from_point_perm(g,lines,lidx) for g in flag_point}
    assert flag==point_stab.intersection(line_stab) and len(flag)==162

    spreads=enumerate_spreads(lines);spread0=set(spreads[0])
    spread={g for g in full if {g[x] for x in spread0}==spread0};assert len(spread)==720
    ident=tuple(range(40));invols=[g for g in full if g!=ident and compose(g,g)==ident]
    t45=next(g for g in invols if sum(i==g[i] for i in range(40))==16)
    c576={g for g in full if compose(g,t45)==compose(t45,g)};assert len(c576)==576
    glist=sorted(full);rng=random.Random(4503);m20=None
    for _ in range(1000):
        a,b=rng.sample(glist,2);h=generated_limited([a,b],limit=2000)
        if len(h)==960:m20=h;break
    assert m20 is not None

    groups={'M20_960':m20,'spread_S6_720':spread,'line_648':line_stab,'point_648':point_stab,'class45_C576':c576,'incident_flag_162':flag}

    def restrict_is_zero(z,H):
        hgens=small_generating_set(H,40);mats=[radical_action(p) for p in hgens]
        assignment=vals_to_bits([z[i*29:(i+1)*29] for i in range(5)])
        vals=[]
        for m in mats:
            forms=hd['seen'][m.tobytes()][1]
            vals.append(eval_forms(forms,assignment))
        A=np.vstack([m^np.eye(29,dtype=np.uint8) for m in mats]);b=np.concatenate(vals)
        return rank2(A)==rank2(np.column_stack((A,b)))

    barcode={}
    for name,H in groups.items():
        killed=[c for c,z in reps.items() if restrict_is_zero(z,H)]
        # Kernel dimension in a 2D F2 space: 0 killed nonzero =>0; 1=>1; 3=>2.
        kd={0:0,1:1,3:2}[len(killed)]
        barcode[name]={'order':len(H),'killed_nonzero_classes':killed,'restriction_kernel_dimension':kd}

    assert barcode['M20_960']['restriction_kernel_dimension']==0
    assert barcode['spread_S6_720']['restriction_kernel_dimension']==0
    assert barcode['class45_C576']['restriction_kernel_dimension']==0
    assert barcode['point_648']['killed_nonzero_classes']==['fixed_line']
    assert barcode['line_648']['restriction_kernel_dimension']==1
    assert 'fixed_line' not in barcode['line_648']['killed_nonzero_classes']
    assert barcode['incident_flag_162']['restriction_kernel_dimension']==2
    assert set(barcode['incident_flag_162']['killed_nonzero_classes'])==set(reps)

    out={
      'pass':4509,
      'theorem':'two-bit radical obstruction restriction barcode explains why point/line maximals fail but their incident flag splits',
      'H1_dimension':2,
      'barcode':barcode,
      'structural_statement':'Point and line stabilizers annihilate distinct 1D obstruction subspaces; their incident intersection annihilates all of H1(G,R29).',
      'relation_to_section_census':'All five maximals remain nonsplit in Pass 4503; the flag is the canonical tested subgroup where both radical obstruction charges vanish, consistent with its exact 384/384 section system.',
      'boundary':'Vanishing of these fixed-line radical H1 restrictions explains an obstruction channel but is not asserted to classify the complete Ext^1(H10,R29) restriction theory for every subgroup.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
