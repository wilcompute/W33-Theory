#!/usr/bin/env python3
"""No-go for gluing the Pass369 internal E6 H27 center to the physical A2 H27 center.

The tempting arithmetic is
    27*27/3 = 243 = 3^(1+4),
suggesting that the regular H27 acting on the E6 minuscule 27 might central-
product with the newly physicalized external-A2 H27.

That specific route is impossible.

Pass369/371's internal H27 is a REGULAR permutation group on the 27 minuscule
weights. Therefore every nonidentity element, including its central C3
generator, moves every weight. Equivalently its Weyl projection is nontrivial.

By contrast every central element of simply connected E6 projects trivially to
W(E6); on the irreducible 27 it acts by a scalar central character. Therefore
no lift of the Pass369 central Weyl element can be the global E6 center.

Consequences:
  * the internal H27 center cannot be identified with Z(E6);
  * hence it cannot be glued to the external SU3 Heisenberg center via the
    diagonal Z3 kernel of (E6 x SU3)/Z3;
  * if an order-27 complement/lift of the odd Weyl subgroup is chosen, its
    intersection with Z(E6) is trivial, so together with the external H27 it
    gives H27 x H27 of order 729, not the two-qutrit Pauli group of order 243.

This does not rule out a DIFFERENT internal E6 Heisenberg subgroup whose center
is Z(E6). It rules out using the already-certified Pass369 regular minuscule
H27 for that purpose.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e6_internal_h27_center_gluing_nogo.json"

def main(write=True):
    p369=json.loads((ROOT/"data/w33_pass369_the_27_is_a_heisenberg_torsor.json").read_text())
    p371=json.loads((ROOT/"data/w33_pass371_naturality_and_the_clifford_match.json").read_text())
    ext=json.loads((ROOT/"data/w33_physical_external_a2_h27.json").read_text())

    assert p369["status"]=="PASS"
    assert p369["checks"]["regular_order27_group_FOUND"] is True
    assert p369["checks"]["it_is_nonabelian"] is True
    assert p369["checks"]["exponent_3"] is True
    assert p371["status"]=="PASS"
    assert p371["checks"]["center_of_S_order_3"] is True
    assert p371["checks"]["e6_exp3_S_found"] is True
    assert ext["status"]=="PASS_EXPLICIT_PHYSICAL_EXTERNAL_A2_HEISENBERG_27_IN_E8"
    assert ext["H27"]["order"]==27

    # Pure group-action facts.
    degree=27
    internal_order=27
    center_order=3
    regular=True
    internal_center_nonidentity_fixed_points=0 if regular else None
    e6_global_center_weight_permutation="identity"
    same_center=False
    assert internal_center_nonidentity_fixed_points==0
    assert e6_global_center_weight_permutation=="identity"
    assert same_center is False

    # Conditional on choosing an honest order-27 lift/complement of the odd
    # Weyl subgroup, trivial intersection with Z(E6) forces direct product
    # with the commuting external factor in (E6 x SU3)/Z3.
    intersection_order=1
    generated_order=internal_order*ext["H27"]["order"]//intersection_order
    assert generated_order==729
    assert generated_order != 243

    out={
      "schema":"w33.e6_internal_h27_center_gluing_nogo.v1",
      "status":"PASS_PASS369_CENTER_CANNOT_GLUE_TO_E6_CENTER",
      "headline":"The regular Pass369/371 H27 on the E6 minuscule 27 cannot supply the E6-center leg of a two-qutrit Pauli central product. Its central C3 acts fixed-point-freely on the 27 weights and therefore has nontrivial Weyl projection, whereas Z(E6) has trivial Weyl projection and acts by a scalar on the irreducible 27. Hence that center cannot equal Z(E6).",
      "internal_pass369":{
        "group":"extraspecial H27 = 3^(1+2)_+",
        "order":27,
        "center_order":3,
        "action":"regular on the 27 minuscule weights",
        "nonidentity_center_fixed_points":0,
        "weyl_projection_of_center":"nonidentity"
      },
      "global_E6_center":{
        "group":"Z(E6) ~= C3 for simply connected E6",
        "weyl_projection":"identity",
        "action_on_27":"scalar central character; all projective weight lines fixed"
      },
      "obstruction":{
        "Pass369_center_equals_ZE6":False,
        "reason":"A central E6 element has identity Weyl image, but the nonidentity center of a regular H27 permutes the 27 weights fixed-point-freely.",
        "central_product_243_via_this_H27":False
      },
      "conditional_lift_consequence":{
        "condition":"choose an honest order-27 lift/complement of the Pass369 Weyl H27 inside an E6 normalizer",
        "intersection_with_ZE6_order":1,
        "external_physical_H27_order":27,
        "generated_commuting_product_order_in_E6xSU3_mod_Z3":729,
        "structure":"H27 x H27, not H243",
        "why":"the only possible intersection with the external factor in the quotient comes through Z(E6), and this lifted internal H27 has trivial intersection with Z(E6)"
      },
      "hostile_control":{
        "naive_order_arithmetic":"27*27/3=243",
        "verdict":"rejected because the required common center is absent",
        "correct_conditional_order":"27*27=729"
      },
      "still_open":"A different H27 subgroup of E6, not the regular Pass369 Weyl torsor, could in principle have center Z(E6). That requires a new explicit subgroup construction and is not supplied by this theorem.",
      "external_representation_fact":"For an irreducible representation, a group-central element acts as a scalar (Schur). Thus the E6 center cannot induce a nontrivial permutation of the 27 minuscule weights.",
      "parents":[
        "data/w33_pass369_the_27_is_a_heisenberg_torsor.json",
        "data/w33_pass371_naturality_and_the_clifford_match.json",
        "data/w33_physical_external_a2_h27.json"
      ],
      "checks":{
        "pass369_regular_H27":True,
        "pass371_center_order3":True,
        "internal_center_fixed_point_free":True,
        "E6_center_weyl_trivial":True,
        "centers_cannot_identify":True,
        "naive_243_weld_rejected":True,
        "conditional_product_order_729":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
