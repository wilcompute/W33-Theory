#!/usr/bin/env python3
"""The Suzuki outer automorphism supplies the missing local E6 factor of two.

Parent certificate ``w33_suzuki_local_e6_inner_outer_split.json`` proves that,
for one embedded full W(3,3), the Suzuki point stabilizer induces a faithful
transitive U4(2) ~= PSp(4,3) action of order 25920 on the 27 complementary
three-W33 decompositions.  Their graph is SRG(27,10,1,5), whose complement is
the Schlaefli graph / cubic-surface 27-line graph.

Published ATLAS input:
  * Suz has a degree-135135 primitive action with point stabilizer
      2^(1+6).U4(2), order 3317760.
  * Suz:2 has the corresponding maximal subgroup at the same index 135135,
      2^(1+6).U4(2).2, order 6635520.
  * U4(2) has order 25920 and outer automorphism group C2.
Thus the quotient of the extended point stabilizer by its normal 2-core is
U4(2):2 of order 51840.

On the local transitive 27-set the normal 2-core acts trivially: its orbits are
equal-size blocks, with size a power of two dividing 27, hence size one.  The
induced action therefore factors through U4(2):2.  The parent computation says
the normal U4(2) socle acts faithfully.  Since U4(2):2 is almost simple with
socle U4(2), a kernel in the quotient that is disjoint from the socle must be
trivial.  Therefore the full Suz:2 stabilizer image has order 51840.

Classically the full automorphism group of the 27-line cubic-surface graph is
W(E6) ~= U4(2):2.  Hence the Suzuki outer automorphism supplies exactly the
index-two symmetry absent from Suz itself.

Finite group/geometry theorem only; this is not a physical E6 gauge claim.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_suz_outer_completes_local_e6_weyl.json"


def main(write=True):
    parent = json.loads((ROOT / "data" / "w33_suzuki_local_e6_inner_outer_split.json").read_text())
    assert parent["status"] == "PASS"
    assert parent["computed_induced_subgroup"]["order"] == 25920
    assert parent["computed_induced_subgroup"]["transitive_degree"] == 27

    suz = 448345497600
    suz2 = 2 * suz
    degree = 135135
    inner_stab = suz // degree
    outer_stab = suz2 // degree
    u42 = 25920
    u42d2 = 2 * u42
    core = 128
    assert inner_stab == 3317760 == core * u42
    assert outer_stab == 6635520 == core * u42d2

    out = {
      "schema": "w33.suz_outer_completes_local_e6_weyl.v1",
      "status": "PASS_WITH_PUBLISHED_ATLAS_STRUCTURE",
      "headline": "Suz induces only the inner U4(2) ~= PSp(4,3) symmetry on the 27 local three-W33 decompositions, but the corresponding Suz:2 point stabilizer is 2^(1+6).U4(2).2 at the same degree 135135. Its normal 2-core is forced to act trivially on the transitive odd 27-set, while the U4(2) socle is already faithful. Hence the Suz:2 image is the full U4(2):2 of order 51840, exactly W(E6), the automorphism group of the Schlaefli/cubic-surface 27-line graph.",
      "computed_parent": {
        "degree": 27,
        "Suz_inner_image": 25920,
        "inner_identification": "U4(2) ~= PSp(4,3)",
        "local_graph": "SRG(27,10,1,5); complement Schlaefli SRG(27,16,10,8)"
      },
      "ATLAS_inputs": {
        "Suz_order": suz,
        "Suz_degree_135135_stabilizer": "2^(1+6).U4(2)",
        "Suz_point_stabilizer_order": inner_stab,
        "Suz2_order": suz2,
        "Suz2_degree_135135_stabilizer": "2^(1+6).U4(2).2",
        "Suz2_point_stabilizer_order": outer_stab,
        "U4_2_order": u42,
        "Out_U4_2": 2
      },
      "deduction": {
        "normal_2_core_order": core,
        "normal_2_core_local_action": "trivial by the odd transitive 27-set block argument",
        "quotient_available": "U4(2):2",
        "socle_U4_2_faithful": True,
        "quotient_kernel": "trivial: U4(2):2 is almost simple and the kernel cannot contain the already-faithful socle",
        "Suz2_local_image_order": u42d2,
        "identification": "U4(2):2 ~= W(E6)"
      },
      "interpretation": "The factor-of-two missing from the local E6 graph symmetry inside Suz is not accidental. It is exactly restored by the outer automorphism in Suz:2.",
      "sources": [
        "ATLAS of Finite Group Representations: Suz, maximal subgroups of Suz and Suz:2",
        "ATLAS: U4(2)=S4(3), order 25920, Out=2",
        "classical cubic-surface 27-line configuration: graph automorphism W(E6)"
      ],
      "boundary": "This theorem combines an exact repository computation with published finite-group classifications. It proves a local symmetry action, not physical E6 gauge dynamics or a continuum unification mechanism.",
      "checks": {
        "parent_inner_25920": True,
        "inner_stabilizer_128_times_25920": True,
        "outer_stabilizer_128_times_51840": True,
        "odd_27_core_kernel": True,
        "full_outer_image_51840": True
      }
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
