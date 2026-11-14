"""Exact dual certificate for the full-cut three-copy F8 regulus bound."""

import argparse
import json
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path

import numpy as np

from toe_20261114_regulus_full_ppt import constraints, logical_terms

D = 16
OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_regulus_ppt_dual.json"


def block_maps():
    triples = [t for t in combinations_with_replacement(range(D), 3) if not (t[0] ^ t[1] ^ t[2])]
    index = {t: i for i, t in enumerate(triples)}
    pairs = list(combinations_with_replacement(range(len(triples)), 2))
    cols = {ij: k for k, ij in enumerate(pairs)}
    orbit_map = np.array([[cols[min(i, j), max(i, j)] for j in range(len(triples))]
                          for i in range(len(triples))])
    labels = [(a, b, a ^ b) for a, b in product(range(D), repeat=2)]
    ppt_map = np.empty((D**2, D**2), dtype=np.int64)
    for i, (a, b, c) in enumerate(labels):
        for j, (t, e, f) in enumerate(labels):
            shift = a ^ t
            row = index[tuple(sorted((t ^ shift, b ^ shift, c ^ shift)))]
            col = index[tuple(sorted((a ^ shift, e ^ shift, f ^ shift)))]
            ppt_map[i, j] = cols[min(row, col), max(row, col)]
    assert np.array_equal(ppt_map, ppt_map.T)

    terms = logical_terms()
    objective = np.zeros(len(pairs), dtype=np.int64)
    sample = np.arange(len(pairs), dtype=np.int64) % 17 - 8
    ppt_sample = sample[ppt_map]
    outputs = [i for i, (_, b, c) in enumerate(labels) if b <= c]
    expected_columns = []
    for x, z, weight in terms:
        indices = [t * D + (t ^ x) for t in range(D)]
        signs = np.array([(-1)**((z & t).bit_count()) for t in range(D)])
        np.add.at(objective, ppt_map[np.ix_(indices, indices)].ravel(),
                  weight * np.outer(signs, signs).ravel())
        expected_columns.extend(ppt_sample[np.ix_(outputs, indices)] @ signs)
    np.testing.assert_array_equal(constraints(triples, cols, terms, D) @ sample, expected_columns)
    trace = np.bincount(np.diag(ppt_map), minlength=len(pairs))
    sizes = np.array([1 if t[0] == t[2] else 3 if len(set(t)) == 2 else 6 for t in triples])
    np.testing.assert_array_equal(trace[orbit_map], np.diag(sizes))
    assert (trace[0], objective[0]) == (1, sum(w for x, z, w in terms if x == 0))
    check_pure_state(triples, pairs, terms, trace, objective)
    return orbit_map, ppt_map, trace, objective



def check_pure_state(triples, pairs, terms, trace, objective):
    # Compare the reduced linear objective with direct Gaussian-integer
    # Pauli moments of a complex state before averaging.
    state = np.array([(i**2 % 11) - 5 + 1j * ((i**3 % 13) - 6) for i in range(D)])
    conjugate = state.conj()
    norm_squared = int(np.vdot(state, state).real)
    cubes = [np.prod(state[np.array(t) ^ shift]) for t in triples for shift in range(D)]
    cubes = np.array(cubes).reshape(len(triples), D)
    coefficients = np.array([int(np.vdot(cubes[j], cubes[i]).real) for i, j in pairs])
    expected = 0
    for x, z, weight in terms:
        moment = sum(conjugate[t ^ x] * state[t] * (-1)**((z & t).bit_count()) for t in range(D))
        expected += weight * (int(moment.real)**2 + int(moment.imag)**2)
    assert trace @ coefficients == norm_squared**3
    assert objective @ coefficients == expected * norm_squared

def gram(factor):
    peak = int(np.max(np.abs(factor)))
    assert factor.shape[1] * peak**2 < 2**63
    return factor @ factor.T


def residual(maps, factor, scale, bound):
    orbit_map, ppt_map, trace, objective = maps
    dual_matrix = gram(factor)
    target = objective * scale**2 - int(bound * scale**2) * trace
    assert Fraction(int(bound * scale**2), scale**2) == bound
    # Keep all coefficient accumulation and residual arithmetic in exact int64.
    assert 2 * (int(np.max(np.abs(target))) + dual_matrix.size *
                int(np.max(np.abs(dual_matrix)))) < 2**63
    coefficient = target.copy()
    np.add.at(coefficient, ppt_map.ravel(), -dual_matrix.ravel())
    matrix = coefficient[orbit_map]
    diagonal = np.diag_indices_from(matrix)
    matrix[diagonal] *= 2
    return matrix


def verify(maps, record):
    scale = record["scale"]
    bound = Fraction(record["bound"])
    assert scale == 2**20 and 2 < bound < 3
    factor = np.array(record["ppt_factor"], dtype=np.int64)
    lower = np.array(record["residual_factor"], dtype=np.int64)
    assert factor.shape == (D**2, 28)
    assert lower.shape == maps[0].shape
    remainder = residual(maps, factor, scale, bound) - gram(lower)
    assert remainder.shape[0] * int(np.max(np.abs(remainder))) < 2**63
    margin = np.min(2 * np.diag(remainder) - np.abs(remainder).sum(axis=1))
    assert int(margin) == record["diagonal_dominance_margin"] > 0
    print(f"PASS: full-cut PPT objective >= {bound} = {float(bound):.12f}. "
          f"Exact diagonal-dominance margin {margin}.", flush=True)


def generate(maps):
    # The solver supplies a candidate factor. Replay uses only the integers.
    import cvxpy as cp

    orbit_map, ppt_map, trace, objective = maps
    coefficients = cp.Variable(len(trace))
    ppt = cp.reshape(coefficients[ppt_map.ravel()], ppt_map.shape, order="C")
    orbit = cp.reshape(coefficients[orbit_map.ravel()], orbit_map.shape, order="C")
    ppt_constraint = ppt >> 0
    problem = cp.Problem(cp.Minimize(objective @ coefficients),
                         [trace @ coefficients == 1, ppt_constraint, orbit >> 0])
    problem.solve(solver="SCS", eps=1e-6, max_iters=3000)
    assert problem.status == cp.OPTIMAL
    dual = ppt_constraint.dual_value
    eigenvalues, eigenvectors = np.linalg.eigh((dual + dual.T) / 2)
    scale = 2**20
    factor = np.rint(scale * eigenvectors[:, -28:] * np.sqrt(eigenvalues[-28:])).astype(np.int64)
    bound = Fraction(20818 * scale**2 // 10000, scale**2)
    matrix = residual(maps, factor, scale, bound)
    lower = np.rint(np.linalg.cholesky(matrix.astype(float) - 10**7 * np.eye(len(matrix)))).astype(np.int64)
    remainder = matrix - gram(lower)
    margin = np.min(2 * np.diag(remainder) - np.abs(remainder).sum(axis=1))
    record = dict(bound=str(bound), scale=scale, numerical_sdp_objective=problem.value,
                  ppt_factor=factor.tolist(), residual_factor=lower.tolist(),
                  diagonal_dominance_margin=int(margin))
    verify(maps, record)
    OUT.write_text(json.dumps(record, separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generate", action="store_true", help="regenerate the integer certificate with SCS")
    maps = block_maps()
    if parser.parse_args().generate:
        generate(maps)
    else:
        verify(maps, json.loads(OUT.read_text(encoding="utf-8")))
