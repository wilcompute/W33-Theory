#!/usr/bin/env python3
"""Analyze the embedding of H27 into the Schläfli intersection graph.

Given an embedding, compute the removed edges (degree-2 leftover per vertex)
so that Schläfli intersection graph = H27 + disjoint 2-regular subgraph.
Report cycle decomposition of the leftover edges.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    n = len(proj_points)

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1

    return adj


def h27_from_w33(adj, v0=0):
    n = len(adj)
    non_neighbors = [j for j in range(n) if j != v0 and adj[v0][j] == 0]

    h_adj = [[0]*27 for _ in range(27)]
    for i, vi in enumerate(non_neighbors):
        for j, vj in enumerate(non_neighbors):
            if i < j and adj[vi][vj]:
                h_adj[i][j] = h_adj[j][i] = 1

    return h_adj


def build_27_lines():
    lines = []
    for i in range(1, 7):
        lines.append(('E', i))
    for i in range(1, 7):
        lines.append(('C', i))
    for i in range(1, 7):
        for j in range(i+1, 7):
            lines.append(('L', i, j))
    return lines


def lines_intersect(L1, L2):
    if L1 == L2:
        return False

    t1, t2 = L1[0], L2[0]

    if t1 == 'E' and t2 == 'E':
        return False
    if t1 == 'C' and t2 == 'C':
        return False

    if t1 == 'E' and t2 == 'C':
        return L1[1] != L2[1]
    if t1 == 'C' and t2 == 'E':
        return L1[1] != L2[1]

    if t1 == 'E' and t2 == 'L':
        return L1[1] in L2[1:]
    if t1 == 'L' and t2 == 'E':
        return L2[1] in L1[1:]

    if t1 == 'C' and t2 == 'L':
        return L1[1] in L2[1:]
    if t1 == 'L' and t2 == 'C':
        return L2[1] in L1[1:]

    if t1 == 'L' and t2 == 'L':
        s1 = set(L1[1:])
        s2 = set(L2[1:])
        return len(s1 & s2) == 0

    return False


def schlafli_intersection_graph():
    lines = build_27_lines()
    n = len(lines)
    adj = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(i+1, n):
            if lines_intersect(lines[i], lines[j]):
                adj[i][j] = adj[j][i] = 1

    return adj, lines


def load_embedding():
    path = ROOT / "artifacts" / "h27_in_schlafli_intersection.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("found_embedding"):
        return None
    mapping = {int(k): int(v) for k, v in data["mapping"].items()}
    return mapping


def cycle_decomposition(adj):
    n = len(adj)
    visited = [False]*n
    cycles = []

    for v in range(n):
        if visited[v]:
            continue
        # walk cycle
        cycle = [v]
        visited[v] = True
        # pick a neighbor
        neighbors = [u for u in range(n) if adj[v][u]]
        if not neighbors:
            cycles.append([v])
            continue
        prev = v
        cur = neighbors[0]
        while True:
            cycle.append(cur)
            visited[cur] = True
            nxts = [u for u in range(n) if adj[cur][u] and u != prev]
            if not nxts:
                break
            nxt = nxts[0]
            prev, cur = cur, nxt
            if cur == cycle[0]:
                break
        cycles.append(cycle)

    # normalize cycle lengths (ignore duplicates if traversal returns to start)
    cycle_lengths = []
    for c in cycles:
        # if closed, last repeats first
        if len(c) > 1 and c[-1] == c[0]:
            cycle_lengths.append(len(c)-1)
        else:
            cycle_lengths.append(len(c))
    return cycle_lengths, cycles


def main():
    mapping = load_embedding()
    if mapping is None:
        print("No embedding available.")
        return

    w33_adj = build_w33()
    h_adj = h27_from_w33(w33_adj, v0=0)
    s_adj, lines = schlafli_intersection_graph()

    # Build mapped H27 adjacency in Schläfli vertex labels
    n = 27
    mapped = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if h_adj[i][j]:
                a = mapping[i]
                b = mapping[j]
                mapped[a][b] = mapped[b][a] = 1

    # leftover edges = Schläfli intersection edges minus mapped H27 edges
    leftover = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if s_adj[i][j] and not mapped[i][j]:
                leftover[i][j] = leftover[j][i] = 1

    # degrees in leftover
    degs = [sum(row) for row in leftover]
    deg_set = sorted(set(degs))

    cycle_lengths, cycles = cycle_decomposition(leftover)
    cycle_labels = []
    for c in cycles:
        if len(c) > 1 and c[-1] == c[0]:
            c = c[:-1]
        cycle_labels.append([lines[v] for v in c])

    results = {
        "leftover_degree_set": deg_set,
        "leftover_edges": sum(sum(row) for row in leftover)//2,
        "cycle_lengths": sorted(cycle_lengths),
        "cycle_count": len(cycle_lengths),
        "cycle_labels": cycle_labels,
    }

    out_path = ROOT / "artifacts" / "h27_schlafli_leftover_cycles.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
