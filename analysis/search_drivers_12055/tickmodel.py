"""Microscopic tick model on two qutrits: 120 ticks (point p, eigenspace k), H(phi) = sum phi_pk (I - Pi_k(p)), phi >= 0."""
import itertools
import sys

import numpy as np
from scipy.optimize import minimize

w = np.exp(2j * np.pi / 3)
X = np.roll(np.eye(3), 1, axis=0)
Z = np.diag([1, w, w * w])


def pauli(v):
    a1, a2, b1, b2 = v
    return np.kron(np.linalg.matrix_power(X, a1) @ np.linalg.matrix_power(Z, b1), np.linalg.matrix_power(X, a2) @ np.linalg.matrix_power(Z, b2))


pts = []
for v in itertools.product(range(3), repeat=4):
    if any(v) and next(x for x in v if x) == 1:
        pts.append(v)
assert len(pts) == 40
omega_form = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % 3  # noqa: E731
Adj = np.array([[int(i != j and omega_form(pts[i], pts[j]) == 0) for j in range(40)] for i in range(40)])
assert sorted(set(Adj.sum(0))) == [12]
proj = []                      # proj[p][k] = projector onto eigenvalue w^k of W_p
for v in pts:
    W = pauli(v)
    ev = np.linalg.eigvals(W)
    assert np.allclose(np.linalg.matrix_power(W, 3), np.eye(9))
    proj.append([(np.eye(9) + w ** (-k) * W + w ** (-2 * k) * W @ W) / 3 for k in range(3)])
H_list = [np.eye(9) - proj[p][k] for p in range(40) for k in range(3)]
H_arr = np.array(H_list)      # 120 x 9 x 9


def free(phi, T):
    H = np.tensordot(phi, H_arr, axes=1)
    e = np.linalg.eigvalsh((H + H.conj().T) / 2)
    if T == 0:
        return e.min(), e
    m = e.min()
    return m - T * np.log(np.sum(np.exp(-(e - m) / T))), e


def minimise(T, n=200, seed=0):
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n):
        f = lambda x: free(x ** 2 / np.linalg.norm(x ** 2), T)[0]  # noqa: E731
        r = minimize(f, rng.random(120), method='L-BFGS-B')
        phi = r.x ** 2 / np.linalg.norm(r.x ** 2)
        if best is None or r.fun < best[0] - 1e-9:
            best = (r.fun, phi)
    return best


def describe(phi):
    a = phi
    sup = np.nonzero(a > 0.05 * a.max())[0]
    P = sorted(set(s // 3 for s in sup))
    ks = sorted(set(s % 3 for s in sup))
    sub = Adj[np.ix_(P, P)]
    return '%d ticks on %d points (%d collinear pairs), values %s' % (len(sup), len(P), sub.sum() // 2, np.round(np.sort(a[sup])[::-1][:6], 3))


if __name__ == '__main__':
    # single tick vs line references
    one = np.zeros(120); one[0] = 1
    for T in [float(t) for t in sys.argv[1:]] or [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0]:
        fb, phi = minimise(T, n=120)
        print('T=%.3f  min F = %.5f   single tick F = %.5f   optimum: %s' % (T, fb, free(one, T)[0], describe(phi)), flush=True)
