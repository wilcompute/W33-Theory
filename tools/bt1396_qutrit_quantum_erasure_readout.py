#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
omega = np.exp(2j * np.pi / 3)


def qutrit_ops():
    I = np.eye(3, dtype=complex)
    X = np.roll(I, 1, axis=0)
    Z = np.diag([1, omega, omega**2])
    F = np.array([[omega ** (i * j) for j in range(3)] for i in range(3)], dtype=complex) / math.sqrt(3)
    return I, X, Z, F


def bell_qutrit():
    psi = np.zeros(9, dtype=complex)
    for i in range(3):
        psi[3*i+i] = 1 / math.sqrt(3)
    return psi


def reduced_route_density(state):
    rho = np.zeros((3, 3), dtype=complex)
    for r1 in range(3):
        for r2 in range(3):
            rho[r1, r2] = sum(state[r1*9 + b] * np.conj(state[r2*9 + b]) for b in range(9))
    return rho


def l1_coherence(rho):
    return float(np.sum(np.abs(rho - np.diag(np.diag(rho)))))


def route_state_after_projection(full_state, bell_projector):
    amp = np.zeros(3, dtype=complex)
    for r in range(3):
        block = full_state[r*9:(r+1)*9]
        amp[r] = np.vdot(bell_projector, block)
    p = float(np.vdot(amp, amp).real)
    if p > 0:
        amp = amp / math.sqrt(p)
    return amp, p


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1396_qutrit_quantum_erasure_readout.json")
    ns = ap.parse_args()
    I, X, Z, F = qutrit_ops()
    base = bell_qutrit()
    bell_branches = [np.kron(B, I) @ base for B in [I, Z, X]]
    overlaps = [[complex(np.vdot(a, b)) for b in bell_branches] for a in bell_branches]
    full = np.concatenate([bell_branches[r] / math.sqrt(3) for r in range(3)])
    rho_trace = reduced_route_density(full)
    eraser = sum(bell_branches) / math.sqrt(3)
    route_erased, p_erased = route_state_after_projection(full, eraser)
    rho_erased = np.outer(route_erased, np.conj(route_erased))
    port_probs = [float(abs(x)**2) for x in (np.conj(F).T @ route_erased)]
    which_route_projector = bell_branches[0]
    route_marked, p_marked = route_state_after_projection(full, which_route_projector)
    rho_marked = np.outer(route_marked, np.conj(route_marked))
    checks = {
        "bell_branches_orthonormal": max(abs(overlaps[i][j] - (1 if i == j else 0)) for i in range(3) for j in range(3)) < 1e-12,
        "trace_route_maximally_mixed": abs(float(np.trace(rho_trace @ rho_trace).real) - 1/3) < 1e-12,
        "eraser_probability_one_third": abs(p_erased - 1/3) < 1e-12,
        "eraser_restores_pure_route": abs(float(np.trace(rho_erased @ rho_erased).real) - 1) < 1e-12,
        "eraser_l1_coherence_two": abs(l1_coherence(rho_erased) - 2) < 1e-12,
        "eraser_routes_to_single_interference_port": max(port_probs) > 1 - 1e-12 and min(port_probs) < 1e-12,
        "which_route_has_no_coherence": l1_coherence(rho_marked) < 1e-12 and abs(p_marked - 1/3) < 1e-12,
    }
    result = {
        "bt": 1396,
        "title": "Qutrit route-control quantum-erasure readout",
        "verified": all(checks.values()),
        "checks": checks,
        "readout": {
            "branches": ["Omega", "Z Omega", "X Omega"],
            "pre_readout_route_purity": float(np.trace(rho_trace @ rho_trace).real),
            "eraser_projector": "(|Omega> + |Z Omega> + |X Omega>)/sqrt(3)",
            "eraser_success_probability": p_erased,
            "conditional_route_density_real": np.real(rho_erased).round(12).tolist(),
            "conditional_route_density_imag": np.imag(rho_erased).round(12).tolist(),
            "conditional_route_l1_coherence": l1_coherence(rho_erased),
            "route_interference_port_probabilities": port_probs,
            "which_route_success_probability": p_marked,
            "which_route_l1_coherence": l1_coherence(rho_marked)
        },
        "interpretation": "The route register is mixed if the Bell legs are discarded, but a Bell-branch eraser measurement restores a pure coherent qutrit route state with l1 coherence 2 and deterministic route interferometer output. This is the missing readout for the reduced photonic demonstrator."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1396, "verified": result["verified"], "p_eraser": p_erased}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
