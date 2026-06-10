#!/usr/bin/env python3
"""
BT699 — Canonical lift selector search.

BT696 proved that every local K33 rectangle has 24 valid center-gauge lifts to
Levi 8-cycles.  BT699 asks whether this 24-fold ambiguity has a canonical
selector from the already present square/orientation/Fano data.

Result:
  * for every one of the 2160 centered K33 rectangles, the 24 valid lifts split
    uniformly as 8 masks times 3 residual choices;
  * the eight masks are exactly the square-orientation masks
      1110, 1101, 1011, 0111, 1100, 1001, 0110, 0011
    in cyclic edge order;
  * each mask has exactly three valid residual choices;
  * therefore an orientation/D4 rule can reduce 24 -> 3, and a Fano-channel
    rule can reduce 3 -> 1, but no symmetry-free canonical selector is present.

Boundary:
  A lexicographic selector exists, but it is coordinate-label dependent and is
  not a geometric selector.
"""
from __future__ import annotations
from itertools import combinations, product
from collections import Counter, defaultdict


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
            centers[tuple(sorted((x,y)))] = tuple(sorted(cs))
    return adj, lines, through, edge_line, centers


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x,c)))]
    lcy = edge_line[tuple(sorted((c,y)))]
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


def valid_masks_for_rectangle(chart_center, rect_edges, centers, edge_line):
    mask_counts = Counter()
    lift_count = 0
    for gauges in product(*(centers[e] for e in rect_edges)):
        paths = [path_edges(x, y, g, edge_line)
                 for (x,y), g in zip(rect_edges, gauges)]
        cycle = xor_path_edges(paths)
        if is_simple_levi_8_cycle(cycle):
            lift_count += 1
            mask_counts[tuple(1 if g == chart_center else 0 for g in gauges)] += 1
    return lift_count, mask_counts


def main() -> None:
    adj, lines, through, edge_line, centers = build()
    expected_masks = {
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    }
    global_masks = Counter()
    rectangles = 0
    for c in range(40):
        for li, lj in combinations(through[c], 2):
            A = tuple(sorted(set(lines[li]) - {c}))
            B = tuple(sorted(set(lines[lj]) - {c}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    # Cyclic order: a0-b0, a1-b0, a1-b1, a0-b1.
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]),
                        (aa[1], bb[0]),
                        (aa[1], bb[1]),
                        (aa[0], bb[1]),
                    ]]
                    assert all(not adj[x][y] for x,y in rect_edges)
                    lift_count, mask_counts = valid_masks_for_rectangle(
                        c, rect_edges, centers, edge_line
                    )
                    assert lift_count == 24
                    assert set(mask_counts) == expected_masks
                    assert set(mask_counts.values()) == {3}
                    global_masks.update(mask_counts)
                    rectangles += 1

    assert rectangles == 2160
    assert sum(global_masks.values()) == 2160*24 == 51840
    assert all(global_masks[m] == 2160*3 for m in expected_masks)

    print("BT699 canonical lift selector search: PASS")
    print("rectangles=2160")
    print("valid_lifts_per_rectangle=24")
    print("mask_count_per_rectangle=8")
    print("residual_choices_per_mask=3")
    print("factorization=24=8*3")
    print("orientation_rule=24->3")
    print("fano_channel_rule=3->1")
    print("canonical_without_extra_gauge=False")
    print("lexicographic_selector_unique_but_coordinate_dependent=True")


if __name__ == "__main__":
    main()
