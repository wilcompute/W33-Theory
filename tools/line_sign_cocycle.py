#!/usr/bin/env python3
"""Find an explicit sign-cocycle obstruction for root line orientations.

We attempt to assign a sign to each root line so that each generator maps
line reps to line reps. When inconsistent, we extract a cycle with product -1.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_e8_roots():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0.0] * 8
                    r[i] = float(si)
                    r[j] = float(sj)
                    roots.append(tuple(r))
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


def main():
    roots = build_e8_roots()
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # Build root lines and reps
    line_id = [-1] * len(roots)
    line_reps = []
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        j = root_to_idx[tuple(-x for x in r)]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        rep = i if i < j else j
        line_reps.append(rep)

    # Load generator perms
    data = json.loads((ROOT / "artifacts" / "sp43_we6_generator_map.json").read_text())
    gens = [g["root_perm"] for g in data["generator_maps"]]

    # Build constraint graph: line a -> line b with sign eps
    adj = defaultdict(list)
    for gi, g in enumerate(gens):
        for lid, rep in enumerate(line_reps):
            img = g[rep]
            lid2 = line_id[img]
            rep2 = line_reps[lid2]
            eps = 1 if img == rep2 else -1
            adj[lid].append((lid2, eps, gi))

    # BFS with parent tracking to extract conflict
    sigma = [None] * len(line_reps)
    parent = [None] * len(line_reps)  # (prev_line, eps, gi)

    for start in range(len(line_reps)):
        if sigma[start] is not None:
            continue
        sigma[start] = 1
        q = deque([start])
        while q:
            u = q.popleft()
            for v, eps, gi in adj[u]:
                implied = eps * sigma[u]
                if sigma[v] is None:
                    sigma[v] = implied
                    parent[v] = (u, eps, gi)
                    q.append(v)
                else:
                    if sigma[v] != implied:
                        # conflict found: reconstruct cycle u -> v
                        # build path u->root and v->root
                        path_u = []
                        cur = u
                        while cur is not None:
                            path_u.append(cur)
                            cur = parent[cur][0] if parent[cur] else None
                        path_v = []
                        cur = v
                        while cur is not None:
                            path_v.append(cur)
                            cur = parent[cur][0] if parent[cur] else None
                        # find LCA
                        set_u = {x: i for i, x in enumerate(path_u)}
                        lca = None
                        for i, x in enumerate(path_v):
                            if x in set_u:
                                lca = x
                                break
                        # build cycle lines
                        cycle = []
                        # u -> lca
                        cur = u
                        while cur != lca:
                            prev, e, gi2 = parent[cur]
                            cycle.append((prev, cur, e, gi2))
                            cur = prev
                        # lca -> v (reverse path_v)
                        idx = path_v.index(lca)
                        for cur in reversed(path_v[:idx]):
                            prev, e, gi2 = parent[cur]
                            # reverse edge; invert eps
                            cycle.append((cur, prev, e, gi2))
                        # add the conflicting edge u->v
                        cycle.append((u, v, eps, gi))

                        out = {
                            "status": "inconsistent",
                            "conflict_edge": {
                                "from": u,
                                "to": v,
                                "eps": eps,
                                "generator": gi,
                            },
                            "cycle": [
                                {"from": a, "to": b, "eps": e, "generator": gii}
                                for (a, b, e, gii) in cycle
                            ],
                        }
                        (ROOT / "artifacts" / "root_line_sign_cocycle.json").write_text(
                            json.dumps(out, indent=2)
                        )
                        print(
                            "Inconsistency cycle written to artifacts/root_line_sign_cocycle.json"
                        )
                        return

    print("No inconsistency found (unexpected)")


if __name__ == "__main__":
    main()
