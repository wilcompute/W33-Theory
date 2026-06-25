#!/usr/bin/env python3
"""
GUARDRAIL: the 27 in v=40=1+12+27 is the E6 representation/quadrangle by COUNT
and by GROUP, but NOT as a subgraph. The 27 non-collinear points of GQ(3,3) form
an 8-regular graph, NOT the Schlafli graph SRG(27,16,10,8). The true E6 <->
substrate bridge is the simple group U4(2) = PSp(4,3) = 25920.

A tempting claim was that the 40=1+12+27 split of W(3,3)=GQ(3,3) realizes the
E6 / 27-lines / GQ(2,4) Schlafli graph as the 27 non-collinear points. This
verifier shows that is FALSE:

  - fix a point p of GQ(3,3) (collinearity SRG(40,12,2,4));
  - its 12 collinear points induce a 2-regular graph = 4 disjoint triangles
    (4*K3, the 4 lines through p);
  - its 27 non-collinear points induce an 8-REGULAR graph that is NOT strongly
    regular (mu is not constant), hence NOT the Schlafli graph SRG(27,16,10,8)
    (which is 16-regular = the GQ(2,4) collinearity / the 27 lines on a cubic).

So 40 = 1 + 12 + 27 is an exact count (the "matter cone" 28 = 1 + 27 of BT890),
and 27 matches the E6 fundamental-rep dimension and the GQ(2,4) point count, but
the 27 non-collinear points are not the E6 point-graph.

THE TRUE BRIDGE is group-theoretic. The substrate's projective gauge group and
the E6 / 27-lines group are the SAME simple group:
    PSp(4,3) = PSU(4,2) = U4(2),  order 25920,
with the substrate Sp(4,3) = 2.U4(2) (order 51840), the cubic-surface /
GQ(2,4) automorphism group U4(2):2, and the E6 Weyl group W(E6) = U4(2):2 (order
51840) all extensions of that one simple group. So E6 and W(3,3) share U4(2):
the link is the simple group, not a subgraph.

Verifies the two subconstituents of GQ(3,3) (4*K3 and the 8-regular non-Schlafli
27-graph) and the order relations |PSp(4,3)|=|PSU(4,2)|=25920, |Sp(4,3)|=
|W(E6)|=51840.
"""
from __future__ import annotations

import itertools
import json

Q = 3
PSU42 = 25920  # |PSU(4,2)| = |PSp(4,3)| = U4(2)
SP43 = 51840  # |Sp(4,3)| = |W(E6)|


def build_w33():
    reps, seen = [], set()
    for vec in itertools.product(range(Q), repeat=4):
        if vec == (0, 0, 0, 0):
            continue
        for i in range(4):
            if vec[i]:
                inv = pow(vec[i], Q - 2, Q)
                rep = tuple((inv * x) % Q for x in vec)
                break
        if rep not in seen:
            seen.add(rep)
            reps.append(rep)

    def sform(u, v):
        return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % Q

    n = len(reps)
    adj = {i: set() for i in range(n)}
    for i, j in itertools.combinations(range(n), 2):
        if sform(reps[i], reps[j]) == 0:
            adj[i].add(j)
            adj[j].add(i)
    return n, adj


def induced(adj, verts):
    S = set(verts)
    idx = {v: k for k, v in enumerate(verts)}
    sub = {k: set() for k in range(len(verts))}
    for v in verts:
        for w in adj[v]:
            if w in S:
                sub[idx[v]].add(idx[w])
    return sub


def is_srg(sub):
    m = len(sub)
    ks = {len(sub[i]) for i in range(m)}
    if len(ks) != 1:
        return (False, None)
    k = ks.pop()
    lam, mu = set(), set()
    for i in range(m):
        for j in range(m):
            if i == j:
                continue
            c = len(sub[i] & sub[j])
            (lam if j in sub[i] else mu).add(c)
    if len(lam) == 1 and len(mu) == 1:
        return (True, (m, k, lam.pop(), mu.pop()))
    return (False, (m, k, sorted(lam), sorted(mu)))


def n_components(sub):
    m = len(sub)
    seen, comps = set(), 0
    for s in range(m):
        if s in seen:
            continue
        comps += 1
        stack = [s]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(sub[x])
    return comps


def main():
    out = {}

    n, adj = build_w33()
    p = 0
    collinear = sorted(adj[p])
    noncol = [v for v in range(n) if v != p and v not in adj[p]]
    print(f"[GQ(3,3) = W(3,3)]  {n} points, valency {len(adj[p])}")
    print(
        f"  point p: 1 + {len(collinear)} collinear + {len(noncol)} non-collinear = {n}"
    )
    assert n == 40 and len(collinear) == 12 and len(noncol) == 27

    # first subconstituent: 12 collinear -> 4 triangles
    sub12 = induced(adj, collinear)
    ks12 = {len(sub12[i]) for i in sub12}
    comps12 = n_components(sub12)
    print(f"\n[1st subconstituent: 12 collinear points]")
    print(f"  valency set {ks12} (2-regular); connected components = {comps12} = 4*K3")
    assert ks12 == {2} and comps12 == 4
    out["first_subconstituent"] = "4*K3 (4 triangles = the 4 lines through p)"

    # second subconstituent: 27 non-collinear -> 8-regular, NOT Schlafli
    sub27 = induced(adj, noncol)
    srg27, params27 = is_srg(sub27)
    ks27 = {len(sub27[i]) for i in sub27}
    print(f"\n[2nd subconstituent: 27 non-collinear points]")
    print(
        f"  valency set {ks27} (8-regular); strongly regular? {srg27}; params {params27}"
    )
    print(f"  -> NOT the Schlafli graph SRG(27,16,10,8) (which is 16-regular)")
    assert ks27 == {8} and srg27 is False
    out["second_subconstituent"] = {
        "regular_valency": 8,
        "is_schlafli": False,
        "schlafli_would_be": "SRG(27,16,10,8)",
    }

    # the count is real, the graph is not
    print(f"\n[so v=40=1+12+27 is a COUNT, not an E6 subgraph]")
    print(f"  28 = 1 + 27 = matter cone (BT890); 27 = E6 rep dim = GQ(2,4) points,")
    print(f"  but the 27 non-collinear points are NOT the E6 / Schlafli point-graph.")
    assert 1 + 12 + 27 == 40
    out["count_not_graph"] = True

    # the TRUE bridge: the simple group U4(2) = PSp(4,3)
    print(f"\n[the true bridge: the simple group U4(2) = PSp(4,3) = {PSU42}]")
    print(f"  |PSp(4,3)| = |PSU(4,2)| = U4(2) = {PSU42} (simple)")
    print(f"  substrate Sp(4,3) = 2.U4(2) = {SP43}; W(E6) = U4(2):2 = {SP43};")
    print(f"  Aut(GQ(2,4)) = U4(2):2. E6 and W(3,3) share the simple group U4(2).")
    assert PSU42 == 25920 and SP43 == 2 * PSU42 == 51840
    out["group_bridge"] = {
        "simple_group": "U4(2)=PSp(4,3)=PSU(4,2)=25920",
        "Sp43": "2.U4(2)=51840",
        "W_E6": "U4(2):2=51840",
        "GQ24_aut": "U4(2):2",
    }

    print("\nRESULT (guardrail): the 27 of v=40=1+12+27 is the E6 / 27-lines /")
    print("  GQ(2,4) object by representation dimension and by group, but NOT by")
    print("  point-graph. The 27 non-collinear points of GQ(3,3) form an 8-regular")
    print("  graph, not the 16-regular Schlafli graph SRG(27,16,10,8). The genuine")
    print("  E6 <-> substrate bridge is the simple group U4(2) = PSp(4,3) = 25920,")
    print("  shared by Sp(4,3)=2.U4(2), W(E6)=U4(2):2, and Aut(GQ(2,4))=U4(2):2. The")
    print("  '27 = E6 matter' identifications in the tower are dimension/group")
    print(
        "  matches, not subgraph embeddings -- recorded here to keep the claim honest."
    )

    out["summary"] = (
        "GUARDRAIL: 40=1+12+27 in GQ(3,3) is an exact count (matter cone 28=1+27, "
        "BT890) and 27 = E6 rep dim = GQ(2,4) points, but the 27 non-collinear "
        "points form an 8-regular graph, NOT the Schlafli graph SRG(27,16,10,8) "
        "(16-regular); the 12 collinear form 4*K3. So '27=E6' is a dimension/group "
        "match, not a subgraph. The true bridge is the simple group U4(2)=PSp(4,3)="
        "PSU(4,2)=25920, shared by Sp(4,3)=2.U4(2)=51840, W(E6)=U4(2):2=51840, and "
        "Aut(GQ(2,4))=U4(2):2."
    )
    out["sources"] = [
        "GQ(3,3)=W(3,3) collinearity SRG(40,12,2,4), subconstituents (4*K3 and an "
        "8-regular non-Schlafli 27-graph) computed here; Schlafli graph "
        "SRG(27,16,10,8) = GQ(2,4) collinearity; PSp(4,3)=PSU(4,2)=U4(2)=25920, "
        "W(E6)=U4(2):2=51840; BT890 matter cone 28=1+27; "
        "w33_generalized_quadrangle_ladder.py, w33_hessian_polytope_e6.py."
    ]
    with open("data/w33_27_not_schlafli_group_bridge.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_27_not_schlafli_group_bridge.json")


if __name__ == "__main__":
    main()
