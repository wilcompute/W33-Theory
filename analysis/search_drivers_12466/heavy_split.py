"""12519 (strengthened): even line sets with a point x on >= 4 chosen lines, split by the group K fixing every line through x.

K = q^{1+2} : F_q^* (Heisenberg radical of the point stabiliser, plus a homology) is computed as explicit line permutations; each generator
is asserted to preserve W(3,q) and to fix all q+1 lines through x.  Three reductions, each exhaustive:
  (a) coverage: 2k chosen lines at a point force weight >= 2k(q+1), since their further neighbours are pairwise disjoint (no triangles), so
      every point has coverage <= 2*floor(W / (2(q+1)));
  (b) K is transitive on the q^2 lines meeting L1 off x (asserted), so S may be assumed to contain one fixed such line M1;
  (c) S has a further line through a chosen point y2 of L2 (and y3 of L3); branch on these lines modulo the stabiliser in K of what is fixed.
Infeasibility of every case proves no even set of <= W lines has a point of coverage >= 4.  An UNKNOWN case proves nothing.
usage: py -3 heavy_split.py q W [secs] [min]     (min: minimise the weight in each case instead of a feasibility test)"""
import itertools, json, sys, time
import numpy as np
from ortools.sat.python import cp_model
from star_cubes import build, _pow, _char

q, W = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 1800
minimise = len(sys.argv) > 4 and sys.argv[4] == "min"
B = build(q); F, add, mul, inv, neg = B["F"], B["add"], B["mul"], B["inv"], B["neg"]
lines, through, pid, norm = B["lines"], B["through"], B["pid"], B["norm"]
x = pid[norm((1, 0, 0, 0))]
pencil = sorted(through[x]); assert len(pencil) == q + 1
prim = next(c for c in F if c and len({_pow(B, c, k) for k in range(q - 1)}) == q - 1)


def block(A):      # A in SL(2,q) on (x1, x3); identity on (x0, x2)
    return lambda v: (v[0], add[mul[A[0][0]][v[1]]][mul[A[0][1]][v[3]]], v[2], add[mul[A[1][0]][v[1]]][mul[A[1][1]][v[3]]])


gens = [block(((1, 1), (0, 1))), block(((1, prim), (0, 1))), block(((0, 1), (neg[1], 0))), lambda v: (v[0], v[1], mul[prim][v[2]], mul[prim][v[3]])]
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
    seen |= o; reps.append(sorted(S))


def heis(a, b, c):      # the radical, in the form x0 w2 - x2 w0 + x1 w3 - x3 w1
    def f(v):
        v0, v1, v2, v3 = v
        na = add[add[v0][mul[a][v1]]][add[mul[b][v3]][mul[c][v2]]]
        return (na, add[v1][mul[b][v2]], v2, add[v3][mul[neg[a]][v2]])
    return f


def homology(c):
    return lambda v: (mul[mul[c][c]][v[0]], mul[c][v[1]], v[2], mul[c][v[3]])


K = []
for a, b, c, d in itertools.product(F, F, F, [t for t in F if t]):
    h, g = heis(a, b, c), homology(d)
    K.append(B["on_lines"](lambda v: h(g(v))))
K = np.array(K, dtype=np.int32)
assert len({r.tobytes() for r in K}) == q ** 3 * (q - 1), "K must have q^3 (q-1) distinct line permutations"
assert (K[:, pencil] == np.array(pencil)).all(), "K must fix every line through x"


def orbit_reps(cands, G):
    left, out = set(cands), []
    while left:
        j = min(left); o = set(int(t) for t in np.unique(G[:, j])); assert o <= set(cands)
        out.append(j); left -= o
    return out


def others(y, L):
    return [j for j in through[y] if j != L]


cases = []
for S4 in reps:
    L1, L2, L3 = S4[:3]
    meet1 = [j for y in lines[L1] if y != x for j in others(y, L1)]
    assert len(meet1) == q * q and len(orbit_reps(meet1, K)) == 1, "K must be transitive on the lines meeting L1 off x"
    M1 = meet1[0]; G1 = K[K[:, M1] == M1]
    y2 = next(y for y in lines[L2] if y != x)
    G2y = G1[np.isin(G1[:, others(y2, L2)[0]], others(y2, L2))]
    for M2 in orbit_reps(others(y2, L2), G2y):
        G2 = G2y[G2y[:, M2] == M2]
        y3 = next(y for y in lines[L3] if y != x)
        G3y = G2[np.isin(G2[:, others(y3, L3)[0]], others(y3, L3))]
        for M3 in orbit_reps(others(y3, L3), G3y):
            cases.append(S4 + [M1, M2, M3])
print(f"q={q}, W={W}: {len(reps)} pencil 4-subset orbits, |K|={len(K)}, {len(cases)} cases", flush=True)
maxz = W // (2 * (q + 1))
assert maxz >= 2, "W below the bound 4(q+1): nothing to do"
res = dict(q=q, W=W, cases=len(cases), infeasible=0, feasible=[], unknown=[]); t0 = time.time()
for n, fixed in enumerate(cases):
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{j}") for j in range(len(lines))]
    for p_ in range(len(B["pts"])):
        z = md.NewIntVar(0, maxz, f"z{p_}"); md.Add(sum(y[j] for j in through[p_]) == 2 * z)
    for j in fixed: md.Add(y[j] == 1)
    md.Add(sum(y) <= W)
    if minimise: md.Minimize(sum(y))
    sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
    st = sv.Solve(md)
    if st == cp_model.INFEASIBLE: res["infeasible"] += 1
    elif st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        res["feasible"].append(dict(case=n, status=sv.StatusName(st), weight=sum(sv.Value(v) for v in y), chosen=[j for j in range(len(lines)) if sv.Value(y[j])]))
    else: res["unknown"].append(n)
    print(f"  {n + 1}/{len(cases)}: {sv.StatusName(st)} infeasible {res['infeasible']} feasible {len(res['feasible'])} unknown {len(res['unknown'])} {time.time() - t0:.0f}s", flush=True)
res["seconds"] = round(time.time() - t0, 1)
print({k: v for k, v in res.items() if k != "feasible"}, "weights", [(f["weight"], f["status"]) for f in res["feasible"]][:20], flush=True)
json.dump(res, open(f"heavy_split_q{q}_W{W}{'_min' if minimise else ''}.json", "w"), indent=1)
