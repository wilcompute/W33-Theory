"""Pass 12655: symmetric codes for the Shannon capacity of the W(3,3) collinearity graph G.  Search for independent sets of
G strong-product G invariant under a cyclic group <(g, h)> acting on V x V (g, h automorphisms of G of the same order, including
h = g^a 'twists' and the diagonal h = g), optionally together with the coordinate swap.  The orbit quotient shrinks the 1600-variable
model, so CP-SAT can close it or go deeper than the unstructured run (58, Pass 12654).  Every set found is re-verified pair by pair.
Control: the same code on C5 with the rotation group must return 5.  usage: py -3 analysis/w33_shannon_symmetric_codes.py [sec_per_group] [workers]"""
import itertools, json, os, sys, time
import numpy as np
from ortools.sat.python import cp_model
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
tl = float(sys.argv[1]) if len(sys.argv) > 1 else 120; wk = int(sys.argv[2]) if len(sys.argv) > 2 else 4


def solve_orbits(n, adj, orbits, tl, wk):
    """orbits: list of lists of (u, v).  Keep internally independent orbits; conflict graph between orbits; maximise total size."""
    close = lambda a, b: a == b or adj[a][b]
    conf = lambda x, y: close(x[0], y[0]) and close(x[1], y[1])
    good = [o for o in orbits if not any(conf(x, y) for x, y in itertools.combinations(o, 2))]
    m = cp_model.CpModel(); xs = [m.NewBoolVar(f"o{i}") for i in range(len(good))]
    for i, j in itertools.combinations(range(len(good)), 2):
        if any(conf(x, y) for x in good[i] for y in good[j]): m.AddBoolOr([xs[i].Not(), xs[j].Not()])
    m.Maximize(sum(len(o) * x for o, x in zip(good, xs)))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = wk
    st = s.Solve(m)
    S = [p for o, x in zip(good, xs) if s.Value(x) for p in o]
    assert not any(conf(x, y) for x, y in itertools.combinations(S, 2))
    return len(S), int(s.BestObjectiveBound()), s.StatusName(st), S, len(good)


def orbits_of(n, gens):
    seen = set(); out = []
    for p in itertools.product(range(n), repeat=2):
        if p in seen: continue
        orb = {p}; fr = [p]
        while fr:
            nx_ = []
            for q in fr:
                for f in gens:
                    r = f(q)
                    if r not in orb: orb.add(r); nx_.append(r)
            fr = nx_
        seen |= orb; out.append(sorted(orb))
    return out


# control C5
c5 = [[int((i - j) % 5 in (1, 4)) for j in range(5)] for i in range(5)]
ctrl = max(solve_orbits(5, c5, orbits_of(5, [lambda q, a=a: ((q[0] + 1) % 5, (q[1] + a) % 5)]), 20, 1)[0] for a in (1, 2, 3, 4))
print("control C5 (rotation-invariant codes):", ctrl, flush=True); assert ctrl == 5
# W(3,3)
pts = sorted({min(tuple((c * x) % 3 for x in v) for c in (1, 2)) for v in itertools.product(range(3), repeat=4) if any(v)})
pid = {p: i for i, p in enumerate(pts)}
J = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]])
om = lambda u, v: int(np.array(u) @ J @ np.array(v)) % 3
adj = [[int(i != j and om(pts[i], pts[j]) == 0) for j in range(40)] for i in range(40)]
norm = lambda v: min(tuple((c * x) % 3 for x in v) for c in (1, 2))
rng = np.random.default_rng(7)


def transvection(a, c):
    return lambda v: tuple((np.array(v) + c * om(v, a) * np.array(a)) % 3)


def random_element(k=8):
    fs = [transvection(pts[int(rng.integers(40))], int(rng.integers(1, 3))) for _ in range(k)]
    perm = []
    for p in pts:
        v = p
        for f in fs: v = f(v)
        perm.append(pid[norm(v)])
    assert sorted(perm) == list(range(40))
    return tuple(perm)


def order(p):
    q = p; k = 1
    while q != tuple(range(40)): q = tuple(p[i] for i in q); k += 1
    return k


def power(p, a):
    q = tuple(range(40))
    for _ in range(a): q = tuple(p[i] for i in q)
    return q


elems = {}
for _ in range(400):
    p = random_element(); o = order(p)
    fixed = sum(1 for i in range(40) if p[i] == i)
    elems.setdefault((o, fixed), p)
print("element classes (order, fixed points):", sorted(elems), flush=True)
results = []; best = (0, None); t0 = time.time()
for (o, fx), gperm in sorted(elems.items()):
    if o == 1: continue
    for a in sorted({a for a in range(1, o) if np.gcd(a, o) == 1}):
        h = power(gperm, a)
        for swap in (False, True):
            gens = [lambda q, gperm=gperm, h=h: (gperm[q[0]], h[q[1]])]
            if swap:
                if a != 1 and (a * a) % o != 1: continue  # swap normalises <(g, g^a)> only if a^2 = 1
                gens.append(lambda q: (q[1], q[0]))
            orbs = orbits_of(40, gens)
            size, bd, st, S, ngood = solve_orbits(40, adj, orbs, tl, wk)
            rec = dict(order=o, fixed=fx, twist=a, swap=swap, n_orbits=len(orbs), usable_orbits=ngood, size=size, bound=bd, status=st)
            results.append(rec); print(rec, round(time.time() - t0), "s", flush=True)
            if size > best[0]: best = (size, S, rec)
            json.dump(dict(control_C5=ctrl, results=results, best_size=best[0], best_record=best[2], best_set=best[1], Theta_lower=best[0] ** 0.5),
                      open(os.path.join(ROOT, "data", "w33_shannon_symmetric_codes.json"), "w"), indent=1, default=int)
print("BEST", best[0], best[2], flush=True)
