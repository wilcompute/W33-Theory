#!/usr/bin/env python3
"""
BT672 — executable K44 -> K33 frame quotient verifier.

This verifies the BT669 statement:

    Match(K_{4,4}) ~= S4,
    six one-factorization frames ~= S4/V4 ~= S3,
    Cay(S3, transpositions) ~= K_{3,3}.

The script is deliberately standalone and integer/combinatorial only.
"""
from __future__ import annotations

from itertools import permutations, combinations


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Composition p after q, acting on 0..n-1."""
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def parity(p: tuple[int, ...]) -> int:
    inv_count = 0
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            if p[i] > p[j]:
                inv_count += 1
    return inv_count % 2


def matching_edges(p: tuple[int, int, int, int]) -> frozenset[tuple[int, int]]:
    """Perfect matching of K4,4 encoded by permutation p: E_i -> O_{p_i}."""
    return frozenset((i, p[i]) for i in range(4))


def canonical_v4() -> set[tuple[int, int, int, int]]:
    return {
        (0, 1, 2, 3),  # identity
        (1, 0, 3, 2),  # (01)(23)
        (2, 3, 0, 1),  # (02)(13)
        (3, 2, 1, 0),  # (03)(12)
    }


def conjugation_quotient_label(p: tuple[int, int, int, int], v4: set[tuple[int, int, int, int]]) -> tuple[int, int, int]:
    """Map S4 -> Aut(V4\{e}) ~= S3 by conjugation."""
    identity = (0, 1, 2, 3)
    nontrivial = sorted(v for v in v4 if v != identity)
    index = {v: i for i, v in enumerate(nontrivial)}
    pinv = inv(p)
    image = []
    for v in nontrivial:
        c = compose(compose(p, v), pinv)
        image.append(index[c])
    return tuple(image)


def main() -> None:
    s4 = set(permutations(range(4)))
    v4 = canonical_v4()
    identity4 = (0, 1, 2, 3)

    # Basic group checks.
    assert len(s4) == 24
    assert len(v4) == 4
    assert identity4 in v4
    for a in v4:
        for b in v4:
            assert compose(a, b) in v4

    # Perfect matchings of K4,4.
    matchings = {p: matching_edges(p) for p in s4}
    assert len(matchings) == 24
    for edges in matchings.values():
        assert len(edges) == 4
        assert len({e for e, _ in edges}) == 4
        assert len({o for _, o in edges}) == 4

    # Six one-factorization frames are cosets of V4 in S4.
    frames: list[frozenset[tuple[int, int, int, int]]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for g in sorted(s4):
        if g in seen:
            continue
        coset = frozenset(compose(g, v) for v in v4)
        frames.append(coset)
        seen |= set(coset)
    assert len(frames) == 6
    assert sum(len(f) for f in frames) == 24
    assert len(seen) == 24

    # Each frame is a one-factorization: four disjoint matchings covering all 16 K4,4 edges.
    k44_edges = {(e, o) for e in range(4) for o in range(4)}
    for frame in frames:
        union_edges = set()
        for p in frame:
            union_edges |= set(matchings[p])
        assert union_edges == k44_edges
        assert sum(len(matchings[p]) for p in frame) == 16

    # Quotient labels identify frames with S3.
    frame_labels = []
    for frame in frames:
        labels = {conjugation_quotient_label(p, v4) for p in frame}
        assert len(labels) == 1
        frame_labels.append(next(iter(labels)))
    assert len(set(frame_labels)) == 6
    assert set(frame_labels) == set(permutations(range(3)))

    # Cay(S3, transpositions) on the six frame labels.
    transpositions = {p for p in permutations(range(3)) if parity(p) == 1}
    assert len(transpositions) == 3
    edges = set()
    for i, a in enumerate(frame_labels):
        for j, b in enumerate(frame_labels):
            if i >= j:
                continue
            diff = compose(inv(a), b)
            if diff in transpositions:
                edges.add((i, j))
    assert len(edges) == 9

    degrees = {i: 0 for i in range(6)}
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1
    assert set(degrees.values()) == {3}

    even = {i for i, lab in enumerate(frame_labels) if parity(lab) == 0}
    odd = set(range(6)) - even
    assert len(even) == len(odd) == 3
    assert edges == {tuple(sorted((i, j))) for i in even for j in odd}

    metric_matching = []
    # Pair each even label with right-multiplication by a fixed transposition family.
    # This is one admissible metric matching inside K3,3.
    preferred = sorted(transpositions)[0]
    for i in sorted(even):
        target = compose(frame_labels[i], preferred)
        j = frame_labels.index(target)
        metric_matching.append(tuple(sorted((i, j))))
    assert len(set(metric_matching)) == 3
    assert set(metric_matching).issubset(edges)

    print("BT672 K44 -> K33 frame quotient verifier: PASS")
    print(f"perfect_matchings={len(matchings)}")
    print(f"frames={len(frames)}")
    print(f"frame_graph_edges={len(edges)}")
    print(f"bipartition={len(even)}+{len(odd)}")
    print(f"metric_matching={sorted(set(metric_matching))}")


if __name__ == "__main__":
    main()
