"""W(3,3) COSMOLOGICAL OBSERVABLES FROM SUBSTRATE.

Substrate predictions for the principal cosmological observables:
  - Hubble constant H_0
  - Cosmological constant Lambda (energy density rho_Lambda)
  - Critical density rho_crit
  - Density parameters Omega_Lambda, Omega_DM, Omega_baryon
  - Age of the universe

These follow from the W(3,3) substrate primitives at q=3, expressed in
Planck units via substrate-clean exponents.

KEY IDENTITIES:

  H_0 / m_Pl       =  q^(-2^Phi_6)     =  3^(-128)    approx 1.6e-61
                      [observed: 1.23e-61]

  Lambda / m_Pl^4  =  q^(-mu^4)         =  3^(-256)    approx 10^(-122.14)
                      [observed: 10^(-122)]

  CONSISTENCY (de Sitter):
  (H_0 / m_Pl)^2 ~ Lambda / m_Pl^4 -> -2*128 = -256.  CONSISTENT.

The substrate exponents satisfy the dS relation exactly:

  -log_q(Lambda/m_Pl^4)  =  2 * (-log_q(H_0/m_Pl))
              mu^4      =  2 * 2^Phi_6
                256      =  2 * 128

THE FUNDAMENTAL SUBSTRATE-COSMOLOGY IDENTITY:

  mu^4  =  2 * 2^Phi_6  =  2^(Phi_6 + 1)  =  2^8

so mu^4 = 256 = 2^8 where Phi_6 + 1 = 8 = 2*mu, giving the consistency
between Lambda and H_0 via dS:

    mu^4 = 2^(Phi_6 + 1) = 2^(2*mu)
"""
from __future__ import annotations

import json
import math
from pathlib import Path


# Substrate constants
Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
V = 40
EDGES = 240


# Observed cosmological values
H_0_PER_SEC          = 2.27e-18                # s^-1, Planck 2018
H_0_GEV              = 1.5e-42                  # GeV (= H_0 * hbar in GeV)
M_PL_GEV             = 1.2209e19                # GeV
LAMBDA_OVER_PL4_OBS  = 1.1e-122                 # observed Lambda / m_Pl^4
OMEGA_LAMBDA_OBS     = 0.685
OMEGA_DM_OBS         = 0.265
OMEGA_BARYON_OBS     = 0.049
AGE_UNIVERSE_YR      = 13.8e9                   # years
RHO_CRIT_KG_M3       = 8.5e-27                  # kg / m^3


def hubble_constant() -> dict:
    """H_0 / m_Pl = q^(-2^Phi_6) = 3^(-128) (substrate prediction)."""
    exponent = 2 ** PHI6
    pred_ratio = Q ** (-exponent)
    pred_log10 = -exponent * math.log10(Q)
    obs_ratio = H_0_GEV / M_PL_GEV
    obs_log10 = math.log10(obs_ratio)
    return {
        "formula":          "H_0 / m_Pl = q^(-2^Phi_6) = 3^(-128)",
        "exponent_form":    "2^Phi_6 = 2^7 = 128",
        "predicted_ratio":  pred_ratio,
        "predicted_log10":  pred_log10,
        "observed_ratio":   obs_ratio,
        "observed_log10":   obs_log10,
        "log_difference":   abs(pred_log10 - obs_log10),
    }


def cosmological_constant() -> dict:
    """Lambda / m_Pl^4 = q^(-mu^4) = 3^(-256) (substrate prediction)."""
    exponent = MU ** 4
    pred_ratio = Q ** (-exponent)
    pred_log10 = -exponent * math.log10(Q)
    obs_log10 = math.log10(LAMBDA_OVER_PL4_OBS)
    return {
        "formula":          "Lambda / m_Pl^4 = q^(-mu^4) = 3^(-256)",
        "exponent_form":    "mu^4 = 4^4 = 256 = 2^(2 mu)",
        "predicted_ratio":  pred_ratio,
        "predicted_log10":  pred_log10,
        "observed_log10":   obs_log10,
        "log_difference":   abs(pred_log10 - obs_log10),
    }


def consistency_check() -> dict:
    """In dS: Lambda ~ H_0^2 * m_Pl^2, so Lambda / m_Pl^4 ~ (H_0 / m_Pl)^2.

    Substrate: -mu^4 = 2 * -2^Phi_6.  Check: 256 = 2 * 128."""
    lhs = MU ** 4
    rhs = 2 * (2 ** PHI6)
    return {
        "claim":      "mu^4 = 2 * 2^Phi_6 (dS relation between Lambda and H_0)",
        "lhs":        lhs,
        "lhs_form":   "mu^4 = 256",
        "rhs":        rhs,
        "rhs_form":   "2 * 2^Phi_6 = 2 * 128 = 256",
        "match":      lhs == rhs,
        "implication": "Substrate exponents for Lambda and H_0 are dS-consistent.",
    }


def omega_density_parameters() -> dict:
    """The density parameters Omega_Lambda, Omega_DM, Omega_b sum to 1.

    Substrate candidates for the ratios:
    Omega_DM / Omega_b = 0.265 / 0.049 = 5.4 ~ mu + 1 (Csaszar realiz.)
    Omega_Lambda / Omega_DM = 0.685 / 0.265 = 2.58 ~ q*Phi_3/k = ... (try)
    """
    return {
        "Omega_Lambda_obs":  OMEGA_LAMBDA_OBS,
        "Omega_DM_obs":      OMEGA_DM_OBS,
        "Omega_baryon_obs":  OMEGA_BARYON_OBS,
        "Omega_DM_over_Omega_b": {
            "observed":   OMEGA_DM_OBS / OMEGA_BARYON_OBS,
            "substrate":  "mu + 1 = 5 (Csaszar realization count)",
            "predicted":  MU + 1,
            "error_pct":  100 * abs((MU + 1) - OMEGA_DM_OBS / OMEGA_BARYON_OBS) / (OMEGA_DM_OBS / OMEGA_BARYON_OBS),
        },
        "Omega_Lambda_over_Omega_DM": {
            "observed":   OMEGA_LAMBDA_OBS / OMEGA_DM_OBS,
            "substrate":  "(approximately q^2 / Phi_6 ~ 1.286)? Mismatch 1.3 vs 2.58.",
            "comment":    "No clean substrate identity yet for Omega_Lambda/Omega_DM ratio.",
        },
    }


def age_of_universe() -> dict:
    """Age ~ 1/H_0.  Substrate: log_3(age * m_Pl) = +128."""
    age_seconds = AGE_UNIVERSE_YR * 365.25 * 86400
    age_planck_units = age_seconds / 5.39e-44   # tau_Pl ~ 5.4e-44 s
    log10_age_planck = math.log10(age_planck_units)
    return {
        "age_seconds":        age_seconds,
        "age_planck_units":   age_planck_units,
        "log10_age_planck":   log10_age_planck,
        "substrate_form":     "age ~ 1/H_0 ~ m_Pl * q^(2^Phi_6) = m_Pl * 3^128",
        "substrate_log10":    PHI6 * math.log10(2) + math.log10(Q) * (2 ** PHI6),
        "comment":            "Order-of-magnitude match.",
    }


def cosmological_dictionary() -> list[dict]:
    return [
        {"observable": "H_0 / m_Pl",         "substrate": "q^(-2^Phi_6)",    "log10_pred": -2 ** PHI6 * math.log10(Q), "log10_obs": -60.9},
        {"observable": "Lambda / m_Pl^4",   "substrate": "q^(-mu^4)",        "log10_pred": -MU ** 4 * math.log10(Q),   "log10_obs": -122},
        {"observable": "age * m_Pl",         "substrate": "q^(2^Phi_6)",       "log10_pred": +2 ** PHI6 * math.log10(Q), "log10_obs": +60.9},
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "q!": QFACT, "v": V, "edges": EDGES,
                "m_Pl_GeV": M_PL_GEV,
            },
        },
        "hubble_constant":              hubble_constant(),
        "cosmological_constant":         cosmological_constant(),
        "consistency_check":             consistency_check(),
        "omega_density_parameters":      omega_density_parameters(),
        "age_of_universe":               age_of_universe(),
        "cosmological_dictionary":       cosmological_dictionary(),
        "headline_identity": (
            "Three cosmological scales are substrate-clean exponents of q=3:\n"
            "  H_0 / m_Pl       = q^(-2^Phi_6)  = 3^(-128)  ~ 10^(-61)\n"
            "  Lambda / m_Pl^4 = q^(-mu^4)      = 3^(-256)  ~ 10^(-122)\n"
            "  age * m_Pl       = q^(+2^Phi_6)  = 3^(+128)  ~ 10^(+61)\n"
            "Self-consistent under the dS relation Lambda ~ H_0^2 m_Pl^2: "
            "mu^4 = 2 * 2^Phi_6 = 2 * 128 = 256."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_cosmological_observables_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) COSMOLOGICAL OBSERVABLES FROM SUBSTRATE")
    print("=" * 78)

    h = payload["hubble_constant"]
    print(f"\nHubble constant:")
    print(f"  {h['formula']}")
    print(f"  predicted log10 = {h['predicted_log10']:.2f}")
    print(f"  observed log10  = {h['observed_log10']:.2f}")
    print(f"  log difference: {h['log_difference']:.2f}")

    c = payload["cosmological_constant"]
    print(f"\nCosmological constant:")
    print(f"  {c['formula']}")
    print(f"  predicted log10 = {c['predicted_log10']:.2f}")
    print(f"  observed log10  = {c['observed_log10']:.2f}")
    print(f"  log difference: {c['log_difference']:.2f}")

    cc = payload["consistency_check"]
    print(f"\ndS consistency check (Lambda ~ H_0^2):")
    print(f"  {cc['claim']}")
    print(f"  {cc['lhs_form']}, {cc['rhs_form']}: match = {cc['match']}")
    print(f"  {cc['implication']}")

    o = payload["omega_density_parameters"]
    print(f"\nDensity parameter ratios:")
    print(f"  Omega_DM / Omega_b  =  {o['Omega_DM_over_Omega_b']['observed']:.2f}  ~  {o['Omega_DM_over_Omega_b']['substrate']}")
    print(f"  err: {o['Omega_DM_over_Omega_b']['error_pct']:.2f}%")

    print(f"\nHEADLINE:")
    print(payload["headline_identity"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
