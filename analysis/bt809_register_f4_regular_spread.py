#!/usr/bin/env python3
"""
BT809 - The icosahedral register is F4^2; the icosahedral spread is THE
        regular spread (stabilizer = the index-36 maximal).

GAP witness (.tmp/gap_register_spread.g), all three conjectures CONFIRMED:

  T1. In the index-27 maximal M = 2^4:A5 of PSp(4,3), the normal 2^4 is
      elementary abelian with M/N = A5 acting IRREDUCIBLY (MeatAxe) in
      dimension 4 over F2.  A5 = SL(2,4) and the unique irreducible
      4-dim F2-module is the natural SL(2,4)-module with scalars
      restricted: THE ICOSAHEDRAL REGISTER IS F4^2 - a two-qudit space
      over the four-element field, carried at matter-shell index 27.

  T2. The stabilizer in Sp(4,3) of the icosahedral spread (BT808) is
      SL(2,9):2 of order 1440 (720 mod center) - precisely the index-36
      maximal S6 = PSigmaL(2,9).  Hence the spread orbit has size 36:
      W(3,3) carries EXACTLY 36 regular spreads, permuted transitively,
      and the embedding chain is

          2I = SL(2,5)  <  SL(2,9)  <  SL(2,9):2 = Stab(spread).

      The 600-cell group is the icosahedral core of a regular-spread
      stabilizer.

  T3. Both icosahedral point-20-orbits meet EVERY spread line in exactly
      2 points: the ten 4-point fibers split 2+2 across the two
      hemispheres - the spread is an icosahedrally balanced fibration.

PYTHON CHECKS (cheap re-verifications):
  * |2^4:A5| = 960 = 2*(600-120) (BT808 user identity)
  * index bookkeeping: 27*960 = 36*720*... = 25920 etc.
  * maximal-subgroup geography table of PSp(4,3).
"""
from __future__ import annotations

import json


def main():
    psp = 25920
    geography = {
        27: ("2^4 : A5", 960, "F4^2 register : icosahedron (BT808/809)"),
        36: ("S6 = PSigmaL(2,9)", 720, "regular spread stabilizer (BT809)"),
        40: ("parabolic P1", 648, "point stabilizer (building)"),
        # second 40 is the line parabolic
        45: ("2^(1+4)-type", 576, "open: edge-family stabilizer"),
    }
    print("PSp(4,3) maximal geography:")
    for idx, (name, order, role) in sorted(geography.items()):
        assert idx * order == psp, (idx, order)
        print(f"  index {idx:3d}: {name:20s} order {order:4d}  {role}")

    assert 960 == 2 * (600 - 120)
    assert 960 == 16 * 60
    print("\n960 = 2*(600-120) = |F4^2| * |A5|  (both identities exact)")

    gap_witness = {
        "register_elementary_abelian": True,
        "register_quotient": "A5",
        "register_module": "irreducible, dim 4 over GF(2) = SL(2,4) natural"
                           " = F4^2",
        "spread_stab_order_sp": 1440,
        "spread_stab_structure": "SL(2,9):2",
        "spread_orbit_size": 36,
        "fiber_split": "each point-20-orbit meets each spread line in 2",
    }
    print("\nGAP witness:")
    for k, v in gap_witness.items():
        print(f"  {k} = {v}")

    print("\nTHE CHAIN:  2I = SL(2,5) < SL(2,9) < SL(2,9):2 = Stab(spread)")
    print("36 regular spreads, transitive; the 600-cell group is the")
    print("icosahedral core of a regular-spread stabilizer; the spread")
    print("fibers split 2+2 over the two icosahedral hemispheres.")

    out = {
        "theorem": "BT809 F4^2 register + regular spread",
        "geography": {str(k): v for k, v in geography.items()},
        "gap_witness": gap_witness,
        "chain": "SL(2,5) < SL(2,9) < SL(2,9):2 = Stab(spread)",
        "regular_spreads": 36,
    }
    with open("data/bt809_register_f4_regular_spread.json", "w") as fj:
        json.dump(out, fj, indent=2)
    print("\nwrote data/bt809_register_f4_regular_spread.json")


if __name__ == "__main__":
    main()
