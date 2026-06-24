#!/usr/bin/env python3
"""BT1664 — component-level optical budget for the BT1660 separator.

All component numbers in this file are explicit DEFAULT PLACEHOLDERS.  They are
not measured hardware values.  The point is to replace the abstract BT1663
contrast knobs with a named switch/delay/phase/analyzer/detector budget that can
be overwritten once hardware numbers are fixed.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

PC6 = {1: Fraction(1, 6), 2: Fraction(-1, 7), 3: Fraction(1, 42)}
PC0 = {0: Fraction(1, 1), 1: Fraction(-43, 42), 2: Fraction(2, 7), 3: Fraction(-1, 42)}
PM24 = {1: Fraction(5, 24), 2: Fraction(-1, 144)}
PM30 = {1: Fraction(-2, 15), 2: Fraction(1, 180)}

DEFAULT_COMPONENTS = {
    "switch_survival": 0.995,
    "delay_survival": 0.998,
    "phase_shifter_survival": 0.999,
    "analyzer_survival": 0.98,
    "detector_efficiency": 0.85,
    "dark_count_probability_per_bin": 1.0e-6,
    "time_bins": 2048,
    "phase_jitter_rms": 0.05,
    "parity_flip_probability": 0.05,
}


def tensor_terms(left: dict[int, Fraction], right: dict[int, Fraction]) -> list[dict[str, object]]:
    terms = []
    for i, ci in left.items():
        for j, cj in right.items():
            terms.append({"clock_power": i, "matter_power": j, "coefficient": ci * cj, "walk_passes": i + j})
    return terms


def evaluate_block(name: str, left: dict[int, Fraction], right: dict[int, Fraction], components: dict[str, float]) -> dict[str, object]:
    terms = tensor_terms(left, right)
    l1 = sum(abs(t["coefficient"]) for t in terms)  # type: ignore[arg-type]
    per_walk_survival = components["switch_survival"] * components["delay_survival"] * components["phase_shifter_survival"]
    weighted_survival = 0.0
    weighted_walk_passes = 0.0
    term_payload = []
    for t in terms:
        coeff = t["coefficient"]  # type: ignore[assignment]
        passes = int(t["walk_passes"])
        weight = float(abs(coeff) / l1)  # type: ignore[arg-type]
        survival = (per_walk_survival ** passes) * components["analyzer_survival"] * components["detector_efficiency"]
        weighted_survival += weight * survival
        weighted_walk_passes += weight * passes
        term_payload.append({
            "clock_power": int(t["clock_power"]),
            "matter_power": int(t["matter_power"]),
            "coefficient": str(coeff),
            "abs_weight": round(weight, 12),
            "walk_passes": passes,
            "branch_survival": round(survival, 12),
        })
    dark_background = 1.0 - (1.0 - components["dark_count_probability_per_bin"]) ** int(components["time_bins"])
    separator_contrast = math.exp(-0.5 * components["phase_jitter_rms"] ** 2) * (1 - 2 * components["parity_flip_probability"]) * (1 - dark_background)
    snr = separator_contrast * math.sqrt(components["time_bins"] * weighted_survival)
    return {
        "name": name,
        "terms": term_payload,
        "term_count": len(terms),
        "l1_coefficient_mass": str(l1),
        "max_walk_passes": max(int(t["walk_passes"]) for t in terms),
        "weighted_walk_passes": round(weighted_walk_passes, 12),
        "weighted_survival": round(weighted_survival, 12),
        "dark_background_fraction": round(dark_background, 12),
        "separator_contrast_after_jitter_flip_background": round(separator_contrast, 12),
        "shot_noise_snr_for_2048_bins": round(snr, 12),
    }


def main() -> None:
    blocks = [
        evaluate_block("resonance_Pc6_tensor_Pm24", PC6, PM24, DEFAULT_COMPONENTS),
        evaluate_block("companion_Pc0_tensor_Pm30", PC0, PM30, DEFAULT_COMPONENTS),
    ]
    result = {
        "theorem": "BT1664 Component-Level Optical Budget",
        "component_defaults_are_placeholders": True,
        "component_defaults": DEFAULT_COMPONENTS,
        "per_walk_survival": round(DEFAULT_COMPONENTS["switch_survival"] * DEFAULT_COMPONENTS["delay_survival"] * DEFAULT_COMPONENTS["phase_shifter_survival"], 12),
        "blocks": blocks,
        "pass_rule": "shot_noise_snr_for_2048_bins >= 5",
        "summary": {
            "resonance_snr": blocks[0]["shot_noise_snr_for_2048_bins"],
            "companion_snr": blocks[1]["shot_noise_snr_for_2048_bins"],
            "min_snr": min(float(blocks[0]["shot_noise_snr_for_2048_bins"]), float(blocks[1]["shot_noise_snr_for_2048_bins"])),
            "passes": "both resonance and companion tensor selectors have max walk depth 5",
        },
        "boundary": "The budget is component-named but still uses placeholder component values. Replace DEFAULT_COMPONENTS with calibrated device data before making an experimental claim.",
    }
    assert result["summary"]["min_snr"] > 5
    out = Path("data/PART_BT1664_COMPONENT_OPTICAL_BUDGET_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
