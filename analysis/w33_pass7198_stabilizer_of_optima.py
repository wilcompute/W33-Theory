"""Pass 7198 -- the stabilizer of the optimal partial ovoids, bounded exactly.

THE GAP THIS CLOSES. Pass 7192 proved the maximum partial ovoid of W(3,7) is invariant under
no element of order 3, and none of order 7 in two of three classes. The order-2 case did not
resolve -- the ILP over 200 orbits never closed -- so a 2-group stabilizer stayed open.

THE METHOD, which avoids the group entirely. |Sp(4,7)| is 276,595,200, so enumeration is out.
But any g stabilizing O also stabilizes every structure canonically built from O. Take

    T_min  =  the smallest level set of the TANGENT FUNCTION
              t(x) = #{ o in O : x collinear with o },  x not in O

which is canonical, and form the bipartite collinearity graph between O and T_min. Then

    Stab(O)  embeds into  Aut(that bipartite graph)

so computing the graph automorphism group -- 50-ish vertices, trivial for VF2 -- gives a hard
UPPER bound on the stabilizer. If it is trivial, the stabilizer is trivial, full stop.

POSITIVE CONTROL, because a negative result from an unvalidated method is worth nothing. At
q=3 and q=5 the optimum IS reached by an order-3-invariant set (Pass 7187), so a correct
method MUST see order 3 dividing the bound there. If it does not, the method is broken and
its q=7 answer is discarded. This is stated before the numbers are known.

    py -3 analysis/w33_pass7198_stabilizer_of_optima.py
"""

from __future__ import annotations

import itertools
import json
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


def aut_order(nodes_a, nodes_b, edges):
    """|Aut| of a bipartite graph, sides kept separate (they have different sizes
    or are distinguished by a colour attribute)."""
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher, categorical_node_match

    G = nx.Graph()
    for v in nodes_a:
        G.add_node(("A", v), side="A")
    for v in nodes_b:
        G.add_node(("B", v), side="B")
    for a, b in edges:
        G.add_edge(("A", a), ("B", b))
    gm = GraphMatcher(G, G, node_match=categorical_node_match("side", None))
    n = 0
    for _ in gm.isomorphisms_iter():
        n += 1
        if n > 200000:
            return None
    return n


def main() -> int:
    print("=" * 78)
    print("Pass 7198 -- stabilizer of the optimal partial ovoids, bounded above")
    print("=" * 78)

    rows = []
    for q in (3, 5, 7, 9):
        fp = ROOT / SOURCES[q]
        if not fp.is_file():
            print(f"\n  q={q}: {SOURCES[q]} missing, skipping")
            continue
        doc = json.loads(fp.read_text(encoding="utf-8"))
        F = Field(q)
        P, idx, adj, B = geometry(F)
        n = len(P)
        O = sorted(idx[tuple(p)] for p in doc["points"])
        assert all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(O, 2)), \
            f"q={q}: stored set is not a partial ovoid"
        Oset = set(O)
        tang = {}
        for x in range(n):
            if x in Oset:
                continue
            tang[x] = len(adj[x] & Oset)
        dist = Counter(tang.values())
        tmin = min(dist, key=lambda v: (dist[v], v))
        T = sorted(x for x, v in tang.items() if v == tmin)
        edges = [(o, x) for x in T for o in adj[x] & Oset]
        a = aut_order(O, T, edges)
        rows.append((q, len(O), tmin, len(T), len(edges), a))
        print(f"\n  q={q}:  |O| = {len(O)}")
        print(f"    tangent distribution: {dict(sorted(dist.items()))}")
        print(f"    smallest level set: t = {tmin}, |T_min| = {len(T)}, "
              f"{len(edges)} incidences")
        print(f"    |Aut(bipartite O x T_min)| = "
              f"{a if a is not None else '> 200000 (abandoned)'}", flush=True)

    print("\n  THE POSITIVE CONTROL, read before the q=7 conclusion\n")
    print(f"    {'q':>3s}  {'|O|':>4s}  {'t_min':>6s}  {'|T_min|':>8s}  {'|Aut| bound':>12s}  "
          f"{'3 divides?':>11s}")
    for q, k, tmin, tsz, ne, a in rows:
        div = "n/a" if a is None else ("YES" if a % 3 == 0 else "no")
        print(f"    {q:3d}  {k:4d}  {tmin:6d}  {tsz:8d}  "
              f"{(str(a) if a is not None else '>200000'):>12s}  {div:>11s}")

    ctrl = {q: a for q, k, tm, ts, ne, a in rows if q in (3, 5)}
    ok = all(a is not None and a % 3 == 0 for a in ctrl.values()) and len(ctrl) == 2
    print()
    if ok:
        print("""    CONTROL PASSES. At q=3 and q=5 the optimum is order-3 invariant and the bound is
    divisible by 3, so the method does detect symmetry that is present. Its verdict at q=7
    therefore carries weight.""")
    else:
        print("""    CONTROL FAILS. At q=3 and/or q=5 the optimum IS order-3 invariant (Pass 7187
    exhibits such a set) yet the bound does not reflect it. The method is not detecting
    symmetry that is known to be there, so NO conclusion is drawn at q=7 and the order-2
    gap in Pass 7192 stays open. Reporting the failure rather than the number.""")

    q7 = next((a for q, k, tm, ts, ne, a in rows if q == 7), None)
    if ok and q7 is not None:
        print(f"""
    AT q=7 THE BOUND IS {q7}. Since Stab(O) embeds into this group, the stabilizer of the
    unique maximum partial ovoid of W(3,7) has order dividing {q7}""" +
              (" -- i.e. it is TRIVIAL, and Pass 7192's order-2 gap is now closed."
               if q7 == 1 else f", which closes the order-2 gap only if {q7} is odd."))

    out = ROOT / "data" / "PART_W33_PASS7198_STABILIZER_BOUNDS.json"
    out.write_text(json.dumps(
        {"boundary": ("upper bounds on Stab(O) via embedding into Aut of a canonical "
                      "bipartite graph. An upper bound, not the stabilizer itself; a "
                      "graph automorphism need not be realised by a symplectic map"),
         "control_passed": ok,
         "method": "Stab(O) embeds into Aut(bipartite O x smallest tangent level set)",
         "rows": [{"q": q, "size": k, "t_min": tm, "T_min_size": ts,
                   "incidences": ne, "aut_bound": a}
                  for q, k, tm, ts, ne, a in rows]}, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
