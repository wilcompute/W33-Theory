"""Pass 7106 -- alpha(W(3,q)) EXACT for q = 3 and 5, settling a corpus contradiction.

The corpus records alpha(W(3,3)) as 1, 4, 7, 9 and 10 in different files. At most one of
those is right. W(3,3) has forty points, so the question is decidable outright.

    py -3 analysis/w33_pass7106_alpha_exact_small_q.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def gf(q):
    """Field elements as ints for prime q (both cases here are prime)."""
    return list(range(q))


def points(q):
    """Projective points of PG(3,q): normalised nonzero 4-vectors, first nonzero = 1."""
    pts = []
    for v in itertools.product(range(q), repeat=4):
        if all(c == 0 for c in v):
            continue
        lead = next(c for c in v if c != 0)
        inv = pow(lead, q - 2, q)
        pts.append(tuple((c * inv) % q for c in v))
    return sorted(set(pts))


def B(u, v, q):
    """The standard symplectic form x0y1 - x1y0 + x2y3 - x3y2."""
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q


def collinearity(q):
    P = points(q)
    n = len(P)
    idx = {p: i for i, p in enumerate(P)}
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if B(P[i], P[j], q) == 0:
                adj[i].add(j)
                adj[j].add(i)
    return P, adj, idx


def hoffman(v, k, lam, mu):
    import math
    D = (lam - mu) ** 2 + 4 * (k - mu)
    s = (lam - mu - math.isqrt(D)) // 2
    return v * (-s) // (k - s), s


def exact_alpha_ilp(adj, n, timelimit=900.0):
    """Exact maximum independent set by ILP with the gap driven to zero."""
    import numpy as np
    from scipy.optimize import LinearConstraint, milp, Bounds

    edges = [(i, j) for i in range(n) for j in adj[i] if i < j]
    rows, cols, vals = [], [], []
    for e, (i, j) in enumerate(edges):
        rows += [e, e]
        cols += [i, j]
        vals += [1.0, 1.0]
    from scipy.sparse import coo_matrix
    A = coo_matrix((vals, (rows, cols)), shape=(len(edges), n))
    res = milp(
        c=-np.ones(n),
        constraints=LinearConstraint(A, -np.inf, 1),
        integrality=np.ones(n),
        bounds=Bounds(0, 1),
        options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True},
    )
    if res.status != 0:
        return None, res.status
    return int(round(-res.fun)), 0


def main() -> int:
    print("=" * 78)
    print("Pass 7106 -- alpha(W(3,q)) exact, q = 3 and 5")
    print("=" * 78)

    results = {}
    for q in (3, 5):
        P, adj, _ = collinearity(q)
        n = len(P)
        k = len(adj[0])
        # SRG parameters of the GQ(q,q) collinearity graph
        v, kk, lam, mu = (q + 1) * (q * q + 1), q * (q + 1), q - 1, q + 1
        hb, s = hoffman(v, kk, lam, mu)
        print(f"\n  q = {q}:  {n} points, degree {k}   "
              f"(SRG({v},{kk},{lam},{mu}), smallest eigenvalue {s})")
        assert n == v and k == kk, "graph does not match the GQ parameters"
        print(f"    Hoffman ratio bound        alpha <= {hb}   (= q^2+1 = "
              f"{q * q + 1}, attained iff an ovoid exists)")
        a, st = exact_alpha_ilp(adj, n)
        if a is None:
            print(f"    ILP did not close (status {st})")
            results[q] = None
            continue
        print(f"    EXACT maximum partial ovoid alpha  = {a}")
        print(f"      ovoid ({q * q + 1}) exists? {'YES' if a == q * q + 1 else 'NO'}"
              f"    deficit from Hoffman: {hb - a}")
        results[q] = a

    print("\n  THE SEQUENCE SO FAR\n")
    print(f"    {'q':>3s}  {'points':>7s}  {'q^2+1':>6s}  {'alpha':>6s}  {'deficit':>8s}")
    for q in (2, 3, 5):
        a = results.get(q, 5 if q == 2 else None)
        if a is None:
            continue
        print(f"    {q:3d}  {(q + 1) * (q * q + 1):7d}  {q * q + 1:6d}  {a:6d}  "
              f"{q * q + 1 - a:8d}")

    if results.get(3) is not None and results.get(5) is not None:
        a3, a5 = results[3], results[5]
        print("\n  CANDIDATE CLOSED FORMS, tested against both exact values\n")
        forms = {
            "q^2 - q + 1": lambda q: q * q - q + 1,
            "q^2 - q": lambda q: q * q - q,
            "(q^2+1)/2": lambda q: (q * q + 1) // 2,
            "q^2 - q + 2": lambda q: q * q - q + 2,
            "2q + 1": lambda q: 2 * q + 1,
            "q^2 - 1": lambda q: q * q - 1,
        }
        for name, f in forms.items():
            ok = f(3) == a3 and f(5) == a5
            print(f"    {name:14s} -> q=3: {f(3):3d}  q=5: {f(5):3d}   "
                  f"{'MATCHES BOTH' if ok else 'no'}")
        print("\n    Two data points cannot select a formula; they can only KILL the ones "
              "that\n    miss. Any survivor is a candidate for q=7, not a result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
