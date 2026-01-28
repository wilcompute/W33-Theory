#!/usr/bin/env python3
"""Generate an interferometric protocol to measure Pancharatnam phase.

Uses explicit triangle examples with phases ±π/6 and ±π/2.
Outputs a concise photonic protocol with ray vectors.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    labels = []

    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
        labels.append(f"e{i}")

    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            labels.append(f"(0,1,-w^{mu},w^{nu})/sqrt3")
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            labels.append(f"(1,0,-w^{mu},-w^{nu})/sqrt3")
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            labels.append(f"(1,-w^{mu},0,w^{nu})/sqrt3")
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
            labels.append(f"(1,w^{mu},w^{nu},0)/sqrt3")

    return rays, labels


def main():
    examples_path = DOCS / "witting_pancharatnam_examples.json"
    if not examples_path.exists():
        print("Missing docs/witting_pancharatnam_examples.json")
        return

    examples = json.loads(examples_path.read_text())
    rays, labels = construct_witting_40_rays()

    md_path = DOCS / "witting_pancharatnam_protocol.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pancharatnam Phase Protocol (π/6, π/2) for Witting Rays\n\n")
        f.write("This protocol measures the geometric phase for a 3‑ray loop:\n")
        f.write("\n")
        f.write("Φ = arg(⟨a|b⟩⟨b|c⟩⟨c|a⟩)\n\n")
        f.write("The Witting set exhibits phase quantization at ±π/6 and ±π/2.\n\n")

        for label in ["+pi/6", "-pi/6", "+pi/2", "-pi/2"]:
            triple = examples.get(label)
            if not triple:
                continue
            i, j, k, ang = triple
            f.write(f"## Target phase {label}\n")
            f.write(f"Ray indices: ({i}, {j}, {k})\n\n")
            f.write("### Ray vectors (C^4)\n")
            for idx in (i, j, k):
                v = rays[idx]
                f.write(f"- r{idx} = {labels[idx]} = {v.tolist()}\n")
            f.write("\n### Interferometric loop (conceptual)\n")
            f.write("1. Prepare |a⟩ = r_i.\n")
            f.write("2. Interfere |a⟩ with |b⟩ to extract arg⟨a|b⟩.\n")
            f.write("3. Interfere |b⟩ with |c⟩ to extract arg⟨b|c⟩.\n")
            f.write("4. Interfere |c⟩ with |a⟩ to extract arg⟨c|a⟩.\n")
            f.write("5. Sum phases to obtain Φ.\n\n")
            f.write(f"Expected phase: **{ang:.6f} rad**\n\n")

        f.write("## Notes\n")
        f.write("- Use any standard Pancharatnam/Berry phase interferometer.\n")
        f.write(
            "- Phase quantization at ±π/6 and ±π/2 is the observed discrete signature.\n"
        )
        f.write(
            "- This is state‑preparation independent (depends only on ray overlaps).\n"
        )

    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
