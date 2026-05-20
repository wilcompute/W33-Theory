"""Average-density packet for the zero-sheet infinite boundary corridor.

This script divides the certified infinite endpoint-delta corridor by the exact
zero-sheet interval width 6 - 4 = 2, producing average order, Hessian, third
derivative, dual-softening, and dual-delta-density enclosures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_infinite_boundary_average_packet,
    completed_defect_spectral_infinite_boundary_average_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    profile = completed_defect_spectral_infinite_boundary_average_profile(prime_limits, s_values, subintervals=80)
    sample_packet = completed_defect_spectral_infinite_boundary_average_packet(10**5, 1.0, subintervals=80)

    payload = {
        "theorem": "Zero-sheet infinite average-density corridor",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_average_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_infinite_average_density_corridor.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_average_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXXIII_zero_sheet_infinite_average_density_corridor_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXIII Zero-Sheet Infinite Average-Density Corridor ===")
    print(
        f"s=1.0, prime_limit=10^5, "
        f"average_order_interval=[{sample_packet['infinite_average_order_parameter_lower_bound']}, "
        f"{sample_packet['infinite_average_order_parameter_upper_bound']}], "
        f"average_dual_softening_interval=[{sample_packet['infinite_average_dual_softening_lower_bound']}, "
        f"{sample_packet['infinite_average_dual_softening_upper_bound']}], "
        f"corridor_width={sample_packet['corridor_width']}"
    )


if __name__ == "__main__":
    main()
