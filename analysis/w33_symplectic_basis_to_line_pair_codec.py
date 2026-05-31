#!/usr/bin/env python3
"""Symplectic basis -> disjoint isotropic line-pair + 12-codec fiber.

After the ordered spread-transport correction, the right regular object is the
set of ordered symplectic bases of F3^4, size 51840.  This verifier asks what
finite incidence data a basis determines.

For a symplectic basis (a,b,c,d) with <a,c>=1 and <b,d>=1:

    L_in  = P(span(a,b))
    L_out = P(span(c,d))

are disjoint totally isotropic projective lines.  The projective anchor is [a],
which lies on L_in.

The map

    (a,b,c,d) -> ([a], L_in, L_out)

has uniform fiber size 12.

Counts:
    anchors:                         40
    isotropic lines through anchor:    4
    isotropic lines disjoint from L:   27
    codec fiber:                      12

    40 * 4 * 27 * 12 = 51840.

Thus the missing refinement between projective line-pair transport and the full
regular symplectic-basis torsor is exactly a 12-state local codec fiber.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

q = 3


def inv3(x: int) -> int:
    x %= q
    if x == 1:
        return 1
    if x == 2:
        return 2
    raise ValueError("zero")


def normalize(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % q for x in v)
    if not any(v):
        raise ValueError("zero")
    i = next(i for i, x in enumerate(v) if x)
    inv = inv3(v[i])
    return tuple((inv * x) % q for x in v)


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % q


def vectors() -> list[tuple[int, ...]]:
    return [v for v in itertools.product(range(q), repeat=4) if any(v)]


def projective_points() -> list[tuple[int, ...]]:
    return sorted({normalize(v) for v in vectors()})


def span_line(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pts = set()
    for x, y in itertools.product(range(q), repeat=2):
        v = tuple((x * a[i] + y * b[i]) % q for i in range(4))
        if any(v):
            pts.add(normalize(v))
    return tuple(sorted(pts))


def isotropic_lines(points: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    pidx = {p: i for i, p in enumerate(points)}
    raw = sorted({span_line(a, b) for a, b in itertools.combinations(points, 2)})
    iso = [L for L in raw if all(symp(a, b) == 0 for a, b in itertools.combinations(L, 2))]
    return [tuple(sorted(pidx[p] for p in L)) for L in iso]


def rank_mod3(rows: list[tuple[int, ...]]) -> int:
    A = [list(r) for r in rows if any(x % q for x in r)]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        piv = next((i for i in range(rank, m) if A[i][col] % q), None)
        if piv is None:
            col += 1
            continue
        A[rank], A[piv] = A[piv], A[rank]
        inv = inv3(A[rank][col])
        A[rank] = [(x * inv) % q for x in A[rank]]
        for i in range(m):
            if i != rank and A[i][col] % q:
                fac = A[i][col] % q
                A[i] = [(x - fac * y) % q for x, y in zip(A[i], A[rank])]
        rank += 1
        col += 1
    return rank


def line_index_for_pair(a: tuple[int, ...], b: tuple[int, ...], point_index: dict[tuple[int, ...], int], line_index: dict[tuple[int, ...], int]) -> int:
    line = tuple(sorted(point_index[p] for p in span_line(a, b)))
    return line_index[line]


def count_symplectic_basis_line_pair_fibers() -> dict:
    V = vectors()
    P = projective_points()
    pidx = {p: i for i, p in enumerate(P)}
    lines = isotropic_lines(P)
    lidx = {L: i for i, L in enumerate(lines)}
    fibers = Counter()
    total = 0
    sample = None

    for a in V:
        anchor = pidx[normalize(a)]
        for c in V:
            if symp(a, c) != 1:
                continue
            U = [x for x in V if symp(a, x) == 0 and symp(c, x) == 0]
            for b in U:
                if not any(b):
                    continue
                for d in U:
                    if symp(b, d) != 1:
                        continue
                    if rank_mod3([a, b, c, d]) != 4:
                        continue
                    Lin = line_index_for_pair(a, b, pidx, lidx)
                    Lout = line_index_for_pair(c, d, pidx, lidx)
                    key = (anchor, Lin, Lout)
                    fibers[key] += 1
                    total += 1
                    if sample is None:
                        sample = {"a": a, "b": b, "c": c, "d": d, "anchor": anchor, "L_in": Lin, "L_out": Lout}

    # Independent incidence counts.
    line_through_anchor = defaultdict(list)
    for i, L in enumerate(lines):
        for p in L:
            line_through_anchor[p].append(i)
    disjoint_count_by_line = {i: sum(1 for j, M in enumerate(lines) if set(lines[i]).isdisjoint(M)) for i in range(len(lines))}
    valid_line_pair_count = sum(len(line_through_anchor[p]) * 27 for p in range(len(P)))

    return {
        "points": len(P),
        "lines": len(lines),
        "total_bases": total,
        "image_size": len(fibers),
        "fiber_size_distribution": dict(Counter(fibers.values())),
        "sample": sample,
        "lines_through_anchor_distribution": dict(Counter(len(v) for v in line_through_anchor.values())),
        "disjoint_lines_per_line_distribution": dict(Counter(disjoint_count_by_line.values())),
        "valid_anchor_line_pair_count": valid_line_pair_count,
    }


def build_payload() -> dict:
    counts = count_symplectic_basis_line_pair_fibers()
    identities = {
        "points_lines": counts["points"] == 40 and counts["lines"] == 40,
        "symplectic_basis_count_51840": counts["total_bases"] == 51840,
        "image_size_4320": counts["image_size"] == 40 * 4 * 27 == 4320,
        "uniform_codec_fiber_12": counts["fiber_size_distribution"] == {12: 4320},
        "lines_through_each_anchor_4": counts["lines_through_anchor_distribution"] == {4: 40},
        "disjoint_lines_per_line_27": counts["disjoint_lines_per_line_distribution"] == {27: 40},
        "factorization": 40 * 4 * 27 * 12 == 51840,
    }
    return {
        "theorem": "symplectic_basis_to_line_pair_codec",
        "map": "(a,b,c,d) -> ([a], P(span(a,b)), P(span(c,d)))",
        "counts": counts,
        "factorization": {
            "anchors": 40,
            "input_lines_through_anchor": 4,
            "output_lines_disjoint_from_input_line": 27,
            "local_codec_fiber": 12,
            "total": "40*4*27*12=51840",
        },
        "interpretation": {
            "meaning": "A symplectic basis projects to an anchored ordered pair of disjoint isotropic lines plus a 12-state local codec.",
            "connection_to_previous": "The arbitrary spread-pair model had the right total count but multiple orbit types; this line-pair + 12-codec map exposes a uniform local refinement of the regular symplectic-basis torsor.",
            "why_12_matters": "The missing orientation/basis information over each projective line-pair is exactly the recurring 12-flag codec denominator.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_symplectic_basis_to_line_pair_codec.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
