#!/usr/bin/env python3
"""Find explicit triangle examples with Pancharatnam phase ±π/6 and ±π/2."""

from __future__ import annotations

import itertools
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
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
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

    target = {"+pi/6": None, "-pi/6": None, "+pi/2": None, "-pi/2": None}

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

        # classify by nearest observed angle (±pi/6, ±pi/2)
        targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
        nearest = min(targets, key=lambda t: abs(ang - t))
        if abs(ang - nearest) < 1e-2:
            if abs(nearest - np.pi / 6) < 1e-6 and target["+pi/6"] is None:
                target["+pi/6"] = (i, j, k, float(ang))
            elif abs(nearest + np.pi / 6) < 1e-6 and target["-pi/6"] is None:
                target["-pi/6"] = (i, j, k, float(ang))
            elif abs(nearest - np.pi / 2) < 1e-6 and target["+pi/2"] is None:
                target["+pi/2"] = (i, j, k, float(ang))
            elif abs(nearest + np.pi / 2) < 1e-6 and target["-pi/2"] is None:
                target["-pi/2"] = (i, j, k, float(ang))

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
