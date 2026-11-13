#!/usr/bin/env python3
"""Exact 9-translation bridge between affine F3^3 and Heisenberg H27.

The full abelian 27-translation group cannot embed in nonabelian H27;
this explicitly constructs the maximal common 9-element translation subgroup
and its central cocycle correction. Based on current repo H27 normal form
w33_e6_cubic_diagonal_phase_weld.py and native E6 address mapping.
"""
from __future__ import annotations
from pathlib import Path
import itertools,json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261113_h27_maximal_translation_bridge.json"
F=tuple(itertools.product(range(3),repeat=3))
def mul(x,y):
    a,b,c=x;A,B,C=y
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
def frame(x):
    a,b,c=x
    return (a,b,(c+a*b)%3)
def right_action_conjugated(x,g):
    a,b,v=x;A,B,C=g
    return ((a+A)%3,(b+B)%3,(v+C+a*B+A*B)%3)

def verify():
    assert len(F)==27 and mul((0,0,0),(0,0,0))==(0,0,0)
    assert len({frame(x) for x in F})==27
    assert all(frame(mul(x,g))==right_action_conjugated(frame(x),g)
               for x in F for g in F)
    Z={(0,0,c) for c in range(3)}
    assert all(mul(z,x)==mul(x,z) for z in Z for x in F)
    central={z for z in F if all(mul(z,x)==mul(x,z) for x in F)}
    assert central==Z
    lines=((1,0),(0,1),(1,1),(1,2))
    planes=[]
    for u,v in lines:
        H={(t*u%3,t*v%3,c) for t in range(3) for c in range(3)}
        assert len(H)==9
        assert all(mul(x,y)==mul(y,x) for x in H for y in H)
        assert all(mul(x,y) in H for x in H for y in H)
        planes.append(H)
    assert all(planes[i]&planes[j]==Z for i in range(4) for j in range(i+1,4))
    assert len(set.union(*planes))==27
    commutator_census=Counter()
    for x in F:
        commutator_census[sum(mul(x,y)==mul(y,x) for y in F)]+=1
    assert commutator_census==Counter({9:24,27:3})
    # The largest commuting subgroup of H27 has order 9, since
    # centralizer size of every noncentral element is precisely 9.
    H0={(A,0,C) for A in range(3) for C in range(3)}
    for x in F:
        for g in H0:
            a,b,v=frame(x);A,_,C=g
            assert frame(mul(x,g))==((a+A)%3,b,(v+C)%3)
    # A right group element with B !=0 creates a shear dependent
    # on the point address a and therefore cannot be pure translation
    # in this linearized frame.
    for g in F:
        if g[1]:
            deltas={tuple((right_action_conjugated(frame(x),g)[j]-frame(x)[j])%3
                          for j in range(3)) for x in F}
            assert len(deltas)==3
        else:
            deltas={tuple((right_action_conjugated(frame(x),g)[j]-frame(x)[j])%3
                          for j in range(3)) for x in F}
            assert len(deltas)==1
    r={"schema":"toe.h27_affine_bridge.v1",
      "status":"PASS_MAXIMAL_NINE_TRANSLATION_INTERTWINER",
      "nonabelian_group":"H27: (a,b,c)*(A,B,C)=(a+A,b+B,c+C-bA)",
      "center_order":3,"noncentral_elements":24,
      "centralizer_size_census":{str(k):v for k,v in commutator_census.items()},
      "four_maximal_abelian_subgroups_order9":len(planes),
      "pairwise_intersection":"common center Z3",
      "no_full_F3_cube_translation_embedding_in_H27":True,
      "maximal_common_commuting_translation_order":9,
      "coordinate_change":"(a,b,c) -> (a,b,v=c+ab)",
      "common_subgroup":"right H0={(A,0,C)} has v->v+C, a->a+A, b fixed",
      "general_right_action":"(a,b,v)*(A,B,C)=(a+A,b+B,v+C+aB+AB)",
      "cross_fiber_cocycle":"aB+AB (mod3), not removable as one fixed translation for B!=0",
      "checked_all_right_actions":27*27,
      "physics_boundary":"No E6 cubic-preserving lift, masses, gauge action, or full F3^3-equivariance is implied.",
      "prior_references":[
        "analysis/w33_e6_cubic_diagonal_phase_weld.py",
        "data/w33_e6id_current_h27_gauge_bridge.json",
        "analysis/w33_pass10975_e6_cubic_reynolds_clock_weld.py",
        "analysis/toe_20261113_chiral_e6_cubic_compatibility.py"]}
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return r

if __name__=="__main__":
    r=verify()
    print(json.dumps({k:r[k] for k in (
        "status","center_order","centralizer_size_census",
        "four_maximal_abelian_subgroups_order9",
        "maximal_common_commuting_translation_order",
        "checked_all_right_actions")},indent=2))
