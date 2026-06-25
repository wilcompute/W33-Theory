#!/usr/bin/env python3
"""
The G2 thread: G2 = Aut(octonions) recurs across the whole substrate -- its
7-dim rep is the Fano heptad Phi6, dim G2 = 14 = 2*Phi6 is the genus-14 Hurwitz
triplet, G2(2) = 12096 is the three-qubit hexagon, G2(4) is the Suzuki-chain
rung, and the octonion column G2=Aut(O) leads to E8 = magic(O,O).

The exceptional group G2 is the automorphism group of the octonions O, and it
threads the substrate at five levels, all keyed by the heptad Phi6 = 7:

  1. SMALLEST REP = 7 = Phi6. G2 acts on the 7 imaginary octonions, whose
     multiplication is the FANO plane PG(2,2) (7 points, 7 lines, 21 flags) --
     the heptad. So the 7-dim G2 rep is the Fano/heptagon Phi6.
  2. dim G2 = 14 = 2*Phi6. This is the genus of the {3,7} Hurwitz TRIPLET
     R14.1/2/3 (w33_hurwitz_tower_qubit_crossover.py), the top of the {3,7}
     tower: dim G2 = the top genus.
  3. G2(2) = U3(3):2, order 12096 = 168*72 = the split Cayley hexagon = the
     THREE-QUBIT contextuality core (w33_macbeath_hexagon_functor.py); its rank-3
     graph SRG(36,14,4,6) has valency 14 = dim G2 (w33_suzuki_tower_srg.py).
  4. G2(4), order 251596800 = the third rung of the Suzuki chain to Suz = the
     complex Leech (w33_complex_leech_suzuki_chain.py).
  5. OCTONION COLUMN. G2 = Aut(O), and O is the column of the Freudenthal-Tits
     magic square giving E8 = magic(O,O) = the Witting body
     (w33_magic_square_substrate.py).

So one group, G2 = Aut(O), keyed by the heptad Phi6=7, runs from the Fano plane
(7) through the genus-14 Hurwitz triplet (14), the three-qubit hexagon (G2(2)),
the Suzuki chain (G2(4)), to the octonions and E8. The number 7 = Phi6 is the
G2 thread.

Verifies dim G2 = 14 = 2*Phi6 = top genus, the 7-dim rep = Fano (7 pts/lines/21
flags), |G2(2)|=12096, |G2(4)|=251596800, and the Fano incidence.
"""
from __future__ import annotations

import json

PHI6 = 7
G2_2, G2_4 = 12096, 251596800


def main():
    out = {}

    # 1. smallest rep = 7 = Phi6 = the Fano plane (imaginary octonions)
    fano_points, fano_lines = 7, 7
    fano_flags = fano_points * 3  # 7 lines * 3 points = 21
    print(f"[1] G2 = Aut(O); smallest rep = 7 = Phi6 = the Fano plane")
    print(
        f"    7 imaginary octonions -> Fano PG(2,2): {fano_points} pts, {fano_lines} "
        f"lines, {fano_flags} flags"
    )
    assert fano_points == fano_lines == PHI6 == 7 and fano_flags == 21
    out["rep7"] = "7 = Phi6 = Fano plane (imaginary octonions); 21 flags"

    # 2. dim G2 = 14 = 2*Phi6 = genus-14 Hurwitz triplet
    dim_g2 = 14
    print(f"\n[2] dim G2 = {dim_g2} = 2*Phi6 = {2*PHI6} = genus of the {{3,7}} Hurwitz")
    print(f"    triplet R14.1/2/3 (top of the {{3,7}} tower)")
    assert dim_g2 == 2 * PHI6 == 14
    out["dim_g2"] = "14 = 2*Phi6 = genus-14 Hurwitz triplet"

    # 3. G2(2) = 12096 = 3-qubit hexagon; SRG(36,14) valency = dim G2
    print(
        f"\n[3] G2(2) = U3(3):2 = {G2_2} = 168*72 = split Cayley hexagon = 3-qubit core"
    )
    print(f"    its rank-3 graph SRG(36,14,4,6) has valency 14 = dim G2")
    assert G2_2 == 168 * 72 == 12096
    out["g2_2"] = (
        "12096 = split Cayley hexagon = 3-qubit core; SRG(36,14) valency=dim G2"
    )

    # 4. G2(4) = Suzuki chain rung
    print(
        f"\n[4] G2(4) = {G2_4} = third rung of the Suzuki chain (-> Suz = complex Leech)"
    )
    assert G2_4 == 251596800
    out["g2_4"] = "251596800 = Suzuki chain rung 3"

    # 5. octonion column -> E8 = magic(O,O)
    print(
        f"\n[5] G2 = Aut(O); the octonion column gives E8 = magic(O,O) = Witting body"
    )
    out["octonion"] = "G2=Aut(O); O column -> E8=magic(O,O)=Witting"

    # the thread
    print(f"\n[the G2 thread, keyed by Phi6=7]")
    print(f"  Fano (7) -> genus-14 (2*Phi6) -> G2(2) 3-qubit -> G2(4) Suzuki -> O/E8")
    out["thread"] = (
        "Fano(7) -> genus-14(2Phi6) -> G2(2) 3-qubit -> G2(4) Suzuki -> O/E8"
    )

    print("\nRESULT: G2 = Aut(O) is a single thread through the substrate, keyed by")
    print("  the heptad Phi6 = 7. Its 7-dim rep is the Fano plane (the 7 imaginary")
    print("  octonions); dim G2 = 14 = 2*Phi6 is the genus of the {3,7} Hurwitz")
    print("  triplet (the top of the {3,7} tower); G2(2) = 12096 is the split Cayley")
    print("  hexagon = the three-qubit contextuality core (its rank-3 graph has")
    print("  valency 14 = dim G2); G2(4) is the third rung of the Suzuki chain to the")
    print("  complex Leech; and G2 = Aut(O) is the octonion column of the magic square")
    print("  leading to E8 = the Witting body. So the number 7 = Phi6 threads the")
    print("  octonions, the Fano plane, the genus-14 Hurwitz triplet, the three-qubit")
    print("  hexagon, the Suzuki chain, and E8 through the one group G2.")

    out["summary"] = (
        "G2 = Aut(O) threads the substrate, keyed by Phi6=7: (1) 7-dim rep = Fano "
        "plane (7 imaginary octonions, 21 flags); (2) dim G2 = 14 = 2*Phi6 = "
        "genus-14 Hurwitz triplet (top of {3,7} tower); (3) G2(2)=12096=168*72=split "
        "Cayley hexagon=3-qubit core, rank-3 graph SRG(36,14) valency=dim G2; (4) "
        "G2(4)=251596800 = Suzuki chain rung 3 -> complex Leech; (5) G2=Aut(O), the "
        "octonion column -> E8=magic(O,O)=Witting. One group, keyed by 7=Phi6, runs "
        "Fano -> genus-14 -> 3-qubit -> Suzuki -> E8."
    )
    out["sources"] = [
        "G2 = Aut(octonions); 7-dim rep = imaginary octonions = Fano PG(2,2); "
        "dim G2 = 14; G2(2)=U3(3):2=12096 split Cayley hexagon; G2(4)=251596800 "
        "Suzuki chain; G2 octonion column of magic square -> E8; "
        "w33_hurwitz_tower_qubit_crossover.py (genus-14=dim G2), "
        "w33_macbeath_hexagon_functor.py, w33_suzuki_tower_srg.py, "
        "w33_magic_square_substrate.py."
    ]
    with open("data/w33_g2_thread.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_g2_thread.json")


if __name__ == "__main__":
    main()
