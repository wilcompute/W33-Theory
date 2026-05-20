"""Wallward flow of barycentric witness coordinates on the zero-sheet corridor.

This script packages a finite s-ladder and tracks how the barycentric witness
coordinates shift toward the wall across the ladder.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_wallward_flow_packet,
)


def main() -> None:
    prime_limit = 10**5
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_wallward_flow_packet(
        prime_limit,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric wallward flow",
        "prime_limit": prime_limit,
        "s_values": s_values,
        "packet": packet,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_wallward_flow.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "all_coordinate_jumps_positive": packet["all_coordinate_jumps_positive"],
        "all_wall_gap_jumps_negative": packet["all_wall_gap_jumps_negative"],
        "dual_softening_midpoint_crossing_interval": packet["dual_softening_midpoint_crossing_interval"],
        "coordinate_offsets": packet["coordinate_offsets"],
        "wall_gap_drop": packet["wall_gap_drop"],
    }
    result_path = ROOT / "PART_MCXXVII_zero_sheet_barycentric_wallward_flow_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXVII Zero-Sheet Barycentric Wallward Flow ===")
    print(
        f"all_coordinate_jumps_positive={packet['all_coordinate_jumps_positive']}, "
        f"all_wall_gap_jumps_negative={packet['all_wall_gap_jumps_negative']}, "
        f"midpoint_crossing={packet['dual_softening_midpoint_crossing_interval']}, "
        f"wall_gap_drop={packet['wall_gap_drop']}"
    )


if __name__ == "__main__":
    main()
