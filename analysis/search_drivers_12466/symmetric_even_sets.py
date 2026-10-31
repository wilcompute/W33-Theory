"""12486: smallest even line sets of W(3,q) INVARIANT under a cyclic symmetry g = A (+) B (A of order r in SL(2,q) on <e0,e2>,
B = A^k on <e1,e3>, the form w = x0y2 + x1y3 - x2y0 - x3y1).  One CP-SAT variable per g-orbit of lines, one parity constraint per
g-orbit of points; minimise the total weight (or test one weight).  Any feasible set is an UPPER bound on the minimum at that q.
Motivation (12485): a Moore (Hoffman-Singleton) even set at q = 13 would have 100 = 2 + 7*14 lines, and an order-7 automorphism of
the Hoffman-Singleton graph fixes exactly one vertex (= one twin pair of lines).
usage: py -3 symmetric_even_sets.py q r [time] [weight]"""
import sys, json, time, itertools
from ortools.sat.python import cp_model
from even_line_sets_gf import build


def order(M, q):
    """Exact multiplicative order of a 2x2 matrix over GF(q) (an earlier loop accepted order 3 as order 2)."""
    P, k = M, 1
    while P != ((1, 0), (0, 1)):
        P = tuple(tuple(sum(P[i][t] * M[t][j] for t in range(2)) % q for j in range(2)) for i in range(2)); k += 1
    return k


def sl2_order(q, r):
    """An element of SL(2,q) of exact order r (searched by trace)."""
    for a, b, c in itertools.product(range(q), repeat=3):
        if a == 0:
            continue
        d = (1 + b * c) * pow(a, -1, q) % q              # det = ad - bc = 1
        M = ((a, b), (c, d))
        if order(M, q) == r:
            return M
    raise ValueError("no element of that order")


def mpow(M, k, q):
    R = ((1, 0), (0, 1))
    for _ in range(k):
        R = tuple(tuple(sum(R[i][t] * M[t][j] for t in range(2)) % q for j in range(2)) for i in range(2))
    return R


def run(q, r, k, tl, weight=None, pre=None):
    pts, lines, N = pre or build(q)
    pid = {p: i for i, p in enumerate(pts)}
    A = sl2_order(q, r); B = mpow(A, k, q)

    def act(v):                                          # A on coordinates (0,2), B on (1,3)
        w = [0] * 4
        w[0] = (A[0][0] * v[0] + A[0][1] * v[2]) % q; w[2] = (A[1][0] * v[0] + A[1][1] * v[2]) % q
        w[1] = (B[0][0] * v[1] + B[0][1] * v[3]) % q; w[3] = (B[1][0] * v[1] + B[1][1] * v[3]) % q
        f = next(x for x in w if x); s = pow(f, -1, q)
        return pid[tuple(x * s % q for x in w)]
    perm = [act(p) for p in pts]
    lid = {frozenset(l): j for j, l in enumerate(lines)}
    lperm = [lid[frozenset(perm[x] for x in l)] for l in lines]      # KeyError here would mean g is not symplectic
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
        p = o[0]
        cnt = {}
        for j in range(len(lines)):
            if N[p, j]: cnt[lorb[j]] = cnt.get(lorb[j], 0) + 1
        z = md.NewIntVar(0, q + 1, f"z{p}")
        md.Add(sum(c * y[i] for i, c in cnt.items()) == 2 * z)
    wt = sum(len(o) * y[i] for i, o in enumerate(lo))
    md.Add(wt >= 1)
    if weight: md.Add(wt == weight)
    else: md.Minimize(wt)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = 8
    t0 = time.time(); st = s.Solve(md)
    rec = dict(q=q, r=r, k=k, line_orbits=len(lo), orbit_sizes=sorted(set(len(o) for o in lo)), status=s.StatusName(st),
               seconds=round(time.time() - t0, 1), target_weight=weight)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        chosen = [j for i, o in enumerate(lo) if s.Value(y[i]) for j in o]
        cov = N[:, chosen].sum(1)
        rec.update(weight=len(chosen), verified_even=bool(not (cov % 2).any()), coverage_profile=sorted(set(int(c) for c in cov)),
                   bound=s.BestObjectiveBound() if not weight else None, chosen=chosen)
    return rec


if __name__ == "__main__":
    q, r = int(sys.argv[1]), int(sys.argv[2]); tl = float(sys.argv[3]) if len(sys.argv) > 3 else 600
    weight = int(sys.argv[4]) if len(sys.argv) > 4 else None
    pre = build(q); out = []
    for k in range(0, r // 2 + 1):
        rec = run(q, r, k, tl, weight, pre)
        print(json.dumps({x: v for x, v in rec.items() if x != "chosen"}), flush=True)
        out.append(rec)
    json.dump(out, open(f"symmetric_q{q}_r{r}" + (f"_w{weight}" if weight else "") + ".json", "w"), indent=1)
