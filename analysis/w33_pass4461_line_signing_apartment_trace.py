#!/usr/bin/env python3
"""Pass 4461 -- exact line-signing / apartment trace theorem for W(3,3).

This pass closes the conceptual gap between the recent signing/2-lift arc
(Passes 4409--4455) and the older Levi/Tits-building apartment arc.

The point-collinearity graph G has 40 vertices and 240 edges.  Its 40 geometric
lines are K4s and partition the 240 edges six at a time.  A *line signing*
chooses sigma_l in {+1,-1} on each geometric line and gives every edge on l the
same sign.

The verifier proves, without a search objective:

  (1) A_sigma = N diag(sigma) N^T - diag(N sigma),
      where N is the 40x40 point-line incidence matrix.

  (2) There are exactly 1620 simple 4-cycles in the point graph.  Their four
      edge-lines are distinct and form a simple 4-cycle in the dual line graph.
      Thus these are exactly the point-shadow / line-shadow descriptions of the
      1620 Levi 8-cycle apartments.

  (3) If W4(sigma) is the sum of the four-line products over those apartments,

          tr(A_sigma^4) = 12000 + 8 W4(sigma).

      Equivalently, if f4 is the fraction of frustrated apartments,

          tr(A_sigma^4) = 24960 - 25920 f4.

      The coefficient 25920 is 16*1620.  No group-theoretic meaning is inferred
      from its numerical equality with |PSp(4,3)|.

  (4) The lower moments are exact too:

          tr(A_sigma^2) = 480,
          tr(A_sigma^3) = 24 sum_l sigma_l.

      Hence a 20/20 balanced line signing has exactly zero cubic trace.

  (5) The 1620 apartment supports are 1620 distinct 4-subsets of the 40 lines.
      Under independent random line signs their Walsh monomials are orthogonal:

          E W4 = 0, Var(W4) = 1620,
          E f4 = 1/2, SD(f4) = 1/(2 sqrt(1620)).

      This is an analytic random baseline, not a Monte-Carlo control.

  (6) Let H be the 40x1620 line/apartment incidence matrix and A* the dual
      line-collinearity graph.  Then

          H H^T = 156 I + 21 A* + 6 J,

      because one line lies in 162 apartments, an intersecting pair in 27, and
      a disjoint pair in 6.  Therefore

          spec(H H^T) = 648^1 + 198^24 + 72^15.

Interpretive boundary: Pass 4434 remains right that fourth-moment pressure is a
generic even-moment fact for signed graphs.  What is W33-specific is that here
the entire variable part of that fourth moment is exactly the apartment-parity
observable of the rank-two building.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
F = 3


def geometry():
    pts = []
    for lead in range(4):
        for tail in itertools.product(range(F), repeat=3 - lead):
            pts.append((0,) * lead + (1,) + tail)
    idx = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

    def norm(v):
        for c in v:
            if c:
                inv = pow(int(c), F - 2, F)
                return tuple((inv * z) % F for z in v)
        raise ValueError("zero vector")

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1 :]:
            if symp(x, y):
                continue
            span = set()
            for a in range(F):
                for b in range(F):
                    if a or b:
                        span.add(norm(tuple((a * u + b * v) % F for u, v in zip(x, y))))
            lines.add(frozenset(idx[v] for v in span))
    lines = sorted(lines, key=lambda L: sorted(L))

    A = np.zeros((40, 40), dtype=np.int64)
    edge_line = {}
    for li, L in enumerate(lines):
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
            edge_line[frozenset((u, v))] = li

    N = np.zeros((40, 40), dtype=np.int64)
    for li, L in enumerate(lines):
        for p in L:
            N[p, li] = 1

    return pts, lines, A, N, edge_line


def simple_four_cycles(A):
    """Return simple C4s as their four undirected edges.

    In SRG(40,12,2,4), every nonedge has four common neighbours.  Choosing two
    gives a C4 with that nonedge as an opposite pair; each C4 is seen from its two
    opposite pairs, so the resulting set has 540*C(4,2)/2 = 1620 members.
    """
    out = set()
    for x, y in itertools.combinations(range(len(A)), 2):
        if A[x, y]:
            continue
        common = [z for z in range(len(A)) if A[x, z] and A[y, z]]
        for z1, z2 in itertools.combinations(common, 2):
            edges = frozenset(
                {
                    frozenset((x, z1)),
                    frozenset((z1, y)),
                    frozenset((y, z2)),
                    frozenset((z2, x)),
                }
            )
            out.add(edges)
    return sorted(out, key=lambda C: sorted(map(sorted, C)))


def signed_adjacency(A, edge_line, sigma):
    S = np.zeros_like(A)
    for e, li in edge_line.items():
        u, v = tuple(e)
        S[u, v] = S[v, u] = int(sigma[li])
    return S


def main() -> int:
    pts, lines, A, N, edge_line = geometry()
    checks = []

    def check(name, cond):
        ok = bool(cond)
        checks.append((name, ok))
        if not ok:
            raise AssertionError(name)

    # Substrate, reconstructed rather than trusted.
    check("40 projective points", len(pts) == 40)
    check("40 totally isotropic lines", len(lines) == 40)
    check("240 collinearity edges", int(A.sum() // 2) == 240)
    check("12-regular", np.all(A.sum(axis=1) == 12))

    lam, mu = set(), set()
    for u, v in itertools.combinations(range(40), 2):
        c = int(A[u] @ A[v])
        (lam if A[u, v] else mu).add(c)
    check("SRG lambda=2", lam == {2})
    check("SRG mu=4", mu == {4})
    check("line K4s partition all edges", len(edge_line) == 240)

    # Apartments / C4s.
    cycles = simple_four_cycles(A)
    check("1620 point-graph quadrangles", len(cycles) == 1620)

    Adual = np.zeros((40, 40), dtype=np.int64)
    for i, j in itertools.combinations(range(40), 2):
        if lines[i] & lines[j]:
            Adual[i, j] = Adual[j, i] = 1
    check("dual graph 12-regular", np.all(Adual.sum(axis=1) == 12))

    supports = []
    for C in cycles:
        support = frozenset(edge_line[e] for e in C)
        check("each apartment uses four distinct lines", len(support) == 4)
        ids = sorted(support)
        induced_edges = sum(int(Adual[i, j]) for i, j in itertools.combinations(ids, 2))
        check("four side-lines induce dual C4", induced_edges == 4)
        supports.append(support)
    check("apartment four-line supports unique", len(set(supports)) == 1620)

    # Apartment incidence design.
    H = np.zeros((40, 1620), dtype=np.int64)
    for a, support in enumerate(supports):
        for li in support:
            H[li, a] = 1
    check("each line in 162 apartments", np.all(H.sum(axis=1) == 162))

    pair_count = defaultdict(int)
    for support in supports:
        for i, j in itertools.combinations(sorted(support), 2):
            pair_count[(i, j)] += 1
    adj_counts, dis_counts = [], []
    for i, j in itertools.combinations(range(40), 2):
        (adj_counts if Adual[i, j] else dis_counts).append(pair_count[(i, j)])
    check("intersecting line pair in 27 apartments", set(adj_counts) == {27})
    check("disjoint line pair in 6 apartments", set(dis_counts) == {6})

    gram_expected = 156 * np.eye(40, dtype=np.int64) + 21 * Adual + 6 * np.ones((40, 40), dtype=np.int64)
    check("HHt Bose-Mesner identity", np.array_equal(H @ H.T, gram_expected))
    evals = np.linalg.eigvalsh(H @ H.T)
    rounded = Counter(int(round(x)) for x in evals)
    check("HHt spectrum 648^1 198^24 72^15", rounded == Counter({648: 1, 198: 24, 72: 15}))

    # Exact trace laws sampled over deterministic line signings.  The formulas
    # themselves are algebraic; samples guard implementation/indexing mistakes.
    rng = np.random.default_rng(4461)
    for trial in range(32):
        sigma = rng.choice(np.array([-1, 1], dtype=np.int64), size=40)
        S = signed_adjacency(A, edge_line, sigma)
        factored = N @ np.diag(sigma) @ N.T - np.diag(N @ sigma)
        check(f"incidence factorization sample {trial}", np.array_equal(S, factored))

        W4 = 0
        frustrated = 0
        for support in supports:
            hol = int(np.prod([sigma[li] for li in support]))
            W4 += hol
            frustrated += int(hol == -1)

        t2 = int(np.trace(np.linalg.matrix_power(S, 2)))
        t3 = int(np.trace(np.linalg.matrix_power(S, 3)))
        t4 = int(np.trace(np.linalg.matrix_power(S, 4)))
        check(f"trace2 sample {trial}", t2 == 480)
        check(f"trace3 sample {trial}", t3 == 24 * int(sigma.sum()))
        check(f"trace4 apartment law sample {trial}", t4 == 12000 + 8 * W4)
        check(f"trace4 frustration law sample {trial}", t4 == 24960 - 16 * frustrated)

    balanced = np.array([1] * 20 + [-1] * 20, dtype=np.int64)
    Sb = signed_adjacency(A, edge_line, balanced)
    check("balanced line signing has exact zero cubic trace", int(np.trace(np.linalg.matrix_power(Sb, 3))) == 0)

    # Exact random-line-signing baseline.  Each apartment is a distinct degree-4
    # Walsh monomial in 40 independent Rademacher variables, hence orthogonal to
    # every other apartment monomial.
    random_baseline = {
        "E_W4": 0,
        "Var_W4": 1620,
        "E_frustrated_fraction": 0.5,
        "SD_frustrated_fraction": 1.0 / (2.0 * np.sqrt(1620.0)),
        "E_trace_A4": 12000,
    }
    check("analytic apartment baseline SD positive", random_baseline["SD_frustrated_fraction"] > 0)

    result = {
        "pass": 4461,
        "theorem": "W33 line-signing apartment trace theorem",
        "substrate": {"points": 40, "lines": 40, "edges": 240, "degree": 12, "lambda": 2, "mu": 4},
        "apartments": {
            "count": 1620,
            "lines_per_apartment": 4,
            "apartments_per_line": 162,
            "apartments_per_intersecting_line_pair": 27,
            "apartments_per_disjoint_line_pair": 6,
        },
        "apartment_incidence_gram": {
            "identity": "H H^T = 156 I + 21 A_dual + 6 J",
            "spectrum": {"648": 1, "198": 24, "72": 15},
        },
        "trace_laws": {
            "trace_A2": "480",
            "trace_A3": "24 * sum(sigma_l)",
            "trace_A4": "12000 + 8*W4 = 24960 - 25920*f4",
        },
        "random_line_signing_baseline": random_baseline,
        "boundary": (
            "Fourth-moment pressure is generic for signed graphs.  The W33-specific theorem is that "
            "the entire variable fourth moment is the parity sum over the 1620 rank-two-building apartments. "
            "The equality 25920=16*1620=|PSp(4,3)| is recorded only as arithmetic and is not used structurally."
        ),
        "checks": {"passed": sum(ok for _, ok in checks), "total": len(checks)},
    }

    out = ROOT / "data" / "PART_W33_PASS4461_LINE_SIGNING_APARTMENT_TRACE.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Pass 4461 -- line-signing apartment trace theorem")
    print("  C4/apartments: 1620")
    print("  H H^T = 156 I + 21 A_dual + 6 J")
    print("  spectrum(H H^T) = 648^1 + 198^24 + 72^15")
    print("  tr A_sigma^4 = 12000 + 8 W4 = 24960 - 25920 f4")
    print(f"  analytic random-line SD(f4) = {random_baseline['SD_frustrated_fraction']:.12f}")
    print(f"  checks: {result['checks']['passed']}/{result['checks']['total']} PASS")
    print(f"  wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
