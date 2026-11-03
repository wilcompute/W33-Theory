"""12527: orthonormal-frame hyperovals.  Q(4,q) = sum x_i^2 = 0 (dual to W(3,q)); the monomial group 2^4:S5 stabilises the frame.  (1) q = 5: the 20 weight-2 singular points meet every singular line in 0 or 2; with the uniqueness of 12525 this IS the minimal set, explaining W(D5).  (2) search: minimum nonzero even set that is a union of orbits of a monomial subgroup, for q = 3..25.  Each answer is re-verified directly.  usage: py -3 frame_orbits.py q [secs] [workers]"""
import itertools, json, sys, time
import numpy as np
from ortools.sat.python import cp_model
from symmetric_even_sets_gf import setup
q = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 300; wk = int(sys.argv[3]) if len(sys.argv) > 3 else 4
F, add, mul, inv, neg = setup(q); Add = np.array([[add[a][b] for b in F] for a in F]) if list(F) == list(range(q)) else None; Mul = np.array([[mul[a][b] for b in F] for a in F]); assert Add is not None
sq = Mul[np.arange(q), np.arange(q)]
def dot(A, B):
    r = np.zeros(A.shape[:-1], dtype=np.int64)
    for i in range(5): r = Add[r, Mul[A[..., i], B[..., i]]]
    return r
pts = []
# normalised vectors with first nonzero coordinate 1; singular ones only
for lead in range(5):
    tail = 4 - lead
    if tail == 0: pts.append(np.array([[0] * lead + [1]], dtype=np.int64)); continue
    grids = np.stack(np.meshgrid(*[np.arange(q)] * tail, indexing="ij"), -1).reshape(-1, tail)
    A_ = np.zeros((len(grids), 5), dtype=np.int64); A_[:, lead] = 1; A_[:, lead + 1:] = grids; pts.append(A_)
pts = np.vstack(pts)
pts = pts[dot(pts, pts) == 0]; n = len(pts); assert n == (q + 1) * (q * q + 1), n
pid = {tuple(p): i for i, p in enumerate(pts.tolist())}
def norm(v):
    f = next(x for x in v if x); s = inv[f]; return tuple(mul[s][x] for x in v)
lines = set()
for i in range(n):
    perp = np.flatnonzero(dot(pts, pts[i][None]) == 0)
    for j in perp:
        j = int(j)
        if j <= i: continue
        L = {i, j}
        for t in F:
            if t: L.add(pid[norm(tuple(add[pts[i][k]][mul[t][pts[j][k]]] for k in range(5)))])
        lines.add(tuple(sorted(L)))
lines = sorted(lines); assert len(lines) == n and all(len(L) == q + 1 for L in lines), len(lines)
inc = [[] for _ in range(n)]
for j, L in enumerate(lines):
    for p in L: inc[p].append(j)
out = dict(q=q, points=n)
wt = (pts != 0).sum(1); out["weight_counts"] = {int(k): int((wt == k).sum()) for k in np.unique(wt)}
for w_ in sorted(out["weight_counts"]):
    T = set(np.flatnonzero(wt == w_).tolist()); c = {sum(p in T for p in L) for L in lines}; out[f"weight_{w_}_line_intersections"] = sorted(c)
def perm_of(g, sgn=None):
    r = []
    for p in pts.tolist():
        v = [p[g[k]] for k in range(5)]
        if sgn: v = [neg[x] if sgn[k] else x for k, x in enumerate(v)]
        r.append(pid[norm(tuple(v))])
    return np.array(r)
sign = [perm_of(list(range(5)), [1 if k == i else 0 for k in range(5)]) for i in range(5)]
S = {"S5": [(1, 0, 2, 3, 4), (1, 2, 3, 4, 0)], "A5": [(1, 2, 0, 3, 4), (1, 2, 3, 4, 0)], "F20": [(1, 2, 3, 4, 0), (0, 2, 4, 1, 3)], "D5": [(1, 2, 3, 4, 0), (0, 4, 3, 2, 1)], "C5": [(1, 2, 3, 4, 0)], "S4": [(1, 0, 2, 3, 4), (1, 2, 3, 0, 4)], "A4": [(1, 2, 0, 3, 4), (1, 0, 3, 2, 4)]}
def orbits(gens):
    lab = np.arange(n)
    while True:
        old = lab.copy()
        for g in gens:
            np.minimum.at(lab, g, lab.copy()); lab = np.minimum(lab, lab[g])
        lab = lab[lab]
        if (lab == old).all(): return lab
res = []
for name, perms in S.items():
    for use_sign in (True,):
        gens = [perm_of(list(g)) for g in perms] + (sign if use_sign else [])
        lab = orbits(gens); reps = np.unique(lab); idx = {int(r): i for i, r in enumerate(reps)}; sizes = np.bincount([idx[int(x)] for x in lab])
        md = cp_model.CpModel(); y = [md.NewBoolVar(f"o{i}") for i in range(len(reps))]; seen = set()
        for L in lines:
            c = {}
            for p in L: c[idx[int(lab[p])]] = c.get(idx[int(lab[p])], 0) + 1
            k = tuple(sorted(c.items()))
            if k in seen: continue
            seen.add(k); z = md.NewIntVar(0, (q + 1) // 2, f"z{len(seen)}"); md.Add(sum(v * y[o] for o, v in c.items()) == 2 * z)
        tot = sum(int(sizes[i]) * y[i] for i in range(len(reps))); md.Add(tot >= 1); md.Minimize(tot)
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = wk; t0 = time.time(); st = sv.Solve(md)
        rec = dict(group="2^4:" + name, orbits=len(reps), status=sv.StatusName(st), seconds=round(time.time() - t0, 1))
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            T = {p for p in range(n) if sv.Value(y[idx[int(lab[p])]])}; assert all(sum(p in T for p in L) % 2 == 0 for L in lines)
            cov = sorted({sum(p in T for p in L) for L in lines}); rec.update(weight=len(T), intersections=cov, bound=sv.BestObjectiveBound())
        res.append(rec); print(rec, flush=True)
out["search"] = res; json.dump(out, open(f"frame_orbits_q{q}.json", "w"), indent=1, default=str); print({k: v for k, v in out.items() if k != "search"}, flush=True)
