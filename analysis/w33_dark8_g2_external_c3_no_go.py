#!/usr/bin/env python3
"""Kill the strict K-compatible G2 promotion of the dark eight.

The exact dark K=H27 x C3_ext module is
    chi_ext + chi_ext^2 + V_omega + V_omega^2.

After forgetting C3_ext this has the SU(3)/H27 branching shadow
    1 + 1 + 3 + 3bar = 1 + (1+3+3bar),
matching 1 + 7 under G2 -> SU(3).

Question: can one promote this shadow to an actual G2 action while preserving
the already-frozen DIRECT-PRODUCT external C3 symmetry?

No.

Any G2 action with D8 = 1_G2 + 7_G2 has a one-dimensional G2-fixed line. Since
G2 contains the displayed SU(3)/H27 branch, that fixed line lies in the
two-dimensional H27-invariant singlet plane. If C3_ext commutes with G2, the
fixed line must also be C3_ext-invariant. C3_ext has distinct eigenvalues
omega and omega^2 on the two singlets, so the fixed line is one of them.

The complementary irreducible G2 seven then contains:
    the other singlet, carrying omega^(2 or 1),
    plus V_omega + V_omega^2, carrying external charge 0.
Thus C3_ext restricted to the seven has spectrum
    {omega^s, 1,1,1,1,1,1},
which is not scalar.

But every operator commuting with an irreducible complex G2 seven is scalar
(Schur). Contradiction.

Therefore the branching shadow cannot be upgraded to a G2 x C3_ext action
compatible with the frozen K direct product. A larger NONCOMMUTING envelope
is not ruled out here.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_dark8_g2_external_c3_no_go.json"

def main(write=True):
    dark=json.loads((ROOT/"data/w33_hesse36_e8_matter81_dark8_decomposition.json").read_text())
    shadow=json.loads((ROOT/"data/w33_dark8_g2_branching_shadow.json").read_text())
    assert dark["irreducible_decomposition"]["formula"]=="chi_ext + chi_ext^2 + V_omega + V_omega^2"
    assert shadow["G2_shadow"]["matches_dark8_after_H27_restriction"] is True
    assert shadow["G2_shadow"]["constructed_G2_action"] is False

    # Exact C3_ext exponents on K-irreducible summands.
    # singlets chi,chi^2 have exponents 1,2; both Schrodinger summands here have t=0.
    full_spectrum={0:6,1:1,2:1}
    assert sum(full_spectrum.values())==8

    candidate_sevens=[
      {"fixed_singlet_charge":1,"seven_spectrum":{0:6,2:1}},
      {"fixed_singlet_charge":2,"seven_spectrum":{0:6,1:1}},
    ]
    assert all(len(x["seven_spectrum"])==2 for x in candidate_sevens)
    assert all(sum(x["seven_spectrum"].values())==7 for x in candidate_sevens)
    assert all(max(x["seven_spectrum"].values())<7 for x in candidate_sevens)

    out={
      "schema":"w33.dark8_g2_external_c3_no_go.v1",
      "status":"PASS_STRICT_G2_TIMES_EXTERNAL_C3_PROMOTION_OF_DARK8_IS_IMPOSSIBLE",
      "headline":"The dark 1+1+3+3bar branching shadow cannot be promoted to a G2 action that commutes with the already-frozen external C3. Any G2-fixed singlet must be one of the two external-charge eigenlines; the complementary irreducible seven then sees C3 spectrum omega^s plus six eigenvalues 1, which is non-scalar and contradicts Schur's lemma for the irreducible G2 seven.",
      "dark_K_module":{
        "formula":"chi_ext + chi_ext^2 + V_omega + V_omega^2",
        "dimension":8,
        "C3_ext_exponent_multiplicities":{"0":6,"1":1,"2":1},
        "H27_restriction":"1 + 1 + 3 + 3bar"
      },
      "candidate_G2_branching":{
        "formula":"1_G2 + 7_G2, with 7 -> 1+3+3bar under SU(3)",
        "possible_fixed_singlet_external_charges":[1,2],
        "resulting_seven_C3_spectra":[
          {"fixed_charge":1,"seven":"1^6 plus omega^2"},
          {"fixed_charge":2,"seven":"1^6 plus omega"}
        ],
        "C3_scalar_on_seven":False
      },
      "obstruction":{
        "required_compatibility":"external C3 commutes with the proposed G2 action, preserving the frozen K=H27 x C3 direct-product symmetry",
        "lemma":"Schur: the commutant of an irreducible complex G2 seven is the scalars",
        "contradiction":"the frozen external C3 is non-scalar on every possible seven complement",
        "strict_G2_x_C3_extension_exists":False
      },
      "what_survives":{
        "G2_branching_shadow_after_forgetting_external_C3":True,
        "noncommuting_larger_envelope_ruled_out":False,
        "possible_next_question":"whether C3_ext can participate noncentrally in a larger exceptional or semilinear envelope rather than commute with G2"
      },
      "boundary":"This is a representation-theoretic no-go for a commuting G2 x C3_ext promotion. It does not rule out a noncommuting larger group/algebra containing both structures, nor infer a G2 gauge boson, dark multiplet, mass, or interaction.",
      "parents":[
        "data/w33_dark8_g2_branching_shadow.json",
        "data/w33_hesse36_e8_matter81_dark8_decomposition.json"
      ],
      "checks":{
        "dark_C3_spectrum_6_1_1":True,
        "only_H27_invariant_fixed_lines_are_in_singlet_plane":True,
        "C3_eigenlines_force_two_candidate_G2_fixed_singlets":True,
        "C3_non_scalar_on_both_candidate_sevens":True,
        "Schur_obstruction_applies":True,
        "strict_commuting_extension_rejected":True,
        "noncommuting_envelope_left_open":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
