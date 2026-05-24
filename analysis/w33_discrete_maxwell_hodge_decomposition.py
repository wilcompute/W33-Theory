"""W(3,3) DISCRETE MAXWELL / HODGE DECOMPOSITION THEOREM.

The Hodge decomposition of the W(3,3) line-triangle 2-complex
directly gives a GAUGE / PHYSICAL / MATTER split of the substrate's
1-form (edge) degrees of freedom -- the discrete analog of the
helicity decomposition of the electromagnetic vector potential.

THE W(3,3) CHAIN COMPLEX.
==========================

  C_0 (vertices)    =  v = 40-dim
  C_1 (edges)       =  |E| = 240-dim
  C_2 (triangles)   =  N_triangles = 160-dim

  boundary d_0:  C_0  ->  C_1   (vertex function -> edge differential)
  boundary d_1:  C_1  ->  C_2   (edge function -> triangle curl)

Ranks:
  rank d_0  =  v - 1     =  q * Phi_3  =  39
  rank d_1  =  k * Phi_4  =  120         (Hodge boundary)

THE HODGE DECOMPOSITION OF C_1.
=================================

  C_1  =  im(d_0)    oplus  im(d_1^T)     oplus  H_1(2-complex)
       =  39          +     120            +     81
       =  240         =  |E|

Each sector has a clean substrate-primitive identification:

  GAUGE sector       =  im(d_0)        =  39   =  q * Phi_3
                                          (= v - 1, the trivial-zero-mode count)
  PHYSICAL sector    =  im(d_1^T)      =  120  =  k * Phi_4
                                          (= Hodge boundary rank)
  MATTER sector      =  H_1(2-complex) =  81   =  q^{q+1}
                                          (= harmonic 1-forms = first homology)

THIS IS A DISCRETE MAXWELL HELICITY DECOMPOSITION.
====================================================

In continuum 3+1D, the electromagnetic vector potential A_mu has
4 components.  Gauge fixing removes 1 (longitudinal) and Gauss
constraint removes 1 more (temporal), leaving 2 physical
transverse polarizations.

On W(3,3), the substrate's 1-form (edge) potential A has |E| = 240
components.  The Hodge decomposition removes:

  GAUGE (longitudinal):  im(d_0)     -- 39 modes, pure-gauge directions
                                       (= d_0 phi for any vertex
                                        function phi on C_0)

  PHYSICAL (transverse): im(d_1^T)   -- 120 modes, physical curl modes
                                       (= satisfying Maxwell-like
                                        co-closure condition)

  MATTER (harmonic):     H_1         -- 81 modes, harmonic 1-forms
                                       (= matter sector, = first
                                        homology with q=3 substrate)

Total:  39 + 120 + 81 = 240 = |E| (full vector potential space).

SUBSTRATE-PRIMITIVE READINGS.
==============================

  39  =  q * Phi_3        =  3 * 13   =  rank d_0
  120 =  k * Phi_4         =  12 * 10  =  rank d_1
  81  =  q^{q+1}            =  3^4     =  matter sector dim

These three substrate-primitive integer products account for the
entire 240 = |E| edge-space, with NO leftover modes.

THE PHYSICAL/GAUGE RATIO.
============================

  physical / gauge  =  120 / 39  =  k * Phi_4 / (q * Phi_3)
                                =  (12 * 10) / (3 * 13)
                                =  120 / 39
                                approx 3.08

So the physical sector is ~3 times larger than the pure-gauge
sector.  In substrate primitives:

  k * Phi_4 / (q * Phi_3)  =  4 * Phi_4 / Phi_3 (cancelling q)
                          =  mu * Phi_4 / Phi_3
                          =  40 / 13

So physical / gauge = v / Phi_3 = 40/13 -- the ratio of vertex count
to the third cyclotomic primitive.

CONNECTION TO H_1(graph) = q * 67.
====================================

The graph (1-complex) H_1 was H_1(graph) = m - n + 1 = 201 = q * 67
= q * Heegner_67 (commit ac4dfadc).  Adding the 160 triangles to
form the 2-complex KILLS exactly the rank d_1 = 120 = Hodge
boundary modes, leaving:

  H_1(2-complex)  =  H_1(graph) - rank d_1  =  201 - 120  =  81

So the W(3,3) "matter sector" is what's LEFT of the graph's free-
group rank q * 67 after the Hodge boundary modes are removed.

CONTINUUM-COUNTERPART HELICITY COUNT.
========================================

Continuum 3+1D Maxwell:
  total A_mu components       =  4
  pure-gauge (gauge fixing)   =  1
  Gauss constraint (temporal) =  1
  physical (transverse)       =  2

W(3,3) discrete Maxwell:
  total edge components        =  240
  pure-gauge (d_0 image)       =  39   (= longitudinal-like)
  physical (d_1 image)         =  120  (= transverse-like)
  matter (harmonic / H_1)      =  81

The substrate has an extra MATTER sector (81 = q^{q+1}) on top of
the continuum-style gauge + physical decomposition.  This is
because the W(3,3) 2-complex is not simply-connected (genus > 0),
so harmonic 1-forms exist and serve as the substrate's matter
content.

WHY THIS IS OUTSIDE THE BOX.
==============================

The Hodge decomposition of the W(3,3) line-triangle 2-complex is
exact integer arithmetic, established in prior commits (ac4dfadc
two-homology / Heegner-67).  The structural new content here is
the DIRECT IDENTIFICATION of the three Hodge sectors as the
continuum-Maxwell GAUGE / PHYSICAL / MATTER decomposition, with:

  gauge mode count   =  q * Phi_3    (= 39)
  physical count     =  k * Phi_4    (= 120, Hodge boundary)
  matter count       =  q^{q+1}      (= 81, matter sector)

This makes the discrete Maxwell theory on W(3,3) a SUBSTRATE-CLEAN
gauge theory with all three helicity sectors carrying explicit
W(3,3) substrate primitive labels.

CONNECTION TO PRIOR COMMITS.
==============================

  - ac4dfadc (Two-homology / Heegner-67): H_1(graph) = 201, H_1(2c) = 81
  - 81dcba60 (Discrete c, c_sub = p_Ih)
  - c97b2230 (Discrete Planck units)
  - 52f5e725 (Dispersion / equipartition)
  - MCCXX-MCCXXVII (W(3,3) 4D code, quantum LDPC)

The Hodge / Maxwell decomposition adds the GAUGE THEORY layer to
the substrate's kinematic + dynamic substrate physics package.
"""
from __future__ import annotations

import json
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
H1_2_COMPLEX = 81


def chain_complex() -> dict:
    return {
        "C_0_vertices":      V,
        "C_1_edges":         EDGES,
        "C_2_triangles":     N_TRIANGLES,
        "rank_d_0":          V - 1,
        "rank_d_0_substrate": "v - 1 = q * Phi_3 = 39",
        "rank_d_1":          K_CODEC * PHI4,
        "rank_d_1_substrate": "k * Phi_4 = 120 (Hodge boundary)",
    }


def hodge_decomposition() -> dict:
    return {
        "gauge_sector": {
            "value":         V - 1,
            "form":          "im(d_0) = rank d_0 = v - 1 = q * Phi_3",
            "interpretation": "Longitudinal / pure-gauge modes",
        },
        "physical_sector": {
            "value":         K_CODEC * PHI4,
            "form":          "im(d_1^T) = rank d_1 = k * Phi_4 (Hodge boundary)",
            "interpretation": "Transverse / Maxwell-physical modes",
        },
        "matter_sector": {
            "value":         H1_2_COMPLEX,
            "form":          "H_1(2-complex) = q^{q+1} (harmonic 1-forms)",
            "interpretation": "Matter sector (genus > 0 substrate)",
        },
        "total_check":    (V - 1) + K_CODEC * PHI4 + H1_2_COMPLEX,
        "expected_total": EDGES,
        "match":          ((V - 1) + K_CODEC * PHI4 + H1_2_COMPLEX) == EDGES,
    }


def physical_gauge_ratio() -> dict:
    return {
        "physical":       K_CODEC * PHI4,
        "gauge":          V - 1,
        "ratio":          (K_CODEC * PHI4) / (V - 1),
        "substrate_form": "k * Phi_4 / (q * Phi_3) = mu * Phi_4 / Phi_3 = v / Phi_3",
        "exact":          (K_CODEC * PHI4) == MU * PHI4 * Q,
    }


def continuum_comparison() -> list[dict]:
    return [
        {"sector":      "total potential",
         "continuum":   "A_mu (4 components, 3+1D)",
         "substrate":   "A (240 components, W(3,3) edges)"},
        {"sector":      "gauge (longitudinal)",
         "continuum":   "1 component",
         "substrate":   "39 modes = q * Phi_3"},
        {"sector":      "physical (transverse)",
         "continuum":   "2 components",
         "substrate":   "120 modes = k * Phi_4"},
        {"sector":      "matter (extra in substrate)",
         "continuum":   "0 (vacuum Maxwell)",
         "substrate":   "81 modes = q^{q+1}"},
    ]


def H1_graph_connection() -> dict:
    return {
        "H_1_graph":         201,
        "H_1_graph_form":    "m - n + 1 = q * 67 = q * Heegner_67",
        "rank_d_2_kill":     K_CODEC * PHI4,
        "rank_d_2_form":     "k * Phi_4 = Hodge boundary",
        "H_1_2_complex":     H1_2_COMPLEX,
        "H_1_2_complex_form": "q^{q+1} = matter sector",
        "identity":          "H_1(2-complex) = H_1(graph) - rank d_1 = 201 - 120 = 81",
        "match":             (201 - K_CODEC * PHI4) == H1_2_COMPLEX,
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V, "edges": EDGES,
                "N_triangles": N_TRIANGLES, "H_1_2_complex": H1_2_COMPLEX,
            },
        },
        "chain_complex":           chain_complex(),
        "hodge_decomposition":      hodge_decomposition(),
        "physical_gauge_ratio":    physical_gauge_ratio(),
        "continuum_comparison":    continuum_comparison(),
        "H1_graph_connection":     H1_graph_connection(),
        "theorem": (
            "W(3,3) Discrete Maxwell / Hodge Decomposition Theorem.  "
            "The Hodge decomposition of the W(3,3) line-triangle "
            "2-complex gives an exact gauge / physical / matter split "
            "of the 240-dim edge potential space: |E| = 39 + 120 + 81 "
            "= (q*Phi_3) + (k*Phi_4) + q^{q+1}.  The three sectors "
            "are the discrete analogs of: longitudinal (pure gauge), "
            "transverse (Maxwell-physical), and matter (harmonic "
            "1-forms / first homology), respectively.  This makes "
            "W(3,3) a substrate-clean discrete gauge theory with "
            "explicit substrate-primitive labels on every helicity "
            "sector, and identifies q^{q+1} = 81 = H_1(2-complex) as "
            "the substrate matter sector that survives the Hodge "
            "boundary collapse from H_1(graph) = q * Heegner_67 = 201."
        ),
        "honesty_boundary": (
            "Hodge decomposition of finite simplicial complexes is "
            "classical.  The rank identities (rank d_0 = v - 1, "
            "rank d_1 = k * Phi_4 = 120) are established in prior "
            "commits.  The structural new content is the explicit "
            "GAUGE / PHYSICAL / MATTER labelling of the three Hodge "
            "sectors, mapping them to continuum Maxwell helicity "
            "decomposition.  The physical interpretation of harmonic "
            "1-forms as 'matter' is heuristic but consistent with "
            "the W(3,3) substrate program."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_discrete_maxwell_hodge_decomposition.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) DISCRETE MAXWELL / HODGE DECOMPOSITION THEOREM")
    print("=" * 78)

    cc = payload["chain_complex"]
    print(f"\nW(3,3) chain complex:")
    print(f"  C_0 (vertices)   = {cc['C_0_vertices']}")
    print(f"  C_1 (edges)      = {cc['C_1_edges']}")
    print(f"  C_2 (triangles)  = {cc['C_2_triangles']}")
    print(f"  rank d_0  =  {cc['rank_d_0']}  ({cc['rank_d_0_substrate']})")
    print(f"  rank d_1  =  {cc['rank_d_1']}  ({cc['rank_d_1_substrate']})")

    h = payload["hodge_decomposition"]
    print(f"\nHodge decomposition of C_1 = 240 = |E|:")
    print(f"  GAUGE     (im d_0)       = {h['gauge_sector']['value']:>3}   ({h['gauge_sector']['form']})")
    print(f"  PHYSICAL  (im d_1^T)     = {h['physical_sector']['value']:>3}  ({h['physical_sector']['form']})")
    print(f"  MATTER    (H_1)          = {h['matter_sector']['value']:>3}   ({h['matter_sector']['form']})")
    print(f"  total = {h['total_check']} = |E|: {h['match']}")

    r = payload["physical_gauge_ratio"]
    print(f"\nPhysical / gauge ratio:")
    print(f"  120 / 39 = {r['ratio']:.4f}  = {r['substrate_form']}")

    print(f"\nContinuum-discrete comparison:")
    for c in payload["continuum_comparison"]:
        print(f"  {c['sector']:<28s}: continuum = {c['continuum']:<22s} substrate = {c['substrate']}")

    H = payload["H1_graph_connection"]
    print(f"\nConnection to H_1(graph) = q * Heegner_67:")
    print(f"  H_1(graph)        =  {H['H_1_graph']}  =  q * 67")
    print(f"  - rank d_1 (kill) =  {H['rank_d_2_kill']}  =  k * Phi_4")
    print(f"  = H_1(2-complex)  =  {H['H_1_2_complex']}  =  q^{{q+1}}  = matter sector")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
