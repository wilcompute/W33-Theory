#!/usr/bin/env python3
"""Readable common source for Passes 3025--3031.

The discrete model is exactly the repository's no/one/two-edge D4 fault model on K10.
Synthetic optical likelihoods are kept in downstream files and never promoted to finite
geometry theorems.
"""
from __future__ import annotations

import itertools
from collections import defaultdict
from functools import lru_cache
from math import comb

import numpy as np

D4 = [(a, b) for a in range(4) for b in range(2)]
D4_INDEX = {g: i for i, g in enumerate(D4)}
IDENTITY = (0, 0)
FAULTS = [g for g in D4 if g != IDENTITY]
VERTICES = tuple(range(10))
EDGES = list(itertools.combinations(VERTICES, 2))
TRIANGLES = list(itertools.combinations(VERTICES, 3))

FROZEN_23 = [
    (5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
    (1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),
    (1,7,8),(1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),
    (3,5,7),(0,1,7),(3,6,8),(0,4,5),(4,6,7),
]

VERIFIED_28 = [
    (0,1,3),(0,2,9),(0,3,7),(0,4,5),(0,4,7),(0,4,8),(0,5,6),
    (0,6,9),(1,2,3),(1,2,6),(1,4,6),(1,4,8),(1,5,8),(1,5,9),
    (1,7,9),(2,3,4),(2,3,8),(2,4,7),(2,5,9),(2,6,7),(2,8,9),
    (3,5,9),(3,6,8),(3,6,9),(3,7,9),(4,8,9),(5,6,7),(5,7,8),
]


def multiply(g: tuple[int, int], h: tuple[int, int]) -> tuple[int, int]:
    a, b = g
    c, d = h
    return ((a + (-1 if b else 1) * c) % 4, (b + d) % 2)


def inverse(g: tuple[int, int]) -> tuple[int, int]:
    a, b = g
    return ((-((-1 if b else 1) * a)) % 4, b)


def directed(edge, group_element, u, v):
    if (u, v) == edge:
        return group_element
    if (v, u) == edge:
        return inverse(group_element)
    return IDENTITY


@lru_cache(maxsize=1)
def hypotheses():
    rows = [tuple()]
    rows.extend(((edge, g),) for edge in EDGES for g in FAULTS)
    rows.extend(
        ((edge, g), (other, h))
        for edge, other in itertools.combinations(EDGES, 2)
        for g in FAULTS
        for h in FAULTS
    )
    assert len(rows) == 48_826
    return rows


def syndrome(hypothesis, selected):
    out = []
    for triangle_index in selected:
        i, j, k = TRIANGLES[triangle_index]
        product = IDENTITY
        for u, v in ((i, j), (j, k), (k, i)):
            edge_value = IDENTITY
            for edge, g in hypothesis:
                edge_value = multiply(directed(edge, g, u, v), edge_value)
            product = multiply(edge_value, product)
        out.append(D4_INDEX[product])
    return tuple(out)


def syndrome_matrix(selected=range(120)):
    return np.asarray(
        [syndrome(hypothesis, selected) for hypothesis in hypotheses()],
        dtype=np.uint8,
    )


def sparse_prior():
    p0, p1, p2 = 0.995, 0.0045, 0.0005
    per_weight = {
        0: p0,
        1: p1 / (45 * 7),
        2: p2 / (comb(45, 2) * 49),
    }
    prior = np.asarray([per_weight[len(row)] for row in hypotheses()], dtype=float)
    assert abs(float(prior.sum()) - 1.0) < 1e-12
    return prior


def frozen_collision_classes(full_syndrome=None):
    if full_syndrome is None:
        full_syndrome = syndrome_matrix()
    frozen_indices = [TRIANGLES.index(t) for t in FROZEN_23]
    groups = defaultdict(list)
    for index, key in enumerate(map(tuple, full_syndrome[:, frozen_indices])):
        groups[key].append(index)
    collisions = [tuple(values) for values in groups.values() if len(values) > 1]
    assert len(groups) == 46_284
    assert len(collisions) == 1_436
    assert max(map(len, collisions)) == 3
    return collisions


def conjugacy_class_id(g):
    a, b = g
    if b == 0:
        if a == 0:
            return 0
        if a == 2:
            return 1
        return 2
    return 3 if a % 2 == 0 else 4
