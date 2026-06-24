#!/usr/bin/env python3
"""
The full {3,n} register atlas: every admissible vertex figure n = 6 + d (d|k=12)
is a substrate REGISTER, and the {3,n} family is its surface tower.

Completing w33_genus_vertex_figure_selection.py: the genus 2<=g<=14 triangular
regular maps select vertex figures n in {7,8,9,10,12} = {Phi6, 2^3, q^2, Phi4, k}.
For each n the {3,n} family has the closed parametrization
    V = 12(g-1)/(n-6),  E = 6n(g-1)/(n-6),  F = 4n(g-1)/(n-6),  |Aut|_rot = 2E,
so per unit of (g-1) the coefficients (cV, cE, cF) are:

    n= 7  Phi6  qutrit heptagon         (12, 42, 28)
    n= 8  2^3   qubit octagon           ( 6, 24, 16)
    n= 9  q^2   single-qutrit phase sp.  ( 4, 18, 12)
    n=10  Phi4  Sp4 / contextual denom   ( 3, 15, 10)
    n=12  k     the degree itself        ( 2, 12,  8)

Each vertex figure is the dimension of a substrate register:
  - n=7=Phi6: one-qutrit readout period (Fano/heptad);
  - n=8=2^3: three-qubit Hilbert space GF(8);
  - n=9=q^2: the single-qutrit phase space F3xF3 = AG(2,3) = the Hesse 9 points
    (the Hessian configuration of fgmarcelis; 4 parallel classes = 4 MUBs);
  - n=10=Phi4: dim Sp(4) = the contextual-fraction denominator (1/Phi4 = 1/10);
  - n=12=k: the W(3,3) valency / the degree.

Verifies the per-n parametrization against all Table-1 maps and the register
identifications.
"""
from __future__ import annotations

import json

Q, LAM, MU, K, F, PHI4, PHI6 = 3, 2, 4, 12, 24, 10, 7

# Table 1 maps grouped is unnecessary; (label, g, n, V, E, F)
TABLE1 = [
    ("R3.1", 3, 7, 24, 84, 56),
    ("R3.2", 3, 8, 12, 48, 32),
    ("R5.1", 5, 8, 24, 96, 64),
    ("R6.1", 6, 10, 15, 75, 50),
    ("R7.1", 7, 7, 72, 252, 168),
    ("R8.1", 8, 8, 42, 168, 112),
    ("R8.2", 8, 8, 42, 168, 112),
    ("R10.1", 10, 9, 36, 162, 108),
    ("R10.2", 10, 12, 18, 108, 72),
    ("R13.1", 13, 10, 36, 180, 120),
    ("R13.2", 13, 12, 24, 144, 96),
    ("R14.1", 14, 7, 156, 546, 364),
    ("R14.2", 14, 7, 156, 546, 364),
    ("R14.3", 14, 7, 156, 546, 364),
]

REGISTER = {
    7: "Phi6  = one-qutrit readout period (heptad/Fano)",
    8: "2^3   = three-qubit Hilbert space GF(8)",
    9: "q^2   = single-qutrit phase space F3xF3 = AG(2,3) = Hesse 9 pts (4 MUBs)",
    10: "Phi4 = dim Sp(4) = contextual-fraction denominator (1/10)",
    12: "k    = W(3,3) valency / degree",
}


def main():
    out = {}

    # per-n coefficients (cV, cE, cF) = (12, 6n, 4n)/(n-6)
    print("[register atlas]  {3,n}: V=12(g-1)/(n-6), E=6n(g-1)/(n-6), F=4n(g-1)/(n-6)")
    coeffs = {}
    for n in (7, 8, 9, 10, 12):
        cV = 12 // (n - 6)
        cE = 6 * n // (n - 6)
        cF = 4 * n // (n - 6)
        assert 12 % (n - 6) == 0 and 6 * n % (n - 6) == 0 and 4 * n % (n - 6) == 0
        coeffs[n] = (cV, cE, cF)
        print(
            f"  n={n:2d}  (cV,cE,cF) per (g-1) = ({cV:2d},{cE:2d},{cF:2d})   "
            f"register: {REGISTER[n]}"
        )
    assert coeffs == {
        7: (12, 42, 28),
        8: (6, 24, 16),
        9: (4, 18, 12),
        10: (3, 15, 10),
        12: (2, 12, 8),
    }
    out["coefficients_per_g_minus_1"] = {str(n): coeffs[n] for n in coeffs}

    # verify every Table-1 map matches its register's parametrization
    print(f"\n[verify all {len(TABLE1)} maps against the per-n parametrization]")
    for label, g, n, V, E, Fc in TABLE1:
        cV, cE, cF = coeffs[n]
        gm = g - 1
        assert V == cV * gm and E == cE * gm and Fc == cF * gm
        assert V - E + Fc == 2 - 2 * g
    print(f"  all {len(TABLE1)} maps reproduced exactly by V=cV*(g-1) etc.")
    out["maps_verified"] = len(TABLE1)

    # the register identifications
    print(f"\n[register = substrate dimension]")
    assert (7, 8, 9, 10, 12) == (PHI6, 2**3, Q**2, PHI4, K)
    out["registers"] = REGISTER

    # the Hesse n=9 detail: AG(2,3) is the single-qutrit phase space
    print(f"\n[the Hesse rung n=9=q^2]")
    print(f"  the {{3,9}} vertex figure = 9 = q^2 = F3xF3 = AG(2,3) = the 9 Hesse")
    print(
        f"  points (Hessian configuration). R10.1 {{3,9}} g10: V=36=9*4, E=162, F=108."
    )
    assert 9 == Q**2 == 3 * 3
    out["hesse_n9"] = "9 = q^2 = AG(2,3) = Hesse 9 points; R10.1 V=36=9*4"

    print("\nRESULT: the surface atlas is one register stack. Each admissible vertex")
    print("  figure n = 6 + d (d | k=12) is a substrate register dimension, and its")
    print("  {3,n} family is the corresponding tower with V=12(g-1)/(n-6) etc. The")
    print("  five registers are n=7=Phi6 (qutrit), 8=2^3 (qubit), 9=q^2 (single-")
    print("  qutrit phase space AG(2,3)), 10=Phi4 (Sp4 / contextual denom 1/10), and")
    print("  12=k (the degree). All 14 genus-2-14 maps are reproduced exactly by the")
    print("  per-register parametrization, so the genus survey is the substrate's")
    print("  register ladder drawn as surfaces.")

    out["summary"] = (
        "the {3,n} register atlas: each admissible vertex figure n=6+d (d|k=12) is "
        "a substrate register, {3,n} its tower with V=12(g-1)/(n-6), E=6n(g-1)/"
        "(n-6), F=4n(g-1)/(n-6). Per-(g-1) coeffs: n7(12,42,28), n8(6,24,16), "
        "n9(4,18,12), n10(3,15,10), n12(2,12,8). Registers: 7=Phi6 qutrit, 8=2^3 "
        "qubit, 9=q^2 single-qutrit Hesse AG(2,3), 10=Phi4 Sp4/contextual denom, "
        "12=k (9=single-qutrit phase space F3^2). All 14 Table-1 maps reproduced."
    )
    out["sources"] = [
        "Bokowski & H., Symmetry 2025, 17, 622, Table 1 (all 14 maps); {3,n}: "
        "V=12(g-1)/(n-6); registers Phi6/2^3/q^2/Phi4/k; AG(2,3)=Hesse 9 points; "
        "w33_genus_vertex_figure_selection.py, w33_qubit_schlafli_tower_3_8.py, "
        "w33_hurwitz_tower_qubit_crossover.py."
    ]
    with open("data/w33_register_atlas_3n.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_register_atlas_3n.json")


if __name__ == "__main__":
    main()
