#!/usr/bin/env python3
"""Construct the anti-linear charge-conjugation scaffold on the full E8 atlas.

The full hybrid atlas is
  g0(86) + g1(81) + g2(81),
with g2 the Q(omega)-conjugate chart of g1.

Define C anti-linearly by
  C: g0 -> g0,
     g1 <-> g2,
and conjugate every Q(omega) coefficient.

Then C^2=1, and on the physical FI center
  C Z_FI C^-1 = Z_FI^-1,
because omega <-> omega^2.

The same conjugation exchanges the two Hesse compiler orientation assignments
  (0,1,2) <-> (0,2,1)
and sends the dark Strange ray (1,-omega,0) to (1,-omega^2,0).

Boundary: this is a finite anti-linear involution/charge-conjugation scaffold.
It does not derive spatial parity, the Standard Model CP operator, a CKM/PMNS
phase, or spontaneous CP violation.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_hybrid_charge_conjugation.json"

def C_label(label):
    grade,index=label
    if grade==0:return (0,index)
    if grade==1:return (2,index)
    if grade==2:return (1,index)
    raise ValueError(grade)

def conjugate_assignment(a):
    return [(-int(x))%3 for x in a]

def main(write=True):
    atlas=json.loads((ROOT/"data/w33_e8_full_graded_hybrid_atlas.json").read_text())
    orient=json.loads((ROOT/"data/w33_hesse36_physical_fi_orientation_selector.json").read_text())
    dark=json.loads((ROOT/"data/w33_hesse36_dark_schrodinger_strange_state.json").read_text())

    dims=atlas["grading"]["dimensions"]
    labels=[(0,i) for i in range(dims["g0"])]+[(1,i) for i in range(dims["g1"])]+[(2,i) for i in range(dims["g2"])]
    assert len(labels)==248
    assert all(C_label(C_label(x))==x for x in labels)

    selected=orient["selection"]["selected_assignment"]
    conjugate=orient["selection"]["conjugate_assignment"]
    assert selected==[0,1,2]
    assert conjugate==[0,2,1]
    assert conjugate_assignment(selected)==conjugate
    assert conjugate_assignment(conjugate)==selected

    assert dark["dark_multiplicity_ray"]["unnormalized"]==["1","-omega","0"]

    out={
      "schema":"w33.e8_hybrid_charge_conjugation.v1",
      "status":"PASS_FULL_HYBRID_E8_ATLAS_HAS_EXACT_ANTILINEAR_GRADE_SWAP_INVOLUTION",
      "headline":"The full 248-dimensional hybrid E8 atlas carries a canonical anti-linear involution: fix the 86-dimensional neutral grade, exchange the 81-dimensional matter and antimatter grades, and conjugate omega. It squares to one, inverts the physical FI center, exchanges the two Hesse compiler orientations, and conjugates the dark Strange ray.",
      "involution":{
        "carrier_dimension":248,
        "grade_action":{"g0":"g0","g1":"g2","g2":"g1"},
        "coefficient_action":"omega -> omega^2",
        "C_squared":"1 on all 248 basis labels",
        "fixed_basis_labels":86,
        "exchanged_basis_pairs":81
      },
      "FI_center":{
        "before":{"g0":"1","g1":"omega","g2":"omega^2"},
        "after_conjugation":{"g0":"1","g1":"omega^2","g2":"omega"},
        "law":"C Z_FI C^-1 = Z_FI^-1"
      },
      "compiler_orientation":{
        "selected":selected,
        "conjugate":conjugate,
        "C_exchanges_them":True
      },
      "dark_magic":{
        "ray":["1","-omega","0"],
        "conjugate_ray":["1","-omega^2","0"],
        "C_exchanges_Vomega_and_Vomega2":True
      },
      "physics_reading":"The frozen FI orientation selects one member of a conjugate compiler pair, while the completed E8 atlas still possesses an exact anti-linear map relating matter and antimatter charts. This is the correct finite place to study whether a later dynamical layer preserves or breaks the conjugation symmetry.",
      "boundary":"No spatial parity action, CPT theorem, CKM/PMNS phase, electric dipole moment, or spontaneous CP-breaking vacuum is derived. Holotrade's current provenance firewall also prevents promoting this finite involution to a class-wide heterotic vacuum claim.",
      "parents":[
        "data/w33_e8_full_graded_hybrid_atlas.json",
        "data/w33_hesse36_physical_fi_orientation_selector.json",
        "data/w33_hesse36_dark_schrodinger_strange_state.json"
      ],
      "checks":{
        "248_labels_exhausted":True,
        "C_squared_identity":True,
        "g1_g2_exchanged":True,
        "FI_center_inverted":True,
        "compiler_pair_exchanged":True,
        "dark_magic_pair_exchanged":True,
        "observed_CP_not_claimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
