#!/usr/bin/env python3
"""
BT743 - Homological code from selected Levi faces.

BT741 glued the 240 local K33 registers along shared selected cycles and
found the flat mask-1110 bundle yields a global F2^4 register.  BT743 asks
the dual, topological question: attach the selected Levi 8-cycles as 2-FACES
to the Levi graph and compute mod-2 homology

    C2 = F2^faces --d2--> C1 = F2^160 --d1--> C0 = F2^80,
    H1 = ker d1 / im d2,   dim H1 = 81 - rank_F2(d2),
    H2 = ker d2,           dim H2 = #faces - rank_F2(d2).

H1 is the logical space of the homological (CSS-type) quantum code with
X-checks = Levi vertices and Z-checks = selected faces.  The question:
does the flat bundle's H1 equal the BT741 global register dimension 4?

Families tested:
  * all 1620 Levi 8-cycles                  (full correspondence)
  * mask-1110 bundle (1306 distinct cycles) (BT741 flat)
  * BT718 sheet (710 distinct cycles)
  * every single-mask bundle
  * each channel sheet of mask 1110
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json


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
            return tuple((c * y) % 3 for y in v)
    raise ValueError("zero vector")


def points():
    return sorted({
        canon((a, b, c, d))
        for a in range(3) for b in range(3) for c in range(3) for d in range(3)
        if (a, b, c, d) != (0, 0, 0, 0)
    })


def symp(x, y) -> int:
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build():
    pts = points()
    adj = [[False] * 40 for _ in range(40)]
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i][j] = adj[j][i] = True
    lines = [tuple(q) for q in combinations(range(40), 4)
             if all(adj[i][j] for i, j in combinations(q, 2))]
    through = defaultdict(list)
    edge_line = {}
    for li, line in enumerate(lines):
        for p in line:
            through[p].append(li)
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li
    centers = {}
    for x, y in combinations(range(40), 2):
        if not adj[x][y]:
            cs = tuple(sorted(c for c in range(40) if adj[x][c] and adj[y][c]))
            centers[tuple(sorted((x, y)))] = cs
    flags = sorted((p, li) for li, line in enumerate(lines) for p in line)
    flag_idx = {f: i for i, f in enumerate(flags)}
    return adj, lines, through, edge_line, centers, flag_idx


def path_edges(x, y, c, edge_line):
    lxc = edge_line[tuple(sorted((x, c)))]
    lcy = edge_line[tuple(sorted((c, y)))]
    return [(x, lxc), (c, lxc), (c, lcy), (y, lcy)]


def xor_path_edges(paths):
    cnt = Counter()
    for path in paths:
        for e in path:
            cnt[e] ^= 1
    return frozenset(e for e, v in cnt.items() if v)


def is_simple_levi_8_cycle(edge_set) -> bool:
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
    if len(deg) != 8 or any(d != 2 for d in deg.values()):
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


def gf2_rank(rows) -> int:
    pivots = []
    rank = 0
    for r in rows:
        for p in pivots:
            r = min(r, r ^ p)
        if r:
            pivots.append(r)
            pivots.sort(reverse=True)
            rank += 1
    return rank


def main() -> None:
    adj, lines, through, edge_line, centers, flag_idx = build()

    all_masks = [
        (1,1,1,0), (1,1,0,1), (1,0,1,1), (0,1,1,1),
        (1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1),
    ]
    sheet_cycles = defaultdict(set)
    for p in range(40):
        for li, lj in combinations(through[p], 2):
            A = tuple(sorted(set(lines[li]) - {p}))
            B = tuple(sorted(set(lines[lj]) - {p}))
            for aa in combinations(A, 2):
                for bb in combinations(B, 2):
                    rect_edges = [tuple(sorted(e)) for e in [
                        (aa[0], bb[0]), (aa[1], bb[0]),
                        (aa[1], bb[1]), (aa[0], bb[1]),
                    ]]
                    per_mask = defaultdict(list)
                    for gauges in product(*(centers[e] for e in rect_edges)):
                        paths = [path_edges(x, y, g, edge_line)
                                 for (x, y), g in zip(rect_edges, gauges)]
                        cycle = xor_path_edges(paths)
                        if is_simple_levi_8_cycle(cycle):
                            mask = tuple(1 if g == p else 0 for g in gauges)
                            per_mask[mask].append(cycle)
                    for mask in all_masks:
                        cycles3 = sorted(per_mask[mask],
                                         key=lambda c: tuple(sorted(c)))
                        for ch, cyc in enumerate(cycles3):
                            sheet_cycles[(mask, ch)].add(cyc)

    def face_vec(cycle):
        v = 0
        for f in cycle:
            v |= 1 << flag_idx[f]
        return v

    def homology(cycles):
        rows = [face_vec(c) for c in cycles]
        r = gf2_rank(rows)
        h1 = 81 - r
        h2 = len(rows) - r
        return len(rows), r, h1, h2

    results = {}

    def report(name, cycles):
        nf, r, h1, h2 = homology(cycles)
        print(f"{name:38s} faces={nf:5d} rank={r:3d} H1={h1:3d} H2={h2:5d}")
        results[name] = dict(faces=nf, rank=r, H1=h1, H2=h2)

    print("BT743 - homological code from selected Levi faces")
    print("=" * 70)
    print("Levi graph: 80 vertices, 160 edges, beta1 = 81 (F2 cycle space)")
    print()

    all_cycles = set()
    for key in sheet_cycles:
        all_cycles |= sheet_cycles[key]
    report("all 1620 Levi 8-cycles", all_cycles)

    bundle_1110 = set()
    for ch in range(3):
        bundle_1110 |= sheet_cycles[((1,1,1,0), ch)]
    report("mask 1110 bundle (BT741 flat)", bundle_1110)

    report("BT718 sheet (1110, ch0)", sheet_cycles[((1,1,1,0), 0)])
    report("sheet (1110, ch1)", sheet_cycles[((1,1,1,0), 1)])
    report("sheet (1110, ch2)", sheet_cycles[((1,1,1,0), 2)])

    for m in all_masks:
        b = set()
        for ch in range(3):
            b |= sheet_cycles[(m, ch)]
        report(f"mask {''.join(map(str, m))} bundle", b)

    with open("data/bt743_selected_face_homological_code.json", "w") as f:
        json.dump({
            "theorem": "BT743 homological code from selected Levi faces",
            "levi": dict(vertices=80, edges=160, beta1=81),
            **results,
        }, f, indent=2)
    print("\nwrote data/bt743_selected_face_homological_code.json")


if __name__ == "__main__":
    main()
