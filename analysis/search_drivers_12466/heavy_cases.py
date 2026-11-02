"""12519: the other half of the cube-and-conquer: even line sets with a point on at least 4 chosen lines.  PSp(4,q) is transitive on
points, so take x = e0; the lines through x are a PG(1,q) = {span(e0, a e1 + b e3)} on which SL(2,q) (acting on <e1, e3>), the similitude
(x2, x3) -> (c x2, c x3) and the field automorphism all act.  Fix one representative of each orbit on 4-subsets of those lines, then ask
for an even line set (any coverage) of at most W lines containing them.  Every such set has >= 4(q+1) lines (other track's bound).
Infeasibility of every case proves no even set of <= W lines has a point of coverage >= 4.  usage: py -3 heavy_cases.py q W [secs]"""
import itertools, json, sys, time
from ortools.sat.python import cp_model
from star_cubes import build, _pow, _char

q, W = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
B = build(q); F, add, mul, inv, neg = B["F"], B["add"], B["mul"], B["inv"], B["neg"]
lines, through, pid, norm = B["lines"], B["through"], B["pid"], B["norm"]
x = pid[norm((1, 0, 0, 0))]
pencil = sorted(through[x]); assert len(pencil) == q + 1
prim = next(c for c in F if c and len({_pow(B, c, k) for k in range(q - 1)}) == q - 1)
def block(A):      # A in SL(2,q) on (x1, x3); identity on (x0, x2)
    return lambda v: (v[0], add[mul[A[0][0]][v[1]]][mul[A[0][1]][v[3]]], v[2], add[mul[A[1][0]][v[1]]][mul[A[1][1]][v[3]]])
gens = [block(((1, 1), (0, 1))), block(((1, prim), (0, 1))), block(((0, 1), (neg[1], 0))),
        lambda v: (v[0], v[1], mul[prim][v[2]], mul[prim][v[3]])]
p, k = _char(q)
if k > 1: gens.append(lambda v: tuple(_pow(B, t, p) for t in v))
lps = [B["on_lines"](g) for g in gens]
assert all(set(lp[j] for j in pencil) == set(pencil) for lp in lps), "generators must fix x"
seen, reps = set(), []
for S in itertools.combinations(pencil, 4):
    S = frozenset(S)
    if S in seen: continue
    o = {S}; fr = [S]
    while fr:
        nx_ = []
        for T in fr:
            for lp in lps:
                U = frozenset(lp[j] for j in T)
                if U not in o: o.add(U); nx_.append(U)
        fr = nx_
    seen |= o; reps.append((sorted(S), len(o)))
print(f"q={q}: {len(reps)} orbits on 4-subsets of the pencil, sizes {[r[1] for r in reps]}", flush=True)
res = dict(q=q, W=W, cases=len(reps), results=[]); t0 = time.time()
for S, size in reps:
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(len(lines))]
    for p_ in range(len(B["pts"])):
        z = md.NewIntVar(0, (q + 1) // 2, f"z{p_}"); md.Add(sum(y[j] for j in through[p_]) == 2 * z)
    for j in S: md.Add(y[j] == 1)
    md.Add(sum(y) <= W)
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
    st = sv.Solve(md); rec = dict(orbit_size=size, status=sv.StatusName(st), seconds=round(sv.WallTime(), 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE): rec["weight"] = sum(sv.Value(v) for v in y); rec["chosen"] = [j for j in range(len(lines)) if sv.Value(y[j])]
    res["results"].append(rec); print({k: v for k, v in rec.items() if k != "chosen"}, flush=True)
res["seconds"] = round(time.time() - t0, 1); json.dump(res, open(f"heavy_cases_q{q}_W{W}.json", "w"), indent=1)
