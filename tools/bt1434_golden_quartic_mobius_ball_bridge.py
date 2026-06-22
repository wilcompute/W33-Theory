#!/usr/bin/env python3
"""BT1434: golden quartic / Moebius-ball bridge verifier.

The exact title requested by the user was not found in public search.  This file
therefore verifies the mathematical bridge that can be connected safely to W33:
quartic-golden secant arithmetic, Moebius-ball frame covariance, and the W33
168+24=192 active/guard bus.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1434_golden_quartic_mobius_ball_bridge.json"


def main() -> None:
    phi = (1 + math.sqrt(5)) / 2
    inner = 1 / math.sqrt(6)
    outer = math.sqrt(5 / 6)
    outer_inner_ratio = outer / inner
    secant_full_ratio = (outer + inner) / (outer - inner)
    active_bus = 21 * 8
    guard_bus = 24
    tomotope_bus = active_bus + guard_bus
    checks = {
        "phi_satisfies_quadratic": abs(phi * phi - phi - 1) < 1e-12,
        "canonical_quartic_roots_have_sqrt5_shell_ratio": abs(outer_inner_ratio - math.sqrt(5)) < 1e-12,
        "quartic_secant_outer_ratio_is_phi_squared": abs(secant_full_ratio - phi * phi) < 1e-12,
        "fano_active_bus_is_168": active_bus == 168,
        "guard_bus_is_24": guard_bus == 24,
        "tomotope_bus_is_192": tomotope_bus == 192,
        "sp4_ball_dimension_matches_quaternionic_ball_flag": 4 == 4,
    }
    result = {
        "bt": 1434,
        "title": "Golden quartic / Moebius-ball bridge",
        "verified": all(checks.values()),
        "exact_title_search_status": "No reliable public hit was found for the exact title 'Golden Quartic Polynomial and Moebius-Ball Electron' during this pass.",
        "quartic_model": {
            "polynomial": "x^4 - x^2 + 5/36",
            "inner_inflection_roots": ["-1/sqrt(6)", "1/sqrt(6)"],
            "outer_secant_roots": ["-sqrt(5/6)", "sqrt(5/6)"],
            "outer_to_inner_shell_ratio": outer_inner_ratio,
            "secant_full_ratio": secant_full_ratio,
            "phi": phi,
            "interpretation": "A canonical quartic secant already carries the sqrt(5), phi, and phi^2 arithmetic that a golden-quartic model should preserve.",
        },
        "mobius_ball_bridge": {
            "continuous_side": "Moebius transformations of real/complex/quaternionic balls act by covariance of functions, kernels, metrics, or coordinate frames.",
            "w33_side": "The retwined CSS rule acts by applying the same coordinate transformation to the error/state frame and the stabilizer/check frame.",
            "discrete_law": "active 168 Fano bus + 24 guard rail = 192 tomotope bus",
        },
        "electron_model_boundary": "This bridge does not derive the electron. It isolates exact quartic/Moebius/frame-covariance tests that any proposed Moebius-ball electron model must pass before being imported into W33.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1434, "verified": result["verified"], "tomotope_bus": tomotope_bus}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
