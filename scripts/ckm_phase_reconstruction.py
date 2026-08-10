#!/usr/bin/env python3
"""
Reconstruct a 3x3 unitary from the overlap magnitudes using alternating
projections between the magnitude constraint and the unitary group.

Writes `data/ckm_phase_reconstruction.json` with the reconstructed unitary,
Jarlskog, unitarity error, and magnitude deviations.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from numpy.linalg import svd, norm
import sys

sys.path.insert(0, str(Path(__file__).parent))
import w33_ckm_mixing as mix


def polar_unitary(A: np.ndarray) -> np.ndarray:
    U, s, Vh = svd(A)
    return U @ Vh


def compute_jarlskog(V: np.ndarray) -> float:
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


def leading_rep(V: np.ndarray) -> np.ndarray:
    U, s, VT = np.linalg.svd(V, full_matrices=False)
    rep = U[:, 0]
    idx = int(np.argmax(np.abs(rep)))
    if rep[idx] != 0:
        rep = rep * np.exp(-1j * np.angle(rep[idx]))
    return rep


def orthonormalize(Q: np.ndarray) -> np.ndarray:
    Qr, R = np.linalg.qr(Q)
    d = np.diag(R)
    s = np.sign(np.real(d))
    s[s == 0] = 1
    return Qr * s


def main():
    p = Path("data/ckm_from_grams.json")
    if not p.exists():
        print("ERROR: data/ckm_from_grams.json not found. Run scripts/ckm_from_grams.py first.")
        return 1

    d = json.loads(p.read_text(encoding="utf-8"))
    M = np.array(d["overlap_matrix"], dtype=float)
    exp = np.array(d.get("experimental", []), dtype=float)

    # magnitude constraint: sqrt of probabilities
    S = np.sqrt(np.maximum(M, 0.0))

    # initial phase estimate from a geometric eigenvector reconstruction
    data = mix.build_all(verbose=False)
    order3, refined = mix.classify_order3_conjugacy(data)
    if len(refined) < 2:
        indices = list(refined.values())[0]
        el1 = order3[indices[0]]
        el2 = None
        for idx in indices[1:]:
            cand = order3[idx]
            v1, v2 = el1[0], cand[0]
            if tuple(v1[i] for i in v2) != tuple(v2[i] for i in v1):
                el2 = cand
                break
        if el2 is None:
            el2 = order3[indices[1]]
    else:
        keys = sorted(refined.keys())
        el1 = order3[refined[keys[0]][0]]
        el2 = order3[refined[keys[1]][0]]

    s1 = mix.compute_generation_eigenspaces(data, el1)
    s2 = mix.compute_generation_eigenspaces(data, el2)
    labels = ["1", "w", "wb"]
    reps1 = np.column_stack([leading_rep(s1[l]) for l in labels])
    reps2 = np.column_stack([leading_rep(s2[l]) for l in labels])
    Q1 = orthonormalize(reps1)
    Q2 = orthonormalize(reps2)
    V0 = Q1.conj().T @ Q2

    # initialize A with magnitudes S and phases from V0
    A = S * np.exp(1j * np.angle(V0))

    max_iter = 500
    tol = 1e-9
    last_err = None
    for it in range(max_iter):
        U = polar_unitary(A)
        mag_err = norm(np.abs(U) - S)
        if mag_err < tol:
            break
        # update A to have magnitudes S and phases from U
        A = S * np.exp(1j * np.angle(U))
        if last_err is not None and abs(last_err - mag_err) < 1e-14:
            break
        last_err = mag_err

    U_final = polar_unitary(A)
    unitary_err = float(norm(U_final @ U_final.conj().T - np.eye(3)))
    J = compute_jarlskog(U_final)
    mags = np.abs(U_final)
    mags2 = mags ** 2

    mag_diff_frob = float(norm(mags - S))
    mag2_diff_frob = float(norm(mags2 - M))
    exp_mag2_diff = float(norm(mags2 - exp)) if exp.size else None

    out = {
        "unitary_real": U_final.real.tolist(),
        "unitary_imag": U_final.imag.tolist(),
        "abs": mags.tolist(),
        "abs2": mags2.tolist(),
        "unitarity_err": unitary_err,
        "jarlskog": J,
        "mag_diff_frob": mag_diff_frob,
        "mag2_diff_frob": mag2_diff_frob,
        "exp_mag2_diff_frob": exp_mag2_diff,
    }

    outp = Path("data/ckm_phase_reconstruction.json")
    outp.write_text(json.dumps(out, indent=2))
    print("Wrote data/ckm_phase_reconstruction.json")
    print(f"unitarity_err={unitary_err:.6g}, jarlskog={J:.6g}")
    print(f"mag2_diff_frob={mag2_diff_frob:.6g}, exp_mag2_diff={exp_mag2_diff}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
