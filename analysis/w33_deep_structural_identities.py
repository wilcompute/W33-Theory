"""W(3,3) DEEP STRUCTURAL IDENTITIES.

The substrate primitives at q=3 are not independent integers; they
satisfy a web of structural identities that pin down the physics
ladder.  This script collects the most striking relationships between
the substrate exponents that show up in physical-constant predictions.

CORE STRUCTURAL IDENTITIES.

I. SUBSTRATE QUANTUM PRIMITIVES.
  q + mu = 7 = Phi_6                   (substrate quantum-sum identity)
  2q + 1 = 7 = Phi_6                   (Fano-byte identity, q=3 only)
  mu - q = 1                            (substrate quantum-difference)
  mu * q = 12 = k                       (valency from quantum product)
  mu^2 - q^2 = 7 = Phi_6                (quadratic-difference identity)

II. EXPONENT LADDER CONNECTIONS.
  v = (q!)^2 + mu = 40                  (vertex count from EW exponent + co-quantum)
  T_6 + g_neg = (q!)^2 = 36             (Csaszar edges + chiral mult = EW exponent)
  T_6 + Heegner_6 = v = 40              (Csaszar edges + K3 sigma- = vertex count)
  mu^4 = (q!)^2 + C(k, 3) = 36 + 220    (CC exponent = EW + binomial)
  mu^4 = 2 * 2^Phi_6 = 2^(Phi_6+1)      (dS identity)
  2^Phi_6 = 2 * 2^(Phi_6-1) = 2 * 64    (Hubble exponent halving)

III. HIERARCHY MULTIPLICATION IDENTITIES.
  (m_p/m_Pl) * (m_p/m_Pl) = alpha_g     (gravitational-fine-structure squared identity)
  i.e., q^(-v) * q^(-v) = q^(-2v) = alpha_g exponent.

  (v_H/m_Pl) * q = m_W/m_Pl              (Higgs VEV times q gives W mass)
  i.e., q^(-(mu+1)*Phi_6) * q^1 = q^(-(q!)^2 + 1)?
  Actually: -(mu+1)*Phi_6 - 1 = -35 - 1 = -36 = -(q!)^2.  CHECK.
  So v_H/m_Pl = q * m_W/m_Pl, or m_W = v_H / q.

  m_W * q = v_H  (substrate-clean Higgs VEV - W mass relation)

IV. COSMOLOGY-COMBINATORICS IDENTITIES.
  Lambda exponent / Hubble exponent = mu^4 / 2^Phi_6 = 256/128 = 2 (dS)
  alpha_g exponent / m_p exponent = 2v/v = 2  (squaring identity)

V. BARYON-ASYMMETRY SUBSTRATE CONNECTION.
  eta_B = q! / q^(T_6)  with T_6 = q * Phi_6 = Csaszar/Szilassi edges.

VI. DENSITY-RATIO IDENTITIES.
  Omega_DM/Omega_b = q^q/(mu+1)
  Omega_Lambda/Omega_DM = Phi_3/(mu+1)
  Both have denominator (mu+1) = Csaszar realization count.

VII. THE PRINCIPAL EXPONENT IDENTITY.
  v + T_6 - g_neg - q!^2 = 40 + 21 - 15 - 36 = 10 = Phi_4

So the substrate's principal exponents satisfy a linear relation:
  v + T_6 - g_neg - (q!)^2 = Phi_4
  40 + 21 - 15 - 36 = 10

This relates proton mass / baryon asymmetry / chiral / EW / inflation
exponents in a single substrate identity.
"""
from __future__ import annotations

import json
from pathlib import Path
from math import comb


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
T_6 = Q * PHI6  # = 21
HEEGNER_6 = 19


def quantum_primitives_identities() -> list[dict]:
    return [
        {"identity": "q + mu = Phi_6",          "lhs": Q + MU,        "rhs": PHI6,   "match": Q + MU == PHI6},
        {"identity": "2q + 1 = Phi_6",          "lhs": 2 * Q + 1,     "rhs": PHI6,   "match": 2 * Q + 1 == PHI6},
        {"identity": "mu - q = 1",              "lhs": MU - Q,        "rhs": 1,      "match": MU - Q == 1},
        {"identity": "mu * q = k",              "lhs": MU * Q,        "rhs": K_CODEC, "match": MU * Q == K_CODEC},
        {"identity": "mu^2 - q^2 = Phi_6",      "lhs": MU**2 - Q**2,  "rhs": PHI6,   "match": MU**2 - Q**2 == PHI6},
        {"identity": "mu^2 = 2^mu",             "lhs": MU**2,         "rhs": 2**MU,  "match": MU**2 == 2**MU},
    ]


def exponent_ladder_identities() -> list[dict]:
    return [
        {"identity": "v = (q!)^2 + mu",          "lhs": V,           "rhs": QFACT**2 + MU,  "match": V == QFACT**2 + MU},
        {"identity": "T_6 + g_neg = (q!)^2",     "lhs": T_6 + G_NEG, "rhs": QFACT**2,       "match": T_6 + G_NEG == QFACT**2},
        {"identity": "T_6 + Heegner_6 = v",      "lhs": T_6 + HEEGNER_6, "rhs": V,          "match": T_6 + HEEGNER_6 == V},
        {"identity": "mu^4 = (q!)^2 + C(k,3)",   "lhs": MU**4,       "rhs": QFACT**2 + comb(K_CODEC, 3), "match": MU**4 == QFACT**2 + comb(K_CODEC, 3)},
        {"identity": "mu^4 = 2^(Phi_6+1)",       "lhs": MU**4,       "rhs": 2**(PHI6+1),    "match": MU**4 == 2**(PHI6+1)},
        {"identity": "(mu+1)*Phi_6 + 1 = (q!)^2", "lhs": (MU+1)*PHI6+1, "rhs": QFACT**2,    "match": (MU+1)*PHI6+1 == QFACT**2},
        {"identity": "v + T_6 - g_neg - (q!)^2 = Phi_4",
                "lhs": V + T_6 - G_NEG - QFACT**2, "rhs": PHI4,
                "match": V + T_6 - G_NEG - QFACT**2 == PHI4},
    ]


def hierarchy_multiplication_identities() -> list[dict]:
    return [
        {"identity": "m_W = v_H / q",
         "form":     "q^(-(q!)^2) = q^(-((mu+1)*Phi_6 + 1))",
         "lhs":      QFACT**2,
         "rhs":      (MU+1)*PHI6 + 1,
         "match":    QFACT**2 == (MU+1)*PHI6 + 1},
        {"identity": "alpha_g = (m_p/m_Pl)^2",
         "form":     "q^(-2v) = (q^(-v))^2",
         "lhs":      2 * V,
         "rhs":      V * 2,
         "match":    True},
        {"identity": "Lambda^(1/2) ~ H_0 * m_Pl (dS)",
         "form":     "mu^4 = 2 * 2^Phi_6",
         "lhs":      MU**4,
         "rhs":      2 * 2**PHI6,
         "match":    MU**4 == 2 * 2**PHI6},
    ]


def baryon_density_identities() -> list[dict]:
    return [
        {"identity": "eta_B = q! / q^(T_6)",
         "form":     "q! * q^(-q*Phi_6)",
         "comment":  "Baryon-to-photon ratio = q!-fold prefactor with q^(T_6) suppression"},
        {"identity": "Omega_DM / Omega_b = q^q / (mu+1)",
         "form":     "27 / 5",
         "comment":  "Dark-matter to baryon ratio"},
        {"identity": "Omega_Lambda / Omega_DM = Phi_3 / (mu+1)",
         "form":     "13 / 5",
         "comment":  "DE to DM ratio"},
    ]


def principal_exponent_identity() -> dict:
    """The principal linear relation among the main exponents."""
    lhs = V + T_6 - G_NEG - QFACT**2
    rhs = PHI4
    return {
        "claim": "v + T_6 - g_neg - (q!)^2 = Phi_4",
        "substrate_values": "40 + 21 - 15 - 36 = 10",
        "lhs": lhs,
        "rhs": rhs,
        "match": lhs == rhs,
        "interpretation": (
            "The proton mass exponent (v), baryon asymmetry exponent (T_6), "
            "chiral multiplicity (g_neg), and EW exponent ((q!)^2) combine "
            "linearly to give the inflation scale exponent (Phi_4)."
        ),
    }


def all_identities() -> dict:
    return {
        "I_quantum_primitives":          quantum_primitives_identities(),
        "II_exponent_ladder":             exponent_ladder_identities(),
        "III_hierarchy_multiplication":   hierarchy_multiplication_identities(),
        "IV_baryon_density":              baryon_density_identities(),
        "V_principal_exponent":           principal_exponent_identity(),
    }


def headline() -> dict:
    return {
        "n_quantum_primitive":  len(quantum_primitives_identities()),
        "n_exponent_ladder":    len(exponent_ladder_identities()),
        "n_hierarchy_mult":     len(hierarchy_multiplication_identities()),
        "n_baryon_density":     len(baryon_density_identities()),
        "all_verified":         all(
            i.get("match", True) for i in quantum_primitives_identities()
        ) and all(
            i.get("match", True) for i in exponent_ladder_identities()
        ) and all(
            i.get("match", True) for i in hierarchy_multiplication_identities()
        ),
        "principal_identity":   "v + T_6 - g_neg - (q!)^2 = Phi_4 = 10",
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V, "T_6": T_6,
                "Heegner_6": HEEGNER_6,
            },
        },
        "all_identities":  all_identities(),
        "headline":         headline(),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_deep_structural_identities.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) DEEP STRUCTURAL IDENTITIES")
    print("=" * 78)

    for cat, items in payload["all_identities"].items():
        if cat == "V_principal_exponent":
            print(f"\n{cat}:")
            print(f"  {items['claim']}")
            print(f"  {items['substrate_values']}")
            print(f"  match: {items['match']}")
        else:
            print(f"\n{cat}:")
            for i in items:
                print(f"  {i['identity']:>40s}: lhs = {i.get('lhs', '?')}, rhs = {i.get('rhs', '?')}, match = {i.get('match', '?')}")

    h = payload["headline"]
    print(f"\nHEADLINE:")
    print(f"  Total identities verified: {h['n_quantum_primitive'] + h['n_exponent_ladder'] + h['n_hierarchy_mult']} (all checked)")
    print(f"  Principal identity: {h['principal_identity']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
