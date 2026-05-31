#!/usr/bin/env python3
"""Symplectic-basis regular lift for the 40*36^2 factorization.

The ordered spread-transport orbit test showed that arbitrary projective triples

    (anchor, source spread, target spread)

are not a single regular PSp(4,3) orbit.  This file identifies the correct
regular object of size 51840:

    ordered symplectic bases of F3^4.

A basis (a,b,c,d) is symplectic if

    <a,c> = 1,
    <b,d> = 1,

and all other pairings among basis vectors vanish, with the standard alternating
form.  Such bases are exactly the column images of the standard basis under
Sp(4,3), so Sp(4,3) acts simply transitively on them.

Counting:
    choose a != 0:                         80 choices
    choose c with <a,c>=1:                 27 choices
    choose b in span(a,c)^perp, b != 0:     8 choices
    choose d in span(a,c)^perp, <b,d>=1:    3 choices

    total = 80*27*8*3 = 51840 = |Sp(4,3)|.

Projectivizing the first vector gives 40 anchors.  For each projective anchor,
there are

    2*27*8*3 = 1296 = 36^2

symplectic bases above it.  This is the precise regular meaning of

    51840 = 40 * 36^2.

The arbitrary ordered spread-pair model has the same count per anchor but not a
regular projective orbit.  The symplectic-basis model is the correct regular
linear/Weyl lift.
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


def dot_linear_combo(coeffs: tuple[int, ...], vecs: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sum(c * v[i] for c, v in zip(coeffs, vecs)) % q for i in range(4))


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


def vectors() -> list[tuple[int, ...]]:
    return [v for v in itertools.product(range(q), repeat=4) if any(v)]


def projective_points() -> list[tuple[int, ...]]:
    return sorted({normalize(v) for v in vectors()})


def is_symplectic_basis(a, b, c, d) -> bool:
    vecs = (a, b, c, d)
    if rank_mod3(list(vecs)) != 4:
        return False
    targets = {
        (0, 2): 1,
        (1, 3): 1,
    }
    for i, j in itertools.combinations(range(4), 2):
        val = symp(vecs[i], vecs[j])
        if targets.get((i, j), 0) != val:
            return False
    return True


def count_symplectic_bases_by_construction() -> dict:
    V = vectors()
    projective_anchor_count = Counter()
    first_vector_count = Counter()
    total = 0
    sample = None
    for a in V:
        c_choices = [c for c in V if symp(a, c) == 1]
        for c in c_choices:
            U = [x for x in V if symp(a, x) == 0 and symp(c, x) == 0]
            b_choices = [b for b in U if any(b)]
            for b in b_choices:
                d_choices = [d for d in U if symp(b, d) == 1]
                for d in d_choices:
                    total += 1
                    first_vector_count[a] += 1
                    projective_anchor_count[normalize(a)] += 1
                    if sample is None:
                        sample = (a, b, c, d)
    return {
        "total": total,
        "first_vector_count_distribution": dict(Counter(first_vector_count.values())),
        "projective_anchor_count_distribution": dict(Counter(projective_anchor_count.values())),
        "sample_basis": sample,
        "sample_is_valid": is_symplectic_basis(*sample) if sample else False,
    }


def build_payload() -> dict:
    counts = count_symplectic_bases_by_construction()
    formula_total = 80 * 27 * 8 * 3
    per_projective_anchor = 2 * 27 * 8 * 3
    per_actual_first_vector = 27 * 8 * 3
    identities = {
        "projective_points_40": len(projective_points()) == 40,
        "nonzero_vectors_80": len(vectors()) == 80,
        "construction_total_51840": counts["total"] == 51840,
        "formula_total_51840": formula_total == 51840,
        "per_projective_anchor_36_squared": per_projective_anchor == 36 * 36 == 1296,
        "per_actual_first_vector_648": per_actual_first_vector == 648,
        "count_distribution_per_projective_anchor": counts["projective_anchor_count_distribution"] == {1296: 40},
        "count_distribution_per_first_vector": counts["first_vector_count_distribution"] == {648: 80},
        "sample_basis_valid": counts["sample_is_valid"],
    }
    return {
        "theorem": "symplectic_basis_regular_lift",
        "regular_object": "ordered symplectic bases (a,b,c,d) of F3^4 with <a,c>=1, <b,d>=1, other pairings zero",
        "count_formula": {
            "a_nonzero": 80,
            "c_pairing_one": 27,
            "b_in_orthogonal_complement": 8,
            "d_pairing_one_with_b": 3,
            "total": formula_total,
        },
        "fiber_over_anchor": {
            "projective_anchors": 40,
            "bases_per_projective_anchor": per_projective_anchor,
            "identity": "51840 = 40 * 1296 = 40 * 36^2",
            "bases_per_actual_first_vector": per_actual_first_vector,
        },
        "computed_counts": counts,
        "interpretation": {
            "correction": "arbitrary ordered spread pairs have the same count but split into projective orbit types; ordered symplectic bases are the correct regular linear object",
            "why_regular": "each ordered symplectic basis is the image of the standard basis under a unique element of Sp(4,3)",
            "meaning_of_36_squared": "for each projective anchor, the fiber of symplectic bases has size 36^2, matching ordered local spread-frame transport count at the level of cardinality",
        },
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_symplectic_basis_regular_lift.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
