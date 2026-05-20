"""Finite stability signature of the zero-sheet barycentric witness coordinates.

This script measures cutoff contraction of the barycentric witness coordinates and
the cross-s wallward shift between the sampled real slices.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_stability_packet,
)


def main() -> None:
    prime_limits = [10**3, 10**4, 10**5]
    s_values = [1.0, 2.0]

    stability_packet = completed_defect_spectral_boundary_barycentric_stability_packet(
        prime_limits,
        s_values,
        subintervals=40,
    )

    payload = {
        "theorem": "Zero-sheet barycentric stability signature",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "stability_packet": stability_packet,
    }

    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_stability_signature.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "minimum_finite_contraction_ratio": stability_packet["minimum_finite_contraction_ratio"],
        "per_s": stability_packet["per_s"],
        "cross_s_shift": stability_packet["cross_s_shift"],
    }
    result_path = ROOT / "PART_MCXXVI_zero_sheet_barycentric_stability_signature_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXVI Zero-Sheet Barycentric Stability Signature ===")
    print(
        f"minimum_finite_contraction_ratio={stability_packet['minimum_finite_contraction_ratio']}, "
        f"all_shift_wallward={stability_packet['cross_s_shift']['all_witnesses_shift_toward_wall']}, "
        f"offsets={stability_packet['cross_s_shift']['coordinate_offsets']}"
    )


if __name__ == "__main__":
    main()
