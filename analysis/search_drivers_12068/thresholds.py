import sys
import numpy as np
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12055_microscopic_tick_model import ADJ, HS, free, PROJ
# compatible set on one context: points of a line through 0 with labels sharing a joint eigenvector
p = 0; q = int(np.nonzero(ADJ[p])[0][0])
line = [p, q] + [r for r in np.nonzero(ADJ[p])[0] if ADJ[q, r]]
line = line[:4]
# choose labels: start (p,0); for each other point pick k with common kernel vector
def kern(idx):
    H = sum(HS[i] for i in idx); return int(np.sum(np.linalg.eigvalsh(H) < 1e-9))
sel = [3 * p]
for x in line[1:]:
    k = next(k for k in range(3) if kern(sel + [3 * x + k]) == 1)
    sel.append(3 * x + k)
print('compatible ticks', sel, 'common kernel', kern(sel))
for n in (2, 3, 4):
    e = np.round(np.linalg.eigvalsh(sum(HS[i] for i in sel[:n]) / n), 9)
    print(n, sorted(set(e)), [int(np.sum(np.isclose(e, v))) for v in sorted(set(e))])
def F(idx, T):
    phi = np.zeros(120); phi[idx] = 1 / len(idx); return free(phi, T)
for T in (0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0):
    F1 = F(sel[:1], T)
    g = {n: n / (n - 1) * (F(sel[:n], T) - F1) for n in (2, 3, 4)}
    Fall = free(np.ones(120) / 120, T)
    g['all'] = 120 / 119 * (Fall - F1)
    # far pair, for comparison
    far = next(x for x in range(40) if x != p and not ADJ[p, x])
    g['far2'] = 2 * (F([0, 3 * far], T) - F1)
    first = min(g, key=g.get)
    print('T %.2f' % T, {k: round(v, 4) for k, v in g.items()}, 'first:', first)
from scipy.optimize import minimize
for T, g in ((0.2, 1.1 * 0.32319), (0.2, 1.5 * 0.32319), (1.0, 1.1 * 0.12261), (1.0, 1.5 * 0.12261)):
    vals = {n: F(sel[:n], T) + g / n for n in (1, 2, 3, 4)}
    # optimise within the 4-set
    def ob(z):
        w = np.exp(z - z.max()); w /= w.sum(); phi = np.zeros(120); phi[sel] = w
        return free(phi, T) + g * np.sum(w ** 2)
    best = min((minimize(ob, np.random.default_rng(s).normal(size=4), method='Nelder-Mead', options=dict(xatol=1e-10, fatol=1e-12, maxiter=4000)) for s in range(10)), key=lambda r: r.fun)
    w = np.exp(best.x - best.x.max()); w /= w.sum()
    print(T, round(g, 4), {k: round(v, 6) for k, v in vals.items()}, ' best in 4-set', round(best.fun, 6), np.round(np.sort(w), 3))
