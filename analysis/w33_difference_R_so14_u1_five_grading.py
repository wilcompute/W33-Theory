#!/usr/bin/env python3
"""Exact E8 -> SO(14) x U(1)_R five-grading for the twin-Z6 difference element.

The single-node correction R from w33_twin_z6_single_node_difference has Kac
coordinates (4,0,0,0,0,0,0,1,0).  In the repository's frozen E8 simple-root
ordering its integer U(1) charge is simply coefficient c_6 (zero based).

This verifier does not recognize representations from dimensions alone.  It:
  * enumerates all 240 roots and proves the charge histogram
        84_0 + 64_{-1}+64_{+1}+14_{-2}+14_{+2};
  * reconstructs the 84 neutral roots as D7;
  * computes dominant Dynkin labels of every charged sector relative to that
    exact D7 simple system;
  * generates the D7 Weyl orbit of each dominant weight and proves it equals
    the whole charge sector.

The ±2 sectors are the 14-vector weights; the ±1 sectors are the two chiral
64-spinor weight systems.  Adding the eight Cartans gives
  248 = (91+1)_0 + 64_{-1}+64_{+1}+14_{-2}+14_{+2}.
"""
from __future__ import annotations
import importlib.util,json,sys
from collections import Counter,deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_difference_R_so14_u1_five_grading.json"
R_NODE=6

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);assert s and s.loader
    m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","so14_parent")
    cls=load(ROOT/"analysis/w33_e8_order6_kac_classification.py","so14_classifier")
    diff=json.loads((ROOT/"data/w33_twin_z6_single_node_difference.json").read_text())
    assert diff["status"]=="PASS_TWIN_Z6_DIFFER_BY_ONE_MARK2_COWEIGHT_PHASE"

    roots=old.e8_roots_doubled();h=(1,3,9,27,81,243,729,2187)
    simp=old.simple_roots(roots,h);cm=old.coeff_map(roots,simp)
    charges=Counter(cm[r][R_NODE] for r in roots)
    assert charges==Counter({0:84,-1:64,1:64,-2:14,2:14})

    neutral=[r for r in roots if cm[r][R_NODE]==0]
    typ,rank=cls.classify_root_subsystem(old,neutral,h)
    assert (typ,rank,len(neutral))==("D7",7,84)
    d7=old.simple_roots(neutral,h);assert len(d7)==7

    def labels(w):
        return tuple(old.dot(w,a)//4 for a in d7)
    def refl(w,a):
        k=old.dot(w,a)//4
        return tuple(w[i]-k*a[i] for i in range(8))
    def orbit(w):
        seen={w};q=deque([w])
        while q:
            x=q.popleft()
            for a in d7:
                y=refl(x,a)
                if y not in seen:seen.add(y);q.append(y)
        return seen

    expected={
      -2:(14,(0,0,0,0,0,1,0),"vector"),
      -1:(64,(1,0,0,0,0,0,0),"chiral_spinor"),
       1:(64,(0,0,0,0,0,0,1),"opposite_chiral_spinor"),
       2:(14,(0,0,0,0,0,1,0),"vector")}
    sectors={}
    for q,(n,lab,rep) in expected.items():
        W={r for r in roots if cm[r][R_NODE]==q};assert len(W)==n
        dom=[r for r in W if all(x>=0 for x in labels(r))]
        assert len(dom)==1 and labels(dom[0])==lab
        O=orbit(dom[0]);assert O==W and len(O)==n
        sectors[str(q)]={
          "root_weights":n,"unique_dominant_dynkin_labels":list(lab),
          "weyl_orbit_size":len(O),"D7_rep":rep,
          "dominant_root_doubled":list(dom[0])}

    even_roots=sum(n for q,n in charges.items() if q%2==0)
    odd_roots=sum(n for q,n in charges.items() if q%2)
    assert (even_roots,odd_roots)==(112,128)
    parity_fixed=even_roots+8
    assert parity_fixed==120

    out={
      "schema":"w33.difference_R_so14_u1_five_grading.v1",
      "status":"PASS_INTERNAL_SO14_U1_FIVE_GRADING_WITH_HIGHEST_WEIGHTS",
      "headline":"The twin-Z6 difference element R is internally and objectwise the standard E8 -> SO(14) x U(1) five-grading. Its 240 roots split 84_0+64_-1+64_+1+14_-2+14_+2. The 84 neutral roots are D7; exact dominant-weight and Weyl-orbit checks identify the ±2 sectors as the D7 vector 14 and the ±1 sectors as the two chiral 64 spinors. With Cartan, 248=(91+1)_0+64_-1+64_+1+14_-2+14_+2.",
      "charge_coordinate":{"simple_root_coefficient_zero_based":R_NODE,"range":[-2,2]},
      "root_charge_histogram":{str(q):n for q,n in sorted(charges.items())},
      "neutral":{"root_system":"D7","roots":84,"rank":7,
        "full_fixed_algebra":"so(14)+u(1)","dimension":92},
      "charged_sectors":sectors,
      "branching":"248=(91+1)_0+64_-1+64_+1+14_-2+14_+2",
      "cube_parity":{
        "rule":"(-1)^q_R","even_roots":even_roots,"odd_roots":odd_roots,
        "fixed_lie_dimension":parity_fixed,"type":"D8 / so(16)",
        "reading":"91+1+14+14 are even (120); 64+64 are odd (128)"},
      "literature_crosscheck":"Matches the standard E8 -> SO(16) -> SO(14)xU(1) branching, but representation identification here is proved internally by D7 dominant weights and Weyl orbits.",
      "parents":["data/w33_twin_z6_single_node_difference.json",
        "analysis/w33_e8_order6_kac_classification.py"],
      "boundary":"Pure E8 root/weight theorem. It does not identify this U(1) with a low-energy unbroken gauge boson after all heterotic projections.",
      "checks":{"histogram":True,"neutral_D7":True,"unique_dominant_weights":True,
        "charged_sectors_are_full_D7_weyl_orbits":True,"parity_120_128":True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));return out
if __name__=="__main__":main(True)
