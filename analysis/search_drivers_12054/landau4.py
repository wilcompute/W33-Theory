import numpy as np
from scipy.optimize import minimize
exec(open('landau3.py').read().split("for name, V in")[0])
def phase(V, thd, rng, n=60):
    th = np.radians(thd); c, s = np.cos(th), np.sin(th)
    f = lambda x: c * np.sum((V @ (x / np.linalg.norm(x))) ** 4) + s * np.sum((V @ (x / np.linalg.norm(x)))[Ei] ** 2 * (V @ (x / np.linalg.norm(x)))[Ej] ** 2)
    best = None
    for _ in range(n):
        r = minimize(f, rng.normal(size=V.shape[1]), method='BFGS')
        if best is None or r.fun < best[0] - 1e-10:
            best = (r.fun, V @ (r.x / np.linalg.norm(r.x)))
    a = np.abs(best[1]); m = a.max(); top = np.nonzero(a > 0.9 * m)[0]
    return len(top), round(float(m), 3)
rng = np.random.default_rng(5)
for name, V, ranges in (('V15', V15, (range(128, 146), range(236, 252))), ('V24', V24, (range(100, 118), range(212, 230)))):
    for rg in ranges:
        print(name, [(t, phase(V, t, rng)) for t in rg])
