"""Pass 12667: does the starting quaternionic spectrum of rho_J MAJORISE the spectrum of the attractor endpoint
rho* = c Pi/2 + (1 - c) I/8, c = N^(1/3) (Pass 12665)?  If yes, rho* = Phi(rho_J) for some unital (mixing) channel Phi (Uhlmann;
Alberti-Uhlmann), so the attractor endpoint is reachable from rho_J by a physical mixing process.  Spectra are compared as
8-vectors (each quaternionic eigenvalue doubled).  Exact: rho* depends only on N = sum (8 p_i - 1)^3 / 24, so the test is a
statement about the simplex {p_1 >= ... >= p_4 >= 0, sum p = 1/2}; checked on 200,000 random points plus the vertices, edges
and face centres, with the partial-sum criterion.   usage: py -3 analysis/w33_attractor_majorisation.py"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def endpoint_spectrum(N):
    c = np.cbrt(N); return np.sort(np.array([c / 2 + (1 - c) / 8] * 2 + [(1 - c) / 8] * 6))[::-1]
def majorises(a, b, tol=1e-12):
    a = np.sort(a)[::-1]; b = np.sort(b)[::-1]
    return bool(np.all(np.cumsum(a)[:-1] >= np.cumsum(b)[:-1] - tol) and abs(a.sum() - b.sum()) < 1e-12)
rng = np.random.default_rng(0); tested = 0; npos = 0; fails = []; worst = np.inf
samples = [rng.dirichlet(np.ones(4) * a) / 2 for a in (0.2, 0.5, 1.0, 3.0) for _ in range(50000)]
samples += [np.array(v) / 2 for v in ([1, 0, 0, 0], [.5, .5, 0, 0], [1 / 3] * 3 + [0], [.25] * 4, [.7, .3, 0, 0], [.6, .2, .2, 0], [.9, .05, .05, 0])]
for p in samples:
    p = np.sort(p)[::-1]; N = float(sum((8 * x - 1) ** 3 for x in p) / 24)
    if N <= 0: continue
    npos += 1
    a = np.repeat(p, 2); b = endpoint_spectrum(N)
    margin = float(np.min(np.cumsum(a)[:-1] - np.cumsum(b)[:-1])); worst = min(worst, margin)
    if not majorises(a, b): fails.append(dict(p=p.tolist(), N=N, margin=margin))
res = dict(points=len(samples), points_with_N_positive=npos, failures=len(fails), first_failures=fails[:5], worst_margin=worst)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_attractor_majorisation.json"), "w"), indent=1)
