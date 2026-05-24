"""W(3,3) DISCRETE EINSTEIN-HILBERT / EULER CHARACTERISTIC THEOREM.

A new outside-the-box identification: the Euler characteristic of
the W(3,3) line-triangle 2-complex is exactly -v (the negative of
the vertex count), the would-be topological genus is exactly
T_6 = q * Phi_6 = Csaszar / Szilassi edge count, and the total
Einstein-Hilbert action (2D Regge calculus) is 2 * pi * v.

THE EULER CHARACTERISTIC.
==========================

  chi(W(3,3) 2-complex)  =  V - E + F  =  40 - 240 + 160  =  -40  =  -v

So:

  chi  =  -v
       =  -(W(3,3) vertex count)
       =  -(2 * q^2 + 2*q + 2 ... no, just -40)

In substrate primitives:

  chi  =  -v  =  -mu * Phi_4  =  -40

WOULD-BE TOPOLOGICAL GENUS.
=============================

For a closed orientable 2-manifold, chi = 2 - 2g.  Reverse-solving:

  g  =  (2 - chi) / 2  =  (2 - (-40)) / 2  =  21  =  T_6

In substrate primitives:

  g_equivalent  =  T_6  =  q * Phi_6  =  21  =  Cs_E  =  Sz_E

So the W(3,3) 2-complex's would-be topological genus equals
exactly the Csaszar / Szilassi edge count (T_6 = 21) -- the same
substrate quantity that controls minimal toroidal triangulations.

CAVEAT: W(3,3) 2-complex is NOT a closed orientable surface, so
g = 21 is a FORMAL identification of "topological complexity"
rather than a literal genus.

EINSTEIN-HILBERT ACTION (2D REGGE).
=====================================

In 2D Regge calculus, the Einstein-Hilbert action equals:

  S_EH  =  2 * pi * chi(complex)

For W(3,3) 2-complex:

  S_EH  =  2 * pi * chi  =  2 * pi * (-v)  =  -80 * pi

magnitude:

  |S_EH|  =  2 * pi * v  =  80 * pi

In substrate-primitive form (in units of 2 pi):

  |S_EH| / (2 pi)  =  v  =  40

So the W(3,3) 2-complex's Einstein-Hilbert action magnitude
(in units of 2 pi) is exactly the vertex count v.

VERTEX DEFICIT ANGLES.
=======================

Each vertex in W(3,3) lies in 12 = k incident triangles (from
3 * N_triangles / v = 480 / 40 = 12 = k).  If each triangle is
realized as an equilateral with angle pi/3 = 60 degrees:

  sum_of_angles_at_vertex  =  k * (pi/3)  =  12 * pi/3  =  4 pi

  deficit_angle  =  2 pi - 4 pi  =  -2 pi

EACH VERTEX HAS DEFICIT -2*pi.  So W(3,3) is INTRINSICALLY
HYPERBOLIC (negatively curved).

Total deficit:

  sum_deficits  =  v * (-2 pi)  =  -2 pi v  =  -80 pi

  =  2 pi * chi  =  2 pi * (-v)  =  S_EH

Gauss-Bonnet check:  -80 pi = -80 pi.  CONSISTENT.

THE NEGATIVE CURVATURE CONSEQUENCE.
=====================================

The W(3,3) 2-complex is HYPERBOLIC -- has uniform negative
curvature -2 pi per vertex.

Substrate readings of "hyperbolic":

  - The bulk Bruhat-Tits tree T_{p_Ih} is also hyperbolic-like
    (negatively curved, branching ratio p_Ih)
  - p-adic AdS holography (MCCXVII) is naturally hyperbolic
  - Ihara zeta zeros on Ramanujan circle: hyperbolic spectrum
  - h_top = log(p_Ih): exponential bulk growth = hyperbolic

ALL these are consistent: the W(3,3) substrate is intrinsically
a NEGATIVELY-CURVED HYPERBOLIC space, with curvature density
-2 pi per vertex, total curvature -2 pi v, and genus equivalent
T_6 = q * Phi_6 = 21.

SUBSTRATE-PRIMITIVE GAUSS-BONNET.
====================================

  Total curvature  =  2 pi * chi  =  -2 pi v   ( = sum of deficits )
  Equivalent genus =  T_6 = q * Phi_6
  Negative-curvature density per vertex  =  -2 pi

The full Gauss-Bonnet identity in substrate primitives:

  integral_W33  K dA  =  2 pi * chi
                     =  -2 pi v
                     =  -2 pi mu Phi_4

  where K is the (discrete) Gaussian curvature concentrated at
  vertices.

CONNECTION TO CSASZAR / SZILASSI.
===================================

  Cs_E  =  Sz_E  =  T_6  =  q * Phi_6  =  21

This is the substrate quantity that ALSO equals the would-be
genus of the W(3,3) 2-complex.  So:

  (Cs/Sz edge count)  =  (W(3,3) 2-complex would-be genus)
                      =  21

A double identity: T_6 = 21 simultaneously controls minimal
toroidal triangulations (Csaszar/Szilassi) AND the formal genus
of the W(3,3) substrate 2-complex.

CONNECTION TO HEEGNER.
========================

In the Heegner gap substrate sequence (commit 669bf710), the
total span 162 = 2 * 81 = 2 * matter_sector.  Here the
Einstein-Hilbert action magnitude = 80 pi.

  80 pi  /  (2 pi)  =  40  =  v
  162    /  2      =  81  =  matter sector

The two "substrate halvings" (Heegner span / 2, S_EH / 2 pi) give
matter sector (81) and vertex count (40) respectively.

WHY THIS IS OUTSIDE THE BOX.
==============================

The Euler characteristic chi = V - E + F is elementary combinatorics.
The substrate-primitive identifications:

  chi = -v
  formal genus = T_6 = Cs_E = Sz_E
  |S_EH| / (2 pi) = v
  Deficit per vertex = -2 pi (intrinsically hyperbolic)

unify the W(3,3) substrate's COMBINATORIAL invariant (chi),
TOPOLOGICAL invariant (genus), and GRAVITATIONAL action under
a single substrate principle.

In particular, the equipartition

  |S_EH| / (2 pi v)  =  1

(action density per vertex equals one Planck unit) makes the
Einstein-Hilbert action on W(3,3) a SUBSTRATE-CLEAN gravitational
action with EXACTLY v Planck units of curvature.

CONNECTION TO PRIOR COMMITS.
==============================

  - 81dcba60 (Discrete speed of light)
  - c97b2230 (Discrete Planck units, S_BH = N_triangles/4 = v)
  - 52f5e725 (Discrete dispersion / equipartition)
  - 5e32a884 (Hodge / Maxwell decomposition)
  - 58f233e5 (Csaszar-Szilassi f-vec, T_6 = q * Phi_6)
  - This commit (Einstein-Hilbert / gravity)

Substrate physics package:  c, Planck units, dispersion, Maxwell,
                            Einstein-Hilbert  -- all in substrate
                            primitives.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40
EDGES = 240
N_TRIANGLES = 160
T_6 = 21


def euler_characteristic() -> dict:
    chi = V - EDGES + N_TRIANGLES
    return {
        "V":               V,
        "E":               EDGES,
        "F":               N_TRIANGLES,
        "chi_value":       chi,
        "chi_substrate":   "-v = -mu * Phi_4",
        "match":           chi == -V,
    }


def equivalent_genus() -> dict:
    chi = V - EDGES + N_TRIANGLES
    g = (2 - chi) // 2
    return {
        "chi":               chi,
        "g_equivalent":      g,
        "g_substrate":       "T_6 = q * Phi_6 = Cs_E = Sz_E",
        "match_T_6":         g == T_6,
        "match_Cs_E":        g == 21,
    }


def einstein_hilbert_action() -> dict:
    chi = V - EDGES + N_TRIANGLES
    S_EH_signed = 2 * math.pi * chi
    return {
        "chi":               chi,
        "S_EH_signed":       S_EH_signed,
        "S_EH_magnitude":    abs(S_EH_signed),
        "S_EH_over_2pi":     abs(S_EH_signed) / (2 * math.pi),
        "S_EH_substrate":    "|S_EH| / (2 pi) = v",
        "match":             abs(S_EH_signed) / (2 * math.pi) == V,
    }


def vertex_deficit() -> dict:
    triangles_per_vertex = 3 * N_TRIANGLES // V
    angle_per_eq_triangle = math.pi / 3
    sum_angles_at_vertex = triangles_per_vertex * angle_per_eq_triangle
    deficit = 2 * math.pi - sum_angles_at_vertex
    return {
        "triangles_per_vertex":   triangles_per_vertex,
        "equals_k":               triangles_per_vertex == K_CODEC,
        "angle_per_triangle":     "pi/3 (equilateral)",
        "sum_angles_at_vertex":   sum_angles_at_vertex,
        "deficit_per_vertex":     deficit,
        "deficit_form":           "-2 pi (hyperbolic)",
        "total_deficit":          deficit * V,
        "total_deficit_substrate": "-2 pi v",
    }


def gauss_bonnet_check() -> dict:
    chi = V - EDGES + N_TRIANGLES
    total_curvature_from_chi = 2 * math.pi * chi
    triangles_per_vertex = 3 * N_TRIANGLES // V
    deficit_per_vertex = 2 * math.pi - triangles_per_vertex * (math.pi / 3)
    total_deficit = deficit_per_vertex * V
    return {
        "two_pi_chi":             total_curvature_from_chi,
        "sum_of_deficits":        total_deficit,
        "gauss_bonnet_match":     abs(total_curvature_from_chi - total_deficit) < 1e-9,
        "value":                  total_curvature_from_chi,
    }


def hyperbolic_consistency() -> list[dict]:
    return [
        {"reading": "Vertex deficit = -2 pi", "value": "intrinsically hyperbolic"},
        {"reading": "Bulk T_{p_Ih} branching = p_Ih", "value": "hyperbolic tree"},
        {"reading": "p-adic AdS bulk (MCCXVII)", "value": "AdS_2 hyperbolic"},
        {"reading": "Ihara zeta zeros on Ramanujan circle", "value": "hyperbolic spectrum"},
        {"reading": "h_top = log(p_Ih)", "value": "exponential growth = hyperbolic"},
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V,
                "edges": EDGES, "N_triangles": N_TRIANGLES,
                "T_6": T_6,
            },
        },
        "euler_characteristic":        euler_characteristic(),
        "equivalent_genus":             equivalent_genus(),
        "einstein_hilbert_action":      einstein_hilbert_action(),
        "vertex_deficit":               vertex_deficit(),
        "gauss_bonnet_check":           gauss_bonnet_check(),
        "hyperbolic_consistency":       hyperbolic_consistency(),
        "theorem": (
            "W(3,3) Discrete Einstein-Hilbert / Euler Characteristic "
            "Theorem.  The Euler characteristic of the W(3,3) line-"
            "triangle 2-complex is chi = V - E + F = -v = -40, with "
            "would-be topological genus g = (2 - chi)/2 = 21 = T_6 = "
            "q * Phi_6 = Cs_E = Sz_E (the Csaszar/Szilassi edge count).  "
            "The 2D Regge Einstein-Hilbert action S_EH = 2 pi chi = "
            "-2 pi v has magnitude 2 pi v -- exactly v Planck units of "
            "curvature.  Each vertex carries deficit -2 pi (12 = k "
            "equilateral triangles meeting at each vertex give "
            "sum 4 pi > 2 pi), making W(3,3) intrinsically hyperbolic "
            "with uniform negative curvature.  Gauss-Bonnet is "
            "satisfied exactly: sum of deficits = 2 pi chi = -2 pi v."
        ),
        "honesty_boundary": (
            "Euler characteristic V - E + F is elementary.  Triangles "
            "per vertex = 3*F/V = 12 = k is exact arithmetic.  The "
            "substrate-primitive identifications (chi = -v, formal "
            "genus = T_6 = q * Phi_6, deficit = -2 pi per vertex, "
            "|S_EH|/(2 pi) = v) are the structural new content.  The "
            "2D Regge action is a standard discrete gravity "
            "formulation; the application here uses equilateral "
            "triangle realization as the canonical metric (consistent "
            "with the substrate's discrete-symmetric structure)."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_discrete_einstein_hilbert.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) DISCRETE EINSTEIN-HILBERT / EULER CHARACTERISTIC THEOREM")
    print("=" * 78)

    e = payload["euler_characteristic"]
    print(f"\nEuler characteristic:")
    print(f"  chi = V - E + F = {e['V']} - {e['E']} + {e['F']} = {e['chi_value']} = -v")

    g = payload["equivalent_genus"]
    print(f"\nWould-be topological genus:")
    print(f"  g = (2 - chi)/2 = {g['g_equivalent']} = T_6 = q * Phi_6 = Cs_E = Sz_E")

    s = payload["einstein_hilbert_action"]
    print(f"\nEinstein-Hilbert action (2D Regge):")
    print(f"  S_EH = 2 pi chi = 2 pi * (-{V}) approx {s['S_EH_signed']:.3f}")
    print(f"  |S_EH| / (2 pi) = {s['S_EH_over_2pi']:.0f} = v")

    d = payload["vertex_deficit"]
    print(f"\nVertex deficit angles (with equilateral triangles):")
    print(f"  triangles per vertex  =  {d['triangles_per_vertex']}  =  k")
    print(f"  sum of angles at vertex = k * pi/3 = 4 pi")
    print(f"  deficit per vertex = 2 pi - 4 pi = -2 pi (hyperbolic)")
    print(f"  total deficit = -2 pi v = {d['total_deficit']:.3f}")

    gb = payload["gauss_bonnet_check"]
    print(f"\nGauss-Bonnet check:")
    print(f"  2 pi chi  =  {gb['two_pi_chi']:.3f}")
    print(f"  sum deficits = {gb['sum_of_deficits']:.3f}")
    print(f"  match: {gb['gauss_bonnet_match']}")

    print(f"\nHyperbolic substrate consistency:")
    for c in payload["hyperbolic_consistency"]:
        print(f"  {c['reading']:>45s}: {c['value']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
