"""12496: symmetric_even_sets.py over any GF(q) (prime powers too): smallest even line sets of W(3,q) invariant under
g = A (+) A^k, A of order r in SL(2,q), one CP-SAT variable per g-orbit of lines.  Field tables from even_line_sets_gf.field; points
are tuples of field-element indices exactly as build(q) makes them.  usage: py -3 symmetric_even_sets_gf.py q r [time] [k]"""
import sys, json, time, itertools
from ortools.sat.python import cp_model
from even_line_sets_gf import build, field


def setup(q):
    F, add, mul = field(q)
    inv = {a: next(b for b in F if mul[a][b] == 1) for a in F if a}
    neg = {a: next(b for b in F if add[a][b] == 0) for a in F}
    return F, add, mul, inv, neg


def matmul(X, Y, add, mul):
    return tuple(tuple(add[mul[X[i][0]][Y[0][j]]][mul[X[i][1]][Y[1][j]]] for j in range(2)) for i in range(2))


def order(M, add, mul):
    I = ((1, 0), (0, 1)); P, k = M, 1
    while P != I:
        P = matmul(P, M, add, mul); k += 1
    return k


def sl2_of_order(q, r, F, add, mul, inv, neg):
    for a, b, c in itertools.product(F, repeat=3):
        if a == 0: continue
        d = mul[add[1][mul[b][c]]][inv[a]]                # ad - bc = 1
        M = ((a, b), (c, d))
        if order(M, add, mul) == r: return M
    raise ValueError("no element of that order")


def run(q, r, k, tl, pre=None):
    pts, lines, N = pre or build(q)
    F, add, mul, inv, neg = setup(q)
    pid = {p: i for i, p in enumerate(pts)}
    A = sl2_of_order(q, r, F, add, mul, inv, neg); B = ((1, 0), (0, 1))
    for _ in range(k): B = matmul(B, A, add, mul)

    def lin(M, x, y):
        return (add[mul[M[0][0]][x]][mul[M[0][1]][y]], add[mul[M[1][0]][x]][mul[M[1][1]][y]])

    def act(v):
        w0, w2 = lin(A, v[0], v[2]); w1, w3 = lin(B, v[1], v[3])
        w = (w0, w1, w2, w3)
        f = next(x for x in w if x); s = inv[f]
        return pid[tuple(mul[s][x] for x in w)]
    perm = [act(p) for p in pts]
    lid = {frozenset(l): j for j, l in enumerate(lines)}
    lperm = [lid[frozenset(perm[x] for x in l)] for l in lines]

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
    md = cp_model.CpModel(); y = [md.NewBoolVar(f"y{i}") for i in range(len(lo))]
    for o in po:
        p = o[0]; cnt = {}
        for j in range(len(lines)):
            if N[p, j]: cnt[lorb[j]] = cnt.get(lorb[j], 0) + 1
        z = md.NewIntVar(0, q + 1, f"z{p}")
        md.Add(sum(c * y[i] for i, c in cnt.items()) == 2 * z)
    wt = sum(len(o) * y[i] for i, o in enumerate(lo))
    md.Add(wt >= 1); md.Minimize(wt)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
    t0 = time.time(); st = s.Solve(md)
    rec = dict(q=q, r=r, k=k, line_orbits=len(lo), status=s.StatusName(st), seconds=round(time.time() - t0, 1))
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [j for i, o in enumerate(lo) if s.Value(y[i]) for j in o]
        cov = N[:, chosen].sum(1)
        rec.update(weight=len(chosen), verified_even=bool(not (cov % 2).any()), coverage_profile=sorted(set(int(c) for c in cov)),
                   bound=s.BestObjectiveBound(), chosen=chosen)
    return rec


if __name__ == "__main__":
    q, r = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    ks = [int(sys.argv[4])] if len(sys.argv) > 4 else list(range(0, r // 2 + 1))
    pre = build(q); out = []
    for k in ks:
        rec = run(q, r, k, tl, pre)
        print(json.dumps({x: v for x, v in rec.items() if x != "chosen"}), flush=True); out.append(rec)
    json.dump(out, open(f"symmetric_gf_q{q}_r{r}.json", "w"), indent=1)
