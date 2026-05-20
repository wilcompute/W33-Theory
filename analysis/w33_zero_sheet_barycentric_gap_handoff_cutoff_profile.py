"""Cutoff-robustness profile for the zero-sheet barycentric gap handoff cascade."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_gap_handoff_cutoff_profile,
)


def main() -> None:
    prime_limits = [1000, 10000, 100000]
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_gap_handoff_cutoff_profile(
        prime_limits,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric gap-handoff cutoff robustness",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_gap_handoff_cutoff_profile.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "shared_resonance_all_equal": packet["shared_resonance_all_equal"],
        "cascade_all_detected": packet["cascade_all_detected"],
        "wall_gap_drop_reference": packet["wall_gap_drop_reference"],
        "wall_gap_drop_max_deviation": packet["wall_gap_drop_max_deviation"],
        "secondary_crossing_reference": packet["secondary_crossing_reference"],
        "secondary_crossing_max_deviation": packet["secondary_crossing_max_deviation"],
        "dominant_recipient_all_equal": packet["dominant_recipient_all_equal"],
        "majority_transfer_all": packet["majority_transfer_all"],
        "per_cutoff": packet["per_cutoff"],
    }
    result_path = ROOT / "PART_MCXXXII_zero_sheet_barycentric_gap_handoff_cutoff_robustness_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXXII Zero-Sheet Barycentric Gap-Handoff Cutoff Robustness ===")
    print(
        f"shared_resonance_all_equal={packet['shared_resonance_all_equal']}, "
        f"cascade_all_detected={packet['cascade_all_detected']}, "
        f"wall_gap_drop_max_deviation={packet['wall_gap_drop_max_deviation']}, "
        f"secondary_crossing_max_deviation={packet['secondary_crossing_max_deviation']}"
    )


if __name__ == "__main__":
    main()