#!/usr/bin/env python3
"""Qutrit modular A2 clock + relational/event-time certificate."""
from __future__ import annotations

import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_modular_a2_event_clock.json"
TOL = 2e-12

# Repo BT943 Weyl matrices in simple-root coordinates.
BT943_S1 = np.array([[-1, 1], [0, 1]], dtype=int)
BT943_S2 = np.array([[1, 0], [1, -1]], dtype=int)

# Population transpositions acting on h=(log p0/p1, log p1/p2).
M01 = np.array([[-1, 0], [1, 1]], dtype=int)
M12 = np.array([[1, 1], [0, -1]], dtype=int)

assert np.array_equal(M01.T, BT943_S1)
assert np.array_equal(M12.T, BT943_S2)


def closure2(gens):
    eye = np.eye(2, dtype=int)
    seen = {tuple(eye.reshape(-1)): eye}
    frontier = [eye]
    while frontier:
        A = frontier.pop()
        for G in gens:
            B = A @ G
            key = tuple(int(x) for x in B.reshape(-1))
            if key not in seen:
                seen[key] = B
                frontier.append(B)
    return list(seen.values())


def pure_bures_angle(psi, phi):
    ov = abs(np.vdot(psi, phi))
    ov = min(1.0, max(0.0, float(ov)))
    return math.acos(ov)


def cyclic_history_state():
    d = 3
    X = np.zeros((d,d), dtype=complex)
    for j in range(d):
        X[(j+1)%d, j] = 1
    psi0 = np.array([1,0,0], dtype=complex)
    hist = np.zeros(d*d, dtype=complex)
    states = []
    for n in range(d):
        psi = np.linalg.matrix_power(X, n) @ psi0
        states.append(psi)
        clock = np.zeros(d, dtype=complex)
        clock[n] = 1
        hist += np.kron(clock, psi) / np.sqrt(d)
    return X, psi0, hist, states


def main():
    W = closure2([M01, M12])
    assert len(W) == 6
    assert len(closure2([BT943_S1, BT943_S2])) == 6


    # A faithful nontracial state gives six directed modular frequencies.
    p = np.array([1/2, 1/3, 1/6], dtype=float)
    assert abs(p.sum() - 1.0) < TOL
    logp = np.log(p)
    h = np.array([logp[0]-logp[1], logp[1]-logp[2]])
    freqs = {}
    values = []
    for i in range(3):
        for j in range(3):
            w = float(logp[j] - logp[i])
            freqs[f"E{i}{j}"] = w
            if i != j:
                values.append(w)
    assert sum(abs(freqs[f"E{i}{i}"]) for i in range(3)) < TOL

    expected = sorted([
        h[0], -h[0],
        h[1], -h[1],
        h[0]+h[1], -(h[0]+h[1]),
    ])
    assert np.allclose(sorted(values), expected, atol=TOL)


    # Tracial state collapses every modular frequency to zero.
    ptr = np.ones(3)/3
    tr_freqs = [
        float(np.log(ptr[j]) - np.log(ptr[i]))
        for i in range(3) for j in range(3)
    ]
    assert max(abs(x) for x in tr_freqs) < TOL

    # Page-Wootters three-step history: globally stationary under paired shift.
    X, psi0, hist, states = cyclic_history_state()
    paired = np.kron(X, X)
    stationarity_error = float(np.linalg.norm(paired @ hist - hist))
    assert stationarity_error < TOL

    # Event-time as state-space path length: identity gives zero; a closed
    # three-step orthogonal cycle returns to start yet has positive length.
    cycle_states = states + [states[0]]
    event_length = sum(
        pure_bures_angle(cycle_states[i], cycle_states[i+1])
        for i in range(3)
    )
    idle_length = sum(pure_bures_angle(states[0], states[0]) for _ in range(3))
    assert abs(event_length - 3*math.pi/2) < TOL
    assert abs(idle_length) < TOL


    eq_affinity = 0.0
    driven_affinity = 3*math.log(2.0)
    assert driven_affinity > 0

    out = {
        "schema": "w33.20260924.modular_a2_event_clock.v1",
        "status": "PASS_MODULAR_A2_RELATIONAL_EVENT_CLOCK",
        "modular_qutrit": {
            "faithful_probabilities": p.tolist(),
            "log_ratio_coordinates": h.tolist(),
            "three_diagonal_zero_modes": True,
            "six_offdiagonal_frequencies": freqs,
            "root_pattern": "plus/minus h1, h2, and h1+h2",
            "tracial_state_all_frequencies_zero": True,
        },

        "A2_weyl_bridge": {
            "population_swap_01_on_log_ratios": M01.tolist(),
            "population_swap_12_on_log_ratios": M12.tolist(),
            "BT943_simple_reflection_1": BT943_S1.tolist(),
            "BT943_simple_reflection_2": BT943_S2.tolist(),
            "exact_relation": "M01^T=S1 and M12^T=S2",
            "interpretation": (
                "the qutrit modular log-ratio plane carries the contragredient "
                "A2 Weyl representation already used in BT943"
            ),
            "group_order": len(W),
        },
        "relational_history": {
            "history": "1/sqrt(3) sum_n |n>_C tensor X^n|0>_S",
            "paired_stationarity": "(X_C tensor X_S)|Psi>=|Psi> for the chosen forward-shift convention",
            "stationarity_error": stationarity_error,
            "conditional_states": ["|0>", "|1>", "|2>"],
        },

        "event_time": {
            "functional": "sum of pure-state Bures angles along the update path",
            "idle_three_updates": idle_length,
            "closed_three_state_cycle": event_length,
            "closed_cycle_endpoint_equals_start": True,
            "lesson": "elapsed distinguishable change is not endpoint displacement or operation count",
        },
        "arrow": {
            "equilibrium_cycle_affinity": eq_affinity,
            "biased_two_to_one_cycle_affinity": driven_affinity,
            "lesson": "arrow/orientation is separate from reversible event-time",
        },
        "boundaries": [
            "This proves a local qutrit modular/A2 correspondence, not yet the external E8 A2 identification.",
            "Bures path length is an operational event-time functional, not a derivation of Lorentzian proper time.",
            "A photon has no rest-frame proper-time clock; laboratory or relational clock variables are required.",
        ],
        "literature": [
            "Connes and Rovelli, gr-qc/9406019, thermal time hypothesis",
            "Page-Wootters relational time and interacting extension, PRL 131, 140202 (2023)",
            "Deffner and Campbell, J. Phys. A 50, 453001 (2017), quantum speed limits",
        ],
    }

    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "A2_group_order": len(W),
        "stationarity_error": stationarity_error,
        "idle_event_time": idle_length,
        "closed_cycle_event_time": event_length,
        "cycle_affinity": driven_affinity,
    }, indent=2))


if __name__ == "__main__":
    main()
