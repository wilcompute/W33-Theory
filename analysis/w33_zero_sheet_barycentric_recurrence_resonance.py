"""Recurrence/resonance analysis for zero-sheet barycentric dispersion data.

This script packages the MCXXIX finite theorem layer extracted from the
MCXXVIII barycentric dispersion-turning ladder.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet,
)


def main() -> None:
    prime_limit = 10**5
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    packet = completed_defect_spectral_boundary_barycentric_recurrence_resonance_packet(
        prime_limit,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric recurrence-resonance law",
        "prime_limit": prime_limit,
        "s_values": s_values,
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_recurrence_resonance.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "shared_resonance_s": packet["shared_resonance_s"],
        "entropy_peak_s": packet["entropy_peak_s"],
        "concentration_trough_s": packet["concentration_trough_s"],
        "entropy_dominant_nonzero_harmonic_index": packet["entropy_harmonics"]["dominant_nonzero_harmonic_index"],
        "concentration_dominant_nonzero_harmonic_index": packet["concentration_harmonics"]["dominant_nonzero_harmonic_index"],
        "entropy_first_harmonic_ratio": packet["entropy_harmonics"]["normalized_dft_abs"][1],
        "concentration_first_harmonic_ratio": packet["concentration_harmonics"]["normalized_dft_abs"][1],
        "entropy_recurrence_coefficients": packet["entropy_recurrence"]["coefficients"],
        "concentration_recurrence_coefficients": packet["concentration_recurrence"]["coefficients"],
        "entropy_max_abs_residual": packet["entropy_recurrence"]["max_abs_residual"],
        "concentration_max_abs_residual": packet["concentration_recurrence"]["max_abs_residual"],
    }
    result_path = ROOT / "PART_MCXXIX_zero_sheet_barycentric_recurrence_resonance_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXIX Zero-Sheet Barycentric Recurrence-Resonance Law ===")
    print(
        f"shared_resonance_s={packet['shared_resonance_s']}, "
        f"entropy_harmonic={packet['entropy_harmonics']['dominant_nonzero_harmonic_index']}, "
        f"concentration_harmonic={packet['concentration_harmonics']['dominant_nonzero_harmonic_index']}, "
        f"entropy_recurrence={packet['entropy_recurrence']['coefficients']}, "
        f"concentration_recurrence={packet['concentration_recurrence']['coefficients']}"
    )


if __name__ == "__main__":
    main()