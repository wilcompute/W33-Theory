#!/usr/bin/env python3
"""Build the 2-qutrit Pauli commutation geometry and compare to W33.

Outputs:
- artifacts/qutrit_pauli_w33.json
- artifacts/qutrit_pauli_w33.md
"""
from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = ROOT / "artifacts" / "qutrit_pauli_w33.json"
OUT_MD = ROOT / "artifacts" / "qutrit_pauli_w33.md"

F3 = [0, 1, 2]


def symplectic(u, v):
    # u = (a1,b1,a2,b2), v = (c1,d1,c2,d2)
    a1, b1, a2, b2 = u
    c1, d1, c2, d2 = v
    return (a1 * d1 - b1 * c1 + a2 * d2 - b2 * c2) % 3


def normalize(v):
    # projective normalization: first nonzero -> 1
    for x in v:
        if x != 0:
            inv = pow(x, -1, 3)
            return tuple((xi * inv) % 3 for xi in v)
    return None


# Build projective points (nonzero vectors mod scalar)
points = []
seen = set()
for v in product(F3, repeat=4):
    if v == (0, 0, 0, 0):
        continue
    nv = normalize(v)
    if nv not in seen:
        seen.add(nv)
        points.append(nv)

# adjacency (commutation) graph
n = len(points)
edge_count = 0
adj = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(i + 1, n):
        if symplectic(points[i], points[j]) == 0:
            adj[i][j] = 1
            adj[j][i] = 1
            edge_count += 1

# compute SRG parameters
k_vals = [sum(adj[i]) for i in range(n)]
k = k_vals[0]

lambda_vals = set()
mu_vals = set()
for i in range(n):
    for j in range(i + 1, n):
        common = sum(1 for x in range(n) if adj[i][x] and adj[j][x])
        if adj[i][j]:
            lambda_vals.add(common)
        else:
            mu_vals.add(common)

# find lines: totally isotropic 2D subspaces
# For each commuting pair, compute its span and collect the projective points.
lines = set()
for i in range(n):
    for j in range(i + 1, n):
        if symplectic(points[i], points[j]) != 0:
            continue
        # span of two vectors in F3^4
        v1 = points[i]
        v2 = points[j]
        sub_pts = set()
        for a in F3:
            for b in F3:
                if a == 0 and b == 0:
                    continue
                v = tuple((a * v1[k] + b * v2[k]) % 3 for k in range(4))
                nv = normalize(v)
                sub_pts.add(nv)
        if len(sub_pts) > 1:
            lines.add(tuple(sorted(sub_pts)))

line_list = [tuple(l) for l in lines]

# compute lines per point
point_index = {p: idx for idx, p in enumerate(points)}
lines_per_point = [0] * n
for line in line_list:
    for p in line:
        lines_per_point[point_index[p]] += 1

# triangles count
triangles = 0
for i, j, k_idx in combinations(range(n), 3):
    if adj[i][j] and adj[i][k_idx] and adj[j][k_idx]:
        triangles += 1

summary = {
    "points": n,
    "edges": edge_count,
    "k": k,
    "lambda": sorted(lambda_vals),
    "mu": sorted(mu_vals),
    "lines": len(line_list),
    "line_sizes": sorted({len(l) for l in line_list}),
    "lines_per_point": sorted(set(lines_per_point)),
    "triangles": triangles,
}

OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

# Markdown summary
lines_md = []
lines_md.append("# 2-Qutrit Pauli Geometry vs W33")
lines_md.append("")
lines_md.append("Constructed projective points in F3^4 and used the symplectic form to model commutation.")
lines_md.append("")
lines_md.append(f"- points: {summary['points']}")
lines_md.append(f"- edges: {summary['edges']}")
lines_md.append(f"- degree k: {summary['k']}")
lines_md.append(f"- lambda: {summary['lambda']}")
lines_md.append(f"- mu: {summary['mu']}")
lines_md.append(f"- lines: {summary['lines']}")
lines_md.append(f"- line sizes: {summary['line_sizes']}")
lines_md.append(f"- lines per point: {summary['lines_per_point']}")
lines_md.append(f"- triangles: {summary['triangles']}")

OUT_MD.write_text("\n".join(lines_md) + "\n", encoding="utf-8")

print(f"Wrote {OUT_JSON}")
print(f"Wrote {OUT_MD}")
