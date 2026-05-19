"""Deformation cumulants and completed spectral action/free-energy package."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from w33.cyclotomic import (
    completed_defect_spectral_deformation_cumulant_profile,
    completed_defect_spectral_free_energy_profile,
)


def main() -> None:
    prime_limits = [31, 1000, 10000, 100000]
    s_values = [0.5, 1.0, 2.0]
    deformation_points = [0.0, 1.0]
    orders = [1, 2, 3, 4, 5]
    payload = {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformation_points": deformation_points,
        "orders": orders,
        "cumulant_profile": completed_defect_spectral_deformation_cumulant_profile(
            prime_limits, s_values, deformation_points, orders
        ),
        "free_energy_profile": completed_defect_spectral_free_energy_profile(
            prime_limits, s_values, deformation_points
        ),
    }

    data_path = Path("data") / "w33_completed_spectral_action_package.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result_path = Path("PART_MCVIII_completed_spectral_action_package_results.json")
    result_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Completed spectral action package generated.")
    sample = payload["free_energy_profile"]["1.0"]["1.0"][-1]
    print(
        "s=1.0, lambda=1.0, prime_limit="
        f"{sample['prime_limit']}, action={sample['action_real']} + {sample['action_imag']}i, "
        f"hessian={sample['hessian_real']} + {sample['hessian_imag']}i"
    )


if __name__ == "__main__":
    main()
