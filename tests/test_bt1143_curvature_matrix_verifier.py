"""BT1143 regression tests for explicit curvature-matrix coefficient verifier."""

import numpy as np
from fractions import Fraction

N = 4
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PAIR_VALUES = [1, -1, 0, 0, -1, 1]


def curvature_tensor():
    R = np.zeros((N, N, N, N), dtype=float)
    for (a, b), val in zip(PAIRS, PAIR_VALUES):
        R[a, b, a, b] = val
        R[b, a, a, b] = -val
        R[a, b, b, a] = -val
        R[b, a, b, a] = val
    return R


def wedge(k):
    M = np.zeros((16, 16), dtype=float)
    for mask in range(16):
        if (mask >> k) & 1:
            continue
        sign = (-1) ** (bin(mask & ((1 << k) - 1)).count("1"))
        M[mask | (1 << k), mask] = sign
    return M


def contract(k):
    M = np.zeros((16, 16), dtype=float)
    for mask in range(16):
        if not ((mask >> k) & 1):
            continue
        sign = (-1) ** (bin(mask & ((1 << k) - 1)).count("1"))
        M[mask & ~(1 << k), mask] = sign
    return M


def rho(A, eps, iot):
    M = np.zeros((16, 16), dtype=float)
    for k in range(N):
        for l in range(N):
            M += A[k, l] * eps[k] @ iot[l]
    return M


def test_curvature_tensor_is_ricci_flat_with_norm_16():
    R = curvature_tensor()
    ric = np.einsum("abad->bd", R)
    assert np.allclose(ric, 0)
    assert Fraction(float(np.sum(R * R))).limit_denominator() == Fraction(16)


def test_hodge_matrix_coefficients_are_derived():
    R = curvature_tensor()
    norm = np.sum(R * R)
    eps = [wedge(k) for k in range(N)]
    iot = [contract(k) for k in range(N)]
    cliff = [eps[k] - iot[k] for k in range(N)]
    Omega = {}
    omega_trace = 0.0
    for i in range(N):
        for j in range(N):
            A = np.zeros((N, N), dtype=float)
            for k in range(N):
                for l in range(N):
                    A[k, l] = R[i, j, l, k]
            Omega[(i, j)] = rho(A, eps, iot)
            omega_trace += np.trace(Omega[(i, j)] @ Omega[(i, j)])
    E = np.zeros((16, 16), dtype=float)
    for i in range(N):
        for j in range(N):
            E += 0.5 * cliff[i] @ cliff[j] @ Omega[(i, j)]
    assert Fraction(float(omega_trace / norm)).limit_denominator() == Fraction(-4)
    assert Fraction(float(np.trace(E @ E) / norm)).limit_denominator() == Fraction(1)
