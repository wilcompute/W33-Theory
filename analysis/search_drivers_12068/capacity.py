import sys
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12055_microscopic_tick_model import ADJ, HS, free, PROJ
rng = np.random.default_rng(1)
def obj(z, T, g):
    phi = np.exp(z - z.max()); phi /= phi.sum()
    return free(phi, T) + g * np.sum(phi ** 2)
def classify(phi):
    sup = [a for a in range(120) if phi[a] > 0.02]
    pts = sorted({a // 3 for a in sup})
    col = all(ADJ[x, y] for x in pts for y in pts if x != y)
    return len(sup), len(pts), col, np.round(np.sort(phi[sup])[::-1], 3).tolist()[:6]
for T in (0.2, 1.0):
    x = np.exp(-1 / (2 * T))
    gstar = 2 * T * np.log(3 * (1 + 2 * x * x) / (1 + 2 * x) ** 2)
    print('T', T, 'g* pair', round(gstar, 5))
    for g in [0.5 * gstar, 0.9 * gstar, 1.1 * gstar, 1.5 * gstar, 2 * gstar, 3 * gstar, 5 * gstar, 10 * gstar]:
        best = None
        for _ in range(40):
            z0 = rng.normal(size=120) * 3
            r = minimize(obj, z0, args=(T, g), method='L-BFGS-B')
            if best is None or r.fun < best.fun:
                best = r
        phi = np.exp(best.x - best.x.max()); phi /= phi.sum()
        print('   g/g* %.1f' % (g / gstar), round(best.fun, 6), classify(phi))
