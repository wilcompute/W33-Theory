"""Boundary effective theory at the finite uniform wall packet λ = 6.

This script packages the exact first-order response coefficients of the positive-real
completed spectral branch in the wall variable ε = 6 - λ.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_wall_effective_packet,
    completed_defect_spectral_wall_effective_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]
    epsilons = [1e-1, 1e-2, 1e-3]

    profile = completed_defect_spectral_wall_effective_profile(prime_limits, s_values, epsilons)
    sample_packet = completed_defect_spectral_wall_effective_packet(10**5, 1.0)

    payload = {
        "theorem": "Completed spectral wall effective theory",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "epsilons": epsilons,
        "sample_wall_effective_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_wall_effective_theory.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_wall_effective_packet": sample_packet,
        "sample_profile": {str(eps): profile["1.0"][str(eps)][-1] for eps in epsilons},
    }
    result_path = ROOT / "PART_MCXIX_completed_spectral_wall_effective_theory_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXIX Completed Spectral Wall Effective Theory ===")
    print(
        f"s=1.0, prime_limit=10^5, wall_hessian={sample_packet['hessian']}, "
        f"third={sample_packet['third_derivative']}, "
        f"epsilon_stiffness_slope={sample_packet['epsilon_stiffness_slope']}"
    )


if __name__ == "__main__":
    main()