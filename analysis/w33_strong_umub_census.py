"""Creative 1 + 2: (1) the smallest strongly unextendible Pauli MUB set in d = 9: classify all 4-sets of pairwise disjoint lines of W(3,3)
up to PSp(4,3) and test each orbit representative for a vector unbiased to all 4 bases (min F over random starts).
(2) cross-rung: weakly unextendible Pauli MUB sets in d = 4 (two qubits, W(3,2)) and d = 8 (three qubits, W(5,2) size 5): strongly too?
F(v) = sum_e (|<e|v>|^2 - 1/d)^2 over unit v; controls: subsets of a complete set (min must be ~0).
usage: py -3 analysis/w33_strong_umub_census.py"""
import itertools, json, os
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

def pauli_ops(p, n):
    om = np.exp(2j * np.pi / p)
    X = np.roll(np.eye(p), 1, axis=0); Z = np.diag([om ** k for k in range(p)])
    def op(v):  # v = (a_1..a_n, b_1..b_n)
        M = np.array([[1.0 + 0j]])
        for i in range(n):
            M = np.kron(M, np.linalg.matrix_power(X, v[i]) @ np.linalg.matrix_power(Z, v[n + i]))
        return M
    return op
def geometry(p, n):
    vecs = [v for v in itertools.product(range(p), repeat=2 * n) if any(v)]
    def norm(v):
        c = next(x for x in v if x); inv = pow(c, -1, p); return tuple((x * inv) % p for x in v)
    pts = sorted({norm(v) for v in vecs})
    w = lambda u, v: sum(u[i] * v[n + i] - u[n + i] * v[i] for i in range(n)) % p
    idx = {q: i for i, q in enumerate(pts)}
    lag = set()
    def span(gens):
        S = set()
        for cs in itertools.product(range(p), repeat=len(gens)):
            v = tuple(sum(c * g[k] for c, g in zip(cs, gens)) % p for k in range(2 * n))
            if any(v): S.add(idx[norm(v)])
        return frozenset(S)
    for gens in itertools.combinations(pts, n):
        if all(w(a, b) == 0 for a, b in itertools.combinations(gens, 2)):
            S = span(gens)
            if len(S) == (p ** n - 1) // (p - 1):
                lag.add(S)
    return pts, sorted(lag, key=sorted), w
def bases_for(p, n, pts, lag):
    op = pauli_ops(p, n); rng = np.random.default_rng(0)
    B = []
    for L in lag:
        H = 0
        for i in L:
            O = op(pts[i]); c = rng.standard_normal() + 1j * rng.standard_normal()
            H = H + c * O + np.conj(c) * O.conj().T
        B.append(np.linalg.eigh(H)[1])
    return B
def minF(B, Ls, d, starts=60, seed=0):
    E = np.concatenate([B[L].T for L in Ls], axis=0)
    rng = np.random.default_rng(seed)
    def F(x):
        v = x[:d] + 1j * x[d:]; v = v / np.linalg.norm(v)
        return float(np.sum((np.abs(E.conj() @ v) ** 2 - 1 / d) ** 2))
    return min(minimize(F, rng.standard_normal(2 * d), method="BFGS", options=dict(gtol=1e-12, maxiter=3000)).fun for _ in range(starts))
def maximal_partial_spreads(lag):
    disj = [[not (a & b) for b in lag] for a in lag]
    out = []
    def bk(R, Pc, X):
        if not Pc and not X:
            out.append(frozenset(R)); return
        for v in list(Pc):
            bk(R | {v}, {u for u in Pc if disj[v][u]}, {u for u in X if disj[v][u]}); Pc = Pc - {v}; X = X | {v}
    bk(set(), set(range(len(lag))), set())
    return out, disj
res = {}
# --- (2) d = 4
pts, lag, w = geometry(2, 2); B = bases_for(2, 2, pts, lag)
mps, disj = maximal_partial_spreads(lag)
sizes = Counter(len(S) for S in mps)
small = sorted(next(S for S in mps if len(S) == min(sizes)))
spread = sorted(next(S for S in mps if len(S) == max(sizes)))
res["d4"] = dict(sizes=dict(sizes), min_unextendible=minF(B, small, 4), control_spread_subset=minF(B, spread[:len(small)], 4))
print("d=4: maximal partial spread sizes", dict(sizes), "| min F smallest set %.3e | control %.3e" % (res["d4"]["min_unextendible"], res["d4"]["control_spread_subset"]))
# --- (2) d = 8
pts, lag, w = geometry(2, 3); B = bases_for(2, 3, pts, lag)
mps, disj = maximal_partial_spreads(lag)
sizes = Counter(len(S) for S in mps)
five = sorted(next(S for S in mps if len(S) == 5)); nine = sorted(next(S for S in mps if len(S) == 9))
res["d8"] = dict(sizes=dict(sizes), min_size5=minF(B, five, 8, starts=40), control_spread5=minF(B, nine[:5], 8, starts=20))
print("d=8: sizes", dict(sizes), "| min F size-5 set %.3e | control (5 of a spread) %.3e" % (res["d8"]["min_size5"], res["d8"]["control_spread5"]))
# --- (1) d = 9: all 4-sets of pairwise disjoint lines up to PSp(4,3)
pts, lag, w = geometry(3, 2); B = bases_for(3, 2, pts, lag)
mps, disj = maximal_partial_spreads(lag)
idx = {q: i for i, q in enumerate(pts)}
def norm(v):
    c = next(x for x in v if x); inv = pow(c, -1, 3); return tuple((x * inv) % 3 for x in v)
li = {L: i for i, L in enumerate(lag)}
gens = []
for v in pts:
    perm = [idx[norm(tuple((x + w(q, v) * vi) % 3 for x, vi in zip(q, v)))] for q in pts]
    gens.append([li[frozenset(perm[x] for x in L)] for L in lag])
four = [frozenset(c) for c in itertools.combinations(range(40), 4) if all(disj[a][b] for a, b in itertools.combinations(c, 2))]
seen = {}; reps = []
for S in four:
    if S in seen: continue
    orb = {S}; todo = [S]
    while todo:
        X = todo.pop()
        for gL in gens:
            Y = frozenset(gL[x] for x in X)
            if Y not in orb: orb.add(Y); todo.append(Y)
    for Y in orb: seen[Y] = len(reps)
    reps.append((sorted(S), len(orb)))
in_pentad = lambda S: any(set(S) <= T for T in mps if len(T) == 5)
in_spread = lambda S: any(set(S) <= T for T in mps if len(T) == 10)
rows = []
for S, osz in reps:
    rows.append(dict(orbit=osz, in_pentad=in_pentad(S), in_spread=in_spread(S), minF=minF(B, S, 9, starts=60)))
    print("d=9 4-set orbit size %d in_pentad %s in_spread %s  min F %.3e" % (osz, rows[-1]["in_pentad"], rows[-1]["in_spread"], rows[-1]["minF"]))
res["d9_foursets"] = rows
res["d9_strongly_unextendible_4set_exists"] = any(r["minF"] > 1e-6 for r in rows)
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_census.json"), "w"), indent=1)
