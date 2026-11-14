"""Exact reduction of the E6 charge-norm gradient and nearest minimum."""

import json

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from toe_20261114_e6_attractor_torus import OUT as TORUS, R

OUT = TORUS.with_name("toe_20261114_e6_attractor_gradient.json")


def calculate():
    cert, cubic, _, _, roots = R.load()
    ix = json.loads(TORUS.read_text(encoding="utf-8"))["native_coordinates"]
    diagonal = sp.Matrix([[int(i in term) for i in range(27)] for term in sorted(cubic)])
    basis = sp.Matrix.hstack(*diagonal.nullspace())
    projector = basis * (basis.T * basis).inv() * basis.T
    plane = projector[:, ix]
    assert plane[ix, :] == sp.eye(3)/3-sp.ones(3)/9
    assert all(not np.any(root[np.ix_(ix, ix)]) for root in roots)

    _, compact = R.pack_roots(roots)
    fixing = [k for k in compact if not np.any(k[:, ix])]
    assert len(fixing) == 12
    symmetric = {}
    for records in cert["cubic_27"]["generators"]:
        a = np.zeros((27, 27), dtype=np.int64)
        for i, j, entry in records:
            a[i, j] = entry
        sym = a + a.T
        if np.any(sym):
            symmetric[sym.tobytes()] = sym
    assert len(symmetric) == 42
    stacked = np.column_stack([a.ravel() for a in symmetric.values()])
    assert modular_rank(stacked, 101) == 42
    commutators = np.column_stack([
        np.concatenate([(a @ k - k @ a).ravel() for k in fixing])
        for a in symmetric.values()])
    assert modular_rank(commutators, 101) == 40
    for column in range(3):
        h = np.diag(np.array(9*plane[:, column], dtype=np.int64).ravel())
        assert all(np.array_equal(h @ k, k @ h) for k in fixing)
    assert plane.rank() == 2

    checks = []
    for initial in [(1., 8., 27.), (.07, .2, .8), (-1., 8., 27.), (1., 8., 0.)]:
        initial = np.square(initial)

        def gradient(_, x):
            return -(4/3)*x*(x-x.mean())

        duration = 20 / np.prod(initial)**(1/3) if np.all(initial > 0) else 50
        solution = solve_ivp(gradient, (0, duration), initial, rtol=1e-10, atol=1e-12)
        assert solution.success
        assert np.max(np.diff(solution.y.sum(axis=0))) < 1e-12
        np.testing.assert_allclose(np.prod(solution.y[:, -1]), np.prod(initial), rtol=1e-8)
        if np.all(initial > 0):
            np.testing.assert_allclose(solution.y[:, -1], np.prod(initial)**(1/3), rtol=1e-7)
            chars = np.array([[-1,-1,1], [-1,1,-1], [1,-1,-1], [1,1,1]])
            for path in (np.sqrt(solution.y),
                         np.sqrt(initial[:, None]**np.linspace(1, 0)
                                 * np.prod(initial)**(np.linspace(0, 1)/3))):
                for sign in (1, -1):
                    partial = np.cumsum(np.sort(sign * (chars @ path), axis=0)[::-1], axis=0)
                    assert np.max(np.diff(partial[:3], axis=1)) < 1e-9
        checks.append(dict(initial=initial.tolist(), endpoint=solution.y[:, -1].tolist()))
    return dict(status="PASS", symmetric_dimension=42, pointwise_skew_generators=len(fixing),
                commutator_rank_mod_101=40, fixed_symmetric_dimension=2,
                projected_metric=[[str(plane[i, j]) for j in range(3)] for i in ix],
                ode_controls=checks)


def modular_rank(matrix, prime):
    matrix = matrix % prime
    rank = 0
    for column in range(matrix.shape[1]):
        pivots = np.flatnonzero(matrix[rank:, column])
        if not len(pivots):
            continue
        pivot = rank + pivots[0]
        matrix[[rank, pivot]] = matrix[[pivot, rank]]
        row = matrix[rank, column:] * pow(int(matrix[rank, column]), -1, prime) % prime
        matrix[rank+1:, column:] = (matrix[rank+1:, column:]
                                  - matrix[rank+1:, column, None]*row) % prime
        rank += 1
    return rank


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
