#!/usr/bin/env python3
"""
Pass 91 -- Aut(W(3,3)) IS the Weyl group of E6: the symmetry capstone of the arithmetic tower.

Pass 90 found the two GQ(3,3) graphs have |Aut| = 51840 = |W(E6)| = |Sp(4,3)|.  This pass upgrades
that from an order coincidence to a proved group isomorphism (GAP, w33_pass91_e6.g):

  * Aut(W(3,3) collinearity graph) has order 51840; its derived subgroup is the SIMPLE group of
    order 25920, named by GAP
        B(2,3) = O(5,3) ~ C(2,3) = S(4,3) ~ 2A(3,2) = U(4,2) ~ 2D(3,2) = O-(6,2)
    i.e. PSp(4,3) = PSU(4,2) = P.Omega_6^-(2), of index 2.  So Aut(W) = PSp(4,3):2.
  * The Weyl group W(E6) has the SAME order 51840 and the SAME simple derived subgroup, and
    GAP's IsomorphismGroups(Aut(W), W(E6)) succeeds: Aut(W(3,3)) ~= W(E6).

Consequently the whole arithmetic tower of W(3,3) sits under one group, W(E6) = Sp(4,3), which acts
on the E6 cubic-surface configuration -- 27 lines, 36 double-sixes, 45 tritangent planes.  The 45
tritangent planes are exactly the 45 minimum-weight codewords of C_2(W) = [40,16,8] (Pass 85), and
the 240 = |E8 roots| appear as the minimum-weight words of the dual [40,24] (Pass 86).  So the
symmetry (W(E6)), the code (45, 240), and the arithmetic all express one exceptional structure.

Grounding: the graph automorphism group of the symplectic GQ W(3,q) is P.Gamma.Sp(4,q); for q=3
(trivial field automorphism) this is PSp(4,3):2 = W(E6) = SO_5(3).

ASCII-only.  Reads the committed GAP certificate.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GAP_OUT = ROOT / "w33_pass91_e6_out.txt"


def read_gap():
    txt = GAP_OUT.read_text()

    def grab(key):
        m = re.search(rf"{key}=(.*)", txt)
        return m.group(1).strip() if m else None

    return {
        "aut_order": int(grab("aut_order")),
        "derived_order": int(grab("derived_order")),
        "derived_is_simple": grab("derived_is_simple") == "true",
        "derived_simple_name": grab("derived_simple_name"),
        "aut_index_over_derived": int(grab("aut_index_over_derived")),
        "WE6_order": int(grab("WE6_order")),
        "WE6_derived_order": int(grab("WE6_derived_order")),
        "aut_iso_WE6": grab("aut_iso_WE6") == "true",
    }


def main():
    g = read_gap()

    # E6 cubic-surface configuration (what W(E6) permutes) and the code tie-ins
    e6_config = {
        "27": "lines on the cubic surface",
        "36": "double-sixes",
        "45": "tritangent planes = 45 minimum-weight codewords of C_2(W)=[40,16,8] (Pass 85)",
        "72": "roots of E6",
        "78": "dim E6 = 2(f+g) = the Ihara oscillatory amplitude (Pass 74)",
        "240": "roots of E8 = 240 min-weight words of the dual [40,24] (Pass 86) = edges of W(3,3)",
    }

    checks = {
        "aut_order_51840": g["aut_order"] == 51840,
        "derived_simple_order_25920": g["derived_order"] == 25920
        and g["derived_is_simple"],
        "aut_is_PSp43_dot_2": g["aut_index_over_derived"] == 2,
        "WE6_same_order_and_derived": g["WE6_order"] == 51840
        and g["WE6_derived_order"] == 25920,
        "Aut_W_isomorphic_to_WE6": g["aut_iso_WE6"],
        "simple_group_is_PSp43_family": "S(4,3)" in g["derived_simple_name"]
        and "U(4,2)" in g["derived_simple_name"],
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print("PASS 91 -- Aut(W(3,3)) IS THE WEYL GROUP OF E6")
    print("=" * 78)
    print(f"|Aut(W(3,3))| = {g['aut_order']} = |W(E6)| = |Sp(4,3)|")
    print(
        f"derived subgroup: order {g['derived_order']}, simple = {g['derived_is_simple']}"
    )
    print(f"   named: {g['derived_simple_name']}")
    print(
        f"   (= PSp(4,3) = PSU(4,2) = P.Omega_6^-(2)), index {g['aut_index_over_derived']} in Aut(W)"
    )
    print(
        f"W(E6): order {g['WE6_order']}, derived {g['WE6_derived_order']} (same simple group)"
    )
    print(f"GAP IsomorphismGroups(Aut(W), W(E6)) succeeds: {g['aut_iso_WE6']}")
    print()
    print(
        "W(E6) = Sp(4,3) permutes the E6 cubic-surface configuration, which threads the tower:"
    )
    for n, desc in e6_config.items():
        print(f"   {n:>3} : {desc}")
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass91.e6.v1",
        "status": "PASS" if all_ok else "FAIL",
        "aut_order": g["aut_order"],
        "derived": {
            "order": g["derived_order"],
            "simple": g["derived_is_simple"],
            "name": g["derived_simple_name"],
            "index_in_aut": g["aut_index_over_derived"],
        },
        "WE6": {"order": g["WE6_order"], "derived_order": g["WE6_derived_order"]},
        "Aut_W_isomorphic_to_WE6": g["aut_iso_WE6"],
        "e6_configuration": e6_config,
        "reading": (
            "Aut(W(3,3)) = PSp(4,3):2 is isomorphic to W(E6) (verified by GAP). So the whole "
            "W(3,3) arithmetic tower -- Ihara zeta, class number/group, code [40,16,8], "
            "dual [40,24], even lattice, weight-20 modular form -- lives under a single "
            "exceptional symmetry, W(E6)=Sp(4,3), whose 27 lines / 45 tritangent planes / "
            "240 E8 roots recur throughout the code and lattice. The symmetry, the code, "
            "and the arithmetic are three faces of one exceptional object."
        ),
        "grounding": "graph automorphism group of the symplectic GQ W(3,q) is P.Gamma.Sp(4,q); "
        "at q=3 this is PSp(4,3):2 = W(E6) = SO_5(3).",
        "checks": checks,
    }
    (ROOT / "w33_pass91_e6.json").write_text(json.dumps(payload, indent=2))
    print("[wrote] w33_pass91_e6.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
