#!/usr/bin/env python3
"""Estimate phase-noise robustness for the Pancharatnam phase test.

We model additive phase noise on each pairwise phase measurement:
  phi_meas = phi_true + eps, eps ~ Uniform[-sigma, sigma].

We compute the probability of correctly classifying the sum phase into
{±π/6, ±π/2} by nearest-neighbor under this noise model.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def classify(phase):
    # map to (-pi, pi]
    a = math.atan2(math.sin(phase), math.cos(phase))
    targets = [math.pi/6, -math.pi/6, math.pi/2, -math.pi/2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return nearest


def simulate(sigma, trials=20000, true_phase=math.pi/6):
    correct = 0
    for _ in range(trials):
        eps1 = random.uniform(-sigma, sigma)
        eps2 = random.uniform(-sigma, sigma)
        eps3 = random.uniform(-sigma, sigma)
        meas = true_phase + eps1 + eps2 + eps3
        if classify(meas) == true_phase:
            correct += 1
    return correct / trials


def main():
    results = []
    for sigma in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]:
        acc_small = simulate(sigma, true_phase=math.pi/6)
        acc_large = simulate(sigma, true_phase=math.pi/2)
        acc_avg = 0.5 * (acc_small + acc_large)
        results.append((sigma, acc_small, acc_large, acc_avg))

    md_path = DOCS / "witting_pancharatnam_noise_threshold.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pancharatnam Phase Noise Robustness (π/6, π/2)\n\n")
        f.write("Assume uniform additive phase noise per pairwise measurement.\n\n")
        f.write("sigma (rad) | acc(π/6) | acc(π/2) | avg\n")
        f.write("--- | --- | --- | ---\n")
        for sigma, acc_small, acc_large, acc_avg in results:
            f.write(f"{sigma:.2f} | {acc_small:.4f} | {acc_large:.4f} | {acc_avg:.4f}\n")

    out_path = DOCS / "witting_pancharatnam_noise_threshold.json"
    out_path.write_text(
        json.dumps({"results": [{"sigma": s, "acc_pi6": a1, "acc_pi2": a2, "acc_avg": a3} for s, a1, a2, a3 in results]}, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {md_path}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
