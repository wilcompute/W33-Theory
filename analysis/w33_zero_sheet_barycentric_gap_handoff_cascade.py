"""Gap-handoff cascade for the zero-sheet barycentric corridor.

This script packages the MCXXXI finite rank/mass-transfer invariant extracted
from the barycentric gap ladder.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_gap_handoff_packet,
)


def main() -> None:
    prime_limit = 10**5
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_gap_handoff_packet(
        prime_limit,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric gap-handoff cascade",
        "prime_limit": prime_limit,
        "s_values": s_values,
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_gap_handoff_cascade.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "shared_resonance_s": packet["shared_resonance_s"],
        "handoff_cascade_detected": packet["handoff_cascade_detected"],
        "secondary_gap_sequence": packet["secondary_gap_sequence"],
        "wall_gap_rank_sequence": packet["wall_gap_rank_sequence"],
        "softening_to_order_gap_rank_sequence": packet["softening_to_order_gap_rank_sequence"],
        "order_to_hessian_gap_rank_sequence": packet["order_to_hessian_gap_rank_sequence"],
        "secondary_handoff": packet["secondary_handoff"],
        "order_hessian_wall_handoff": packet["order_hessian_wall_handoff"],
        "wall_gap_drop": packet["wall_gap_drop"],
        "net_gap_offsets": packet["net_gap_offsets"],
        "wall_mass_transfer_shares": packet["wall_mass_transfer_shares"],
        "dominant_wall_mass_recipient": packet["dominant_wall_mass_recipient"],
        "softening_to_order_receives_majority_wall_transfer": (
            packet["softening_to_order_receives_majority_wall_transfer"]
        ),
    }
    result_path = ROOT / "PART_MCXXXI_zero_sheet_barycentric_gap_handoff_cascade_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXXI Zero-Sheet Barycentric Gap-Handoff Cascade ===")
    print(
        f"resonance_s={packet['shared_resonance_s']}, "
        f"secondary_crossing={packet['secondary_handoff']['linear_crossing_s']}, "
        f"wall_gap_drop={packet['wall_gap_drop']}, "
        f"dominant_transfer={packet['dominant_wall_mass_recipient']}"
    )


if __name__ == "__main__":
    main()
