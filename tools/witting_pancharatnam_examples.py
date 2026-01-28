#!/usr/bin/env python3
"""Find explicit triangle examples with Pancharatnam phase 0 and ±2π/3."""
from __future__ import annotations

import json
import itertools
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


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


def phase_triangle(a, b, c):
    prod = np.vdot(a, b) * np.vdot(b, c) * np.vdot(c, a)
    if abs(prod) < 1e-12:
        return None
    return np.angle(prod / abs(prod))


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    target = {"0": None, "+2pi/3": None, "-2pi/3": None}

    for i, j, k in itertools.combinations(range(n), 3):
        if abs(np.vdot(rays[i], rays[j])) < 1e-8:
            continue
        if abs(np.vdot(rays[j], rays[k])) < 1e-8:
            continue
        if abs(np.vdot(rays[k], rays[i])) < 1e-8:
            continue

        ang = phase_triangle(rays[i], rays[j], rays[k])
        if ang is None:
            continue

        # normalize to (-pi, pi]
        ang = np.arctan2(np.sin(ang), np.cos(ang))

        if target["0"] is None and abs(ang - 0) < 1e-3:
            target["0"] = (i, j, k, float(ang))
        if target["+2pi/3"] is None and abs(ang - 2*np.pi/3) < 1e-3:
            target["+2pi/3"] = (i, j, k, float(ang))
        if target["-2pi/3"] is None and abs(ang + 2*np.pi/3) < 1e-3:
            target["-2pi/3"] = (i, j, k, float(ang))

        if all(target.values()):
            break

    out = {k: v for k, v in target.items()}
    out_path = DOCS / "witting_pancharatnam_examples.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")

    md_path = DOCS / "witting_pancharatnam_examples.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Pancharatnam Triangle Examples\n\n")
        for label, triple in out.items():
            if triple is None:
                f.write(f"- {label}: not found\n")
                continue
            i, j, k, ang = triple
            f.write(f"- {label}: rays ({i},{j},{k}), phase ≈ {ang:.6f} rad\n")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
