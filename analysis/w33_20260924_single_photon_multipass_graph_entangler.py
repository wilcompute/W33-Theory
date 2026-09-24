#!/usr/bin/env python3
"""One flying qutrit ancilla compiles even-memory graph entanglers.

For the fixed ADQC interaction E=(F_A^dagger tensor F_R)CZ, let one ancilla
visit 2n memories in order and then be measured computationally.  The resulting
branch is a unitary weighted graph entangler up to a known local X frame.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_single_photon_multipass_graph_entangler.json"
D = 3
omega = np.exp(2j * np.pi / D)
TOL = 3e-12
def alternating_odd_sum(r, j):
    """a_j = r_{2j-1} - r_{2j-3} + ... in one-based notation."""
    return sum(((-1) ** (j - h)) * r[2 * h - 2] for h in range(1, j + 1)) % D


def phase_exponent(r, m):
    k = len(r)
    assert k % 2 == 0
    n = k // 2
    a = [alternating_odd_sum(r, j) for j in range(1, n + 1)]
    q = sum(a[j - 1] * r[2 * j - 1] for j in range(1, n + 1))
    q -= m * a[-1]
    return q % D


def adjacency_for_even_sweep(k):
    assert k % 2 == 0
    n = k // 2
    A = np.zeros((k, k), dtype=int)
    for j in range(1, n + 1):
        even = 2 * j - 1
        for h in range(1, j + 1):
            odd = 2 * h - 2
            weight = (-1) ** (j - h)
            A[odd, even] = A[even, odd] = weight % D
    return A
def output_x_frame(k, m):
    """X exponents after pulling the measurement-dependent Z phases through F."""
    assert k % 2 == 0
    n = k // 2
    frame = [0] * k
    for h in range(1, n + 1):
        odd = 2 * h - 2
        frame[odd] = (m * ((-1) ** (n - h))) % D
    return frame


def direct_basis_amplitude(r, s, m):
    """Dynamic-program the exact ancilla path sum for one basis matrix element."""
    k = len(r)
    # ancilla begins in |+>: amplitudes 1/sqrt(3)
    v = np.ones(D, dtype=complex) / np.sqrt(D)
    for ri, si in zip(r, s):
        nxt = np.zeros(D, dtype=complex)
        for a_prev in range(D):
            for a_new in range(D):
                exponent = a_prev * ri - a_new * a_prev + si * ri
                nxt[a_new] += v[a_prev] * omega**exponent / D
        v = nxt
    return v[m]
def predicted_basis_amplitude(r, s, m):
    k = len(r)
    assert k % 2 == 0
    local_fourier = omega ** sum(si * ri for si, ri in zip(s, r)) / (D ** (k / 2))
    graph_phase = omega ** phase_exponent(r, m)
    return local_fourier * graph_phase / np.sqrt(D)


def verify_k(k, samples=120):
    assert k % 2 == 0
    rng = np.random.default_rng(10942 + k)
    errors = []
    for _ in range(samples):
        r = tuple(int(x) for x in rng.integers(0, D, size=k))
        s = tuple(int(x) for x in rng.integers(0, D, size=k))
        for m in range(D):
            got = direct_basis_amplitude(r, s, m)
            want = predicted_basis_amplitude(r, s, m)
            errors.append(abs(got - want))
    max_error = max(errors)
    assert max_error < TOL
    A = adjacency_for_even_sweep(k)
    # Quadratic phase is sum_{i<j} A_ij r_i r_j.
    for _ in range(samples):
        r = tuple(int(x) for x in rng.integers(0, D, size=k))
        quad = sum(A[i, j] * r[i] * r[j] for i in range(k) for j in range(i + 1, k)) % D
        no_measurement = phase_exponent(r, 0)
        assert quad == no_measurement
    return max_error, A
rows = []
for k in (2, 4, 6, 8):
    max_error, A = verify_k(k)
    edges = [
        {"u": i, "v": j, "weight_mod3": int(A[i, j])}
        for i in range(k) for j in range(i + 1, k) if A[i, j]
    ]
    rows.append({
        "memory_qutrits": k,
        "branch_probability": 1 / D,
        "verified_random_basis_amplitudes_per_outcome": 120,
        "max_amplitude_error": max_error,
        "weighted_edges": edges,
        "edge_count": len(edges),
        "measurement_frames": {str(m): output_x_frame(k, m) for m in range(D)},
    })

assert [r["edge_count"] for r in rows] == [1, 3, 6, 10]
out = {
    "schema": "w33.20260924.single_photon_multipass_graph_entangler.v1",
    "status": "PASS_SINGLE_PHOTON_EVEN_SWEEP_GRAPH_ENTANGLER",
    "theorem": {
        "setup": "one |+> qutrit ancilla visits memories R1,...,R_2n via the same fixed E_AR, then is measured in Z",
        "branch": (
            "K_m=(1/sqrt(3)) X_frame(m) F^(tensor 2n) D_G, "
            "where D_G is a weighted qutrit graph-phase Clifford"
        ),
        "phase_law": (
            "q_m(r)=sum_{j=1}^n a_j r_(2j) - m a_n mod 3, "
            "a_j=sum_{h=1}^j (-1)^(j-h) r_(2h-1)"
        ),
        "graph_edges": (
            "edge (2h-1,2j) has weight (-1)^(j-h) mod 3 for 1<=h<=j<=n"
        ),
        "edge_count": "n(n+1)/2",
        "outcome_probability": "1/3 independent of the memory input",
        "odd_sweep_boundary": (
            "An odd number of visited memories does not yield a full-rank unitary branch "
            "under the same final computational measurement."
        ),
    },
    "verified_sweeps": rows,
    "network_interpretation": {
        "result": (
            "A single flying photonic qutrit can compile a nontrivial multi-memory "
            "Clifford graph entangler in one coherent sweep, followed only by frame update."
        ),
        "comparison": (
            "This is structurally analogous to single-photon network-bus proposals where "
            "one photon mediates controlled phases across multiple stationary nodes, but "
            "the qutrit phase law here is derived directly from the ADQC interaction."
        ),
        "holonet_opportunity": (
            "Route selection can choose which stationary memories participate in a sweep; "
            "the existing routing graph can therefore be studied as a graph-entangler compiler."
        ),
    },
    "boundary": (
        "Exact circuit algebra only. It does not prove a physical qutrit cavity interaction, "
        "photon survival across many nodes, or fault tolerance. The useful branch is Clifford; "
        "non-Clifford power still comes from the programmed analyzer of the companion theorem."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "status": out["status"],
    "sweeps": [{"k": r["memory_qutrits"], "edges": r["edge_count"],
                "error": r["max_amplitude_error"]} for r in rows],
}, indent=2))
