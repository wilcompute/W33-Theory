"""Zero-sheet interior-to-wall transfer law for the completed spectral branch.

This script packages the exact transfer identities between the canonical interior packet
at λ = 4 and the wall packet at λ = 6.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_transfer_packet,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    profile = {
        str(s): [completed_defect_spectral_boundary_transfer_packet(prime_limit, s, subintervals=120) for prime_limit in prime_limits]
        for s in s_values
    }
    sample_packet = completed_defect_spectral_boundary_transfer_packet(10**4, 1.0, subintervals=160)

    payload = {
        "theorem": "Zero-sheet boundary transfer law",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_transfer_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_boundary_transfer_law.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_transfer_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXX_zero_sheet_boundary_transfer_law_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXX Zero-Sheet Boundary Transfer Law ===")
    print(
        f"s=1.0, prime_limit=10^4, delta_order={sample_packet['delta_order_parameter']}, "
        f"delta_stiffness={sample_packet['delta_stiffness']}, "
        f"order_transfer_error={sample_packet['order_transfer_error']}"
    )


if __name__ == "__main__":
    main()
