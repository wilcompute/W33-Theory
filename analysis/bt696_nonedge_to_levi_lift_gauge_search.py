#!/usr/bin/env python3
"""
BT696 — Nonedge-to-Levi lift gauge search.

For a W33 nonedge {x,y}, there are mu=4 common centers c.  Each choice c gives
an incidence-path lift in the point-line Levi graph:

    x -- line(x,c) -- c -- line(c,y) -- y.

A local K33 rectangle has four nonedges.  We search all 4^4 center-gauge
assignments and ask when the mod-2 sum of the four Levi paths is a simple Levi
8-cycle.

Result:
  * every local K33 rectangle has exactly 24 valid gauge assignments;
  * 2160 centered rectangles * 24 = 51840 valid presentations;
  * these collapse onto exactly 1620 unique Levi 8-cycles;
  * every Levi 8-cycle occurs with multiplicity 32.

This is the missing lift functor boundary from BT694, now resolved at the
presentation level.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import defaultdict, Counter


def inv3(a: int) -> int:
    a %= 3
    if a == 1:
        return 1
    if a == 2:
        return 2
    raise ZeroDivisionError


def canon(v):
    for x in v:
        if x % 3:
            c = inv3(x)
            return tuple((c*y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a,b,c,d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a,b,c,d) != (0,0,0,0)
    })


def symp(x,y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False]*40 for _ in range(40)]
    for i,j in combinations(range(40),2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [tuple(q) for q in combinations(range(40),4)
             if all(adj[i][j] for i,j in combinations(q,2))]
    through = defaultdict(list)
    edge_line = {}
    for li,line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a,b in combinations(line,2):
            edge_line[tuple(sorted((a,b)))] = li
    centers = {}
    for x,y in combinations(range(40),2):
        if not adj[x][y]:
            cs = [c for c in range(40) if adj[x][c] and adj[y][c]]
            assert len(cs) == 4
            centers[tuple(sorted((x,y)))] = cs
    return adj, lines, through, edge_line, centers


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x,c)))]
    lcy = edge_line[tuple(sorted((c,y)))]
    # Levi edges are flags (point,line).
    return [(x,lxc), (c,lxc), (c,lcy), (y,lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e,v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set):
    if len(edge_set) != 8:
        return False
    deg = Counter()
    graph = defaultdict(list)
    for p, li in edge_set:
        a = ("p", p)
        b = ("l", li)
        deg[a] += 1
        deg[b] += 1
        graph[a].append(b)
        graph[b].append(a)
    if len(deg) != 8:
        return False
    if any(d != 2 for d in deg.values()):
        return False
    start = next(iter(deg))
    seen = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == 8


def main() -> None:
    adj, lines, through, edge_line, centers = build()
    rectangle_count = 0
    valid_presentations = 0
    valid_per_rectangle = Counter()
    unique_cycles = Counter()

    for c in range(40):
        for li, lj in combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]),
                        (aa[1], bb[0]),
                        (aa[1], bb[1]),
                        (aa[0], bb[1]),
                    ]]
                    assert all(not adj[x][y] for x,y in rect_edges)
                    count = 0
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g, edge_line)
                                 for (x,y), g in zip(rect_edges, gauges)]
                        cycle = xor_path_edges(paths)
                        if is_simple_levi_8_cycle(cycle):
                            count += 1
                            unique_cycles[cycle] += 1
                    rectangle_count += 1
                    valid_presentations += count
                    valid_per_rectangle[count] += 1

    assert rectangle_count == 2160
    assert valid_per_rectangle == Counter({24:2160})
    assert valid_presentations == 2160*24 == 51840
    assert len(unique_cycles) == 1620
    assert Counter(unique_cycles.values()) == Counter({32:1620})

    print("BT696 nonedge-to-Levi lift gauge search: PASS")
    print("centered_k33_rectangles=2160")
    print("valid_lifts_per_rectangle=24")
    print("valid_lift_presentations=51840")
    print("unique_levi_8_cycles=1620")
    print("presentations_per_levi_8_cycle=32")
    print("identity=2160*24=51840=1620*32")
    print("interpretation=local K33 rectangles lift to Levi H1 via 24 center-gauge presentations")


if __name__ == "__main__":
    main()
