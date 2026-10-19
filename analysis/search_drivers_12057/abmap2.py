import sys, numpy as np, json
from scipy.optimize import minimize
exec(open('abmap.py').read().split("rng = np.random")[0])
rng = np.random.default_rng(7)
def best(thd, n=4):
    th = np.radians(thd); a, b = np.cos(th), np.sin(th)
    f = lambda q: (lambda F, G: a * F + b * G)(*FG(spec(q[:4] + 1j * q[4:])))
    bb = None
    for _ in range(n):
        r = minimize(f, rng.normal(size=8), method='Nelder-Mead', options=dict(maxiter=3000, xatol=1e-9, fatol=1e-12))
        if bb is None or r.fun < bb.fun: bb = r
    e = spec(bb.x[:4] + 1j * bb.x[4:]); F, G = FG(e)
    return int(np.sum(e < 1e-6)), round(F, 4), round(G, 4), (bb.x[:4] + 1j * bb.x[4:]).tolist()
out = {}
for t in (270, 315, 345, 8, 12, 188, 193):
    z, F, G, c = best(t)
    out[t] = dict(zeros=z, F=F, G=G)
    print(t, z, F, G, flush=True)
json.dump(out, open('abmap2.json', 'w'))
