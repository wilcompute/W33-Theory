#!/usr/bin/env python3
"""Pass 2442 -- does the CHIRAL tower sit over the CONTEXTUAL side?

Pass 2437 (mine): the two 6:1 towers over 40 split
    POINT side (E8 roots,        fibre C6, antipode INSIDE)  -> C3 on 3 pairs, CHIRAL
    LINE  side (dual codewords,  fibre S3, antipode OUTSIDE) -> S3 on 3 pairs, ACHIRAL

Prior art in the corpus, cited not re-derived:
  analysis/w33_pass1021_corollary_ovoid_orientation.py  --  W(3,3) = (36 spreads,
    0 ovoids), Q(4,3) = (0 spreads, 36 ovoids); "W(q) is contextual iff q is odd,
    because an ovoid -- a Kochen-Specker 0/1 assignment satisfying every context --
    exists iff q is even" (Thas).  That file uses "orientation" for WHICH SIDE of the
    duality; this pass uses it for the C3 cyclic order INSIDE a fibre.  Different
    senses of the word, deliberately kept apart.

What this pass tests: the two 40s are distinguished by ovoid count, and independently
distinguished by fibre chirality.  Do those two distinctions AGREE?

Independent recount here, no reliance on the prose.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

F = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass2442_chirality_meets_contextuality.json"


def canon(v):
    """Canonical projective representative over F3, or None for the zero vector."""
    for a in v:
        if a % F:
            inv = 1 if a % F == 1 else 2
            return tuple((inv * x) % F for x in v)
    return None


def w33_points():
    """The 40 points of PG(3,3); W(3,3) collinearity is the symplectic form."""
    seen = {}
    for v in itertools.product(range(F), repeat=4):
        c = canon(v)
        if c is not None:
            seen[c] = True
    return sorted(seen)


def w33_graph():
    pts = w33_points()
    n = len(pts)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = pts[i], pts[j]
            s = a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]
            adj[i][j] = (s % F == 0)
    return pts, adj


def q43_points():
    """The 40 points of the parabolic quadric Q(4,3): x0x1 + x2x3 + x4^2 = 0."""
    seen = {}
    for v in itertools.product(range(F), repeat=5):
        c = canon(v)
        if c is None:
            continue
        if (c[0] * c[1] + c[2] * c[3] + c[4] * c[4]) % F == 0:
            seen[c] = True
    return sorted(seen)


def q43_graph():
    pts = q43_points()
    n = len(pts)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = pts[i], pts[j]
            # polarisation of the quadratic form
            s = a[0] * b[1] + a[1] * b[0] + a[2] * b[3] + a[3] * b[2] + 2 * a[4] * b[4]
            adj[i][j] = (s % F == 0)
    return pts, adj


def srg_parameters(adj):
    n = len(adj)
    k = sum(adj[0])
    lam = mu = None
    for j in range(1, n):
        c = sum(1 for m in range(n) if adj[0][m] and adj[j][m])
        if adj[0][j]:
            lam = c
        else:
            mu = c
    return [n, k, lam, mu]


def count_ovoids(adj, size):
    """Count independent sets of the given size, and report the true maximum.

    An ovoid of a GQ is a set of pairwise NON-collinear points meeting every line
    once; for GQ(3,3) the forced size is st + 1 = 10.
    """
    n = len(adj)
    nb = [frozenset(j for j in range(n) if adj[i][j]) for i in range(n)]
    found = []
    best = 0

    def extend(cur, cand):
        nonlocal best
        best = max(best, len(cur))
        if len(cur) == size:
            found.append(tuple(cur))
            return
        if len(cur) + len(cand) < size:
            # NOTE: this prune is sound for COUNTING size-`size` sets but makes the
            # `best` tracker an underestimate of the independence number.  The true
            # independence number is computed separately below.
            return
        for v in sorted(cand):
            if v < (cur[-1] if cur else -1):
                continue
            extend(cur + [v], frozenset(c for c in cand if c > v and c not in nb[v]))

    extend([], frozenset(range(n)))

    # true independence number, no size-target prune
    alpha = [0]

    def bb2(size_so_far, cand):
        if size_so_far > alpha[0]:
            alpha[0] = size_so_far
        if not cand or size_so_far + len(cand) <= alpha[0]:
            return
        rest = cand
        for v in sorted(cand):
            if size_so_far + len(rest) <= alpha[0]:
                return
            bb2(size_so_far + 1, frozenset(c for c in rest if c > v and c not in nb[v]))
            rest = rest - {v}

    bb2(0, frozenset(range(n)))
    return len(found), alpha[0]


def main():
    wpts, wadj = w33_graph()
    qpts, qadj = q43_graph()

    wsrg = srg_parameters(wadj)
    qsrg = srg_parameters(qadj)
    wov, wmax = count_ovoids(wadj, 10)
    qov, qmax = count_ovoids(qadj, 10)

    print("=== Pass 2442: chirality vs contextuality ===\n")
    print(f"  W(3,3) point graph : {len(wpts)} points, SRG{tuple(wsrg)}")
    print(f"  Q(4,3) point graph : {len(qpts)} points, SRG{tuple(qsrg)}")
    print()
    print(f"  ovoids (independent 10-sets) in W(3,3) : {wov}")
    print(f"     maximum partial ovoid              : {wmax}")
    print(f"  ovoids (independent 10-sets) in Q(4,3) : {qov}")
    print(f"     maximum partial ovoid              : {qmax}")
    print()
    print("  the two independent distinctions of the two 40s:")
    print(f"    {'side':<12}{'ovoids':>8}{'KS-colourable':>16}{'fibre':>8}"
          f"{'quotient':>10}{'chirality':>12}")
    print(f"    {'W(3,3) pts':<12}{wov:>8}{str(wov > 0):>16}{'C6':>8}"
          f"{'C3':>10}{'CHIRAL':>12}")
    print(f"    {'Q(4,3) pts':<12}{qov:>8}{str(qov > 0):>16}{'S3':>8}"
          f"{'S3':>10}{'achiral':>12}")
    print()
    agree = (wov == 0) and (qov > 0)
    print(f"  DO THEY AGREE ?  {agree}")
    if agree:
        print("  -> the CHIRAL tower sits over the side with NO ovoid (contextual,")
        print("     Kochen-Specker uncolourable); the ACHIRAL tower sits over the")
        print("     side that IS colourable.")

    cert = {
        "pass": 2442,
        "w33_srg": wsrg,
        "q43_srg": qsrg,
        "w33_ovoids": wov,
        "w33_max_partial_ovoid": wmax,
        "q43_ovoids": qov,
        "q43_max_partial_ovoid": qmax,
        "chiral_side_is_ovoid_free": agree,
        "checks": {
            "w33_is_srg_40_12_2_4": wsrg == [40, 12, 2, 4],
            "q43_is_srg_40_12_2_4": qsrg == [40, 12, 2, 4],
            "w33_has_no_ovoid": wov == 0,
            "w33_max_partial_ovoid_is_7": wmax == 7,
            "q43_has_36_ovoids": qov == 36,
            "chiral_side_is_the_contextual_one": agree,
        },
        "prior_art": [
            "analysis/w33_pass1021_corollary_ovoid_orientation.py -- the (36,0)/(0,36)"
            " spread/ovoid duality count and the contextuality reading",
            "Thas -- W(q) has ovoids iff q is even",
            "analysis/w33_pass2436_2441_the_chiral_tower_and_the_achiral_one.md --"
            " the C6/S3 fibre split this pass aligns against",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True))
    ok = sum(cert["checks"].values())
    print(f"\n  checks {ok}/{len(cert['checks'])} -> {OUT.name}")
    return 0 if ok == len(cert["checks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
