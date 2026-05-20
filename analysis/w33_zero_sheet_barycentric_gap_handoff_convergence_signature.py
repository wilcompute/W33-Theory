"""Directional convergence signature for the zero-sheet barycentric gap-handoff cutoff profile."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_boundary_barycentric_gap_handoff_convergence_signature,
)


def _build_from_profile_payload(profile_payload: dict[str, object], prime_limits: list[int], s_values: list[float]) -> dict[str, object]:
    rows = profile_payload["per_cutoff"]

    def _nondecreasing(values: list[float], tolerance: float = 0.0) -> bool:
        return all(values[index] <= values[index + 1] + tolerance for index in range(len(values) - 1))

    def _nonincreasing(values: list[float], tolerance: float = 0.0) -> bool:
        return all(values[index] + tolerance >= values[index + 1] for index in range(len(values) - 1))

    wall_gap_drop_sequence = [row["wall_gap_drop"] for row in rows]
    secondary_crossing_sequence = [row["secondary_handoff_linear_crossing_s"] for row in rows]
    order_hessian_crossing_sequence = [row["order_hessian_wall_linear_crossing_s"] for row in rows]
    softening_share_sequence = [row["wall_mass_transfer_shares"]["softening_to_order"] for row in rows]
    interior_share_sequence = [row["wall_mass_transfer_shares"]["interior_to_softening"] for row in rows]
    order_hessian_share_sequence = [row["wall_mass_transfer_shares"]["order_to_hessian"] for row in rows]
    hessian_third_share_sequence = [row["wall_mass_transfer_shares"]["hessian_to_third_derivative"] for row in rows]
    secondary_reference_abs_offsets = [
        abs(0.0 if row["from_reference_secondary_handoff_delta"] is None else row["from_reference_secondary_handoff_delta"])
        for row in rows
    ]
    wall_reference_abs_offsets = [abs(row["from_reference_wall_gap_drop_delta"]) for row in rows]

    directional_signature = {
        "wall_gap_drop_nondecreasing": _nondecreasing(wall_gap_drop_sequence, tolerance=1e-15),
        "secondary_crossing_nondecreasing": _nondecreasing(secondary_crossing_sequence, tolerance=1e-15),
        "order_hessian_crossing_nonincreasing": _nonincreasing(order_hessian_crossing_sequence, tolerance=1e-15),
        "softening_share_nonincreasing": _nonincreasing(softening_share_sequence, tolerance=1e-15),
        "interior_share_nondecreasing": _nondecreasing(interior_share_sequence, tolerance=1e-15),
        "order_hessian_share_nondecreasing": _nondecreasing(order_hessian_share_sequence, tolerance=1e-15),
        "hessian_third_share_nonincreasing": _nonincreasing(hessian_third_share_sequence, tolerance=1e-15),
        "secondary_reference_offset_nonincreasing": _nonincreasing(secondary_reference_abs_offsets, tolerance=1e-15),
        "wall_reference_offset_nonincreasing": _nonincreasing(wall_reference_abs_offsets, tolerance=1e-15),
    }

    return {
        "prime_limits": prime_limits,
        "s_values": s_values,
        "cutoff_profile": profile_payload,
        "wall_gap_drop_sequence": wall_gap_drop_sequence,
        "secondary_crossing_sequence": secondary_crossing_sequence,
        "order_hessian_crossing_sequence": order_hessian_crossing_sequence,
        "softening_share_sequence": softening_share_sequence,
        "interior_share_sequence": interior_share_sequence,
        "order_hessian_share_sequence": order_hessian_share_sequence,
        "hessian_third_share_sequence": hessian_third_share_sequence,
        "secondary_reference_abs_offsets": secondary_reference_abs_offsets,
        "wall_reference_abs_offsets": wall_reference_abs_offsets,
        "directional_signature": directional_signature,
        "convergence_signature_detected": all(directional_signature.values()),
    }


def main() -> None:
    prime_limits = [1000, 10000, 100000]
    s_values = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

    mcxxxii_result_path = ROOT / "PART_MCXXXII_zero_sheet_barycentric_gap_handoff_cutoff_robustness_results.json"
    if mcxxxii_result_path.exists():
        profile_payload = json.loads(mcxxxii_result_path.read_text(encoding="utf-8"))
        packet = _build_from_profile_payload(profile_payload, prime_limits, s_values)
    else:
        packet = completed_defect_spectral_boundary_barycentric_gap_handoff_convergence_signature(
            prime_limits,
            s_values,
            subintervals=40,
        )

    payload = {
        "theorem": "Zero-sheet barycentric gap-handoff directional convergence signature",
        "prime_limits": prime_limits,
        "s_values": s_values,
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_zero_sheet_barycentric_gap_handoff_convergence_signature.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "convergence_signature_detected": packet["convergence_signature_detected"],
        "directional_signature": packet["directional_signature"],
        "wall_gap_drop_sequence": packet["wall_gap_drop_sequence"],
        "secondary_crossing_sequence": packet["secondary_crossing_sequence"],
        "order_hessian_crossing_sequence": packet["order_hessian_crossing_sequence"],
        "softening_share_sequence": packet["softening_share_sequence"],
        "interior_share_sequence": packet["interior_share_sequence"],
        "order_hessian_share_sequence": packet["order_hessian_share_sequence"],
        "hessian_third_share_sequence": packet["hessian_third_share_sequence"],
        "secondary_reference_abs_offsets": packet["secondary_reference_abs_offsets"],
        "wall_reference_abs_offsets": packet["wall_reference_abs_offsets"],
    }
    result_path = ROOT / "PART_MCXXXIII_zero_sheet_barycentric_gap_handoff_convergence_signature_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXXXIII Zero-Sheet Barycentric Gap-Handoff Directional Convergence Signature ===")
    print(
        f"signature={packet['convergence_signature_detected']}, "
        f"wall_drop_seq={packet['wall_gap_drop_sequence']}, "
        f"secondary_crossing_seq={packet['secondary_crossing_sequence']}"
    )


if __name__ == "__main__":
    main()