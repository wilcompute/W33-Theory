#!/usr/bin/env python3
"""Pass 1193: exact A5 intersection bridge between W(E6)/S5 and PSp(4,3)/A5.

The index-two subgroup is constructed as the even-reflection-word kernel in W(E6).
For a 432-point A2-triple orbit, its S5 stabilizer meets that kernel in A5.
"""
from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, product
import json
import math
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1193_a5_intersection_bridge.json"


def dot(a: Iterable[int], b: Iterable[int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def e8_roots() -> tuple[tuple[int, ...], ...]:
    roots: list[tuple[int, ...]] = []
    for i, j in combinations(range(8), 2):
        for si in (-2, 2):
            for sj in (-2, 2):
                v = [0] * 8
                v[i], v[j] = si, sj
                roots.append(tuple(v))
    for signs in product((-1, 1), repeat=8):
        if sum(s == -1 for s in signs) % 2 == 0:
            roots.append(tuple(signs))
    assert len(roots) == len(set(roots)) == 240
    return tuple(roots)


@lru_cache(maxsize=1)
def base_data() -> dict[str, object]:
    roots = e8_roots()
    index = {r: i for i, r in enumerate(roots)}
    chosen = None
    for i, a in enumerate(roots):
        for j in range(i + 1, len(roots)):
            b = roots[j]
            if dot(a, b) != -4:
                continue
            c = tuple(-x - y for x, y in zip(a, b))
            if c in index:
                chosen = tuple(sorted((i, j, index[c])))
                break
        if chosen is not None:
            break
    assert chosen is not None
    a2_roots = [roots[i] for i in chosen]
    orthogonal = [i for i, r in enumerate(roots) if all(dot(r, a) == 0 for a in a2_roots)]
    assert len(orthogonal) == 72

    def d(i: int, j: int) -> int:
        return dot(roots[i], roots[j])

    adjacent = {i: [j for j in orthogonal if d(i, j) == -4] for i in orthogonal}
    simple = None
    for center in orthogonal:
        for leaf, left, right in combinations(adjacent[center], 3):
            if any(d(x, y) != 0 for x, y in combinations((leaf, left, right), 2)):
                continue
            for left_end in adjacent[left]:
                if left_end == center or any(d(left_end, x) != 0 for x in (center, leaf, right)):
                    continue
                for right_end in adjacent[right]:
                    if right_end in (center, leaf, left, left_end):
                        continue
                    if any(d(right_end, x) != 0 for x in (center, leaf, left, left_end)):
                        continue
                    simple = (left_end, left, leaf, center, right, right_end)
                    break
                if simple is not None:
                    break
            if simple is not None:
                break
        if simple is not None:
            break
    assert simple is not None
    return {"roots": roots, "index": index, "a2": chosen, "simple": simple}


def reflection_permutation(root_index: int) -> np.ndarray:
    data = base_data()
    roots = data["roots"]
    index = data["index"]
    r = np.asarray(roots[root_index], dtype=np.int16)
    out = np.empty(240, dtype=np.uint8)
    for i, v in enumerate(roots):
        vv = np.asarray(v, dtype=np.int16)
        coeff = int(vv.dot(r) // 4)
        out[i] = index[tuple((vv - coeff * r).tolist())]
    return out


def compose(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a[b]


def inverse(p: np.ndarray) -> np.ndarray:
    q = np.empty_like(p)
    q[p] = np.arange(len(p), dtype=p.dtype)
    return q


def permutation_order(p: np.ndarray) -> int:
    seen = np.zeros(len(p), dtype=bool)
    out = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        length = 0
        while not seen[j]:
            seen[j] = True
            j = int(p[j])
            length += 1
        out = math.lcm(out, length)
    return out


def enumerate_we6_with_parity() -> tuple[tuple[np.ndarray, ...], tuple[int, ...]]:
    gens = tuple(reflection_permutation(i) for i in base_data()["simple"])
    identity = np.arange(240, dtype=np.uint8)
    elements = [identity]
    parity = [0]
    seen = {identity.tobytes(): 0}
    queue = deque([0])
    while queue:
        idx = queue.popleft()
        x = elements[idx]
        px = parity[idx]
        for g in gens:
            y = compose(g, x)
            key = y.tobytes()
            py = px ^ 1
            if key in seen:
                assert parity[seen[key]] == py, "reflection parity must be well defined"
                continue
            seen[key] = len(elements)
            elements.append(y)
            parity.append(py)
            queue.append(len(elements) - 1)
    assert len(elements) == 51840
    assert Counter(parity) == {0: 25920, 1: 25920}
    return tuple(elements), tuple(parity)


def a2_triples() -> tuple[tuple[int, int, int], ...]:
    roots = base_data()["roots"]
    index = base_data()["index"]
    triples: set[tuple[int, int, int]] = set()
    for i, a in enumerate(roots):
        for j in range(i + 1, len(roots)):
            b = roots[j]
            if dot(a, b) != -4:
                continue
            c = tuple(-x - y for x, y in zip(a, b))
            triples.add(tuple(sorted((i, j, index[c]))))
    assert len(triples) == 2240
    return tuple(sorted(triples))


def generator_actions(triples: tuple[tuple[int, int, int], ...]) -> tuple[np.ndarray, ...]:
    index = {t: i for i, t in enumerate(triples)}
    actions = []
    for root_index in base_data()["simple"]:
        g = reflection_permutation(root_index)
        a = np.empty(len(triples), dtype=np.int16)
        for i, t in enumerate(triples):
            a[i] = index[tuple(sorted(int(g[x]) for x in t))]
        actions.append(a)
    return tuple(actions)


def orbit_partition(actions: tuple[np.ndarray, ...], degree: int) -> list[list[int]]:
    unseen = set(range(degree))
    out = []
    while unseen:
        seed = min(unseen)
        orb = {seed}
        queue = deque([seed])
        while queue:
            x = queue.popleft()
            for g in actions:
                y = int(g[x])
                if y not in orb:
                    orb.add(y)
                    queue.append(y)
        unseen -= orb
        out.append(sorted(orb))
    return sorted(out, key=lambda x: (len(x), x[0]))


def fixes_triple(p: np.ndarray, triple: tuple[int, int, int]) -> bool:
    return tuple(sorted(int(p[x]) for x in triple)) == triple


def main() -> dict[str, object]:
    triples = a2_triples()
    orbits = orbit_partition(generator_actions(triples), len(triples))
    sizes = [len(o) for o in orbits]
    assert sizes == [1, 1, 27, 27, 27, 27, 27, 27, 240, 270, 270, 432, 432, 432]
    representative = triples[next(o[0] for o in orbits if len(o) == 432)]

    group, parity = enumerate_we6_with_parity()
    stab_indices = [i for i, g in enumerate(group) if fixes_triple(g, representative)]
    even_indices = [i for i, p in enumerate(parity) if p == 0]
    intersection = [i for i in stab_indices if parity[i] == 0]

    assert len(stab_indices) == 120
    assert len(intersection) == 60
    order_dist = Counter(permutation_order(group[i]) for i in intersection)
    assert order_dist == {1: 1, 2: 15, 3: 20, 5: 24}

    intersection_keys = {group[i].tobytes() for i in intersection}
    for i in stab_indices:
        gi = inverse(group[i])
        for j in intersection:
            assert compose(group[i], compose(group[j], gi)).tobytes() in intersection_keys

    result = {
        "schema": "w33.pass1193.a5_intersection_bridge.v1",
        "status": "PASS",
        "groups": {
            "WE6_order": len(group),
            "even_reflection_kernel_order": len(even_indices),
            "even_kernel_identification": "PSp(4,3)",
            "S5_stabilizer_order": len(stab_indices),
            "intersection_order": len(intersection),
            "intersection_identification": "A5",
            "intersection_element_orders": dict(sorted(order_dist.items())),
        },
        "indices": {
            "WE6_over_S5": len(group) // len(stab_indices),
            "PSp43_over_A5": len(even_indices) // len(intersection),
            "S5_over_A5": len(stab_indices) // len(intersection),
            "WE6_over_PSp43": len(group) // len(even_indices),
        },
        "bridge": {
            "statement": "The inclusion PSp(4,3) -> W(E6) induces a bijection PSp(4,3)/A5 -> W(E6)/S5 on each 432-point orbit.",
            "same_degree_432": True,
            "intersection_normal_in_S5": True,
            "quotient_is_C2": True,
            "parity_split_inside_stabilizer": {"even": 60, "odd": 60},
        },
        "representative_a2_triple": list(representative),
        "scope": "Exact finite permutation computation on the 240 E8 roots. The index-two kernel is the even-reflection-word subgroup.",
    }
    assert result["indices"]["WE6_over_S5"] == 432
    assert result["indices"]["PSp43_over_A5"] == 432
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "intersection": "A5", "degree": 432}, indent=2))
    return result


if __name__ == "__main__":
    main()
