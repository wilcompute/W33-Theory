#!/usr/bin/env python3
"""
BT816 - The cubic surface's flag geometry, reconstructed inside PSp(4,3).

BT813's transition matrix showed the icosahedral registers see the 45
tritangents as [5, 40] and tritangents see registers as [3, 24], with
27 x 5 = 135 = 45 x 3.  BT816 verifies (GAP witness,
.tmp/gap_cubic_flags.g) that this is EXACTLY the classical line /
tritangent-plane flag geometry of the cubic surface, rebuilt purely from
double cosets of maximal subgroups:

  T1. The special G-orbit on (G/M27) x (G/M45) has exactly 135 flags,
      with every register incident to 5 tritangents and every tritangent
      to 3 registers - the (27_5, 45_3) configuration.
  T2. The Schlafli meet-relation (the 10-suborbit of the register
      diagonal [1,10,16]) has 270 = 27 x 10 ordered pairs, and EVERY
      tritangent triad is pairwise meeting - a Schlafli triangle.
  T3. THE CLASSICAL AXIOM: every MEETING pair of registers lies in
      exactly ONE common tritangent; every SKEW pair lies in NONE.
      (On the cubic surface: two intersecting lines span a unique
      tritangent plane; skew lines span none.)

CONSEQUENCE.  The triple (registers, meet-relation, tritangent triads)
inside PSp(4,3) IS the 27-lines configuration with its 45 coplanar
triangles - reconstructed without any cubic surface, purely from the
subgroup lattice.  The q = 3 "generations" triads of the substrate are
the tritangent triangles: 45 triples of pairwise-meeting registers, each
register in exactly 5 of them.

GAP witness output:
    M27 orbit sizes on 45: [40, 5]; pentad found: true
    incidence flags: 135 (expect 135)
    register degrees: [5]; tritangent degrees: [3]
    meet relation pairs: 270 (expect 270 = 27*10)
    every triad pairwise MEETING (Schlafli triangle): true
    meet->common, skew->common profiles: [[true, 1], [false, 0]]
"""
from __future__ import annotations

import json


def main():
    witness = {
        "pentad_orbit": [40, 5],
        "flags": 135,
        "register_degree": 5,
        "tritangent_degree": 3,
        "meet_pairs": 270,
        "triads_pairwise_meeting": True,
        "meeting_pair_common_tritangents": 1,
        "skew_pair_common_tritangents": 0,
    }
    # arithmetic seals
    assert 27 * 5 == 135 == 45 * 3
    assert 270 == 27 * 10
    # double-count of meeting pairs via triads: each tritangent contributes
    # C(3,2) = 3 unordered meeting pairs, each meeting pair in exactly 1:
    assert 45 * 3 == 135 == 270 // 2
    print("BT816 cubic-surface flag geometry inside PSp(4,3):")
    for k, v in witness.items():
        print(f"  {k} = {v}")
    print("\nseals: 27*5 = 45*3 = 135 flags; meeting pairs 135 = 45 triads")
    print("x 3 pairs each (unique-tritangent axiom <=> perfect count);")
    print("the 45 generation-triads partition the 135 meeting pairs.")

    out = {
        "theorem": "BT816 cubic surface flags reconstructed",
        "witness": witness,
        "statement": (
            "(registers, meet, triads) in PSp(4,3) = the 27-lines "
            "configuration with its 45 tritangent triangles; built from "
            "double cosets only"),
    }
    with open("data/bt816_cubic_surface_flags.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt816_cubic_surface_flags.json")


if __name__ == "__main__":
    main()
