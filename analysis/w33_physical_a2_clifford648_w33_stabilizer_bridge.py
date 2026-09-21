#!/usr/bin/env python3
"""Physicalize the full order-648 qutrit Clifford/Hessian normalizer.

Today’s physical external-A2 theorem supplies an explicit H27 inside the
certified E8 -> E6 x A2 embedding.  Pass5730 supplies the standard qutrit
normalizer actions
    F: X -> Z,   Z -> X^-1
    P: X -> XZ, Z -> Z
on H27/Z(H27) ~= F3^2.

In the (X,Z) coordinate convention these are
    F = [[0,2],[1,0]],
    P = [[1,0],[1,1]],
and they generate all SL(2,3), order 24.

Pass1054 independently computes the W33 point stabilizer, extracts its normal
H27, and records the full 24-matrix SL(2,3) conjugation image on H27/Z.  This
bridge checks literal equality of the matrix set and therefore fixes explicit
quotient-generator names inside the already-proved abstract isomorphism.

Hence the physical external-A2 qutrit subgroup has normalizer
    H27 : SL(2,3), order 648,
with the same quotient action as the selected W33 point stabilizer.

Boundary: this is a finite subgroup/normalizer identification.  It does not
identify a surviving low-energy gauge group or a laboratory Clifford gate.
"""
from __future__ import annotations
import importlib.util
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_physical_a2_clifford648_w33_stabilizer_bridge.json"

def load(path:Path,name:str):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def mm(A,B):
    return tuple(sum(A[2*r+k]*B[2*k+c] for k in range(2))%3 for r in range(2) for c in range(2))

I=(1,0,0,1)
F=(0,2,1,0)
P=(1,0,1,1)

def closure(gens):
    seen={I}; todo=[I]
    while todo:
        a=todo.pop()
        for g in gens:
            b=mm(a,g)
            if b not in seen:
                seen.add(b); todo.append(b)
    return seen

def det(A): return (A[0]*A[3]-A[1]*A[2])%3

def main(write=True):
    physical=json.loads((ROOT/"data/w33_physical_external_a2_h27.json").read_text())
    p371=json.loads((ROOT/"data/w33_pass371_naturality_and_the_clifford_match.json").read_text())
    assert physical["status"]=="PASS_EXPLICIT_PHYSICAL_EXTERNAL_A2_HEISENBERG_27_IN_E8"
    assert p371["status"]=="PASS"
    assert p371["checks"]["w33_normalizer_order_648"] is True
    assert p371["checks"]["both_are_the_qutrit_clifford_group"] is True

    # Re-run Pass1054 to obtain the exact quotient matrix set from the W33
    # point stabilizer rather than copying a theoretical SL(2,3) list.
    p1054=load(ROOT/"analysis/w33_pass1054_hessian_affine_isomorphism.py","p1054bridge")
    r=p1054.main()
    assert r["status"]=="PASS"
    assert r["orders"]=={"stabilizer":648,"heisenberg":27,"complement":24,"affine_image":648}
    mats={tuple(x) for x in r["linear_quotient"]["matrices_row_major"]}
    assert len(mats)==24
    assert all(det(A)==1 for A in mats)

    generated=closure([F,P])
    assert len(generated)==24
    assert generated==mats
    assert F in mats and P in mats

    # Standard exact relations in SL(2,3).
    F2=mm(F,F); F4=mm(F2,F2)
    P2=mm(P,P); P3=mm(P2,P)
    assert F4==I and P3==I
    minusI=(2,0,0,2)
    assert F2==minusI

    # Extension order.
    H27_order=physical["H27"]["order"]
    normalizer_order=H27_order*len(generated)
    assert normalizer_order==648

    out={
      "schema":"w33.physical_a2_clifford648_w33_stabilizer_bridge.v1",
      "status":"PASS_PHYSICAL_A2_H27_NORMALIZER_EQUALS_W33_CLIFFORD648_AT_QUOTIENT_ACTION_LEVEL",
      "headline":"The explicit physical external-A2 H27 in E8 extends by the Pass5730 Fourier and quadratic-phase automorphisms to H27:SL(2,3), order 648. On H27/Z these have matrices F=[[0,2],[1,0]] and P=[[1,0],[1,1]], which generate all 24 elements of SL(2,3). Re-running Pass1054 shows the selected W33 point stabilizer has exactly the same 24-matrix conjugation image on its normal H27 quotient. Thus the physical E8 qutrit normalizer and the W33 point stabilizer are matched with explicit quotient generators.",
      "physical_E8_side":{
        "carrier":"external A2 ~= SU(3) in E8 -> E6 x A2",
        "H27_order":27,
        "center":"physical FI/Qpsi Z3",
        "quotient":"F3^2 with basis (X,Z)",
        "Fourier_matrix_row_major":list(F),
        "quadratic_phase_matrix_row_major":list(P),
        "generated_SL23_order":len(generated),
        "normalizer_order":normalizer_order,
        "normalizer_structure":"H27 : SL(2,3)"
      },
      "W33_side":{
        "point_stabilizer_order":r["orders"]["stabilizer"],
        "normal_H27_order":r["orders"]["heisenberg"],
        "complement_order":r["orders"]["complement"],
        "quotient_matrix_count":len(mats),
        "contains_physical_F_matrix":F in mats,
        "contains_physical_P_matrix":P in mats,
        "quotient_matrix_set_equals_physical_SL23":mats==generated
      },
      "generator_relations":{
        "F_order":4,
        "F_squared":"-I",
        "P_order":3,
        "det_F":det(F),
        "det_P":det(P)
      },
      "upgrade_over_pass371":"Pass371 already proved the W33 and E6 27-point normalizers are abstract/permutation-isomorphic Clifford-648 groups. The new input is the physical external-A2 H27 root-gauge identification; this bridge pins its standard F,P normalizer generators to the exact SL(2,3) quotient action computed from the W33 point stabilizer.",
      "boundary":"The equality proved is the finite H27:SL(2,3) normalizer and its exact quotient action. A chosen 3x3 complex matrix conjugator to Pass1054's 27-point permutation model is not serialized here, and no low-energy gauge or hardware claim follows.",
      "parents":[
        "data/w33_physical_external_a2_h27.json",
        "analysis/w33_pass5727_5730_torsion_family_heisenberg.py",
        "analysis/w33_pass1054_hessian_affine_isomorphism.py",
        "data/w33_pass371_naturality_and_the_clifford_match.json"
      ],
      "checks":{
        "physical_H27_order27":True,
        "F_P_generate_SL23_order24":True,
        "pass1054_matrix_image_order24":True,
        "literal_matrix_set_equality":True,
        "normalizer_order648":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
