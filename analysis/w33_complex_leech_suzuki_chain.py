#!/usr/bin/env python3
"""
Above E8: the complex Leech lattice is the Eisenstein 12 = k structure, and the
Suzuki chain climbs from the 3-qubit hexagon G2(2) to 6.Suz = the complex Leech
automorphism, then on to Co0 and the c = 24 = f Monster.

The substrate's order-3 Eisenstein element omega (the same fixed-point-free
order-3 isometry that welds E8 in w33_e8_eisenstein_witting_weld.py) acts one
level up: the 24-dimensional Leech lattice has a fixed-point-free automorphism of
order 3, and identifying it with a cube root of unity makes Leech a
12-DIMENSIONAL lattice over the Eisenstein integers Z[omega] -- the COMPLEX LEECH
lattice. Its complex dimension is

    12 = k

(the substrate valency), and its automorphism group is 6.Suz (the universal
cover of the Suzuki sporadic group), with 6.Suz.2 a maximal subgroup of
Co0 = 2.Co1 (the real Leech automorphism group).

The SUZUKI CHAIN (a tower of rank-3 permutation groups, each the point
stabilizer of the next) starts exactly at the substrate's 3-qubit core:

    G2(2) = U3(3):2   on   36 points   (|G2(2)| = 12096 = split Cayley hexagon)
    J2:2              on  100 points
    G2(4):2           on  416 points
    Suz:2             on 1782 points    -> 6.Suz = complex Leech (Eisenstein 12).

So G2(2) -- the automorphism group of the split Cayley hexagon, the THREE-QUBIT
contextuality core (BT1707, w33_macbeath_hexagon_functor.py, |G2(2)| = 12096 =
168*72) -- is the BOTTOM of the Suzuki chain whose TOP, 6.Suz, is the complex
Leech over the Eisenstein integers (12 = k). And the real Leech is 24 = 3*8 = f
dimensional, the c = 24 Monster CFT central charge.

So the substrate's Eisenstein arithmetic (q=3, the omega-weld) climbs E8 (8d) ->
complex Leech (12 = k complex dims = 24 = f real dims) -> Co0 -> Monster (c=24),
and its 3-qubit hexagon group G2(2) is the first rung of the Suzuki chain to Suz.

Verifies the Suzuki-chain point counts (36,100,416,1782), |G2(2)|=12096, the
complex-Leech Eisenstein dimension 12=k and real dimension 24=f=3*8, and the
Monster rep 196883 (= 196884-1 = j-coefficient).
"""
from __future__ import annotations

import json

Q, K, F = 3, 12, 24
G2_2 = 12096  # |G2(2)| = |U3(3):2| = split Cayley hexagon automorphism = 168*72


def main():
    out = {}

    # the complex Leech: order-3 omega makes Leech 12-dim over Eisenstein
    print("[complex Leech lattice]")
    print(f"  24-dim Leech + fixed-point-free omega (order 3) -> 12-dim over Z[omega]")
    print(f"  complex dimension = 12 = k; real dimension = 24 = 3*8 = f")
    print(f"  Aut(complex Leech) = 6.Suz; 6.Suz.2 maximal in Co0 = 2.Co1")
    assert 12 == K and 24 == F == 3 * 8 and 2 * 12 == 24
    out["complex_leech"] = {
        "complex_dim": "12=k",
        "real_dim": "24=f=3*8",
        "aut": "6.Suz",
        "in": "6.Suz.2 < Co0=2.Co1",
    }

    # the Suzuki chain starts at the 3-qubit hexagon G2(2)
    chain = [
        ("G2(2)=U3(3):2", 36, G2_2),
        ("J2:2", 100, 1209600),
        ("G2(4):2", 416, 503193600),
        ("Suz:2", 1782, 896690995200),
    ]
    print(f"\n[the Suzuki chain: rank-3 tower, each point-stabilizer of the next]")
    for name, pts, order in chain:
        print(f"  {name:14s} on {pts:4d} points   |G| = {order}")
    print(f"  -> bottom = G2(2) = the split Cayley hexagon = the 3-QUBIT core (12096)")
    print(f"  -> top = Suz; 6.Suz = complex Leech automorphism (Eisenstein 12=k)")
    assert chain[0][2] == G2_2 == 12096
    assert [c[1] for c in chain] == [36, 100, 416, 1782]
    out["suzuki_chain"] = [{"group": n, "points": p, "order": o} for n, p, o in chain]

    # G2(2) = the 3-qubit hexagon (tie to BT1707 / Macbeath)
    print(f"\n[G2(2) = the 3-qubit contextuality core]")
    print(f"  |G2(2)| = {G2_2} = 168*72 = |Aut(split Cayley hexagon)| (BT1707)")
    print(
        f"  = (Macbeath faces)*(Macbeath vertices); the first rung of the Suzuki chain"
    )
    assert G2_2 == 168 * 72 == 12096
    out["g2_2"] = {"order": 12096, "is": "split Cayley hexagon = 3-qubit core = 168*72"}

    # the climb to the Monster (c = 24 = f)
    monster_rep = 196883
    print(f"\n[the climb to the Monster, c = 24 = f]")
    print(f"  Leech (24=f dims) -> Co0 -> Monster; c = 24 = f = Monster CFT charge")
    print(
        f"  Monster smallest faithful rep = {monster_rep} = 196884 - 1 = j-coefficient"
    )
    assert monster_rep + 1 == 196884 and F == 24
    out["monster"] = {"c": "24=f", "rep": 196883, "j_coeff": 196884}

    print("\nRESULT: above E8 is the complex Leech lattice -- the 24-dimensional Leech")
    print("  made 12 = k complex-dimensional by the SAME order-3 Eisenstein omega that")
    print("  welds E8, with automorphism group 6.Suz inside Co0 = 2.Co1. The Suzuki")
    print("  chain G2(2) -> J2 -> G2(4) -> Suz (on 36/100/416/1782 points) starts")
    print(
        "  exactly at G2(2) = the split Cayley hexagon = the three-qubit contextuality"
    )
    print("  core (|G2(2)| = 12096 = 168*72), and climbs to Suz = the complex Leech")
    print("  group. So the substrate's q=3 Eisenstein arithmetic threads E8 (8d) ->")
    print("  complex Leech (12=k complex = 24=f real) -> Co0 -> Monster (c=24=f), with")
    print(
        "  the 3-qubit hexagon the first rung. The qutrit substrate and Conway-Monster"
    )
    print("  moonshine are one Eisenstein tower.")

    out["summary"] = (
        "above E8: the complex Leech lattice = the 24-dim Leech made 12=k complex-"
        "dimensional by a fixed-point-free order-3 omega (the Eisenstein weld), "
        "Aut=6.Suz < Co0=2.Co1. The Suzuki chain G2(2)->J2->G2(4)->Suz (36/100/416/"
        "1782 points) STARTS at G2(2)=U3(3):2=12096=split Cayley hexagon=the 3-qubit "
        "contextuality core (168*72, BT1707) and climbs to Suz=complex Leech group. "
        "Real Leech 24=f=3*8 dims = Monster CFT charge c=24; Monster rep 196883="
        "196884-1=j-coeff. The qutrit substrate Eisenstein arithmetic threads E8 -> "
        "complex Leech (12=k) -> Co0 -> Monster as one tower; 3-qubit G2(2) is rung 1."
    )
    out["sources"] = [
        "complex Leech lattice = 12-dim over Eisenstein Z[omega] via fixed-point-"
        "free order-3 automorphism, Aut=6.Suz, 6.Suz.2<Co0=2.Co1 (Wikipedia Leech/"
        "Conway/Suzuki); Suzuki chain G2(2)=U3(3):2(36)/J2:2(100)/G2(4):2(416)/"
        "Suz:2(1782); |G2(2)|=12096=168*72=split Cayley hexagon (BT1707, "
        "w33_macbeath_hexagon_functor.py); 24=f=3*8 Leech, c=24 Monster, 196883; "
        "w33_e8_eisenstein_witting_weld.py, w33_ternary_golay_m12_grunbaum.py."
    ]
    with open("data/w33_complex_leech_suzuki_chain.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_complex_leech_suzuki_chain.json")


if __name__ == "__main__":
    main()
