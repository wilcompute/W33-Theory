#!/usr/bin/env python3
"""Pass 3199: test the tempting 45-block / 45-route-edge identification.

The chromatic packet supplies a natural degree-32 graph on its 45 canonical blocks. The
curvature packet supplies the exceptional S6 action on the 45 edges of the ten 3+3
partitions of a six-set. Any S6-equivariant identification would carry the chromatic graph
to a union of S6 pair orbitals on those 45 edges. This verifier enumerates every such union
and proves that none has the chromatic graph's exact polynomial identity.
"""
from __future__ import annotations

import itertools
import json
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3199_CHROMATIC_CURVATURE_BRIDGE_results.json"
Q = 3


def normalize(vector):
    row = tuple(x % Q for x in vector)
    for x in row:
        if x:
            inverse = pow(x, -1, Q)
            return tuple((inverse * y) % Q for y in row)
    raise ValueError("zero vector")


def symp(left, right):
    return (left[0] * right[3] - left[3] * right[0] + left[1] * right[2] - left[2] * right[1]) % Q


def geometry():
    points = sorted({normalize(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    pidx = {point: i for i, point in enumerate(points)}
    adjacency = np.zeros((40, 40), dtype=np.int8)
    for i, j in itertools.combinations(range(40), 2):
        if symp(points[i], points[j]) == 0:
            adjacency[i, j] = adjacency[j, i] = 1
    line_set = set()
    for i, j in itertools.combinations(range(40), 2):
        if not adjacency[i, j]:
            continue
        span = set()
        for a, b in itertools.product(range(Q), repeat=2):
            vector = tuple((a * points[i][k] + b * points[j][k]) % Q for k in range(4))
            if any(vector):
                span.add(pidx[normalize(vector)])
        line_set.add(tuple(sorted(span)))
    lines = sorted(line_set)
    edges = [(i, j) for i, j in itertools.combinations(range(40), 2) if adjacency[i, j]]
    eidx = {edge: i for i, edge in enumerate(edges)}
    frames = []
    matchings = []
    for a, b in itertools.combinations(range(40), 2):
        if set(lines[a]) & set(lines[b]):
            continue
        matching = []
        for x in lines[a]:
            neighbours = [y for y in lines[b] if adjacency[x, y]]
            assert len(neighbours) == 1
            matching.append(eidx[tuple(sorted((x, neighbours[0])))])
        frames.append((a, b))
        matchings.append(tuple(sorted(matching)))
    incidence = np.zeros((540, 240), dtype=np.int8)
    for row, matching in enumerate(matchings):
        incidence[row, list(matching)] = 1
    frame_graph = (incidence @ incidence.T).astype(np.int16)
    np.fill_diagonal(frame_graph, 0)
    return points, adjacency, lines, frames, frame_graph


def transvection(points, pidx, vector):
    vector = normalize(vector)
    permutation = []
    for point in points:
        coefficient = symp(point, vector)
        image = tuple((point[i] + coefficient * vector[i]) % Q for i in range(4))
        permutation.append(pidx[normalize(image)])
    return tuple(permutation)


def chromatic_block_graph():
    points, adjacency, lines, frames, frame_graph = geometry()
    octets = []
    seen = set()
    for left in itertools.combinations(range(40), 4):
        if any(adjacency[i, j] for i, j in itertools.combinations(left, 2)):
            continue
        right = tuple(v for v in range(40) if all(adjacency[v, u] for u in left))
        if len(right) != 4 or any(adjacency[i, j] for i, j in itertools.combinations(right, 2)):
            continue
        key = tuple(sorted((tuple(left), tuple(right))))
        if key not in seen:
            seen.add(key)
            octets.append(key)
    assert len(octets) == 45
    pidx = {point: i for i, point in enumerate(points)}
    lidx = {line: i for i, line in enumerate(lines)}
    fidx = {frame: i for i, frame in enumerate(frames)}
    oidx = {octet: i for i, octet in enumerate(octets)}
    point_generators = [
        transvection(points, pidx, vector)
        for vector in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (1, 0, 1, 0))
    ]
    frame_generators = []
    octet_generators = []
    for permutation in point_generators:
        line_permutation = tuple(lidx[tuple(sorted(permutation[x] for x in line))] for line in lines)
        frame_generators.append(tuple(fidx[tuple(sorted((line_permutation[a], line_permutation[b])))] for a, b in frames))
        image = []
        for left, right in octets:
            key = tuple(sorted((tuple(sorted(permutation[x] for x in left)), tuple(sorted(permutation[x] for x in right)))))
            image.append(oidx[key])
        octet_generators.append(tuple(image))
    unseen = set(range(540 * 45))
    pair_orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            value = queue.popleft()
            frame, octet = divmod(value, 45)
            for fg, og in zip(frame_generators, octet_generators):
                image = fg[frame] * 45 + og[octet]
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        unseen -= orbit
        pair_orbits.append(orbit)
    relation = min(pair_orbits, key=len)
    blocks = [[] for _ in range(45)]
    for value in relation:
        frame, octet = divmod(value, 45)
        blocks[octet].append(frame)
    partition = np.zeros((540, 45), dtype=np.int64)
    for column, block in enumerate(blocks):
        partition[block, column] = 1
    quotient = partition.T @ frame_graph.astype(np.int64) @ partition
    graph = (quotient == 9).astype(np.int64)
    np.fill_diagonal(graph, 0)
    assert set(map(int, graph.sum(axis=1))) == {32}
    identity = np.eye(45, dtype=np.int64)
    assert np.count_nonzero((graph - 32 * identity) @ (graph - 2 * identity) @ (graph + 4 * identity)) == 0
    return graph


def route_edge_orbitals():
    partitions = []
    for subset in itertools.combinations(range(6), 3):
        complement = tuple(sorted(set(range(6)) - set(subset)))
        key = tuple(sorted((tuple(subset), complement)))
        if key not in partitions:
            partitions.append(key)
    partitions.sort()
    pidx = {partition: i for i, partition in enumerate(partitions)}
    actions = set()
    for permutation in itertools.permutations(range(6)):
        image = []
        for left, right in partitions:
            a = tuple(sorted(permutation[x] for x in left))
            b = tuple(sorted(permutation[x] for x in right))
            image.append(pidx[tuple(sorted((a, b)))])
        actions.add(tuple(image))
    assert len(actions) == 720
    edges = list(itertools.combinations(range(10), 2))
    eidx = {edge: i for i, edge in enumerate(edges)}
    edge_actions = [tuple(eidx[tuple(sorted((action[u], action[v])))] for u, v in edges) for action in actions]
    unseen = set(itertools.combinations(range(45), 2))
    orbitals = []
    while unseen:
        seed = min(unseen)
        orbit = {tuple(sorted((action[seed[0]], action[seed[1]]))) for action in edge_actions}
        unseen -= orbit
        matrix = np.zeros((45, 45), dtype=np.int64)
        for i, j in orbit:
            matrix[i, j] = matrix[j, i] = 1
        orbitals.append(matrix)
    assert sorted(int(matrix.sum(axis=1)[0]) for matrix in orbitals) == [2, 2, 8, 8, 8, 16]
    return orbitals


def annihilated_by_chromatic_polynomial(matrix):
    identity = np.eye(45, dtype=np.int64)
    product = (matrix - 32 * identity) @ (matrix - 2 * identity) @ (matrix + 4 * identity)
    return np.count_nonzero(product) == 0


def main() -> None:
    chromatic = chromatic_block_graph()
    orbitals = route_edge_orbitals()
    candidates = []
    for mask in range(1, 1 << len(orbitals)):
        selected = [i for i in range(len(orbitals)) if (mask >> i) & 1]
        matrix = sum((orbitals[i] for i in selected), np.zeros((45, 45), dtype=np.int64))
        degree = int(matrix.sum(axis=1)[0])
        if degree == 32:
            candidates.append({
                "orbitals": selected,
                "chromatic_polynomial_identity": annihilated_by_chromatic_polynomial(matrix),
                "trace_square": int(np.trace(matrix @ matrix)),
                "trace_cube": int(np.trace(matrix @ matrix @ matrix)),
            })
    assert len(candidates) == 3
    assert not any(candidate["chromatic_polynomial_identity"] for candidate in candidates)
    result = {
        "schema": "w33.pass3199.chromatic_curvature_bridge_falsifier.v1",
        "chromatic_block_relation": {
            "vertices": 45,
            "degree": 32,
            "polynomial_identity": "(A-32I)(A-2I)(A+4I)=0",
            "spectrum": {"32": 1, "2": 24, "-4": 20},
        },
        "route_edge_action": {
            "group": "exceptional S6 action on ten unordered 3+3 partitions",
            "objects": "45 edges of K10",
            "pair_orbital_degrees": [2, 2, 8, 8, 8, 16],
            "degree_32_orbital_unions": len(candidates),
        },
        "degree_32_candidates": candidates,
        "equivariant_bridge_exists_for_natural_relations": False,
        "theorem": "No S6-equivariant bijection can carry the canonical 45-block chromatic relation to an invariant relation on the 45 curvature-route edges.",
        "interpretation": "The shared number 45 is real but insufficient: chromatic defect and route curvature live in inequivalent natural relation structures. Any bridge must add extra phase/gauge data or abandon equivariance.",
        "boundary": "This falsifies the direct natural-relation identification only. It does not exclude nonlinear, non-equivariant, derived-category or higher-incidence correspondences."
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"degree32_candidates": len(candidates), "equivariant_bridge": False}, sort_keys=True))


if __name__ == "__main__":
    main()
