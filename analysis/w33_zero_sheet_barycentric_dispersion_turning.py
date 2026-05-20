"""Finite dispersion-turning law for zero-sheet barycentric gap coordinates."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_dispersion_turning_packet,
)


def main() -> None:
    prime_limit = 10**5
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_dispersion_turning_packet(
        prime_limit,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric dispersion turning law",
        "prime_limit": prime_limit,
        "s_values": s_values,
        "packet": packet,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_dispersion_turning.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "entropy_peak_s": packet["entropy_peak_s"],
        "concentration_trough_s": packet["concentration_trough_s"],
        "entropy_sign_pattern": packet["entropy_sign_pattern"],
        "concentration_sign_pattern": packet["concentration_sign_pattern"],
        "dominant_gap_all_interior_to_softening": packet["dominant_gap_all_interior_to_softening"],
        "wall_gap_strictly_decreases": packet["wall_gap_strictly_decreases"],
    }

    result_path = ROOT / "PART_MCXXVIII_zero_sheet_barycentric_dispersion_turning_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXVIII Zero-Sheet Barycentric Dispersion Turning Law ===")
    print(
        f"entropy_peak_s={packet['entropy_peak_s']}, concentration_trough_s={packet['concentration_trough_s']}, "
        f"entropy_sign_pattern={packet['entropy_sign_pattern']}, concentration_sign_pattern={packet['concentration_sign_pattern']}"
    )


if __name__ == "__main__":
    main()
