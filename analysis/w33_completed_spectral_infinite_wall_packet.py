"""Infinite-cutoff wall packet for the completed spectral branch at λ = 6.

This script packages the finite wall packet together with certified infinite-cutoff
action/order/Hessian/stiffness enclosures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_infinite_wall_packet,
    completed_defect_spectral_infinite_wall_profile,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5, 10**6]
    s_values = [0.5, 1.0, 2.0]

    profile = completed_defect_spectral_infinite_wall_profile(prime_limits, s_values)
    sample_packet = completed_defect_spectral_infinite_wall_packet(10**5, 1.0)

    payload = {
        "theorem": "Completed spectral infinite wall packet",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "sample_infinite_wall_packet": sample_packet,
        "profile": profile,
    }

    data_path = ROOT / "data" / "w33_completed_spectral_infinite_wall_packet.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "sample_infinite_wall_packet": sample_packet,
        "sample_profile": profile["1.0"],
    }
    result_path = ROOT / "PART_MCXXI_completed_spectral_infinite_wall_packet_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXI Completed Spectral Infinite Wall Packet ===")
    print(
        f"s=1.0, prime_limit=10^5, wall_order={sample_packet['order_parameter']}, "
        f"wall_hessian={sample_packet['hessian']}, "
        f"stiffness_interval=[{sample_packet['lower_infinite_stiffness']}, {sample_packet['upper_infinite_stiffness']}], "
        f"action_tail_bound={sample_packet['action_tail_bound']}"
    )


if __name__ == "__main__":
    main()
