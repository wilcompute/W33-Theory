#!/usr/bin/env python3
"""
PART CCCCXLII: Alpha--Mass--Mixing Constraint Web

This verifier continues from the latest master commits:
  - CCCCXLI: alpha^{-1} refined Gaussian identity
  - CCCXXIV/CCCXXV/CCCXXVI: Higgs, CKM/Wolfenstein, top Yukawa
  - CCCXXIX: charm Yukawa y_c = 1/137
  - CCCCXXXVIII/CCCCXXXIX: exceptional/triality and prime-tower synthesis

New point:
  The Higgs quartic, CKM A/lambda, top Yukawa cube, charm Yukawa, and
  refined electromagnetic coupling are not separate tables. They form a
  small exact constraint web over the same W(3,3) atoms.

The decisive eliminations are:
  1. A_CKM / lambda_H = q^4 / Phi_3 = 81/13.
  2. lambda_CKM * y_t^3 = q^2 / (v+1) = 9/41.
  3. A_CKM - lambda_H = (Phi_3 + mu)/(mu+1)^2 = 17/25.
  4. A_CKM + lambda_H = (v + Phi_6)/(lambda*(mu+1)^2) = 47/50.
  5. y_c^{-1} = |(k-1)+mu i|^2 = Phi_3*Phi_4 + Phi_6 = 137.
  6. alpha^{-1} - y_c^{-1} = v / M_eff = 880/24445.

Run:
    python exploration/PART_CCCCXLII_ALPHA_MASS_MIXING_CONSTRAINT_WEB.py
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class ExactIdentity:
    name: str
    left: str
    right: str
    value: str
    decimal: float
    passes: bool


def frac(num: int, den: int = 1) -> Fraction:
    return Fraction(num, den)


def identity(name: str, left: str, right: str, value: Fraction, expected: Fraction) -> ExactIdentity:
    return ExactIdentity(
        name=name,
        left=left,
        right=right,
        value=f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator),
        decimal=float(value),
        passes=(value == expected),
    )


def main() -> None:
    q = 3
    lam = 2
    mu = 4
    k = 12
    v = 40
    f = 24
    g = 15
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    lambda_H = frac(phi3, phi4**2)             # 13/100
    ckm_lambda = frac(q**2, v)                 # 9/40
    ckm_A = frac(q**4, phi4**2)                # 81/100
    rho_bar = frac(lam**2, (mu + 1) ** 2)      # 4/25
    eta_bar = frac(phi6**3, phi4**3)           # 343/1000
    top_yukawa_cubed = frac(v, v + 1)          # 40/41

    alpha_core = (k - 1) ** 2 + mu**2          # 137
    alpha_core_cyclotomic = phi3 * phi4 + phi6 # 137
    alpha_core_suzuki = q**q * (mu + 1) + lam  # 137
    alpha_core_alt = q**2 * g + lam            # 137
    y_c = frac(1, alpha_core)

    m_vac = (k - 1) * ((k - lam) ** 2 + 1)     # 1111
    delta_mass = frac(q, lam * (k - 1))        # 3/22
    m_eff = frac(m_vac, 1) + delta_mass        # 24445/22
    alpha_correction = frac(v, 1) / m_eff      # 880/24445
    alpha_inv_refined = frac(alpha_core, 1) + alpha_correction
    alpha_refined = frac(1, 1) / alpha_inv_refined

    exact_identities = [
        identity("A_over_lambdaH", "A_CKM/lambda_H", "q^4/Phi_3", ckm_A / lambda_H, frac(q**4, phi3)),
        identity("lambdaCKM_times_topcube", "lambda_CKM*y_t^3", "q^2/(v+1)", ckm_lambda * top_yukawa_cubed, frac(q**2, v + 1)),
        identity("A_minus_lambdaH", "A_CKM-lambda_H", "(Phi_3+mu)/(mu+1)^2", ckm_A - lambda_H, frac(phi3 + mu, (mu + 1) ** 2)),
        identity("A_plus_lambdaH", "A_CKM+lambda_H", "(v+Phi_6)/(lambda*(mu+1)^2)", ckm_A + lambda_H, frac(v + phi6, lam * (mu + 1) ** 2)),
        identity("rho_bar_definition", "rho_bar", "(lambda/(mu+1))^2", rho_bar, frac(lam**2, (mu + 1) ** 2)),
        identity("eta_bar_definition", "eta_bar", "(Phi_6/Phi_4)^3", eta_bar, frac(phi6**3, phi4**3)),
        identity("alpha_core_gaussian_equals_cyclotomic", "(k-1)^2+mu^2", "Phi_3*Phi_4+Phi_6", frac(alpha_core, 1), frac(alpha_core_cyclotomic, 1)),
        identity("alpha_core_gaussian_equals_suzuki", "(k-1)^2+mu^2", "q^q*(mu+1)+lambda", frac(alpha_core, 1), frac(alpha_core_suzuki, 1)),
        identity("alpha_core_gaussian_equals_alt", "(k-1)^2+mu^2", "q^2*g+lambda", frac(alpha_core, 1), frac(alpha_core_alt, 1)),
        identity("charm_inverse_equals_alpha_core", "1/y_c", "|(k-1)+mu*i|^2", frac(1, 1) / y_c, frac(alpha_core, 1)),
        identity("alpha_refined_slip_from_charm_inverse", "alpha_refined^{-1}-y_c^{-1}", "v/M_eff", alpha_inv_refined - frac(1, 1) / y_c, alpha_correction),
        identity("alpha_correction_expanded", "v/M_eff", "v*lambda*(k-1)/(lambda*(k-1)*M_vac+q)", alpha_correction, frac(v * lam * (k - 1), lam * (k - 1) * m_vac + q)),
    ]

    dashboard = {
        "lambda_H": float(lambda_H),
        "ckm_lambda": float(ckm_lambda),
        "ckm_A": float(ckm_A),
        "rho_bar": float(rho_bar),
        "eta_bar": float(eta_bar),
        "top_yukawa_cubed": float(top_yukawa_cubed),
        "top_yukawa": float(top_yukawa_cubed) ** (1.0 / 3.0),
        "y_c_core": float(y_c),
        "alpha_inv_core": float(alpha_core),
        "alpha_inv_refined": float(alpha_inv_refined),
        "alpha_refined": float(alpha_refined),
        "alpha_minus_yc": float(alpha_refined - y_c),
        "yc_over_alpha_minus_1": float((y_c / alpha_refined) - 1),
    }

    result = {
        "part": "CCCCXLII",
        "title": "Alpha--Mass--Mixing Constraint Web",
        "atoms": {"q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "f": f, "g": g, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6},
        "derived_quantities": {
            "lambda_H": str(lambda_H),
            "ckm_lambda": str(ckm_lambda),
            "ckm_A": str(ckm_A),
            "rho_bar": str(rho_bar),
            "eta_bar": str(eta_bar),
            "top_yukawa_cubed": str(top_yukawa_cubed),
            "alpha_core": alpha_core,
            "M_vac": m_vac,
            "Delta_M": str(delta_mass),
            "M_eff": str(m_eff),
            "alpha_correction": str(alpha_correction),
            "alpha_inv_refined": str(alpha_inv_refined),
        },
        "exact_identities": [asdict(x) for x in exact_identities],
        "all_exact_identities_pass": all(x.passes for x in exact_identities),
        "dashboard": dashboard,
        "interpretation": (
            "The refined electromagnetic coupling does not merely sit near the charm Yukawa; "
            "its integer core is exactly the inverse charm Yukawa, and the refined alpha correction "
            "is a W(3,3) finite-spectral slip v/M_eff. Simultaneously, Higgs and CKM share Phi4^2, "
            "and CKM lambda times the top-Yukawa cube collapses to q^2/(v+1)=9/41."
        ),
    }

    out = Path("PART_CCCCXLII_alpha_mass_mixing_constraint_web_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCCXLII: Alpha--Mass--Mixing Constraint Web")
    print("=" * 68)
    for item in exact_identities:
        status = "PASS" if item.passes else "FAIL"
        print(f"{status:4s} {item.name:42s} {item.left} = {item.value} = {item.right}")
    print("-" * 68)
    print(f"alpha_inv_refined = {float(alpha_inv_refined):.12f}")
    print(f"alpha_core        = {alpha_core}")
    print(f"alpha correction  = {alpha_correction} = {float(alpha_correction):.12f}")
    print(f"lambda_CKM*y_t^3 = {ckm_lambda * top_yukawa_cubed} = {float(ckm_lambda * top_yukawa_cubed):.12f}")
    print(f"A_CKM/lambda_H   = {ckm_A / lambda_H} = {float(ckm_A / lambda_H):.12f}")
    print(f"all_exact_identities_pass={result['all_exact_identities_pass']}")
    print(f"wrote {out}")

    assert result["all_exact_identities_pass"]
    assert math.isclose(float(alpha_inv_refined), 137.0359991818378, rel_tol=0.0, abs_tol=1e-12)
    assert ckm_lambda * top_yukawa_cubed == frac(9, 41)
    assert ckm_A / lambda_H == frac(81, 13)


if __name__ == "__main__":
    main()
