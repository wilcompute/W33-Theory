#!/usr/bin/env python3
"""Pass5677: a genuinely connected refinement tower from fresh Levi H^1 classes.

Pass5629 killed the tempting iteration of one fixed Kronecker C2 lift: after the first
bipartite double cover, pulling the same class back and lifting again gives two copies.
The correct graph-cover statement is cohomological.  A Z2 voltage double cover of a
connected graph is connected iff the voltage around some cycle is nonzero, equivalently
iff its class in H^1(G;F2) is nontrivial.

The W33 point-line Levi graph L has

    V=80, E=160, beta_1=81, degree=4.

At each level this verifier chooses a spanning tree and places voltage 1 on one
non-tree edge and 0 on every other edge.  The fundamental cycle of that chord has
voltage 1, so the derived 2-cover is connected.  Repeating the construction on the
NEW graph, rather than pulling back the old voltage, gives an infinite connected tower

    L_0 <- L_1 <- L_2 <- ...

with exact counts

    |V(L_n)| = 80*2^n,
    |E(L_n)| = 160*2^n,
    beta_1(L_n) = 1 + 80*2^n.

Thus the dead repeated-C2 route was a statement about reusing one cohomology class,
not a no-go for connected binary refinement itself.  The price is that a fresh H^1
choice is required at every level; the finite geometry has not yet selected a unique
one.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5677_CONNECTED_LEVI_VOLTAGE_TOWER.json"
Q = 3
J = np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]], dtype=int) % Q


def norm(v):
    v = tuple(int(x) % Q for x in v)
    for a in v:
        if a:
            z = pow(a, -1, Q)
            return tuple((z*x) % Q for x in v)
    raise ValueError("zero")


def B(x, y):
    return int(np.array(x, dtype=int) @ J @ np.array(y, dtype=int)) % Q


def levi_graph():
    pts = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    pi = {p:i for i,p in enumerate(pts)}
    lines = set()
    for i,p in enumerate(pts):
        for q in pts[i+1:]:
            if B(p,q) != 0:
                continue
            line = {norm(tuple((a*p[k]+b*q[k]) % Q for k in range(4)))
                    for a,b in itertools.product(range(Q), repeat=2) if (a,b)!=(0,0)}
            if len(line) == 4:
                lines.add(tuple(sorted(pi[x] for x in line)))
    lines = sorted(lines)
    assert len(pts) == len(lines) == 40
    adj = [set() for _ in range(80)]
    for li,line in enumerate(lines):
        v = 40 + li
        for p in line:
            adj[p].add(v); adj[v].add(p)
    assert {len(a) for a in adj} == {4}
    return adj


def edges(adj):
    return sorted((u,v) for u in range(len(adj)) for v in adj[u] if u < v)


def components(adj):
    seen = set(); sizes = []
    for s in range(len(adj)):
        if s in seen:
            continue
        stack=[s]; seen.add(s); n=0
        while stack:
            u=stack.pop(); n+=1
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
        sizes.append(n)
    return sorted(sizes, reverse=True)


def spanning_tree(adj):
    seen={0}; q=deque([0]); T=[]
    while q:
        u=q.popleft()
        for v in sorted(adj[u]):
            if v not in seen:
                seen.add(v); q.append(v); T.append(tuple(sorted((u,v))))
    assert len(seen)==len(adj)
    return set(T)


def fresh_connected_two_lift(adj):
    E=edges(adj); T=spanning_tree(adj)
    chord=next(e for e in E if e not in T)
    n=len(adj); out=[set() for _ in range(2*n)]
    for u,v in E:
        sign = 1 if (u,v)==chord else 0
        for sheet in (0,1):
            a=u+sheet*n
            b=v+(sheet ^ sign)*n
            out[a].add(b); out[b].add(a)
    assert components(out)==[2*n]
    return out, chord


def main():
    L=levi_graph()
    assert components(L)==[80]
    levels=[]; chords=[]
    current=L
    for depth in range(8):
        V=len(current); E=len(edges(current)); beta=E-V+1
        assert V==80*(2**depth)
        assert E==160*(2**depth)
        assert beta==1+80*(2**depth)
        assert {len(a) for a in current}=={4}
        assert components(current)==[V]
        levels.append({"depth":depth,"vertices":V,"edges":E,"beta1":beta,"degree":4})
        if depth<7:
            current,ch=fresh_connected_two_lift(current)
            chords.append(list(ch))

    out={
      "pass":5677,
      "status":"INFINITE_CONNECTED_BINARY_VOLTAGE_TOWER_EXISTS_FROM_FRESH_LEVI_H1_CLASSES",
      "base":{"graph":"W33 point-line Levi graph","vertices":80,"edges":160,"degree":4,"beta1":81},
      "connectivity_criterion":"a Z2 derived cover is connected iff the cycle-voltage image is all Z2, equivalently the voltage class in H^1(G;F2) is nonzero",
      "construction":"at every level choose a spanning tree, put voltage 1 on one non-tree chord and 0 elsewhere; its fundamental cycle has voltage 1",
      "closed_forms":{"vertices":"80*2^n","edges":"160*2^n","beta1":"1+80*2^n","degree":4},
      "verified_levels":levels,
      "chosen_chords_first_7_levels":chords,
      "relation_to_pass5629":"reusing the pulled-back first C2 class trivializes it and disconnects; choosing a fresh nonzero H^1 class on each new cover restores connectedness",
      "noncanonicity":"the tower exists canonically as a class of constructions, but the finite geometry has not selected a unique fresh H^1 class at each level",
      "physics_boundary":"Graph covering refines global sheet structure while preserving local degree. Existence of this tower is not yet a continuum spacetime limit or a derived spectral dimension."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
