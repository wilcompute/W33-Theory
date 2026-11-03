"""12527: independent check of a frame-orbit even set.  Re-solve for the 2^4:S5 minimum; report which monomial orbits compose it; carry it to W(3,q) by the Klein correspondence: a line of W(3,q) (fast_build, form x0y2 - x2y0 + x1y3 - x3y1) has Plucker vector; on the hyperplane p02 + p13 = 0 the quadric is p01 p23 - p02 p13 + p03 p12 = p01 p23 + p02^2 + p03 p12, which is carried to sum x_i^2 explicitly when i^2 = -1 exists (q = 1 mod 4).  Then every point of W(3,q) must lie on an even number of the chosen lines, in that separately built geometry.  usage: py -3 verify_frame_set.py q"""
import json, sys, collections
src = open("frame_orbits.py", encoding="utf-8").read().split("res = []\nfor name, perms in S.items():")[0]
qarg = sys.argv[1]; sys.argv = ["frame_orbits.py", qarg, "300", "4"]; exec(src)
from symmetric_fast import fast_build
gens = [perm_of(list(g)) for g in S["S5"]] + sign; lab = orbits(gens); reps = np.unique(lab); idx = {int(r): i for i, r in enumerate(reps)}; sizes = np.bincount([idx[int(x)] for x in lab])
md = cp_model.CpModel(); y = [md.NewBoolVar(f"o{i}") for i in range(len(reps))]; seen = set()
for L in lines:
    c = {}
    for p in L: c[idx[int(lab[p])]] = c.get(idx[int(lab[p])], 0) + 1
    k = tuple(sorted(c.items()))
    if k in seen: continue
    seen.add(k); z = md.NewIntVar(0, (q + 1) // 2, f"z{len(seen)}"); md.Add(sum(v * y[o] for o, v in c.items()) == 2 * z)
tot = sum(int(sizes[i]) * y[i] for i in range(len(reps))); md.Add(tot >= 1); md.Minimize(tot)
sv = cp_model.CpSolver(); sv.parameters.num_workers = 4; sv.parameters.max_time_in_seconds = 300; st = sv.Solve(md); assert st == cp_model.OPTIMAL
chosen = [i for i in range(len(reps)) if sv.Value(y[i])]; T = {p for p in range(n) if idx[int(lab[p])] in chosen}
res = dict(q=q, weight=len(T), orbit_table=[dict(rep=pts[int(reps[i])].tolist(), size=int(sizes[i]), hamming=int((pts[int(reps[i])] != 0).sum()), chosen=i in chosen) for i in range(len(reps))])
hist = collections.Counter(sum(p in T for p in L) for L in lines); res["line_intersection_histogram"] = {int(k): int(v) for k, v in sorted(hist.items())}
# Klein: x = (p01, p23, p03, p12, p02); Q = p01 p23 + p03 p12 + p02^2.  With i^2 = -1 and h = 1/2: u v = a^2 + b^2 for a = h(u + v), b = h(u - v)/i ...
imag = next((c for c in F if c and sq[c] == neg[1]), None); assert imag is not None, "needs q = 1 mod 4"
h = inv[add[1][1]]; ii = inv[imag]
def to_sq(u, v):
    a = mul[h][add[u][v]]; b = mul[mul[h][add[u][neg[v]]]][ii]
    return a, b
pW, lW = fast_build(q); hits = [0] * len(pW); cnt = 0; form_ok = True
def det2(a, b, i, j): return add[mul[a[i]][b[j]]][neg[mul[a[j]][b[i]]]]
for j, L in enumerate(lW):
    a, b = pW[L[0]], pW[L[1]]
    p01, p23, p03, p12, p02, p13 = det2(a, b, 0, 1), det2(a, b, 2, 3), det2(a, b, 0, 3), det2(a, b, 1, 2), det2(a, b, 0, 2), det2(a, b, 1, 3)
    form_ok &= add[p02][p13] == 0
    x = to_sq(p01, p23) + to_sq(p03, p12) + (p02,)
    assert sum(1 for t in x if t) > 0
    s_ = 0
    for t in x: s_ = add[s_][mul[t][t]]
    form_ok &= s_ == 0
    pid_ = pid[norm(tuple(int(t) for t in x))]
    if pid_ in T:
        cnt += 1
        for p in L: hits[p] += 1
res.update(isotropic_lines_have_p02_plus_p13_zero_and_map_to_the_quadric=bool(form_ok), lines_in_W=cnt, all_points_even_in_W=all(h_ % 2 == 0 for h_ in hits), coverage_in_W={int(k): int(v) for k, v in sorted(collections.Counter(hits).items())})
print(json.dumps(res)); json.dump(res, open(f"verify_frame_set_q{q}.json", "w"), indent=1)
