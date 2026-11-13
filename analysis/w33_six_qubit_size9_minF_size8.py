"""Pass 12652 item 5: six qubits.  (a) numerical min F for the verified six-qubit size-9 maximal set (Pass 12651; d = 64, 9*63 = 567
covered Paulis; F = (1/64) sum_C <P>^2), compared with the stabiliser values m/64.  (b) annealing for a size-8 set (6 matrices) in the
rank-code form, with the same move set as the five-qubit search; control: size 9 (7 matrices) must be found.
Not finding size 8 is evidence only.  usage: py -3 analysis/w33_six_qubit_size9_minF_size8.py [anneal_seconds]"""
import json, os, sys, time, math
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 6; d = 64; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_six_qubit_size9_verify.json")))["example"]
def decode(code):
    S = np.zeros((n, n), int)
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: S[i, j] = S[j, i] = 1
    return S
pts = set()
for x in range(1, 1 << n):
    xv = np.array([(x >> i) & 1 for i in range(n)])
    pts.add((tuple(xv), (0,) * n)); pts.add(((0,) * n, tuple(xv)))
    for c in ex: pts.add((tuple(xv), tuple(decode(c) @ xv % 2)))
assert len(pts) == 9 * 63
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(xv, zv):
    M = np.eye(1)
    for i in range(n):
        M = np.kron(M, (1j) ** (xv[i] * zv[i]) * np.linalg.matrix_power(X1, xv[i]) @ np.linalg.matrix_power(Z1, zv[i]))
    return M
Ps = np.array([pauli(a, b) for a, b in pts])
def fg(z):
    v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
    Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
    gval = float(np.sum(f ** 2)) / d
    gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * gval * v / nv ** 3
    return gval / nv ** 2, np.concatenate([gr.real, gr.imag])
rng = np.random.default_rng(11); t0 = time.time()
vals = sorted(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-12, maxiter=20000)).fun for _ in range(60))
res = dict(n_covered=len(pts), min_F=float(vals[0]), min_F_times_64=float(vals[0] * 64), lowest_five=[float(v) for v in vals[:5]], minF_seconds=round(time.time() - t0, 1))
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_qubit_size9_minF_size8.json"), "w"), indent=1)
# (b) annealing
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_rank_code_greedy_sizes.py")}
src = open(os.path.join(HERE, "w33_rank_code_greedy_sizes.py"), encoding="utf-8").read()
exec(src[: src.index("res = {}")], g)
_, sing, _, ns = g["setup"](n)
def run(k, tlimit, seed):
    rng = np.random.default_rng(seed); t0 = time.time(); best = 10 ** 9; restarts = 0; hist = []
    def compat(S):
        m = np.ones(len(ns), bool)
        for s in S: m &= ~sing[ns ^ s]
        return m
    while time.time() - t0 < tlimit:
        restarts += 1; S = []; avail = np.ones(len(ns), bool)
        while len(S) < k and avail.any():
            i = int(rng.choice(np.flatnonzero(avail))); S.append(int(ns[i])); avail &= ~sing[ns ^ ns[i]]
        if len(S) < k: continue
        c = int(compat(S).sum()); T = 30.0
        for step in range(3000):
            if time.time() - t0 > tlimit: break
            drop = list(rng.choice(k, 2 if rng.random() < 0.3 else 1, replace=False)); keep = [S[i] for i in range(k) if i not in drop]
            new = list(keep)
            for _ in drop:
                cand = np.flatnonzero(compat(new))
                if len(cand) == 0: break
                new.append(int(ns[int(rng.choice(cand))]))
            if len(new) < k: continue
            c2 = int(compat(new).sum())
            if c2 <= c or rng.random() < math.exp(-(c2 - c) / max(T, 1e-3)): S, c = new, c2
            T = max(0.5, T * 0.998)
            best = min(best, c)
            if c == 0: return dict(size=k + 2, found=True, example=S, restarts=restarts, seconds=round(time.time() - t0, 1))
        hist.append(c)
    return dict(size=k + 2, found=False, best_cost=best, restarts=restarts, seconds=round(time.time() - t0, 1))
ta = float(sys.argv[1]) if len(sys.argv) > 1 else 2400
res["anneal_control_size9"] = run(7, ta / 2, 1); print(res["anneal_control_size9"], flush=True)
res["anneal_size8"] = run(6, ta, 2); print(res["anneal_size8"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_six_qubit_size9_minF_size8.json"), "w"), indent=1)
