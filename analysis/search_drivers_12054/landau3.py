import numpy as np
from scipy.optimize import minimize
exec(open('landau.py').read().split("pats, hyp = patterns()")[0])
E = [(p, q) for p in range(40) for q in range(p + 1, 40) if Adj[p, q]]
Ei, Ej = np.array([e[0] for e in E]), np.array([e[1] for e in E])
def geometry(S):
    S = sorted(S); sub = Adj[np.ix_(S, S)]
    k = len(S); e = int(sub.sum() // 2)
    tag = ''
    if k == 1: tag = 'point'
    elif k == 4 and e == 6: tag = 'isotropic line'
    elif k == 4 and e == 0: tag = '4 pairwise non-collinear (hyperbolic line?)'
    elif k == 8 and e == 16 and np.all(sub.sum(0) == 4): tag = 'K44 (factorisation?)'
    elif k == 13: tag = 'perp?' if e == 18 + 0 else 'size13'
    return '%d points, %d edges, degrees %s %s' % (k, e, sorted(set(sub.sum(0).tolist())), tag)
def describe(phi):
    a = np.abs(phi); m = a.max()
    top = np.nonzero(a > 0.9 * m)[0]
    flat = np.allclose(a, a.mean(), rtol=2e-3)
    if flat:
        plus = np.nonzero(phi > 0)[0]
        return 'FLAT +-1, plus-set: ' + geometry(plus)
    return 'top-support: ' + geometry(top) + '  (top value %.3f)' % m
for name, V in (('V15', V15), ('V24', V24)):
    rng = np.random.default_rng(2)
    print(name)
    for thd in (0, 20, 40, 55, 70, 90, 120, 180, 230, 270, 300, 330):
        th = np.radians(thd); c, s = np.cos(th), np.sin(th)
        f = lambda x: c * np.sum((V @ (x / np.linalg.norm(x))) ** 4) + s * np.sum((V @ (x / np.linalg.norm(x)))[Ei] ** 2 * (V @ (x / np.linalg.norm(x)))[Ej] ** 2)
        best = None
        for _ in range(80):
            r = minimize(f, rng.normal(size=V.shape[1]), method='BFGS')
            if best is None or r.fun < best[0] - 1e-10:
                best = (r.fun, V @ (r.x / np.linalg.norm(r.x)))
        print('  theta %3d:' % thd, describe(best[1]))
