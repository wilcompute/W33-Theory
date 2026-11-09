"""Item 1 (certificate): sum-of-squares lower bound for F(x) = sum_e (|<e|v>|^2 - |v|^2/9)^2 on the unit sphere, x = (Re v, Im v) in R^18.
Find the largest delta with F - delta (x.x)^2 = m(x)^T G m(x), G PSD over the 171 degree-2 monomials (Clarabel via cvxpy).
delta > 0 certifies F > 0 for v != 0, i.e. strong unextendibility (numerical SDP certificate; exact rounding is a further step).
Control: 4 bases of a complete spread (solutions exist) must give delta ~ 0.  Numerical minimum on the sphere (Pass 12637): 0.14711.
usage: py -3 analysis/w33_strong_umub_sos.py"""
import itertools, json, os, time
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_strong_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_strong_umub.py"), encoding="utf-8").read().split("ctrl_a = minF")[0], ns)
states, maxsets, spread = ns["states"], ns["maxsets"], ns["spread"]
n = 18
mons = [(i, j) for i in range(n) for j in range(i, n)]
def quartic_coeffs(E):
    T = np.zeros((n, n, n, n))
    for e in E:
        a = np.concatenate([e.real, e.imag]); b = np.concatenate([-e.imag, e.real])  # <e|v> = a.x + i b.x  (conj(e).v)
        Q = np.outer(a, a) + np.outer(b, b)
        A = Q - np.eye(n) / 9
        T += np.einsum("ij,kl->ijkl", A, A)
    C = {}
    for idx in itertools.product(range(n), repeat=4):
        k = tuple(sorted(idx))
        C[k] = C.get(k, 0.0) + T[idx]
    return C
def norm4():
    C = {}
    for i in range(n):
        for j in range(n):
            k = tuple(sorted((i, i, j, j)))
            C[k] = C.get(k, 0.0) + 1.0
    return C
def sos_delta(E):
    C = quartic_coeffs(E); N4 = norm4()
    keys = sorted(set(C) | set(N4))
    kidx = {k: i for i, k in enumerate(keys)}
    m = len(mons)
    G = cp.Variable((m, m), symmetric=True)
    delta = cp.Variable()
    rows = {k: [] for k in keys}
    for a in range(m):
        for b in range(m):
            k = tuple(sorted(mons[a] + mons[b]))
            rows[k].append((a, b))
    cons = [G >> 0]
    for k in keys:
        cons.append(sum(G[a, b] for a, b in rows[k]) == C.get(k, 0.0) - delta * N4.get(k, 0.0))
    prob = cp.Problem(cp.Maximize(delta), cons)
    t = time.time()
    prob.solve(solver=cp.CLARABEL)
    return float(delta.value), prob.status, time.time() - t
res = {}
d, st, tt = sos_delta(states(spread[:4]))
res["control_4_spread"] = dict(delta=d, status=st, sec=tt)
print("control (4 spread bases): delta = %.3e  status %s  %.0fs" % (d, st, tt))
d, st, tt = sos_delta(states(sorted(maxsets[0])))
res["pentad"] = dict(delta=d, status=st, sec=tt)
print("pentad: delta = %.6f  status %s  %.0fs   (sphere minimum 0.14711)" % (d, st, tt))
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_sos.json"), "w"), indent=1)
