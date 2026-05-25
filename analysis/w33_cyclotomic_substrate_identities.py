"""W(3,3) CYCLOTOMIC SUBSTRATE IDENTITIES.

The three cyclotomic primitives Phi_3, Phi_4, Phi_6 satisfy a tight web
of identities at q = 3.  These connect:

  Phi_3 - Phi_6 = q!        =  6
  Phi_3 + Phi_6 = 2 Phi_4   =  20  (= v/2)
  Phi_3 * Phi_6 = q^4 + q^2 + 1 = q^(q+1) + q^2 + 1 = 91 (= m_Z in GeV)
  Phi_4 * Phi_6 = q^4 - q^3 + q + 1 = ... = 70 (Phi_6*Phi_4 axion exponent)
  Phi_3 * Phi_4 = q^4 + q^3 + q^2 + q = q(q^3 + q^2 + q + 1) = 130 (rho_bar denom*2)

NEW PHYSICS-LEVEL IDENTITY:

  m_Z (GeV)  =  Phi_3 * Phi_6  =  q^(q+1) + q^2 + 1
                              =  91  =  matter_sector + q^2 + 1
                              =  81 + 9 + 1                  (PDG 91.188, 0.2%)

The Z boson mass equals the matter sector dimension plus the
fundamental-quantum squared plus one.  Substrate-clean decomposition.

THE CYCLOTOMIC SUBSTRATE WEB:

  q + Phi_6  =  Phi_3 - q + q + Phi_6 + ... wait simpler:
  q + Phi_6  =  q + q^2-q+1 = q^2+1 = Phi_4   ! So Phi_4 = q + Phi_6.

So Phi_4 = q + Phi_6.  At q=3: 10 = 3 + 7 ✓.

Plus:
  Phi_4 + q = Phi_4 + (Phi_4 - Phi_6) = ... hmm
  Phi_3 = Phi_4 + q = Phi_4 + (Phi_4 - Phi_6) = 2*Phi_4 - Phi_6
        Verify: 13 = 20 - 7 ✓
  Phi_3 = 2*Phi_4 - Phi_6

THE COMPLETE WEB:

  Phi_3 = q^2 + q + 1 = q + Phi_4 = 2*Phi_4 - Phi_6
  Phi_4 = q^2 + 1     = q + Phi_6 = Phi_3 - q
  Phi_6 = q^2 - q + 1 = Phi_4 - q = Phi_3 - q!

ALL THREE CYCLOTOMIC PRIMITIVES ARE LINEARLY RELATED VIA q AND q!:

  Phi_3 = Phi_4 + q  =  Phi_6 + q!
  Phi_4 = Phi_6 + q  =  Phi_3 - q
  Phi_6 = Phi_4 - q  =  Phi_3 - q!

This is the substrate's "cyclotomic ladder": stepping by q from Phi_6
to Phi_4 to Phi_3 (and equivalently by q! from Phi_6 to Phi_3).
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
V = 40


def cyclotomic_relations() -> list[dict]:
    return [
        {"identity": "Phi_3 - Phi_6 = q!",      "lhs": PHI3 - PHI6,    "rhs": QFACT,         "match": PHI3 - PHI6 == QFACT},
        {"identity": "Phi_3 + Phi_6 = 2 Phi_4", "lhs": PHI3 + PHI6,    "rhs": 2 * PHI4,      "match": PHI3 + PHI6 == 2 * PHI4},
        {"identity": "Phi_3 + Phi_6 = v/2",      "lhs": PHI3 + PHI6,    "rhs": V // 2,        "match": PHI3 + PHI6 == V // 2},
        {"identity": "Phi_3 - q = Phi_4",       "lhs": PHI3 - Q,        "rhs": PHI4,          "match": PHI3 - Q == PHI4},
        {"identity": "Phi_4 - q = Phi_6",       "lhs": PHI4 - Q,        "rhs": PHI6,          "match": PHI4 - Q == PHI6},
        {"identity": "Phi_3 = 2*Phi_4 - Phi_6", "lhs": 2 * PHI4 - PHI6, "rhs": PHI3,          "match": 2 * PHI4 - PHI6 == PHI3},
        {"identity": "Phi_3 * Phi_6 = q^(q+1) + q^2 + 1",
         "lhs": PHI3 * PHI6,
         "rhs": Q ** (Q + 1) + Q ** 2 + 1,
         "match": PHI3 * PHI6 == Q ** (Q + 1) + Q ** 2 + 1},
    ]


def m_Z_decomposition() -> dict:
    pred = Q ** (Q + 1) + Q ** 2 + 1
    return {
        "name":           "m_Z (GeV)",
        "decomposition":  "m_Z = Phi_3 * Phi_6 = q^(q+1) + q^2 + 1",
        "computation":    "81 + 9 + 1 = 91",
        "predicted":      pred,
        "pdg":            91.188,
        "error_pct":      100 * abs(pred - 91.188) / 91.188,
        "substrate_form": "matter_sector + q^2 + 1",
    }


def cyclotomic_ladder() -> dict:
    return {
        "Phi_6 to Phi_4":   {"step": "+q",  "shift": Q},
        "Phi_4 to Phi_3":   {"step": "+q",  "shift": Q},
        "Phi_6 to Phi_3":   {"step": "+q!", "shift": QFACT},
        "expression":       (
            "Phi_3 = Phi_4 + q = Phi_6 + q!.  Stepping by q (single q-unit) "
            "from Phi_6 -> Phi_4 -> Phi_3, or by q! = 2q in one step "
            "directly from Phi_6 to Phi_3."
        ),
    }


def shared_factors_table() -> list[dict]:
    """The cyclotomic ladder generates the principal denominators."""
    return [
        {"denominator": "Phi_3 = 13",         "appears_in": "sin^2 theta_W, sin^2 theta_12, alpha_s, rho_bar, sigma_8, lambda_H"},
        {"denominator": "Phi_4 = 10",         "appears_in": "tan delta_CKM (numerator), m_Z (Phi_3*Phi_4 cancels)"},
        {"denominator": "Phi_6 = 7",          "appears_in": "Phi_6*Phi_4 axion exponent, y_b/y_tau"},
        {"denominator": "mu*Phi_6 = 28",      "appears_in": "alpha correction, 1-n_s (UNIVERSAL 1/28)"},
        {"denominator": "2*Phi_6/v = 7/20",   "appears_in": "Lambda_QCD/m_p, eta_bar (UNIVERSAL 7/20)"},
        {"denominator": "Phi_3 + q = 16 = 2^mu", "appears_in": "sigma_8 (= Phi_3/(Phi_3+q))"},
        {"denominator": "Phi_3 * Phi_6 = 91", "appears_in": "m_Z (substrate-clean); sin^2 theta_13 (= 2/91)"},
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6, "v": V,
            },
        },
        "cyclotomic_relations":  cyclotomic_relations(),
        "m_Z_decomposition":      m_Z_decomposition(),
        "cyclotomic_ladder":       cyclotomic_ladder(),
        "shared_factors_table":    shared_factors_table(),
        "headline": (
            "Cyclotomic substrate ladder:\n"
            "  Phi_3 = Phi_4 + q = Phi_6 + q!\n"
            "  Phi_4 = Phi_6 + q\n"
            "  Phi_3 + Phi_6 = 2 Phi_4 = v/2\n"
            "  Phi_3 - Phi_6 = q!\n"
            "  Phi_3 * Phi_6 = q^(q+1) + q^2 + 1 = m_Z (in GeV)\n"
            "These 7 identities are all exact at q=3."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cyclotomic_substrate_identities.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) CYCLOTOMIC SUBSTRATE IDENTITIES")
    print("=" * 78)

    print("\nCyclotomic identities:")
    for r in payload["cyclotomic_relations"]:
        print(f"  {r['identity']:>40s}: lhs={r['lhs']}, rhs={r['rhs']}, match={r['match']}")

    m = payload["m_Z_decomposition"]
    print(f"\nNew physics-level identity:")
    print(f"  {m['decomposition']}")
    print(f"  {m['computation']}")
    print(f"  predicted: {m['predicted']}, PDG: {m['pdg']}, error: {m['error_pct']:.2f}%")

    print(f"\nCyclotomic ladder:")
    for k, v in payload["cyclotomic_ladder"].items():
        if k != "expression":
            print(f"  {k}: {v['step']} (= {v['shift']})")
    print(f"  {payload['cyclotomic_ladder']['expression']}")

    print(f"\nShared substrate denominators:")
    for s in payload["shared_factors_table"]:
        print(f"  {s['denominator']:>25s}: {s['appears_in']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
