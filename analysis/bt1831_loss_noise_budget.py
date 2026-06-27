#!/usr/bin/env python3
"""
BT1831 -- Photonic syndrome loss/noise budget.

This extends the BT1830 compiler IR with an explicit first-pass noise ledger.
The model deliberately separates erasures/loss from wrong-syndrome flips:
loss is postselected or flagged, while surviving shots carry a syndrome-error
union bound.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1831_loss_noise_budget.json"

RESOURCE_COUNTS = {
    "qutrit_sorters": 3,
    "D4_quartet_registers": 3,
    "D4_parity_ancillas": 2,
    "K4_equality_interferometers": 3,
    "C12_ring_winding_readouts": 1,
    "phase_slip_collision_guards": 3,
}

ERROR_MODEL = {
    "qutrit_misroute": 5.0e-4,
    "D4_register_error": 4.0e-4,
    "D4_parity_error": 7.5e-4,
    "K4_equality_error": 1.0e-3,
    "C12_winding_error": 8.0e-4,
    "phase_slip_false_guard": 2.0e-4,
    "detector_dark": 1.0e-5,
    "component_loss": 2.0e-3,
}


def main() -> int:
    syndrome_union_bound = (
        3 * ERROR_MODEL["qutrit_misroute"]
        + 3 * ERROR_MODEL["D4_register_error"]
        + 2 * ERROR_MODEL["D4_parity_error"]
        + 3 * ERROR_MODEL["K4_equality_error"]
        + ERROR_MODEL["C12_winding_error"]
        + 3 * ERROR_MODEL["phase_slip_false_guard"]
        + 12 * ERROR_MODEL["detector_dark"]
    )
    components = sum(RESOURCE_COUNTS.values())
    survival = (1.0 - ERROR_MODEL["component_loss"]) ** components
    erasure_probability = 1.0 - survival
    total_unconditional_bound = erasure_probability + syndrome_union_bound

    checks = {
        "resource_count_15": components == 15,
        "syndrome_bound_below_one_percent": syndrome_union_bound < 0.01,
        "erasure_below_four_percent": erasure_probability < 0.04,
        "total_bound_below_five_percent": total_unconditional_bound < 0.05,
        "loss_separated_from_syndrome_flips": True,
        "all_probabilities_valid": all(0 <= p < 1 for p in ERROR_MODEL.values()),
    }

    payload = {
        "bt": "BT1831",
        "title": "Photonic Syndrome Loss/Noise Budget",
        "verified": all(checks.values()),
        "summary": (
            "BT1831 attaches a first-pass error ledger to the BT1830 compiler IR. "
            "At the stated primitive rates, the surviving-shot syndrome-error union bound "
            "is 0.00872, component-loss erasure is 0.02958, and the conservative "
            "unconditional bound is 0.03830.  Loss is tracked as an erasure/postselection "
            "channel rather than silently folded into logical flips."
        ),
        "resource_counts": RESOURCE_COUNTS,
        "primitive_error_model": ERROR_MODEL,
        "derived": {
            "component_count": components,
            "survival_probability": survival,
            "erasure_probability": erasure_probability,
            "surviving_shot_syndrome_error_union_bound": syndrome_union_bound,
            "unconditional_error_or_erasure_bound": total_unconditional_bound,
            "effective_postselected_success_rate": survival * (1.0 - syndrome_union_bound),
        },
        "dominant_terms": [
            "K4 equality interferometers: 3e-3",
            "component loss / erasure: 2.958e-2",
            "qutrit misrouting: 1.5e-3",
            "D4 parity ancillas: 1.5e-3",
        ],
        "boundary": (
            "This is a union-bound and postselection budget, not a chip calibration. "
            "Correlated errors, mode-dependent loss, detector dead time, and continuous "
            "wavepacket deformation remain outside this pass."
        ),
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "derived": payload["derived"]}, indent=2))
    return 0 if payload["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
