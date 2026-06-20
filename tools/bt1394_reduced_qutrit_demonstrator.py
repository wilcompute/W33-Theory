#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
omega = np.exp(2j * np.pi / 3)


def kron(a, b):
    return np.kron(a, b)


def qutrit_ops():
    I = np.eye(3, dtype=complex)
    X = np.roll(I, 1, axis=0)
    Z = np.diag([1, omega, omega**2])
    F = np.array([[omega ** (i * j) for j in range(3)] for i in range(3)], dtype=complex) / math.sqrt(3)
    return I, X, Z, F


def bell_qutrit():
    psi = np.zeros(9, dtype=complex)
    for i in range(3):
        psi[3 * i + i] = 1 / math.sqrt(3)
    return psi


def visibility(psi, U):
    amp = np.vdot(psi, U @ psi)
    return float(abs(amp) ** 2)


def route_control_state():
    I, X, Z, _F = qutrit_ops()
    omega_bell = bell_qutrit()
    r = np.ones(3, dtype=complex) / math.sqrt(3)
    psi = np.kron(r, omega_bell)
    blocks = [I, Z, X]
    U = np.zeros((27, 27), dtype=complex)
    for rr, B in enumerate(blocks):
        proj = np.zeros((3, 3), dtype=complex)
        proj[rr, rr] = 1
        U += np.kron(proj, kron(B, I))
    out = U @ psi
    rho_R = np.zeros((3, 3), dtype=complex)
    for r1 in range(3):
        for r2 in range(3):
            s = 0j
            for ab in range(9):
                s += out[r1 * 9 + ab] * np.conj(out[r2 * 9 + ab])
            rho_R[r1, r2] = s
    purity = float(np.real(np.trace(rho_R @ rho_R)))
    coherence_l1 = float(np.sum(np.abs(rho_R - np.diag(np.diag(rho_R)))))
    return out, rho_R, purity, coherence_l1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1394_reduced_qutrit_demonstrator.json")
    ns = ap.parse_args()
    I, X, Z, F = qutrit_ops()
    psi = bell_qutrit()
    vis = {
        "I_tensor_I": visibility(psi, kron(I, I)),
        "F_tensor_F_conj": visibility(psi, kron(F, np.conj(F))),
        "X_tensor_I": visibility(psi, kron(X, I)),
        "Z_tensor_I": visibility(psi, kron(Z, I)),
    }
    out, rho_R, purity, coherence_l1 = route_control_state()
    route_probs = [float(np.real(rho_R[i, i])) for i in range(3)]
    checks = {
        "bell_norm_1": abs(float(np.vdot(psi, psi).real) - 1.0) < 1e-12,
        "V_I_is_1": abs(vis["I_tensor_I"] - 1.0) < 1e-12,
        "V_F_is_1_over_3": abs(vis["F_tensor_F_conj"] - 1.0 / 3.0) < 1e-12,
        "V_X_is_0": abs(vis["X_tensor_I"]) < 1e-12,
        "V_Z_is_0": abs(vis["Z_tensor_I"]) < 1e-12,
        "route_probs_uniform": all(abs(p - 1.0 / 3.0) < 1e-12 for p in route_probs),
        "route_reduced_state_maximally_mixed": abs(purity - 1.0 / 3.0) < 1e-12 and coherence_l1 < 1e-12,
        "controlled_state_norm_1": abs(float(np.vdot(out, out).real) - 1.0) < 1e-12,
    }
    result = {
        "bt": 1394,
        "title": "Reduced photonic Bell-qutrit route demonstrator simulator",
        "verified": all(checks.values()),
        "checks": checks,
        "bell_qutrit": "|Omega>=(|00>+|11>+|22>)/sqrt(3)",
        "visibility_targets": {"V(I)": 1.0, "V(F3)": 1.0/3.0, "V(X)": 0.0, "V(Z)": 0.0},
        "visibility_results": vis,
        "route_control": {
            "operation": "|0><0|⊗I + |1><1|⊗Z + |2><2|⊗X on Bell-qutrit fiber leg",
            "route_probabilities": route_probs,
            "route_reduced_density_real": np.real(rho_R).round(12).tolist(),
            "route_reduced_density_imag": np.imag(rho_R).round(12).tolist(),
            "route_purity": purity,
            "route_l1_coherence": coherence_l1
        },
        "interpretation": "The minimal demonstrator verifies Bell-qutrit signatures and route-controlled Clifford transport. In the fully entangling route-control setting, tracing out the Bell legs leaves the route register maximally mixed; therefore route coherence must be certified by an interferometric/quantum-erasure readout, not by the reduced route density matrix alone."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1394, "verified": result["verified"], "V_F": vis["F_tensor_F_conj"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
