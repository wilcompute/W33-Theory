from __future__ import annotations

import math

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form

from pass1370_1374 import modular_radicals

from .common import capture, denominator_lcm, factor_kernel_key, sha


def ambient_multiplication(g):
    tensor = np.asarray(g["tensor"], dtype=np.int64)
    left = [sp.Matrix(tensor[:, a, :].tolist()) for a in range(83)]
    right = [sp.Matrix(tensor[:, :, b].tolist()) for b in range(83)]
    return tensor, left, right


def linear_combination(mats, coeffs):
    out = sp.zeros(83)
    for c, M in zip(coeffs, mats):
        if c:
            out += sp.Rational(c) * M
    return out


def order_left_matrices(L, ambient_left):
    Linv = L.inv()
    mats = []
    for a in range(83):
        La = linear_combination(ambient_left, L[:, a])
        M = (Linv * La * L).applyfunc(sp.cancel)
        assert all(sp.Rational(x).q == 1 for x in M)
        mats.append(np.asarray(M.tolist(), dtype=np.int64))
    return mats


def radical_basis(left_mats, p):
    factors = modular_radicals.composition_factors([M % p for M in left_mats], p)
    equations = []
    for F in factors:
        d = F[0].shape[0]
        for i in range(d):
            for j in range(d):
                equations.append([int(F[a][i, j]) for a in range(83)])
    J = modular_radicals.nullspace(np.asarray(equations, dtype=np.int64) % p, p)
    classes = {}
    for F in factors:
        key = factor_kernel_key(F, p)
        classes.setdefault(key, F[0].shape[0])
    return J, sorted(int(x) for x in classes.values())


def ideal_lattice_in_order(J, p):
    G = sp.Matrix.hstack(p * sp.eye(83), sp.Matrix(J.T.tolist()))
    H = hermite_normal_form(G)
    assert H.shape == (83, 83) and H.det() != 0
    return H


def integral_matrix(M):
    assert all(sp.Rational(x).q == 1 for x in M)
    return sp.Matrix(M.rows, M.cols, lambda i, j: int(M[i, j]))


def two_sided_idealizer(I, ambient_left, ambient_right):
    Iinv = I.inv()
    condition_rows = []
    denominator = 1
    condition_mats = []
    for j in range(83):
        h = I[:, j]
        for mats in (ambient_left, ambient_right):
            Mh = linear_combination(mats, h)
            R = (Iinv * Mh).applyfunc(sp.cancel)
            condition_mats.append(R)
            denominator = math.lcm(denominator, denominator_lcm(R))
    for R in condition_mats:
        for i in range(83):
            condition_rows.append([int(sp.Rational(denominator * R[i, j])) for j in range(83)])
    for i in range(83):
        row = [0] * 83
        row[i] = denominator
        condition_rows.append(row)
    G = sp.Matrix(condition_rows).T
    H = hermite_normal_form(G)
    assert H.shape == (83, 83) and H.det() != 0
    Y = (denominator * H.inv().T).applyfunc(sp.cancel)
    return Y, denominator


def multiplication_integral(L, ambient_left):
    Linv = L.inv()
    for a in range(83):
        La = linear_combination(ambient_left, L[:, a])
        M = (Linv * La * L).applyfunc(sp.cancel)
        if any(sp.Rational(x).q != 1 for x in M):
            return False
    return True


def valuation(n, p):
    n = abs(int(n))
    out = 0
    while n and n % p == 0:
        n //= p
        out += 1
    return out


def discriminant(L, gramO):
    G = (L.T * gramO * L).applyfunc(sp.cancel)
    assert all(sp.Rational(x).q == 1 for x in G)
    return abs(int(G.det(method="domain-ge")))


def chain_for_prime(p, gramO, ambient_left, ambient_right, max_steps=8):
    L = sp.eye(83)
    rows = []
    previous_disc = discriminant(L, gramO)
    for step in range(max_steps):
        left_mats = order_left_matrices(L, ambient_left)
        J, simple_degrees = radical_basis(left_mats, p)
        H = ideal_lattice_in_order(J, p)
        I = L * H
        Y, condition_denominator = two_sided_idealizer(I, ambient_left, ambient_right)
        assert multiplication_integral(Y, ambient_left)
        contain = (Y.inv() * L).applyfunc(sp.cancel)
        assert all(sp.Rational(x).q == 1 for x in contain)
        index = abs(int(contain.det()))
        new_disc = discriminant(Y, gramO)
        rows.append({
            "step": step,
            "order_discriminant": str(previous_disc),
            "p_valuation_before": valuation(previous_disc, p),
            "radical_dimension": int(J.shape[0]),
            "semisimple_simple_degrees": simple_degrees,
            "idealizer_condition_denominator": condition_denominator,
            "overorder_index": str(index),
            "new_discriminant": str(new_disc),
            "p_valuation_after": valuation(new_disc, p),
        })
        if index == 1:
            L = Y
            previous_disc = new_disc
            break
        assert previous_disc == new_disc * index * index
        L = Y
        previous_disc = new_disc
        if valuation(new_disc, p) == 0:
            break
    return L, rows, previous_disc


def analyze():
    _public, cap = capture()
    g = cap["g"]
    _tensor, ambient_left, ambient_right = ambient_multiplication(g)

    # Reduced-trace Gram matrix of the orbital basis, reconstructed from frozen matrix units.
    from pass1370_1374 import core
    blocks = core.matrix_units_full(g, cap["full_records"])
    columns = []
    gm = sp.zeros(83)
    cursor = 0
    for block in blocks:
        E = block["E"]
        n = len(E)
        columns.extend(E[i][j] for i in range(n) for j in range(n))
        for i in range(n):
            for j in range(n):
                gm[cursor + i * n + j, cursor + j * n + i] = 1
        cursor += n * n
    C = sp.Matrix.hstack(*columns)
    B = C.inv()
    gramO = (B.T * gm * B).applyfunc(sp.cancel)
    assert all(sp.Rational(x).q == 1 for x in gramO)

    primes = {}
    final_orders = {}
    for p in (2, 3):
        L, chain, disc = chain_for_prime(p, gramO, ambient_left, ambient_right)
        final_orders[p] = L
        primes[str(p)] = {
            "chain": chain,
            "steps": len(chain),
            "final_discriminant": str(disc),
            "final_p_valuation": valuation(disc, p),
            "p_maximal_certified_by_unit_discriminant": valuation(disc, p) == 0,
            "basis_stats": {
                "max_denominator": denominator_lcm(L),
                "sha256": sha([[[int(sp.Rational(x).p), int(sp.Rational(x).q)] for x in L.row(i)] for i in range(83)]),
            },
        }

    result = {
        "theorem": "Pass 1413 Local Radical-Idealizer Maximal Overorders",
        "method": "Iterate the two-sided idealizer of pO plus the lifted Jacobson radical of the current reduction; verify every new lattice is an integral overorder and track the reduced-trace discriminant exactly.",
        "primes": primes,
        "both_local_maximality_certificates_complete": all(primes[str(p)]["p_maximal_certified_by_unit_discriminant"] for p in (2, 3)),
        "boundary": "A zero local discriminant valuation certifies p-maximality in the split rational algebra. If a chain stabilizes earlier, the certificate reports that obstruction rather than declaring maximality.",
    }
    result["sha256"] = sha(result)
    return result
