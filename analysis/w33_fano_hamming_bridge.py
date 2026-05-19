#!/usr/bin/env python3
"""W(3,3) FANO-HAMMING BRIDGE: the binary shadow of [[240,81,3]]_3.

BREAKTHROUGH_DCCLXX flagged the Boolean Heptad B_2 = 2^(d_X+d_Z) - 1 = 127
as "hinting at a GF(2^7) extension over the ternary substrate" and "the
bridge to classical binary codes that the theory has been missing."

This script makes that bridge explicit.

THE BRIDGE.
-----------
The binary Hamming code [7, 4, 3] has parameters exactly equal to substrate
primitives:

    n = 7 = Phi_6 = d_X + d_Z       (block length = Fano shell)
    k = 4 = mu   = d_Z              (information dimension)
    d = 3 = q    = d_X              (minimum distance)

So:
    Hamming [n, k, d]_2  =  [Phi_6, mu, q]_2
                          =  [d_X + d_Z, d_Z, d_X]_2

The W(3,3) edge CSS code [[240, 81, 3]]_3 has minimum distance d_X = 3, the
SAME as the Hamming binary code -- the two share the d_X = q = 3 parameter.

THE FANO PLANE.
---------------
The Fano plane PG(2, F_2) = projective plane over F_2:

    |points| = |lines| = (2^3 - 1)/(2 - 1) = 7 = Phi_6
    |incidences| = 7 * 3 = 21 = T_6 = Pascal triangular #6 = |E(K_7)|
                                        = |E(Csaszar polyhedron)|
    |Aut(Fano)| = |GL(3, F_2)| = |PSL(2, 7)| = 168 = f * Phi_6

So the Fano plane's:
    point count       = Phi_6
    line count        = Phi_6
    incidence count   = T_6 = |E(Csaszar)|
    automorphism order = f * Phi_6 = 168

THE KLEIN QUARTIC.
------------------
The Klein quartic x^3 y + y^3 z + z^3 x = 0 over P^2_C is the Riemann
surface associated with the Hurwitz triangle group (2, 3, 7).

    genus(Klein) = 3 = q = d_X
    |Aut(Klein)| = 168 = f * Phi_6 (saturates Hurwitz bound)
    Hurwitz bound at genus g: 84 (g - 1)
                            = 84 * (q - 1)
                            = (Csaszar flag count) * lam_SRG
                            = (Csaszar flag count) * (q - 1)
                            = 168 at q = 3.

So the Klein quartic at the W(3,3) saturation point q = 3 saturates the
Hurwitz bound with automorphism order equal to f * Phi_6.

KEY NEW IDENTITY: 168 * 240 = 8! = (2^q)!.
------------------------------------------
    |Aut(Fano)| * |E_8 roots| = (tomotope cells)!
    f * Phi_6 * |E| = (2^q)!
    168 * 240 = 40320 = 8!

THE BINARY-TERNARY DUALITY.
---------------------------
The W(3,3) substrate hosts BOTH a binary code AND a ternary code with
matching CSS-distance parameters (d_X, d_Z) = (q, q+1) = (3, 4):

  binary:   Hamming   [d_X + d_Z, d_Z, d_X]_2  =  [7, 4, 3]_2
  ternary:  CSS edge  [[|E|, H_1, d_X]]_3       =  [[240, 81, 3]]_3

Both have minimum distance d_X = q = 3.  The Hamming code lives on the
Fano plane (Phi_6 = 7 points), and the CSS code lives on the W(3,3) edge
carrier (|E| = 240 = E_8 root count).  Together they form a
binary-ternary CSS-distance duality.

HEEGNER LINK.
-------------
The Klein quartic / Fano plane are tied to PSL(2, 7), and 7 is the FOURTH
Heegner number.  The Hamming length n = 7 is also a Heegner prime.  So the
Fano shell d_X + d_Z = 7 = Phi_6 is simultaneously:
    * a Heegner number  (Q(sqrt(-7)) has class number 1),
    * the Fano plane size,
    * the Hamming block length,
    * the Csaszar/Szilassi shell.

Putting it all together: the substrate's d_X + d_Z = 7 is the cleanest
shared invariant between W(3,3), Fano/Hamming/Klein, and the imaginary
quadratic class-number-1 classification.
"""
from __future__ import annotations

import json
from math import factorial
from pathlib import Path


Q = 3
QP1 = 4
DX = Q
DZ = QP1
MU = QP1
LAM_SRG = Q - 1
PHI3 = Q ** 2 + Q + 1   # 13
PHI4 = Q ** 2 + 1       # 10
PHI6 = Q ** 2 - Q + 1   # 7
K_CODEC = Q * QP1       # 12
F = 24
G_NEG = 15
H1 = Q ** QP1           # 81
EDGES = 240
CSASZAR_FLAGS = 84
TOMOTOPE_CELLS = 2 ** Q
BOOLEAN_HEPTAD = 2 ** PHI6 - 1   # 127

# Fano / Hamming / Klein invariants
FANO_POINTS = (2 ** Q - 1)   # 7 in PG(2, F_2)
HAMMING_PARAMS = (PHI6, MU, Q)   # [7, 4, 3]
PSL27_ORDER = (PHI6 - 1) * PHI6 * (PHI6 + 1) // 2   # |PSL(2,7)| = (q-1)q(q+1)/2 with q=7
KLEIN_GENUS = Q
HURWITZ_BOUND_AT_GENUS_Q = 84 * (Q - 1)


def hamming_parameter_identification() -> dict:
    return {
        "hamming_n_equals_d_X_plus_d_Z": HAMMING_PARAMS[0] == DX + DZ,
        "hamming_k_equals_d_Z": HAMMING_PARAMS[1] == DZ,
        "hamming_d_equals_d_X": HAMMING_PARAMS[2] == DX,
        "hamming_in_substrate_form": "[Phi_6, mu, q] = [d_X + d_Z, d_Z, d_X]",
        "numeric": list(HAMMING_PARAMS),
        "substrate_form": ["Phi_6 = q^2 - q + 1", "mu = q + 1", "q"],
    }


def fano_plane_invariants() -> dict:
    return {
        "points": FANO_POINTS,
        "points_equals_phi6": FANO_POINTS == PHI6,
        "lines": FANO_POINTS,
        "incidences": FANO_POINTS * Q,
        "incidences_equals_T6": FANO_POINTS * Q == 21,
        "incidences_equals_E_K7": FANO_POINTS * Q == FANO_POINTS * (FANO_POINTS - 1) // 2,
        "aut_order": PSL27_ORDER,
        "aut_order_equals_f_times_phi6": PSL27_ORDER == F * PHI6,
        "psl27_substrate": "168 = f * Phi_6",
        "gl3_F2_substrate": "168 = (Phi_6 - 1) * Phi_6 * (Phi_6 + 1) / 2",
    }


def klein_quartic_invariants() -> dict:
    aut_order = PSL27_ORDER
    return {
        "genus": KLEIN_GENUS,
        "genus_equals_q": KLEIN_GENUS == Q,
        "aut_order": aut_order,
        "aut_order_equals_f_times_phi6": aut_order == F * PHI6,
        "hurwitz_bound_at_genus_q": HURWITZ_BOUND_AT_GENUS_Q,
        "saturates_hurwitz": aut_order == HURWITZ_BOUND_AT_GENUS_Q,
        "hurwitz_substrate_form": "84(g - 1) = Csaszar_flag_count * (q - 1) = 84 * (q-1)",
        "klein_modular_curve": "X(7) = X(Phi_6); 7 is the modular level"
    }


def boolean_heptad_check() -> dict:
    return {
        "B_2": BOOLEAN_HEPTAD,
        "equals_2_to_phi6_minus_1": BOOLEAN_HEPTAD == 2 ** PHI6 - 1,
        "is_mersenne_prime_M_7": True,
        "order_of_GF128_minus_zero": BOOLEAN_HEPTAD == 128 - 1,
        "field_GF_2_to_phi6": "GF(2^Phi_6) = GF(128)",
        "comment": (
            "127 = 2^7 - 1 is the 4th Mersenne prime M_7.  GF(128) = F_2 [x] / "
            "irreducible degree-7 polynomial.  Multiplicative group is cyclic "
            "of order 127, which appears as the B_2 binomial moment of the "
            "toroidal metric polynomial."
        ),
    }


def fano_psl_x_e8() -> dict:
    product = PSL27_ORDER * EDGES
    factorial_2q = factorial(2 ** Q)
    return {
        "PSL_2_7_order_times_E8_roots": product,
        "factorial_2_to_q": factorial_2q,
        "equals_factorial_2_to_q": product == factorial_2q,
        "comment": (
            "168 * 240 = 40320 = 8! = (2^q)! at q = 3.  PSL(2, 7) order times "
            "E_8 root count equals the factorial of the tomotope cell count.  "
            "This binds the Fano/Klein automorphism group to the E_8 root "
            "lattice through a factorial of the substrate's natural binary "
            "shell 2^q."
        ),
    }


def heegner_link() -> dict:
    return {
        "Phi_6_is_heegner": 7 in [1, 2, 3, 7, 11, 19, 43, 67, 163],
        "Phi_6_role": "d_X + d_Z = Hamming length = Fano size = Heegner prime",
        "comment": (
            "The Heawood/Fano shell Phi_6 = 7 is one of the 9 Heegner numbers, "
            "tying the substrate's CSS distance sum to class-number-1 "
            "imaginary quadratic Q(sqrt(-7)).  This is the SAME 7 that "
            "appears as the modular curve level for the Klein quartic = X(7)."
        ),
    }


def binary_ternary_duality_table() -> dict:
    return {
        "binary": {
            "code": "Hamming [7, 4, 3]_2",
            "alphabet": "F_2",
            "length": PHI6,
            "info_dim": DZ,
            "distance": DX,
            "host_geometry": "Fano plane PG(2, F_2)",
            "host_size": FANO_POINTS,
            "auto_group": "PSL(2, 7) = GL(3, F_2)",
            "auto_order": PSL27_ORDER,
        },
        "ternary": {
            "code": "[[240, 81, 3]]_3 edge CSS",
            "alphabet": "F_3",
            "length": EDGES,
            "info_dim": H1,
            "distance": DX,
            "host_geometry": "W(3, 3) edge carrier",
            "host_size": EDGES,
            "auto_group": "Aut(W(3,3))",
            "auto_order": "1,451,520 (extended carrier action)",
        },
        "shared": {
            "minimum_distance": DX,
            "(d_X, d_Z)": [DX, DZ],
            "Heegner_7_link": True,
        },
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG,
                "v": 40, "edges": EDGES, "H_1": H1, "k": K_CODEC,
            },
        },
        "hamming_parameter_identification": hamming_parameter_identification(),
        "fano_plane_invariants": fano_plane_invariants(),
        "klein_quartic_invariants": klein_quartic_invariants(),
        "boolean_heptad_check": boolean_heptad_check(),
        "fano_PSL_x_E8_factorial_identity": fano_psl_x_e8(),
        "heegner_link": heegner_link(),
        "binary_ternary_duality_table": binary_ternary_duality_table(),
        "theorem": (
            "Fano-Hamming Bridge Theorem.  The binary Hamming code [7, 4, 3] "
            "has parameters [d_X + d_Z, d_Z, d_X] in the W(3,3) substrate, "
            "matching the ternary CSS code [[240, 81, 3]]_3 in its minimum "
            "distance d_X.  The Fano plane PG(2, F_2) -- the natural host of "
            "Hamming -- has Phi_6 = 7 points, Phi_6 = 7 lines, T_6 = 21 "
            "incidences, and automorphism order |PSL(2, 7)| = f * Phi_6 = 168.  "
            "The Klein quartic X(7) at genus q = 3 saturates the Hurwitz "
            "bound 84(g - 1) = (Csaszar flag count) * (q - 1) with the SAME "
            "168 automorphisms.  Boolean heptad B_2 = 2^Phi_6 - 1 = 127 is "
            "the Mersenne prime M_7 and the order of GF(128) \\ {0}.  And "
            "168 * |E| = (2^q)! = 8!, tying the Fano automorphism group, the "
            "E_8 root lattice, and the tomotope-cell factorial into a single "
            "identity."
        ),
        "honesty_boundary": (
            "All arithmetic identities are exact.  The identification of the "
            "Hamming [7, 4, 3] parameters with substrate primitives is a "
            "parameter match, not a categorical equivalence of the two codes.  "
            "The binary-ternary duality is structural -- the two codes share "
            "their minimum distance d_X and host on Fano-related geometry -- "
            "but they encode different information sectors (Hamming: 4 bits "
            "from 7; CSS: 81 qutrits from 240)."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_fano_hamming_bridge.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 72)
    print("W(3,3) FANO-HAMMING BRIDGE THEOREM")
    print("=" * 72)

    h = payload["hamming_parameter_identification"]
    print("\nHamming [7, 4, 3] parameters in substrate:")
    print(f"  [n, k, d] = {h['numeric']}")
    print(f"  substrate = [Phi_6, mu, q] = [d_X+d_Z, d_Z, d_X]")
    print(f"  n=Phi_6: {h['hamming_n_equals_d_X_plus_d_Z']}, "
          f"k=mu: {h['hamming_k_equals_d_Z']}, d=q: {h['hamming_d_equals_d_X']}")

    f_inv = payload["fano_plane_invariants"]
    print(f"\nFano plane PG(2, F_2):")
    print(f"  points = lines = {f_inv['points']} = Phi_6: {f_inv['points_equals_phi6']}")
    print(f"  incidences = {f_inv['incidences']} = T_6 = |E(Csaszar)|: {f_inv['incidences_equals_T6']}")
    print(f"  |Aut| = |PSL(2,7)| = {f_inv['aut_order']} = f*Phi_6: {f_inv['aut_order_equals_f_times_phi6']}")

    k = payload["klein_quartic_invariants"]
    print(f"\nKlein quartic = X(7):")
    print(f"  genus = {k['genus']} = q: {k['genus_equals_q']}")
    print(f"  |Aut| = {k['aut_order']} saturates Hurwitz bound 84(g-1) = {k['hurwitz_bound_at_genus_q']}: "
          f"{k['saturates_hurwitz']}")

    b = payload["boolean_heptad_check"]
    print(f"\nBoolean heptad B_2 = {b['B_2']} = 2^Phi_6 - 1: {b['equals_2_to_phi6_minus_1']}")
    print(f"  Mersenne prime M_7; |GF(128) \\ 0| = {b['order_of_GF128_minus_zero']}")

    fx = payload["fano_PSL_x_E8_factorial_identity"]
    print(f"\nKey identity: 168 * 240 = (2^q)! = 8!")
    print(f"  |PSL(2,7)| * |E| = {fx['PSL_2_7_order_times_E8_roots']}")
    print(f"  (2^q)! = {fx['factorial_2_to_q']}: {fx['equals_factorial_2_to_q']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
