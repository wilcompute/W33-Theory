"""12501: icosahedral even line sets of W(3,q).  The q = 9 48-line set is ONE orbit of K = F_q^* . 2.A5 . 2 acting on a hyperbolic
pair X (+) Y (M on X, M^{-T} on Y, plus the swap x_i -> y_i, y_i -> -x_i).  For every q with A5 < PSL(2,q), build such K and find the
smallest K-invariant even line set (CP-SAT, one variable per K-orbit of lines, one parity constraint per K-orbit of points).  Several
random A5 subgroups are tried (PSL(2,q) can have two classes).  usage: py -3 icosa_even.py q [n_A5_tries] [time]"""
import sys, json, time, random, itertools
from ortools.sat.python import cp_model
from symmetric_fast import fast_build
from symmetric_even_sets_gf import setup


def run(q, tries=4, tl=600, seed=1):
    pts, lines = fast_build(q); F, add, mul, inv, neg = setup(q)
    pid = {p: i for i, p in enumerate(pts)}; lid = {L: j for j, L in enumerate(lines)}; sets = [frozenset(L) for L in lines]
    w = lambda u, v: add[add[mul[u[0]][v[2]]][mul[u[1]][v[3]]]][neg[add[mul[u[2]][v[0]]][mul[u[3]][v[1]]]]]
    scal = lambda c, v: tuple(mul[c][x] for x in v)
    vadd = lambda u, v: tuple(add[a][b] for a, b in zip(u, v))
    norm = lambda v: tuple(mul[inv[next(t for t in v if t)]][t] for t in v)
    # a hyperbolic pair: X = line 0, Y = any line disjoint from it
    X = 0; Y = next(j for j in range(len(lines)) if not (sets[j] & sets[X]))
    xs = [pts[p] for p in lines[X]]; Yv = [scal(c, pts[p]) for p in lines[Y] for c in F if c]
    x1, x2 = xs[0], xs[1]
    y1 = next(v for v in Yv if w(x1, v) == 1 and w(x2, v) == 0); y2 = next(v for v in Yv if w(x1, v) == 0 and w(x2, v) == 1)
    coords = lambda v: (w(v, y1), w(v, y2), w(x1, v), w(x2, v))
    fromc = lambda a1, a2, b1, b2: vadd(vadd(scal(a1, x1), scal(a2, x2)), vadd(scal(b1, y1), scal(b2, y2)))
    mm = lambda A, B: tuple(tuple(add[mul[A[i][0]][B[0][j]]][mul[A[i][1]][B[1][j]]] for j in range(2)) for i in range(2))
    det = lambda M: add[mul[M[0][0]][M[1][1]]][neg[mul[M[0][1]][M[1][0]]]]

    def pkey(M):
        flat = [M[0][0], M[0][1], M[1][0], M[1][1]]; s = inv[next(x for x in flat if x)]; return tuple(mul[s][x] for x in flat)

    def closure_size(gens, cap=200):
        I = ((1, 0), (0, 1)); seen = {pkey(I)}; fr = [I]
        while fr and len(seen) <= cap:
            nx_ = []
            for A in fr:
                for g in gens:
                    B = mm(A, g); k = pkey(B)
                    if k not in seen: seen.add(k); nx_.append(B)
            fr = nx_
        return len(seen)

    def porder(M):
        I = pkey(((1, 0), (0, 1))); k, P = 1, M
        while pkey(P) != I and k < 200: P = mm(P, M); k += 1
        return k
    rng = random.Random(seed)
    SL = [((a, b), (c, d)) for a, b, c, d in itertools.product(F, repeat=4) if det(((a, b), (c, d))) == 1]
    o2 = [M for M in SL if porder(M) == 2]; o3 = [M for M in SL if porder(M) == 3]
    found = []
    for _ in range(4000):                                  # A5 = <s, t | s^2 = t^3 = (st)^5 = 1> in PGL
        s, t = rng.choice(o2), rng.choice(o3)
        if porder(mm(s, t)) == 5 and closure_size([s, t]) == 60:
            found.append((s, t))
            if len(found) >= tries: break
    if not found: return dict(q=q, status="no A5 found")
    def mult_order(c):
        k, x = 1, c
        while x != 1: x = mul[x][c]; k += 1
        return k
    prim = next(c for c in F if c and mult_order(c) == q - 1)     # a generator of F_q^*
    results = []
    for s, t in found:
        def elem(M):
            MinvT = None
            d = inv[det(M)]; Mi = ((mul[d][M[1][1]], mul[d][neg[M[0][1]]]), (mul[d][neg[M[1][0]]], mul[d][M[0][0]]))
            MT = ((Mi[0][0], Mi[1][0]), (Mi[0][1], Mi[1][1]))
            def g(p):
                a1, a2, b1, b2 = coords(pts[p])
                na = (add[mul[M[0][0]][a1]][mul[M[0][1]][a2]], add[mul[M[1][0]][a1]][mul[M[1][1]][a2]])
                nb = (add[mul[MT[0][0]][b1]][mul[MT[0][1]][b2]], add[mul[MT[1][0]][b1]][mul[MT[1][1]][b2]])
                return pid[norm(fromc(na[0], na[1], nb[0], nb[1]))]
            return g

        def swap(p):
            a1, a2, b1, b2 = coords(pts[p]); return pid[norm(fromc(neg[b1], neg[b2], a1, a2))]
        gens = [elem(s), elem(t), elem(((prim, 0), (0, prim))), swap]
        pperm = [[g(p) for p in range(len(pts))] for g in gens]
        lperm = [[lid[tuple(sorted(pm[x] for x in L))] for L in lines] for pm in pperm]

        def orbits(perms, n):
            seen = [False] * n; out = []
            for s0 in range(n):
                if seen[s0]: continue
                o = [s0]; seen[s0] = True; i = 0
                while i < len(o):
                    for pm in perms:
                        u = pm[o[i]]
                        if not seen[u]: seen[u] = True; o.append(u)
                    i += 1
                out.append(o)
            return out
        lo, po = orbits(lperm, len(lines)), orbits(pperm, len(pts))
        lorb = {j: i for i, o in enumerate(lo) for j in o}
        through = [[] for _ in pts]
        for j, L in enumerate(lines):
            for p in L: through[p].append(j)
        md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{i}") for i in range(len(lo))]
        for o in po:
            cnt = {}
            for j in through[o[0]]: cnt[lorb[j]] = cnt.get(lorb[j], 0) + 1
            z = md.NewIntVar(0, q + 1, f"z{o[0]}"); md.Add(sum(c * y[i] for i, c in cnt.items()) == 2 * z)
        wt = sum(len(o) * y[i] for i, o in enumerate(lo)); md.Add(wt >= 1); md.Minimize(wt)
        sv = cp_model.CpSolver(); sv.parameters.max_time_in_seconds = tl; sv.parameters.num_workers = 8
        st = sv.Solve(md)
        rec = dict(line_orbits=len(lo), orbit_sizes=sorted(set(len(o) for o in lo)), status=sv.StatusName(st))
        if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            chosen = [j for i, o in enumerate(lo) if sv.Value(y[i]) for j in o]
            cov = [0] * len(pts)
            for j in chosen:
                for p in lines[j]: cov[p] += 1
            rec.update(weight=len(chosen), verified_even=all(c % 2 == 0 for c in cov), coverage=sorted(set(cov)),
                       bound=sv.BestObjectiveBound(), chosen=chosen)
        results.append(rec)
        print(json.dumps({k: v for k, v in rec.items() if k != "chosen"}), flush=True)
    return dict(q=q, results=results)


if __name__ == "__main__":
    q = int(sys.argv[1]); tries = int(sys.argv[2]) if len(sys.argv) > 2 else 4; tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    t0 = time.time(); out = run(q, tries, tl); out["seconds"] = round(time.time() - t0, 1)
    json.dump(out, open(f"icosa_even_q{q}.json", "w"), indent=1)
