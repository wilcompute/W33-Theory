#!/usr/bin/env python3
"""Toy two-band pump phase diagram, deliberately outside the logic-switch ABI.

This evaluates the standard two-tone two-level Hamiltonian on a parameter torus.
It is a model calculation, not a construction of a Holonet device, a binary-Q3
switch, or a physical oscillator.  In particular the model is gapless at
``m=0`` (and at ``m=2``): B vanishes at high-symmetry torus points, so a band
Chern number is not defined there.  Earlier output that called m=0 a natural
topological operating point was therefore invalid.

The script now evaluates only gapped sample values and records the gap-closing
boundary explicitly.  A nonzero Chern number belongs to this chosen Hamiltonian;
it does not establish topological frequency conversion for a BC or Holonet
implementation without a device Hamiltonian and a parameter-to-device map.
"""
from __future__ import annotations

import json
import numpy as np

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def field(phi1: float, phi2: float, m: float) -> np.ndarray:
    return np.array(
        [np.sin(phi1), np.sin(phi2), m + np.cos(phi1) + np.cos(phi2)]
    )


def gap_closing_points(m: float) -> list[tuple[float, float]]:
    """Exact high-symmetry zeros of B for the sampled positive-m phase diagram."""
    candidates = (0.0, np.pi)
    return [
        (phi1, phi2)
        for phi1 in candidates
        for phi2 in candidates
        if np.linalg.norm(field(phi1, phi2, m)) < 1e-12
    ]


def lower_band_state(phi1, phi2, m):
    """two-tone driven qubit: h = (sin phi1, sin phi2, m + cos phi1 + cos phi2)."""
    h = field(phi1, phi2, m)
    if np.linalg.norm(h) < 1e-12:
        raise ValueError("Chern bands are undefined at a gap-closing point")
    H = h[0] * SX + h[1] * SY + h[2] * SZ
    w, v = np.linalg.eigh(H)
    return v[:, 0]                      # lower band eigenvector


def chern_number(m, N=24):
    """Fukui-Hatsugai-Suzuki lattice Chern number of the lower band on T^2."""
    grid = np.linspace(0, 2 * np.pi, N, endpoint=False)
    psi = [[lower_band_state(p1, p2, m) for p2 in grid] for p1 in grid]
    F_sum = 0.0
    for i in range(N):
        for j in range(N):
            u00 = psi[i][j]
            u10 = psi[(i + 1) % N][j]
            u11 = psi[(i + 1) % N][(j + 1) % N]
            u01 = psi[i][(j + 1) % N]
            U1 = np.vdot(u00, u10); U1 /= abs(U1)
            U2 = np.vdot(u10, u11); U2 /= abs(U2)
            U3 = np.vdot(u11, u01); U3 /= abs(U3)
            U4 = np.vdot(u01, u00); U4 /= abs(U4)
            F_sum += np.angle(U1 * U2 * U3 * U4)
    return F_sum / (2 * np.pi)


def main():
    out = {
        "schema": "w33.toy_two_band_pump_phase_diagram.v2",
        "scope": "Model Hamiltonian only; excluded from the verified finite logic-switch ABI.",
    }
    print("[toy two-band pump: gapped Chern samples vs longitudinal field m]")
    results = {}
    for m in (0.5, 1.0, 1.5, 2.5):
        C = chern_number(m)
        Cr = int(round(C))
        results[m] = Cr
        regime = "TOPOLOGICAL" if Cr != 0 else "trivial"
        print(f"  m={m:4.1f}: Chern C = {C:+.4f} -> {Cr:+d}  ({regime})")
    assert gap_closing_points(0.0) == [(0.0, np.pi), (np.pi, 0.0)]
    assert gap_closing_points(2.0) == [(np.pi, np.pi)]
    operating_chern = results[1.0]
    assert abs(operating_chern) == 1
    out["chern_vs_gapped_m"] = {str(k): v for k, v in results.items()}
    out["gap_closings"] = {
        "m=0": [[0.0, float(np.pi)], [float(np.pi), 0.0]],
        "m=2": [[float(np.pi), float(np.pi)]],
    }
    out["operating_model_point"] = {"m": 1.0, "lower_band_chern": operating_chern}

    print("\nRESULT (model only): the chosen gapped two-band Hamiltonian has a")
    print(f"  lower-band Chern number {operating_chern:+d} at m=1.0. It is not a")
    print("  certificate for a Holonet device, a topological harmonic oscillator, or")
    print("  the binary-Q3/Q6 logic-switch pipeline. The m=0 and m=2 gap closings are")
    print("  recorded explicitly and are excluded from Chern evaluation.")

    out["honest_scope"] = (
        "Chern values are computed for this explicitly chosen two-band Hamiltonian "
        "on T^2. No BC/Helonet carrier Hamiltonian, calibration, or implementation "
        "map is supplied; the model is not evidence for the finite logic ABI."
    )
    out["source"] = "Martin, Refael, Halperin, PRX 7, 041008 (2017)"
    with open("data/w33_topological_pump_test.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_topological_pump_test.json")


if __name__ == "__main__":
    main()
