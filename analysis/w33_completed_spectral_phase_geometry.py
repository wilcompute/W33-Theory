"""Completed spectral phase geometry on the real deformation slice.

This script packages the order parameter and Hessian of the completed spectral action
into a monotone, positive, infinite-cutoff profile with certified tail bounds.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_phase_geometry_profile,
    completed_defect_spectral_order_parameter_tail_bound,
    completed_defect_spectral_hessian_tail_bound,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5, 10**6]
    s_values = [0.5, 1.0, 2.0]
    deformations = [0.0, 1.0, 2.0, 5.0]

    profile = completed_defect_spectral_phase_geometry_profile(prime_limits, s_values, deformations)

    payload = {
        "theorem": "Completed spectral phase geometry and no-critical-point branch",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_tail_bounds": {
            "order_lambda1_X1e6": completed_defect_spectral_order_parameter_tail_bound(10**6, 1.0),
            "hessian_lambda1_X1e6": completed_defect_spectral_hessian_tail_bound(10**6, 1.0),
            "order_lambda2_X1e6": completed_defect_spectral_order_parameter_tail_bound(10**6, 2.0),
            "hessian_lambda2_X1e6": completed_defect_spectral_hessian_tail_bound(10**6, 2.0),
        },
        "sample_rows": {
            "s=1.0,lambda=1.0": profile["1.0"]["1.0"][-1],
            "s=1.0,lambda=2.0": profile["1.0"]["2.0"][-1],
            "s=2.0,lambda=1.0": profile["2.0"]["1.0"][-1],
        },
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_phase_geometry.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_tail_bounds": payload["sample_tail_bounds"],
        "sample_rows": payload["sample_rows"],
    }
    result_path = ROOT / "PART_MCX_completed_spectral_phase_geometry_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    row = payload["sample_rows"]["s=1.0,lambda=1.0"]
    print("=== MCX Completed Spectral Phase Geometry ===")
    print(
        "s=1.0, lambda=1.0, prime_limit=10^6, "
        f"order={row['order_parameter_real']}, hessian={row['hessian_real']}, "
        f"order_tail={row['order_tail_bound']}, hessian_tail={row['hessian_tail_bound']}"
    )


if __name__ == "__main__":
    main()
