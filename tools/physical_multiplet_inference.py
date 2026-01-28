#!/usr/bin/env python3
"""Infer pattern‑class correlations with v23 parity/centers/holonomy via Q45 mapping.

Pipeline:
1) Load W33 rays (complex) and build collinearity via inner product.
2) Enumerate K4 components in z4_analysis order.
3) Load q45_quantum_numbers.csv (q45 vertex -> k4_u,k4_v).
4) Map each Q45 vertex to a pattern‑class signature from its two K4s.
5) Load v23 triangles (Q45 indices + parity, centers, holonomy).
6) Aggregate parity/center/holonomy statistics per pattern class.

Outputs artifacts/physical_multiplet_inference.json
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RAYS_CSV = ROOT / "data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
Q45_CSV = ROOT / "data/q45_quantum_numbers.csv"
V23_CSV = ROOT / "data/_v23/v23/Q_triangles_with_centers_Z2_S3_fiber6.csv"


def load_rays():
    V = [[0j]*4 for _ in range(40)]
    with open(RAYS_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = int(row['point_id'])
            for i in range(4):
                V[pid][i] = complex(str(row[f'v{i}']).replace(' ', ''))
    return V


def collinearity(V):
    col = [[0]*40 for _ in range(40)]
    for i in range(40):
        for j in range(i+1, 40):
            inner = sum((V[i][k].conjugate()*V[j][k] for k in range(4)))
            if abs(inner) < 1e-6:
                col[i][j] = col[j][i] = 1
    return col


def compute_k4_components(col):
    k4s = []
    n = 40
    for a in range(n):
        for b in range(a+1, n):
            if col[a][b]:
                continue
            for c in range(b+1, n):
                if col[a][c] or col[b][c]:
                    continue
                for d in range(c+1, n):
                    if col[a][d] or col[b][d] or col[c][d]:
                        continue
                    # common neighbors
                    common = []
                    for p in range(n):
                        if p in (a,b,c,d):
                            continue
                        if col[a][p] and col[b][p] and col[c][p] and col[d][p]:
                            common.append(p)
                    if len(common) == 4:
                        k4s.append((tuple(sorted([a,b,c,d])), tuple(sorted(common))))
    return k4s


def pattern_class_by_vertex():
    inter = json.loads((ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text())
    orbit_map = json.loads((ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text())
    mapping = orbit_map["mapping"]

    patterns = [tuple(row) for row in inter["matrix"]]
    pat_ids = {}
    for row in patterns:
        if row not in pat_ids:
            pat_ids[row] = len(pat_ids)

    orbit_class = {i: pat_ids[patterns[i]] for i in range(40)}
    point_to_orbit = {tuple(v): int(k) for k, v in mapping.items()}

    # build points in standard order
    F3 = [0,1,2]
    points=[]; seen=set()
    for v in product(F3, repeat=4):
        if all(x==0 for x in v):
            continue
        v=list(v)
        for i in range(4):
            if v[i]!=0:
                inv=1 if v[i]==1 else 2
                v=tuple((x*inv)%3 for x in v)
                break
        if v not in seen:
            seen.add(v); points.append(v)

    class_by_vertex=[]
    for p in points:
        oid = point_to_orbit[p]
        class_by_vertex.append(orbit_class[oid])
    return class_by_vertex


def load_q45_mapping():
    q45 = {}
    with open(Q45_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = int(row['q45_vertex'])
            q45[q] = (int(row['k4_u']), int(row['k4_v']))
    return q45


def load_v23_triangles():
    tris = []
    with open(V23_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tris.append({
                'u': int(row['u']),
                'v': int(row['v']),
                'w': int(row['w']),
                'centers': int(row['centers']),
                'z2_parity': int(row['z2_parity']),
                'fiber6_cycle_type': row['fiber6_cycle_type'],
            })
    return tris


def main():
    V = load_rays()
    col = collinearity(V)
    k4s = compute_k4_components(col)
    class_by_vertex = pattern_class_by_vertex()

    # Build K4 -> class multiset signature
    k4_sig = []
    for outer, center in k4s:
        cls = [class_by_vertex[v] for v in outer] + [class_by_vertex[v] for v in center]
        k4_sig.append(tuple(sorted(cls)))

    # Q45 mapping
    q45 = load_q45_mapping()
    q45_sig = {}
    for q, (u, v) in q45.items():
        sig = tuple(sorted(k4_sig[u] + k4_sig[v]))
        q45_sig[q] = sig

    # V23 triangles
    tris = load_v23_triangles()

    # Aggregate parity/center/holonomy stats per pattern class
    class_parity = defaultdict(Counter)
    class_centers = defaultdict(Counter)
    class_fiber = defaultdict(Counter)

    for t in tris:
        qvs = [t['u'], t['v'], t['w']]
        parity = t['z2_parity']
        centers = t['centers']
        ftype = t['fiber6_cycle_type']
        for q in qvs:
            sig = q45_sig.get(q)
            if sig is None:
                continue
            for c in sig:
                class_parity[c][parity] += 1
                class_centers[c][centers] += 1
                class_fiber[c][ftype] += 1

    out = {
        "k4_count": len(k4s),
        "q45_count": len(q45),
        "triangle_count": len(tris),
        "class_parity_counts": {str(k): dict(v) for k, v in class_parity.items()},
        "class_center_counts": {str(k): dict(v) for k, v in class_centers.items()},
        "class_fiber_counts": {str(k): dict(v) for k, v in class_fiber.items()},
    }

    (ROOT / "artifacts" / "physical_multiplet_inference.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/physical_multiplet_inference.json")


if __name__ == "__main__":
    main()
