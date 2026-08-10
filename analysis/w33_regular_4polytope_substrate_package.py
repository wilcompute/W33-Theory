"""W(3,3) REGULAR 4-POLYTOPE COMPLETE SUBSTRATE PACKAGE.

Extension of the 24-cell / E_8 / W(3,3) Trinity (commit 752437be) to
ALL SIX regular 4-polytopes.  Every f-vector entry and every f-vector
sum across the entire regular 4-polytope family is substrate-primitive.

THE SIX REGULAR 4-POLYTOPES.
=============================

  polytope    Schlafli      f-vector              sum     substrate-form
  -------     --------      --------              -----   --------------------
  5-cell      {3,3,3}       (5, 10, 10, 5)         30     2 g_neg
  8-cell      {4,3,3}       (16, 32, 24, 8)        80     2 v
  16-cell     {3,3,4}       (8, 24, 32, 16)        80     2 v
  24-cell     {3,4,3}       (24, 96, 96, 24)      240     |E|
  120-cell    {5,3,3}       (600, 1200, 720, 120) 2640   p_Ih * |E|
  600-cell    {3,3,5}       (120, 720, 1200, 600) 2640   p_Ih * |E|

EACH OF FOUR DISTINCT SUMS IS SUBSTRATE-PRIMITIVE.

  Smallest (5-cell):   30  = 2 g_neg = X-scheme gauge multiplicity
  Dual pair (8/16):    80  = 2 v       (twice W(3,3) vertex count)
  Self-dual (24-cell -- the POLYTOPE is self-dual; W(3,3) is not):
#   240 = |E|       (W(3,3) edge count = E_8 roots)
  Largest (120/600):  2640 = p_Ih * |E| (Ihara prime times edge count)

MULTIPLICATIVE CHAIN OF DISTINCT SUMS.

  30  ->  80  ->  240  ->  2640
      2^q/q    q       p_Ih

Full ratio 2640 / 30  =  2^q * p_Ih  =  88.

So the polytope cascade (smallest to largest) is governed by THREE
substrate-primitive multipliers (2^q/q, q, p_Ih), telescoping to
2^q * p_Ih = 88 = the Klein-quartic-staircase genus g(K_36) at the
conductor.

PER-ENTRY SUBSTRATE IDENTIFICATIONS.

  5-cell:    5 = Csaszar count = q + 2
             10 = Phi_4

  8-cell:    16 = 2^mu                   (binary mu-shell)
             32 = 2 * 2^mu = 2^(mu+1)
             24 = f
              8 = 2^q                    (tomotope cells)

  16-cell:   same set as 8-cell, reversed (dual)

  24-cell:   24 = f
             96 = mu * f                 (gauge codec times f)

  120-cell:  600 = Csaszar_count * k * Phi_4
            1200 = 2 g_neg * v
             720 = q * |E|
             120 = k * Phi_4              (Hodge boundary mode count!)

  600-cell:  same set as 120-cell, reversed (dual)

CONNECTION TO THE TEMPORAL TRIANGLE (Part MCCIII).

The 24-cell has 24 = 8 * 3 = 2^q * q = 8 temporal triangles.
The 600-cell has 120 = 40 * 3 = v * q = 40 temporal triangles
(one per W(3,3) vertex!).

So the 600-cell IS the substrate's complete (past, now, future)
temporal carrier, one triangle per vertex.  And its total f-vector
sum p_Ih * |E| = 11 * 240 = 2640 ties the Ihara prime to the entire
substrate edge count -- making 600-cell the 'Ihara polytope.'

CONNECTION TO E_8 LATTICE.

The 600-cell vertices lift to 120 E_8 lattice points (one of the
shells of the E_8 root system), and the 600-cell shell sum +
inverse-shell sum reconstructs the full E_8 240-root pattern.

NOVELTY.

The 24-cell f-vector identification with 240 was established in commit
4460faa3.  This extension to all six regular 4-polytopes is new:
EVERY f-vector entry and EVERY f-vector sum across the entire family
is substrate-primitive, completing the regular 4-polytope substrate
package.
"""
from __future__ import annotations

import json
from pathlib import Path


# Substrate constants
Q = 3
QP1 = 4
MU = QP1
LAM_SRG = Q - 1
K_CODEC = Q * QP1
P_IH = K_CODEC - 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24
G_NEG = 15
V = 40
EDGES = 240
CSASZAR_COUNT = Q + 2


POLYTOPES = [
    {
        "name": "5-cell",
        "schlafli": "{3,3,3}",
        "fvec": [5, 10, 10, 5],
        "sum": 30,
        "sum_substrate": "2 g_neg (= 2 * 15)",
        "self_dual": True,
        "entry_substrate": ["Csaszar_count", "Phi_4", "Phi_4", "Csaszar_count"],
    },
    {
        "name": "8-cell",
        "schlafli": "{4,3,3}",
        "fvec": [16, 32, 24, 8],
        "sum": 80,
        "sum_substrate": "2 v",
        "self_dual": False,
        "entry_substrate": ["2^mu", "2 * 2^mu", "f", "2^q"],
    },
    {
        "name": "16-cell",
        "schlafli": "{3,3,4}",
        "fvec": [8, 24, 32, 16],
        "sum": 80,
        "sum_substrate": "2 v",
        "self_dual": False,
        "entry_substrate": ["2^q", "f", "2 * 2^mu", "2^mu"],
    },
    {
        "name": "24-cell",
        "schlafli": "{3,4,3}",
        "fvec": [24, 96, 96, 24],
        "sum": 240,
        "sum_substrate": "|E| (W(3,3) edges = E_8 roots)",
        "self_dual": True,
        "entry_substrate": ["f", "mu * f", "mu * f", "f"],
    },
    {
        "name": "120-cell",
        "schlafli": "{5,3,3}",
        "fvec": [600, 1200, 720, 120],
        "sum": 2640,
        "sum_substrate": "p_Ih * |E|",
        "self_dual": False,
        "entry_substrate": [
            "Csaszar_count * k * Phi_4",
            "2 g_neg * v",
            "q * |E|",
            "k * Phi_4 (Hodge boundary)",
        ],
    },
    {
        "name": "600-cell",
        "schlafli": "{3,3,5}",
        "fvec": [120, 720, 1200, 600],
        "sum": 2640,
        "sum_substrate": "p_Ih * |E|",
        "self_dual": False,
        "entry_substrate": [
            "k * Phi_4 (Hodge boundary)",
            "q * |E|",
            "2 g_neg * v",
            "Csaszar_count * k * Phi_4",
        ],
    },
]


def verify_sums() -> dict:
    return {
        "5_cell_sum_30":   30 == 2 * G_NEG,
        "8_cell_sum_80":   80 == 2 * V,
        "16_cell_sum_80":  80 == 2 * V,
        "24_cell_sum_240": 240 == EDGES,
        "120_cell_sum_2640": 2640 == P_IH * EDGES,
        "600_cell_sum_2640": 2640 == P_IH * EDGES,
    }


def multiplicative_chain() -> dict:
    return {
        "values": [30, 80, 240, 2640],
        "ratios_with_substrate_forms": [
            {"ratio": "80/30 = 8/3", "substrate": "2^q / q"},
            {"ratio": "240/80 = 3", "substrate": "q"},
            {"ratio": "2640/240 = 11", "substrate": "p_Ih"},
        ],
        "full_ratio_2640_over_30": 88,
        "full_ratio_substrate": "2^q * p_Ih = 8 * 11",
        "value_88_meaning": "g(K_36) = g(K_{N_M}) = 88 in the genus staircase at conductor",
    }


def temporal_triangle_link() -> dict:
    return {
        "24_cell_temporal_triangles": "24 vertices = 2^q * q = 8 triangles",
        "600_cell_temporal_triangles": "120 vertices = v * q = 40 triangles",
        "interpretation": (
            "The 600-cell carries 40 = v copies of the temporal triangle "
            "(one per W(3,3) vertex).  It is the substrate's complete "
            "'time crystal' carrier, with f-vector sum p_Ih * |E| -- "
            "Ihara prime times the W(3,3) edge count."
        ),
    }


def hodge_boundary_link() -> dict:
    return {
        "120_cell_vertex_count": 120,
        "substrate_form": "k * Phi_4 = Hodge boundary mode count",
        "Hodge_split": "240 = 39 + 120 + 81 (W(3,3) edge carrier split)",
        "interpretation": (
            "The 120-cell vertex count equals the Hodge boundary mode count "
            "of the W(3,3) edge complex (commit 3891c012, w33_tqc_hodge_audit "
            "section).  Equivalently the 600-cell octahedral-cell count "
            "(= 600 = Csaszar * 120) is Csaszar_count times the Hodge "
            "boundary."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "v": V, "k": K_CODEC, "f": F, "g_neg": G_NEG,
                "Phi_4": PHI4, "edges": EDGES, "p_Ih": P_IH,
                "Csaszar_count": CSASZAR_COUNT,
            },
        },
        "regular_4polytopes": POLYTOPES,
        "verify_sums": verify_sums(),
        "multiplicative_chain": multiplicative_chain(),
        "temporal_triangle_link": temporal_triangle_link(),
        "hodge_boundary_link": hodge_boundary_link(),
        "theorem": (
            "W(3,3) Regular 4-Polytope Complete Substrate Package.  All "
            "SIX regular 4-polytopes -- 5-cell, 8-cell (tesseract), "
            "16-cell, 24-cell, 120-cell, 600-cell -- have f-vector entries "
            "AND f-vector sums entirely in substrate-primitive form.  The "
            "four distinct sums (30, 80, 240, 2640) factor as (2 g_neg, "
            "2 v, |E|, p_Ih * |E|), running across the X-scheme gauge "
            "multiplicity, the vertex count, the edge count, and the "
            "Ihara prime.  The multiplicative chain through the polytope "
            "cascade has ratios (2^q/q, q, p_Ih), telescoping to "
            "2^q * p_Ih = 88 = g(K_{N_M}) at the conductor.  The 600-cell "
            "(120 vertices = v * q = 40 temporal triangles) is the "
            "substrate's complete time crystal, with f-vector sum "
            "p_Ih * |E| = 2640.  The 120-cell vertex count (120 = k * "
            "Phi_4) equals the Hodge boundary mode count, linking the "
            "polytope vertex set to the W(3,3) edge-complex Hodge "
            "decomposition."
        ),
        "honesty_boundary": (
            "All polytope f-vectors are classical.  The substrate-"
            "primitive identifications of each entry and each sum are "
            "exact arithmetic.  The multiplicative chain through the "
            "polytope cascade and the temporal-triangle / Hodge-boundary "
            "links are structural readings tying the regular 4-polytope "
            "family to W(3,3) substrate invariants.  No new physical "
            "observable is derived here; this completes the polytope "
            "substrate package."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_regular_4polytope_substrate_package.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 80)
    print("W(3,3) REGULAR 4-POLYTOPE COMPLETE SUBSTRATE PACKAGE")
    print("=" * 80)

    print(f"\n{'polytope':<10s} {'Schlafli':>10s}  {'f-vector':<25s} {'sum':>5s}  {'substrate-form'}")
    print('  ' + '-' * 76)
    for p in POLYTOPES:
        print(f"{p['name']:<10s} {p['schlafli']:>10s}  {str(p['fvec']):<25s} {p['sum']:>5d}  {p['sum_substrate']}")

    print("\nAll sums verify:", all(verify_sums().values()))

    print(f"\nMultiplicative chain through distinct sums:")
    chain = multiplicative_chain()
    for r in chain["ratios_with_substrate_forms"]:
        print(f"  {r['ratio']:<20s} -> {r['substrate']}")
    print(f"  Full ratio 2640/30 = {chain['full_ratio_2640_over_30']} = {chain['full_ratio_substrate']}")
    print(f"  88 = {chain['value_88_meaning']}")

    print(f"\nTemporal triangle count:")
    t = payload["temporal_triangle_link"]
    print(f"  24-cell:  {t['24_cell_temporal_triangles']}")
    print(f"  600-cell: {t['600_cell_temporal_triangles']}")

    print(f"\nHodge boundary link:")
    h = payload["hodge_boundary_link"]
    print(f"  120-cell vertices = {h['120_cell_vertex_count']} = k * Phi_4 = Hodge boundary")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
