#!/usr/bin/env python3
"""
BT675 — K3,3 metric-matching automorphism verifier.

This hardens BT672's frame quotient into the Weyl-sized group check:

    Aut(K_{3,3}) has order 72,
    Aut(K_{3,3}, M_metric) has order 12 ~= D6 ~= W(G2).

The graph is the secondary six-frame graph, not the raw 160-flag Levi graph.
"""
from __future__ import annotations

from itertools import permutations


def build_k33():
    plus = [(+1, i) for i in range(3)]
    minus = [(-1, i) for i in range(3)]
    vertices = plus + minus
    edges = {frozenset((p, m)) for p in plus for m in minus}
    matching = {frozenset(((+1, i), (-1, i))) for i in range(3)}
    return vertices, edges, matching


def image_edge(edge, mapping):
    a, b = tuple(edge)
    return frozenset((mapping[a], mapping[b]))


def is_graph_automorphism(vertices, edges, perm):
    mapping = dict(zip(vertices, perm))
    return {image_edge(e, mapping) for e in edges} == edges


def main() -> None:
    vertices, edges, matching = build_k33()
    assert len(vertices) == 6
    assert len(edges) == 9
    degrees = {v: 0 for v in vertices}
    for e in edges:
        for v in e:
            degrees[v] += 1
    assert set(degrees.values()) == {3}

    aut = []
    stabilizer = []
    for perm in permutations(vertices):
        if not is_graph_automorphism(vertices, edges, perm):
            continue
        mapping = dict(zip(vertices, perm))
        aut.append(mapping)
        if {image_edge(e, mapping) for e in matching} == matching:
            stabilizer.append(mapping)

    assert len(aut) == 72
    assert len(stabilizer) == 12

    # Identify the stabilizer as S3 pair permutations times a global side swap.
    pair_permutations = set()
    side_swap_values = set()
    for mapping in stabilizer:
        sigma = []
        for i in range(3):
            image = mapping[(+1, i)]
            sigma.append(image[1])
            side_swap_values.add(image[0])
            # The matched minus endpoint must land in the same matched pair.
            assert mapping[(-1, i)][1] == image[1]
        pair_permutations.add(tuple(sigma))
    assert len(pair_permutations) == 6
    assert side_swap_values == {+1, -1}

    print("BT675 K3,3 metric automorphism verifier: PASS")
    print("Aut(K3,3)=72")
    print("Aut(K3,3,M_metric)=12 ~= D6 ~= W(G2)")
    print("boundary=secondary frame quotient only")


if __name__ == "__main__":
    main()
