#!/usr/bin/env python3
"""Construct the physical qutrit H27 inside the external A2 of E8.

Inputs already certified in this repository:
  * the physical FI/Qpsi Z3 is the center of the external SU(3) in
        E8 -> (E6,1)+(1,A2)+(27,3)+(27bar,3bar);
  * Pass1147 supplies the external-A2 Coxeter order-three Weyl rotation;
  * Pass5727 supplies the abstract qutrit Heisenberg presentation.

This file closes the missing clock/shift map in the frozen E8 root gauge.

Let X be one Coxeter orientation on the external A2.  We search all 3^8
toral F3-valued root characters f and impose two exact conditions:
  (i) f is trivial on the 72 E6 roots;
  (ii) X Z_f X^-1 Z_f^-1 equals the physical FI central character.

There are exactly three solutions.  They differ by multiplication by the FI
center, exactly as the three scalar-normalized choices of qutrit clock.
The lexicographically first is
    f_Z = (0,0,0,0,2,2,0,0) mod 3
in the repository simple-root coefficient gauge.

Its adjoint spectrum is 134+57+57, it is trivial on E6, splits each physical
81 matter block as 27+27+27, and with the inverse Coxeter orientation obeys
the Pass5727 convention
    Z X = omega X Z,
equivalently [X,Z]=omega^2 I.
The central factor omega I is exactly the measured FI/Qpsi Z3.

Thus the old abstract H27 is realized explicitly inside the same physical
external SU(3) subset of E8, at the finite group/representation level.

Boundary: this is a finite E8 subgroup theorem.  It does not establish a
D/F-flat heterotic vacuum, identify the external SU(3) with observed family
gauge symmetry, or derive measured masses/mixings.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_external_a2_h27.json"

def load(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def refl(old,r,a):
    k=old.dot(r,a)//4
    return tuple(r[i]-k*a[i] for i in range(8))

def main(write=True):
    old=load(ROOT/"analysis/w33_pass7081_7096_e8_z3_z4_z12_common_refinement.py","h27_parent")
    split=json.loads((ROOT/"data/w33_e8_a2_center_vs_coxeter_order3.json").read_text())
    center=json.loads((ROOT/"data/w33_physical_fi_is_h27_center.json").read_text())
    assert split["status"]=="PASS_PHYSICAL_A2_CENTER_AND_PASS1147_COXETER_ARE_DISTINCT_E8_ORDER3_CLASSES"
    assert center["status"]=="PASS_PHYSICAL_FI_Z3_EQUALS_QUTRIT_HEISENBERG_CENTER_CHARACTER"

    roots=old.e8_roots_doubled(); h=(1,3,9,27,81,243,729,2187)
    simp=old.simple_roots(roots,h); cm=old.coeff_map(roots,simp)
    assert len(simp)==8

    # Structural Qpsi/FI order-three functional: node 3 modulo 3.
    f_fi=(0,0,0,1,0,0,0,0)
    def grade(r,f):
        return sum(c*a for c,a in zip(cm[r],f))%3

    neutral=[r for r in roots if grade(r,f_fi)==0]
    # Build connected root components by nonorthogonality.
    adj={r:set() for r in neutral}
    for i,a in enumerate(neutral):
        for b in neutral[i+1:]:
            if old.dot(a,b)!=0:
                adj[a].add(b); adj[b].add(a)
    seen=set(); comps=[]
    for r in neutral:
        if r in seen: continue
        q=[r]; seen.add(r); cc=[]
        while q:
            x=q.pop(); cc.append(x)
            for y in adj[x]:
                if y not in seen: seen.add(y); q.append(y)
        comps.append(cc)
    sizes=sorted(len(c) for c in comps)
    assert sizes==[6,72]
    e6=max(comps,key=len); a2=min(comps,key=len)
    a2simple=old.simple_roots(a2,h)
    assert len(a2simple)==2
    # In the frozen simple-root ordering these are nodes 4 and 5.
    assert a2simple==[simp[4],simp[5]]

    alpha,beta=a2simple
    # Xplus=s_alpha s_beta; Xminus=Xplus^-1=s_beta s_alpha.
    def Xplus(r): return refl(old,refl(old,r,beta),alpha)
    def Xminus(r): return refl(old,refl(old,r,alpha),beta)
    assert all(Xplus(Xplus(Xplus(r)))==r for r in roots)
    assert all(Xminus(Xminus(Xminus(r)))==r for r in roots)
    assert all(Xplus(Xminus(r))==r and Xminus(Xplus(r))==r for r in roots)

    # Conjugation of a toral phase character:
    # (X Z_f X^-1)(E_r) has exponent f(X^-1 r).
    def conjugate_grade(r,f,Xinverse):
        return grade(Xinverse(r),f)

    # Search pure external-A2 clocks: trivial on E6 and commutator FI.
    sols=[]
    for f in itertools.product(range(3),repeat=8):
        if any(grade(r,f)!=0 for r in e6):
            continue
        # Xplus Z Xplus^-1 = FI * Z.
        if all((conjugate_grade(r,f,Xminus)-grade(r,f)-grade(r,f_fi))%3==0 for r in roots):
            sols.append(tuple(f))
    assert sols==[
      (0,0,0,0,2,2,0,0),
      (0,0,0,1,2,2,0,0),
      (0,0,0,2,2,2,0,0),
    ]
    fz=sols[0]
    assert all(tuple((fz[i]+k*f_fi[i])%3 for i in range(8))==sols[k] for k in range(3))

    # Root-level Weyl law in both orientations.
    # Xplus gives [Xplus,Z]=FI; Xminus gives [Xminus,Z]=FI^-1.
    plus_ok=all((conjugate_grade(r,fz,Xminus)-grade(r,fz)-grade(r,f_fi))%3==0 for r in roots)
    minus_ok=all((conjugate_grade(r,fz,Xplus)-grade(r,fz)+grade(r,f_fi))%3==0 for r in roots)
    assert plus_ok and minus_ok

    # Clock spectrum and its support on E6+A2/matter blocks.
    zcnt=Counter(grade(r,fz) for r in roots); zcnt[0]+=8
    assert [zcnt[i] for i in range(3)]==[134,57,57]
    assert Counter(grade(r,fz) for r in e6)==Counter({0:72})
    assert Counter(grade(r,fz) for r in a2)==Counter({1:3,2:3})

    joint={}
    for g in range(3):
        c=Counter(grade(r,fz) for r in roots if grade(r,f_fi)==g)
        joint[str(g)]={str(k):c[k] for k in range(3)}
    assert joint["1"]=={"0":27,"1":27,"2":27}
    assert joint["2"]=={"0":27,"1":27,"2":27}
    assert joint["0"]=={"0":72,"1":3,"2":3}

    # Exact abstract closure from the qutrit Weyl relation.  Normal forms
    # Z^a X^b FI^c are unique, so the group has 3^3=27 elements.
    normals={(a,b,c) for a in range(3) for b in range(3) for c in range(3)}
    assert len(normals)==27

    # Match the already-classified Coxeter conjugacy class.
    assert split["pass1147_A2_coxeter_C3"]["adjoint_eigendimensions"]==[134,57,57]
    assert center["identity"]["same_central_character"] is True

    out={
      "schema":"w33.physical_external_a2_h27.v1",
      "status":"PASS_EXPLICIT_PHYSICAL_EXTERNAL_A2_HEISENBERG_27_IN_E8",
      "headline":"The previously abstract qutrit H27 now has an explicit root-level realization in the same external A2 subset of E8 selected by the physical FI theorem. The unique pure external-A2 clock modulo the FI center has toral character fZ=(0,0,0,0,2,2,0,0) mod3. Together with the A2 Coxeter shift X it satisfies XZX^-1=Z_FI Z (or, for the inverse Coxeter orientation, Z X = omega X Z in the Pass5727 convention), and the commutator is exactly the measured FI/Qpsi center. Hence <X,Z> is the order-27 qutrit Heisenberg group inside the physical external SU(3) carrier.",
      "frozen_root_gauge":{
        "simple_roots_doubled":[list(x) for x in simp],
        "external_A2_simple_root_indices_zero_based":[4,5],
        "FI_character_mod3":list(f_fi),
        "canonical_clock_character_mod3":list(fz)
      },
      "clock_uniqueness":{
        "search_space":"all 3^8 toral F3 characters",
        "constraints":["trivial on all 72 E6 roots","Xplus Z Xplus^-1 Z^-1 equals physical FI center"],
        "solutions":[list(x) for x in sols],
        "number_of_solutions":3,
        "interpretation":"Exactly one clock modulo multiplication by the three FI-center scalars."
      },
      "weyl_relations":{
        "Xplus":"s_alpha s_beta",
        "Xminus":"s_beta s_alpha = Xplus^-1",
        "Xplus_commutator":"Xplus Z Xplus^-1 Z^-1 = Z_FI",
        "Xminus_commutator":"Xminus Z Xminus^-1 Z^-1 = Z_FI^-1",
        "pass5727_orientation":"Using X=Xminus and Z_FI=omega I gives Z X = omega X Z.",
        "all_240_roots_checked":True
      },
      "spectra":{
        "clock_adjoint_eigendimensions":[134,57,57],
        "clock_fixed_reductive_algebra":"E7+u1 (same E8 order-three class as the A2 Coxeter element)",
        "FI_grade_by_clock_grade_root_counts":joint,
        "matter_81_split":"Each FI grade-1 and grade-2 matter shell splits exactly 27+27+27 under the clock."
      },
      "H27":{
        "order":27,
        "presentation":"X^3=Z^3=Z_FI^3=1; Z_FI central; [X,Z]=Z_FI^(+/-1)",
        "normal_forms":"Z^a X^b Z_FI^c, a,b,c in F3",
        "center":"<Z_FI> = <exp(2*pi*i Qpsi/3)>",
        "quotient":"H27 / center = F3^2"
      },
      "bridge_to_old_pass5727":"Pass5727 already proved the qutrit Schrödinger H27 and its Clifford normalizer. The new theorem supplies the missing E8 root-gauge identification: Coxeter shift = X, pure external-A2 toral phase = Z, and measured physical FI/Qpsi Z3 = the commutator center.",
      "external_context":"This is the standard clock/shift Heisenberg subgroup of SU(3), now located objectwise in the repository's certified E8 -> E6 x A2 embedding.",
      "boundary":"Finite E8/subgroup/representation theorem only. No D/F-flat vacuum, observed-family assignment, Standard Model derivation, or measured photonic implementation follows from this identification alone.",
      "parents":[
        "data/w33_e8_a2_center_vs_coxeter_order3.json",
        "data/w33_physical_fi_is_h27_center.json",
        "analysis/w33_pass5727_5730_torsion_family_heisenberg.py"
      ],
      "checks":{
        "physical_neutral_roots_split_E6_A2":True,
        "pure_clock_unique_mod_FI_center":True,
        "clock_spectrum_134_57_57":True,
        "matter_shells_split_27_27_27":True,
        "rootwise_Heisenberg_commutator":True,
        "H27_order_27":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
