#!/usr/bin/env python3
"""Pass 4296 -- two of Spence's 28 share |Aut| = 51,840.  What separates them?

Pass 4281: all 28 non-isomorphic SRG(40,12,2,4) graphs have identical Ihara zetas, so the
78 = dim(E6) pole count is a parameter fact and cannot identify W(3,3).
Pass 4287: their automorphism orders span 1 to 51,840 across 20 values -- an invariant the
zeta discards -- but the maximum is attained by TWO of them, not one.

So neither the spectrum nor the group order picks a graph, and the residual ambiguity was
recorded as open.  This closes it, or reports honestly that it does not.

Invariants tried, cheapest first, all computed from the adjacency matrix alone:
  * permutation RANK of Aut (number of orbits on ordered pairs).  A rank-3 graph is one
    whose group is transitive on vertices, edges and non-edges -- the defining property of
    the symplectic graph, and the thing that makes W(3,3) special in this project.
  * vertex- and edge-transitivity.
  * local structure: the subgraph induced on a vertex's neighbourhood, and on its
    non-neighbourhood, as spectra rather than counts (Pass 328's rule: compare characters,
    not sizes).
  * small-subgraph census: triangles, 4-cliques, independent sets in the neighbourhood.

    py -3 analysis/w33_pass4296_separate_the_final_pair.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def g6_decode(line):
    data = [ord(c) - 63 for c in line.strip()]
    n = data[0]
    bits = []
    for byte in data[1:]:
        bits.extend((byte >> k) & 1 for k in range(5, -1, -1))
    A = np.zeros((n, n), dtype=int)
    idx = 0
    for j in range(1, n):
        for i in range(j):
            if idx < len(bits) and bits[idx]:
                A[i, j] = A[j, i] = 1
            idx += 1
    return A


def automorphisms(A, cap=None):
    """All automorphisms as permutations, by refinement-guided backtracking."""
    n = A.shape[0]
    adj = [set(np.flatnonzero(A[i]).tolist()) for i in range(n)]

    def refine(colour):
        while True:
            sig = {i: (colour[i], tuple(sorted(colour[j] for j in adj[i])))
                   for i in range(n)}
            order = {s: t for t, s in enumerate(sorted(set(sig.values())))}
            new = [order[sig[i]] for i in range(n)]
            if len(set(new)) == len(set(colour)):
                return new
            colour = new

    base = refine([0] * n)
    out, perm = [], [-1] * n

    def bt(k):
        if cap and len(out) >= cap:
            return
        if k == n:
            out.append(tuple(perm))
            return
        used = set(perm[:k])
        for img in range(n):
            if img in used or base[img] != base[k]:
                continue
            if all((img in adj[perm[j]]) == (k in adj[j]) for j in range(k)):
                perm[k] = img
                bt(k + 1)
                perm[k] = -1

    bt(0)
    return out


def orbital_rank(A, auts):
    """Number of Aut-orbits on ORDERED pairs.  Rank 3 <=> transitive on vertices, on
    ordered edges, and on ordered non-edges."""
    n = A.shape[0]
    seen = -np.ones((n, n), dtype=int)
    r = 0
    for i in range(n):
        for j in range(n):
            if seen[i, j] >= 0:
                continue
            for p in auts:
                seen[p[i], p[j]] = r
            r += 1
    return r


def local_spectra(A):
    """Spectrum of the subgraph induced on each neighbourhood, as a multiset of rounded
    characteristic data -- a character-level comparison, not a count."""
    n = A.shape[0]
    out = Counter()
    for v in range(n):
        nb = np.flatnonzero(A[v])
        sub = A[np.ix_(nb, nb)]
        ev = tuple(np.round(np.linalg.eigvalsh(sub), 6).tolist())
        out[ev] += 1
    return out


def local_cycle_type(A):
    """For an SRG with lambda = 2 every neighbourhood is 2-regular on k vertices, hence a
    disjoint union of cycles.  The multiset of cycle lengths -- the LOCAL GRAPH -- is the
    classical separator for strongly regular graphs, and it is not a spectrum, a count of
    triangles, or anything else tried above.  An earlier version of this pass compared the
    NUMBER of distinct local spectra (1 for both) instead of the spectra themselves, which
    is exactly the counts-versus-characters mistake CLAUDE.md warns about."""
    n = A.shape[0]
    out = Counter()
    for v in range(n):
        nb = list(np.flatnonzero(A[v]))
        idx = {u: i for i, u in enumerate(nb)}
        sub = A[np.ix_(nb, nb)]
        seen, cycles = set(), []
        for s in range(len(nb)):
            if s in seen:
                continue
            length, cur, prev = 0, s, -1
            while cur not in seen:
                seen.add(cur)
                length += 1
                nxt = [j for j in np.flatnonzero(sub[cur]) if j != prev]
                if not nxt:
                    break
                prev, cur = cur, int(nxt[0])
            cycles.append(length)
        out[tuple(sorted(cycles))] += 1
    return out


def main() -> int:
    print("=" * 78)
    print("Pass 4296 -- separating the two SRG(40,12,2,4) graphs with |Aut| = 51,840")
    print("=" * 78)
    path = ROOT / "data" / "spence_srg_40_12_2_4.g6"
    graphs = [g6_decode(l) for l in path.read_text().splitlines() if l.strip()]

    # Locate the pair again rather than trusting the indices recorded at Pass 4287.
    cand = []
    for i, A in enumerate(graphs):
        k = len(automorphisms(A, cap=51841))
        if k == 51840:
            cand.append(i)
    print(f"  graphs with |Aut| = 51,840: {cand}")
    if len(cand) != 2:
        print("  expected exactly two; aborting rather than guessing")
        return 1

    results = {}
    for i in cand:
        A = graphs[i]
        auts = automorphisms(A)
        n = A.shape[0]
        vt = len({p[0] for p in auts}) == n
        rank = orbital_rank(A, auts)
        tri = int(np.trace(np.linalg.matrix_power(A, 3)) // 6)
        loc = local_spectra(A)
        # 4-cliques
        q = 0
        for a in range(n):
            for b in range(a + 1, n):
                if not A[a, b]:
                    continue
                common = np.flatnonzero(A[a] & A[b])
                for ci in range(len(common)):
                    for di in range(ci + 1, len(common)):
                        if A[common[ci], common[di]]:
                            q += 1
        cyc = local_cycle_type(A)
        results[i] = {"aut": len(auts), "vertex_transitive": vt, "orbital_rank": rank,
                      "triangles": tri, "four_cliques": q // 6,
                      "distinct_local_spectra": len(loc),
                      "local_spectrum": str(sorted(loc)[0][:4]) + "...",
                      "local_cycle_type": str(dict(cyc))}
        print(f"\n  graph {i}")
        for k2, v2 in results[i].items():
            print(f"    {k2:24s} {v2}")

    a, b = cand
    diffs = [k2 for k2 in results[a] if results[a][k2] != results[b][k2]]
    print(f"\n  invariants that DIFFER: {diffs if diffs else 'none'}")

    # Every cheap invariant agreeing on two supposedly non-isomorphic graphs is itself a
    # claim worth testing rather than accepting.  Search for an explicit isomorphism.
    def isomorphism(A1, A2):
        n = A1.shape[0]
        ad1 = [set(np.flatnonzero(A1[i]).tolist()) for i in range(n)]
        ad2 = [set(np.flatnonzero(A2[i]).tolist()) for i in range(n)]
        perm = [-1] * n

        def bt(k):
            if k == n:
                return tuple(perm)
            used = set(perm[:k])
            for img in range(n):
                if img in used:
                    continue
                if all((img in ad2[perm[j]]) == (k in ad1[j]) for j in range(k)):
                    perm[k] = img
                    got = bt(k + 1)
                    if got:
                        return got
                    perm[k] = -1
            return None

        return bt(0)

    iso = isomorphism(graphs[a], graphs[b])
    print(f"  explicit isomorphism found: {iso is not None}")

    # THE HYPOTHESIS THE NUMBERS POINT AT.  Two non-isomorphic rank-3 graphs on the same
    # parameters, same |Aut|, same local structure, is the signature of a DUALITY rather
    # than of two unrelated objects: the generalized quadrangle GQ(3,3) has 40 points AND
    # 40 totally isotropic lines, and for odd q the point graph and the line graph are
    # non-isomorphic.  Build both from the symplectic form and test.
    J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
    vecs = [v for v in ((p, q_, r_, s_) for p in range(3) for q_ in range(3)
                        for r_ in range(3) for s_ in range(3)) if any(v)]
    seen_pts, pts = set(), []
    for v in vecs:
        key = min(tuple((c * x) % 3 for x in v) for c in (1, 2))
        if key not in seen_pts:
            seen_pts.add(key)
            pts.append(key)

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    P = np.zeros((40, 40), dtype=int)
    for i in range(40):
        for j in range(40):
            if i != j and form(pts[i], pts[j]) == 0:
                P[i, j] = 1

    lines = set()
    for i in range(40):
        for j in range(i + 1, 40):
            if form(pts[i], pts[j]):
                continue
            span = set()
            for c1 in range(3):
                for c2 in range(3):
                    w = tuple((c1 * pts[i][t] + c2 * pts[j][t]) % 3 for t in range(4))
                    if any(w):
                        span.add(min(tuple((c * x) % 3 for x in w) for c in (1, 2)))
            if len(span) == 4:
                lines.add(frozenset(span))
    lines = sorted(lines, key=lambda s: sorted(s))
    L = np.zeros((len(lines), len(lines)), dtype=int)
    for i in range(len(lines)):
        for j in range(len(lines)):
            if i != j and lines[i] & lines[j]:
                L[i, j] = 1
    print(f"\n  built the symplectic GQ(3,3): {len(pts)} points, {len(lines)} lines")
    print(f"  line graph is 12-regular: "
          f"{bool(L.sum(axis=1).min() == 12 and L.sum(axis=1).max() == 12)}")
    match = {}
    for lbl, G in (("point graph", P), ("line graph", L)):
        for i in cand:
            if G.shape == graphs[i].shape and isomorphism(G, graphs[i]) is not None:
                match[lbl] = i
    print(f"  matches: {match}")
    if len(match) == 2 and match.get("point graph") != match.get("line graph"):
        print(f"""
  THE PAIR IS THE GQ DUALITY, and that reframes the whole question.

  Graph {match['point graph']} is the POINT graph of the symplectic generalized quadrangle
  GQ(3,3) and graph {match['line graph']} is its LINE graph.  They are not two unrelated
  strongly regular graphs that happen to collide on every invariant -- they are the two
  halves of ONE geometry, and for odd q the duality W(3,q) <-> Q(4,q) is not an
  isomorphism, which is exactly why they are non-isomorphic while sharing the parameters,
  the spectrum, |Aut| = 51,840, rank 3, and the locally-4K3 structure.

  So the "residual ambiguity" Pass 4287 recorded as open was never an ambiguity about
  which graph is exceptional.  Both are.  The invariants agree because points and lines of
  a self-dual-parameter GQ are interchangeable at the level of every count, and the thing
  that separates them is which role they play -- precisely the p/f distinction this
  machine's register is built on (Pass 4282).

  The identification ladder, finally honest: the zeta sees 1 class of 28, |Aut| sees 20,
  and the last two are the point and line sides of the same object.""")
        dual = True
    else:
        print("""
  NOT the point/line pair of the symplectic GQ, or only one side matched.  The hypothesis
  was worth testing and it is not confirmed here; the pair stays open.""")
        dual = False
    if iso is not None:
        P = np.zeros((40, 40), dtype=int)
        for i, j in enumerate(iso):
            P[i, j] = 1
        ok = bool((P @ graphs[b] @ P.T == graphs[a]).all())
        print(f"  verified P A_{b} P^T == A_{a}: {ok}")
        print(f"""
  THE TWO ARE ISOMORPHIC.  Every cheap invariant agreed because there was nothing to
  separate: entries {a} and {b} of data/spence_srg_40_12_2_4.g6 are the SAME GRAPH in two
  labellings, and the isomorphism is exhibited and verified above.

  So the file holds 28 lines but at most 27 pairwise non-isomorphic graphs, and Pass 4287's
  "the maximum |Aut| is attained by two of the 28" was an artefact of that duplication.
  Corrected: |Aut| = 51,840 is attained by ONE graph up to isomorphism, and it is W(3,3).

  The identification ladder therefore does close, and more cleanly than expected: the zeta
  distinguishes nothing among these parameters, and |Aut| alone singles out W(3,3).  The
  lesson is the one this repo keeps relearning -- when several independent invariants all
  agree, the first hypothesis to test is that the objects are the same, not that the
  invariants are weak.""")
        out_iso = {"isomorphic": True, "permutation": list(iso), "verified": ok}
    else:
        out_iso = {"isomorphic": False, "permutation": None, "verified": None}

    if iso is not None or dual:
        pass                    # the isomorphism / duality block above said it all
    elif diffs:
        print(f"""
  SEPARATED.  The two graphs that share both the Ihara zeta and |Aut| = 51,840 are
  distinguished by {', '.join(diffs)}.

  The one with orbital rank 3 is the symplectic graph W(3,3): rank 3 means its
  automorphism group is transitive on vertices, on ordered edges AND on ordered
  non-edges, which is exactly the property the rest of this project relies on when it
  treats the 40 points and their incidences as a single homogeneous object.  The other
  graph has the same group ORDER and a coarser action.

  So the identification ladder is now complete and each rung is honest about what it does:
  the zeta distinguishes 1 class of 28, |Aut| distinguishes 20, and the orbital rank
  separates the final pair.  What makes W(3,3) exceptional is not its spectrum and not the
  size of its symmetry group -- it is that the symmetry acts with rank 3.""")
    else:
        print("""
  NOT SEPARATED by any invariant tried here.  The pair share the zeta, the automorphism
  order, the orbital rank, the triangle and 4-clique counts, and their local spectra.
  That is a stronger statement than 'I could not tell them apart': these are the standard
  cheap invariants, and they are exhausted.  Distinguishing the pair needs the group
  action itself -- a conjugacy test in S_40 -- rather than any derived count, and that
  stays open.""")

    out = {"candidates": cand, "isomorphism": out_iso, "results": {str(k2): v2 for k2, v2 in results.items()},
           "separating_invariants": diffs, "gq_duality": dual}
    p = ROOT / "data" / "PART_W33_PASS4296_SEPARATE_FINAL_PAIR.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
