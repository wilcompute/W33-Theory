#!/usr/bin/env python3
"""
Reconstruct a 3x3 unitary matching the fitted scaled magnitudes
(from `data/ckm_fitted_scalings.json`) using alternating projections
and save results to `data/ckm_scaled_phase_reconstruction.json`.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from numpy.linalg import svd, norm
import sys


def polar_unitary(A: np.ndarray) -> np.ndarray:
    U, s, Vh = svd(A)
    return U @ Vh


def compute_jarlskog(V: np.ndarray) -> float:
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def load_prev_unitary(path: Path) -> np.ndarray | None:
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    real = np.array(d.get("unitary_real"))
    imag = np.array(d.get("unitary_imag"))
    if real.size == 0 or imag.size == 0:
        return None
    return real + 1j * imag


def main():
    p = Path("data/ckm_fitted_scalings.json")
    if not p.exists():
        print("ERROR: data/ckm_fitted_scalings.json not found; run scripts/ckm_fit_scalings.py first")
        return 1

    d = json.loads(p.read_text(encoding="utf-8"))
    A = np.array(d.get("scaled_matrix", []), dtype=float)
    if A.size == 0:
        print("ERROR: scaled_matrix missing from data/ckm_fitted_scalings.json")
        return 1

    # target magnitudes
    S = np.sqrt(np.maximum(A, 0.0))

    # initial phases: try previous phase reconstruction
    prev = load_prev_unitary(Path("data/ckm_phase_reconstruction.json"))
    if prev is not None and prev.shape == (3, 3):
        init_phase = np.angle(prev)
    else:
        rng = np.random.default_rng(42)
        init_phase = rng.uniform(-np.pi, np.pi, size=(3, 3))

    U_phased = S * np.exp(1j * init_phase)

    max_iter = 2000
    tol = 1e-12
    last_err = None
    for it in range(max_iter):
        U = polar_unitary(U_phased)
        mag_err = norm(np.abs(U) - S)
        if mag_err < tol:
            break
        U_phased = S * np.exp(1j * np.angle(U))
        if last_err is not None and abs(last_err - mag_err) < 1e-14:
            break
        last_err = mag_err

    U_final = polar_unitary(U_phased)
    unitary_err = float(norm(U_final @ U_final.conj().T - np.eye(3)))
    J = compute_jarlskog(U_final)
    mags = np.abs(U_final)
    mags2 = mags ** 2
    mag2_diff_frob = float(norm(mags2 - A))

    out = {
        "unitary_real": U_final.real.tolist(),
        "unitary_imag": U_final.imag.tolist(),
        "abs": mags.tolist(),
        "abs2": mags2.tolist(),
        "unitarity_err": unitary_err,
        "jarlskog": J,
        "mag2_diff_frob": mag2_diff_frob,
    }

    outp = Path("data/ckm_scaled_phase_reconstruction.json")
    outp.write_text(json.dumps(out, indent=2))
    print("Wrote data/ckm_scaled_phase_reconstruction.json")
    print(f"unitarity_err={unitary_err:.6g}, jarlskog={J:.6g}, mag2_diff_frob={mag2_diff_frob:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
