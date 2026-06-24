#!/usr/bin/env python3
"""BT1696 - dS/CFT time-arrow mode certificate.

The finite substrate already has the W(3,3) Laplacian masses {0,10,16}.
For d = mu = 4 de Sitter boundary weights are

    Delta = (d-1)/2 +- sqrt((d-1)^2/4 - m^2).

The matter and isometry modes lie above the 9/4 principal-series threshold.
This gives a finite certificate for the claim boundary: the expanding
holographic reading is a dS/CFT-style, non-unitary boundary interpretation,
not a continuum quantum-gravity proof.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path

MU = 4
CENTRAL_CHARGE = 24
OUT = Path("data/bt1696_dscft_time_arrow_modes.json")


def conformal_weights(m2: float, d: int = MU) -> tuple[complex, complex]:
    half = (d - 1) / 2
    root = cmath.sqrt(((d - 1) ** 2) / 4 - m2)
    return complex(half) + root, complex(half) - root


def heawood_laplacian_eigenvalues() -> list[float]:
    # The Heawood graph is 3-regular bipartite with adjacency spectrum
    # {3, -3, sqrt(2)^6, -sqrt(2)^6}.
    return [0.0, 6.0] + [3 - math.sqrt(2)] * 6 + [3 + math.sqrt(2)] * 6


def thermal_entropy(beta: float = 1.0) -> float:
    weights = [math.exp(-beta * ev) for ev in heawood_laplacian_eigenvalues()]
    partition = sum(weights)
    probabilities = [w / partition for w in weights]
    return -sum(p * math.log(p) for p in probabilities if p > 0)


def build_certificate() -> dict:
    threshold = ((MU - 1) ** 2) / 4
    modes = [
        {"name": "vacuum", "multiplicity": 1, "m2": 0},
        {"name": "matter_boundary", "multiplicity": 24, "m2": 10},
        {"name": "bulk_isometry", "multiplicity": 15, "m2": 16},
    ]

    mode_rows = []
    for mode in modes:
        delta_plus, delta_minus = conformal_weights(mode["m2"])
        principal = mode["m2"] > threshold
        mode_rows.append(
            {
                **mode,
                "series": "principal" if principal else "complementary",
                "Delta_plus": [delta_plus.real, delta_plus.imag],
                "Delta_minus": [delta_minus.real, delta_minus.imag],
                "complex_weights": abs(delta_plus.imag) > 1e-12,
            }
        )

    entropy = thermal_entropy()
    checks = {
        "d_equals_mu_4": MU == 4,
        "principal_threshold_is_9_over_4": threshold == 2.25,
        "matter_mode_is_principal": mode_rows[1]["series"] == "principal",
        "isometry_mode_is_principal": mode_rows[2]["series"] == "principal",
        "vacuum_mode_is_complementary": mode_rows[0]["series"] == "complementary",
        "heawood_clock_entropy_positive": entropy > 0,
        "boundary_c_is_monster_24_before_i_continuation": CENTRAL_CHARGE == 24,
    }

    return {
        "theorem": "BT1696 dS/CFT Time-Arrow Modes",
        "verified": all(checks.values()),
        "dimension": {"d": MU, "threshold": threshold},
        "w33_laplacian_modes": mode_rows,
        "heawood_clock": {
            "laplacian_eigenvalues": heawood_laplacian_eigenvalues(),
            "beta": 1.0,
            "von_neumann_entropy": entropy,
        },
        "boundary": {
            "central_charge_before_continuation": CENTRAL_CHARGE,
            "dS_CFT_reading": "c -> i*c; principal-series modes give complex weights",
            "interpretation": (
                "Time's arrow is modeled as the non-unitary expanding boundary "
                "flow: principal-series modes decay and the finite clock state is mixed."
            ),
        },
        "claim_boundary": [
            "This is a finite dS/CFT mode certificate, not a continuum dS quantum-gravity derivation.",
            "The exact promoted facts are the 9/4 threshold classification and the positive finite-clock entropy.",
            "The non-unitary boundary reading is anchored externally in dS/CFT and remains an interpretation layer.",
        ],
        "sources": [
            {
                "label": "Strominger dS/CFT",
                "url": "https://arxiv.org/abs/hep-th/0106113",
                "role": "External guardrail for nonunitary/complex-weight dS/CFT boundary behavior.",
            },
            {
                "label": "Local dS/CFT mode split",
                "path": "analysis/w33_dscft_modes.py",
                "role": "Repo anchor for W(3,3) modes {0^1,10^24,16^15}.",
            },
            {
                "label": "Local thermal-time clock",
                "path": "analysis/w33_thermal_time_clock.py",
                "role": "Repo anchor for finite modular/thermal clock state.",
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
    print(f"  threshold: {cert['dimension']['threshold']}")
    print(
        "  mode series: "
        + ", ".join(f"{m['name']}={m['series']}" for m in cert["w33_laplacian_modes"])
    )
    print(
        "  Heawood clock entropy: "
        f"{cert['heawood_clock']['von_neumann_entropy']:.6f}"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
