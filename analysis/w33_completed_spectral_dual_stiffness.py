"""Completed spectral dual stiffness and reciprocal susceptibility.

This script packages the Legendre-dual curvature of the completed spectral action,
both at finite cutoff and in the infinite-cutoff limit with certified enclosures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_dual_stiffness,
    completed_defect_spectral_infinite_dual_stiffness_interval,
    completed_defect_spectral_infinite_dual_stiffness_profile,
    completed_defect_spectral_order_parameter_real_global,
)


def main() -> None:
    reference_prime_limit = 10**3
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]
    deformations = [1.0, 2.0]

    profile = completed_defect_spectral_infinite_dual_stiffness_profile(
        reference_prime_limit,
        prime_limits,
        s_values,
        deformations,
    )

    sample_target = completed_defect_spectral_order_parameter_real_global(reference_prime_limit, 1.0, 1.0)
    sample_packet = completed_defect_spectral_dual_stiffness(10**5, 1.0, sample_target, deformation_max=1.0)
    sample_interval = completed_defect_spectral_infinite_dual_stiffness_interval(10**5, 1.0, sample_target, deformation_max=1.0)

    payload = {
        "theorem": "Completed spectral dual stiffness and reciprocal susceptibility",
        "reference_prime_limit": reference_prime_limit,
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_target_order_parameter": sample_target,
        "sample_dual_stiffness_packet": sample_packet,
        "sample_infinite_stiffness_interval": sample_interval,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_dual_stiffness.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_target_order_parameter": sample_target,
        "sample_dual_stiffness_packet": sample_packet,
        "sample_infinite_stiffness_interval": sample_interval,
    }
    result_path = ROOT / "PART_MCXIII_completed_spectral_dual_stiffness_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXIII Completed Spectral Dual Stiffness ===")
    print(
        f"target_order={sample_target}, recovered_lambda={sample_packet['deformation']}, "
        f"stiffness={sample_packet['stiffness']}, "
        f"interval=[{sample_interval['lower_stiffness']}, {sample_interval['upper_stiffness']}], "
        f"width={sample_interval['stiffness_interval_width']}"
    )


if __name__ == "__main__":
    main()