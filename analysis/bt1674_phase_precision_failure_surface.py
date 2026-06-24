#!/usr/bin/env python3
"""BT1674 — phase-precision failure surface for candidate LCU projectors."""
from __future__ import annotations

import json
from pathlib import Path

POINTS = [
    ("block_encoded_best_4_2", 4, 2, 5.845219638242888),
    ("proxy_physical_8_8", 8, 8, 22793.067727163656),
    ("raw_l1_9_8", 9, 8, 98887.50411072331),
]
SIGMAS = [1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3]
TOLERANCES = [1e-2, 1e-3, 1e-4]


def main() -> None:
    points = []
    for name, dc, dm, kappa in POINTS:
        thresholds = {str(tol): tol / kappa for tol in TOLERANCES}
        sweep = []
        for sigma in SIGMAS:
            err = kappa * sigma
            sweep.append({"phase_rms": sigma, "linear_error_proxy": err, "passes_1e_minus_2": err <= 1e-2})
        points.append(
            {
                "name": name,
                "clock_degree": dc,
                "matter_degree": dm,
                "calibration_sensitivity": kappa,
                "max_phase_rms_by_error_tolerance": thresholds,
                "pass_count_for_1e_minus_2_over_grid": sum(1 for row in sweep if row["passes_1e_minus_2"]),
                "sweep": sweep,
            }
        )
    result = {
        "theorem": "BT1674 Phase-Precision Failure Surface",
        "model": "linearized projector error <= kappa * phase_rms",
        "phase_rms_grid": SIGMAS,
        "points": points,
        "interpretation": "After BT1673 normalization, the shallow (4,2) projector is vastly more phase-tolerant than the high-degree (8,8) and (9,8) projectors.",
        "boundary": "This is a first-order sensitivity surface. A full optical simulation should replace kappa*sigma with sampled phase errors through the compiled interferometer."
    }
    assert points[0]["pass_count_for_1e_minus_2_over_grid"] == 11
    assert points[1]["pass_count_for_1e_minus_2_over_grid"] == 4
    assert points[2]["pass_count_for_1e_minus_2_over_grid"] == 3
    out = Path("data/PART_BT1674_PHASE_PRECISION_FAILURE_SURFACE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
