"""Completed spectral equation of state and Legendre duality.

This script packages the real physical branch of the completed spectral action into
an invertible equation of state and its finite-cutoff Legendre dual description.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_equation_of_state_profile,
    completed_defect_spectral_legendre_dual,
    completed_defect_spectral_order_parameter_real_global,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]
    deformations = [1.0, 2.0]

    profile = completed_defect_spectral_equation_of_state_profile(prime_limits, s_values, deformations)
    sample_order = completed_defect_spectral_order_parameter_real_global(10**5, 1.0, 1.0)
    sample_dual = completed_defect_spectral_legendre_dual(10**5, 1.0, sample_order)

    payload = {
        "theorem": "Completed spectral equation of state and Legendre duality",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "deformations": deformations,
        "sample_order_parameter": sample_order,
        "sample_dual_packet": sample_dual,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_equation_of_state.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_order_parameter": payload["sample_order_parameter"],
        "sample_dual_packet": payload["sample_dual_packet"],
    }
    result_path = ROOT / "PART_MCXI_completed_spectral_equation_of_state_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXI Completed Spectral Equation of State ===")
    print(
        f"s=1.0, prime_limit=10^5, order_parameter={sample_order}, "
        f"recovered_lambda={sample_dual['deformation']}, dual={sample_dual['dual']}"
    )


if __name__ == "__main__":
    main()
