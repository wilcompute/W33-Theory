#!/usr/bin/env python3
"""Pass 3989: complete orbit census of maximum A4=57 extensions.

This standalone verifier reconstructs the fixed [36,6,16] parent code, its
945 admissible weight-four dual words, the O6-(2) coordinate group, all
maximum cliques through one representative of the 135-orbit, and the three
full group orbits of maximum cliques.  Runtime is typically under one minute.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_3989_MAXIMUM_CODE_ORBIT_CENSUS.json"
GENERATOR_VECTORS = (3, 7, 11, 13, 16, 17, 32)
EXPECTED_SEMANTIC = "e2d3b136f48ec6e5107b38e0e8c4083ee8f44e63f645d91fcdd0d4cbbd15d8dd"


def bits(x: int, n: int = 6) -> tuple[int, ...]:
    return tuple((x >> i) & 1 for i in range(n))


def qform(x: int) -> int:
    b = bits(x)
    return (b[0] * b[1] + b[2] * b[3] + b[4] * b[5] + b[4] + b[5]) & 1


def beta(x: int, y: int) -> int:
    return qform(x ^ y) ^ qform(x) ^ qform(y)


def polar(x: int, y: int) -> int:
    a, b = bits(x), bits(y)
    return (a[0]*b[1] + a[1]*b[0] + a[2]*b[3] + a[3]*b[2]
            + a[4]*b[5] + a[5]*b[4]) & 1


def symmetry(v: int, x: int) -> int:
    return x ^ (v if polar(x, v) else 0)


def gf2_basis(values: list[int]) -> list[int]:
    pivots: dict[int, int] = {}
    for value in values:
        x = int(value)
        while x:
            p = x.bit_length() - 1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                for pp in list(pivots):
                    if pp != p and ((pivots[pp] >> p) & 1):
                        pivots[pp] ^= x
                break
    return [pivots[p] for p in sorted(pivots, reverse=True)]


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def group_closure(generators: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    queue = [identity]
    while queue:
        x = queue.pop()
        for g in generators:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return sorted(seen)


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    out = 0
    while word:
        bit = word & -word
        i = bit.bit_length() - 1
        out |= 1 << permutation[i]
        word ^= bit
    return out


def color_sort(candidates: int, adjacency: list[int]) -> tuple[list[int], list[int]]:
    order: list[int] = []
    bounds: list[int] = []
    color = 0
    unused = candidates
    while unused:
        color += 1
        available = unused
        while available:
            bit = available & -available
            v = bit.bit_length() - 1
            unused ^= bit
            available &= ~bit
            available &= ~adjacency[v]
            order.append(v)
            bounds.append(color)
    return order, bounds


def enumerate_maximum_through(vertex: int, adjacency: list[int], target: int = 57) -> list[tuple[int, ...]]:
    answers: list[tuple[int, ...]] = []

    def expand(clique: list[int], candidates: int) -> None:
        if len(clique) == target:
            answers.append(tuple(sorted(clique)))
            return
        if candidates.bit_count() < target - len(clique):
            return
        order, bounds = color_sort(candidates, adjacency)
        for index in range(len(order) - 1, -1, -1):
            if len(clique) + bounds[index] < target:
                return
            v = order[index]
            bit = 1 << v
            if not candidates & bit:
                continue
            expand(clique + [v], candidates & adjacency[v])
            candidates ^= bit
            if candidates.bit_count() < target - len(clique):
                return

    expand([vertex], adjacency[vertex])
    return sorted(set(answers))


def sha_json(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def span(values: list[int]) -> tuple[list[int], list[int]]:
    basis = gf2_basis(values)
    words = [0]
    for vector in basis:
        words += [word ^ vector for word in words]
    return basis, words


def component_parameters(clique: tuple[int, ...], words: list[int]) -> tuple[list[list[int]], dict[str, int]]:
    n = len(clique)
    graph = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (words[clique[i]] & words[clique[j]]).bit_count() == 2:
                graph[i].add(j)
                graph[j].add(i)
    remaining = set(range(n))
    components: list[list[int]] = []
    while remaining:
        seed = remaining.pop()
        component = {seed}
        queue = [seed]
        while queue:
            u = queue.pop()
            for v in graph[u]:
                if v in remaining:
                    remaining.remove(v)
                    component.add(v)
                    queue.append(v)
        components.append(sorted(component))
    parameters: list[list[int]] = []
    for component in sorted(components, key=len, reverse=True):
        C = set(component)
        degrees = {len(graph[v] & C) for v in component}
        assert len(degrees) == 1
        degree = next(iter(degrees))
        adjacent_common, nonadjacent_common = set(), set()
        for ii, u in enumerate(component):
            for v in component[ii + 1:]:
                common = len(graph[u] & graph[v] & C)
                (adjacent_common if v in graph[u] else nonadjacent_common).add(common)
        assert len(adjacent_common) == len(nonadjacent_common) == 1
        parameters.append([len(component), degree,
                           next(iter(adjacent_common)), next(iter(nonadjacent_common))])
    coordinate_degrees = [0] * 36
    for index in clique:
        word = words[index]
        for coordinate in range(36):
            coordinate_degrees[coordinate] += (word >> coordinate) & 1
    profile = {str(k): v for k, v in sorted(Counter(coordinate_degrees).items())}
    return parameters, profile


def build() -> dict[str, object]:
    nonsingular = [x for x in range(1, 64) if qform(x)]
    assert len(nonsingular) == 36
    coordinate_index = {x: i for i, x in enumerate(nonsingular)}

    character_words: list[int] = []
    for label in range(64):
        word = 0
        for i, x in enumerate(nonsingular):
            if beta(label, x):
                word |= 1 << i
        character_words.append(word)
    parent_basis = gf2_basis(character_words)
    assert len(parent_basis) == 6

    candidates: list[int] = []
    for support in itertools.combinations(range(36), 4):
        word = sum(1 << i for i in support)
        if all(((word & b).bit_count() & 1) == 0 for b in parent_basis):
            candidates.append(word)
    assert len(candidates) == 945
    candidate_index = {word: i for i, word in enumerate(candidates)}

    adjacency = [0] * len(candidates)
    for i, left in enumerate(candidates):
        for j in range(i + 1, len(candidates)):
            if ((left & candidates[j]).bit_count() & 1) == 0:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    assert {row.bit_count() for row in adjacency} == {624}

    coordinate_generators = [
        tuple(coordinate_index[symmetry(v, x)] for x in nonsingular)
        for v in GENERATOR_VECTORS
    ]
    group = group_closure(coordinate_generators)
    assert len(group) == 51840
    vertex_generators = [
        tuple(candidate_index[permute_word(word, p)] for word in candidates)
        for p in coordinate_generators
    ]

    remaining = set(range(945))
    vertex_orbits: list[tuple[int, ...]] = []
    while remaining:
        seed = min(remaining)
        orbit = {seed}
        queue = [seed]
        while queue:
            u = queue.pop()
            for p in vertex_generators:
                v = p[u]
                if v not in orbit:
                    orbit.add(v)
                    queue.append(v)
        remaining.difference_update(orbit)
        vertex_orbits.append(tuple(sorted(orbit)))
    vertex_orbits.sort(key=len)
    assert [len(orbit) for orbit in vertex_orbits] == [135, 810]
    orbit_id = {v: i for i, orbit in enumerate(vertex_orbits) for v in orbit}

    fixed = vertex_orbits[0][0]
    fixed_cliques = enumerate_maximum_through(fixed, adjacency)
    assert len(fixed_cliques) == 57
    fixed_distribution = Counter(sum(orbit_id[v] == 0 for v in clique)
                                 for clique in fixed_cliques)
    assert fixed_distribution == Counter({15: 45, 3: 12})

    clique_orbits: list[set[tuple[int, ...]]] = []
    seen: set[tuple[int, ...]] = set()
    for representative in fixed_cliques:
        if representative in seen:
            continue
        orbit = {representative}
        queue = [representative]
        while queue:
            clique = queue.pop()
            for p in vertex_generators:
                image = tuple(sorted(p[v] for v in clique))
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        seen.update(orbit)
        clique_orbits.append(orbit)
    clique_orbits.sort(key=len, reverse=True)
    assert [len(orbit) for orbit in clique_orbits] == [540, 270, 135]
    all_cliques = sorted(set().union(*clique_orbits))
    assert len(all_cliques) == 945

    orbit_payload = []
    expected_weight_distribution = {
        "0": 1, "4": 57, "8": 852, "12": 7332, "16": 57294,
        "20": 57294, "24": 7332, "28": 852, "32": 57, "36": 1,
    }
    for orbit in clique_orbits:
        representative = min(orbit)
        basis, codewords = span(parent_basis + [candidates[i] for i in representative])
        distribution = {str(k): v for k, v in sorted(Counter(w.bit_count() for w in codewords).items())}
        parameters, profile = component_parameters(representative, candidates)
        assert len(basis) == 17
        assert min(w.bit_count() for w in codewords if w) == 4
        assert distribution == expected_weight_distribution
        assert parameters == [[45, 16, 8, 4], [6, 4, 2, 4], [6, 4, 2, 4]]
        assert profile == {"3": 16, "9": 20}
        sorted_orbit = sorted(orbit)
        orbit_payload.append({
            "orbit_size": len(orbit),
            "stabilizer_order": 51840 // len(orbit),
            "parent_vertex_orbit_counts": {
                "135": sum(orbit_id[v] == 0 for v in representative),
                "810": sum(orbit_id[v] == 1 for v in representative),
            },
            "code_dimension": 17,
            "minimum_weight": 4,
            "weight_distribution": distribution,
            "intersection_two_component_parameters": parameters,
            "coordinate_degree_profile": profile,
            "orbit_clique_sha256": sha_json([list(c) for c in sorted_orbit]),
            "representative_support_sha256": hashlib.sha256(
                "\n".join(f"{candidates[i]:09x}" for i in representative).encode()
            ).hexdigest(),
        })

    payload: dict[str, object] = {
        "schema": "w33.pass3989.maximum_code_orbit_census.v1",
        "status": "PASS_EXACT_COMPLETE_FIXED_PARENT_MAXIMUM_CODE_CENSUS",
        "parent_code": "[36,6,16]",
        "compatibility_graph": {
            "vertices": 945,
            "degree": 624,
            "maximum_clique_size": 57,
            "vertex_orbits": [135, 810],
        },
        "fixed_135_vertex_census": {
            "representative": fixed,
            "maximum_cliques_through_representative": 57,
            "intersection_distribution": {"3": 12, "15": 45},
        },
        "maximum_cliques_total": 945,
        "maximum_clique_orbits": orbit_payload,
        "global_clique_sha256": sha_json([list(c) for c in all_cliques]),
        "group_order": 51840,
        "generator_vectors_hex": [f"{v:02x}" for v in GENERATOR_VECTORS],
        "boundary": "Complete orbit census for maximum doubly-even self-orthogonal extensions containing the fixed [36,6,16] parent. No classification of unrelated length-36 codes is implied.",
    }
    payload["semantic_sha256"] = sha_json(payload)
    assert payload["semantic_sha256"] == EXPECTED_SEMANTIC
    return payload


def main() -> None:
    payload = build()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS_MAXIMUM_CODE_ORBIT_CENSUS", payload["semantic_sha256"])


if __name__ == "__main__":
    main()
