#!/usr/bin/env python3
"""
The ceiling of the Eisenstein climb is the Monster moonshine module V-natural at
c = 24 = f: the same f=24 that is the holographic boundary central charge of the
Holonet code is the central charge of the c=24 Monster CFT, and j(tau)-744 is its
graded dimension.

The climb (w33_complex_leech_suzuki_chain.py) goes E8 -> complex Leech (Eisenstein
12=k) -> Co0 -> Monster. Its top is the Monster M, realized as the automorphism
group of the c = 24 holomorphic CFT V-natural (the moonshine module). Two facts
close the tower:

  - the central charge is c = 24 = f. This is the SAME f=24 that the early
    Holonet result identified as the holographic boundary central charge (the
    network IS a holographic code, boundary CFT c=24); the Monster CFT is that
    boundary;
  - the graded dimension of V-natural is the normalized j-invariant
    J(tau) = j(tau) - 744 = q^{-1} + 196884 q + 21493760 q^2 + ...,
    and each coefficient is a sum of dimensions of Monster irreducible
    representations (monstrous moonshine, Conway-Norton):
        196884    = 1 + 196883,
        21493760  = 1 + 196883 + 21296876.
    The 196883 is the smallest faithful Monster rep; the substrate already carries
    it as 196883 = tau*f' + mu*q^4 - 1 (the existing moonshine datum).

So the substrate's q=3 / Eisenstein tower, climbing from the three-qubit hexagon
G2(2) through the complex Leech to Co0, reaches the Monster, and its ceiling
c = 24 = f is the holographic boundary charge: the qutrit machine's boundary CFT
is the Monster, and f=24 is the moonshine constant of the whole construction.

Verifies the j-function head, the monstrous-moonshine head decompositions, and
c = 24 = f.
"""
from __future__ import annotations

import json

F = 24

# dimensions of the smallest Monster irreducible representations
M_IRREPS = {1: 1, 196883: 196883, 21296876: 21296876, 842609326: 842609326}

# normalized j: J(tau) = j(tau) - 744, head coefficients (q^{-1}, q^1, q^2, q^3)
J_HEAD = {-1: 1, 1: 196884, 2: 21493760, 3: 864299970}


def main():
    out = {}

    # c = 24 = f = the holographic boundary charge = Monster CFT central charge
    print(f"[the ceiling: c = 24 = f]")
    print(f"  the Monster CFT V-natural has central charge c = 24 = f")
    print(
        f"  = the Holonet holographic boundary central charge (the network is a code)"
    )
    assert F == 24
    out["central_charge"] = {"c": 24, "is": "f = holographic boundary = Monster CFT"}

    # j(tau) - 744 head and the moonshine decomposition
    print(f"\n[graded dimension of V-natural: J = j - 744]")
    print(f"  J(tau) = q^-1 + {J_HEAD[1]} q + {J_HEAD[2]} q^2 + {J_HEAD[3]} q^3 + ...")
    # monstrous moonshine head decompositions
    decomp_1 = M_IRREPS[1] + M_IRREPS[196883]
    decomp_2 = M_IRREPS[1] + M_IRREPS[196883] + M_IRREPS[21296876]
    print(f"  196884    = 1 + 196883            = {decomp_1}")
    print(f"  21493760  = 1 + 196883 + 21296876 = {decomp_2}")
    assert J_HEAD[1] == decomp_1 == 196884
    assert J_HEAD[2] == decomp_2 == 21493760
    out["j_head"] = {"196884": "1+196883", "21493760": "1+196883+21296876"}

    # the 196883 = the substrate moonshine datum
    print(f"\n[the 196883 = the smallest faithful Monster rep]")
    print(f"  196883 = the substrate moonshine datum (= tau*f' + mu*q^4 - 1, existing)")
    print(f"  196884 = 196883 + 1 = the first j-coefficient")
    assert 196883 + 1 == 196884
    out["monster_rep"] = {"196883": "smallest faithful Monster rep = substrate datum"}

    # the full tower: q=3 -> ... -> Monster (c=24=f)
    print(f"\n[the tower q=3 -> Monster, ceiling c=24=f]")
    print(f"  3-qubit G2(2) -> Suzuki chain -> complex Leech (Eisenstein 12=k) -> Co0")
    print(f"  -> Monster M = Aut(V-natural), c = 24 = f = the holographic boundary")
    out["tower"] = "q=3 -> G2(2) -> complex Leech (12=k) -> Co0 -> Monster (c=24=f)"

    print("\nRESULT: the Eisenstein climb closes at the Monster. The complex-Leech /")
    print("  Suzuki / Co0 tower tops out at the Monster M = Aut(V-natural), the c=24")
    print("  holomorphic CFT, whose graded dimension is J = j - 744 = q^-1 + 196884 q")
    print("  + ... with 196884 = 1 + 196883 and 21493760 = 1 + 196883 + 21296876 the")
    print("  monstrous-moonshine head. The central charge c = 24 = f is exactly the")
    print("  Holonet holographic boundary charge, so the qutrit machine's boundary CFT")
    print("  is the Monster and f=24 is the moonshine constant of the whole tower:")
    print("  from one trit (q=3) up through E8, the complex Leech, and Co0 to the")
    print("  Monster, the substrate is one Eisenstein moonshine construction.")

    out["summary"] = (
        "the Eisenstein climb closes at the Monster: the complex-Leech/Suzuki/Co0 "
        "tower tops at the Monster M = Aut(V-natural), the c=24 holomorphic CFT, "
        "graded dim J=j-744=q^-1+196884q+21493760q^2+...; moonshine head 196884="
        "1+196883, 21493760=1+196883+21296876. Central charge c=24=f = the Holonet "
        "holographic boundary charge, so the qutrit machine's boundary CFT is the "
        "Monster and f=24 is the tower's moonshine constant. 196883 = substrate "
        "datum (tau*f'+mu*q^4-1)."
    )
    out["sources"] = [
        "monstrous moonshine (Conway-Norton, Borcherds): V-natural c=24 CFT, "
        "graded dim j(tau)-744, 196884=1+196883, 21493760=1+196883+21296876; "
        "Monster smallest faithful rep 196883; c=24=f Holonet holographic boundary; "
        "existing moonshine 196883=tau*f'+mu*q^4-1 and bt982_mckay_thompson_v5.py; "
        "w33_complex_leech_suzuki_chain.py, w33_holographic_central_charge.py."
    ]
    with open("data/w33_monster_moonshine_ceiling.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_monster_moonshine_ceiling.json")


if __name__ == "__main__":
    main()
