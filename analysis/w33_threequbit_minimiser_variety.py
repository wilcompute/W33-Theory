"""Pass 12647: are all minimisers of F (three-qubit size-5 set, min 1/8) stabiliser states?  Collect local minima from random starts;
for each at F = 1/8 count Paulis with |<P>| = 1 (a stabiliser state has 7).  Non-stabiliser minimisers would add kernel directions to
the degree-6 certificate.  Also report the numerical rank of the span of q(v) over all minimisers found (sector-0 shifted), against the
rank 20 obtained from the 160 stabiliser minimisers.
usage: py -3 analysis/w33_threequbit_minimiser_variety.py"""
import os, contextlib, io, json, itertools
import numpy as np
from collections import Counter
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_threequbit_exact_one_eighth.py")}
src = open(os.path.join(HERE, "w33_threequbit_exact_one_eighth.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(src[: src.index("def exact_complement")], g)
E, qvec, qi, shiftG, s0G, d, kerG = g["red"]["E"], g["qvec"], g["qi"], g["shiftG"], g["s0G"], 8, g["kerG"]
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(a):
    M = np.eye(1)
    for i in range(3):
        x, z = a[i], a[3 + i]
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
Pall = [pauli(a) for a in itertools.product(range(2), repeat=6) if any(a)]
def F(z):
    v = z[:d] + 1j * z[d:]; v = v / np.linalg.norm(v)
    return sum((abs(np.vdot(e, v)) ** 2 - 1 / d) ** 2 for e in E)
rng = np.random.default_rng(5); minima = []
for _ in range(300):
    r = minimize(F, rng.standard_normal(2 * d), method="BFGS", options=dict(gtol=1e-12))
    if r.fun < 0.125 + 1e-8:
        v = r.x[:d] + 1j * r.x[d:]; minima.append(v / np.linalg.norm(v))
nstab = Counter(sum(1 for P in Pall if abs(np.vdot(v, P @ v)) > 1 - 1e-6) for v in minima)
extra = []
for v in minima:
    q = qvec(v)
    for a in range(d): extra.append([q[qi[shiftG(t, a)]] for t in s0G])
rank_stab = np.linalg.matrix_rank(np.array(kerG), tol=1e-8)
rank_all = np.linalg.matrix_rank(np.array(kerG + extra), tol=1e-6)
res = dict(n_minima_at_one_eighth=len(minima), paulis_with_unit_expectation_histogram=dict(nstab), q_span_rank_stabiliser=int(rank_stab), q_span_rank_all=int(rank_all))
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_minimiser_variety.json"), "w"), indent=1)
# ---- structure: which Pauli is fixed, and is the whole eigenspace minimal?
pidx = Counter()
labels = [a for a in itertools.product(range(2), repeat=6) if any(a)]
for v in minima:
    for k, P in enumerate(Pall):
        if abs(np.vdot(v, P @ v)) > 1 - 1e-6: pidx[labels[k]] += 1
pts, lag, S = g["red"]["pts"], g["red"]["lag"], g["red"]["S"]
C = frozenset().union(*[lag[L] for L in S]); ptid = {tuple(p): i for i, p in enumerate(pts)}
info = {}
for a, c in pidx.items():
    covered = ptid.get(tuple(a)) in C
    P = Pall[labels.index(a)]
    vals = []
    for sgn in (1, -1):
        Pr = (np.eye(d) + sgn * P) / 2; w_, Vv = np.linalg.eigh(Pr); Vs = Vv[:, w_ > 0.5]
        fs = [F(np.concatenate([(Vs @ (rng.standard_normal(4) + 1j * rng.standard_normal(4))).real, (Vs @ (rng.standard_normal(4) + 1j * rng.standard_normal(4))).imag])) for _ in range(1)]
        rnd = []
        for _ in range(20):
            u = Vs @ (rng.standard_normal(4) + 1j * rng.standard_normal(4)); rnd.append(F(np.concatenate([u.real, u.imag])))
        vals.append((sgn, float(min(rnd)), float(max(rnd))))
    info[str(a)] = dict(count=c, covered=covered, random_states_in_eigenspaces_F_range=vals)
res.update(fixed_paulis=info)
print(json.dumps(info, indent=1)); json.dump(res, open(os.path.join(ROOT, "data", "w33_threequbit_minimiser_variety.json"), "w"), indent=1)
