import sys, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
import w33_pass11884_11886_one_loop_trinification as P
H = P.H
def spec(c):
    return P.vec_spectrum((c / np.linalg.norm(c)) @ H)
def FG(e):
    e = e[e > 1e-12]
    return np.sum(e ** 2 * np.log(e)), np.sum(e * np.log(e))
wit = spec(np.array([1, 0, 0, 0], complex))
print('Witting: zeros', int(np.sum(wit < 1e-9)), 'F,G', FG(wit))
rng = np.random.default_rng(0)
for thd in range(0, 360, 15):
    th = np.radians(thd); a, b = np.cos(th), np.sin(th)
    f = lambda q: (lambda F, G: a * F + b * G)(*FG(spec(q[:4] + 1j * q[4:])))
    best = None
    for _ in range(6):
        r = minimize(f, rng.normal(size=8), method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-9, fatol=1e-12))
        if best is None or r.fun < best.fun: best = r
    e = spec(best.x[:4] + 1j * best.x[4:])
    F, G = FG(e)
    print('theta %3d  (a,b)=(%+.2f,%+.2f)  zeros %2d  F=%.4f G=%.4f  %s' % (thd, a, b, int(np.sum(e < 1e-6)), F, G,
          'WITTING (point)' if abs(F - FG(wit)[0]) < 1e-5 and abs(G - FG(wit)[1]) < 1e-5 else ''), flush=True)
