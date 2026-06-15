#!/usr/bin/env python3
"""BT1146 -- random Ricci-flat Weyl-basis verifier.

Build the full 10-dimensional linear space of 4D Ricci-flat algebraic curvature
tensors and sample random integer combinations.  For every nonzero sample the
matrix contractions recover the BT1143/BT1141 ratios

  omega_spin=-1/2, omega_hodge=-4, e2_hodge=1.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

import numpy as np
import sympy as sp

N = 4
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}
VARS = [(i, j) for i in range(6) for j in range(i, 6)]


def R_expr(x, a, b, c, d):
    if a == b or c == d:
        return 0
    s1, p = (1, (a, b)) if a < b else (-1, (b, a))
    s2, q = (1, (c, d)) if c < d else (-1, (d, c))
    i, j = PAIR_INDEX[p], PAIR_INDEX[q]
    if i > j:
        i, j = j, i
    return s1 * s2 * x[VARS.index((i, j))]


def nullspace_basis():
    x = [sp.Symbol(f"x{k}") for k in range(len(VARS))]
    eqs = []
    for a, b, c, d in itertools.product(range(N), repeat=4):
        val = R_expr(x, a, b, c, d) + R_expr(x, a, c, d, b) + R_expr(x, a, d, b, c)
        if val != 0:
            eqs.append(val)
    for b, d in itertools.product(range(N), repeat=2):
        val = sum(R_expr(x, a, b, a, d) for a in range(N))
        if val != 0:
            eqs.append(val)
    mat = sp.Matrix([[sp.expand(eq).coeff(s) for s in x] for eq in eqs])
    return [np.array([float(v) for v in vec]) for vec in mat.nullspace()]


def tensor_from_vec(vec):
    M = np.zeros((6, 6), dtype=float)
    for val, (i, j) in zip(vec, VARS):
        M[i, j] = val
        M[j, i] = val
    R = np.zeros((N, N, N, N), dtype=float)
    for a, b, c, d in itertools.product(range(N), repeat=4):
        if a == b or c == d:
            continue
        s1, p = (1, (a, b)) if a < b else (-1, (b, a))
        s2, q = (1, (c, d)) if c < d else (-1, (d, c))
        R[a, b, c, d] = s1 * s2 * M[PAIR_INDEX[p], PAIR_INDEX[q]]
    return R


def gamma_matrices():
    s0 = np.array([[1, 0], [0, 1]], dtype=complex)
    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    return [np.kron(s1, s0), np.kron(s2, s0), np.kron(s3, s1), np.kron(s3, s2)]


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


def ratios(R):
    norm = np.sum(R * R)
    gam = gamma_matrices()
    spin_trace = 0j
    for i in range(N):
        for j in range(N):
            om = np.zeros((4, 4), dtype=complex)
            for a in range(N):
                for b in range(N):
                    om += 0.25 * R[i, j, a, b] * gam[a] @ gam[b]
            spin_trace += np.trace(om @ om)
    eps = [wedge(k) for k in range(N)]
    iot = [contract(k) for k in range(N)]
    cliff = [eps[k] - iot[k] for k in range(N)]
    Omega = {}
    htrace = 0.0
    for i in range(N):
        for j in range(N):
            A = np.zeros((N, N), dtype=float)
            for k in range(N):
                for l in range(N):
                    A[k, l] = R[i, j, l, k]
            Omega[(i, j)] = rho(A, eps, iot)
            htrace += np.trace(Omega[(i, j)] @ Omega[(i, j)])
    E = np.zeros((16, 16), dtype=float)
    for i in range(N):
        for j in range(N):
            E += 0.5 * cliff[i] @ cliff[j] @ Omega[(i, j)]
    return (
        str(Fraction(float(np.real_if_close(spin_trace / norm))).limit_denominator()),
        str(Fraction(float(htrace / norm)).limit_denominator()),
        str(Fraction(float(np.trace(E @ E) / norm)).limit_denominator()),
    )


def main():
    basis = nullspace_basis()
    samples = []
    for seed in range(1, 8):
        rng = np.random.default_rng(seed)
        coeff = rng.integers(-3, 4, size=len(basis))
        if not coeff.any():
            coeff[0] = 1
        vec = sum(c * b for c, b in zip(coeff, basis))
        R = tensor_from_vec(vec)
        samples.append({
            "seed": seed,
            "norm": str(Fraction(float(np.sum(R * R))).limit_denominator()),
            "ricci_flat": bool(np.allclose(np.einsum("abad->bd", R), 0)),
            "ratios": ratios(R),
        })
    ok = all(s["ricci_flat"] and s["ratios"] == ("-1/2", "-4", "1") for s in samples)
    print(json.dumps({"bt": 1146, "basis_dimension": len(basis), "samples": samples, "all_checks_pass": ok}, indent=2))


if __name__ == "__main__":
    main()
