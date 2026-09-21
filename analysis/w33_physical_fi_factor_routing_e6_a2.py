#!/usr/bin/env python3
"""Route the physical twin-A4 factors through the FI-induced E6+A2 split.

Consumes the two new exact physical verifiers:
  - twin A4 index-5 E8 gluing;
  - physical FI E6+A2 Z3 grading.

Result: inside the FI-induced neutral root system, the six neutral roots of the
organizer A4's 3-block are *exactly* the external A2 component.  The organizer
2-block A1 and all 20 roots of the physical Wilson-line SU(5) A4 lie in the
72-root E6 component.

This is a root-set equality for this physical decomposition.  It provides a
candidate physical realization of the repo's family SU(3), but does not identify
it with the separately constructed W33/affine family action without an explicit
Weyl/intertwiner map.
"""
from __future__ import annotations
import importlib.util,json,itertools
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_fi_factor_routing_e6_a2.json"

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);assert spec and spec.loader
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
T=load(ROOT/"analysis/w33_physical_twin_a4_e8_index5_gluing.py","twin")
Z=load(ROOT/"analysis/w33_physical_fi_e6_a2_z3_grading.py","z3")

def components(R):
    R=list(R);adj=[set() for _ in R]
    for i,j in itertools.combinations(range(len(R)),2):
        if Z.dot(R[i],R[j])!=0:adj[i].add(j);adj[j].add(i)
    seen=set();out=[]
    for i in range(len(R)):
        if i in seen:continue
        todo=[i];seen.add(i);cc=set()
        while todo:
            x=todo.pop();cc.add(R[x])
            for y in adj[x]:
                if y not in seen:seen.add(y);todo.append(y)
        out.append(cc)
    return sorted(out,key=len)

def main(write=True):
    R=set(Z.roots_e8())
    t=Z.lin(Z.A4,Z.COEFF)
    neutral={r for r in R if Z.dot(t,r)%1==0}
    cc=components(neutral)
    assert [len(x) for x in cc]==[6,72]
    A2,E6=cc

    center={r for r in R if T.proj_norm(r,T.CENTER)==2 and T.proj_norm(r,T.GAUGE)==0}
    gauge={r for r in R if T.proj_norm(r,T.GAUGE)==2 and T.proj_norm(r,T.CENTER)==0}
    center0=center&neutral
    assert len(center)==20 and len(gauge)==20 and len(center0)==8

    assert A2 <= center0 and len(A2)==6
    center_A1=center0-A2
    assert len(center_A1)==2 and center_A1 <= E6
    assert gauge <= E6
    assert len(E6&gauge)==20
    assert len(E6&center)==2

    # The routed E6 contains the root subsystem A4_gauge + A1_FI.
    assert all(Z.dot(a,b)==0 for a in gauge for b in center_A1)
    beta=next(iter(center_A1))
    assert Z.matrix_rank(list(T.GAUGE)+[beta])==5

    out={
      "schema":"w33.physical_fi_factor_routing_e6_a2.v1",
      "status":"PASS_PHYSICAL_FI_FACTOR_ROUTING",
      "headline":"For the FI-induced E8 -> E6+A2 grading, the organizer A4's six neutral roots belonging to its 3-block are exactly the external A2 component. Its remaining neutral root pair (the 2-block A1) lies in E6, and all 20 roots of the physical Wilson-line SU(5) A4 lie in the same E6 component. Thus A4_gauge + A1_FI is an orthogonal rank-5 root subsystem inside E6, while A2_FI is the external SU(3) factor.",
      "counts":{
        "FI_neutral_roots_total":78,"E6_roots":72,"external_A2_roots":6,
        "organizer_A4_neutral_roots":8,"organizer_A2_roots":6,
        "organizer_A1_roots":2,"physical_gauge_A4_roots":20},
      "exact_set_relations":{
        "organizer_A2_equals_external_A2":True,
        "organizer_A1_subset_E6":True,
        "physical_gauge_A4_subset_E6":True,
        "gauge_A4_orthogonal_to_FI_A1":True,
        "A4_plus_A1_rank_inside_E6":5},
      "subgroup_reading":{
        "inside_FI_neutral_E6":"A4_gauge + A1_FI + u(1), compatible with SU(5)xSU(2)xU(1) inside E6",
        "external_factor":"A2_FI, i.e. SU(3)",
        "candidate_family_bridge":"The project already interprets the external A2 of an E6xA2 branching as a three-family factor. This physical root-set routing makes the FI 3-block a concrete candidate for that factor."},
      "boundary":"No equality with the separately constructed W33/affine SU(3)_family action is claimed. A Weyl element or explicit intertwiner between that canonical W33 A2 and this physical FI-induced A2 remains required.",
      "parents":[
        "analysis/w33_physical_twin_a4_e8_index5_gluing.py",
        "analysis/w33_physical_fi_e6_a2_z3_grading.py"],
      "checks":{"component_sizes_6_72":True,"A2_set_equality":True,
        "A1_in_E6":True,"gauge_A4_in_E6":True,"rank5_subsystem":True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));return out
if __name__=="__main__":main(True)
