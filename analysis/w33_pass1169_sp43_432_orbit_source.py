#!/usr/bin/env python3
"""Pass 1169 v2: corrected 432-coset restriction mechanism."""
from __future__ import annotations
import json
from pathlib import Path


def main() -> dict:
    psp, sp, we6, a5, s5 = 25920, 51840, 51840, 60, 120
    assert we6//s5 == psp//a5 == sp//s5 == 432
    result={
      "schema":"w33.pass1169.coset_restriction_432.v2","status":"BOUNDARY_LOCKED",
      "groups":{
        "PSp(4,3)":{"order":psp,"role":"faithful projective subgroup"},
        "Sp(4,3)":{"order":sp,"role":"central double cover of PSp(4,3)"},
        "W(E6)":{"order":we6,"role":"outer extension PSp(4,3):2"},
      },
      "coset_sizes":{"W(E6)/S5":we6//s5,"PSp(4,3)/A5":psp//a5,"Sp(4,3)/order120":sp//s5},
      "correct_bridge":"Restrict the W(E6)/S5 action to the normal index-two PSp(4,3) subgroup. It is the PSp/A5 coset action exactly when S5 intersects PSp in A5.",
      "required_unfinished_check":"Compute the intersection H∩PSp for each of the three 432-orbit stabilizers and exhibit the equivariant bijection.",
      "rejected_bridge":"There is no asserted central quotient W(E6)->Sp(4,3), and S5 cannot quotient to A5 by killing a central involution because S5 has trivial center and no normal C2.",
      "projective_geometry":{"points":40,"lines":40,"flags":160,"unordered_pair_orbits":[240,540]},
    }
    out=Path("data/SP43_432_ORBIT_SOURCE_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1169 v2 432 bridge reduced to subgroup-intersection test")
    return result


if __name__=="__main__":main()
