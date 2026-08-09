#!/usr/bin/env python3
"""Pass 4493 compatibility witness, corrected by Pass 4503/4507.

The historical Pass-4493 full-group result remains valid:

    PSp(4,3): rank(A)=389, rank([A|b])=390, no section.

Its originally frozen restricted-subgroup table was a false positive and is
superseded.  Re-execution from the exact current geometry gives:

    line stabilizer, order 648:      386/387, no section;
    point stabilizer, order 648:     387/388, no section;
    incident flag, order 162:        384/384, split, affine dimension 6;
    apartment stabilizer, order 16:  357/358, no section.

Pass 4503 extends this correction to all five maximal subgroup types.  This file
is kept runnable because historical CI and citations point at Pass 4493.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from w33_apartment_section_core import *  # noqa: F401,F403

ROOT=Path(__file__).resolve().parents[1]


def main()->int:
    pts,pidx,lines,lidx,_,Astar,*_=build_geometry();Astar=np.asarray(Astar,dtype=np.uint8)
    _,Ereps,Vreps,coordE,coordV,Pi=quotient_model(Astar)
    matrices=[transvection_matrix(v) for v in pts]
    point_trans=[point_perm_from_matrix(M,pts,pidx) for M in matrices]
    line_trans=[build_line_perm(M,pts,pidx,lines,lidx) for M in matrices]
    selected=[];full_line={tuple(range(40))}
    for i,p in enumerate(line_trans):
        trial=perm_group([line_trans[j] for j in selected]+[p],40)
        if len(trial)>len(full_line):selected.append(i);full_line=trial
        if len(full_line)==25920:break
    assert len(full_line)==25920
    full_point=perm_group([point_trans[i] for i in selected],40);assert len(full_point)==25920

    line_stab={g for g in full_line if g[0]==0}
    point_stab_point={g for g in full_point if g[0]==0}
    point_stab={line_perm_from_point_perm(g,lines,lidx) for g in point_stab_point}
    fp,fl=min((p,li) for li,L in enumerate(lines) for p in L)
    flag_point={g for g in full_point if g[fp]==fp and line_perm_from_point_perm(g,lines,lidx)[fl]==fl}
    flag={line_perm_from_point_perm(g,lines,lidx) for g in flag_point}
    apartment=first_apartment(Astar)
    apartment_stab={g for g in full_line if frozenset(g[x] for x in apartment)==apartment}

    specs={"full_PSp":full_line,"one_line_stabilizer":line_stab,"one_point_stabilizer":point_stab,
           "incident_flag_stabilizer":flag,"apartment_setwise_stabilizer":apartment_stab}
    results={}
    for name,H in specs.items():
        gens=small_generating_set(H,40);GE,GV=actions_from_line_gens(gens,Ereps,Vreps,coordE,coordV);sec=section_system(Pi,GE,GV)
        results[name]={"order":len(H),"index_in_PSp":25920//len(H),"fixed_dim_E39":fixed_dimension(GE,39),
          "fixed_dim_V10":fixed_dimension(GV,10),"section_system":sec}

    expected={
      "full_PSp":(389,390,False,None),
      "one_line_stabilizer":(386,387,False,None),
      "one_point_stabilizer":(387,388,False,None),
      "incident_flag_stabilizer":(384,384,True,6),
      "apartment_setwise_stabilizer":(357,358,False,None),
    }
    for name,(r,a,s,d) in expected.items():
        q=results[name]["section_system"]
        assert (q["rank_coefficient"],q["rank_augmented"],q["consistent"],q["affine_dimension"])==(r,a,s,d),(name,q)
    assert (len(line_stab),len(point_stab),len(flag),len(apartment_stab))==(648,648,162,16)

    out={"pass":4493,"status":"CORRECTED_BY_PASSES_4503_4507",
      "theorem":"corrected natural geometric restriction census for the nonsplit apartment extension",
      "sequence":"0 -> K/J (29) -> E=M/J (39) -> V=M/K=H10 (10) -> 0",
      "tested_subgroups":results,
      "erratum":{"withdrawn":"the historical 370/370 point-line split, 338 flag rank and 308 apartment rank",
                 "replacement":"point/line remain nonsplit; canonical order-162 incident flag splits 384/384 with affine dimension 6",
                 "full_group_result_preserved":"389/390 nonsplitting"},
      "boundary":"Pass 4503 proves all five maximal subgroup types are nonsplit. The order-162 flag is a verified splitting subgroup, not yet a classification of every subgroup."}
    p=ROOT/'data/PART_W33_PASS4493_SYMMETRY_BREAKING_SECTION_THRESHOLD.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
