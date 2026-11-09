"""Outside-the-box 1: are the 432 pentads STRONGLY unextendible (no vector unbiased to all 5 bases), not just weakly (no Pauli class)?
Mandayam-Bandyopadhyay-Grassl-Wootters distinguish weak/strong; strong unextendibility is the rare, interesting case.
Minimise F(v) = sum over the 45 states e of (|<e|v>|^2 - 1/9)^2 over unit v in C^9, 200 random starts (BFGS).
Controls that must reach 0: (a) 4 bases of a complete spread (the 6 remaining spread bases are exact solutions); (b) every 4-subset of the
pentad (a solution may or may not exist - reported); a pentad is strongly unextendible iff min F > 0 robustly.
usage: py -3 analysis/w33_pentad_strong_umub.py"""
import itertools, json, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
src = open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0]
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, ns)
bases, maxsets, lines, disj = ns["bases"], ns["maxsets"], ns["lines"], ns["disj"]
def states(Ls):
    return np.concatenate([bases[L].T for L in Ls], axis=0)  # rows = states (conj applied in overlap)
def minF(Ls, starts=200, seed=0):
    E = states(Ls)
    rng = np.random.default_rng(seed)
    def F(x):
        v = x[:9] + 1j * x[9:]
        v = v / np.linalg.norm(v)
        p = np.abs(E.conj() @ v) ** 2
        return float(np.sum((p - 1 / 9) ** 2))
    best = np.inf
    for _ in range(starts):
        r = minimize(F, rng.standard_normal(18), method="BFGS", options=dict(gtol=1e-12, maxiter=2000))
        best = min(best, r.fun)
    return best
# a complete spread (maximal partial spread of size 10)
spread = None
def bk(R, Pc, X):
    global spread
    if spread is not None:
        return
    if not Pc and not X:
        if len(R) == 10: spread = sorted(R)
        return
    for v in list(Pc):
        bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
bk(set(), set(range(40)), set())
ctrl_a = minF(spread[:4], starts=40)
pent = sorted(maxsets[0])
sub4 = [minF(list(c), starts=40, seed=i) for i, c in enumerate(itertools.combinations(pent, 4))]
full = [minF(sorted(maxsets[k]), starts=200, seed=10 + k) for k in range(3)]
res = dict(control_spread4_min=ctrl_a, pentad_4subsets_min=sub4, pentads_min=full,
           strongly_unextendible=all(x > 1e-6 for x in full) and ctrl_a < 1e-10)
print("control (4 spread bases) min F:", "%.2e" % ctrl_a)
print("pentad 4-subsets min F:", ["%.2e" % x for x in sub4])
print("three pentads min F over 200 starts each:", ["%.3e" % x for x in full], "| strongly unextendible:", res["strongly_unextendible"])
json.dump(res, open(os.path.join(ROOT, "data", "w33_pentad_strong_umub.json"), "w"), indent=1)
