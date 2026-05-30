#!/usr/bin/env python3
"""Local 13+27 shell stats for the W(3,3) symplectic graph."""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path

import numpy as np


def normalize(x):
    x = tuple(a % 3 for a in x)
    i = next(i for i, a in enumerate(x) if a)
    inv = 1 if x[i] == 1 else 2
    return tuple((inv * a) % 3 for a in x)


def points():
    return sorted({normalize(x) for x in itertools.product(range(3), repeat=4) if any(x)})


def symp(a, b):
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % 3


def adjacency():
    pts = points()
    A = np.zeros((len(pts), len(pts)), dtype=int)
    for i, j in itertools.combinations(range(len(pts)), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    return pts, A


def component_sizes(A, nodes):
    nodes = set(nodes)
    seen = set()
    out = []
    for s in sorted(nodes):
        if s in seen:
            continue
        q = deque([s])
        seen.add(s)
        comp = []
        while q:
            u = q.popleft()
            comp.append(u)
            for v in nodes:
                if v not in seen and A[u, v]:
                    seen.add(v)
                    q.append(v)
        out.append(len(comp))
    return sorted(out)


def induced_degree_counter(A, nodes):
    return Counter(int(sum(A[i, j] for j in nodes if j != i)) for i in nodes)


def build_payload():
    pts, A = adjacency()
    anchor = 0
    near = [i for i in range(40) if A[anchor, i]]
    far = [i for i in range(40) if i != anchor and not A[anchor, i]]
    far_edges = int(sum(A[i, j] for i, j in itertools.combinations(far, 2)))
    identities = {
        "graph_40_240_12": A.shape == (40, 40) and int(A.sum() // 2) == 240 and set(A.sum(axis=1)) == {12},
        "local_13_plus_27": 1 + len(near) == 13 and len(far) == 27,
        "neighbor_shell_is_four_triangles": component_sizes(A, near) == [3, 3, 3, 3] and induced_degree_counter(A, near) == {2: 12},
        "far_shell_is_27_vertices_8_regular": induced_degree_counter(A, far) == {8: 27},
        "far_shell_edges_108": far_edges == 108,
    }
    return {
        "theorem": "w33_local_27_shell_stats",
        "anchor": anchor,
        "neighbor_shell": {
            "vertices": len(near),
            "component_sizes": component_sizes(A, near),
            "degree_distribution": dict(induced_degree_counter(A, near)),
        },
        "far_shell": {
            "vertices": len(far),
            "degree_distribution": dict(induced_degree_counter(A, far)),
            "edges": far_edges,
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main():
    payload = build_payload()
    out = Path("data/w33_local_27_shell_stats.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
