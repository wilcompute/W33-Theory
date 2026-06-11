#!/usr/bin/env python3
"""
BT780 - The rank-32 cube-web suborbit atlas.

BT779 found that the PSp(4,3) action on the 540 skew-pair / cube-chart
nodes has orbital rank 32.  Rank is only the character shadow.  BT780
constructs the 32 actual relations: fix one cube chart, compute its
48-element stabilizer, split all 540 charts into stabilizer suborbits,
then measure each relation against the BT777 cube-web adjacency and the
W(3,3) line-incidence geometry.

The output is a concrete routing table: the rank-32 association scheme is
not a slogan; it is a 32-state finite automaton around a cube chart.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path

import networkx as nx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def inv3(a):
    a %= 3
    if a in (1, 2):
        return a
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def build_geometry():
    pts = points()
    n = 40
    pt_index = {p: i for i, p in enumerate(pts)}
    adj = [[False]*n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [frozenset(q) for q in combinations(range(n), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    assert len(lines) == 40
    line_sets = [set(l) for l in lines]
    line_key_index = {tuple(sorted(l)): i for i, l in enumerate(lines)}
    skew = [(i, j) for i, j in combinations(range(40), 2)
            if not (line_sets[i] & line_sets[j])]
    assert len(skew) == 540
    pair_to_skew = -np.ones((40, 40), dtype=np.int16)
    for s, (i, j) in enumerate(skew):
        pair_to_skew[i, j] = pair_to_skew[j, i] = s
    skew_index = {frozenset(p): k for k, p in enumerate(skew)}
    return pts, pt_index, adj, lines, line_sets, line_key_index, skew, skew_index, pair_to_skew


def build_psp(pts, pt_index):
    n = len(pts)

    def transvection_perm(v):
        out = []
        for x in pts:
            w = symp(x, v)
            out.append(pt_index[canon(tuple(
                (x[k] + w * v[k]) % 3 for k in range(4)))])
        return tuple(out)

    # Eight transvections are enough here; this keeps the verifier fast while
    # still generating the full order-25920 PSp(4,3).
    seed_vectors = [
        canon((1, 0, 0, 0)), canon((0, 1, 0, 0)),
        canon((0, 0, 1, 0)), canon((0, 0, 0, 1)),
        canon((1, 1, 0, 0)), canon((1, 0, 1, 0)),
        canon((1, 0, 0, 1)), canon((0, 1, 1, 0)),
    ]
    gens = [transvection_perm(v) for v in seed_vectors]
    ident = tuple(range(n))
    group = {ident}
    frontier = [ident]
    while frontier:
        nxt = []
        for g in frontier:
            for h in gens:
                gh = compose(h, g)
                if gh not in group:
                    group.add(gh)
                    nxt.append(gh)
        frontier = nxt
    assert len(group) == 25920
    return list(group)


def line_perm(g, lines, line_key_index):
    out = np.empty(40, dtype=np.int16)
    for li, line in enumerate(lines):
        out[li] = line_key_index[tuple(sorted(g[x] for x in line))]
    return out


def build_web(skew, skew_index, line_sets):
    web = nx.Graph()
    web.add_nodes_from(range(540))
    for (i, j) in skew:
        tv = [k for k in range(40)
              if k != i and k != j
              and line_sets[k] & line_sets[i] and line_sets[k] & line_sets[j]]
        for a, b in combinations(tv, 2):
            if not (line_sets[a] & line_sets[b]):
                web.add_edge(skew_index[frozenset((i, j))],
                             skew_index[frozenset((a, b))])
    return web


def line_relation_to_base(t, base_a, base_b, line_sets):
    if t == base_a or t == base_b:
        return "equal"
    ma = bool(line_sets[t] & line_sets[base_a])
    mb = bool(line_sets[t] & line_sets[base_b])
    if ma and mb:
        return "transversal2"
    if ma or mb:
        return "one_side"
    return "zero_side"


def main():
    (pts, pt_index, adj, lines, line_sets, line_key_index,
     skew, skew_index, pair_to_skew) = build_geometry()
    psp = build_psp(pts, pt_index)
    web = build_web(skew, skew_index, line_sets)
    assert web.number_of_nodes() == 540 and web.number_of_edges() == 1620

    base = 0
    base_a, base_b = skew[base]
    skew_i = np.array([i for i, _ in skew], dtype=np.int16)
    skew_j = np.array([j for _, j in skew], dtype=np.int16)

    stabilizer_line_perms = []
    for g in psp:
        lp = line_perm(g, lines, line_key_index)
        if {int(lp[base_a]), int(lp[base_b])} == {base_a, base_b}:
            stabilizer_line_perms.append(lp)
    assert len(stabilizer_line_perms) == 48

    stab_skew_perms = []
    for lp in stabilizer_line_perms:
        stab_skew_perms.append(pair_to_skew[lp[skew_i], lp[skew_j]])

    seen = set()
    orbits = []
    for s in range(540):
        if s in seen:
            continue
        q = deque([s])
        seen.add(s)
        orb = []
        while q:
            x = q.popleft()
            orb.append(x)
            for perm in stab_skew_perms:
                y = int(perm[x])
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        orbits.append(sorted(orb))

    # Put the base orbit first, then sort by graph distance and size.
    dist = nx.single_source_shortest_path_length(web, base)
    orbits.sort(key=lambda o: (0 if base in o else 1,
                               min(dist[x] for x in o), len(o), min(o)))
    orbit_id = {}
    for oi, orb in enumerate(orbits):
        for x in orb:
            orbit_id[x] = oi

    # Web quotient/intersection table: for a node in orbit i, how many web
    # neighbors land in orbit j?  Stabilizer transitivity makes this constant.
    quotient = []
    for orb in orbits:
        rep = orb[0]
        row = [0]*len(orbits)
        for nb in web.neighbors(rep):
            row[orbit_id[nb]] += 1
        quotient.append(row)

    orbit_rows = []
    for oi, orb in enumerate(orbits):
        rep = orb[0]
        ra, rb = skew[rep]
        rels = [line_relation_to_base(ra, base_a, base_b, line_sets),
                line_relation_to_base(rb, base_a, base_b, line_sets)]
        rel_counter = Counter(rels)
        point_overlap = len((line_sets[base_a] | line_sets[base_b]) &
                            (line_sets[ra] | line_sets[rb]))
        distance_profile = Counter(dist[x] for x in orb)
        target_union = line_sets[ra] | line_sets[rb]
        base_union = line_sets[base_a] | line_sets[base_b]
        orbit_rows.append({
            "orbit": oi,
            "size": len(orb),
            "representative_skew_pair": [int(ra), int(rb)],
            "web_distance_profile_from_base": dict(sorted(distance_profile.items())),
            "line_relation_multiset_to_base": dict(sorted(rel_counter.items())),
            "base_target_point_overlap": point_overlap,
            "target_union_size": len(target_union),
            "base_union_size": len(base_union),
            "web_neighbor_counts_to_orbits": {str(j): c for j, c in enumerate(quotient[oi]) if c},
        })

    shell_sizes = Counter(dist.values())
    orbit_size_profile = Counter(len(o) for o in orbits)
    adjacency_orbit = orbit_id[next(iter(web.neighbors(base)))]
    base_row = quotient[0]

    assert len(orbits) == 32
    assert sum(len(o) for o in orbits) == 540
    assert len(stabilizer_line_perms) == 48
    assert sum(base_row) == 6
    assert base_row[adjacency_orbit] == 6

    print("BT780 rank-32 suborbit atlas")
    print(f"group order: {len(psp)}")
    print(f"base stabilizer order: {len(stabilizer_line_perms)}")
    print(f"suborbits: {len(orbits)}")
    print(f"orbit size profile: {dict(sorted(orbit_size_profile.items()))}")
    print(f"web distance shells: {dict(sorted(shell_sizes.items()))}")
    print(f"web adjacency is orbit {adjacency_orbit} of size {len(orbits[adjacency_orbit])}")
    print("first 12 orbits:")
    for row in orbit_rows[:12]:
        print(f"  R{row['orbit']:02d}: size={row['size']:>2}, "
              f"dist={row['web_distance_profile_from_base']}, "
              f"rel={row['line_relation_multiset_to_base']}, "
              f"overlap={row['base_target_point_overlap']}")

    out = {
        "theorem": "BT780 rank-32 cube-web suborbit atlas",
        "group_order": len(psp),
        "base_chart": base,
        "base_skew_pair": [int(base_a), int(base_b)],
        "base_stabilizer_order": len(stabilizer_line_perms),
        "suborbit_count": len(orbits),
        "suborbit_sizes": [len(o) for o in orbits],
        "orbit_size_profile": dict(sorted(orbit_size_profile.items())),
        "web_distance_shells_from_base": dict(sorted(shell_sizes.items())),
        "web_adjacency_orbit": int(adjacency_orbit),
        "base_web_adjacency_row": {str(j): c for j, c in enumerate(base_row) if c},
        "orbits": orbit_rows,
        "web_quotient_matrix": quotient,
    }
    outpath = ROOT / "data" / "bt780_rank32_suborbit_atlas.json"
    outpath.parent.mkdir(exist_ok=True)
    with outpath.open("w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {outpath.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
