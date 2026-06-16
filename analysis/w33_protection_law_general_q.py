#!/usr/bin/env python3
"""
The self-protection law across qudit dimensions: |C|_max = q-1, and why the
substrate's q=3 carrier is doubly protected.

A qudit of dimension d=q carries spin S=(q-1)/2 under the rotation (BC) drive, so
the two-tone topological pump is the spin-S monopole, whose band with weight m_s
has Chern number 2 m_s. The EXTREMAL bands (m_s = +-S) carry

    |C|_max = 2S = q - 1 = lambda   (the substrate SRG parameter).

So the topological self-protection grows linearly with q. The substrate's q=3 is
fixed by physics (q! = 2q, the spectral-action (q-3)(3q-1), KO-dim 2q=6); the
carrier inherits it and gets |C| = q-1 = 2 -- DOUBLE the qubit (q=2 -> |C|=1).
We verify the law by computing the extremal band Chern of the spin-S pump for
q = 2,3,4 (Fukui-Hatsugai-Suzuki at an interior operating point).
"""
from __future__ import annotations

import json
import numpy as np


def spin_matrices(S):
    d = int(round(2 * S + 1))
    m = np.array([S - i for i in range(d)])          # S, S-1, ..., -S
    Sz = np.diag(m).astype(complex)
    Sp = np.zeros((d, d), complex)
    for i in range(1, d):
        mm = m[i]                                    # lower state weight
        Sp[i - 1, i] = np.sqrt(S * (S + 1) - mm * (mm + 1))
    Sx = (Sp + Sp.conj().T) / 2
    Sy = (Sp - Sp.conj().T) / (2j)
    return Sx, Sy, Sz


def band_chern(S, m0=1.3, N=30):
    Sx, Sy, Sz = spin_matrices(S)
    d = Sx.shape[0]
    grid = np.linspace(0, 2 * np.pi, N, endpoint=False)
    psi = [[None] * N for _ in range(N)]
    for i, p1 in enumerate(grid):
        for j, p2 in enumerate(grid):
            B = (np.sin(p1), np.sin(p2), m0 + np.cos(p1) + np.cos(p2))
            H = B[0] * Sx + B[1] * Sy + B[2] * Sz
            w, v = np.linalg.eigh(H)
            psi[i][j] = v
    C = []
    for b in range(d):
        F = 0.0
        for i in range(N):
            for j in range(N):
                u00 = psi[i][j][:, b]; u10 = psi[(i + 1) % N][j][:, b]
                u11 = psi[(i + 1) % N][(j + 1) % N][:, b]; u01 = psi[i][(j + 1) % N][:, b]
                U1 = np.vdot(u00, u10); U2 = np.vdot(u10, u11)
                U3 = np.vdot(u11, u01); U4 = np.vdot(u01, u00)
                F += np.angle((U1 / abs(U1)) * (U2 / abs(U2)) *
                              (U3 / abs(U3)) * (U4 / abs(U4)))
        C.append(int(round(F / (2 * np.pi))))
    return C


def main():
    out = {}
    print("[self-protection law: extremal band Chern of the spin-S pump = q-1]")
    print("  q | spin S | band Chern numbers        | |C|_max | q-1 | match")
    for q in (2, 3, 4):
        S = (q - 1) / 2
        C = band_chern(S)
        cmax = max(abs(c) for c in C)
        match = cmax == q - 1 and sum(C) == 0
        print(f"  {q} |  {S:>3}   | {str(C):24s} | {cmax:5d}  | {q-1:3d} | {match}")
        out[f"q={q}"] = {"spin": S, "band_chern": C, "Cmax": cmax,
                         "equals_q_minus_1": match}
        assert match

    print("\n  => |C|_max = q-1 = lambda confirmed for q=2,3,4 (sum of band Cherns")
    print("     = 0 each). Protection grows linearly with q.")
    print("\nRESULT: the topological self-protection law is |C|_max = q-1. The")
    print("  substrate's q=3 (fixed by physics: q!=2q, (q-3)(3q-1), KO-dim 2q=6)")
    print("  gives the carrier |C|=2 -- double the qubit's |C|=1. The architecture")
    print("  does not independently optimize q; it INHERITS q=3 from the substrate")
    print("  physics and reaps the enhanced (|C|=q-1=2) topological protection as")
    print("  a consequence. Same q-1=lambda that sets the BC drive cos=-(q-1)/q and")
    print("  the 2=lambda transverse photon helicities: one substrate number,")
    print("  three faces (drive, protection, polarization).")

    out["law"] = "|C|_max = q-1 = lambda (spin-(q-1)/2 monopole, extremal band)"
    out["q3_inherited"] = ("q=3 fixed by physics (q!=2q, spectral action, KO-dim); "
                           "carrier inherits it, gets |C|=2 = double the qubit")
    out["one_number_three_faces"] = ("q-1=lambda sets: BC drive cos=-(q-1)/q, "
                                     "topological protection |C|=q-1, photon "
                                     "transverse helicities 2=lambda=q-1")
    with open("data/w33_protection_law_general_q.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_protection_law_general_q.json")


if __name__ == "__main__":
    main()
