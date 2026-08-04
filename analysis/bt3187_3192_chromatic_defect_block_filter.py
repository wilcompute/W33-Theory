#!/usr/bin/env python3
"""Passes 3187-3192: exact ten-colour defect and A4-block filter.

This verifier reconstructs W(3,3), the 540-frame graph, the canonical
45-by-12 frame/octet block system, and the frozen proper eleven-colouring.
It then freezes exact necessary conditions for any hypothetical ten-colouring.
It does not claim that a ten-colouring exists or is impossible.
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT3187_BT3192_CHROMATIC_DEFECT_BLOCK_FILTER_results.json"
COLORING = ROOT / "data" / "w33_pass2561_coloring11.txt"
Q = 3


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    w = tuple(x % Q for x in v)
    for x in w:
        if x:
            z = pow(x, -1, Q)
            return tuple((z * y) % Q for y in w)
    raise ValueError("zero vector has no projective normalization")


def symp(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[3] - u[3] * v[0] + u[1] * v[2] - u[2] * v[1]) % Q


def build_geometry():
    points = sorted(
        {normalize(v) for v in itertools.product(range(Q), repeat=4) if any(v)}
    )
    pidx = {p: i for i, p in enumerate(points)}
    adjacency = np.zeros((40, 40), dtype=np.int8)
    for i, j in itertools.combinations(range(40), 2):
        if symp(points[i], points[j]) == 0:
            adjacency[i, j] = adjacency[j, i] = 1

    line_sets: set[tuple[int, ...]] = set()
    for i, j in itertools.combinations(range(40), 2):
        if not adjacency[i, j]:
            continue
        span = set()
        for a, b in itertools.product(range(Q), repeat=2):
            w = tuple((a * points[i][k] + b * points[j][k]) % Q for k in range(4))
            if any(w):
                span.add(pidx[normalize(w)])
        line_sets.add(tuple(sorted(span)))
    lines = sorted(line_sets)

    edges = [
        (i, j)
        for i, j in itertools.combinations(range(40), 2)
        if adjacency[i, j]
    ]
    eidx = {edge: i for i, edge in enumerate(edges)}
    frames: list[tuple[int, int]] = []
    matchings: list[tuple[int, ...]] = []
    for a, b in itertools.combinations(range(40), 2):
        if set(lines[a]) & set(lines[b]):
            continue
        matching = []
        for x in lines[a]:
            ys = [y for y in lines[b] if adjacency[x, y]]
            assert len(ys) == 1
            matching.append(eidx[tuple(sorted((x, ys[0])))])
        frames.append((a, b))
        matchings.append(tuple(sorted(matching)))

    incidence = np.zeros((540, 240), dtype=np.int8)
    for row, matching in enumerate(matchings):
        incidence[row, list(matching)] = 1
    frame_graph = (incidence @ incidence.T).astype(np.int16)
    np.fill_diagonal(frame_graph, 0)
    assert set(np.unique(frame_graph)) <= {0, 1}
    return points, adjacency, lines, edges, frames, incidence, frame_graph


def transvection(points, pidx, v):
    v = normalize(v)
    out = []
    for x in points:
        c = symp(x, v)
        y = tuple((x[i] + c * v[i]) % Q for i in range(4))
        out.append(pidx[normalize(y)])
    return tuple(out)


def canonical_blocks(points, adjacency, lines, frames):
    octets = []
    seen = set()
    for left in itertools.combinations(range(40), 4):
        if any(adjacency[i, j] for i, j in itertools.combinations(left, 2)):
            continue
        right = tuple(v for v in range(40) if all(adjacency[v, u] for u in left))
        if len(right) != 4 or any(
            adjacency[i, j] for i, j in itertools.combinations(right, 2)
        ):
            continue
        key = tuple(sorted((tuple(left), tuple(right))))
        if key not in seen:
            seen.add(key)
            octets.append(key)
    assert len(octets) == 45

    pidx = {p: i for i, p in enumerate(points)}
    lidx = {line: i for i, line in enumerate(lines)}
    fidx = {frame: i for i, frame in enumerate(frames)}
    oidx = {octet: i for i, octet in enumerate(octets)}
    point_generators = [
        transvection(points, pidx, v)
        for v in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (1, 0, 1, 0))
    ]
    frame_generators = []
    octet_generators = []
    for p in point_generators:
        line_perm = tuple(lidx[tuple(sorted(p[x] for x in line))] for line in lines)
        frame_generators.append(
            tuple(fidx[tuple(sorted((line_perm[a], line_perm[b])))] for a, b in frames)
        )
        op = []
        for left, right in octets:
            key = tuple(
                sorted(
                    (
                        tuple(sorted(p[x] for x in left)),
                        tuple(sorted(p[x] for x in right)),
                    )
                )
            )
            op.append(oidx[key])
        octet_generators.append(tuple(op))

    unseen = set(range(540 * 45))
    pair_orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        queue = collections.deque([seed])
        while queue:
            z = queue.popleft()
            frame, octet = divmod(z, 45)
            for fg, og in zip(frame_generators, octet_generators):
                zz = fg[frame] * 45 + og[octet]
                if zz not in orbit:
                    orbit.add(zz)
                    queue.append(zz)
        unseen -= orbit
        pair_orbits.append(orbit)
    relation = min(pair_orbits, key=len)
    assert len(relation) == 540
    blocks = [[] for _ in range(45)]
    for z in relation:
        frame, octet = divmod(z, 45)
        blocks[octet].append(frame)
    assert all(len(block) == 12 for block in blocks)
    return octets, [sorted(block) for block in blocks], sorted(map(len, pair_orbits))


def load_coloring() -> np.ndarray:
    tokens = COLORING.read_text(encoding="utf-8").split()
    assert int(tokens[0]) == 11
    colors = np.array(list(map(int, tokens[1:])), dtype=np.int64)
    assert len(colors) == 540
    return colors


def defect_gram(frame_graph: np.ndarray, colors: np.ndarray, k: int):
    x = np.zeros((540, k), dtype=np.int64)
    x[np.arange(540), colors] = 1
    sizes = x.sum(axis=0)
    ordered_edge_counts = x.T @ frame_graph @ x
    integer_gram = 15 * (ordered_edge_counts + 4 * np.diag(sizes)) - np.outer(sizes, sizes)
    return sizes, ordered_edge_counts, integer_gram


def semantic_hash(data: dict) -> str:
    body = dict(data)
    body.pop("sha256_without_hash_field", None)
    return hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def certificate() -> dict:
    points, adjacency, lines, edges, frames, incidence, frame_graph = build_geometry()
    _, blocks, pair_orbit_sizes = canonical_blocks(points, adjacency, lines, frames)

    block_degrees = []
    complement_component_sizes = []
    for block in blocks:
        local = frame_graph[np.ix_(block, block)]
        block_degrees.append(tuple(sorted(map(int, local.sum(axis=1)))))
        complement = np.ones((12, 12), dtype=np.int8) - np.eye(12, dtype=np.int8) - local
        unseen = set(range(12))
        components = []
        while unseen:
            seed = min(unseen)
            unseen.remove(seed)
            component = {seed}
            queue = [seed]
            while queue:
                x = queue.pop()
                for y in list(unseen):
                    if complement[x, y]:
                        unseen.remove(y)
                        component.add(y)
                        queue.append(y)
            components.append(component)
        complement_component_sizes.append(tuple(sorted(map(len, components))))

    colors = load_coloring()
    sizes, ordered_edge_counts, integer_gram = defect_gram(frame_graph, colors, 11)
    upper_triangle = np.transpose(np.where(np.triu(frame_graph, 1)))

    checks = {
        "w33_counts": (len(points), len(lines), len(edges), len(frames))
        == (40, 40, 240, 540),
        "frame_graph_regular_32": set(map(int, frame_graph.sum(axis=1))) == {32},
        "frame_graph_edges_8640": int(frame_graph.sum() // 2) == 8640,
        "identity_H_plus_4I_MMT": np.array_equal(
            frame_graph + 4 * np.eye(540, dtype=np.int16), incidence @ incidence.T
        ),
        "frame_octet_pair_orbits": pair_orbit_sizes == [540, 3240, 3240, 4320, 12960],
        "fortyfive_blocks_of_twelve": len(blocks) == 45
        and all(len(block) == 12 for block in blocks),
        "each_block_K12_minus_3K4": set(block_degrees) == {(8,) * 12}
        and set(complement_component_sizes) == {(4, 4, 4)},
        "frozen_11_coloring_proper": all(
            colors[i] != colors[j] for i, j in upper_triangle
        ),
        "frozen_11_class_sizes": sorted(map(int, sizes))
        == [43, 44, 46, 46, 47, 48, 48, 49, 51, 58, 60],
        "gram_row_sum_zero": np.all(integer_gram.sum(axis=1) == 0),
        "gram_diagonal_formula": all(
            integer_gram[i, i] == sizes[i] * (60 - sizes[i]) for i in range(11)
        ),
        "gram_mod15_rank_one_congruence": np.array_equal(
            integer_gram % 15, (-np.outer(sizes, sizes)) % 15
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    assert all(checks.values()), [key for key, value in checks.items() if not value]

    trace_integer = int(np.trace(integer_gram))
    trace_defect = Fraction(trace_integer, 15)
    data = {
        "schema": "w33.pass3187_3192.chromatic_defect_block_filter.v1",
        "status": "PASS_EXACT_FILTER_WITHOUT_TEN_COLOR_DECISION",
        "graph": {
            "vertices": 540,
            "edges": 8640,
            "degree": 32,
            "identity": "H+4I=M M^T",
            "spectrum": {"32": 1, "14": 44, "8": 15, "4": 81, "2": 84, "-4": 315},
        },
        "canonical_block_system": {
            "blocks": 45,
            "block_size": 12,
            "block_graph": "K12 minus 3K4",
            "block_internal_degree": 8,
            "frame_octet_pair_orbit_sizes": pair_orbit_sizes,
            "partition_sha256": hashlib.sha256(
                json.dumps(blocks, separators=(",", ":")).encode("utf-8")
            ).hexdigest(),
        },
        "frozen_11_coloring": {
            "source": "data/w33_pass2561_coloring11.txt",
            "class_sizes": list(map(int, sizes)),
            "sorted_class_sizes": sorted(map(int, sizes)),
            "defect_gram_integer_scale": 15,
            "integer_gram": integer_gram.tolist(),
            "ordered_color_edge_counts": ordered_edge_counts.tolist(),
            "trace_integer_gram": trace_integer,
            "trace_defect": str(trace_defect),
        },
        "ten_color_filter": {
            "class_sizes": "s_i are positive integers, s_i<=60, and sum_i s_i=540",
            "deficits": "d_i=60-s_i>=0 and sum_i d_i=60",
            "integer_gram_diagonal": "K_ii=s_i(60-s_i)",
            "integer_gram_offdiagonal": "K_ij=15 e_ij-s_i s_j",
            "integer_gram_definition": "K=15 G, G=X^T(H+4I)X-(1/15)ss^T",
            "gram_constraints": [
                "K is positive semidefinite",
                "K*1=0",
                "rank(K)<=9",
                "K congruent to -s s^T modulo 15",
                "every 2x2 minor of K is divisible by 15",
            ],
            "trace_identity": "tr(G)=240-(1/15) sum_i d_i^2",
            "trace_upper_bound": 216,
            "trace_equality_condition": "s_1=...=s_10=54",
            "non_hoffman_squared_mass_upper_bound": 36,
            "spectral_gap_used": 6,
            "local_block_rule": "within each K12-minus-3K4 block, every color is confined to one K4 cell",
            "local_repeat_savings_lower_bound": 90,
        },
        "checks": checks,
        "theorem": (
            "Every hypothetical ten-colouring is simultaneously a near-Hoffman partition "
            "and a constrained colouring of forty-five A4-torsor blocks. Its centered color "
            "indicators have total H+4I energy at most 216 and total squared mass outside "
            "the exact-cover eigenspace at most 36. Its 10-by-10 integer defect Gram matrix "
            "is positive semidefinite, has row sum zero and rank at most nine, is congruent "
            "to -s s^T modulo 15, and all its 2-by-2 minors are divisible by 15. Locally, "
            "the colouring must realize at least 90 repeated-color savings across the 45 blocks."
        ),
        "boundary": (
            "This is a proof-producing necessary-condition filter. It neither constructs "
            "a ten-colouring nor proves ten-colour infeasibility. Bounded heuristic and MILP "
            "searches are diagnostics only and are not theorem evidence."
        ),
    }
    data["sha256_without_hash_field"] = semantic_hash(data)
    return data


def main() -> None:
    data = certificate()
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": data["status"], "sha256": data["sha256_without_hash_field"]}, sort_keys=True))


if __name__ == "__main__":
    main()
