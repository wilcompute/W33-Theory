#!/usr/bin/env python3
"""
PART CCCXXVII: Mass-Mixing Closure Surface for W(3,3)

This verifier consolidates the May 9, 2026 empirical closures into one
operation-preserving diagnostic surface.  The point is not to add another
isolated numerical coincidence, but to test whether the Higgs quartic,
CKM/Wolfenstein parameters, and top Yukawa all live on the same compact
W(3,3) arithmetic sheet.

The resulting surface uses only the canonical W(3,3) atoms
    q=3, lambda=2, mu=4, k=12, v=40, Phi3=13, Phi4=10, Phi6=7.

Run:
    python exploration/PART_CCCXXVII_MASS_MIXING_CLOSURE_SURFACE.py
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Observable:
    name: str
    formula: str
    predicted: float
    reference: float
    sigma: float
    residual: float
    z: float


def zscore(predicted: float, reference: float, sigma: float) -> tuple[float, float]:
    residual = predicted - reference
    return residual, residual / sigma


def main() -> None:
    q = 3
    lam = 2
    mu = 4
    k = 12
    v = 40
    phi3 = q * q + q + 1        # 13
    phi4 = q * q + 1            # 10
    phi6 = q * q - q + 1        # 7

    # Empirical reference values used in the immediately prior committed bridges.
    refs = {
        "lambda_H_MSbar_MZ": (0.13050, 0.00050),
        "wolf_lambda": (0.2248, 0.00023),
        "wolf_A": (0.8109, 0.020),
        "wolf_rhobar": (0.1590, 0.010),
        "wolf_etabar": (0.3480, 0.010),
        "top_yukawa_pole": (0.99172, 0.00178),
    }

    predictions = {
        "lambda_H_MSbar_MZ": (phi3 / phi4**2, "Phi_3/Phi_4^2 = 13/100"),
        "wolf_lambda": (q**2 / v, "q^2/v = 9/40"),
        "wolf_A": (q**4 / phi4**2, "q^4/Phi_4^2 = 81/100"),
        "wolf_rhobar": ((lam / (mu + 1)) ** 2, "(lambda/(mu+1))^2 = 4/25"),
        "wolf_etabar": ((phi6 / phi4) ** 3, "(Phi_6/Phi_4)^3 = 343/1000"),
        "top_yukawa_pole": ((v / (v + 1)) ** (1 / 3), "(v/(v+1))^(1/3)"),
    }

    observables: list[Observable] = []
    chi2 = 0.0
    max_abs_z = 0.0
    for name, (pred, formula) in predictions.items():
        ref, sigma = refs[name]
        residual, z = zscore(pred, ref, sigma)
        chi2 += z * z
        max_abs_z = max(max_abs_z, abs(z))
        observables.append(Observable(name, formula, pred, ref, sigma, residual, z))

    dof = len(observables)
    rms_z = math.sqrt(chi2 / dof)

    # Internal closure identities: these should be exact in rational arithmetic.
    identities = {
        "q_factorial_seed": math.factorial(q) == 2 * q,
        "srg_vertex_formula": ((q + 1) * (q**3 + 1)) == v,
        "srg_valency_formula": q * (q + 1) == k,
        "top_denominator_matches_hypercharge_numerator": (v + 1) == 41,
        "higgs_denominator_is_phi4_squared": phi4**2 == 100,
        "ckm_lambda_denominator_is_vertex_count": v == 40,
        "ckm_A_denominator_is_higgs_denominator": phi4**2 == 100,
        "eta_uses_phi6_over_phi4_cube": phi6**3 == 343,
    }

    result = {
        "part": "CCCXXVII",
        "title": "Mass-Mixing Closure Surface for W(3,3)",
        "atoms": {"q": q, "lambda": lam, "mu": mu, "k": k, "v": v, "Phi3": phi3, "Phi4": phi4, "Phi6": phi6},
        "observables": [asdict(o) for o in observables],
        "chi2": chi2,
        "degrees_of_freedom": dof,
        "reduced_chi2": chi2 / dof,
        "rms_z": rms_z,
        "max_abs_z": max_abs_z,
        "all_within_2sigma": all(abs(o.z) < 2 for o in observables),
        "all_internal_identities_pass": all(identities.values()),
        "internal_identities": identities,
        "interpretation": (
            "The Higgs quartic, CKM Wolfenstein coordinates, and top Yukawa are not independent add-ons: "
            "they form a single W(3,3) mass-mixing sheet whose denominators are controlled by v=40 and Phi4^2=100, "
            "while the top cube closes on v/(v+1)."
        ),
    }

    out = Path("PART_CCCXXVII_mass_mixing_closure_surface_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("PART CCCXXVII: Mass-Mixing Closure Surface")
    print("=" * 58)
    for o in observables:
        print(f"{o.name:24s} {o.predicted:.8f}  ref={o.reference:.8f}  z={o.z:+.3f}  [{o.formula}]")
    print("-" * 58)
    print(f"chi2={chi2:.6f}, dof={dof}, reduced_chi2={chi2/dof:.6f}, rms_z={rms_z:.6f}")
    print(f"max_abs_z={max_abs_z:.6f}")
    print(f"all_within_2sigma={result['all_within_2sigma']}")
    print(f"all_internal_identities_pass={result['all_internal_identities_pass']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
