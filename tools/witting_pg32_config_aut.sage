#!/usr/bin/env sage
"""
Compute automorphism group of the 14-point/16-line configuration.

We build the bipartite incidence graph between the 14 covered PG(3,2) points
and the 16 hit lines derived from Witting ray trace images, then compute
Aut(G) and basic orbit data.

Outputs:
- artifacts/witting_pg32_config_aut.json
- artifacts/witting_pg32_config_aut.md
"""
from sage.all import *
import json
from itertools import combinations, product
from datetime import datetime

out_json = "artifacts/witting_pg32_config_aut.json"
out_md = "artifacts/witting_pg32_config_aut.md"

# GF(4) arithmetic (same encoding: 0,1,ω,ω^2 -> 0,1,2,3)
def gf4_add(a, b):
    return a ^ b

def gf4_mul(a, b):
    if a == 0 or b == 0:
        return 0
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    c0 = a0 * b0
    c1 = a0 * b1 + a1 * b0
    c2 = a1 * b1
    c0 = (c0 + c2) % 2
    c1 = (c1 + c2) % 2
    return (c1 << 1) | c0

def gf4_square(a):
    return gf4_mul(a, a)

def gf4_trace(a):
    return gf4_add(a, gf4_square(a)) & 1

def gf4_inv(a):
    if a == 0:
        raise ZeroDivisionError
    for b in [1, 2, 3]:
        if gf4_mul(a, b) == 1:
            return b
    raise ZeroDivisionError

omega = 2
omega2 = 3
omega_powers = [1, omega, omega2]

def build_base_states():
    states = []
    for i in range(4):
        v = [0, 0, 0, 0]
        v[i] = 1
        states.append(tuple(v))
    for mu, nu in product(range(3), repeat=2):
        w_mu = omega_powers[mu]
        w_nu = omega_powers[nu]
        states.append((0, 1, w_mu, w_nu))
        states.append((1, 0, w_mu, w_nu))
        states.append((1, w_mu, 0, w_nu))
        states.append((1, w_mu, w_nu, 0))
    return states

def normalize_projective(v):
    for x in v:
        if x != 0:
            inv = gf4_inv(x)
            return tuple(gf4_mul(inv, xi) for xi in v)
    return None

def trace_map(v):
    return tuple(gf4_trace(x) for x in v)

def build_pg32_points():
    return [v for v in product([0, 1], repeat=4) if v != (0, 0, 0, 0)]

def build_pg32_lines(points):
    lines = set()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p = points[i]
            q = points[j]
            r = tuple((pi ^ qi) for pi, qi in zip(p, q))
            line = tuple(sorted([p, q, r]))
            lines.add(line)
    return sorted(lines)

base_states = [normalize_projective(s) for s in build_base_states()]
base_states = list(dict.fromkeys(base_states))
scalars = [1, omega, omega2]
ray_images = []
for s in base_states:
    imgs = set()
    for c in scalars:
        scaled = tuple(gf4_mul(c, x) for x in s)
        p = trace_map(scaled)
        if p != (0, 0, 0, 0):
            imgs.add(p)
    ray_images.append(tuple(sorted(imgs)))

pg_points = build_pg32_points()
pg_lines = build_pg32_lines(pg_points)
pg_line_set = {tuple(sorted(line)) for line in pg_lines}

hit_lines = sorted(set(tuple(im) for im in ray_images if len(im) == 3 and tuple(im) in pg_line_set))
covered_points = sorted(set(p for line in hit_lines for p in line))

# bipartite incidence graph
P = len(covered_points)
L = len(hit_lines)
point_labels = [f"P{i}" for i in range(P)]
line_labels = [f"L{j}" for j in range(L)]
idx_point = {p: i for i, p in enumerate(covered_points)}

edges = []
for j, line in enumerate(hit_lines):
    for p in line:
        if p in idx_point:
            edges.append((point_labels[idx_point[p]], line_labels[j]))

G = Graph()
G.add_vertices(point_labels + line_labels)
G.add_edges(edges)

aut = G.automorphism_group(partition=[point_labels, line_labels])
aut_order = aut.order()

# Full automorphism group (allowing potential point/line swaps)
aut_full = G.automorphism_group()
aut_full_order = aut_full.order()

# orbits on points and lines (partition-preserving)
all_orbits = aut.orbits()
point_label_set = set(point_labels)
line_label_set = set(line_labels)
point_orbits = [orb for orb in all_orbits if set(orb).issubset(point_label_set)]
line_orbits = [orb for orb in all_orbits if set(orb).issubset(line_label_set)]

# Check whether any full-group orbit mixes points and lines
full_orbits = aut_full.orbits()
full_mixed = any((set(orb) & point_label_set) and (set(orb) & line_label_set) for orb in full_orbits)

results = {
    "timestamp": datetime.now().isoformat(),
    "points": P,
    "lines": L,
    "aut_order": int(aut_order),
    "aut_order_full": int(aut_full_order),
    "full_orbit_mixed_points_lines": bool(full_mixed),
    "point_orbit_sizes": sorted([len(o) for o in point_orbits]),
    "line_orbit_sizes": sorted([len(o) for o in line_orbits]),
}

import os
os.makedirs("artifacts", exist_ok=True)
with open(out_json, "w") as f:
    json.dump(results, f, indent=2)

lines_out = []
lines_out.append("# 14-Point / 16-Line Configuration Automorphisms")
lines_out.append("")
lines_out.append(f"Generated: {results['timestamp']}")
lines_out.append(f"- points: {results['points']}")
lines_out.append(f"- lines: {results['lines']}")
lines_out.append(f"- |Aut|: {results['aut_order']}")
lines_out.append(f"- |Aut| (full): {results['aut_order_full']}")
lines_out.append(f"- full group mixes points/lines: {results['full_orbit_mixed_points_lines']}")
lines_out.append(f"- point orbit sizes: {results['point_orbit_sizes']}")
lines_out.append(f"- line orbit sizes: {results['line_orbit_sizes']}")

with open(out_md, "w") as f:
    f.write("\n".join(lines_out) + "\n")

print(f"Wrote {out_json}")
print(f"Wrote {out_md}")
