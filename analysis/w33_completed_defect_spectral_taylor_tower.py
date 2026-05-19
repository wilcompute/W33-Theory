"""Odd Taylor tower and radius-six analyticity for the completed defect spectral L-family."""

from __future__ import annotations

import json
from pathlib import Path

from w33.cyclotomic import (
    completed_defect_spectral_log_odd_coefficient,
    completed_defect_spectral_series_profile,
    completed_defect_spectral_uniform_radius_lower_bound,
)


def main() -> None:
    prime_limits = [31, 1000, 10000, 100000]
    s_values = [0.5, 1.0, 2.0]
    deformations = [0.5, 1.0]
    max_orders = [1, 3, 5, 7, 9]
    sample_prime_limit = 100000
    sample_s = 1.0
    sample_coefficients = {}
    for order in max_orders:
        coeff = completed_defect_spectral_log_odd_coefficient(sample_prime_limit, sample_s, order)
        sample_coefficients[str(order)] = {
            "real": coeff.real,
            "imag": coeff.imag,
        }

    payload = {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "max_orders": max_orders,
        "uniform_radius_lower_bound": completed_defect_spectral_uniform_radius_lower_bound(),
        "sample_prime_limit": sample_prime_limit,
        "sample_s": sample_s,
        "sample_coefficients": sample_coefficients,
        "profile": completed_defect_spectral_series_profile(prime_limits, s_values, deformations, max_orders),
    }

    data_path = Path("data") / "w33_completed_defect_spectral_taylor_tower.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result_path = Path("PART_MCVI_completed_defect_spectral_taylor_tower_results.json")
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Completed defect spectral Taylor tower generated.")
    print(f"Uniform radius lower bound on the positive real s-axis: {payload['uniform_radius_lower_bound']}")
    print(f"Sample λ^1 coefficient at s={sample_s}, X={sample_prime_limit}: {sample_coefficients['1']['real']} + {sample_coefficients['1']['imag']}i")
    print(f"Sample λ^3 coefficient at s={sample_s}, X={sample_prime_limit}: {sample_coefficients['3']['real']} + {sample_coefficients['3']['imag']}i")


if __name__ == "__main__":
    main()
