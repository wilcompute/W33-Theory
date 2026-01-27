#!/usr/bin/env python3
"""Sage: test whether each W33 line corresponds to a D4 root subsystem in E8.

Discovery idea:
- Use E8 Coxeter 6-orbits to map each W33 vertex to a 6-root orbit.
- A W33 line has 4 vertices => union of 4 orbits = 24 roots.
- Check if those 24 roots form a D4 root system (rank 4, closed under reflections).
"""
from __future__ import annotations

import json
from pathlib import Path
from itertools import product, combinations

from sage.all import Matrix, vector

ROOT = Path(__file__).resolve().parents[1]


def build_proj_points():
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
    return proj_points


def omega(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_lines(proj_points):
    idx = {p: i for i, p in enumerate(proj_points)}
    lines = set()
    n = len(proj_points)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) != 0:
                continue
            # span of i,j over F3
            pts = set()
            for a, b in product([0,1,2],[0,1,2]):
                if a == 0 and b == 0:
                    continue
                v = tuple((a*proj_points[i][k] + b*proj_points[j][k]) % 3 for k in range(4))
                # normalize projectively
                v = list(v)
                for t in range(4):
                    if v[t] != 0:
                        inv = 1 if v[t] == 1 else 2
                        v = tuple((x * inv) % 3 for x in v)
                        break
                pts.add(idx[v])
            if len(pts) == 4:
                lines.add(tuple(sorted(pts)))
    return sorted(lines)


def load_orbit_mapping():
    orb_map = json.loads(Path('artifacts/e8_orbit_to_f3_point.json').read_text())['mapping']
    # invert to point->orbit
    point_to_orbit = {tuple(v): int(k) for k, v in orb_map.items()}
    return point_to_orbit


def load_orbits():
    orbits = json.loads(Path('artifacts/e8_coxeter6_orbits.json').read_text())['orbits']
    return orbits


def is_d4_root_system(root_vecs):
    # root_vecs: list of sage vectors in R^8
    # check norm = 2
    for r in root_vecs:
        if (r * r) != 2:
            return False
    # rank
    M = Matrix(root_vecs)
    if M.rank() != 4:
        return False
    # closure under reflections
    root_set = {tuple(r) for r in root_vecs}
    for a in root_vecs:
        for b in root_vecs:
            ip = a * b
            if ip == 0:
                continue
            # reflection: b - (2*ip/(a*a)) * a ; but a*a=2 -> b - ip*a
            r = b - ip * a
            if tuple(r) not in root_set:
                return False
    return True


def main():
    proj_points = build_proj_points()
    lines = build_lines(proj_points)
    point_to_orbit = load_orbit_mapping()
    orbits = load_orbits()

    # map line -> root set
    line_results = []
    d4_count = 0
    rank_counts = {}

    for L in lines:
        # map each point to orbit
        orbs = [point_to_orbit[proj_points[i]] for i in L]
        roots = []
        for o in orbs:
            for r in orbits[o]:
                roots.append(vector(r))

        # inner product distribution within this 24-root set
        ip_counts = {}
        for i in range(len(roots)):
            for j in range(i+1, len(roots)):
                ip = int(roots[i] * roots[j])
                ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # compute rank of span
        M = Matrix(roots)
        rank = int(M.rank())
        rank_counts[rank] = rank_counts.get(rank, 0) + 1

        is_d4 = is_d4_root_system(roots)
        if is_d4:
            d4_count += 1
        line_results.append({
            "line": list(L),
            "orbits": orbs,
            "rank": rank,
            "ip_counts": ip_counts,
            "is_d4": bool(is_d4)
        })

    out = {
        "lines": len(lines),
        "d4_lines": d4_count,
        "rank_counts": rank_counts,
        "results": line_results
    }

    out_path = ROOT / "artifacts" / "w33_lines_to_d4.json"
    out_path.write_text(json.dumps(out, indent=2), encoding='utf-8')
    print("lines", len(lines), "d4_lines", d4_count)
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
