#!/usr/bin/env python3
"""Pass 4538 -- global large-order splitting census for PSp(4,3).

Pass 4503 proved all five maximal subgroup types nonsplit; Pass 4528 proved the
canonical order-162 Borel is maximal in its own overgroup interval.  Here we
push globally above order 162.

Using the five standard maximal structures
  2^4:A5 (960), S6 (720), 3^3:S4 (648), 3^(1+2):2A4 (648),
  2.(A4 x A4).2 (576),
ordinary subgroup structure reduces every proper subgroup of order >162 to
one of seven additional conjugacy types, of orders
  360,324,288,216,216,192,192.
The executable constructs exact representatives inside the corresponding
maximals and recomputes the apartment-extension section system. Every class is
nonsplit. Therefore no splitting subgroup has order >162; the known Borel of
order162 attains the global maximum splitting order.

The classification reduction is group-theoretic input (standard subgroup
structures of the displayed maximals), while every section rank and every
representative order below is independently checked in the exact 40-point
permutation action.
"""
from __future__ import annotations
import json,random
from collections import deque
from pathlib import Path

from w33_apartment_section_core import (
    actions_from_line_gens,build_geometry,build_line_perm,compose,
    line_perm_from_point_perm,perm_group,point_perm_from_matrix,quotient_model,
    section_system,small_generating_set,transvection_matrix,
)
from w33_pass4503_maximal_subgroup_splitting_erratum import enumerate_spreads,generated_limited

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4538_GLOBAL_LARGE_SPLITTING_CENSUS.json'


def invp(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)

def comm(a,b):return compose(compose(compose(invp(a),invp(b)),a),b)
def normal_closure(seed,ambient_gens):
    H=perm_group(seed,40)
    while True:
        changed=False; hg=small_generating_set(H,40)
        for g in ambient_gens:
            gi=invp(g)
            for h in hg:
                z=compose(compose(g,h),gi)
                if z not in H:
                    H=perm_group(hg+[z],40);changed=True;break
            if changed:break
        if not changed:return H

def derived(H):
    gs=small_generating_set(H,40)
    return normal_closure([comm(a,b) for a in gs for b in gs],gs)

def sec(H,Ereps,Vreps,coordE,coordV,Pi):
    gs=small_generating_set(H,40)
    GE,GV=actions_from_line_gens(gs,Ereps,Vreps,coordE,coordV)
    s=section_system(Pi,GE,GV)
    return {'order':len(H),'rank_coefficient':s['rank_coefficient'],
            'rank_augmented':s['rank_augmented'],'split':s['consistent']}

def first_generated_order(H,target):
    gs=[]; base=small_generating_set(H,40)
    # First try extensions of the derived subgroup; then deterministic pairs.
    D=derived(H); dgens=small_generating_set(D,40)
    for g in sorted(H):
        T=perm_group(dgens+[g],40)
        if len(T)==target:return T
    gl=sorted(H)
    for i,a in enumerate(gl):
        for b in gl[i+1:]:
            T=generated_limited([a,b],40,limit=len(H))
            if len(T)==target:return T
    raise AssertionError(('no subgroup',len(H),target))


def main():
    pts,pidx,lines,lidx,_Ap,Astar,*_=build_geometry()
    _,Ereps,Vreps,coordE,coordV,Pi=quotient_model(Astar)
    ptrans=[point_perm_from_matrix(transvection_matrix(v),pts,pidx) for v in pts]
    ltrans=[build_line_perm(transvection_matrix(v),pts,pidx,lines,lidx) for v in pts]
    chosen=[];G={tuple(range(40))}
    for i,g in enumerate(ltrans):
        T=perm_group([ltrans[j] for j in chosen]+[g],40)
        if len(T)>len(G):chosen.append(i);G=T
        if len(G)==25920:break
    assert len(G)==25920
    Gp=perm_group([ptrans[i] for i in chosen],40);assert len(Gp)==25920

    line648={g for g in G if g[0]==0}
    point648={line_perm_from_point_perm(g,lines,lidx) for g in Gp if g[0]==0}
    spreads=enumerate_spreads(lines);S0=set(spreads[0])
    spread720={g for g in G if {g[x] for x in S0}==S0}
    I=tuple(range(40)); inv=[g for g in G if g!=I and compose(g,g)==I]
    fixed16=[g for g in inv if sum(i==g[i] for i in range(40))==16];t=fixed16[0]
    c576={g for g in G if compose(g,t)==compose(t,g)}
    rng=random.Random(4503);gl=sorted(G);m960=None
    for _trial in range(1000):
        a,b=rng.sample(gl,2);T=generated_limited([a,b],40,limit=2000)
        if len(T)==960:m960=T;break
    assert m960 is not None
    maxes={'M960_2^4_A5':m960,'M720_S6':spread720,'M648_3^3_S4':line648,
           'M648_3extraspecial_2A4':point648,'M576_double_A4':c576}
    assert [len(maxes[k]) for k in maxes]==[960,720,648,648,576]

    reps={
      'A6_order360':derived(spread720),
      '3^3_A4_order324':derived(line648),
      'c576_index2_order288':first_generated_order(c576,288),
      'extraspecial_Q8_order216':derived(point648),
      '3^3_D8_order216':first_generated_order(line648,216),
      '2^4_A4_order192':first_generated_order(m960,192),
      'c576_index3_order192':first_generated_order(c576,192),
    }
    expected_orders=[360,324,288,216,216,192,192]
    assert [len(H) for H in reps.values()]==expected_orders
    results={name:sec(H,Ereps,Vreps,coordE,coordV,Pi) for name,H in reps.items()}
    expected_ranks={
      'A6_order360':(386,387),'3^3_A4_order324':(386,387),
      'c576_index2_order288':(386,387),'extraspecial_Q8_order216':(385,386),
      '3^3_D8_order216':(386,387),'2^4_A4_order192':(385,386),
      'c576_index3_order192':(380,381)}
    for name,rr in expected_ranks.items():
        assert (results[name]['rank_coefficient'],results[name]['rank_augmented'])==rr
        assert results[name]['split'] is False

    c4503=json.loads((ROOT/'data/PART_W33_PASS4503_MAXIMAL_SUBGROUP_SPLITTING_ERRATUM.json').read_text())
    assert c4503['all_five_maximal_types_nonsplit'] is True
    out={
      'pass':4538,
      'group':'PSp(4,3) ~= U4(2)','group_order':25920,
      'maximal_orders':[960,720,648,648,576],
      'all_maximals_nonsplit_from_pass4503':True,
      'proper_subgroup_classes_above_162_below_maximals':results,
      'large_class_orders':expected_orders,
      'all_large_classes_nonsplit':all(not r['split'] for r in results.values()),
      'global_maximum_splitting_order':162,
      'attained_by':'canonical flag/Borel N_G(Sylow_3), Pass 4519',
      'classification_reduction':{
        '2^4:A5':'only >162 proper type is 2^4:A4 (192)',
        'S6':'only >162 proper type is A6 (360)',
        '3^3:S4':'types 3^3:A4 (324) and 3^3:D8 (216)',
        '3^(1+2):2A4':'only >162 proper type is 3^(1+2):Q8 (216)',
        '2.(A4xA4).2':'large proper types represented at 288 and the two global 192 classes; the second 192 class is shared with 2^4:A4'
      },
      'theorem':'Combining the standard subgroup structures of the five maximal types with exact section tests gives a global order bound: every subgroup of PSp(4,3) of order >162 is nonsplit, while the order-162 Borel splits.',
      'boundary':'The completeness step uses standard finite-group subgroup structure of the five ATLAS maximal types. The executable independently verifies the exact representatives and section ranks, but is not itself a from-scratch enumeration of every subgroup of the 25920-element group.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
