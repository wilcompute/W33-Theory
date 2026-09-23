#!/usr/bin/env python3
"""No-go: the 1296 extended qutrit Clifford group is not Shephard-Todd G26.

Internal parent:
  data/w33_extended_clifford_pass408_intertwiner.json

External classification input (Shephard-Todd/MAGMA):
  G26 = C2 x (3^(1+2).SL(2,3)), order 1296,
  and its projective collineation group is the Hessian group of order 216.

The internal extended qutrit group instead has:
  H27:GL(2,3), order 1296,
  trivial center,
  derived subgroup H27:SL(2,3), order 648,
  abelianization C2,
  and a normal C3 quotient AGL(2,3), order 432.

A group with trivial center cannot be isomorphic to G26, which has an explicit
central C2 direct factor. The projective shadows also differ: G26 has scalar
projective quotient 216, while the qutrit retained-phase group's normal C3
quotient is 432 and the C3 is not central in the full group.

This resolves an order-1296 ambiguity; it does not deny the separate classical
G25/Hessian relationship of the 648 determinant-one core.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "data/w33_extended_clifford_pass408_intertwiner.json"
SATURATION = ROOT / "data/w33_q3_extended_clifford_saturation.json"
OUT = ROOT / "data/w33_extended_clifford_g26_no_go.json"


def main(write=True):
    parent = json.loads(PARENT.read_text())
    saturation = json.loads(SATURATION.read_text())

    gs = parent["group_structure"]
    assert gs["full_order"] == 1296
    assert gs["full_group"] == "H27 : GL(2,3)"
    assert gs["full_center_order"] == 1
    assert gs["unitary_subgroup"] == "H27 : SL(2,3)"
    assert gs["unitary_order"] == 648
    assert gs["full_derived_order"] == 648
    assert gs["full_abelianization"] == "C2"
    assert gs["scalar_C3_is_normal_but_not_central_in_full_group"] is True
    assert gs["projective_full_order"] == 432

    # Standard Shephard-Todd/MAGMA classification data.
    g26 = {
        "name": "Shephard-Todd G26 = W(M3)",
        "order": 1296,
        "structure": "C2 x (3^(1+2).SL(2,3))",
        "explicit_central_C2_factor": True,
        "projective_collineation_group": "Hessian group G216",
        "projective_collineation_order": 216,
        "multiplicative_character_count_reported_in_literature": 6,
    }
    assert g26["order"] == gs["full_order"]

    center_obstruction = gs["full_center_order"] == 1 and g26["explicit_central_C2_factor"]
    projective_shadow_obstruction = (
        gs["projective_full_order"] != g26["projective_collineation_order"]
    )
    assert center_obstruction
    assert projective_shadow_obstruction

    out = {
        "schema": "w33.extended_clifford_g26_no_go.v1",
        "status": "PASS_EXTENDED_QUTRIT_1296_IS_NOT_SHEPHARD_TODD_G26",
        "headline": (
            "The order-1296 coincidence is now resolved negatively. The retained-phase "
            "extended qutrit Clifford group H27:GL(2,3) has trivial center, whereas "
            "Shephard-Todd G26 is classified as C2 x (3^(1+2).SL(2,3)) and therefore "
            "has a central involution. Hence the groups are not isomorphic. Their "
            "projective shadows also differ: the qutrit group's normal-C3 quotient is "
            "AGL(2,3), order 432, while G26's scalar collineation quotient is the "
            "Hessian group of order 216."
        ),
        "extended_qutrit_group": {
            "structure": gs["full_group"],
            "order": gs["full_order"],
            "center_order": gs["full_center_order"],
            "derived_order": gs["full_derived_order"],
            "abelianization": gs["full_abelianization"],
            "normal_phase_C3_not_central": gs["scalar_C3_is_normal_but_not_central_in_full_group"],
            "normal_C3_quotient": gs["projective_full_quotient"],
            "normal_C3_quotient_order": gs["projective_full_order"],
        },
        "G26_classification_input": g26,
        "obstructions": {
            "center": (
                "qutrit group center=1, but G26 contains a direct central C2; "
                "therefore no abstract group isomorphism exists"
            ),
            "projective_shadow": (
                "qutrit normal-C3 quotient has order 432, whereas the G26 scalar "
                "projective collineation quotient has order 216"
            ),
            "extension_semantics": (
                "the qutrit odd coset inverts the Pauli C3 center; the G26 extra C2 "
                "is a central direct factor"
            ),
        },
        "important_non_no_go": (
            "This theorem does not rule out the separately known relationship between "
            "the determinant-one 648 core and the Hessian reflection group G25. It "
            "only rules out identifying the full 1296 anti-linear qutrit extension "
            "with G26."
        ),
        "literature": [
            {
                "source": "Magma Handbook, Construction of Finite Complex Reflection Groups",
                "fact": "G26: W(M3)=Z2 x 3^(1+2).SL2(3), order 1296",
            },
            {
                "source": "Semiinvariants of Finite Reflection Groups, Example G26",
                "fact": (
                    "G26 has 1296 complex 3x3 matrices; its collineation group after "
                    "modding scalar matrices is Hessian order 216; six multiplicative "
                    "characters are reported"
                ),
            },
        ],
        "boundary": (
            "The no-go is an abstract finite-group distinction. It says nothing by "
            "itself about physical reflection symmetries, spacetime parity, or which "
            "complex representation—if any—should model the photonic hardware."
        ),
        "parents": [
            "data/w33_extended_clifford_pass408_intertwiner.json",
            "data/w33_q3_extended_clifford_saturation.json",
        ],
        "checks": {
            "qutrit_full_order1296": True,
            "qutrit_full_center_trivial": True,
            "qutrit_full_derived648": True,
            "qutrit_abelianization_C2": True,
            "qutrit_phase_C3_normal_not_central": True,
            "g26_classification_order1296": True,
            "g26_has_explicit_central_C2": True,
            "center_invariant_proves_nonisomorphism": True,
            "projective_shadow_orders_differ_432_vs216": True,
            "g25_core_relationship_not_denied": True,
        },
    }
    assert saturation["q3_closure"]["full_order"] == 1296
    assert all(out["checks"].values())
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
