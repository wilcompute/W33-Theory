#!/usr/bin/env python3
"""Find an explicit isomorphism between the balanced 27-root graph and Schlaefli skew graph.

Then transfer E/C/L labels to the balanced nodes and analyze distributions by Z3 phase
and by integral/half root type.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
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


def build_balanced_root_graph():
    points, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    bias = json.loads((ROOT / 'artifacts' / 'su3_phase_orbit_bias.json').read_text())
    balanced_orbit = None
    for k, v in bias['orbit_sums'].items():
        if v == {'0': 9, '1': 9, '2': 9} or v == {0: 9, 1: 9, 2: 9}:
            balanced_orbit = int(k.split('_')[1])
    if balanced_orbit is None:
        raise RuntimeError("No balanced orbit found")

    we6 = json.loads((ROOT / 'artifacts' / 'we6_orbit_labels.json').read_text())
    root_to_orbit = {eval(k): v for k, v in we6['mapping'].items()}
    edge_map = json.loads((ROOT / 'artifacts' / 'explicit_bijection_decomposition.json').read_text())
    edge_to_root_idx = {int(k): v for k, v in edge_map['edge_to_root_index'].items()}
    root_coords = [tuple(r) for r in edge_map['root_coords']]

    # Phase function
    def phase(v):
        return v[3] % 3

    # Collect balanced edges and associated roots
    bal_edges = []
    roots = []
    phases = []
    root_types = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info['orbit_size'] == 27 and info['orbit_id'] == balanced_orbit:
            bal_edges.append(e)
            roots.append(np.array([x / 2.0 for x in r], dtype=float))
            phases.append(int((phase(points[e[0]]) + phase(points[e[1]])) % 3))
            has_odd = any(abs(x) % 2 == 1 for x in r)
            root_types.append('half' if has_odd else 'integral')

    n = len(roots)
    adj = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            ip = float(np.dot(roots[i], roots[j]))
            if abs(ip - 1.0) < 1e-6:
                adj[i][j] = adj[j][i] = 1

    return adj, bal_edges, phases, root_types


def build_schlafli_skew():
    # Build Schlaefli lines
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
    # Precompute neighbor sets for quick checks
    neighA = [set(i for i in range(n) if adjA[v][i]) for v in range(n)]
    neighB = [set(i for i in range(n) if adjB[v][i]) for v in range(n)]

    # Order vertices by degree to break ties (all same), then by index
    order = list(range(n))

    mapping = {}
    used = set()

    def candidates(u):
        # Candidates in B not used and consistent with assigned neighbors
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

    # Anchor mapping: map u0=0 to v0=0
    mapping[0] = 0
    used.add(0)

    # Also anchor one neighbor to reduce symmetry
    u1 = next(iter(neighA[0]))
    for v1 in neighB[0]:
        mapping[u1] = v1
        used.add(v1)

        # Backtracking
        def backtrack():
            if len(mapping) == n:
                return True
            # choose next unassigned with most constraints (max assigned neighbors)
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
    adj_bal, bal_edges, phases, root_types = build_balanced_root_graph()
    adj_sch, lines = build_schlafli_skew()

    mapping = find_isomorphism(adj_bal, adj_sch)
    if mapping is None:
        print("No isomorphism found")
        return

    # Invert mapping: bal_node -> schlafli_line
    bal_to_line = {u: lines[v] for u, v in mapping.items()}

    # Distribution by line type and phase
    line_type_counts = Counter()
    phase_line_counts = defaultdict(Counter)
    root_line_counts = defaultdict(Counter)

    for u, line in bal_to_line.items():
        line_type = line[0]
        line_type_counts[line_type] += 1
        phase_line_counts[phases[u]][line_type] += 1
        root_line_counts[root_types[u]][line_type] += 1

    # Verify isomorphism
    ok = True
    for i in range(len(adj_bal)):
        for j in range(i+1, len(adj_bal)):
            if adj_bal[i][j] != adj_sch[mapping[i]][mapping[j]]:
                ok = False
                break
        if not ok:
            break

    results = {
        "line_type_counts": dict(line_type_counts),
        "phase_line_counts": {str(k): dict(v) for k, v in phase_line_counts.items()},
        "root_line_counts": {k: dict(v) for k, v in root_line_counts.items()},
        "mapping_sample": {str(k): bal_to_line[k] for k in sorted(bal_to_line.keys())[:10]},
        "isomorphism_verified": ok,
    }

    out_path = ROOT / 'artifacts' / 'balanced_orbit_schlafli_isomorphism.json'
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(results)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
