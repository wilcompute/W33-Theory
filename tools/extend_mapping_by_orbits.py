#!/usr/bin/env python3
"""Extend Schlaefli labeling across all six 27-orbits.

For each 27-orbit of E8 roots under W(E6), we:
  - build the root graph (ip=1)
  - verify SRG(27,16,10,8)
  - find a graph isomorphism to the Schlaefli skew graph
  - report phase/line-type/root-type distributions
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

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

    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i+1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def build_schlafli_skew():
    lines = []
    for i in range(1, 7):
        lines.append(('E', i))
    for i in range(1, 7):
        lines.append(('C', i))
    for i in range(1, 7):
        for j in range(i+1, 7):
            lines.append(('L', i, j))

    def intersect(L1, L2):
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
            return len(set(L1[1:]) & set(L2[1:])) == 0
        return False

    n = len(lines)
    adj_inter = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if intersect(lines[i], lines[j]):
                adj_inter[i][j] = adj_inter[j][i] = 1
    # Skew graph = complement
    adj_skew = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            adj_skew[i][j] = 1 - adj_inter[i][j]
    return adj_skew, lines


def find_isomorphism(adjA, adjB):
    n = len(adjA)
    neighA = [set(i for i in range(n) if adjA[v][i]) for v in range(n)]
    neighB = [set(i for i in range(n) if adjB[v][i]) for v in range(n)]

    order = list(range(n))
    mapping = {}
    used = set()

    def candidates(u):
        cand = []
        for v in range(n):
            if v in used:
                continue
            ok = True
            for u2, v2 in mapping.items():
                if (u2 in neighA[u]) != (v2 in neighB[v]):
                    ok = False
                    break
            if ok:
                cand.append(v)
        return cand

    mapping[0] = 0
    used.add(0)
    u1 = next(iter(neighA[0]))
    for v1 in neighB[0]:
        mapping[u1] = v1
        used.add(v1)

        def backtrack():
            if len(mapping) == n:
                return True
            unassigned = [u for u in order if u not in mapping]
            unassigned.sort(key=lambda u: -sum(1 for u2 in mapping if u2 in neighA[u]))
            u = unassigned[0]
            for v in candidates(u):
                mapping[u] = v
                used.add(v)
                if backtrack():
                    return True
                used.remove(v)
                del mapping[u]
            return False

        if backtrack():
            return mapping
        used.remove(v1)
        del mapping[u1]

    return None


def main():
    # W33 edge->root map
    points, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    # Phase function on edges
    def phase(v):
        return v[3] % 3

    edge_phase = {}
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        edge_phase[eidx] = int((phase(points[e[0]]) + phase(points[e[1]])) % 3)

    # Schlaefli skew graph
    sch_adj, lines = build_schlafli_skew()

    # Collect orbits of size 27
    orbits = defaultdict(list)
    for ridx, r in enumerate(root_coords):
        info = root_to_orbit.get(tuple(r))
        if info and info['orbit_size'] == 27:
            orbits[info['orbit_id']].append(ridx)

    orbit_results = {}
    for oid, rlist in sorted(orbits.items()):
        # Build root graph adjacency (ip=1)
        n = len(rlist)
        adj = [[0]*n for _ in range(n)]
        for i in range(n):
            ri = np.array(root_coords[rlist[i]], dtype=float) / 2.0
            for j in range(i+1, n):
                rj = np.array(root_coords[rlist[j]], dtype=float) / 2.0
                if abs(float(np.dot(ri, rj)) - 1.0) < 1e-6:
                    adj[i][j] = adj[j][i] = 1

        # SRG parameters
        degrees = [sum(row) for row in adj]
        k = degrees[0]
        lam = None
        mu = None
        lam_set = set()
        mu_set = set()
        for i in range(n):
            for j in range(i+1, n):
                common = sum(1 for t in range(n) if adj[i][t] and adj[j][t])
                if adj[i][j] == 1:
                    lam_set.add(common)
                else:
                    mu_set.add(common)
        lam = sorted(lam_set)
        mu = sorted(mu_set)

        # Isomorphism to Schlaefli skew graph
        mapping = find_isomorphism(adj, sch_adj)
        if mapping is None:
            orbit_results[oid] = {"srg": (n, k, lam, mu), "isomorphic": False}
            continue

        # Distributions by line type / phase / root type
        line_type_counts = Counter()
        phase_counts = Counter()
        phase_line_counts = defaultdict(Counter)
        root_type_counts = Counter()
        root_line_counts = defaultdict(Counter)

        for u in range(n):
            line = lines[mapping[u]]
            line_type_counts[line[0]] += 1

            ridx = rlist[u]
            # root type
            has_odd = any(abs(x) % 2 == 1 for x in root_coords[ridx])
            rtype = 'half' if has_odd else 'integral'
            root_type_counts[rtype] += 1
            root_line_counts[rtype][line[0]] += 1

            # phase from corresponding edge
            # map root to any edge index using edge_to_root_idx inverse
            # build inverse map once
        # Build inverse edge->root map
        root_to_edge = {}
        for eidx, ridx2 in edge_to_root_idx.items():
            root_to_edge[ridx2] = eidx
        for u in range(n):
            ridx = rlist[u]
            ph = edge_phase[root_to_edge[ridx]]
            phase_counts[ph] += 1
            line = lines[mapping[u]]
            phase_line_counts[ph][line[0]] += 1

        orbit_results[oid] = {
            "srg": (n, k, lam, mu),
            "isomorphic": True,
            "line_type_counts": dict(line_type_counts),
            "phase_counts": dict(phase_counts),
            "phase_line_counts": {str(k): dict(v) for k, v in phase_line_counts.items()},
            "root_type_counts": dict(root_type_counts),
            "root_line_counts": {k: dict(v) for k, v in root_line_counts.items()},
        }

    out_path = ROOT / 'artifacts' / 'schlafli_by_orbit.json'
    out_path.write_text(json.dumps(orbit_results, indent=2), encoding='utf-8')
    print(orbit_results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
