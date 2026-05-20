"""Mean-density witness ladder inside the zero-sheet corridor.

This script selects finite deformation witnesses where the order, Hessian, third
derivative, and dual-softening density equal their corridor averages on [4, 6].
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_mean_witness_packet,
    completed_defect_spectral_boundary_mean_witness_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    profile = completed_defect_spectral_boundary_mean_witness_profile(prime_limits, s_values, subintervals=80)
    sample_packet = completed_defect_spectral_boundary_mean_witness_packet(10**5, 1.0, subintervals=80)

    payload = {
        "theorem": "Zero-sheet mean-density witness ladder",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_mean_witness_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_mean_density_witness_ladder.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_mean_witness_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXXIV_zero_sheet_mean_density_witness_ladder_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXIV Zero-Sheet Mean-Density Witness Ladder ===")
    print(
        f"s=1.0, prime_limit=10^5, "
        f"dual_softening_lambda={sample_packet['dual_softening_mean_deformation']}, "
        f"order_lambda={sample_packet['order_mean_deformation']}, "
        f"hessian_lambda={sample_packet['hessian_mean_deformation']}, "
        f"third_lambda={sample_packet['third_derivative_mean_deformation']}"
    )


if __name__ == "__main__":
    main()
