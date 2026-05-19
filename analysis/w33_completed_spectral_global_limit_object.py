"""Standalone infinite-cutoff completed spectral L-limit profile.

This script packages the MCVII/MCVIII spectral family into a genuine infinite-cutoff
analytic object by certifying explicit finite-cutoff log/value error bounds on compact
lambda-disks inside |lambda| < 6.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_global_limit_profile,
    completed_defect_spectral_log_compact_tail_bound,
    completed_defect_spectral_relative_error_bound,
    completed_defect_spectral_uniform_radius_lower_bound,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5, 10**6]
    s_values = [0.5, 1.0, 2.0]
    deformations = [1.0, 2.0, 5.0]

    profile = completed_defect_spectral_global_limit_profile(prime_limits, s_values, deformations)

    sample_rows = {
        "s=1.0,lambda=1.0": profile["1.0"]["1.0"][-1],
        "s=1.0,lambda=2.0": profile["1.0"]["2.0"][-1],
        "s=2.0,lambda=1.0": profile["2.0"]["1.0"][-1],
    }

    payload = {
        "theorem": "Standalone infinite-cutoff completed spectral L-limit",
        "uniform_radius_lower_bound": completed_defect_spectral_uniform_radius_lower_bound(),
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_log_tail_bounds": {
            "rho=1,X=10^6": completed_defect_spectral_log_compact_tail_bound(10**6, 1.0),
            "rho=2,X=10^6": completed_defect_spectral_log_compact_tail_bound(10**6, 2.0),
            "rho=5,X=10^6": completed_defect_spectral_log_compact_tail_bound(10**6, 5.0),
        },
        "sample_relative_error_bounds": {
            "rho=1,X=10^6": completed_defect_spectral_relative_error_bound(10**6, 1.0),
            "rho=2,X=10^6": completed_defect_spectral_relative_error_bound(10**6, 2.0),
            "rho=5,X=10^6": completed_defect_spectral_relative_error_bound(10**6, 5.0),
        },
        "sample_rows": sample_rows,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_global_limit_object.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "uniform_radius_lower_bound": payload["uniform_radius_lower_bound"],
        "sample_log_tail_bounds": payload["sample_log_tail_bounds"],
        "sample_relative_error_bounds": payload["sample_relative_error_bounds"],
        "sample_rows": sample_rows,
    }
    result_path = ROOT / "PART_MCIX_completed_spectral_global_limit_object_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    sample = sample_rows["s=1.0,lambda=1.0"]
    print("=== MCVIX Standalone Global Completed Spectral L-Limit ===")
    print(f"uniform radius lower bound = {payload['uniform_radius_lower_bound']}")
    print(
        "s=1.0, lambda=1.0, prime_limit=10^6, "
        f"log={sample['log_real']} + {sample['log_imag']}i, "
        f"tail_bound={sample['log_tail_bound']}, "
        f"relative_error_bound={sample['relative_value_error_bound']}"
    )


if __name__ == "__main__":
    main()
