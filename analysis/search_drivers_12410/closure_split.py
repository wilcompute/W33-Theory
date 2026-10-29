"""12410: the closure solutions by eigenspace dimension, and the correction to 12402-12409.
For q = 1 mod 4 (i in F_q), a P-symmetric kappa with kappa^2 = -1 is the same as a P-orthogonal decomposition L = U (+) U^perp with U
nondegenerate, kappa = i on U and -i on U^perp, for ANY a = dim U in 0..6.  Hodge stars have a = 3 (equivalently tr kappa = 0).
(1) explicit non-metric solutions at q = 5: kappa = 2 I (2^2 = -1) and a 1 + 5 split -- checked P-symmetric with kappa^2 = -1 and
    tr != 0;  (2) exact counts N_a of nondegenerate a-dim subspaces of the hyperbolic 6-space (orbit-stabiliser over the isometry types),
    for q = 5, 13: the metric (a = 3) solutions are a strict subset of all closure solutions;  (3) for q = 3 mod 4 the Frobenius pairs the
    two eigenspaces (U' = sigma U), forcing a = 3 -- consistent with the exhaustive q = 3 count (16848, all metric)."""
import json
import numpy as np


def go(n, q, eps=0):
    if n == 0:
        return 1
    if n % 2:
        m = (n - 1) // 2
        r = 2 * q ** (m * m)
        for i in range(1, m + 1):
            r *= q ** (2 * i) - 1
        return r
    m = n // 2
    r = 2 * q ** (m * (m - 1)) * (q ** m - eps)
    for i in range(1, m):
        r *= q ** (2 * i) - 1
    return r


def counts(q):
    V = go(6, q, +1)
    N = {}
    for a in range(7):
        b = 6 - a
        if a in (0, 6):
            N[a] = 1
        elif a % 2:
            N[a] = 2 * (V // (go(a, q) * go(b, q)))          # two discriminant classes of U, each one orbit
        else:
            N[a] = V // (go(a, q, +1) * go(b, q, +1)) + V // (go(a, q, -1) * go(b, q, -1))
    return N


out = {}
q = 5
P = np.zeros((6, 6), dtype=np.int64)
for i in range(3):
    P[i, 3 + i] = 1
    P[3 + i, i] = 1
K = 2 * np.eye(6, dtype=np.int64) % q
ex1 = dict(P_symmetric=bool(((P @ K - (P @ K).T) % q == 0).all()), closure=bool(((K @ K + np.eye(6, dtype=np.int64)) % q == 0).all()),
           trace=int(np.trace(K) % q))
# 1 + 5 split: U = span(u) with P(u, u) != 0
u = np.array([1, 0, 0, 1, 0, 0], dtype=np.int64)
assert int(u @ P @ u) % q != 0
Pu = (P @ u) % q
proj = (np.outer(u, Pu) * pow(int(u @ P @ u) % q, q - 2, q)) % q          # P-orthogonal projector onto U
K2 = (2 * proj - 2 * (np.eye(6, dtype=np.int64) - proj)) % q
ex2 = dict(P_symmetric=bool(((P @ K2 - (P @ K2).T) % q == 0).all()), closure=bool(((K2 @ K2 + np.eye(6, dtype=np.int64)) % q == 0).all()),
           trace=int(np.trace(K2) % q))
out['q5_examples'] = dict(kappa_2I=ex1, split_1_5=ex2)
for qq in (5, 13):
    N = counts(qq)
    out[f'q{qq}_counts_by_dimU'] = N
    out[f'q{qq}_total'] = sum(N.values())
    out[f'q{qq}_metric_fraction'] = N[3] / sum(N.values())
print(json.dumps(out, indent=1))
json.dump(out, open('closure_split.json', 'w'), indent=1)
