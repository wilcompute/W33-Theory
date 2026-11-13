"""Pass 12653: lift points of the five-qubit maximal 9-set (Pass 12650/12651).  For an uncovered p0, the quotient p0^perp/<p0> is
W(7,2); each Lagrangian L (p0 not in L) gives the Lagrangian (L cap p0^perp + <p0>)/<p0>.  p0 is a LIFT POINT if the nine images are
pairwise disjoint and form a MAXIMAL partial spread of W(7,2) (every quotient Lagrangian meets their union), i.e. the five-qubit set
is a lift of a four-qubit maximal 9-set -- as type B (four qubits) is the lift of the three-qubit 5-sets (Pass 12648).
For each lift point the image set is classified by: number of quotient Lagrangians inside the covered set (Pass 12646 invariant
'n_inside': 17, 14, 12 ... for the certified d = 16 nine-sets) and its numerical min F (1/16 expected if it is one of the certified sets).
Control: the same code on the four-qubit type-B five-set must find 120 lift points and on type A none (Pass 12648).
usage: py -3 analysis/w33_five_qubit_lift_points.py"""
import json, os, time, itertools
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def omega(n):
    lo = (1 << n) - 1
    return lambda a, b: (bin((a & lo) & (b >> n)).count("1") + bin((a >> n) & (b & lo)).count("1")) % 2


def span(gens):
    s = {0}
    for gg in gens:
        s |= {x ^ gg for x in s}
    return s


def lagrangians_of(vecs, w):
    """all maximal isotropic subspaces inside the nondegenerate space spanned by vecs (list of ints, closed under xor incl. 0),
    via orbit of one Lagrangian under the transvections of that space."""
    nz = [v for v in vecs if v]
    # greedy isotropic basis
    basis = []
    for v in nz:
        if all(w(v, b) == 0 for b in basis) and v not in span(basis):
            basis.append(v)
    L0 = frozenset(span(basis)); orb = {L0}; fr = [L0]
    while fr:
        nx = []
        for L in fr:
            for u in nz:
                M = frozenset(x ^ (u if w(u, x) else 0) for x in L)
                if M not in orb: orb.add(M); nx.append(M)
        fr = nx
    return list(orb), len(basis)


def lift_analysis(n, lags_C, w, max_points=None):
    N = 1 << (2 * n)
    C = set().union(*lags_C) - {0}
    U = [p for p in range(1, N) if p not in C]
    out = []
    for p0 in U[: max_points or len(U)]:
        q = next(v for v in range(1, N) if w(v, p0))
        W8 = [v for v in range(N) if w(v, p0) == 0 and w(v, q) == 0]  # complement of <p0, q>: quotient reps
        rep = lambda v: v if w(v, q) == 0 else v ^ p0
        imgs = [frozenset(rep(v) for v in L if v and w(v, p0) == 0) for L in lags_C]
        if any(len(a & b) for a, b in itertools.combinations(imgs, 2)): continue
        out.append((p0, imgs, W8))
    return U, out


def five_qubit_set():
    n = 5; pos = [(i, j) for i in range(n) for j in range(i, n)]
    ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]
    def S(code):
        M = [[0] * n for _ in range(n)]
        for b, (i, j) in enumerate(pos):
            if code >> b & 1: M[i][j] = M[j][i] = 1
        return M
    enc = lambda x, z: x | (z << n)
    lags = [frozenset(enc(x, 0) for x in range(1 << n)), frozenset(enc(0, x) for x in range(1 << n))]
    for c in ex:
        M = S(c)
        zof = lambda x: sum((sum(M[i][j] * (x >> j & 1) for j in range(n)) % 2) << i for i in range(n))
        lags.append(frozenset(enc(x, zof(x)) for x in range(1 << n)))
    return n, lags


def pauli_mats(n):
    X1 = np.array([[0, 1], [1, 0]], complex); Z1 = np.diag([1, -1]).astype(complex)
    def P(v):
        M = np.eye(1)
        for i in range(n):
            xi, zi = v >> i & 1, v >> (n + i) & 1
            M = np.kron(M, (1j) ** (xi * zi) * np.linalg.matrix_power(X1, xi) @ np.linalg.matrix_power(Z1, zi))
        return M
    return P


def minF_quotient(covered_reps, W8, n, w, starts=24, seed=0):
    """numerical min F of the image four-qubit set: map W8 symplectically onto standard W(7,2) coordinates first."""
    # find a symplectic basis e1..e4, f1..f4 of W8
    nz = [v for v in W8 if v]; es, fs = [], []
    rest = list(nz)
    while len(es) < n - 1:
        e = next(v for v in rest if all(w(v, x) == 0 for x in es + fs) and v not in span(es + fs))
        f = next(v for v in rest if w(e, v) == 1 and all(w(v, x) == 0 for x in es + fs))
        es.append(e); fs.append(f)
        rest = [v for v in rest if all(w(v, x) == 0 for x in es + fs)]
    m = n - 1
    coord = {}
    for v in W8:
        x = sum(w(v, fs[i]) << i for i in range(m)); z = sum(w(v, es[i]) << i for i in range(m))
        coord[v] = x | (z << m)
    P = pauli_mats(m); d = 1 << m
    Ps = np.array([P(coord[v]) for v in covered_reps])
    rng = np.random.default_rng(seed)
    def fg(zv):
        v = zv[:d] + 1j * zv[d:]; nv = np.vdot(v, v).real; e = np.einsum("i,kij,j->k", v.conj(), Ps, v).real
        f = (e ** 2).sum() / nv ** 2 / d
        g = (4 * np.einsum("k,kij,j->i", e, Ps, v) / nv ** 2 - 4 * (e ** 2).sum() * v / nv ** 3) / d
        return f, np.concatenate([g.real, g.imag])
    return min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B").fun for _ in range(starts))


def count_lifts(n, lags, w):
    U, cand = lift_analysis(n, lags, w); good = []; cache = {}
    nq = {4: 135, 5: 2295}[n]
    for p0, imgs, W8 in cand:
        key = tuple(W8)
        if key not in cache:
            qL, dimL = lagrangians_of(W8, w); assert len(qL) == nq and dimL == n - 1; cache = {key: qL}
        union = frozenset().union(*imgs)
        if all(len((L - {0}) & union) > 0 for L in cache[key]): good.append(p0)
    return len(good)


t0 = time.time(); res = {}
ex4 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src4 = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src4[: src4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
ctrl = [count_lifts(4, [frozenset(lags4[i]) for i in t["example"]], omega(4)) for t in census["types"]]
print("control four-qubit type A, B lift points:", ctrl, flush=True)
assert ctrl == [0, 120]
res["control_typeA_typeB"] = ctrl
n, lags = five_qubit_set(); w = omega(n)
assert len(set().union(*lags) - {0}) == 279
U, cand = lift_analysis(n, lags, w)
print("five-qubit: uncovered", len(U), "points with disjoint images", len(cand), round(time.time() - t0), "s", flush=True)
qL_cache = None; lifts = []
for p0, imgs, W8 in cand:
    if qL_cache is None or qL_cache[0] != tuple(W8):
        qL, dimL = lagrangians_of(W8, w); assert len(qL) == 2295 and dimL == 4
        qL_cache = (tuple(W8), qL)
    qL = qL_cache[1]
    union = frozenset().union(*imgs)
    maximal = all(len((L - {0}) & union) > 0 for L in qL)
    if not maximal: continue
    inside = sum(1 for L in qL if (L - {0}) <= union)
    lifts.append(dict(p0=p0, n_inside=inside, W8=W8, imgs=imgs))
print("lift points:", len(lifts), "n_inside distribution:", sorted({l["n_inside"] for l in lifts}), round(time.time() - t0), "s", flush=True)
res["n_uncovered"] = len(U); res["disjoint_image_points"] = len(cand); res["lift_points"] = len(lifts)
from collections import Counter
res["n_inside_distribution"] = dict(Counter(l["n_inside"] for l in lifts))
mfs = {}
for l in lifts:
    k = l["n_inside"]
    if k in mfs: continue
    cov = sorted(set().union(*l["imgs"]) - {0})
    mfs[k] = minF_quotient(cov, l["W8"], n, w)
    print("n_inside", k, "image four-qubit set min F", mfs[k], flush=True)
res["image_minF_by_n_inside"] = {str(k): v for k, v in mfs.items()}
res["seconds"] = round(time.time() - t0, 1)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_lift_points.json"), "w"), indent=1)
