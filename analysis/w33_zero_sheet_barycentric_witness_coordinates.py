"""Barycentric coordinates of the zero-sheet mean-density witness ladder.

This script normalizes the MCXXIV deformation witnesses by the exact zero-sheet
corridor width, b = (lambda - 4) / 2, and records the resulting scale-free
coordinate gaps.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_witness_packet,
    completed_defect_spectral_boundary_barycentric_witness_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    profile = completed_defect_spectral_boundary_barycentric_witness_profile(prime_limits, s_values, subintervals=80)
    sample_packet = completed_defect_spectral_boundary_barycentric_witness_packet(10**5, 1.0, subintervals=80)

    payload = {
        "theorem": "Zero-sheet barycentric witness coordinates",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_barycentric_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_witness_coordinates.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_barycentric_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXXV_zero_sheet_barycentric_witness_coordinates_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXV Zero-Sheet Barycentric Witness Coordinates ===")
    print(
        f"s=1.0, prime_limit=10^5, "
        f"soft_b={sample_packet['dual_softening_barycentric_coordinate']}, "
        f"order_b={sample_packet['order_barycentric_coordinate']}, "
        f"hessian_b={sample_packet['hessian_barycentric_coordinate']}, "
        f"third_b={sample_packet['third_derivative_barycentric_coordinate']}, "
        f"gap_sum={sample_packet['barycentric_gap_sum']}"
    )


if __name__ == "__main__":
    main()
