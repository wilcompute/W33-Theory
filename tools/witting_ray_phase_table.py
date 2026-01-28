#!/usr/bin/env python3
"""Generate amplitude/phase table for the 40 Witting rays in C^4.

Outputs a CSV with magnitude and phase (radians and degrees) for each component.
"""

from __future__ import annotations

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
    rays, labels = construct_witting_40_rays()
    out_path = DOCS / "witting_ray_amplitude_phase.csv"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("ray_index,label,comp,amp,phase_rad,phase_deg\n")
        for i, v in enumerate(rays):
            for k in range(4):
                amp = abs(v[k])
                phase = np.angle(v[k])
                f.write(
                    f'{i},"{labels[i]}",{k},{amp:.8f},{phase:.8f},{np.degrees(phase):.4f}\n'
                )

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
