"""Pass 7216 -- does the LNS transfer to OTHER generalized quadrangles with published answers?

WHY THIS IS THE RIGHT TEST. Everything so far validates the exact-repair LNS on W(3,q) alone,
where it is measured 6/6 at q=7. That could be a property of the symplectic quadrangle rather
than of the method. Cimrakova-Fack (2005) Table 1 publishes EXHAUSTIVE maxima for two other
classical GQs:

    Q^-(5,4)   (s,t) = (4,16)   325 points   largest maximal partial ovoid 25   (3 up to equiv)
    H(4,4)     (s,t) = (4,8)    165 points   largest maximal partial ovoid 21   (1 up to equiv)

If the method reaches those numbers on geometries it was not tuned for, it transfers. If it
falls short, its W(3,q) results are a local success and should be quoted more narrowly.

THIS REQUIRES GENERAL GF(p^k), which W(3,q) work had not needed beyond GF(9). Implemented here
by finding an irreducible polynomial of degree k over F_p by search and representing elements
as base-p digit vectors packed into ints. That also unlocks q = 25 and 27 for the
arithmetic-conditionality question, which is a separate pass.

Q^-(5,q) is the elliptic quadric in PG(5,q): the quadric
    x0*x1 + x2*x3 + f(x4,x5) = 0
with f an irreducible binary quadratic form, giving a GQ of order (q, q^2) with
(q+1)(q^3+1) points. A partial ovoid is again a set of pairwise non-collinear points, where
collinearity is orthogonality with respect to the associated bilinear form.

    py -3 analysis/w33_pass7216_general_field_and_other_gqs.py [--q 4]
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


class GF:
    """GF(p^k) with elements 0..q-1 encoding base-p coefficient vectors."""

    def __init__(self, q: int):
        p, k = None, None
        for pp in range(2, q + 1):
            if q % pp == 0:
                e, t = 0, q
                while t % pp == 0:
                    t //= pp
                    e += 1
                if t == 1:
                    p, k = pp, e
                break
        if p is None:
            raise ValueError(f"{q} is not a prime power")
        self.q, self.p, self.k = q, p, k
        if k == 1:
            self.add = [[(a + b) % p for b in range(p)] for a in range(p)]
            self.mul = [[(a * b) % p for b in range(p)] for a in range(p)]
        else:
            poly = self._irreducible(p, k)
            self.poly = poly

            def tovec(x):
                v = []
                for _ in range(k):
                    v.append(x % p)
                    x //= p
                return v

            def toint(v):
                x = 0
                for i in reversed(range(k)):
                    x = x * p + v[i]
                return x

            def pmul(a, b):
                A, B = tovec(a), tovec(b)
                C = [0] * (2 * k - 1)
                for i in range(k):
                    for j in range(k):
                        C[i + j] = (C[i + j] + A[i] * B[j]) % p
                for d in range(2 * k - 2, k - 1, -1):
                    c = C[d]
                    if c:
                        C[d] = 0
                        for i in range(k):
                            C[d - k + i] = (C[d - k + i] - c * poly[i]) % p
                return toint(C[:k])

            self.add = [[toint([(x + y) % p for x, y in zip(tovec(a), tovec(b))])
                         for b in range(q)] for a in range(q)]
            self.mul = [[pmul(a, b) for b in range(q)] for a in range(q)]
        self.neg = [next(b for b in range(q) if self.add[a][b] == 0) for a in range(q)]
        self.inv = {}
        for a in range(1, q):
            for b in range(1, q):
                if self.mul[a][b] == 1:
                    self.inv[a] = b
                    break
        assert len(self.inv) == q - 1, f"GF({q}) construction failed"

    @staticmethod
    def _irreducible(p, k):
        """monic x^k = sum poly[i] x^i; return poly (length k) with x^k - poly irreducible."""
        for cand in itertools.product(range(p), repeat=k):
            poly = list(cand)

            def red(C):
                for d in range(len(C) - 1, k - 1, -1):
                    c = C[d]
                    if c:
                        C[d] = 0
                        for i in range(k):
                            C[d - k + i] = (C[d - k + i] - c * poly[i]) % p
                return C[:k]

            # x^(p^k) == x  and  gcd-free: test by checking no root-based factor for k<=3
            ok = True
            if k == 2:
                ok = all((r * r - sum(poly[i] * (r ** i) for i in range(k))) % p != 0
                         for r in range(p))
            elif k == 3:
                ok = all((r ** 3 - sum(poly[i] * (r ** i) for i in range(k))) % p != 0
                         for r in range(p))
            else:
                ok = all((pow(r, k, p) - sum(poly[i] * pow(r, i, p) for i in range(k))) % p
                         != 0 for r in range(p))
            if ok:
                return poly
        raise RuntimeError(f"no irreducible found for GF({p}^{k})")

    def dot(self, xs, ys):
        t = 0
        for x, y in zip(xs, ys):
            t = self.add[t][self.mul[x][y]]
        return t


def elliptic_quadric(F: GF):
    """Q^-(5,q): points of PG(5,q) on x0x1 + x2x3 + f(x4,x5) = 0, f irreducible."""
    q = F.q
    # irreducible binary quadratic a*x^2 + b*x*y + c*y^2 over GF(q)
    fq = None
    for a in range(1, q):
        for b in range(q):
            for c in range(1, q):
                bad = any(F.add[F.add[F.mul[a][F.mul[t][t]]][F.mul[b][t]]][c] == 0
                          for t in range(q))
                if not bad:
                    fq = (a, b, c)
                    break
            if fq:
                break
        if fq:
            break
    assert fq, "no irreducible binary quadratic form found"
    a, b, c = fq

    def Qform(v):
        t = F.add[F.mul[v[0]][v[1]]][F.mul[v[2]][v[3]]]
        u = F.add[F.add[F.mul[a][F.mul[v[4]][v[4]]]][F.mul[b][F.mul[v[4]][v[5]]]]][
            F.mul[c][F.mul[v[5]][v[5]]]]
        return F.add[t][u]

    def Bil(u, v):
        s = 0
        for x, y in ((0, 1), (1, 0), (2, 3), (3, 2)):
            s = F.add[s][F.mul[u[x]][v[y]]]
        s = F.add[s][F.mul[F.add[a][a]][F.mul[u[4]][v[4]]]]
        s = F.add[s][F.mul[b][F.add[F.mul[u[4]][v[5]]][F.mul[u[5]][v[4]]]]]
        s = F.add[s][F.mul[F.add[c][c]][F.mul[u[5]][v[5]]]]
        return s

    pts = []
    for v in itertools.product(range(q), repeat=6):
        if not any(v):
            continue
        lead = next(x for x in v if x)
        iv = F.inv[lead]
        w = tuple(F.mul[x][iv] for x in v)
        if w == v and Qform(v) == 0:
            pts.append(v)
    return sorted(set(pts)), Bil


def lns(P, adj, budget, rng, target=None):
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    n = len(P)
    nbr = [0] * n
    for i in range(n):
        m = 0
        for j in adj[i]:
            m |= 1 << j
        nbr[i] = m

    def repair(c):
        m = len(c)
        if m == 0:
            return []
        pos = {p: i for i, p in enumerate(c)}
        r, cc, v, e = [], [], [], 0
        for i, p in enumerate(c):
            for qq in adj[p]:
                j = pos.get(qq)
                if j is not None and j > i:
                    r += [e, e]
                    cc += [i, j]
                    v += [1.0, 1.0]
                    e += 1
        if e == 0:
            return list(c)
        A = coo_matrix((v, (r, cc)), shape=(e, m))
        res = milp(c=-np.ones(m), constraints=LinearConstraint(A, -np.inf, 1),
                   integrality=np.ones(m), bounds=Bounds(0, 1),
                   options={"mip_rel_gap": 0.0, "time_limit": 10.0, "presolve": True})
        return [] if res.x is None else [c[i] for i in range(m) if res.x[i] > 0.5]

    best = []
    for _ in range(200):
        S, banned = [], 0
        order = list(range(n))
        rng.shuffle(order)
        for p in order:
            if not (banned >> p) & 1:
                S.append(p)
                banned |= nbr[p] | (1 << p)
        if len(S) > len(best):
            best = S
    cur, t0, it = list(best), time.time(), 0
    while time.time() - t0 < budget:
        it += 1
        k = rng.randint(4, max(5, min(16, len(cur) - 2)))
        keep = list(cur)
        rng.shuffle(keep)
        keep = keep[:len(keep) - k]
        blocked = 0
        for p in keep:
            blocked |= nbr[p] | (1 << p)
        new = keep + repair([p for p in range(n) if not (blocked >> p) & 1])
        if len(new) >= len(cur):
            cur = new
        if len(cur) > len(best):
            best = list(cur)
            if target and len(best) >= target:
                break
        if it % 50 == 0:
            cur = list(best)
    return best, it


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=4)
    ap.add_argument("--budget", type=float, default=300.0)
    args = ap.parse_args()

    print("=" * 78)
    print(f"Pass 7216 -- Q^-(5,{args.q}) with general GF(p^k), against published maxima")
    print("=" * 78)

    for q in (2, 3, args.q) if args.q not in (2, 3) else (2, 3):
        F = GF(q)
        print(f"\n  GF({q}) = GF({F.p}^{F.k}) built, {len(F.inv)} units", flush=True)
        P, Bil = elliptic_quadric(F)
        n = len(P)
        expect = (q + 1) * (q ** 3 + 1)
        print(f"  Q^-(5,{q}): {n} points   expect (q+1)(q^3+1) = {expect}   "
              f"{'OK' if n == expect else 'MISMATCH -- aborting this q'}", flush=True)
        if n != expect:
            continue
        adj = [set() for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if Bil(P[i], P[j]) == 0:
                    adj[i].add(j)
                    adj[j].add(i)
        print(f"    collinearity degree {len(adj[0])}   "
              f"(GQ(q,q^2) expects q(q^2+1) = {q * (q * q + 1)})", flush=True)
        rng = random.Random(7216 + q)
        best, it = lns(P, adj, args.budget, rng)
        bad = [(a, b) for a, b in itertools.combinations(best, 2) if Bil(P[a], P[b]) == 0]
        pub = {4: 25}.get(q)
        print(f"    LNS best partial ovoid: {len(best)}  ({it} iterations, "
              f"{len(bad)} violations)")
        if pub:
            print(f"    published exhaustive maximum (Cimrakova-Fack Table 1): {pub}   "
                  f"-> {'REACHES' if len(best) >= pub else f'falls {pub - len(best)} short'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
