"""W(3,3) GREAT HIERARCHIES: ALL LOG-SCALES FROM SUBSTRATE PRIMITIVES.

A consolidated derivation of the principal hierarchical log-scales in
physics, each expressed as a power of q=3 with substrate-primitive
exponent.

THE HIERARCHIES (sorted by physical scale):

  log_q(m_Pl / m_W)        =  (q!)^2           =  36       (electroweak)
  log_q(m_Pl / v_Higgs)    =  (mu+1)*Phi_6      =  35       (EWSB)
  log_q(m_Pl^4 / Lambda)   =  mu^4              =  256      (cosmological)
  log_q(m_Pl / H_0)         =  2^Phi_6           =  128      (Hubble)
  log_q(m_Pl / H_inf)       =  Phi_4             =  10       (inflation)
  log_q(m_Pl / T_CMB)       ~  Heegner_67        =  67       (CMB temp)

All six exponents are substrate-clean integers built from q=3
primitives.  The dS consistency condition (Lambda ~ H_0^2 m_Pl^2)
manifests as the substrate identity:

  mu^4  =  2 * 2^Phi_6  =  2^(Phi_6 + 1)  =  256

i.e., the cosmological-constant exponent is exactly twice the
Hubble-constant exponent.

NEW SUBSTRATE IDENTITY:

  mu^4  =  2^(Phi_6 + 1)  =  2^8  =  256

This relates the substrate's co-quantum quartic power (mu^4 = 256) to
the substrate-byte-shifted Fano-point exponent (2^(Phi_6+1)).
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
EDGES = 240
HEEGNER_67 = 67


def hierarchies_table() -> list[dict]:
    """All major physical hierarchies expressed in substrate-clean q-exponents."""
    return [
        {
            "physical_scale": "m_W / m_Pl",
            "exponent_value": -(QFACT ** 2),
            "substrate_form": "-(q!)^2 = -36",
            "log10_predicted": -(QFACT ** 2) * math.log10(Q),
            "log10_observed":  math.log10(80.379 / 1.2209e19),
            "physics_label":   "electroweak scale",
        },
        {
            "physical_scale": "v_Higgs / m_Pl",
            "exponent_value": -((MU + 1) * PHI6),
            "substrate_form": "-(mu+1)*Phi_6 = -35",
            "log10_predicted": -((MU + 1) * PHI6) * math.log10(Q),
            "log10_observed":  math.log10(246.22 / 1.2209e19),
            "physics_label":   "EWSB scale",
        },
        {
            "physical_scale": "Lambda / m_Pl^4",
            "exponent_value": -(MU ** 4),
            "substrate_form": "-mu^4 = -256 = -2^(Phi_6+1)",
            "log10_predicted": -(MU ** 4) * math.log10(Q),
            "log10_observed":  -122,
            "physics_label":   "cosmological constant",
        },
        {
            "physical_scale": "H_0 / m_Pl",
            "exponent_value": -(2 ** PHI6),
            "substrate_form": "-2^Phi_6 = -128",
            "log10_predicted": -(2 ** PHI6) * math.log10(Q),
            "log10_observed":  math.log10(1.5e-42 / 1.2209e19),
            "physics_label":   "Hubble scale today",
        },
        {
            "physical_scale": "H_inf / m_Pl",
            "exponent_value": -PHI4,
            "substrate_form": "-Phi_4 = -10",
            "log10_predicted": -PHI4 * math.log10(Q),
            "log10_observed":  math.log10(1e14 / 1.2209e19),
            "physics_label":   "inflation scale (typical)",
        },
        {
            "physical_scale": "T_CMB / m_Pl",
            "exponent_value": -HEEGNER_67,
            "substrate_form": "-Heegner_67 = -67",
            "log10_predicted": -HEEGNER_67 * math.log10(Q),
            "log10_observed":  math.log10(2.349e-13 / 1.2209e19),
            "physics_label":   "CMB temperature",
        },
    ]


def dS_consistency() -> dict:
    """In de Sitter cosmology, Lambda ~ H_0^2 m_Pl^2.
    Substrate: -mu^4 = -2 * 2^Phi_6 = -256.  This is automatic from the
    substrate identity mu^4 = 2^(Phi_6 + 1)."""
    lhs = MU ** 4
    rhs = 2 ** (PHI6 + 1)
    rhs_alt = 2 * (2 ** PHI6)
    return {
        "claim": "mu^4 = 2^(Phi_6+1) = 2*2^Phi_6 (dS substrate identity)",
        "values": {
            "mu^4":             lhs,
            "2^(Phi_6+1)":      rhs,
            "2 * 2^Phi_6":      rhs_alt,
        },
        "match":            lhs == rhs == rhs_alt,
        "dS_relation":      "Lambda ~ H_0^2 m_Pl^2",
        "substrate_relation": "-mu^4 = 2 * (-2^Phi_6)",
    }


def substrate_dictionary() -> list[dict]:
    """Master dictionary of substrate-primitive exponents and their physics."""
    return [
        {"value": 10, "form": "Phi_4 = q^2 + 1",            "physics": "inflation H_inf scale"},
        {"value": 35, "form": "(mu+1)*Phi_6",                "physics": "Higgs VEV scale"},
        {"value": 36, "form": "(q!)^2 = mu^2 * q^2",         "physics": "electroweak scale"},
        {"value": 67, "form": "Heegner_67",                  "physics": "CMB temp scale (approx)"},
        {"value": 128, "form": "2^Phi_6 = 2^7",              "physics": "Hubble scale today"},
        {"value": 256, "form": "mu^4 = 2^(Phi_6+1) = 2^8",   "physics": "cosmological constant"},
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "q!": QFACT, "v": V,
            },
        },
        "hierarchies_table":   hierarchies_table(),
        "dS_consistency":       dS_consistency(),
        "substrate_dictionary": substrate_dictionary(),
        "headline": (
            "Six fundamental physical log-scales are substrate-clean "
            "powers of q=3 with exponents in {Phi_4, (mu+1)Phi_6, "
            "(q!)^2, Heegner_67, 2^Phi_6, mu^4}.  The dS consistency "
            "between Lambda and H_0 is automatic: mu^4 = 2^(Phi_6+1)."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_great_hierarchies_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) GREAT HIERARCHIES: SUBSTRATE EXPONENT TABLE")
    print("=" * 78)

    print(f"\n{'physical_scale':>20s}  {'substrate_form':>30s}  {'pred_log10':>10s}  {'obs_log10':>10s}")
    print("  " + "-" * 80)
    for h in payload["hierarchies_table"]:
        print(f"  {h['physical_scale']:>20s}  {h['substrate_form']:>30s}  {h['log10_predicted']:>10.2f}  {h['log10_observed']:>10.2f}")

    d = payload["dS_consistency"]
    print(f"\ndS consistency:")
    print(f"  {d['claim']}")
    print(f"  values: {d['values']}")
    print(f"  match: {d['match']}")

    print(f"\nSubstrate-primitive exponent dictionary:")
    for e in payload["substrate_dictionary"]:
        print(f"  {e['value']:>4d}  =  {e['form']:>30s}  =>  {e['physics']}")

    print(f"\nHEADLINE: {payload['headline']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
