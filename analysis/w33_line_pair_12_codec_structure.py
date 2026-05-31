#!/usr/bin/env python3
"""Explicit structure of the 12-codec fiber over an anchored disjoint line pair.

Previous theorem:
    ordered symplectic bases (a,b,c,d) map to ([a], L_in, L_out), where
    L_in=P(span(a,b)) and L_out=P(span(c,d)).  The fiber size is uniformly 12.

This verifier identifies the 12 states exactly.

For a fixed projective anchor A=[a], input isotropic line U=L_in through A, and
output isotropic line V=L_out disjoint from U:

    1. choose an actual representative a of A: 2 choices;
    2. choose b in U not in <a>: 6 choices = 3 projective non-anchor points * 2 signs;
    3. the pair (c,d) in V is then uniquely forced by the duality equations

           <a,c>=1, <b,d>=1, <a,d>=0, <b,c>=0.

Thus the 12-codec fiber is not mysterious:

    12 = 2 * 6 = signs(anchor) * oriented non-anchor vector on L_in.

Equivalently, it is the set of ordered bases (a,b) of the 2D input line U with
first projective point fixed to A; the output basis (c,d) is the unique symplectic
dual basis in V.
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


def subspace_vectors(line: tuple[int, ...], points: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    out = {(0, 0, 0, 0)}
    for pidx in line:
        p = points[pidx]
        out.add(p)
        out.add(tuple((2 * x) % q for x in p))
    return out


def point_representatives(point: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [point, tuple((2 * x) % q for x in point)]


def solve_dual_basis(a: tuple[int, ...], b: tuple[int, ...], V: set[tuple[int, ...]]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    nonzero_V = [x for x in V if any(x)]
    sols = []
    for c in nonzero_V:
        if symp(a, c) != 1 or symp(b, c) != 0:
            continue
        for d in nonzero_V:
            if symp(a, d) == 0 and symp(b, d) == 1:
                sols.append((c, d))
    return sols


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


def is_symplectic_basis(a, b, c, d) -> bool:
    return (
        rank_mod3([a, b, c, d]) == 4
        and symp(a, c) == 1
        and symp(b, d) == 1
        and symp(a, b) == symp(a, d) == symp(b, c) == symp(c, d) == 0
    )


def analyze() -> dict:
    points = projective_points()
    lines = isotropic_lines(points)
    # Choose a deterministic anchored disjoint pair.
    anchor = 0
    L_in = next(i for i, L in enumerate(lines) if anchor in L)
    L_out = next(j for j, M in enumerate(lines) if set(lines[L_in]).isdisjoint(M))
    U = subspace_vectors(lines[L_in], points)
    V = subspace_vectors(lines[L_out], points)
    anchor_vecs = point_representatives(points[anchor])

    constructed = []
    dual_solution_counts = Counter()
    b_projective_counter = Counter()
    for a in anchor_vecs:
        b_choices = [b for b in U if any(b) and normalize(b) != points[anchor]]
        for b in b_choices:
            sols = solve_dual_basis(a, b, V)
            dual_solution_counts[len(sols)] += 1
            if len(sols) == 1:
                c, d = sols[0]
                constructed.append((a, b, c, d))
                b_projective_counter[normalize(b)] += 1

    valid = [is_symplectic_basis(*basis) for basis in constructed]
    c_projective_counter = Counter(normalize(c) for _, _, c, _ in constructed)
    d_projective_counter = Counter(normalize(d) for _, _, _, d in constructed)

    # Compare against brute force fiber for this anchored line pair.
    brute = []
    for a in vectors():
        if normalize(a) != points[anchor]:
            continue
        for b in U:
            if not any(b):
                continue
            for c in V:
                if not any(c):
                    continue
                for d in V:
                    if not any(d):
                        continue
                    if is_symplectic_basis(a, b, c, d):
                        brute.append((a, b, c, d))
    constructed_set = set(constructed)
    brute_set = set(brute)

    return {
        "anchor": anchor,
        "L_in": L_in,
        "L_out": L_out,
        "L_in_points": lines[L_in],
        "L_out_points": lines[L_out],
        "anchor_representatives": anchor_vecs,
        "constructed_count": len(constructed),
        "brute_force_fiber_count": len(brute),
        "constructed_equals_brute": constructed_set == brute_set,
        "dual_solution_count_distribution": dict(dual_solution_counts),
        "all_constructed_are_symplectic_bases": all(valid),
        "b_projective_distribution": {str(k): v for k, v in b_projective_counter.items()},
        "c_projective_distribution": {str(k): v for k, v in c_projective_counter.items()},
        "d_projective_distribution": {str(k): v for k, v in d_projective_counter.items()},
        "sample_states": constructed[:12],
    }


def build_payload() -> dict:
    a = analyze()
    identities = {
        "constructed_count_12": a["constructed_count"] == 12,
        "brute_force_fiber_count_12": a["brute_force_fiber_count"] == 12,
        "constructed_equals_brute": a["constructed_equals_brute"],
        "unique_dual_basis_for_each_a_b": a["dual_solution_count_distribution"] == {1: 12},
        "all_constructed_are_symplectic_bases": a["all_constructed_are_symplectic_bases"],
        "b_projective_three_points_two_signs_each": sorted(a["b_projective_distribution"].values()) == [4, 4, 4] or sorted(a["b_projective_distribution"].values()) == [4, 4, 4],
    }
    # For b, each of the three non-anchor projective points appears 4 times across 12 states:
    # two a signs times two b signs.
    return {
        "theorem": "line_pair_12_codec_structure",
        "statement": "The 12 fiber states over ([a], L_in, L_out) are exactly signed anchor representatives times non-anchor input-line vectors; the output basis is uniquely forced by symplectic duality.",
        "analysis": a,
        "codec_dictionary": {
            "2": "choice of actual representative a of projective anchor [a]",
            "6": "choice of b in L_in not proportional to a: three non-anchor projective points times two signs",
            "12": "2*6 ordered input-line bases (a,b); each has a unique dual output basis (c,d) in L_out",
        },
        "interpretation": {
            "basis_orientation": "The local 12-codec is an oriented/signed basis codec on the input isotropic line with first projective point fixed.",
            "dual_forcing": "Once (a,b) is chosen, the disjoint output line supplies a unique symplectic dual pair (c,d).",
            "tetrahedral_hint": "12 = oriented edge choices of a 4-point projective line with one point fixed: three target points times two signs times two anchor signs.",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_line_pair_12_codec_structure.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
