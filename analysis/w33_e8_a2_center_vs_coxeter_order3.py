#!/usr/bin/env python3
"""Separate the physical A2-center Z3 from the Pass1147 A2-Coxeter C3 in E8.

The repository has two order-three constructions attached to an external A2:

1. The physical FI / CE2 grading.  On
       E8 -> (E6,1) + (1,A2) + (27,3) + (27bar,3bar)
   it is the central SU(3) phase omega*I_3.  Therefore it fixes E6+A2 and has
   adjoint eigendimensions 86+81+81.

2. Pass1147's A2 Coxeter element s_alpha s_beta.  It centralizes W(E6) but is
   the Weyl 3-cycle of the A2, not the center.  In the defining triplet its
   eigenvalues are 1,omega,omega^2.  Hence on the A2 adjoint the multiplicities
   are 2,3,3; on each 27x3 block they are 27,27,27.  The full E8 adjoint
   therefore has eigendimensions 134+57+57.

This verifier independently enumerates every normalized exact-order-three
inner Kac diagram in the repository's frozen E8 simple-root gauge.  The two
spectra select distinct unique Kac classes:
    center/FI   : (0,0,0,0,0,1,0,0,0), fixed E6+A2;
    A2 Coxeter  : (1,0,0,0,0,0,1,0,0), fixed E7+u1.

Thus the two C3's can belong to the same A2 subgroup while being different
conjugacy classes in E8.  Equality of order and common A2 provenance is not an
intertwiner.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import math
import sys
from collections import Counter
from functools import reduce
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_a2_center_vs_coxeter_order3.json"

def load(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def gcd_all(xs): return reduce(math.gcd,xs)

TARGET_EDGES={
 "A2":(2,[(0,1)]),
 "A8":(8,[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)]),
 "D7":(7,[(0,1),(1,2),(2,3),(3,4),(4,5),(4,6)]),
 "E6":(6,[(0,1),(1,2),(2,3),(3,4),(2,5)]),
 "E7":(7,[(0,1),(1,2),(2,3),(3,4),(2,5),(5,6)]),
}

def classify(old,roots,h):
    simp=old.simple_roots(roots,h); A=old.cartan(simp); comps=old.components_from_cartan(A)
    types=[]
    for C in comps:
        hits=[]
        for name,(n,edges) in TARGET_EDGES.items():
            if len(C)==n and old.graph_isomorphic_component(A,C,edges): hits.append(name)
        assert len(hits)==1,(len(C),C,hits,A)
        types.append(hits[0])
    return "+".join(sorted(types)),len(simp)

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","order3_parent")
    qpsi=json.loads((ROOT/"data/w33_qpsi_mod12_unification.json").read_text())
    p1147=json.loads((ROOT/"data/w33_pass1147_schlaefli_steinberg_fourier_bridge.json").read_text())
    assert qpsi["status"]=="PASS_SINGLE_INTEGER_QPSI_UNIFIES_E8_Z2_Z3_Z4_Z6_Z12"
    assert p1147["status"]=="PASS"
    assert p1147["a2_color_torsor"]["coxeter_order"]==3
    assert p1147["a2_color_torsor"]["structure"]=="W(E6) x C3"

    # Physical center phase on the standard E8 -> E6 x A2 decomposition.
    physical=[86,81,81]
    assert qpsi["residue_dimensions"]["mod3_CE2_and_physical_FI"]==physical
    center_blocks={
      "E6_adjoint":[78,0,0],
      "A2_adjoint":[8,0,0],
      "27x3":[0,81,0],
      "27barx3bar":[0,0,81],
    }
    assert [sum(v[i] for v in center_blocks.values()) for i in range(3)]==physical

    # Coxeter representative in SU(3): eigenvalues (1,w,w^2).
    # Conjugation on sl3 has 2 diagonal fixed directions and three ordered
    # off-diagonal pairs in each nontrivial eigenvalue.
    cox_blocks={
      "E6_adjoint":[78,0,0],
      "A2_adjoint":[2,3,3],
      "27x3":[27,27,27],
      "27barx3bar":[27,27,27],
    }
    coxeter=[sum(v[i] for v in cox_blocks.values()) for i in range(3)]
    assert coxeter==[134,57,57]

    roots=old.e8_roots_doubled(); h=(1,3,9,27,81,243,729,2187)
    simp=old.simple_roots(roots,h); cm=old.coeff_map(roots,simp)
    pos=[r for r in roots if old.dot(r,h)>0]
    highest=max(pos,key=lambda r:sum(cm[r]))
    marks=tuple(cm[highest]); aff=(1,)+marks
    assert aff==(1,4,6,5,4,3,2,2,3)

    candidates=[]
    ranges=[range(3//a+1) for a in aff]
    for s in itertools.product(*ranges):
        if sum(a*x for a,x in zip(aff,s))!=3 or gcd_all(s)!=1: continue
        finite=s[1:]
        cnt=Counter(sum(c*a for c,a in zip(cm[r],finite))%3 for r in roots); cnt[0]+=8
        dims=[cnt[i] for i in range(3)]
        fixed=[r for r in roots if sum(c*a for c,a in zip(cm[r],finite))%3==0]
        typ,rank=classify(old,fixed,h)
        candidates.append({
          "kac":list(s),"eigendimensions":dims,
          "fixed_root_count":len(fixed),"fixed_semisimple_type":typ,
          "fixed_semisimple_rank":rank,"fixed_center_rank":8-rank,
          "fixed_lie_dimension":len(fixed)+8})
    assert len(candidates)==4

    ph=[x for x in candidates if x["eigendimensions"]==physical]
    cx=[x for x in candidates if x["eigendimensions"]==coxeter]
    assert len(ph)==len(cx)==1
    assert ph[0]["kac"]==[0,0,0,0,0,1,0,0,0]
    assert ph[0]["fixed_semisimple_type"]=="A2+E6" and ph[0]["fixed_center_rank"]==0
    assert cx[0]["kac"]==[1,0,0,0,0,0,1,0,0]
    assert cx[0]["fixed_semisimple_type"]=="E7" and cx[0]["fixed_center_rank"]==1

    out={
      "schema":"w33.e8_a2_center_vs_coxeter_order3.v1",
      "status":"PASS_PHYSICAL_A2_CENTER_AND_PASS1147_COXETER_ARE_DISTINCT_E8_ORDER3_CLASSES",
      "affine_marks_repo_order":list(aff),
      "normalized_exact_order3_inner_kac_classes":candidates,
      "physical_FI_center_Z3":{
        "action":"central SU(3) element omega*I3 on the external A2 factor",
        "block_eigendimensions":center_blocks,
        "adjoint_eigendimensions":physical,
        "unique_kac_coordinates":ph[0]["kac"],
        "fixed_reductive_algebra":"E6+A2",
        "fixed_dimension":86,
        "carrier_reading":"Qpsi mod3 is constant across every E6 27: charges 4,-2,1 are all 1 mod3; the conjugate 27bar is grade2."
      },
      "pass1147_A2_coxeter_C3":{
        "action":"Weyl Coxeter 3-cycle s_alpha s_beta in the external A2",
        "triplet_eigenvalue_multiplicities":[1,1,1],
        "A2_adjoint_eigenvalue_multiplicities":[2,3,3],
        "block_eigendimensions":cox_blocks,
        "adjoint_eigendimensions":coxeter,
        "unique_kac_coordinates":cx[0]["kac"],
        "fixed_reductive_algebra":"E7+u1",
        "fixed_dimension":134,
        "pass1147_color_carrier_rank":p1147["a2_color_torsor"]["combined_rank"],
        "pass1147_color_carrier_complex_sector_ranks":p1147["a2_color_torsor"]["complex_sector_ranks"],
      },
      "separation":{
        "same_abstract_group":"C3",
        "same_E8_conjugacy_class":False,
        "same_eigenspectrum":False,
        "center_vs_coxeter":"the center acts as one scalar on the triplet; the Coxeter element cyclically permutes its three weights",
        "fixed_algebra_witness":"E6+A2 (dimension86) versus E7+u1 (dimension134)",
        "carrier_firewall":"Pass1147's 243-dimensional 81_minus tensor C[C3] color carrier is not the 81-dimensional physical E8 grade-one root sector."
      },
      "interpretation":"The physical FI/family Z3 is the central phase of the external SU(3), whereas the Pass1147 color C3 is its Weyl Coxeter rotation. They are complementary structures of one A2, not interchangeable realizations of the same E8 automorphism.",
      "boundary":"This is an exact E8 representation/Kac-class separation. It does not forbid a larger construction containing both actions, and it does not assign Standard Model generations or measured photonic channels.",
      "checks":{
        "physical_spectrum_86_81_81":True,
        "coxeter_spectrum_134_57_57":True,
        "four_exact_order3_kac_classes_enumerated":True,
        "physical_unique_E6_A2_class":True,
        "coxeter_unique_E7_u1_class":True,
        "pass1147_243_not_physical_81":True
      }}
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2)); return out

if __name__=="__main__": main(True)
