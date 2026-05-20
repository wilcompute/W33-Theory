"""Infinite-cutoff corridor from the zero-sheet interior packet to the wall packet.

This script packages the certified endpoint-delta intervals obtained by combining
the finite [4, 6] transfer law with the infinite-cutoff wall and compact interior
enclosures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_infinite_boundary_corridor_packet,
    completed_defect_spectral_infinite_boundary_corridor_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    profile = completed_defect_spectral_infinite_boundary_corridor_profile(prime_limits, s_values, subintervals=80)
    sample_packet = completed_defect_spectral_infinite_boundary_corridor_packet(10**5, 1.0, subintervals=80)

    payload = {
        "theorem": "Zero-sheet infinite boundary corridor",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_corridor_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_infinite_boundary_corridor.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_corridor_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXXII_zero_sheet_infinite_boundary_corridor_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXII Zero-Sheet Infinite Boundary Corridor ===")
    print(
        f"s=1.0, prime_limit=10^5, "
        f"delta_action_interval=[{sample_packet['infinite_delta_action_lower_bound']}, "
        f"{sample_packet['infinite_delta_action_upper_bound']}], "
        f"stiffness_loss_interval=[{sample_packet['infinite_stiffness_loss_lower_bound']}, "
        f"{sample_packet['infinite_stiffness_loss_upper_bound']}], "
        f"action_width={sample_packet['infinite_delta_action_interval_width']}"
    )


if __name__ == "__main__":
    main()
