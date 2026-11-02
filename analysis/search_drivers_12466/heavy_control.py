"""12519 positive control at q = 9: a genuine even set with a point of coverage 4 (symmetric difference of the 48-set and a transvection image) is carried
through the same reductions as heavy_split.py: heavy point to x, its 4 lines to the orbit representative, then K to M1, then the stabilisers to M2, M3.
It must end up containing the fixed lines of one listed case and satisfy that case's model.  Then the solver is asked for that case at the set's own weight.
usage: py -3 heavy_control.py [secs]"""
import json, random, sys
import numpy as np
tl = sys.argv[1] if len(sys.argv) > 1 else "600"
sys.argv = ["heavy_split.py", "9", "96", tl]
exec(open("heavy_split.py", encoding="utf-8").read().split("maxz = W //")[0])
src = open("passant_orbits.py", encoding="utf-8").read().split("rng = random.Random(2)")[0]
ns = {}; exec(src, ns)
assert [tuple(p) for p in ns["pts"]] == [tuple(p) for p in B["pts"]]
lidB = {tuple(sorted(L)): j for j, L in enumerate(lines)}
S48 = {lidB[tuple(sorted(ns["lines"][j]))] for j in ns["S"]}
pts = B["pts"]


def transvection(a):
    o = lambda u, v: add[add[mul[u[0]][v[2]]][neg[mul[u[2]][v[0]]]]][add[mul[u[1]][v[3]]][neg[mul[u[3]][v[1]]]]]
    return lambda v: tuple(add[v[i]][mul[o(v, a)][a[i]]] for i in range(4))


rng = random.Random(5); npts = len(pts)
cov = lambda T, p: sum(j in T for j in through[p])
while True:
    lp = B["on_lines"](transvection(pts[rng.randrange(npts)])); lp2 = B["on_lines"](transvection(pts[rng.randrange(npts)]))
    S2 = {lp2[lp[j]] for j in S48}; Sd = S48 ^ S2
    heavy = [p for p in range(npts) if cov(Sd, p) >= 4]
    if heavy and all(cov(Sd, p) % 2 == 0 for p in range(npts)): break
w0 = len(Sd); hp = heavy[0]
cur = set(Sd); moves = 0
while cov(cur, x) < 4:
    lp = B["on_lines"](transvection(pts[rng.randrange(npts)])); cur = {lp[j] for j in cur}; moves += 1
    assert moves < 3000
chosen = sorted(j for j in through[x] if j in cur)[:4]
# carry those 4 lines to a representative by breadth-first search over the pencil generators
targets = {frozenset(r): r for r in reps}
fr = [(frozenset(chosen), None)]; seen_ = {frozenset(chosen): []}; path_ = None
queue = [frozenset(chosen)]
while queue and path_ is None:
    nx_ = []
    for s in queue:
        if s in targets: path_ = seen_[s]; rep4 = targets[s]; break
        for i, lp in enumerate(lps):
            u = frozenset(lp[j] for j in s)
            if u not in seen_: seen_[u] = seen_[s] + [i]; nx_.append(u)
    queue = nx_
assert path_ is not None
for i in path_: cur = {lps[i][j] for j in cur}
L1, L2, L3 = rep4[:3]; assert all(j in cur for j in rep4)
meet1 = [j for y in lines[L1] if y != x for j in others(y, L1)]; M1 = meet1[0]
g = next(g for g in K if any(g[j] == M1 for j in cur & set(meet1))); cur = {int(g[j]) for j in cur}; assert M1 in cur
G1 = K[K[:, M1] == M1]; y2 = next(y for y in lines[L2] if y != x); G2y = G1[np.isin(G1[:, others(y2, L2)[0]], others(y2, L2))]
want2 = {c[4 + 1] for c in cases if c[:5] == rep4 + [M1]}
g = next(g for g in G2y if any(int(g[j]) in want2 for j in cur & set(others(y2, L2)))); cur = {int(g[j]) for j in cur}
M2 = next(m for m in want2 if m in cur); G2 = G2y[G2y[:, M2] == M2]
y3 = next(y for y in lines[L3] if y != x); G3y = G2[np.isin(G2[:, others(y3, L3)[0]], others(y3, L3))]
want3 = {c[6] for c in cases if c[:6] == rep4 + [M1, M2]}
g = next(g for g in G3y if any(int(g[j]) in want3 for j in cur & set(others(y3, L3)))); cur = {int(g[j]) for j in cur}
M3 = next(m for m in want3 if m in cur); case = rep4 + [M1, M2, M3]
assert case in cases and set(case) <= cur and all(cov(cur, p) % 2 == 0 for p in range(npts))
maxcov = max(cov(cur, p) for p in range(npts))
md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(len(lines))]
for p_ in range(npts):
    z = md.NewIntVar(0, w0 // (2 * (q + 1)), f"z{p_}"); md.Add(sum(y[j] for j in through[p_]) == 2 * z)
for j in case: md.Add(y[j] == 1)
md.Add(sum(y) <= w0)
for j in range(len(lines)): md.AddHint(y[j], int(j in cur))
sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = float(tl); sv.parameters.num_workers = 8; st = sv.Solve(md)
out = dict(q=q, weight=w0, max_coverage=maxcov, case_index=cases.index(case), cases=len(cases), lands_in_listed_case=True, status_at_own_weight=sv.StatusName(st))
print(out); json.dump(out, open("heavy_control.json", "w"), indent=1)
