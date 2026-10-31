"""12482: minimal even line sets of W(3,q) over any finite field GF(q) (12467/12474 used arithmetic mod q, so prime q only).
Same MILP as even_line_sets.py (N y = 2 z, y_0 = 1, optional sym2 break of 12474) but the polar space is built over GF(p^k) and the
chosen lines are saved, so the structure of the optimum can be inspected.  Sanity: (q+1)(q^2+1) lines, every point on q+1 lines, every
line totally isotropic.  usage: py -3 even_line_sets_gf.py q [time] [sym2]"""
import sys, json, time, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

IRRED = {4: (2, [1, 1]), 8: (2, [1, 1, 0]), 9: (3, [2, 0]), 16: (2, [1, 1, 0, 0]), 25: (5, [2, 0]), 27: (3, [1, 1, 0]), 49: (7, [3, 0])}
# (p, c) means x^k = c_0 + c_1 x + ... (coefficients of the reduction); x^2 = x + 1 (F4), x^3 = x + 1 (F8), x^2 = -1 (F9),
# x^4 = x + 1 (F16), x^2 = 2 (F25: 2 is a non-square mod 5).


def field(q):
    if q not in IRRED:                                   # prime field
        return list(range(q)), [[(a + b) % q for b in range(q)] for a in range(q)], [[a * b % q for b in range(q)] for a in range(q)]
    p, red = IRRED[q]; k = len(red)
    els = [tuple(reversed(e)) for e in itertools.product(range(p), repeat=k)]  # low degree first; index 1 is the constant 1
    idx = {e: i for i, e in enumerate(els)}

    def mul(a, b):
        prod = [0] * (2 * k - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                prod[i + j] = (prod[i + j] + x * y) % p
        for d in range(2 * k - 2, k - 1, -1):            # x^d = x^(d-k) * x^k
            c = prod[d]; prod[d] = 0
            for i, r in enumerate(red):
                prod[d - k + i] = (prod[d - k + i] + c * r) % p
        return tuple(prod[:k])
    add = [[idx[tuple((x + y) % p for x, y in zip(a, b))] for b in els] for a in els]
    mt = [[idx[mul(a, b)] for b in els] for a in els]
    return list(range(q)), add, mt


def build(q):
    F, add, mul = field(q)
    one = next(a for a in F if all(mul[a][b] == b for b in F))
    assert one == 1 and all(sum(1 for b in F if mul[a][b] == one) == 1 for a in F if a), "not a field"
    inv = {a: next(b for b in F if mul[a][b] == one) for a in F if a}
    neg = {a: next(b for b in F if add[a][b] == 0) for a in F}
    pts = []
    for v in itertools.product(F, repeat=4):
        if any(v):
            f = next(x for x in v if x)
            if f == one: pts.append(v)
    pid = {v: i for i, v in enumerate(pts)}

    def norm(v):
        f = next(x for x in v if x); s = inv[f]
        return tuple(mul[s][x] for x in v)

    def omega(u, v):                                     # u0 v2 + u1 v3 - u2 v0 - u3 v1
        s = 0
        for a, b, sg in ((0, 2, 1), (1, 3, 1), (2, 0, -1), (3, 1, -1)):
            t = mul[u[a]][v[b]]
            s = add[s][t if sg > 0 else neg[t]]
        return s
    lines = set()
    for i, u in enumerate(pts):
        for j in range(i + 1, len(pts)):
            v = pts[j]
            if omega(u, v) == 0:
                L = {i, j}
                for t in F:
                    if t:
                        L.add(pid[norm(tuple(add[u[c]][mul[t][v[c]]] for c in range(4)))])
                lines.add(tuple(sorted(L)))
    lines = sorted(lines)
    n, m = len(pts), len(lines)
    assert m == (q + 1) * (q * q + 1) and n == m and all(len(L) == q + 1 for L in lines)
    N = np.zeros((n, m), dtype=int)
    for j, L in enumerate(lines): N[list(L), j] = 1
    assert (N.sum(1) == q + 1).all()
    assert all(omega(pts[a], pts[b]) == 0 for L in lines[:50] for a in L for b in L)
    return pts, lines, N


def solve(q, tl, sym2):
    pts, lines, N = build(q); n, m = N.shape
    c = np.concatenate([np.ones(m), np.zeros(n)])
    M = np.vstack([np.hstack([N, -2 * np.eye(n)]), np.concatenate([np.ones(m), np.zeros(n)])[None, :]])
    lo = np.concatenate([np.zeros(n), [1]]); hi = np.concatenate([np.zeros(n), [np.inf]])
    lb = np.zeros(m + n); ub = np.concatenate([np.ones(m), np.full(n, (q + 1) // 2)]); lb[0] = 1
    if sym2:
        meet = [j for j in range(1, m) if set(lines[j]) & set(lines[0])]
        lb[meet[0]] = 1
    t0 = time.time()
    r = milp(c, constraints=LinearConstraint(M, lo, hi), integrality=np.ones(m + n), bounds=Bounds(lb, ub), options=dict(time_limit=tl))
    rec = dict(q=q, lines=m, sym2=sym2, optimal=bool(r.status == 0), seconds=round(time.time() - t0, 1), status=r.message,
               dual_bound=getattr(r, "mip_dual_bound", None))
    if r.x is not None:
        y = np.round(r.x[:m]).astype(int); cov = N @ y
        rec.update(min_even_line_set=int(y.sum()), verified_even=bool(not (cov % 2).any()),
                   coverage_profile=sorted(set(int(v) for v in cov)), points_covered=int((cov > 0).sum()),
                   chosen_lines=[[list(pts[p]) for p in lines[j]] for j in np.flatnonzero(y)])
    return rec


if __name__ == "__main__":
    q = int(sys.argv[1]); tl = float(sys.argv[2]) if len(sys.argv) > 2 else 1800; sym2 = len(sys.argv) > 3 and sys.argv[3] == "sym2"
    rec = solve(q, tl, sym2)
    print(json.dumps({k: v for k, v in rec.items() if k != "chosen_lines"}), flush=True)
    json.dump(rec, open(f"even_line_sets_gf_q{q}" + ("_sym2" if sym2 else "") + ".json", "w"), indent=1)
