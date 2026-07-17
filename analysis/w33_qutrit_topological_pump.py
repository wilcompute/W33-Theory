#!/usr/bin/env python3
"""Toy spin-1 pump phase diagram, not a Holonet logic-switch certificate.

For a chosen spin-1 two-tone Hamiltonian
    H(phi1,phi2) = B(phi1,phi2) . S ,   S = spin-1 angular momentum,
    B = (sin phi1, sin phi2, m + cos phi1 + cos phi2),
the spin-1 bands can have Chern profile (+2,0,-2) in the gapped region 0<m<2.
This is a model calculation only. It does not establish a qutrit device
Hamiltonian, a physical pump, or any connection to the verified binary-Q3/Q6
logic-switch pipeline. The gapless m=0 and m=2 boundaries are excluded.
"""
from __future__ import annotations

import json
import numpy as np

s2 = np.sqrt(2)
SX = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex) / s2
SY = np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]], dtype=complex) / s2
SZ = np.array([[1, 0, 0], [0, 0, 0], [0, 0, -1]], dtype=complex)


def bands(phi1, phi2, m):
    B = (np.sin(phi1), np.sin(phi2), m + np.cos(phi1) + np.cos(phi2))
    H = B[0] * SX + B[1] * SY + B[2] * SZ
    w, v = np.linalg.eigh(H)                 # ascending eigenvalues
    return [v[:, k] for k in range(3)]       # 3 band eigenvectors


def chern_bands(m, N=28):
    grid = np.linspace(0, 2 * np.pi, N, endpoint=False)
    psi = [[bands(p1, p2, m) for p2 in grid] for p1 in grid]
    C = [0.0, 0.0, 0.0]
    for b in range(3):
        F = 0.0
        for i in range(N):
            for j in range(N):
                u00 = psi[i][j][b]; u10 = psi[(i + 1) % N][j][b]
                u11 = psi[(i + 1) % N][(j + 1) % N][b]; u01 = psi[i][(j + 1) % N][b]
                U1 = np.vdot(u00, u10); U2 = np.vdot(u10, u11)
                U3 = np.vdot(u11, u01); U4 = np.vdot(u01, u00)
                for U in (U1, U2, U3, U4):
                    pass
                F += np.angle((U1 / abs(U1)) * (U2 / abs(U2)) *
                              (U3 / abs(U3)) * (U4 / abs(U4)))
        C[b] = F / (2 * np.pi)
    return C


def main():
    out = {
        "schema": "w33.toy_spin1_pump_phase_diagram.v2",
        "scope": "Model Hamiltonian only; excluded from the verified finite logic-switch ABI.",
    }
    theta = np.arccos(-2 / 3)
    print("[toy spin-1 two-tone pump: gapped band Chern samples vs m]")
    print("  band order: [lowest, middle, highest] eigenvalue")
    for m in (0.5, 1.0, 1.5, 2.5):
        C = chern_bands(m)
        Cr = [int(round(c)) for c in C]
        regime = "TOPOLOGICAL" if any(Cr) else "trivial"
        print(f"  m={m:4.1f}: Chern (lo,mid,hi) = {Cr}  sum={sum(Cr)}  ({regime})")
        out[f"m={m}"] = Cr

    # The clean model regime is the interior 0<m<2; use m=1.0 as a sample point.
    C0 = [int(round(c)) for c in chern_bands(1.0)]
    print(f"\n  at the interior operating point m=1.0: band Chern = {C0}, "
          f"sum = {sum(C0)}")
    print(f"  (m=0 is a band-touching singularity -> excluded; topological regime")
    print(f"   is 0<m<2, trivializing past the gap-closing at m=2.)")
    print(f"  this spin-1 model has extremal |C|=2 (vs the toy two-band |C|=1).")
    assert sorted(C0) == [-2, 0, 2] and sum(C0) == 0

    out["band_chern_m1"] = C0
    out["theta"] = float(theta)

    print("\nRESULT (model only): this chosen gapped spin-1 Hamiltonian has")
    print("  band Chern profile {+2,0,-2} at m=1.0. It supplies no device map, no")
    print("  calibrated pump, and no evidence for a Holonet state transition.")
    out["result"] = "toy spin-1 pump at m=1.0, band Chern profile {+2,0,-2}"
    out["honest"] = ("The spin-1 representation and parameter torus are model choices. "
                     "A device-specific Hamiltonian and an implementation map would "
                     "be required before assigning this Chern calculation to hardware.")
    out["source"] = "Martin-Refael-Halperin, PRX 7, 041008 (2017); spin-S monopole Chern 2 m_s"
    with open("data/w33_qutrit_topological_pump.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_qutrit_topological_pump.json")


if __name__ == "__main__":
    main()
