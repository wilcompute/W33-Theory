#!/usr/bin/env python3
"""
BT1807: Defect phase-plane transversal design theorem.

This witness extends the Pass 64/65 interrupt-controller line without relying on
seeded telemetry. It rebuilds W(3,3) from the symplectic form over F_3^4 and
proves that every defect center carries a rigid TD(4,3) escape surface:

  * the 27 safe non-neighbors split into 9 all-centers-in-perp triads;
  * the 9 unlit/cheap-target quads are transversals of the four star lines;
  * each neighbor appears in 3 quads; every cross-star pair appears once;
  * globally, cheap exits form a 3-fold cover of the 480 directed fabric edges.

So Pass 65's walking defect samples an exact design already written into the
interrupt vector table; the seed controls only the walk, not the escape geometry.
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

MOD = 3
OUT = Path("data/PART_BT1807_DEFECT_PHASE_PLANE_TRANSVERSAL_DESIGN_results.json")


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    """Projective normalization over F_3: first nonzero coordinate becomes 1."""
    for x in v:
        if x % MOD:
            inv = 1 if x % MOD == 1 else 2
            return tuple((inv * y) % MOD for y in v)
    raise ValueError("zero vector has no projective representative")


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    """Alternating form x1*y2-x2*y1+x3*y4-x4*y3 over F_3."""
    return (a[0] * b[1] - a[1] * b[0] + a[2] * b[3] - a[3] * b[2]) % MOD


def build_w33():
    pts: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for v in product(range(MOD), repeat=4):
        if v == (0, 0, 0, 0):
            continue
        n = normalize(v)
        if n not in seen:
            seen.add(n)
            pts.append(n)

    idx = {p: i for i, p in enumerate(pts)}
    n = len(pts)
    adj = [[i != j and symp(pts[i], pts[j]) == 0 for j in range(n)] for i in range(n)]

    lines: set[tuple[int, ...]] = set()
    for i, j in combinations(range(n), 2):
        if not adj[i][j]:
            continue
        line = set()
        for a, b in product(range(MOD), repeat=2):
            v = tuple((a * pts[i][k] + b * pts[j][k]) % MOD for k in range(4))
            if v != (0, 0, 0, 0):
                line.add(idx[normalize(v)])
        assert len(line) == 4
        lines.add(tuple(sorted(line)))
    return pts, adj, sorted(lines)


def star_lines(center: int, lines: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    groups = []
    for line in lines:
        if center in line:
            groups.append(tuple(x for x in line if x != center))
    return sorted(groups)


def vector_table(center: int, pts, adj):
    """Closed-form Pass-64 vector table at one defect center."""
    n = len(pts)
    neighbors = {j for j in range(n) if adj[center][j]}
    safe = sorted(set(range(n)) - neighbors - {center})
    rows = []
    for triad in combinations(safe, 3):
        if any(adj[a][b] for a, b in combinations(triad, 2)):
            continue
        quad = tuple(
            j for j in range(n)
            if all(symp(pts[j], pts[t]) == 0 for t in triad)
        )
        if len(quad) == 4 and set(quad).issubset(neighbors):
            lit = tuple(sorted(set(triad) | (neighbors - set(quad))))
            rows.append({"triad": tuple(sorted(triad)), "quad": tuple(sorted(quad)), "lit": lit})
    return sorted(rows, key=lambda row: (row["triad"], row["quad"])), neighbors, safe


def main() -> None:
    pts, adj, lines = build_w33()
    n = len(pts)
    degrees = [sum(row) for row in adj]
    undirected_edges = sum(sum(row) for row in adj) // 2

    assert n == 40
    assert len(lines) == 40
    assert set(degrees) == {12}
    assert undirected_edges == 240

    per_center = []
    directed_cheap: Counter[tuple[int, int]] = Counter()
    undirected_cheap: Counter[tuple[int, int]] = Counter()

    for center in range(n):
        rows, neighbors, safe = vector_table(center, pts, adj)
        groups = star_lines(center, lines)
        group_id = {x: gi for gi, group in enumerate(groups) for x in group}

        assert len(rows) == 9
        assert len(neighbors) == 12
        assert len(safe) == 27
        assert len(groups) == 4 and all(len(group) == 3 for group in groups)

        triad_cover = Counter(x for row in rows for x in row["triad"])
        quad_cover = Counter(x for row in rows for x in row["quad"])
        assert set(triad_cover) == set(safe)
        assert set(triad_cover.values()) == {1}
        assert set(quad_cover) == set(neighbors)
        assert set(quad_cover.values()) == {3}

        quad_intersections = Counter(
            len(set(a["quad"]) & set(b["quad"])) for a, b in combinations(rows, 2)
        )
        assert quad_intersections == Counter({1: 36})

        pair_counts: Counter[tuple[int, int]] = Counter()
        for row in rows:
            assert sorted(group_id[x] for x in row["quad"]) == [0, 1, 2, 3]
            assert not any(adj[a][b] for a, b in combinations(row["quad"], 2))
            for a, b in combinations(sorted(row["quad"]), 2):
                assert group_id[a] != group_id[b]
                pair_counts[(a, b)] += 1

        cross_pairs = 0
        same_star_pairs = 0
        for a, b in combinations(sorted(neighbors), 2):
            if group_id[a] == group_id[b]:
                same_star_pairs += 1
                assert pair_counts[(a, b)] == 0
            else:
                cross_pairs += 1
                assert pair_counts[(a, b)] == 1
        assert cross_pairs == 54
        assert same_star_pairs == 12

        for row in rows:
            for target in row["quad"]:
                assert adj[center][target]
                directed_cheap[(center, target)] += 1
                undirected_cheap[tuple(sorted((center, target)))] += 1

        per_center.append({
            "center": center,
            "ground_triad_count": len(rows),
            "safe_zone_size": len(safe),
            "neighbor_count": len(neighbors),
            "star_line_count": len(groups),
            "star_line_size_profile": sorted(len(group) for group in groups),
            "triad_replication_profile": sorted(Counter(triad_cover.values()).items()),
            "quad_replication_profile": sorted(Counter(quad_cover.values()).items()),
            "quad_intersection_profile": dict(sorted(quad_intersections.items())),
            "cross_star_neighbor_pairs_once": cross_pairs,
            "same_star_neighbor_pairs_zero": same_star_pairs,
        })

    directed_edges = [(i, j) for i in range(n) for j in range(n) if adj[i][j]]
    assert len(directed_edges) == 480
    assert len(directed_cheap) == 480
    assert set(directed_cheap.values()) == {3}
    assert len(undirected_cheap) == 240
    assert set(undirected_cheap.values()) == {6}

    summary = {
        "theorem": "BT1807 Defect Phase-Plane Transversal Design Theorem",
        "substrate": {
            "points": n,
            "lines": len(lines),
            "degree": degrees[0],
            "undirected_fabric_edges": undirected_edges,
            "directed_fabric_edges": len(directed_edges),
            "srg": [40, 12, 2, 4],
        },
        "local_law_per_defect_center": {
            "ground_triad_count": 9,
            "safe_non_neighbors_partitioned": 27,
            "star_neighbors": 12,
            "star_lines": 4,
            "star_line_size": 3,
            "cheap_quads": 9,
            "cheap_quad_size": 4,
            "quad_design": "TD(4,3): 4 star-line groups of size 3, 9 transversal blocks",
            "neighbor_replication_in_quads": 3,
            "quad_pair_intersection": 1,
            "cross_star_pairs": 54,
            "cross_star_pair_replication": 1,
            "same_star_pairs": 12,
            "same_star_pair_replication": 0,
        },
        "global_cheap_exit_cover": {
            "ground_vectors": 40 * 9,
            "cheap_directed_exits": 40 * 9 * 4,
            "directed_fabric_edges": 480,
            "directed_edge_cover_multiplicity": 3,
            "undirected_fabric_edges": 240,
            "undirected_edge_cover_multiplicity": 6,
            "identity": "40*9*4 = 1440 = 3*480 = 6*240",
        },
        "checks": {
            "all_40_centers_have_9_ground_triads": True,
            "all_safe_zones_partitioned_by_triads": True,
            "all_quad_blocks_are_star_transversals": True,
            "all_quad_blocks_are_independent": True,
            "all_cross_star_neighbor_pairs_once": True,
            "all_directed_edges_covered_three_times": True,
        },
        "per_center_first_three": per_center[:3],
        "honest_scope": (
            "Exact finite-geometric design witness. It strengthens the seeded walking-defect telemetry "
            "into a local/global incidence law, but it does not claim hardware timing, ergodicity, "
            "or physical noise tolerance."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary["substrate"], indent=2))
    print(json.dumps(summary["local_law_per_defect_center"], indent=2))
    print(json.dumps(summary["global_cheap_exit_cover"], indent=2))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
