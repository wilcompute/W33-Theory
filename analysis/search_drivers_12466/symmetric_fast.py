"""12499: fast W(3,q) builder (totally isotropic 2-spaces enumerated in reduced echelon form, any GF(q)) and the symmetric even-line-set
search on point->line adjacency lists, for q far beyond the pairwise builder (q = 25, 27, 49).  The builder is checked against
even_line_sets_gf.build at q = 3, 5, 9 (same line sets).  usage: py -3 symmetric_fast.py q r [time] [k ...]  |  py -3 symmetric_fast.py check"""
import sys, json, time, itertools
from ortools.sat.python import cp_model
from even_line_sets_gf import field


def fast_build(q):
    F, add, mul = field(q)
    inv = {a: next(b for b in F if mul[a][b] == 1) for a in F if a}
    neg = {a: next(b for b in F if add[a][b] == 0) for a in F}

    def omega(u, v):                                     # u0 v2 + u1 v3 - u2 v0 - u3 v1
        s = add[mul[u[0]][v[2]]][mul[u[1]][v[3]]]
        return add[s][neg[add[mul[u[2]][v[0]]][mul[u[3]][v[1]]]]]

    def norm(v):
        f = next(x for x in v if x); s = inv[f]
        return tuple(mul[s][x] for x in v)
    pts, pid, lines = [], {}, []

    def pidx(v):
        v = norm(v)
        if v not in pid: pid[v] = len(pts); pts.append(v)
        return pid[v]
    for c1, c2 in itertools.combinations(range(4), 2):
        free1 = [j for j in range(c1 + 1, 4) if j != c2]       # row 1: 1 at c1, 0 at c2, free right of c1
        free2 = [j for j in range(c2 + 1, 4)]                  # row 2: 1 at c2, free right of c2
        for vals in itertools.product(F, repeat=len(free1) + len(free2)):
            r1 = [0] * 4; r2 = [0] * 4; r1[c1] = 1; r2[c2] = 1
            for idx, (j, x) in enumerate(zip(free1 + free2, vals)):
                (r1 if idx < len(free1) else r2)[j] = x
            if omega(r1, r2): continue
            L = [pidx(r2)] + [pidx([add[r1[i]][mul[t][r2[i]]] for i in range(4)]) for t in F]
            lines.append(tuple(sorted(L)))
    assert len(lines) == (q + 1) * (q * q + 1) and len(pts) == len(lines), (len(lines), len(pts))
    return pts, lines


def run(q, r, k, tl, pre):
    from symmetric_even_sets_gf import setup, sl2_of_order, matmul
    pts, lines = pre
    F, add, mul, inv, neg = setup(q)
    pid = {p: i for i, p in enumerate(pts)}
    A = sl2_of_order(q, r, F, add, mul, inv, neg); B = ((1, 0), (0, 1))
    for _ in range(k): B = matmul(B, A, add, mul)
    lin = lambda M, x, y: (add[mul[M[0][0]][x]][mul[M[0][1]][y]], add[mul[M[1][0]][x]][mul[M[1][1]][y]])

    def act(v):
        w0, w2 = lin(A, v[0], v[2]); w1, w3 = lin(B, v[1], v[3]); w = (w0, w1, w2, w3)
        s = inv[next(x for x in w if x)]
        return pid[tuple(mul[s][x] for x in w)]
    perm = [act(p) for p in pts]
    lid = {L: j for j, L in enumerate(lines)}
    lperm = [lid[tuple(sorted(perm[x] for x in L))] for L in lines]

    def orbits(pm):
        seen, out = set(), []
        for s in range(len(pm)):
            if s in seen: continue
            o = [s]; seen.add(s); t = pm[s]
            while t != s: o.append(t); seen.add(t); t = pm[t]
            out.append(o)
        return out
    lo, po = orbits(lperm), orbits(perm)
    lorb = {j: i for i, o in enumerate(lo) for j in o}
    through = [[] for _ in pts]
    for j, L in enumerate(lines):
        for p in L: through[p].append(j)
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{i}") for i in range(len(lo))]
    for o in po:
        cnt = {}
        for j in through[o[0]]: cnt[lorb[j]] = cnt.get(lorb[j], 0) + 1
        z = md.NewIntVar(0, q + 1, f"z{o[0]}")
        md.Add(sum(c * y[i] for i, c in cnt.items()) == 2 * z)
    wt = sum(len(o) * y[i] for i, o in enumerate(lo))
    md.Add(wt >= 1); md.Minimize(wt)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
    t0 = time.time(); st = s.Solve(md)
    rec = dict(q=q, r=r, k=k, line_orbits=len(lo), status=s.StatusName(st), seconds=round(time.time() - t0, 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [j for i, o in enumerate(lo) if s.Value(y[i]) for j in o]
        cov = [0] * len(pts)
        for j in chosen:
            for p in lines[j]: cov[p] += 1
        rec.update(weight=len(chosen), verified_even=all(c % 2 == 0 for c in cov), coverage_profile=sorted(set(cov)),
                   bound=s.BestObjectiveBound(), chosen=chosen)
    return rec


if __name__ == "__main__":
    if sys.argv[1] == "check":
        from even_line_sets_gf import build
        for q in (3, 5, 9):
            p1, l1, _ = build(q); p2, l2 = fast_build(q)
            a = {frozenset(p1[x] for x in L) for L in l1}; b = {frozenset(p2[x] for x in L) for L in l2}
            print(q, "same line sets:", a == b, len(a))
        sys.exit()
    q, r = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    ks = [int(x) for x in sys.argv[4:]] or list(range(0, r // 2 + 1))
    t0 = time.time(); pre = fast_build(q); print(f"built W(3,{q}) in {time.time() - t0:.0f}s", flush=True)
    out = []
    for k in ks:
        rec = run(q, r, k, tl, pre)
        print(json.dumps({x: v for x, v in rec.items() if x != "chosen"}), flush=True); out.append(rec)
    json.dump(out, open(f"symmetric_fast_q{q}_r{r}.json", "w"), indent=1)
