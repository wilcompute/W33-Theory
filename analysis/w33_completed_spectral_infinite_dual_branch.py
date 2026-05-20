"""Infinite-cutoff completed spectral equation-of-state branch.

This script packages the monotone convergence of finite-cutoff inverse branches toward the
infinite-cutoff equation of state, together with certified inverse enclosures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_infinite_dual_branch_profile,
    completed_defect_spectral_infinite_equation_of_state_interval,
    completed_defect_spectral_order_parameter_real_global,
)


def main() -> None:
    reference_prime_limit = 10**3
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]
    deformations = [1.0, 2.0]

    profile = completed_defect_spectral_infinite_dual_branch_profile(
        reference_prime_limit,
        prime_limits,
        s_values,
        deformations,
    )

    sample_target = completed_defect_spectral_order_parameter_real_global(reference_prime_limit, 1.0, 1.0)
    sample_interval = completed_defect_spectral_infinite_equation_of_state_interval(10**5, 1.0, sample_target)

    payload = {
        "theorem": "Infinite-cutoff spectral equation of state and dual branch limit",
        "reference_prime_limit": reference_prime_limit,
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_target_order_parameter": sample_target,
        "sample_interval": sample_interval,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_infinite_dual_branch.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_target_order_parameter": sample_target,
        "sample_interval": sample_interval,
        "sample_profile": profile["1.0"]["1.0"]["rows"],
    }
    result_path = ROOT / "PART_MCXII_completed_spectral_infinite_dual_branch_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    last = profile["1.0"]["1.0"]["rows"][-1]
    print("=== MCXII Infinite-Cutoff Spectral Dual Branch ===")
    print(
        f"target_order={sample_target}, recovered_lambda={last['recovered_lambda']}, "
        f"interval=[{last['interval_lower_lambda']}, {last['interval_upper_lambda']}], width={last['interval_width']}"
    )


if __name__ == "__main__":
    main()
