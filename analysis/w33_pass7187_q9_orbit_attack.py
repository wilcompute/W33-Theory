"""Pass 7187 -- the q=9 partial ovoid by SYMMETRY, after brute force failed.

WHY THIS AND NOT MORE SEARCH. A feasibility ILP for a 52-point partial ovoid in W(3,9)
ran 3000s over 257,727 nodes and returned primal bound `inf` -- it found nothing and proved
nothing. The 820-point graph is simply too big for an unstructured search.

THE ARGUMENT FOR SYMMETRY. Cimrakova-Fack (2005) report that the largest partial ovoid of
W(3,7), of size 33, is UNIQUE up to equivalence (their Table 1, #O' = 1). A unique extremal
object has a large stabilizer. So the extremal objects in this family are symmetric, and the
right search space is H-invariant point sets for subgroups H <= Sp(4,q) -- which collapses
820 binary variables to one variable per H-orbit, typically a few dozen.

This is a restriction: if a maximum partial ovoid has trivial stabilizer, this cannot find
it. It is a search for EXISTENCE, so a hit is a theorem and a miss is not.

CALIBRATION FIRST. The same sweep is run at q=3, 5, 7 where the answers are known (7, 18,
33). If symmetric search cannot reach the known optimum at q=5 and q=7, its silence at q=9
means nothing, and the script says so.

GF(9) = F_3[x]/(x^2+1), NOT Z/9.

    py -3 analysis/w33_pass7187_q9_orbit_attack.py [--q 9] [--trials 400]
"""

from __future__ import annotations

import argparse
import itertools
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ------------------------------------------------------------------ fields --
class Field:
    """GF(q) for q in {3,5,7} (prime) and q=9 = F_3[x]/(x^2+1)."""

    def __init__(self, q: int):
        self.q = q
        if q == 9:
            self.add = [[0] * 9 for _ in range(9)]
            self.mul = [[0] * 9 for _ in range(9)]
            for k in range(9):
                for m in range(9):
                    a, b = k % 3, k // 3
                    c, d = m % 3, m // 3
                    self.add[k][m] = ((a + c) % 3) + 3 * ((b + d) % 3)
                    self.mul[k][m] = ((a * c - b * d) % 3) + 3 * ((a * d + b * c) % 3)
            self.neg = [(-(k % 3)) % 3 + 3 * ((-(k // 3)) % 3) for k in range(9)]
        else:
            self.add = [[(k + m) % q for m in range(q)] for k in range(q)]
            self.mul = [[(k * m) % q for m in range(q)] for k in range(q)]
            self.neg = [(-k) % q for k in range(q)]
        self.inv = {}
        for k in range(1, q):
            for m in range(1, q):
                if self.mul[k][m] == 1:
                    self.inv[k] = m
                    break
        assert len(self.inv) == q - 1, f"GF({q}) built wrong"
        if q == 9:
            assert self.mul[3][3] == 2, "i^2 must be -1 = 2; Z/9 would give 0"

    def dot(self, xs, ys):
        t = 0
        for x, y in zip(xs, ys):
            t = self.add[t][self.mul[x][y]]
        return t


def geometry(F: Field):
    """Projective points of PG(3,q) and the collinearity relation of W(3,q)."""
    q = F.q
    P = []
    for v in itertools.product(range(q), repeat=4):
        if not any(v):
            continue
        lead = next(c for c in v if c)
        iv = F.inv[lead]
        P.append(tuple(F.mul[c][iv] for c in v))
    P = sorted(set(P))

    def B(u, v):
        a = F.add[F.mul[u[0]][v[1]]][F.neg[F.mul[u[1]][v[0]]]]
        b = F.add[F.mul[u[2]][v[3]]][F.neg[F.mul[u[3]][v[2]]]]
        return F.add[a][b]

    n = len(P)
    idx = {p: i for i, p in enumerate(P)}
    adj = [set() for _ in range(n)]
    for i in range(n):
        Pi = P[i]
        for j in range(i + 1, n):
            if B(Pi, P[j]) == 0:
                adj[i].add(j)
                adj[j].add(i)
    return P, idx, adj, B


# ------------------------------------------------------- symplectic group --
def transvection(F: Field, v, lam):
    """t(x) = x + lam*B(x,v)*v -- a symplectic transvection. These generate Sp(4,q)."""
    q = F.q

    def B(u, w):
        a = F.add[F.mul[u[0]][w[1]]][F.neg[F.mul[u[1]][w[0]]]]
        b = F.add[F.mul[u[2]][w[3]]][F.neg[F.mul[u[3]][w[2]]]]
        return F.add[a][b]

    M = []
    for e in range(4):
        x = tuple(1 if k == e else 0 for k in range(4))
        c = F.mul[lam][B(x, v)]
        M.append(tuple(F.add[x[k]][F.mul[c][v[k]]] for k in range(4)))
    # rows of M are images of basis vectors; act on the right
    return tuple(tuple(col) for col in zip(*M))


def matmul(F, A, Bm):
    return tuple(tuple(F.dot(A[i], [Bm[k][j] for k in range(4)]) for j in range(4))
                 for i in range(4))


def apply(F, M, p):
    img = tuple(F.dot(M[i], p) for i in range(4))
    lead = next((c for c in img if c), None)
    if lead is None:
        return None
    iv = F.inv[lead]
    return tuple(F.mul[c][iv] for c in img)


IDENT = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))


def order_of(F, M, cap=200):
    X, k = M, 1
    while X != IDENT and k <= cap:
        X = matmul(F, X, M)
        k += 1
    return k if X == IDENT else None


def closure(F, gens, cap=600):
    """Subgroup generated by gens, abandoned above `cap` elements."""
    seen = {IDENT}
    frontier = [IDENT]
    while frontier:
        nxt = []
        for X in frontier:
            for g in gens:
                Y = matmul(F, X, g)
                if Y not in seen:
                    seen.add(Y)
                    if len(seen) > cap:
                        return None
                    nxt.append(Y)
        frontier = nxt
    return seen


def orbits_of(F, H, P, idx):
    n = len(P)
    seen = [False] * n
    orbs = []
    for i in range(n):
        if seen[i]:
            continue
        o = set()
        stack = [i]
        seen[i] = True
        while stack:
            j = stack.pop()
            o.add(j)
            for M in H:
                k = idx[apply(F, M, P[j])]
                if not seen[k]:
                    seen[k] = True
                    stack.append(k)
        orbs.append(sorted(o))
    return orbs


# --------------------------------------------------------- orbit max-clique --
def best_invariant_set(orbs, adj):
    """Max-weight set of orbits that is pairwise and internally non-collinear."""
    good = []
    for o in orbs:
        if all(b not in adj[a] for a, b in itertools.combinations(o, 2)):
            good.append(o)
    m = len(good)
    if not m:
        return 0, []
    comp = [[False] * m for _ in range(m)]
    for i in range(m):
        si = set(good[i])
        for j in range(i + 1, m):
            ok = not any(adj[a] & si for a in good[j])
            comp[i][j] = comp[j][i] = ok
    order = sorted(range(m), key=lambda i: -len(good[i]))
    best = [0, []]

    def expand(cur, cand, wt):
        if wt + sum(len(good[i]) for i in cand) <= best[0]:
            return
        if wt > best[0]:
            best[0] = wt
            best[1] = list(cur)
        for pos, i in enumerate(cand):
            expand(cur + [i], [j for j in cand[pos + 1:] if comp[i][j]],
                   wt + len(good[i]))

    expand([], order, 0)
    pts = sorted(p for i in best[1] for p in good[i])
    return best[0], pts


def sweep(q: int, trials: int, cap: int, verbose=True):
    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    if verbose:
        print(f"\n  q={q}: {n} points, degree {len(adj[0])}")
    rng = random.Random(20260821 + q)
    nz = [p for p in P]
    best_overall, best_pts, best_desc = 0, [], ""
    seen_sub = set()
    for t in range(trials):
        k = rng.choice([1, 1, 2])
        gens = []
        for _ in range(k):
            v = rng.choice(nz)
            lam = rng.randrange(1, q)
            g = transvection(F, v, lam)
            # random conjugate-ish power to diversify orders
            for _ in range(rng.randrange(0, 3)):
                v2 = rng.choice(nz)
                g = matmul(F, g, transvection(F, v2, rng.randrange(1, q)))
            gens.append(g)
        H = closure(F, gens, cap=cap)
        if H is None or len(H) < 3:
            continue
        key = frozenset(H)
        if key in seen_sub:
            continue
        seen_sub.add(key)
        orbs = orbits_of(F, H, P, idx)
        w, pts = best_invariant_set(orbs, adj)
        if w > best_overall:
            best_overall, best_pts = w, pts
            best_desc = f"|H|={len(H)}, {len(orbs)} orbits"
            if verbose:
                print(f"    |H|={len(H):4d}  {len(orbs):4d} orbits  ->  "
                      f"invariant partial ovoid of size {w}")
    return best_overall, best_pts, best_desc, P, adj, B, len(seen_sub)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=0, help="0 = calibrate then run q=9")
    ap.add_argument("--trials", type=int, default=400)
    ap.add_argument("--cap", type=int, default=600)
    args = ap.parse_args()

    print("=" * 78)
    print("Pass 7187 -- q=9 partial ovoid by symmetry (brute force already failed)")
    print("=" * 78)

    known = {3: 7, 5: 18, 7: 33}
    qs = [args.q] if args.q else [3, 5, 7, 9]
    results = {}
    for q in qs:
        w, pts, desc, P, adj, B, nsub = sweep(q, args.trials, args.cap)
        bad = [(a, b) for a, b in itertools.combinations(pts, 2) if B(P[a], P[b]) == 0]
        results[q] = (w, desc, nsub, len(bad))
        tag = ""
        if q in known:
            tag = (f"   known optimum {known[q]}  -> symmetric search "
                   f"{'REACHES it' if w >= known[q] else f'falls {known[q]-w} short'}")
        print(f"    best over {nsub} distinct subgroups: {w}{tag}")
        if bad:
            print(f"    !! {len(bad)} collinear pairs -- INVALID, discarding")
            continue
        if q == 9 and w >= 52:
            import json
            out = ROOT / "data" / f"PART_W33_Q9_PARTIAL_OVOID_{w}.json"
            out.write_text(json.dumps(
                {"q": 9, "size": w, "subgroup": desc,
                 "points": [list(P[i]) for i in pts],
                 "encoding": "GF(9) k = (k%3) + (k//3)*i, i^2 = -1",
                 "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2"},
                indent=2), encoding="utf-8")
            print(f"    *** wrote {out.relative_to(ROOT).as_posix()} ***")

    print("\n  CALIBRATION IS THE POINT OF THE q=3,5,7 ROWS.")
    ok = all(results[q][0] >= known[q] for q in (3, 5, 7) if q in results)
    if ok:
        print("  Symmetric search reaches every known optimum, so its q=9 answer is")
        print("  informative.")
    else:
        short = [q for q in (3, 5, 7) if q in results and results[q][0] < known[q]]
        print(f"  Symmetric search FAILS to reach the known optimum at q={short}.")
        print("  Therefore its q=9 number is a LOWER BOUND ONLY and its failure to reach")
        print("  52 is NOT evidence that 52 does not exist. Stated because it is the")
        print("  difference between a result and a wasted run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
