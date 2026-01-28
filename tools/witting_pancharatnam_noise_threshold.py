#!/usr/bin/env python3
"""Estimate phase-noise robustness for the Z3 Pancharatnam phase test.

We model additive phase noise on each pairwise phase measurement:
  phi_meas = phi_true + eps, eps ~ Uniform[-sigma, sigma].

We compute the probability of correctly classifying the sum phase into
{0, ±2π/3} by nearest-neighbor under this noise model.
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
    targets = [0, 2*math.pi/3, -2*math.pi/3]
    nearest = min(targets, key=lambda t: abs(a - t))
    return nearest


def simulate(sigma, trials=20000, true_phase=2*math.pi/3):
    correct = 0
    for _ in range(trials):
        eps1 = random.uniform(-sigma, sigma)
        eps2 = random.uniform(-sigma, sigma)
        eps3 = random.uniform(-sigma, sigma)
        meas = true_phase + eps1 + eps2 + eps3
        if classify(meas) == 2*math.pi/3:
            correct += 1
    return correct / trials


def main():
    results = []
    for sigma in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25]:
        acc = simulate(sigma)
        results.append((sigma, acc))

    md_path = DOCS / "witting_pancharatnam_noise_threshold.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pancharatnam Z3 Phase Noise Robustness\n\n")
        f.write("Assume uniform additive phase noise per pairwise measurement.\n\n")
        f.write("sigma (rad) | classification accuracy\n")
        f.write("--- | ---\n")
        for sigma, acc in results:
            f.write(f"{sigma:.2f} | {acc:.4f}\n")

    out_path = DOCS / "witting_pancharatnam_noise_threshold.json"
    out_path.write_text(
        json.dumps({"results": [{"sigma": s, "accuracy": a} for s, a in results]}, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {md_path}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
