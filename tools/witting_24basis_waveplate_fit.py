#!/usr/bin/env python3
"""Fit QWP-HWP-QWP angles for each 2x2 Givens rotation in the 24-basis set.

We model waveplates with Jones matrices:
J(δ,θ) = R(-θ) diag(e^{-iδ/2}, e^{iδ/2}) R(θ),
with δ=π/2 for QWP and δ=π for HWP.

We fit angles α,β,γ in [0,π) such that
U_target ≈ e^{iχ} QWP(α) HWP(β) QWP(γ).
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def R(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=complex)


def waveplate(delta, theta):
    # R(-θ) diag(e^{-iδ/2}, e^{iδ/2}) R(θ)
    D = np.array(
        [[np.exp(-1j * delta / 2), 0], [0, np.exp(1j * delta / 2)]],
        dtype=complex,
    )
    return R(-theta) @ D @ R(theta)


def QWP(theta):
    return waveplate(math.pi / 2, theta)


def HWP(theta):
    return waveplate(math.pi, theta)


def target_unitary(theta, phi):
    # SU(2) rotation (global phase irrelevant)
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array(
        [[c, np.exp(1j * phi) * s], [-np.exp(-1j * phi) * s, c]],
        dtype=complex,
    )


def phase_invariant_error(U, V):
    # Minimize ||U - e^{iχ} V|| via χ = arg(Tr(U^† V))
    inner = np.trace(U.conj().T @ V)
    if abs(inner) < 1e-12:
        return 1.0
    chi = inner / abs(inner)
    diff = U - chi * V
    return float(np.linalg.norm(diff))


def fit_angles(U, trials=50, step=0.1, refinements=4):
    best = (1e9, (0.0, 0.0, 0.0))
    rng = random.Random(0)

    for _ in range(trials):
        a = rng.random() * math.pi
        b = rng.random() * math.pi
        c = rng.random() * math.pi
        V = QWP(a) @ HWP(b) @ QWP(c)
        err = phase_invariant_error(U, V)
        if err < best[0]:
            best = (err, (a, b, c))

    # Coordinate descent
    a, b, c = best[1]
    for _ in range(refinements):
        for idx in range(3):
            base = [a, b, c]
            best_local = (best[0], base)
            for delta in [-2, -1, 0, 1, 2]:
                trial = base.copy()
                trial[idx] = (trial[idx] + delta * step) % math.pi
                V = QWP(trial[0]) @ HWP(trial[1]) @ QWP(trial[2])
                err = phase_invariant_error(U, V)
                if err < best_local[0]:
                    best_local = (err, trial)
            a, b, c = best_local[1]
            best = (best_local[0], (a, b, c))
        step *= 0.5

    return best


def main():
    in_path = DOCS / "witting_24basis_reck.json"
    if not in_path.exists():
        print("Missing docs/witting_24basis_reck.json")
        return

    data = json.loads(in_path.read_text())
    out = []

    for entry in data:
        basis_ops = []
        for op in entry["ops"]:
            theta = float(op["theta"])
            phi = float(op["phi"])
            U = target_unitary(theta, phi)
            err, angles = fit_angles(U)
            a, b, c = angles
            basis_ops.append({
                "i": op["i"],
                "j": op["j"],
                "theta": theta,
                "phi": phi,
                "qwp1": a,
                "hwp": b,
                "qwp2": c,
                "fit_error": err,
            })
        out.append({
            "basis_index": entry["basis_index"],
            "rays": entry["rays"],
            "ops": basis_ops,
        })

    json_path = DOCS / "witting_24basis_waveplates.json"
    json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = DOCS / "witting_24basis_waveplates.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis Waveplate Schedule (QWP‑HWP‑QWP)\n\n")
        f.write("Angles in radians. Each op approximates the target SU(2) rotation\n")
        f.write("up to global phase.\n\n")
        for entry in out:
            f.write(f"## Basis B{entry['basis_index']:02d}\n")
            f.write(f"Rays: {entry['rays']}\n\n")
            for op in entry["ops"]:
                f.write(
                    f"- mix({op['i']},{op['j']}): QWP={op['qwp1']:.4f}, HWP={op['hwp']:.4f}, QWP={op['qwp2']:.4f}, err={op['fit_error']:.3e}\n"
                )
            f.write("\n")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
