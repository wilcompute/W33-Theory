"""Pass 7199 -- the stabilizer again, with an invariant that actually discriminates.

PASS 7198 USED A USELESS INVARIANT AND ITS CONTROL DID NOT CATCH IT. The bipartite graph
between O and the smallest tangent level set had 7 incidences on 7+7 vertices at q=3 -- a
perfect matching, whose automorphism group is S_7 of order 5040. That IS divisible by 3, so
the positive control passed, while the bound was vacuous. A control can only prove a method
detects what is there; it cannot prove the method says anything USEFUL. Both are needed, and
Pass 7198 checked only the first.

THE REPLACEMENT INVARIANT, defined on PAIRS inside O, where the structure actually lives.
In a GQ(q,q) any two non-collinear points a, b have

    trace(a,b) = { x : x collinear with both }   with  |trace(a,b)| = q+1 exactly,

so the trace SIZE is constant and carries nothing. But the tangent function
t(x) = #{o in O : x collinear with o} is canonical for O, so

    w(a,b) = the sorted multiset of t(x) for x in trace(a,b)

is a genuine O-invariant colouring of the pairs. Any g stabilizing O permutes O preserving w,
hence Stab(O) embeds in Aut of the edge-coloured complete graph on O. That is a real bound.

TWO CONTROLS THIS TIME, both stated before the numbers:
  1. DETECTION -- at q=3 and q=5 the optimum is order-3 invariant, so 3 must divide the bound;
  2. DISCRIMINATION -- the bound must be far below |O|!, or the invariant is doing no work
     and the number is meaningless whatever it is.

    py -3 analysis/w33_pass7199_stabilizer_trace_invariant.py
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SOURCES = {
    3: "data/PART_W33_Q3_PARTIAL_OVOID_7.json",
    5: "data/PART_W33_Q5_ORDER3_OVOID_18.json",
    7: "data/PART_W33_Q7_LNS_OVOID_33.json",
    9: "data/PART_W33_Q9_LNS_OVOID_51.json",
}


def aut_edge_coloured(k, colour, cap=2000000):
    """|Aut| of the complete graph on k vertices with edge colouring `colour`."""
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher, categorical_edge_match

    G = nx.Graph()
    G.add_nodes_from(range(k))
    for i in range(k):
        for j in range(i + 1, k):
            G.add_edge(i, j, c=colour[(i, j)])
    gm = GraphMatcher(G, G, edge_match=categorical_edge_match("c", None))
    n = 0
    for _ in gm.isomorphisms_iter():
        n += 1
        if n > cap:
            return None
    return n


def main() -> int:
    print("=" * 78)
    print("Pass 7199 -- Stab(O) bounded by an invariant that discriminates")
    print("=" * 78)

    rows = []
    for q in (3, 5, 7, 9):
        fp = ROOT / SOURCES[q]
        if not fp.is_file():
            continue
        doc = json.loads(fp.read_text(encoding="utf-8"))
        F = Field(q)
        P, idx, adj, B = geometry(F)
        n = len(P)
        O = sorted(idx[tuple(p)] for p in doc["points"])
        Oset = set(O)
        assert all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(O, 2))
        t = {x: len(adj[x] & Oset) for x in range(n) if x not in Oset}
        k = len(O)
        colour, sizes = {}, Counter()
        for i in range(k):
            for j in range(i + 1, k):
                tr = adj[O[i]] & adj[O[j]]
                sizes[len(tr)] += 1
                colour[(i, j)] = tuple(sorted(t.get(x, -1) for x in tr))
        ncol = len(set(colour.values()))
        a = aut_edge_coloured(k, colour)
        rows.append((q, k, dict(sizes), ncol, a))
        print(f"\n  q={q}:  |O| = {k}")
        print(f"    trace sizes: {dict(sizes)}   (constant q+1 = {q + 1} expected)")
        print(f"    distinct pair-colours: {ncol} over {k * (k - 1) // 2} pairs")
        print(f"    |Aut(edge-coloured K_{k})| = "
              f"{a if a is not None else 'abandoned'}", flush=True)

    print("\n  BOTH CONTROLS\n")
    print(f"    {'q':>3s}  {'|O|':>4s}  {'colours':>8s}  {'|Aut|':>8s}  "
          f"{'|O|!':>12s}  {'3 | Aut':>8s}  {'discriminates':>14s}")
    for q, k, sz, ncol, a in rows:
        fact = math.factorial(k)
        div = "n/a" if a is None else ("YES" if a % 3 == 0 else "no")
        disc = "n/a" if a is None else ("YES" if a < fact / 10 ** 6 or a <= 10 ** 4
                                        else "weak")
        fs = f"{fact:.3g}" if fact > 10 ** 12 else str(fact)
        print(f"    {q:3d}  {k:4d}  {ncol:8d}  "
              f"{(str(a) if a is not None else 'abandoned'):>8s}  {fs:>12s}  "
              f"{div:>8s}  {disc:>14s}")

    ctrl = {q: a for q, k, sz, nc, a in rows if q in (3, 5)}
    detect = all(a is not None and a % 3 == 0 for a in ctrl.values()) and len(ctrl) == 2
    discrim = all(a is not None and a <= 10 ** 4 for a in ctrl.values())
    print()
    if detect and discrim:
        print("""    BOTH CONTROLS PASS. The invariant detects the order-3 symmetry that is known to
    be present at q=3 and q=5, AND the bounds are small enough to be doing real work.""")
    elif detect and not discrim:
        print("""    DETECTION PASSES, DISCRIMINATION FAILS -- the bound is too close to |O|! for the
    invariant to be constraining anything. This is exactly the failure Pass 7198 shipped, and
    no conclusion is drawn at q=7 or q=9.""")
    else:
        print("""    DETECTION FAILS: the invariant misses order-3 symmetry known to be present.
    No conclusion is drawn anywhere. Reporting the failure rather than the number.""")

    q7 = next((a for q, k, sz, nc, a in rows if q == 7), None)
    if detect and discrim and q7 is not None:
        print(f"""
    AT q=7 THE BOUND IS {q7}. Stab(O) embeds into this group, so the stabilizer of the unique
    maximum partial ovoid of W(3,7) has order dividing {q7}.""")
        if q7 % 2:
            print(f"""    {q7} IS ODD, so no involution stabilizes O and PASS 7192'S ORDER-2 GAP IS CLOSED:
    combined with orders 3 and 7, the stabilizer is TRIVIAL.""")

    out = ROOT / "data" / "PART_W33_PASS7199_STABILIZER_TRACE.json"
    out.write_text(json.dumps(
        {"boundary": ("upper bounds on Stab(O) by embedding into Aut of the edge-coloured "
                      "complete graph on O. An UPPER bound: a graph automorphism need not be "
                      "realised by a symplectic map"),
         "supersedes": ("Pass 7198, whose invariant was a perfect matching at q=3 and whose "
                        "control passed while the bound was vacuous"),
         "invariant": "w(a,b) = sorted multiset of tangent values over trace(a,b)",
         "controls": {"detection_order3_at_q3_q5": detect,
                      "discrimination_bound_small": discrim},
         "rows": [{"q": q, "size": k, "trace_sizes": sz, "colours": nc, "aut_bound": a}
                  for q, k, sz, nc, a in rows]}, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
