"""Characteristic-root phase split for the zero-sheet barycentric recurrences.

This script packages the characteristic roots of the MCXXIX entropy and
concentration order-two recurrence fits.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_recurrence_phase_packet,
)


def main() -> None:
    prime_limit = 10**5
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_recurrence_phase_packet(
        prime_limit,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric recurrence phase split",
        "prime_limit": prime_limit,
        "s_values": s_values,
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_recurrence_phase_split.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "shared_resonance_s": packet["shared_resonance_s"],
        "phase_split_detected": packet["phase_split_detected"],
        "entropy_phase": packet["entropy_phase"],
        "concentration_phase": packet["concentration_phase"],
        "entropy_damped_oscillatory": packet["entropy_damped_oscillatory"],
        "concentration_real_expanding_mode_detected": packet["concentration_real_expanding_mode_detected"],
    }
    result_path = ROOT / "PART_MCXXX_zero_sheet_barycentric_recurrence_phase_split_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXX Zero-Sheet Barycentric Recurrence Phase Split ===")
    print(
        f"entropy_phase={packet['entropy_phase']['phase_type']}, "
        f"entropy_radius={packet['entropy_phase']['spectral_radius']}, "
        f"concentration_phase={packet['concentration_phase']['phase_type']}, "
        f"concentration_radius={packet['concentration_phase']['spectral_radius']}"
    )


if __name__ == "__main__":
    main()
