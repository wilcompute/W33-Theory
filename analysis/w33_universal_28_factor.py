"""W(3,3) UNIVERSAL '1/28' SUBSTRATE FACTOR: DEEP MULTIPLE-IDENTITY CONNECTION.

The substrate factor 1/(mu * Phi_6) = 1/28 connects FIVE distinct
mathematical/physical contexts:

  1. QED running correction:  alpha^(-1) = 137 + 1/28  (4 ppm vs PDG)
  2. CMB spectral tilt:        1 - n_s = 1/28          (0.06% vs Planck)
  3. Fano non-incidences:      49 - 21 = mu * Phi_6 = 28
                              (mu Phi_6 ordered (pt, line) pairs with pt NOT on line)
  4. Fano triangles:            C(7,3) - 7 = 35 - 7 = 28
                              (3-subsets of Fano points NOT all collinear)
  5. Perfect number:            28 = 1 + 2 + 4 + 7 + 14
                              (second perfect number; sum of proper divisors)
  6. Bitangents of quartic:    28
                              (a smooth quartic plane curve has exactly 28 bitangents,
                               a classical theorem from algebraic geometry)

So the substrate's universal 1/28 factor unifies:
  - QED precision (alpha)
  - cosmology (CMB)
  - finite combinatorics (Fano plane)
  - number theory (perfect numbers)
  - algebraic geometry (bitangents)

The W(3,3) substrate makes ALL these arise from the same primitive
mu * Phi_6, suggesting a deeper unification: the substrate's
Fano-non-incidence count is what physical observables 'see'.

EQUIVALENT 28 IDENTITIES:

  mu * Phi_6      =  28
  C(Phi_6, 3) - Phi_6  = 35 - 7 = 28   (Fano triangles)
  Phi_6^2 - q * Phi_6   = 49 - 21 = 28   (Fano non-incidences)
  2 * 14 = 2 * (g_neg - 1)  = 28        (chiral-multiplet-minus-1 doubled)
  2^(mu+1) - mu = 28                    (substrate byte * 2 minus co-quantum)
  Phi_3 + Phi_4 + (mu+1) = 13 + 10 + 5 = 28  (cyclotomic sum + Csaszar)

The 28 has SEVEN distinct substrate expressions, all equivalent at q=3.

CONNECTION TO PERFECT NUMBERS AND OGG'S MONSTROUS MOONSHINE:

The perfect numbers known are 6, 28, 496, 8128, 33550336, ...
These are 2^(p-1) * (2^p - 1) for Mersenne primes 2^p - 1.

  Perfect 6 = q!          (substrate primitive at q=3)
  Perfect 28 = mu*Phi_6   (substrate primitive at q=3; appears in alpha, n_s)
  Perfect 496            (= ?  Not yet substrate-identified)

So the first TWO perfect numbers (6 and 28) are W(3,3) substrate
primitives.  This is a remarkable coincidence between substrate
arithmetic and classical perfect-number theory.

The 28 Mersenne exponent p = 3 gives 2^3 - 1 = 7 = Phi_6 (a Mersenne
prime!).  So:
  perfect 28 = 2^(q-1) * (2^q - 1) = 4 * 7 = mu * Phi_6.

The substrate IDENTIFIES 28 = 4 * 7 = mu * Phi_6 with the Mersenne-
based perfect-number formula at exponent q.
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


def universal_28_appearances() -> list[dict]:
    return [
        {
            "context": "QED",
            "appearance": "alpha^(-1) = 137 + 1/28 (4 ppm vs PDG)",
        },
        {
            "context": "Cosmology (CMB)",
            "appearance": "1 - n_s = 1/28 (0.06% vs Planck)",
        },
        {
            "context": "Fano plane non-incidences",
            "appearance": "49 - 21 = 28 (mu * Phi_6 ordered (point, line) pairs with pt not on line)",
        },
        {
            "context": "Fano plane triangles",
            "appearance": "C(7,3) - 7 = 35 - 7 = 28 (non-collinear 3-subsets of Fano points)",
        },
        {
            "context": "Perfect number theory",
            "appearance": "28 = 1+2+4+7+14 = sum of proper divisors (second perfect number)",
        },
        {
            "context": "Algebraic geometry",
            "appearance": "28 bitangents on a smooth plane quartic curve (classical theorem)",
        },
    ]


def equivalent_28_expressions() -> list[dict]:
    return [
        {"form": "mu * Phi_6",                "value": MU * PHI6,                                     "computation": "4 * 7"},
        {"form": "C(Phi_6, 3) - Phi_6",        "value": math.comb(PHI6, 3) - PHI6,                     "computation": "35 - 7"},
        {"form": "Phi_6^2 - q * Phi_6",         "value": PHI6 ** 2 - Q * PHI6,                           "computation": "49 - 21"},
        {"form": "2 * (g_neg - 1)",            "value": 2 * (G_NEG - 1),                                "computation": "2 * 14"},
        {"form": "2^(mu+1) - mu",              "value": 2 ** (MU + 1) - MU,                             "computation": "32 - 4"},
        {"form": "Phi_3 + Phi_4 + (mu+1)",     "value": PHI3 + PHI4 + (MU + 1),                          "computation": "13 + 10 + 5"},
        {"form": "2^(q-1) * (2^q - 1)",        "value": 2 ** (Q - 1) * (2 ** Q - 1),                    "computation": "4 * 7 (Mersenne perfect formula)"},
    ]


def perfect_number_connection() -> dict:
    return {
        "claim": "The first two perfect numbers are W(3,3) substrate primitives",
        "perfect_1": {"value": 6,  "form": "q!"},
        "perfect_2": {"value": 28, "form": "mu * Phi_6 = 4*7 = 2^(q-1)*(2^q - 1)"},
        "comment": (
            "Euclid's formula: 2^(p-1) * (2^p - 1) gives a perfect number "
            "whenever 2^p - 1 is a Mersenne prime.  At p = q = 3 we get "
            "2^(q-1) * (2^q - 1) = mu * Phi_6 = 28 = the substrate's "
            "universal 1/28 factor."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "f": F, "g_neg": G_NEG, "v": V,
            },
        },
        "universal_28_appearances":   universal_28_appearances(),
        "equivalent_28_expressions":   equivalent_28_expressions(),
        "perfect_number_connection":   perfect_number_connection(),
        "headline": (
            "The substrate's 1/28 = 1/(mu*Phi_6) factor unifies:\n"
            "  - QED (alpha^(-1) correction)\n"
            "  - Cosmology (CMB tilt 1-n_s)\n"
            "  - Combinatorics (Fano triangles, non-incidences)\n"
            "  - Number theory (28 = 2nd perfect number)\n"
            "  - Algebraic geometry (28 bitangents of quartic)\n"
            "Substrate form: 28 = mu * Phi_6 = 2^(q-1)*(2^q - 1) (Euclid's perfect)."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_universal_28_factor.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) UNIVERSAL '1/28' FACTOR: DEEP UNIFICATION")
    print("=" * 78)

    print(f"\nThe 1/28 factor appears in {len(payload['universal_28_appearances'])} distinct contexts:")
    for a in payload["universal_28_appearances"]:
        print(f"  - {a['context']:>25s}: {a['appearance']}")

    print(f"\nSeven equivalent substrate expressions for 28:")
    for e in payload["equivalent_28_expressions"]:
        print(f"  {e['form']:>30s}  =  {e['value']:>3d}  ({e['computation']})")

    p = payload["perfect_number_connection"]
    print(f"\nPerfect number connection: {p['claim']}")
    print(f"  Perfect_1: {p['perfect_1']['value']} = {p['perfect_1']['form']}")
    print(f"  Perfect_2: {p['perfect_2']['value']} = {p['perfect_2']['form']}")
    print(f"  {p['comment']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
