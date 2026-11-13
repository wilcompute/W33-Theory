"""Pass 12652 addendum: LOWER bound on theta(G) for the 744-vertex uncovered anticommutation graph G (five-qubit size-9 set), via
Lovasz's theta(G) * theta(Gbar) >= n (Lovasz 1979, Cor. 2), with theta(Gbar) bounded ABOVE by the same eigenvalue formulation as
w33_five_qubit_size9_theta_eig.py (any feasible A gives theta(Gbar) <= lambda_max(A)).  If theta(Gbar) < 744/30 = 24.8 then
theta(G) > 30 rigorously, so the Lovasz/de Gois bound Sigma_U <= theta cannot certify min F = 1/32.
Control: on the Petersen graph (theta = 4, theta(complement) = 2.5, n = 10, product exactly n) the optimiser must return ~2.5 and ~4.
usage: py -3 analysis/w33_five_qubit_size9_theta_lower.py"""
import json, os, time
import numpy as np
import networkx as nx
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def theta_upper(adj, betas=(5, 20, 80, 320, 1280, 5000), iters=600):
    N = len(adj); ii, jj = np.nonzero(np.triu(adj, 1)); J = np.ones((N, N))

    def build(e):
        A = J.copy(); A[ii, jj] -= e; A[jj, ii] -= e
        return A

    def smooth(e, beta):
        w, V = np.linalg.eigh(build(e)); m = w[-1]; p = np.exp(beta * (w - m)); s = p.sum(); q = p / s
        return m + np.log(s) / beta, -2 * ((V * q) @ V.T)[ii, jj]

    lam = np.linalg.eigvalsh(adj.astype(float))
    e = np.full(len(ii), N / (lam[-1] - lam[0])) if len(ii) else np.zeros(0)
    hist = [float(np.linalg.eigvalsh(build(e))[-1])]
    for b in betas:
        e = minimize(smooth, e, args=(b,), jac=True, method="L-BFGS-B", options=dict(maxiter=iters, maxcor=30)).x
        hist.append(float(np.linalg.eigvalsh(build(e))[-1]))
    return hist[-1], hist


# control
P = nx.to_numpy_array(nx.petersen_graph()).astype(int)
Pc = 1 - P - np.eye(10, dtype=int)
ctrl = dict(petersen=theta_upper(P)[0], petersen_complement=theta_upper(Pc)[0])
print("control", ctrl, flush=True)
assert abs(ctrl["petersen"] - 4) < 1e-3 and abs(ctrl["petersen_complement"] - 2.5) < 1e-3

n = 5; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]


def decode(code):
    S = np.zeros((n, n), int)
    for b, (i, j) in enumerate(pos):
        if code >> b & 1:
            S[i, j] = S[j, i] = 1
    return S


vec = lambda xv, zv: tuple(int(v) for v in xv) + tuple(int(v) for v in zv)
C = set()
for x in range(1, 1 << n):
    xv = np.array([(x >> i) & 1 for i in range(n)])
    C.add(vec(xv, [0] * n)); C.add(vec([0] * n, xv))
    for c in ex:
        C.add(vec(xv, decode(c) @ xv % 2))
U = [p for p in (tuple((v >> i) & 1 for i in range(2 * n)) for v in range(1, 1 << (2 * n))) if p not in C]
Ua = np.array(U); N = len(U)
adj = (Ua[:, :n] @ Ua[:, n:].T + Ua[:, n:] @ Ua[:, :n].T) % 2
comp = 1 - adj - np.eye(N, dtype=int)
t0 = time.time()
tb, hist = theta_upper(comp)
res = dict(control=ctrl, theta_complement_upper=tb, history=hist, theta_G_lower=N / tb, threshold=N / 30,
           theta_G_exceeds_30=bool(N / tb > 30), seconds=round(time.time() - t0, 1))
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta_lower.json"), "w"), indent=1)
