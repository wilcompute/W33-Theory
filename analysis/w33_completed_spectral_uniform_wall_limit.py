"""Completed spectral uniform-wall limit on the positive real slice.

This script packages the finite thermodynamic wall packet at the uniform scale λ = 6,
showing that the completed spectral branch approaches that scale continuously from below.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_uniform_wall_packet,
    completed_defect_spectral_uniform_wall_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]
    deformations = [5.0, 5.5, 5.9, 5.99, 6.0]

    profile = completed_defect_spectral_uniform_wall_profile(prime_limits, s_values, deformations)
    sample_wall = completed_defect_spectral_uniform_wall_packet(10**5, 1.0)

    payload = {
        "theorem": "Completed spectral uniform-wall limit",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_wall_packet": sample_wall,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_uniform_wall_limit.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_wall_packet": sample_wall,
        "sample_wall_profile": [profile["1.0"][key][-1] for key in ["5.0", "5.5", "5.9", "5.99", "6.0"]],
    }
    result_path = ROOT / "PART_MCXV_completed_spectral_uniform_wall_limit_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXV Completed Spectral Uniform-Wall Limit ===")
    print(
        f"s=1.0, prime_limit=10^5, wall_order={sample_wall['order_parameter']}, "
        f"wall_hessian={sample_wall['hessian']}, wall_stiffness={sample_wall['stiffness']}"
    )


if __name__ == "__main__":
    main()