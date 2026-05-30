#!/usr/bin/env python3
"""Symplectic structure on the PG(5,3) -> W33 projection fibers.

Projection theorem before this file:
    PG(5,3) has 364 points and projects to PG(3,3)=W33 with
    40 fibers of size 9 plus a kernel PG(1,3) of size 4.

This verifier adds the 3-qutrit symplectic form.  Each 9-point affine fiber over
a W33 anchor is F3^2.  Its internal commuting graph is four qutrit lines through
the affine zero:

    9 vertices, 12 edges, degree distribution {8:1, 2:8}.

Equivalently, it is four triangles sharing the same central point.  The 4 kernel
points are exactly the four projective directions of that affine plane; each
kernel direction selects one 3-point affine line in every fiber.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

q = 3
base_dim = 4
tail_dim = 2


def normalize(v):
    v = tuple(x % q for x in v)
    if not any(v):
        raise ValueError("zero")
    i = next(i for i, x in enumerate(v) if x)
    inv = 1 if v[i] == 1 else 2
    return tuple((inv * x) % q for x in v)


def pg_points(dim):
    return sorted({normalize(v) for v in itertools.product(range(q), repeat=dim) if any(v)})


def symp2(a, b):
    return (a[0] * b[1] - a[1] * b[0]) % q


def symp4(a, b):
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q


def symp6(a, b):
    return (symp4(a[:4], b[:4]) + symp2(a[4:], b[4:])) % q


def project_to_base(p):
    head = p[:4]
    if not any(head):
        return None
    return normalize(head)


def fiber_coordinate(p):
    """Return tail coordinate after normalizing head to the standard base representative."""
    head = p[:4]
    i = next(i for i, x in enumerate(head) if x)
    inv = 1 if head[i] == 1 else 2
    return tuple((inv * x) % q for x in p[4:])


def affine_line_through_zero(direction):
    d = normalize(direction)
    return {((a * d[0]) % q, (a * d[1]) % q) for a in range(q)}


def build_payload():
    pts6 = pg_points(6)
    base_pts = pg_points(4)
    kernel = [p for p in pts6 if project_to_base(p) is None]
    fibers = defaultdict(list)
    for p in pts6:
        b = project_to_base(p)
        if b is not None:
            fibers[b].append(p)

    sample_base = base_pts[0]
    sample = fibers[sample_base]
    coords = {p: fiber_coordinate(p) for p in sample}
    internal_edges = []
    for a, b in itertools.combinations(sample, 2):
        if symp6(a, b) == 0:
            internal_edges.append((a, b))
    internal_degree = Counter()
    for a, b in internal_edges:
        internal_degree[coords[a]] += 1
        internal_degree[coords[b]] += 1

    directions = [k[4:] for k in kernel]
    direction_lines = {normalize(d): affine_line_through_zero(d) for d in directions}
    line_sizes = Counter(len(line) for line in direction_lines.values())
    nonzero_hits = Counter()
    for line in direction_lines.values():
        for x in line:
            if x != (0, 0):
                nonzero_hits[x] += 1

    kernel_selection_counts = Counter()
    for k in kernel:
        for p in pts6:
            if project_to_base(p) is not None and symp6(k, p) == 0:
                kernel_selection_counts[k] += 1

    # Cross-fiber pair counts depend only on base symplectic relation.
    base_adj_counts = Counter()
    cross_counts = Counter()
    for b1, b2 in itertools.combinations(base_pts, 2):
        base_rel = symp4(b1, b2)
        key = "base_commuting" if base_rel == 0 else "base_noncommuting"
        base_adj_counts[key] += 1
        c = 0
        for p in fibers[b1]:
            for r in fibers[b2]:
                if symp6(p, r) == 0:
                    c += 1
        cross_counts[(key, c)] += 1

    identities = {
        "PG5_points_364": len(pts6) == 364,
        "base_points_40": len(base_pts) == 40,
        "kernel_points_4": len(kernel) == 4,
        "forty_fibers_size_9": len(fibers) == 40 and {len(v) for v in fibers.values()} == {9},
        "sample_internal_edges_12": len(internal_edges) == 12,
        "sample_degree_distribution_center8_others2": Counter(internal_degree.values()) == {8: 1, 2: 8},
        "four_kernel_directions": len(direction_lines) == 4,
        "each_direction_line_size_3": line_sizes == {3: 4},
        "nonzero_fiber_points_partitioned_by_directions": len(nonzero_hits) == 8 and set(nonzero_hits.values()) == {1},
        "zero_in_all_four_direction_lines": all((0, 0) in line for line in direction_lines.values()),
        "each_kernel_direction_selects_3_points_per_fiber": set(kernel_selection_counts.values()) == {120},
        "base_pair_counts_240_540": base_adj_counts == {"base_commuting": 240, "base_noncommuting": 540},
        "cross_fiber_commuting_counts": cross_counts == {("base_commuting", 33): 240, ("base_noncommuting", 24): 540},
    }
    return {
        "theorem": "symplectic_projection_fiber_lines",
        "projection": "PG(5,3) -> PG(3,3)=W33 with 40 affine 9-fibers plus PG(1,3) kernel",
        "fiber_geometry": {
            "sample_base": sample_base,
            "fiber_size": len(sample),
            "internal_edges": len(internal_edges),
            "degree_distribution": dict(Counter(internal_degree.values())),
            "description": "four qutrit affine lines through the zero coordinate; equivalently four triangles sharing one center",
        },
        "kernel_direction_geometry": {
            "kernel_points": len(kernel),
            "direction_lines": {str(k): sorted(list(v)) for k, v in direction_lines.items()},
            "kernel_selection_counts": {str(k): v for k, v in kernel_selection_counts.items()},
            "description": "each kernel point is a direction at infinity and selects one 3-point affine line in each of the 40 fibers",
        },
        "cross_fiber_commutation": {
            "base_pair_counts": dict(base_adj_counts),
            "commuting_pair_counts_between_fibers": {str(k): v for k, v in cross_counts.items()},
            "description": "commuting base anchors have 33 commuting fiber pairs; noncommuting base anchors have 24",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main():
    payload = build_payload()
    out = Path("data/w33_symplectic_projection_fiber_lines.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
