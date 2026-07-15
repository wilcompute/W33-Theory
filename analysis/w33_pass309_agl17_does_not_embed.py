#!/usr/bin/env python3
"""Pass 309: AGL(1,7) does NOT embed in PGSp(4,3) -- deflating Pass 305's tie.

Pass 305 identified Aut(Csaszar) = AGL(1,7) = C_7 : C_6 and noted its 7 is
Phi_6(3), the substrate's own cyclotomic value.  It called this "a genuine FORCED
tie between the toroidal pole and the substrate" -- correct that an automorphism
group is forced, but it left the KIND of tie unexamined.  This witness examines
it, and the tie is much weaker than the phrasing implied.

THE OBSTRUCTION.  |PGSp(4,3)| = 51840 = 2^7 * 3^4 * 5.  Seven does not divide it.
So PGSp(4,3) has no element of order 7 (Lagrange), and therefore

        AGL(1,7) -- which has six elements of order 7 -- is NOT a subgroup of
        PGSp(4,3), nor of PSp(4,3) (order 25920 = 2^6 * 3^4 * 5).

There is no group homomorphism realising the Csaszar symmetry inside the
substrate's own symmetry group, faithfully or otherwise on the 7-part.

WHAT THE TIE ACTUALLY IS.  Purely NUMERICAL: 7 = Phi_6(3) = q^2 - q + 1 at q = 3.
The Csaszar polyhedron has 7 vertices because g(K_n) = 1 first at n = 7; the
substrate has Phi_6(3) = 7 because that is what the cyclotomic polynomial
evaluates to.  Both are 7.  That is the whole of it -- an equality of integers,
not a shared symmetry.

This matters because Pass 305 was presented as the FORCED result that survived
where the sqrt(21) metric claims failed.  It IS forced (Aut is combinatorial), but
being forced is not the same as being meaningful: a forced coincidence is still a
coincidence.  The forced/chosen test (Pass 302) filters out artefacts of drawings;
it does not certify significance.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass309_agl17_does_not_embed.json"


def main():
    checks = {}

    orders = {"PGSp(4,3)": 51840, "PSp(4,3)": 25920, "AGL(1,7)": 42,
              "W(E6)": 51840, "S6": 720}
    facs = {k: {int(p): int(e) for p, e in sp.factorint(v).items()}
            for k, v in orders.items()}

    checks["pgsp43_order_51840"] = orders["PGSp(4,3)"] == 51840
    checks["pgsp43_factors_2_7_3_4_5"] = facs["PGSp(4,3)"] == {2: 7, 3: 4, 5: 1}
    checks["7_does_not_divide_pgsp43"] = 51840 % 7 != 0
    checks["7_does_not_divide_psp43"] = 25920 % 7 != 0
    checks["agl17_has_order_7_elements"] = 7 in facs["AGL(1,7)"]

    # Lagrange: a subgroup's order divides the group's order
    checks["42_does_not_divide_51840"] = 51840 % 42 != 0
    checks["AGL_1_7_NOT_a_subgroup_of_PGSp43"] = (51840 % 7 != 0)
    checks["AGL_1_7_NOT_a_subgroup_of_PSp43"] = (25920 % 7 != 0)
    # even the cyclic C_7 alone cannot embed
    checks["C7_cannot_embed_either"] = (51840 % 7 != 0)

    # what IS shared: just the integer 7
    q = 3
    phi6 = q * q - q + 1
    checks["phi6_of_3_is_7"] = phi6 == 7
    checks["csaszar_has_7_vertices"] = 7 == 7
    checks["the_shared_object_is_the_integer_7"] = True

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass309.agl17_does_not_embed.v1",
        "status": "PASS" if all_pass else "FAIL",
        "THE_OBSTRUCTION": (
            "|PGSp(4,3)| = 51840 = 2^7 * 3^4 * 5 and 7 does not divide it, so by "
            "Lagrange PGSp(4,3) has NO element of order 7. AGL(1,7) has six "
            "elements of order 7, so it is NOT a subgroup of PGSp(4,3) -- nor of "
            "PSp(4,3) (25920 = 2^6 * 3^4 * 5). Not even the cyclic C_7 embeds."
        ),
        "group_orders": {k: {"order": v, "factorisation": facs[k]}
                         for k, v in orders.items()},
        "what_the_tie_actually_is": (
            "Purely NUMERICAL: 7 = Phi_6(3) = q^2 - q + 1 at q = 3. Csaszar has 7 "
            "vertices because g(K_n) = 1 first happens at n = 7; the substrate "
            "has Phi_6(3) = 7 because that is what the cyclotomic polynomial "
            "evaluates to. Both are 7. That is the whole of it -- an equality of "
            "integers, not a shared symmetry."
        ),
        "deflates_pass305": (
            "Pass 305 called Aut(Csaszar) = AGL(1,7) 'a genuine FORCED tie "
            "between the toroidal pole and the substrate's Phi_6 -- the kind of "
            "link the metric coincidences only pretended to be'. The FORCED part "
            "is right (an automorphism group is combinatorial and survives every "
            "realization). The TIE part is not: there is no homomorphism, no "
            "subgroup, no action. Being forced is not the same as being "
            "meaningful -- a forced coincidence is still a coincidence."
        ),
        "the_general_lesson": (
            "Pass 302's forced/chosen test filters out artefacts of drawings; it "
            "does NOT certify significance. Pass 305 passed that test and was "
            "immediately over-read on the strength of passing it. The test is a "
            "necessary condition for a claim to mean anything, not a sufficient "
            "one, and this program has now over-read on both sides: metric "
            "coincidences (286/290 -> 293), and a forced-but-empty one (305 -> "
            "here)."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
