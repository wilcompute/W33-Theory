#!/usr/bin/env python3
"""
The lattice part of the holonet's fault-tolerance threshold, fixed by the
substrate: nominal coding gains of the GKP code lattices A2 < D4 < E8.

The flagged architecture residual is the quantitative fault-tolerance threshold
(GKP code distance + squeezing-dB budget). The full threshold needs a noise
model and the chosen FT protocol, but ONE part of it is purely the code lattice
and is therefore substrate-fixed: how much a given GKP lattice suppresses
displacement noise relative to the trivial (square, Z^{2n}) GKP code. That is the
lattice's NOMINAL CODING GAIN

    gamma(Lambda) = d_min^2(Lambda) / det(Lambda)^{1/n}   (linear),
    gamma_dB      = 10 * log10(gamma),

a standard lattice invariant (Conway-Sloane). Bigger gamma = larger minimum
distance per unit phase-space volume = lower required squeezing. The substrate's
GKP lattices are the DENSEST in their dimensions, so they MAXIMISE gamma among
symplectic lattices of that rank, and they are ISODUAL (symplectically
self-dual) -- the 'balanced GKP' condition (position and momentum protected
equally). So the substrate not only picks WHICH lattice (A2,D4,E8: the matter/
gauge tower) but also fixes the best achievable lattice-level error suppression.

Numbers (min norm 2 for A2,D4,E8; 4 for Leech; determinants 3,4,1,1):
  A2 : 0.6 dB, D4 : 1.5 dB, E8 : 3.0 dB, (Leech : 6.0 dB),
relative to the square code -- i.e. the substrate's 2-mode code (D4) already buys
~1.5 dB, and the 4-mode code (E8) ~3 dB, off the squeezing threshold for free.
Honest: this is the LATTICE contribution only; the absolute fault-tolerance
threshold also depends on the noise model, finite-squeezing GKP state quality,
and the syndrome-extraction/FT protocol -- not claimed here.
"""
from __future__ import annotations

import json
import math


def coding_gain(min_norm: float, det: float, n: int):
    gamma = min_norm / det ** (1.0 / n)
    return gamma, 10.0 * math.log10(gamma)


def main():
    # (name, dimension n, min squared norm, determinant, isodual?)
    lattices = [
        ("Z^2 (square, baseline)", 2, 1, 1, True),
        ("A2 (hexagonal, 1 mode)", 2, 2, 3, True),
        ("D4 (2 modes)", 4, 2, 4, True),
        ("E8 (4 modes)", 8, 2, 1, True),
        ("Leech L24 (12 modes)", 24, 4, 1, True),
    ]
    print("[nominal coding gain of GKP code lattices, vs the square code]")
    print("  lattice                  | n  | d_min^2 | det | gamma | dB    | isodual")
    rows = []
    for name, n, mn, det, iso in lattices:
        g, gdb = coding_gain(mn, det, n)
        rows.append({"lattice": name, "n": n, "d_min2": mn, "det": det,
                     "gamma": round(g, 4), "dB": round(gdb, 3), "isodual": iso})
        print(f"  {name:24s} | {n:2d} | {mn:7d} | {det:3d} | {g:5.3f} | "
              f"{gdb:5.3f} | {iso}")

    # checks against the standard Conway-Sloane values
    def gdb(mn, det, n):
        return round(coding_gain(mn, det, n)[1], 2)
    assert gdb(2, 3, 2) == 0.62          # A2 ~ 0.6 dB
    assert gdb(2, 4, 4) == 1.51          # D4 ~ 1.5 dB
    assert gdb(2, 1, 8) == 3.01          # E8 ~ 3.0 dB
    assert gdb(4, 1, 24) == 6.02         # Leech ~ 6.0 dB
    print("\n  coding gains 0.6 / 1.5 / 3.0 / 6.0 dB (A2/D4/E8/Leech) confirmed.")
    print("  all substrate GKP lattices are ISODUAL (balanced GKP: q,p protected")
    print("  equally) and densest in their dimension (max gain at that rank).")

    print("\nRESULT: the substrate fixes the LATTICE part of the FT threshold.")
    print("  D4 (the holonet's 2-mode code) buys ~1.5 dB and E8 (4-mode) ~3.0 dB")
    print("  of squeezing-threshold margin over the trivial square code, for free,")
    print("  because the matter/gauge lattices are the densest isodual lattices.")
    print("  RESIDUAL (not claimed): the absolute threshold also needs the noise")
    print("  model, finite-squeezing state quality, and the FT protocol.")

    out = {
        "result": "substrate GKP lattices A2/D4/E8 are isodual + densest, with "
                  "nominal coding gains 0.6/1.5/3.0 dB (lattice part of the FT "
                  "threshold)",
        "coding_gains": rows,
        "formula": "gamma = d_min^2 / det^{1/n}; dB = 10 log10(gamma)",
        "isodual": "all are symplectically self-dual = balanced GKP",
        "honest_scope": "lattice contribution only; absolute fault-tolerance "
                        "threshold also needs noise model + finite-squeezing GKP "
                        "state quality + FT/syndrome protocol -- not claimed",
        "sources": ["Conway-Sloane, Sphere Packings, Lattices and Groups "
                    "(nominal coding gains)",
                    "Conrad-Eisert-Hangleiter, GKP codes: a lattice perspective, "
                    "Quantum 6, 648 (2022)"],
    }
    with open("data/w33_gkp_coding_gain.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_gkp_coding_gain.json")


if __name__ == "__main__":
    main()
