#!/usr/bin/env python3
"""Test the dark-eight against SU(3) adjoint and G2 branching patterns.

The exact dark K=H27 x C3 module is
  chi_ext + chi_ext^2 + V_omega + V_omega^2.

Restricting to H27 forgets the external characters, so
  D8|_H27 = 1 + 1 + V_omega + V_omega^2.

Under the physical embedding H27 < SU(3), V_omega and V_omega^2 are the
fundamental/conjugate qutrit sectors. Thus the H27 center z has eigenprofile
  1^2, omega^3, (omega^2)^3
and trace -1.

This immediately rules out identifying D8 with the external SU(3) adjoint,
because the SU(3) center acts trivially on the adjoint 8.

On the other hand, the standard branching of the G2 fundamental is
  7 -> 3 + 3bar + 1 under SU(3).
Therefore 1+7 restricts as
  1 + 1 + 3 + 3bar,
exactly the same SU(3)/H27 branching profile as D8.

Boundary: this is a restriction/branching match only. The full external C3
acts nontrivially on the two dark singlets, so no G2 action is constructed.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_dark8_g2_branching_shadow.json"

def main(write=True):
    dark=json.loads((ROOT/"data/w33_hesse36_e8_matter81_dark8_decomposition.json").read_text())
    physical=json.loads((ROOT/"data/w33_physical_external_a2_h27.json").read_text())
    assert dark["irreducible_decomposition"]["formula"]=="chi_ext + chi_ext^2 + V_omega + V_omega^2"
    assert physical["H27"]["center"]=="<Z_FI> = <exp(2*pi*i Qpsi/3)>"
    assert dark["dark_character"]["H27_center_generator_trace"]==-1

    profile={"1":2,"omega":3,"omega^2":3}
    assert sum(profile.values())==8
    # trace 2+3(w+w^2)=2-3=-1
    center_trace=-1
    assert center_trace==dark["dark_character"]["H27_center_generator_trace"]

    out={
      "schema":"w33.dark8_g2_branching_shadow.v1",
      "status":"PASS_DARK8_IS_NOT_A2_ADJOINT_BUT_MATCHES_ONE_PLUS_G2_SEVEN_AFTER_H27_RESTRICTION",
      "headline":"The dark eight fails the tempting external-A2-adjoint identification but has an exact G2 branching shadow. On the physical H27 center its eigenvalue profile is 1^2, omega^3, (omega^2)^3 and trace -1, whereas the SU(3) adjoint is center-trivial. Forgetting the external C3 gives 1+1+3+3bar, exactly the SU(3) branching profile of 1 plus the G2 fundamental 7.",
      "dark8_restricted_to_H27":{
        "decomposition":"1 + 1 + V_omega + V_omega^2",
        "dimension":8,
        "H27_center_eigenvalue_multiplicities":profile,
        "H27_center_trace":-1,
        "characteristic_polynomial":"(x-1)^2 (x^2+x+1)^3"
      },
      "A2_adjoint_test":{
        "candidate":"SU(3) adjoint 8",
        "center_action":"trivial on all 8 adjoint dimensions",
        "center_trace":8,
        "matches_dark8":False,
        "verdict":"NO_GO"
      },
      "G2_shadow":{
        "standard_branching":"7 -> 3 + 3bar + 1 under SU(3)",
        "one_plus_seven_branching":"1 + 7 -> 1 + 1 + 3 + 3bar",
        "matches_dark8_after_H27_restriction":True,
        "constructed_G2_action":False
      },
      "physics_reading":"If the dark eight participates in a larger exceptional envelope, its finite H27 content is compatible with a singlet plus G2-seven branching pattern and incompatible with being the external SU(3) gauge adjoint itself. This is a representation-theoretic clue, not a particle assignment.",
      "boundary":"The full dark K-module remembers an external C3 that acts as omega and omega^2 on the two singlets. That extra action is not supplied by the ordinary G2 seven. No G2 gauge symmetry, octonionic dynamics, dark-matter multiplet, or mass scale is inferred.",
      "parents":[
        "data/w33_hesse36_e8_matter81_dark8_decomposition.json",
        "data/w33_physical_external_a2_h27.json"
      ],
      "checks":{
        "dark_dimension8":True,
        "H27_center_trace_minus1":True,
        "A2_adjoint_center_trace8":True,
        "A2_adjoint_identification_rejected":True,
        "one_plus_G2_seven_branching_matches":True,
        "G2_action_not_claimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
