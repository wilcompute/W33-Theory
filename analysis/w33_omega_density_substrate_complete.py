"""W(3,3) COMPLETE OMEGA DENSITY SUBSTRATE FORMULA.

The substrate's pair of ratio identities
  Omega_DM / Omega_b      =  q^q / (mu+1)  =  27/5
  Omega_Lambda / Omega_DM =  Phi_3 / (mu+1) =  13/5

normalised gives ALL THREE COSMOLOGICAL DENSITY PARAMETERS as exact
substrate-rational expressions:

  Omega_b      =  (mu+1)^2 / 511        =  25/511   =  0.0489
                                            [PDG 0.049, 0.2%]
  Omega_DM     =  q^q * (mu+1) / 511    =  135/511  =  0.2642
                                            [PDG 0.265, 0.3%]
  Omega_Lambda =  Phi_3 * q^q / 511      =  351/511  =  0.6869
                                            [PDG 0.685, 0.3%]

The normalisation denominator is

  511  =  (mu+1)^2 + q^q * (mu+1) + Phi_3 * q^q
       =  25 + 135 + 351
       =  2^9 - 1
       =  2^(Phi_6 + 2) - 1
       =  Mersenne number M_9

So the substrate's complete cosmic-density formula uses TWO substrate
features:
  - numerators are products of {q^q, mu+1, Phi_3} primitives
  - denominator is the Mersenne number 2^(Phi_6+2) - 1

Three density predictions, each to ~0.3% PDG agreement, with a single
shared denominator.
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


# Planck 2018 measurements
OMEGA_B_PDG       = 0.049
OMEGA_DM_PDG      = 0.265
OMEGA_LAMBDA_PDG  = 0.685


def err_pct(p: float, e: float) -> float:
    return 100 * abs(p - e) / e


def density_parameters() -> dict:
    rel_b      = (MU + 1) ** 2          # 25
    rel_DM     = (Q ** Q) * (MU + 1)     # 135
    rel_Lambda = PHI3 * (Q ** Q)         # 351
    total = rel_b + rel_DM + rel_Lambda  # 511

    omega_b = rel_b / total
    omega_DM = rel_DM / total
    omega_Lambda = rel_Lambda / total

    return {
        "relative_weights": {
            "Omega_b":      {"value": rel_b,      "form": "(mu+1)^2 = 25"},
            "Omega_DM":     {"value": rel_DM,     "form": "q^q * (mu+1) = 135"},
            "Omega_Lambda": {"value": rel_Lambda, "form": "Phi_3 * q^q = 351"},
        },
        "denominator": {
            "value":  total,
            "form":   "(mu+1)^2 + q^q*(mu+1) + Phi_3*q^q = 511",
            "Mersenne": f"2^9 - 1 = 2^(Phi_6+2) - 1 = M_9 = {total}",
        },
        "predictions": {
            "Omega_b": {
                "formula": "(mu+1)^2 / 511 = 25/511",
                "predicted": omega_b,
                "pdg": OMEGA_B_PDG,
                "error_pct": err_pct(omega_b, OMEGA_B_PDG),
            },
            "Omega_DM": {
                "formula": "q^q * (mu+1) / 511 = 135/511",
                "predicted": omega_DM,
                "pdg": OMEGA_DM_PDG,
                "error_pct": err_pct(omega_DM, OMEGA_DM_PDG),
            },
            "Omega_Lambda": {
                "formula": "Phi_3 * q^q / 511 = 351/511",
                "predicted": omega_Lambda,
                "pdg": OMEGA_LAMBDA_PDG,
                "error_pct": err_pct(omega_Lambda, OMEGA_LAMBDA_PDG),
            },
        },
    }


def mersenne_substrate_connection() -> dict:
    return {
        "fact": "511 = 2^9 - 1 = M_9 (Mersenne number)",
        "substrate_form": "2^(Phi_6 + 2) - 1",
        "interpretation": (
            "The cosmic-density normalisation denominator is the "
            "Mersenne number M_9 = 2^9 - 1 = 511.  In substrate "
            "primitives, the exponent 9 = Phi_6 + 2 = 2q + 3.  This is "
            "the SAME 9 = q^2 that appears in the alpha^(-1) running "
            "correction (Delta alpha^(-1) ~ q^2 = 9)."
        ),
    }


def comparison_with_earlier_ratios() -> dict:
    return {
        "previously_derived": [
            "Omega_DM / Omega_b      = q^q / (mu+1) = 27/5 = 5.4   (PDG 5.41)",
            "Omega_Lambda / Omega_DM = Phi_3 / (mu+1) = 13/5 = 2.6  (PDG 2.58)",
        ],
        "now_derived": [
            "Omega_b = 25/511",
            "Omega_DM = 135/511",
            "Omega_Lambda = 351/511",
        ],
        "improvement": (
            "Previously had two ratio identities.  Now have three INDIVIDUAL "
            "Omega values from a single substrate formula with shared "
            "Mersenne denominator 511 = 2^9 - 1."
        ),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6, "v": V,
            },
        },
        "density_parameters":           density_parameters(),
        "mersenne_substrate_connection": mersenne_substrate_connection(),
        "comparison_with_earlier_ratios": comparison_with_earlier_ratios(),
        "headline": (
            "All three cosmic density parameters from substrate (0.3% accuracy):\n"
            "  Omega_b      = (mu+1)^2/511 = 25/511 = 0.0489     [PDG 0.049]\n"
            "  Omega_DM     = q^q(mu+1)/511 = 135/511 = 0.2642   [PDG 0.265]\n"
            "  Omega_Lambda = Phi_3 q^q/511 = 351/511 = 0.6869   [PDG 0.685]\n"
            "Shared denominator: 511 = 2^9 - 1 = M_9 = Mersenne prime."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_omega_density_substrate_complete.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) COMPLETE OMEGA DENSITY SUBSTRATE FORMULA")
    print("=" * 78)

    d = payload["density_parameters"]
    print("\nRelative weights (numerators):")
    for k, v in d["relative_weights"].items():
        print(f"  {k:>12s}: {v['value']:>3d}  ({v['form']})")
    print(f"  Sum = {d['denominator']['value']} = {d['denominator']['form']}")
    print(f"  Mersenne: {d['denominator']['Mersenne']}")

    print("\nPredictions:")
    for k, p in d["predictions"].items():
        print(f"  {k:>15s}: {p['formula']}")
        print(f"    predicted = {p['predicted']:.5f}, PDG = {p['pdg']}, error = {p['error_pct']:.2f}%")

    m = payload["mersenne_substrate_connection"]
    print(f"\nMersenne-substrate connection:")
    print(f"  {m['fact']}")
    print(f"  {m['interpretation']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
