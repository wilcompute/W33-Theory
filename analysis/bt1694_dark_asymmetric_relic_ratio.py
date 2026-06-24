#!/usr/bin/env python3
"""BT1694 - asymmetric dark relic ratio.

This promotes the local dark-relic draft with a stricter boundary:

* a strongly coupled symmetric relic at the usual thermal cross section is
  tens of TeV, not tens of GeV;
* the hidden-SU(4) dark-hadron branch must therefore be interpreted as
  asymmetry dominated if it is kept at the E8/tens-of-GeV scale;
* the substrate abundance ratio is the exact rational 82/15.

The output is a finite certificate, not a direct-detection claim.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

V = 40
LAMBDA = 2
MU = 4
G_NEG = 15

SIGMA_V_RELIC_GEV2 = 2.57e-9  # roughly one picobarn in natural units
DARK_HADRON_REFERENCE_GEV = 22.8

OUT = Path("data/bt1694_dark_asymmetric_relic_ratio.json")


def build_certificate() -> dict:
    symmetric_mass = math.sqrt(math.pi / SIGMA_V_RELIC_GEV2)
    omega_dm = Fraction(MU, G_NEG)
    omega_b = Fraction(LAMBDA, V + 1)
    ratio = omega_dm / omega_b
    mass_ratio_equal_asymmetry = ratio

    checks = {
        "symmetric_relic_is_above_10_TeV": symmetric_mass > 10_000,
        "symmetric_relic_exceeds_tens_GeV_branch_by_1000x": (
            symmetric_mass / DARK_HADRON_REFERENCE_GEV > 1000
        ),
        "substrate_ratio_is_82_over_15": ratio == Fraction(82, 15),
        "ratio_lies_in_cosmic_coincidence_window": 5.0 < float(ratio) < 6.0,
    }

    return {
        "theorem": "BT1694 Dark Asymmetric Relic Ratio",
        "verified": all(checks.values()),
        "constants": {
            "v": V,
            "lambda": LAMBDA,
            "mu": MU,
            "g_negative_multiplicity": G_NEG,
            "thermal_relic_cross_section_GeV_minus_2": SIGMA_V_RELIC_GEV2,
            "dark_hadron_reference_GeV": DARK_HADRON_REFERENCE_GEV,
        },
        "symmetric_relic_check": {
            "formula": "m_sym = sqrt(pi / <sigma v>_thermal)",
            "mass_GeV": symmetric_mass,
            "mass_TeV": symmetric_mass / 1000,
            "ratio_to_reference_dark_hadron": symmetric_mass
            / DARK_HADRON_REFERENCE_GEV,
            "interpretation": (
                "The tens-of-GeV hidden-SU(4) hadron branch cannot be a "
                "strong symmetric thermal relic under this geometric estimate."
            ),
        },
        "abundance_ratio": {
            "Omega_DM": str(omega_dm),
            "Omega_b": str(omega_b),
            "Omega_DM_over_Omega_b": str(ratio),
            "Omega_DM_over_Omega_b_float": float(ratio),
            "equal_asymmetry_mass_ratio": str(mass_ratio_equal_asymmetry),
            "equal_asymmetry_dark_mass_GeV_if_mp_0_938": float(
                mass_ratio_equal_asymmetry
            )
            * 0.93827208816,
        },
        "claim_boundary": [
            "This is a branch-selection certificate: symmetric WIMP-like freeze-out is rejected for the tens-of-GeV hidden-SU(4) branch.",
            "The exact ratio 82/15 is a substrate abundance ratio; a detector cross section is not derived here.",
            "A heavier dark hadron remains possible if the dark asymmetry is correspondingly smaller than the baryon asymmetry.",
        ],
        "sources": [
            {
                "label": "Kaplan-Luty-Zurek asymmetric dark matter",
                "url": "https://arxiv.org/abs/0901.4117",
                "role": "External guardrail for abundance controlled by a dark/visible asymmetry.",
            },
            {
                "label": "Local hidden-SU(4) dark confinement branch",
                "path": "analysis/w33_dark_matter_mass.py",
                "role": "Repo anchor for the confining hidden-SU(4) branch.",
            },
            {
                "label": "Local dark Lambda estimate",
                "path": "analysis/w33_dark_lambda_gut.py",
                "role": "Repo anchor for the tens-of-GeV dark scale.",
            },
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")

    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(
        "  symmetric relic mass: "
        f"{cert['symmetric_relic_check']['mass_TeV']:.2f} TeV"
    )
    print("  Omega_DM/Omega_b: " f"{cert['abundance_ratio']['Omega_DM_over_Omega_b']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
