"""Sparse exact-diagonalization control; requires NumPy and SciPy."""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh


def critical_gap(n):
    i = np.arange(1 << n)
    s = 1 - 2 * ((i[:, None] >> np.arange(n)) & 1)
    cols = np.concatenate([i] + [i ^ (1 << k) for k in range(n)])
    vals = np.r_[-(s * np.roll(s, 1, axis=1)).sum(1), -np.ones(n * len(i))]
    h = coo_matrix((vals, (np.tile(i, n + 1), cols)), shape=(len(i), len(i))).tocsr()
    e = np.sort(eigsh(h, k=2, which='SA', return_eigenvectors=False, tol=1e-12))
    return float(e[1] - e[0])


if __name__ == '__main__':
    for n in (4, 6, 8, 10, 12):
        gap = critical_gap(n)
        np.testing.assert_allclose(gap, 2 * np.tan(np.pi / (4 * n)), atol=1e-10)
        print(n, gap, n * gap)
