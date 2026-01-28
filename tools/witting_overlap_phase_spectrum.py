#!/usr/bin/env python3
"""Analyze phase spectrum of pairwise overlaps between Witting rays.

We show:
  - Non-orthogonal overlaps all have |<ri|rj>|^2 = 1/3.
  - Overlap phases are quantized in multiples of pi/6.
  - Phase distribution depends on whether a basis ray is involved.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def is_basis_ray(ray, tol=1e-12):
    return sum(1 for z in ray if abs(z) < tol) == 3


def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


def main():
    rays = construct_witting_40_rays()
    n = len(rays)
    basis_flags = [is_basis_ray(r) for r in rays]

    phase_counts = Counter()
    phase_by_basis = defaultdict(Counter)
    mag_counts = Counter()

    for i in range(n):
        for j in range(i + 1, n):
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                mag_counts[0.0] += 1
                continue
            mag_counts[round(float(abs(ip) ** 2), 6)] += 1
            ang = wrap_angle(np.angle(ip))
            ang_r = round(float(ang), 6)
            phase_counts[ang_r] += 1
            bcount = int(basis_flags[i]) + int(basis_flags[j])
            phase_by_basis[bcount][ang_r] += 1

    # Check quantization on pi/6 grid
    grid_step = np.pi / 6
    max_resid = 0.0
    for ang in phase_counts.keys():
        k = round(ang / grid_step)
        resid = abs(ang - k * grid_step)
        max_resid = max(max_resid, resid)

    out = {
        "pairs_total": n * (n - 1) // 2,
        "overlap_magnitude_counts": {str(k): v for k, v in sorted(mag_counts.items())},
        "phase_counts": {str(k): v for k, v in sorted(phase_counts.items())},
        "phase_by_basis": {
            str(k): {str(a): c for a, c in sorted(v.items())}
            for k, v in phase_by_basis.items()
        },
        "pi_over_6_max_residual": max_resid,
    }

    out_path = ROOT / "artifacts" / "witting_overlap_phase_spectrum.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_overlap_phase_spectrum.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Ray Overlap Phase Spectrum\n\n")
        f.write(f"Total ray pairs: **{out['pairs_total']}**\n\n")
        f.write("## |<ri|rj>|^2 distribution\n\n")
        f.write("value | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(mag_counts.items()):
            f.write(f"{k} | {v}\n")
        f.write("\n## Phase spectrum (non‑orthogonal pairs)\n\n")
        f.write("phase (rad) | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(phase_counts.items()):
            f.write(f"{k} | {v}\n")
        f.write(
            "\nQuantization check: max residual from π/6 grid = "
            f"{max_resid:.6e} rad\n"
        )
        f.write("\n## Phase spectrum by basis‑ray count in pair\n\n")
        f.write("basis rays in pair | phase counts\n")
        f.write("--- | ---\n")
        for bcount in sorted(phase_by_basis.keys()):
            clusters = ", ".join(f"{k}:{v}" for k, v in sorted(phase_by_basis[bcount].items()))
            f.write(f"{bcount} | {clusters}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
