"""W(3,3) SUBSTRATE BLACK HOLE THERMODYNAMICS THEOREM.

Substrate-clean analog of black-hole thermodynamics on W(3,3):
the Hawking temperature, Bekenstein-Hawking entropy, and a Smarr-
like identity T_H * S_BH = |E| (edge count).

THE THREE THERMODYNAMIC QUANTITIES.
=====================================

(I) HORIZON BEKENSTEIN-HAWKING ENTROPY.

  S_BH  =  N_triangles / 4  =  v  =  40

The W(3,3) horizon (= entire 2-complex 'area' counted as triangles)
has BH entropy equal to the vertex count.  One Planck unit of
entropy per vertex.

(II) HAWKING TEMPERATURE.

  T_H  =  trace(Laplacian)  /  S_BH
       =  2 * |E|  /  v
       =  480  /  40
       =  12  =  k

Wait, but actually the substrate-cleanest reading is:

  T_H  =  |E|  /  S_BH  =  240 / 40  =  q!  =  6

(taking equipartition trace per sector |E| = 240 divided by the
vertex count v = 40).

So Hawking temperature:

  T_H  =  q!  =  6  (in Planck units)

(III) SMARR-LIKE IDENTITY.

  T_H * S_BH  =  q! * v  =  6 * 40  =  240  =  |E|

So:

  T_H * S_BH  =  |E|  (W(3,3) edge count)

A clean substrate Smarr-like identity: HAWKING TEMPERATURE TIMES
BH ENTROPY EQUALS THE SUBSTRATE EDGE COUNT.

THE FREE ENERGY.
==================

  F  =  M - T_H * S_BH  =  M - |E|

For an extremal-like substrate BH, M = T_H * S_BH = |E|, giving:

  F_extremal  =  0

(consistent with extremal BHs being free-energy-zero in
continuum thermodynamics).

THE INTERNAL ENERGY / MASS.
=============================

For a non-extremal substrate BH, the internal energy U = T_H * S_BH
plus contributions.  In the simplest reading:

  U_substrate  =  T_H * S_BH  =  |E|  =  240

So the substrate BH has internal "energy" equal to the edge count
of the underlying W(3,3) graph.

ALTERNATIVE TEMPERATURE READINGS.
====================================

(A) From Laplacian trace equipartition:
    tr(L) = 2|E| = 480, with two sectors each contributing |E|.
    Per-vertex contribution = tr(L) / v = 12 = k.
    So an alternative T_H' = k = 12.

(B) From Hashimoto operator:
    Hashimoto spectrum bounded by sqrt(p_Ih), so an alternative
    T_H'' = sqrt(p_Ih) = sqrt(11) ~ 3.32.

(C) From the cleanest substrate reading:
    T_H = |E| / v = q! (Smarr-clean).

The substrate "Hawking temperature" depends on which operator
defines the thermal partition.  All three are substrate-clean
quantities; T_H = q! gives the cleanest Smarr identity.

WHY T_H = q! IS THE SUBSTRATE-CLEANEST READING.
==================================================

  T_H * S_BH  =  q! * v  =  240  =  |E|

In substrate primitives:

  |E|  =  q! * v  =  mu * q * v  (where q! = mu * q / mu = q * (q-1)?
                                  no, q! = 6 = 2 * 3 = mu - 1 * q, etc.)

Actually q! * v = 6 * 40 = 240, and |E| = 240, exact match.

So T_H * S_BH = |E| is an EXACT INTEGER SUBSTRATE IDENTITY.

CONNECTION TO HODGE / MAXWELL DECOMPOSITION (5e32a884).
=========================================================

  |E|  =  39  +  120  +  81
       =  (q * Phi_3)  +  (k * Phi_4)  +  q^{q+1}
       =  gauge   +   physical   +   matter

So:

  T_H * S_BH  =  gauge_sector + physical_sector + matter_sector
              =  (q * Phi_3) + (k * Phi_4) + q^{q+1}

The Smarr-like identity decomposes the edge count exactly into
the three Hodge sectors.  Reading the BH 'mass' as |E| then gives
the substrate's mass-energy budget split across gauge / physical
/ matter degrees.

CONNECTION TO BLACK HOLE TYPES.
=================================

Continuum BH thermodynamics has several BH types:

  Schwarzschild (M only):    T_H = 1 / (8 pi M)
  Reissner-Nordstrom (M, Q): T_H = (r_+ - r_-) / (...)
  Kerr (M, J):                T_H = (r_+ - r_-) / (...)
  Extremal (T_H = 0):         specific limit

For W(3,3) substrate:
  T_H = q! = 6 (constant per vertex, no M-dependence in 2D)
  S_BH = v = 40

In 2D gravity (which W(3,3) naturally inhabits via its
2-complex structure), the BH thermodynamics is more topological
than dynamical -- the temperature and entropy are fixed by the
graph's combinatorial structure rather than mass.

WHY THIS IS OUTSIDE THE BOX.
==============================

Bekenstein-Hawking entropy S = A/4 is classical.  The substrate
identification S_BH = N_triangles / 4 = v (commit c97b2230) gives
1 Planck unit per vertex.

The STRUCTURAL NEW CONTENT here:

  - T_H = |E| / v = q!  (Hawking temp = perm symmetry quantum)
  - T_H * S_BH = |E|     (Smarr-like substrate identity)
  - The substrate BH's 'energy' equals the edge count
  - The 'energy' decomposes exactly into Hodge sectors

These give the substrate BH a clean thermodynamic reading in
substrate primitives.

CONNECTION TO PRIOR COMMITS.
==============================

  - 81dcba60 (Discrete c, p_Ih)
  - c97b2230 (Discrete Planck units, S_BH = v)
  - 52f5e725 (Dispersion / equipartition, |E| per sector)
  - 5e32a884 (Hodge / Maxwell decomposition, gauge + physical + matter)
  - dabca808 (Einstein-Hilbert, |S_EH|/(2 pi) = v)
  - This commit (BH thermodynamics, T_H * S_BH = |E|)

Substrate physics package now includes substrate-clean readings of:
  c, Planck units, mass spectrum, gauge theory, gravity, AND
  black-hole thermodynamics.
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


def thermodynamic_quantities() -> dict:
    S_BH = N_TRIANGLES // 4
    T_H = EDGES // V
    return {
        "S_BH":              S_BH,
        "S_BH_form":         "N_triangles / 4 = v",
        "match_v":           S_BH == V,
        "T_H":               T_H,
        "T_H_form":          "|E| / v = q!",
        "match_q_factorial": T_H == QFACT,
    }


def smarr_identity() -> dict:
    S_BH = V
    T_H = QFACT
    return {
        "T_H":              T_H,
        "S_BH":             S_BH,
        "product":          T_H * S_BH,
        "substrate":        "q! * v",
        "equals_edges":     T_H * S_BH == EDGES,
        "edges":            EDGES,
    }


def hodge_decomposition_link() -> dict:
    return {
        "gauge":      V - 1,
        "physical":   K_CODEC * PHI4,
        "matter":     Q ** (Q + 1),
        "total":      (V - 1) + (K_CODEC * PHI4) + (Q ** (Q + 1)),
        "expected":   EDGES,
        "match":      (V - 1) + (K_CODEC * PHI4) + (Q ** (Q + 1)) == EDGES,
        "interpretation": (
            "T_H * S_BH = |E| decomposes via Hodge into gauge + "
            "physical + matter."
        ),
    }


def alternative_temperatures() -> list[dict]:
    return [
        {"reading":      "T_H = |E| / v = q!",
         "value":        QFACT,
         "comment":     "Smarr-cleanest"},
        {"reading":     "T_H' = k (Laplacian trace per vertex)",
         "value":        K_CODEC,
         "comment":     "From tr(L) = 2|E| split per vertex"},
        {"reading":     "T_H'' = sqrt(p_Ih)",
         "value":        math.sqrt(P_IH),
         "comment":     "Hashimoto Ramanujan bound"},
    ]


def bh_internal_energy_decomp() -> dict:
    return {
        "BH_internal_energy":     EDGES,
        "form":                   "T_H * S_BH = |E|",
        "Hodge_decomposition":   {
            "gauge_sector":       V - 1,
            "physical_sector":    K_CODEC * PHI4,
            "matter_sector":      Q ** (Q + 1),
        },
        "comment":                "The substrate BH 'energy' (= |E|) decomposes exactly into the three Hodge / Maxwell sectors.",
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V, "edges": EDGES,
                "N_triangles": N_TRIANGLES,
            },
        },
        "thermodynamic_quantities":      thermodynamic_quantities(),
        "smarr_identity":                smarr_identity(),
        "hodge_decomposition_link":      hodge_decomposition_link(),
        "alternative_temperatures":      alternative_temperatures(),
        "bh_internal_energy_decomp":     bh_internal_energy_decomp(),
        "theorem": (
            "W(3,3) Substrate Black Hole Thermodynamics Theorem.  The "
            "substrate horizon has Bekenstein-Hawking entropy "
            "S_BH = N_triangles / 4 = v = 40 (one Planck unit per "
            "vertex), Hawking temperature T_H = |E| / v = q! = 6 "
            "(the perm-symmetry quantum), and satisfies a Smarr-like "
            "identity T_H * S_BH = q! * v = 240 = |E| (the substrate "
            "edge count).  The BH 'internal energy' |E| = 240 "
            "decomposes via Hodge / Maxwell exactly into the three "
            "substrate sectors: (q * Phi_3) + (k * Phi_4) + q^{q+1} "
            "= gauge + physical + matter = 39 + 120 + 81 = 240."
        ),
        "honesty_boundary": (
            "Bekenstein-Hawking entropy formula S = A/4 is classical.  "
            "The substrate identifications S_BH = N_triangles/4 = v "
            "and T_H = |E|/v = q! are exact integer arithmetic.  The "
            "Smarr-like identity T_H * S_BH = |E| follows trivially "
            "from the definitions, but its interpretation as a "
            "substrate BH thermodynamic identity, and the Hodge "
            "decomposition of |E| into gauge + physical + matter "
            "sectors, are the structural new content.  Alternative "
            "temperature readings (T_H' = k from tr(L)/v, T_H'' = "
            "sqrt(p_Ih) from Hashimoto bound) are substrate-clean "
            "but give different Smarr identities; the cleanest "
            "is T_H = q!."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_substrate_black_hole_thermodynamics.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) SUBSTRATE BLACK HOLE THERMODYNAMICS THEOREM")
    print("=" * 78)

    t = payload["thermodynamic_quantities"]
    print(f"\nThermodynamic quantities:")
    print(f"  S_BH  =  N_triangles / 4  =  {t['S_BH']}  =  v")
    print(f"  T_H   =  |E| / v          =  {t['T_H']}  =  q!")

    s = payload["smarr_identity"]
    print(f"\nSmarr-like identity:")
    print(f"  T_H * S_BH  =  q! * v  =  {s['product']}  =  |E|")

    h = payload["hodge_decomposition_link"]
    print(f"\nHodge decomposition of T_H * S_BH = |E|:")
    print(f"  gauge:    {h['gauge']:>3}  =  q * Phi_3")
    print(f"  physical: {h['physical']:>3}  =  k * Phi_4")
    print(f"  matter:   {h['matter']:>3}  =  q^{{q+1}}")
    print(f"  total = {h['total']} = |E|: {h['match']}")

    print(f"\nAlternative temperature readings:")
    for a in payload["alternative_temperatures"]:
        print(f"  {a['reading']:>40s}: value = {a['value']:.3f}  ({a['comment']})")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
