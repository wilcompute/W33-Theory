"""Item 1: two ququints (d = 25, W(3,5)) and item 3: three qubits at degree 8.
(1) M = (1/d) sum_{u covered, u != 0} W_u (x) W_u^dag (twirl identity, no bases needed); delta* = lambda_min(Pi M Pi | Sym^2(C^d)) > 0 proves
    strong unextendibility.  Control: the d = 9 pentad gives 1/9.  d = 25: random greedy maximal partial spreads of W(3,5): size, delta*,
    and the sentinel structure of the uncovered set (splits {b, b-perp} inside it, uniform multiplicity?).
(3) three qubits, size-5 unextendible sets: degree-8 Hermitian bound via the unique representative of the (4,4)-form on Sym^4(C^8).
usage: py -3 analysis/w33_ququint_umub.py"""
import itertools, json, os, random
from collections import Counter
import numpy as np
import scipy.sparse as sp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
exec(_src[: _src.index("\nres = {}")], cs)
geometry, pauli_ops, bases_for, maximal_partial_spreads = cs["geometry"], cs["pauli_ops"], cs["bases_for"], cs["maximal_partial_spreads"]
def sym2_basis(d):
    cols = []
    for i in range(d):
        for j in range(i, d):
            v = np.zeros(d * d)
            if i == j: v[i * d + i] = 1
            else: v[i * d + j] = v[j * d + i] = 1 / np.sqrt(2)
            cols.append(v)
    return np.array(cols).T
def delta_from_cover(p, n, pts, covered_pts):
    d = p ** n; op = pauli_ops(p, n)
    S = sp.csr_matrix(sym2_basis(d))
    acc = sp.csr_matrix((d * d, d * d), dtype=complex)
    for i in covered_pts:
        for c in range(1, p):
            u = tuple((c * x) % p for x in pts[i])
            W = sp.csr_matrix(op(u))
            acc = acc + sp.kron(W, W.conj().T, format="csr")
    H = (S.T @ acc @ S).toarray() / d
    H = (H + H.conj().T) / 2
    return float(np.linalg.eigvalsh(H)[0])
out = {}
pts9, lag9, w9 = geometry(3, 2)
mps9, disj9 = maximal_partial_spreads(lag9)
pent = sorted(next(S for S in mps9 if len(S) == 5))
out["control_d9_pentad"] = delta_from_cover(3, 2, pts9, frozenset().union(*[lag9[L] for L in pent]))
print("control d=9 pentad via twirl formula: delta* = %.6f (expect 1/9)" % out["control_d9_pentad"], flush=True)
pts, lag, w = geometry(5, 2)
nL = len(lag)
print("W(3,5): points", len(pts), "lines", nL, flush=True)
disj = [[not (lag[a] & lag[b]) for b in range(nL)] for a in range(nL)]
idx = {q: i for i, q in enumerate(pts)}
def norm(v):
    c = next(x for x in v if x); inv = pow(c, -1, 5); return tuple((x * inv) % 5 for x in v)
planes = set()
for a, b in itertools.combinations(range(len(pts)), 2):
    if w(pts[a], pts[b]) != 0:
        planes.add(frozenset(idx[norm(tuple((x * pts[a][k] + y * pts[b][k]) % 5 for k in range(4)))] for x in range(5) for y in range(5) if (x, y) != (0, 0)))
perp = lambda S2: frozenset(i for i in range(len(pts)) if all(w(pts[i], pts[j]) == 0 for j in S2))
splits = [tuple(s) for s in {frozenset((S2, perp(S2))) for S2 in planes}]
print("splits of W(3,5):", len(splits), flush=True)
rng = random.Random(3)
rows = []; seen = set()
for trial in range(24):
    order = list(range(nL)); rng.shuffle(order)
    C = []
    for L in order:
        if all(disj[L][M] for M in C):
            C.append(L)
    key = frozenset(C)
    if key in seen: continue
    seen.add(key)
    cov = frozenset().union(*[lag[L] for L in C]); unc = frozenset(range(len(pts))) - cov
    inside = [s for s in splits if (s[0] | s[1]) <= unc]
    mult = Counter(q for b, bp in inside for q in (b | bp))
    uniform = bool(mult) and set(mult) == unc and len(set(mult.values())) == 1
    dl = delta_from_cover(5, 2, pts, cov)
    rows.append(dict(size=len(C), delta=dl, uncovered=len(unc), n_splits_inside=len(inside), uniform_split_cover=uniform, mult=sorted(set(mult.values()))))
    print("d=25 maximal partial spread size %2d  uncovered %3d  delta* %+.4f  splits inside %d  uniform cover %s" % (len(C), len(unc), dl, len(inside), uniform), flush=True)
out["d25"] = rows
out["d25_certified"] = [r for r in rows if r["delta"] > 1e-6]
# three qubits, degree 8
pts8, lag8, w8 = geometry(2, 3); B8 = bases_for(2, 3, pts8, lag8)
mps8, disj8 = maximal_partial_spreads(lag8)
five = sorted(next(S for S in mps8 if len(S) == 5))
E = [b for L in five for b in B8[L].T]
d = 8
cols = []
for combo in itertools.combinations_with_replacement(range(d), 4):
    v = np.zeros(d ** 4)
    for pp in set(itertools.permutations(combo)):
        ix = 0
        for x in pp: ix = ix * d + x
        v[ix] = 1
    cols.append(v / np.linalg.norm(v))
S4 = np.array(cols).T
I8 = np.eye(d)
X = S4.T.reshape(-1, d, d, d, d)
KS = np.zeros(X.shape, complex)
for e in E:
    A = np.outer(e, e.conj()) - I8 / d
    KS += np.einsum("ai,bj,nijkl->nabkl", A, A, X)
H = S4.T @ KS.reshape(X.shape[0], -1).T
H = (H + H.conj().T) / 2
out["three_qubit_degree8_delta"] = float(np.linalg.eigvalsh(H)[0])
print("three qubits, size 5: degree-8 Hermitian bound delta_8 = %.6f" % out["three_qubit_degree8_delta"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_ququint_umub.json"), "w"), indent=1, default=str)
