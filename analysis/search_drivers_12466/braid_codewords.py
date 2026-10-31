"""12507: braiding acts on the minimal even line sets of W(3,3).  The SU(2)_4 / Temperley-Lieb (delta = sqrt 3) braid generators are
order-3 symplectic transvections T_p(x) = x + w(x,p) p along an induced path p_0..p_4 in the two-qutrit noncommutation graph (other
track, ad8846e59; Cui-Wang metaplectic anyons: braid image = qutrit Clifford).  For B_k (k-1 generators, k = 3..6): the order of the
generated group on the 40 points (PSp(4,3) has 25,920) and its orbits on the 216 minimal even line sets (Pass 173's route codewords,
one PSp(4,3)-orbit).  Braid relations are checked.  usage: py -3 braid_codewords.py"""
import json, itertools
import numpy as np
from even_line_sets_gf import build
from scipy.optimize import milp, LinearConstraint, Bounds

q = 3
pts, lines, N = build(q); n = len(pts)
pid = {p: i for i, p in enumerate(pts)}; lid = {frozenset(l): j for j, l in enumerate(lines)}
w = lambda u, v: (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % q
def norm(v):
    f = next(x for x in v if x); s = pow(f, -1, q); return tuple(x * s % q for x in v)
def T(a):
    return tuple(pid[norm(tuple((x[c] + w(x, a) * a[c]) % q for c in range(4)))] for x in pts)
# induced path in the noncommutation graph (adjacent iff w != 0)
nc = lambda i, j: w(pts[i], pts[j]) != 0
path = None
for p0 in range(n):
    stack = [[p0]]
    while stack and path is None:
        P = stack.pop()
        if len(P) == 5: path = P; break
        for v in range(n):
            if v not in P and nc(P[-1], v) and all(not nc(u, v) for u in P[:-1]): stack.append(P + [v])
    if path: break
gens = [T(pts[p]) for p in path]
compose = lambda a, b: tuple(a[b[i]] for i in range(n))       # a after b
braid_ok = all(compose(compose(gens[i], gens[i + 1]), gens[i]) == compose(compose(gens[i + 1], gens[i]), gens[i + 1]) for i in range(4))
far_ok = all(compose(gens[i], gens[j]) == compose(gens[j], gens[i]) for i in range(5) for j in range(i + 2, 5))
def group(gs, cap=30000):
    e = tuple(range(n)); seen = {e}; fr = [e]
    while fr and len(seen) <= cap:
        nx_ = []
        for g in fr:
            for h in gs:
                k = compose(h, g)
                if k not in seen: seen.add(k); nx_.append(k)
        fr = nx_
    return seen
# the 216 minimal even line sets: orbit of one optimum under all transvections
m = len(lines); c = np.concatenate([np.ones(m), np.zeros(n)])
M = np.vstack([np.hstack([N, -2 * np.eye(n)]), np.concatenate([np.ones(m), np.zeros(n)])[None, :]])
r = milp(c, constraints=LinearConstraint(M, np.concatenate([np.zeros(n), [1]]), np.concatenate([np.zeros(n), [np.inf]])),
         integrality=np.ones(m + n), bounds=Bounds(np.zeros(m + n), np.concatenate([np.ones(m), np.full(n, 2)])))
start = frozenset(np.flatnonzero(np.round(r.x[:m])).tolist())
lmap = lambda g: [lid[frozenset(g[x] for x in lines[j])] for j in range(m)]
allT = [lmap(T(a)) for a in pts]
orb = {start}; fr = [start]
while fr:
    nx_ = []
    for S in fr:
        for g in allT:
            S2 = frozenset(g[j] for j in S)
            if S2 not in orb: orb.add(S2); nx_.append(S2)
    fr = nx_
codewords = list(orb)
out = dict(path=path, braid_relations=braid_ok, far_commutation=far_ok, minimal_codewords=len(codewords), by_k={})
for k in range(3, 7):
    G = group(gens[:k - 1])
    lms = [lmap(g) for g in gens[:k - 1]]
    seen, orbs = set(), []
    for S in codewords:
        if S in seen: continue
        o = {S}; f = [S]
        while f:
            nx_ = []
            for X in f:
                for g in lms:
                    Y = frozenset(g[j] for j in X)
                    if Y not in o: o.add(Y); nx_.append(Y)
            f = nx_
        seen |= o; orbs.append(len(o))
    out["by_k"][k] = dict(generators=k - 1, group_order_on_points=len(G), orbits_on_216=sorted(orbs))
    print(k, out["by_k"][k], flush=True)
print(json.dumps({k: v for k, v in out.items() if k != "by_k"}))
json.dump(out, open("braid_codewords.json", "w"), indent=1)
