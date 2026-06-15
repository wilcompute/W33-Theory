#!/usr/bin/env python3
"""
BT1143 -- explicit curvature-matrix verifier for the K3 a4 coefficients.

This is the promised matrix check behind BT1141.  It chooses one algebraic
Ricci-flat 4D curvature tensor, computes the spin and exterior-bundle curvature
matrices explicitly, and recovers

    omega_spin  = -1/2,
    omega_hodge = -4,
    e2_hodge    = 1.

Because the contractions are O(4)-invariant quadratic forms on the Ricci-flat
(Weyl) curvature module, checking one nonzero Ricci-flat Weyl component fixes
the scalar ratios used by the convention table.
"""

from __future__ import annotations

import json
from fractions import Fraction

import numpy as np

N = 4
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
# Diagonal curvature operator on Lambda^2 with zero Ricci contraction.
PAIR_VALUES = [1, -1, 0, 0, -1, 1]


def frac(x: complex | float) -> str:
    return str(Fraction(float(np.real_if_close(x))).limit_denominator())


def curvature_tensor() -> np.ndarray:
    R = np.zeros((N, N, N, N), dtype=float)
    for (a, b), val in zip(PAIRS, PAIR_VALUES):
        R[a, b, a, b] = val
        R[b, a, a, b] = -val
        R[a, b, b, a] = -val
        R[b, a, b, a] = val
    return R


def gamma_matrices() -> list[np.ndarray]:
    s0 = np.array([[1, 0], [0, 1]], dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [np.kron(s1, s0), np.kron(s2, s0), np.kron(s3, s1), np.kron(s3, s2)]


def wedge_matrix(k: int) -> np.ndarray:
    dim = 1 << N
    M = np.zeros((dim, dim), dtype=float)
    for mask in range(dim):
        if (mask >> k) & 1:
            continue
        sign = (-1) ** (bin(mask & ((1 << k) - 1)).count("1"))
        M[mask | (1 << k), mask] = sign
    return M


def contraction_matrix(k: int) -> np.ndarray:
    dim = 1 << N
    M = np.zeros((dim, dim), dtype=float)
    for mask in range(dim):
        if not ((mask >> k) & 1):
            continue
        sign = (-1) ** (bin(mask & ((1 << k) - 1)).count("1"))
        M[mask & ~(1 << k), mask] = sign
    return M


def exterior_rho(A: np.ndarray, eps: list[np.ndarray], iot: list[np.ndarray]) -> np.ndarray:
    M = np.zeros((1 << N, 1 << N), dtype=float)
    for k in range(N):
        for l in range(N):
            M += A[k, l] * eps[k] @ iot[l]
    return M


def main() -> None:
    R = curvature_tensor()
    norm = float(np.sum(R * R))
    ric = np.einsum("abad->bd", R)

    gam = gamma_matrices()
    spin_trace = 0j
    for i in range(N):
        for j in range(N):
            omega = np.zeros((4, 4), dtype=complex)
            for a in range(N):
                for b in range(N):
                    omega += 0.25 * R[i, j, a, b] * gam[a] @ gam[b]
            spin_trace += np.trace(omega @ omega)
    omega_spin = spin_trace / norm

    eps = [wedge_matrix(k) for k in range(N)]
    iot = [contraction_matrix(k) for k in range(N)]
    cliff = [eps[k] - iot[k] for k in range(N)]
    Omega = {}
    hodge_trace = 0.0
    for i in range(N):
        for j in range(N):
            A = np.zeros((N, N), dtype=float)
            for k in range(N):
                for l in range(N):
                    A[k, l] = R[i, j, l, k]
            Omega[(i, j)] = exterior_rho(A, eps, iot)
            hodge_trace += np.trace(Omega[(i, j)] @ Omega[(i, j)])
    omega_hodge = hodge_trace / norm

    E_hodge = np.zeros((1 << N, 1 << N), dtype=float)
    for i in range(N):
        for j in range(N):
            E_hodge += 0.5 * cliff[i] @ cliff[j] @ Omega[(i, j)]
    e2_hodge = np.trace(E_hodge @ E_hodge) / norm

    result = {
        "bt": 1143,
        "title": "explicit curvature-matrix verifier for spin and Hodge a4 coefficients",
        "curvature_operator_diagonal_on_Lambda2": PAIR_VALUES,
        "riemann_norm_squared": frac(norm),
        "ricci_matrix": ric.astype(int).tolist(),
        "derived_coefficients": {
            "omega_spin": frac(omega_spin),
            "omega_hodge": frac(omega_hodge),
            "e2_hodge": frac(e2_hodge),
        },
        "checks": {
            "ricci_flat": bool(np.allclose(ric, 0)),
            "norm_is_16": bool(np.isclose(norm, 16)),
            "omega_spin_is_minus_half": frac(omega_spin) == "-1/2",
            "omega_hodge_is_minus_four": frac(omega_hodge) == "-4",
            "e2_hodge_is_one": frac(e2_hodge) == "1",
        },
    }
    result["checks"]["all_checks_pass"] = all(result["checks"].values())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
