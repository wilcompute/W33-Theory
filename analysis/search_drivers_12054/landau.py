"""Landau phase map of an Sp(4,3)-invariant tick condensate on the forty points."""
import itertools
import sys

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

Adj, invs, tick, fib = setup()
ev, U = np.linalg.eigh(Adj.astype(float))
P = {lam: U[:, np.isclose(ev, lam)] for lam in (12.0, 2.0, -4.0)}
print({k: v.shape[1] for k, v in P.items()})
V15, V24 = P[-4.0], P[2.0]


def patterns():
    pts = range(40)
    out = {}
    out['point'] = np.eye(40)[0]
    nb = list(np.nonzero(Adj[0])[0])
    q = nb[0]
    line = [0, q] + [r for r in nb if Adj[q, r]]
    out['isotropic line'] = np.isin(np.arange(40), line).astype(float)
    out['perp (13)'] = np.isin(np.arange(40), [0] + nb).astype(float)
    # hyperbolic line through 0 and a far point: {x, y} plus the points collinear with neither...: the 4 points
    # pairwise non-collinear spanning a 2-dim non-isotropic subspace = common non-neighbours closure
    far = [r for r in pts if r != 0 and not Adj[0, r]]
    y = far[0]
    hyp = [r for r in pts if r not in (0, y) and not Adj[0, r] and not Adj[y, r] and
           set(np.nonzero(Adj[r])[0]) & set(np.nonzero(Adj[0])[0]) == set(np.nonzero(Adj[0])[0]) & set(np.nonzero(Adj[y])[0])]
    out['hyperbolic line'] = np.isin(np.arange(40), [0, y] + hyp[:2]).astype(float)
    for kind, s in invs:
        if kind == 'split':
            S = [x for x in range(40) if not s[fib[x]].any()]
            out['factorisation (8)'] = np.isin(np.arange(40), S).astype(float)
            break
    # a maximal partial ovoid (pairwise non-collinear set), greedy
    best = []
    rng = np.random.default_rng(0)
    for _ in range(300):
        order = rng.permutation(40)
        S = []
        for v in order:
            if all(not Adj[v, w] for w in S):
                S.append(v)
        if len(S) > len(best):
            best = S
    out['partial ovoid (%d)' % len(best)] = np.isin(np.arange(40), best).astype(float)
    return out, hyp


def opt(V, sign, n=400, seed=0):
    rng = np.random.default_rng(seed)
    f = lambda c: sign * np.sum((V @ (c / np.linalg.norm(c))) ** 4)  # noqa: E731
    best = None
    for _ in range(n):
        r = minimize(f, rng.normal(size=V.shape[1]), method='BFGS')
        if best is None or r.fun < best[0]:
            best = (r.fun, V @ (r.x / np.linalg.norm(r.x)))
    return sign * best[0], best[1]


pats, hyp = patterns()
print('hyperbolic line extra points found:', len(hyp))
for name, V in (('V15', V15), ('V24', V24)):
    for sign, lab in ((-1, 'MAX'), (1, 'MIN')):
        val, phi = opt(V, sign)
        sims = {}
        for k, x in pats.items():
            px = V @ (V.T @ x)
            if np.linalg.norm(px) < 1e-9:
                sims[k] = None
                continue
            px /= np.linalg.norm(px)
            # best overlap over the group orbit is expensive; compare sorted-|value| profiles instead
            sims[k] = round(float(np.linalg.norm(np.sort(np.abs(px)) - np.sort(np.abs(phi)))), 4)
        q4 = {k: (round(float(np.sum((V @ (V.T @ x) / np.linalg.norm(V @ (V.T @ x))) ** 4)), 5) if np.linalg.norm(V @ (V.T @ x)) > 1e-9 else None) for k, x in pats.items()}
        print(name, lab, 'sum phi^4 = %.5f' % val, ' profile distance to patterns:', sims)
        print('     pattern sum phi^4 values:', q4)
        print('     optimiser |phi| profile (sorted, rounded):', np.round(np.sort(np.abs(phi))[::-1][:16], 3))
