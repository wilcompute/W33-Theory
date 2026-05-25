"""W(3,3) BARYON ASYMMETRY ETA_B FROM SUBSTRATE.

The baryon-to-photon ratio eta_B = n_B / n_gamma ~ 6e-10 is the most
direct quantitative measure of matter-antimatter asymmetry in the
observable universe.  It is one of the principal unexplained numbers
in cosmology.

The W(3,3) substrate predicts:

  eta_B  =  q! / q^(T_6)  =  q! / q^(q * Phi_6)
        =  6 / 3^21
        =  6 / 1.05e10
        =  5.72e-10

  PDG (2024):  eta_B = (6.10 +/- 0.04) e-10.
  Substrate:   5.72e-10.
  Error:       6.3%.

Refined identity using exact CMB-determined eta_B = 6.10e-10:

  eta_B  ~  q!  *  q^(-T_6)
        ~  6  *  3^(-21)

Substrate readings of the exponent T_6 = 21:
  T_6 = q * Phi_6  =  3 * 7  =  21  (Fano flag count)
  T_6 = Csaszar_E = Szilassi_E       (genus-1 minimal poly edges)
  T_6 = triangular number T_(Phi_6) = 6*7/2 = 21

The baryon asymmetry is therefore a substrate suppression by
q^(T_6) = 3^21, with a q!-fold combinatorial prefactor.

CONNECTION TO LEPTOGENESIS:

In leptogenesis, eta_B ~ eta_L * sphaleron_factor ~ 10^-10.
The CP asymmetry parameter eps ~ 10^-6 typical.
sphaleron conversion ~ 10^-3 ~ 1/k? or 1/Phi_3?

eps * sphaleron ~ 10^-9 ~ eta_B (order of magnitude).

The substrate q!/q^(T_6) reading subsumes these contributions into
a single substrate-clean ratio.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
V = 40
T_6 = Q * PHI6  # 21


ETA_B_PDG = 6.10e-10
ETA_B_PDG_LOG10 = math.log10(ETA_B_PDG)


def baryon_asymmetry() -> dict:
    """eta_B = q! / q^(T_6) = 6 / 3^21."""
    pred = QFACT / (Q ** T_6)
    log10_pred = math.log10(pred)
    return {
        "formula":           "eta_B = q! / q^(T_6) = q! / q^(q*Phi_6)",
        "substrate_form":    "6 / 3^21 = 6 / 1.05e10",
        "predicted":         pred,
        "log10_predicted":   log10_pred,
        "pdg":               ETA_B_PDG,
        "log10_pdg":         ETA_B_PDG_LOG10,
        "error_pct":         100 * abs(pred - ETA_B_PDG) / ETA_B_PDG,
        "log_discrepancy":   abs(log10_pred - ETA_B_PDG_LOG10),
    }


def t_6_substrate_readings() -> list[dict]:
    return [
        {"reading": "q * Phi_6 = 3 * 7 = 21",
         "interpretation": "Fano flag count (point-line incidences in Fano plane)"},
        {"reading": "Csaszar_E = Szilassi_E = 21",
         "interpretation": "Edge count of genus-1 minimal toroidal polyhedra"},
        {"reading": "triangular number T_{Phi_6} = 6*7/2",
         "interpretation": "6th triangular number"},
    ]


def cosmological_relationships() -> dict:
    return {
        "leptogenesis_estimate":  "eta_B ~ eps * (sphaleron factor) ~ 10^-6 * 10^-3 ~ 10^-9",
        "substrate_subsumes":     "q!/q^(T_6) = 6/3^21 ~ 6e-10",
        "physical_interpretation": (
            "The baryon-to-photon ratio is a q^(T_6)-fold substrate "
            "suppression with q! combinatorial prefactor.  T_6 = Csaszar "
            "edge count = q*Phi_6 = Fano flag count."
        ),
    }


def joint_with_cosmological_constants() -> dict:
    return {
        "Lambda / m_Pl^4":  {"substrate": "q^(-mu^4)",   "exponent": -256},
        "H_0 / m_Pl":        {"substrate": "q^(-2^Phi_6)", "exponent": -128},
        "T_CMB / m_Pl":      {"substrate": "q^(-Heegner_67)", "exponent": -67},
        "eta_B":             {"substrate": "q! * q^(-T_6)", "exponent": -21},
        "alpha_g":           {"substrate": "q^(-2v)",     "exponent": -80},
        "m_p / m_Pl":        {"substrate": "q^(-v)",       "exponent": -40},
        "m_W / m_Pl":        {"substrate": "q^(-(q!)^2)",  "exponent": -36},
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC, "q!": QFACT,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "T_6": T_6, "v": V,
            },
        },
        "baryon_asymmetry":                  baryon_asymmetry(),
        "T_6_substrate_readings":            t_6_substrate_readings(),
        "cosmological_relationships":        cosmological_relationships(),
        "joint_with_cosmological_constants": joint_with_cosmological_constants(),
        "headline_identity": (
            "eta_B = q! / q^(T_6) = q!/3^21 = 5.72e-10 "
            "(PDG 6.10e-10, 6% in linear, 0.03 in log space). "
            "The baryon asymmetry is a substrate suppression by "
            "Csaszar/Szilassi-edge powers of q with q! prefactor."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_baryon_asymmetry_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) BARYON ASYMMETRY ETA_B SUBSTRATE IDENTITY")
    print("=" * 78)

    b = payload["baryon_asymmetry"]
    print(f"\nMain prediction:")
    print(f"  {b['formula']}")
    print(f"  substrate: {b['substrate_form']}")
    print(f"  predicted: {b['predicted']:.3e}")
    print(f"  PDG:       {b['pdg']:.3e}")
    print(f"  error:     {b['error_pct']:.2f}% (linear), {b['log_discrepancy']:.3f} (log10)")

    print(f"\nT_6 = 21 substrate readings:")
    for r in payload["T_6_substrate_readings"]:
        print(f"  {r['reading']:>40s}: {r['interpretation']}")

    print(f"\nJoint with cosmological constants (all q^(-X) exponents):")
    for k, v in payload["joint_with_cosmological_constants"].items():
        print(f"  {k:>20s}: {v['substrate']:>20s}, exponent = {v['exponent']}")

    print(f"\nHEADLINE: {payload['headline_identity']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
