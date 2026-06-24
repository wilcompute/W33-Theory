#!/usr/bin/env python3
"""
Pump-protection theorem: a spin-S qudit's topological frequency-conversion pump has
extreme-band Chern number 2S, so the qutrit (S=1) pumps exactly lambda = q-1 = 2 --
protected by a Floquet gap that sets the demonstrator's drive/temperature spec.

The demonstrator's flagship measurement (w33_demonstrator_measures_substrate.py) is
the Martin-Refael-Halperin pump quantum. This makes it a theorem and a spec:
  - THEOREM. For a spin-S (a (2S+1)-level qudit) driven by two incommensurate tones
    over the phase torus T^2 via H = sin th1 Sx + sin th2 Sy + (m - cos th1 - cos
    th2) Sz, the bands carry Chern numbers {2S, 2S-2, ..., -2S}; the extreme band
    has |C| = 2S. So the pump quantum is 2S = (2S+1) - 1 = d - 1. For the qutrit
    d = q = 3, S = 1: pump quantum = 2S = q - 1 = lambda = 2. (Verified here for
    S = 1/2, 1, 3/2.)
  - PROTECTION / SPEC. The quantization holds while the drive is adiabatic and
    coherent relative to the instantaneous gap. The minimum Floquet gap over the
    torus, Delta_min, sets the requirements:
        drive rate: omega_1, omega_2 << Delta_min  (adiabaticity);
        decoherence/temperature: k_B T, hbar/T2 << Delta_min.
    Delta_min is computed below for the qutrit; in lab units (Delta ~ the EOM Rabi
    scale, tens of MHz-GHz) the pump quantum C = 2 is robust for slow two-tone
    drives at cryo/room T -- a concrete, buildable spec.

Verifies extreme-band Chern = 2S for S = 1/2, 1, 3/2, and the qutrit min Floquet
gap (the protection scale).
"""
from __future__ import annotations

import json

import numpy as np


def spin_matrices(S):
    d = int(round(2 * S + 1))
    m = np.array([S - i for i in range(d)])  # m = S, S-1, ..., -S
    Sz = np.diag(m).astype(complex)
    Sp = np.zeros((d, d), complex)
    for i in range(d - 1):
        mm = m[i + 1]
        Sp[i, i + 1] = np.sqrt(S * (S + 1) - mm * (mm + 1))
    Sm = Sp.conj().T
    Sx = (Sp + Sm) / 2
    Sy = (Sp - Sm) / (2j)
    return Sx, Sy, Sz


def chern_and_gap(S, m=1.0, Ng=22):
    Sx, Sy, Sz = spin_matrices(S)
    d = int(round(2 * S + 1))
    th = np.linspace(0, 2 * np.pi, Ng, endpoint=False)

    def HE(i, j):
        H = (
            np.sin(th[i]) * Sx
            + np.sin(th[j]) * Sy
            + (m - np.cos(th[i]) - np.cos(th[j])) * Sz
        )
        w, v = np.linalg.eigh(H)
        return w, v

    W = [[None] * Ng for _ in range(Ng)]
    V = [[None] * Ng for _ in range(Ng)]
    for i in range(Ng):
        for j in range(Ng):
            W[i][j], V[i][j] = HE(i, j)
    # min gap between adjacent bands over the torus
    gap = min(min(np.diff(W[i][j])) for i in range(Ng) for j in range(Ng))
    # Fukui-Hatsugai Chern per band
    cherns = []
    for b in range(d):
        F = 0.0
        for i in range(Ng):
            for j in range(Ng):
                u00 = V[i][j][:, b]
                u10 = V[(i + 1) % Ng][j][:, b]
                u11 = V[(i + 1) % Ng][(j + 1) % Ng][:, b]
                u01 = V[i][(j + 1) % Ng][:, b]
                Ux = np.vdot(u00, u10)
                Uy = np.vdot(u10, u11)
                Ux2 = np.vdot(u01, u11)
                Uy2 = np.vdot(u00, u01)
                F += np.log(
                    (Ux / abs(Ux))
                    * (Uy / abs(Uy))
                    / ((Ux2 / abs(Ux2)) * (Uy2 / abs(Uy2)))
                ).imag
        cherns.append(int(round(F / (2 * np.pi))))
    return cherns, float(gap)


def main():
    out = {}
    print("[pump-protection theorem]  spin-S pump: extreme-band Chern = 2S\n")
    print("   S   d=2S+1   Chern bands              |C|_max   2S")
    res = {}
    for S in [0.5, 1.0, 1.5]:
        cherns, gap = chern_and_gap(S)
        cmax = max(abs(c) for c in cherns)
        print(
            f"  {S:3}    {int(2*S+1):3d}    {str(sorted(cherns, reverse=True)):24s} "
            f"{cmax:5d}   {int(2*S)}"
        )
        assert cmax == int(2 * S)
        res[str(S)] = {
            "chern": sorted(cherns, reverse=True),
            "Cmax": cmax,
            "2S": int(2 * S),
        }
    out["spin_scan"] = res

    # qutrit = the substrate carrier
    cherns1, gap1 = chern_and_gap(1.0)
    print(
        f"\n[qutrit S=1 (the photon's 3 modes)]  Chern {sorted(cherns1, reverse=True)}"
        f", pump quantum |C| = 2S = q-1 = lambda = 2"
    )
    print(
        f"  min Floquet gap over the two-tone torus: Delta_min = {gap1:.4f} "
        f"(drive units)"
    )
    print(
        f"  SPEC: omega_1, omega_2 << Delta_min (adiabatic); k_B T, hbar/T2 << "
        f"Delta_min (coherent)"
    )
    assert max(abs(c) for c in cherns1) == 2 and gap1 > 0.5
    out["qutrit_pump_quantum"] = 2
    out["qutrit_min_floquet_gap"] = round(gap1, 4)

    print("\nRESULT: the demonstrator's pump quantum is a theorem, not a fit. A")
    print("  (2S+1)-level qudit driven by two incommensurate tones has extreme-band")
    print("  Chern number 2S, so the pump transfers exactly 2S quanta per cycle; for")
    print("  the qutrit (the photon's three modes, S=1) that is 2S = q-1 = lambda =")
    print("  2. The quantization is protected by a finite Floquet gap (Delta_min ~")
    print("  O(1) in drive units), which sets a concrete buildable spec: slow two-")
    print("  tone drive and coherence/temperature below the gap. Measuring 2 quanta")
    print("  per cycle confirms lambda; anything else falsifies the substrate.")

    out["summary"] = (
        "theorem: spin-S two-tone pump has extreme-band Chern = 2S "
        "(verified S=1/2,1,3/2: |C|max=1,2,3); qutrit S=1 -> pump "
        "quantum 2S=q-1=lambda=2, protected by min Floquet gap "
        f"Delta_min~{round(gap1,2)} (drive units). Spec: omega<<gap "
        "(adiabatic), k_BT/decoherence<<gap (coherent). Falsifier: pump "
        "quantum != 2."
    )
    out["sources"] = [
        "Martin-Refael-Halperin topological frequency conversion (PRX "
        "2017); spin-S monopole Chern = 2S; Fukui-Hatsugai; "
        "w33_demonstrator_measures_substrate.py"
    ]
    with open("data/w33_pump_protection_theorem.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_pump_protection_theorem.json")


if __name__ == "__main__":
    main()
