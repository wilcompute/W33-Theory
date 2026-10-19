import numpy as np, sys
from scipy.optimize import minimize
exec(open('landau.py').read().split("pats, hyp = patterns()")[0])
E = [(p, q) for p in range(40) for q in range(p + 1, 40) if Adj[p, q]]
Ei, Ej = np.array([e[0] for e in E]), np.array([e[1] for e in E])
def classify(phi):
    a = np.sort(np.abs(phi))[::-1]
    if np.allclose(a, a[0], atol=1e-4):
        return 'flat +-1 (two-sublattice)'
    for name, V in (('V15', V15), ('V24', V24)):
        pe = V @ V[0]; pe /= np.linalg.norm(pe)
        if np.allclose(np.sort(np.abs(pe))[::-1], a, atol=2e-3):
            return 'single event'
    return 'other: top ' + str(np.round(a[:6], 3))
for name, V in (('V15', V15), ('V24', V24)):
    rng = np.random.default_rng(1)
    phases = []
    for th in np.linspace(0, 2 * np.pi, 72, endpoint=False):
        c, s = np.cos(th), np.sin(th)
        def f(x):
            phi = V @ (x / np.linalg.norm(x))
            return c * np.sum(phi ** 4) + s * np.sum(phi[Ei] ** 2 * phi[Ej] ** 2)
        best = None
        for _ in range(60):
            r = minimize(f, rng.normal(size=V.shape[1]), method='BFGS')
            if best is None or r.fun < best[0] - 1e-10:
                best = (r.fun, V @ (r.x / np.linalg.norm(r.x)))
        phases.append((round(np.degrees(th)), classify(best[1])))
    from itertools import groupby
    print(name)
    for k, g in groupby(phases, key=lambda t: t[1]):
        g = list(g); print('   theta %4d..%4d deg : %s' % (g[0][0], g[-1][0], k))
