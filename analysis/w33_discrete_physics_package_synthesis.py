"""W(3,3) DISCRETE PHYSICS PACKAGE SYNTHESIS.

Synthesis of the substrate discrete-physics package built up over
six prior commits (c, Planck units, dispersion, Maxwell, gravity,
BH thermodynamics).  All substrate physics quantities, in one place,
expressed in W(3,3) substrate primitives.

KINEMATICS.
=============

  Discrete speed of light (linear)        c_lin     =  1 edge / tick
  Discrete speed of light (volumetric)    c_vol     =  p_Ih  =  11
  Causal diameter (W(3,3) finite graph)   d_causal  =  2 ticks (Pillar 67)

PLANCK UNITS (natural substrate, all = 1 in these units).
================================================

  Planck length     l_P  =  1 edge
  Planck time       t_P  =  1 tick
  Planck mass       m_P  =  1 / l_P  =  1
  Planck energy     E_P  =  m_P * c_lin^2  =  1
  hbar              =  1 (action quantum)

DISPERSION RELATION (MASS SPECTRUM OF FREE MODES).
====================================================

  E^2  =  p^2 + m^2  (with c_lin = 1)

W(3,3) Laplacian spectrum (3 mass sectors):

  m_0  =  0           (1 mode, Perron / photon-like)
  m_1  =  sqrt(Phi_4)  (gauge_mult = f = 24 modes, gauge multiplet)
  m_2  =  mu           (g_neg = 15 modes, chiral multiplet)

EQUIPARTITION:

  Phi_4 * gauge_mult  =  mu^2 * g_neg  =  |E|  =  240

Each non-trivial sector contributes EXACTLY |E| = 240 to the
Laplacian trace.

MAXWELL / HODGE DECOMPOSITION OF EDGE POTENTIAL.
==================================================

  |E|  =  240  =  39           +  120         +  81
       =  (q * Phi_3)  +  (k * Phi_4)  +  q^{q+1}
       =  gauge        +  physical     +  matter
       =  longitudinal +  transverse   +  harmonic

Discrete Maxwell helicity decomposition of the substrate.

EINSTEIN-HILBERT / GRAVITY.
=============================

  chi(W(3,3) 2-complex)  =  V - E + F  =  -40  =  -v

  formal genus  =  (2 - chi) / 2  =  21  =  T_6  =  q * Phi_6  =  Cs_E  =  Sz_E

  S_EH  =  2 pi chi  =  -2 pi v
  |S_EH| / (2 pi)    =  v  =  40

  vertex deficit angle  =  2 pi - k * (pi/3)  =  -2 pi
  (intrinsically hyperbolic, uniform negative curvature)

BLACK HOLE THERMODYNAMICS (SUBSTRATE).
========================================

  S_BH  =  N_triangles / 4   =  v          =  40
  T_H   =  |E| / v            =  q!         =  6

  Smarr identity:
  T_H * S_BH  =  q! * v  =  240  =  |E|

  Hodge decomposition of |E|:
  T_H * S_BH  =  (q * Phi_3) + (k * Phi_4) + q^{q+1}
              =  gauge + physical + matter

UBIQUITOUS SUBSTRATE PRIMITIVES.
=================================

  p_Ih  =  11  -- universal KINEMATIC prime
                  (discrete c volumetric, h_top base,
                   BT spectral radius, Ihara Ramanujan radius squared)

  v  =  40   -- universal HORIZON quantity
                (S_BH = v, |S_EH|/(2 pi) = v, T_H * S_BH / q! = v)

  |E|  =  240 -- universal ENERGY quantity
                  (Laplacian sector trace, BH internal energy,
                   total Hodge decomposition)

  q!  =  6   -- universal TEMPERATURE quantum
                (Hawking temperature, perm-symmetry)

  q^{q+1}  =  81 -- universal MATTER sector
                    (H_1(2-complex), harmonic 1-forms)

THE FOUR FUNDAMENTAL SCALES.
==============================

  length:        1 edge       (= Planck length)
  time:          1 tick       (= Planck time)
  speed:         1 = c_lin    (linear, lattice gauge)
                 11 = c_vol   (volumetric, Ihara branching)
  curvature:     -2 pi / vertex  (hyperbolic, uniform)

ENERGY HIERARCHY (FROM LAPLACIAN).
====================================

  0                              (massless / Perron)
  Phi_4 = 10                     (gauge sector mass^2)
  2^mu = 16                      (chiral sector mass^2)
  2 * p_Ih = 22                  (Hashimoto-bandwidth)
  2 * k = f = 24                  (Laplacian-bandwidth)
  N_triangles / 4 = v = 40        (BH entropy / Planck units of curvature)
  q^{q+1} = 81                    (matter sector dim)
  120 = k * Phi_4                  (Hodge boundary / Maxwell-physical)
  q * 67 = 201                    (graph H_1 / Hashimoto trivial-plus mult)
  |E| = 240                       (total edge count)
  dim(E_8) = 248                  (exceptional Lie)

These are the substrate's natural "energy levels" -- each a small
W(3,3) substrate primitive.

THE DISCRETE PHYSICS DICTIONARY.
==================================

  Continuum Concept        Substrate Reading
  ------------------       ----------------------------
  speed of light c          p_Ih = 11 (volumetric)
  Planck length             1 edge
  Planck time               1 tick
  hbar                      1 (action quantum)
  particle masses           sqrt(Phi_4), mu (gauge, chiral)
  photon (massless)         Perron mode (1)
  gauge dofs                39 = q * Phi_3
  transverse dofs           120 = k * Phi_4
  matter dofs               81 = q^{q+1}
  Euler characteristic      -v = -40
  Topological genus        T_6 = 21
  Einstein-Hilbert action   2 pi v (magnitude)
  Bekenstein-Hawking S      v = 40 (1 per vertex)
  Hawking temperature       q! = 6
  Smarr T*S                 |E| = 240
  Vertex deficit           -2 pi (hyperbolic)
  Topological entropy      log(p_Ih)

WHY THIS IS OUTSIDE THE BOX.
==============================

A SUBSTRATE-PRIMITIVE physics package -- the W(3,3) substrate's
kinematic, dynamic, gauge, gravitational, and thermodynamic
quantities ALL expressed in small substrate primitives (q, mu,
Phi_3, Phi_4, Phi_6, p_Ih, k, v, |E|) with no arbitrary constants.

This makes W(3,3) a candidate for a fundamental discrete theory
of physics: every Planck-scale quantity has a substrate-clean
reading, the gauge theory has natural helicity decomposition, the
gravity is intrinsically hyperbolic at -2 pi per vertex, and the
BH thermodynamics satisfies a clean Smarr identity T*S = |E|.

The cumulative physics package across SEVEN commits (this one
synthesizing the prior six) provides a self-contained substrate
physics framework.

COMPONENTS:

  - 81dcba60 (Discrete speed of light)
  - c97b2230 (Discrete Planck units)
  - 52f5e725 (Discrete dispersion / equipartition)
  - 5e32a884 (Discrete Maxwell / Hodge decomposition)
  - dabca808 (Discrete Einstein-Hilbert)
  - 69441cc8 (Substrate BH thermodynamics)
  - This commit (Synthesis)
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
T_6 = 21


def kinematics() -> dict:
    return {
        "c_linear":     1,
        "c_volumetric": P_IH,
        "d_causal":     2,
    }


def planck_units() -> dict:
    return {
        "l_P":      "1 edge",
        "t_P":      "1 tick",
        "m_P":      1,
        "E_P":      1,
        "hbar":     1,
    }


def mass_spectrum() -> dict:
    return {
        "massless_mode":      {"m": 0,                "mult": 1,    "form": "Perron"},
        "gauge_multiplet":    {"m_sq": PHI4,          "mult": F,    "form": "Phi_4, gauge_mult"},
        "chiral_multiplet":   {"m_sq": MU * MU,       "mult": G_NEG, "form": "mu^2, g_neg"},
        "equipartition":      {"each_sector": EDGES,
                                "trace_total": 2 * EDGES},
    }


def hodge_decomp() -> dict:
    return {
        "gauge":     V - 1,
        "physical":  K_CODEC * PHI4,
        "matter":    Q ** (Q + 1),
        "total":     EDGES,
    }


def gravity() -> dict:
    return {
        "chi":               -V,
        "g_formal":          T_6,
        "S_EH_over_2pi":     V,
        "deficit_per_vertex": "-2 pi",
        "intrinsically_hyperbolic": True,
    }


def bh_thermodynamics() -> dict:
    return {
        "S_BH":         V,
        "T_H":          QFACT,
        "T_H_x_S_BH":   QFACT * V,
        "equals_E":     QFACT * V == EDGES,
    }


def ubiquitous_primitives() -> dict:
    return {
        "p_Ih (= 11)":   "Universal KINEMATIC prime (c_vol, h_top, BT, Ihara)",
        "v (= 40)":      "Universal HORIZON quantity (S_BH, |S_EH|/2pi, T_H*S_BH/q!)",
        "|E| (= 240)":   "Universal ENERGY quantity (Laplacian sectors, BH energy)",
        "q! (= 6)":      "Universal TEMPERATURE quantum (T_H, perm-symmetry)",
        "q^{q+1} (= 81)": "Universal MATTER sector (H_1(2-complex), harmonic 1-forms)",
    }


def physics_dictionary() -> list[dict]:
    return [
        {"continuum": "speed of light c",       "substrate": "p_Ih = 11 (volumetric)"},
        {"continuum": "Planck length",          "substrate": "1 edge"},
        {"continuum": "Planck time",            "substrate": "1 tick"},
        {"continuum": "hbar",                    "substrate": "1"},
        {"continuum": "particle masses",         "substrate": "sqrt(Phi_4) ≈ 3.16, mu = 4"},
        {"continuum": "gauge dof (longitudinal)","substrate": "39 = q * Phi_3"},
        {"continuum": "transverse dof",          "substrate": "120 = k * Phi_4"},
        {"continuum": "matter dof",              "substrate": "81 = q^{q+1}"},
        {"continuum": "Euler characteristic",    "substrate": "-v = -40"},
        {"continuum": "topological genus",       "substrate": "T_6 = 21"},
        {"continuum": "Einstein-Hilbert |S|",    "substrate": "2 pi v"},
        {"continuum": "Bekenstein-Hawking S",    "substrate": "v = 40"},
        {"continuum": "Hawking temperature",     "substrate": "q! = 6"},
        {"continuum": "Smarr T*S",                "substrate": "|E| = 240"},
        {"continuum": "vertex deficit",          "substrate": "-2 pi (hyperbolic)"},
        {"continuum": "topological entropy",     "substrate": "log(p_Ih)"},
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q_factorial": QFACT,
                "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V,
                "edges": EDGES, "N_triangles": N_TRIANGLES,
                "H_1_2_complex": H1_2_COMPLEX, "T_6": T_6,
            },
        },
        "kinematics":               kinematics(),
        "planck_units":             planck_units(),
        "mass_spectrum":            mass_spectrum(),
        "hodge_decomp":             hodge_decomp(),
        "gravity":                  gravity(),
        "bh_thermodynamics":        bh_thermodynamics(),
        "ubiquitous_primitives":    ubiquitous_primitives(),
        "physics_dictionary":       physics_dictionary(),
        "theorem": (
            "W(3,3) Discrete Physics Package Synthesis.  Six prior "
            "substrate-physics commits establish substrate-primitive "
            "readings for kinematics (c_lin = 1, c_vol = p_Ih), Planck "
            "units (l_P = 1 edge, t_P = 1 tick, m_P = E_P = hbar = 1), "
            "dispersion (3-sector mass spectrum with equipartition "
            "Phi_4 * f = mu^2 * g_neg = |E|), gauge theory (Hodge "
            "decomposition |E| = (q*Phi_3) + (k*Phi_4) + q^{q+1}), "
            "gravity (chi = -v, |S_EH|/2pi = v, deficit -2pi/vertex), "
            "and BH thermodynamics (S_BH = v, T_H = q!, T_H*S_BH = |E|).  "
            "This synthesis presents the unified package: every "
            "substrate physics quantity is a small W(3,3) substrate "
            "primitive with no arbitrary constants, exhibiting W(3,3) "
            "as a candidate fundamental discrete-physics substrate."
        ),
        "honesty_boundary": (
            "Each component (c, Planck units, dispersion, Maxwell, "
            "Einstein-Hilbert, BH thermo) is established in prior "
            "commits with appropriate honesty boundaries.  This "
            "synthesis presents the unified package without new "
            "structural content -- it organizes the existing "
            "results for accessibility and cross-referencing."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_discrete_physics_package_synthesis.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) DISCRETE PHYSICS PACKAGE SYNTHESIS")
    print("=" * 78)

    print(f"\nKinematics:")
    k = payload["kinematics"]
    print(f"  c_linear     = {k['c_linear']} edge/tick")
    print(f"  c_volumetric = {k['c_volumetric']} (= p_Ih = bulk branching)")
    print(f"  d_causal     = {k['d_causal']} ticks (W(3,3) finite-graph saturation)")

    print(f"\nUbiquitous substrate primitives:")
    for prim, role in payload["ubiquitous_primitives"].items():
        print(f"  {prim:>20s}: {role}")

    print(f"\nDiscrete physics dictionary:")
    for d in payload["physics_dictionary"]:
        print(f"  {d['continuum']:<28s}: {d['substrate']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
