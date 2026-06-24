#!/usr/bin/env python3
"""BT1663 — timing-noise robustness simulator for the BT1660 separator."""
from __future__ import annotations

import json
import math
from pathlib import Path


def contrast(phase_jitter_rms: float, parity_flip_prob: float, background_fraction: float) -> float:
    return math.exp(-0.5 * phase_jitter_rms**2) * (1 - 2 * parity_flip_prob) * (1 - background_fraction)


def snr(shots: int, loss_fraction: float, c: float) -> float:
    return abs(c) * math.sqrt(max(0.0, shots * (1 - loss_fraction)))


def max_parity_for_5sigma(shots: int, loss_fraction: float, phase_jitter_rms: float, background_fraction: float) -> float:
    effective = shots * (1 - loss_fraction)
    if effective <= 0:
        return 0.0
    required_contrast = 5 / math.sqrt(effective)
    attenuation = math.exp(-0.5 * phase_jitter_rms**2) * (1 - background_fraction)
    if attenuation <= 0:
        return 0.0
    return max(0.0, min(0.5, 0.5 * (1 - required_contrast / attenuation)))


def main() -> None:
    shots = 2048
    phase_jitter_rms = 0.05
    background_fraction = 0.02
    losses = [0.0, 0.1, 0.25, 0.5, 0.75]
    rows = []
    for loss in losses:
        pmax = max_parity_for_5sigma(shots, loss, phase_jitter_rms, background_fraction)
        c = contrast(phase_jitter_rms, pmax, background_fraction)
        rows.append({
            "loss_fraction": loss,
            "max_parity_flip_for_5sigma": round(pmax, 6),
            "contrast_at_threshold": round(c, 6),
            "effective_shots": round(shots * (1 - loss), 3),
            "snr_at_threshold": round(snr(shots, loss, c), 6)
        })

    nominal = {
        "shots": shots,
        "loss_fraction": 0.1,
        "phase_jitter_rms": phase_jitter_rms,
        "background_fraction": background_fraction,
        "parity_flip_prob": 0.05,
    }
    nominal_c = contrast(nominal["phase_jitter_rms"], nominal["parity_flip_prob"], nominal["background_fraction"])
    nominal["contrast"] = round(nominal_c, 6)
    nominal["snr"] = round(snr(shots, nominal["loss_fraction"], nominal_c), 6)

    result = {
        "theorem": "BT1663 Timing-Noise Robustness Simulator",
        "model": "separator contrast = exp(-sigma_phi^2/2) * (1 - 2p_flip) * (1 - background)",
        "nominal_case": nominal,
        "five_sigma_parity_thresholds": rows,
        "pass_rule": "separator is accepted when absolute contrast times sqrt(effective shots) is at least 5",
        "interpretation": "the BT1660 -1/+1 separator is robust to moderate loss because loss mainly reduces shot number, while parity flips directly reduce contrast",
        "boundary": "This is a first analytic-noise model, not a full optical device simulation. It should be replaced by measured component loss once hardware numbers are fixed."
    }
    assert nominal["snr"] > 5
    out = Path("data/PART_BT1663_TIMING_NOISE_ROBUSTNESS_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
