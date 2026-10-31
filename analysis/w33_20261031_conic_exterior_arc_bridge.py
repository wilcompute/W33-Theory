"""Exact prime-field audit of the Pass 12489 matching/exterior-arc dictionary.

Run from any directory. Uses only the standard library. This is a dictionary to
classical geometry, not a new classification or a physical theory.
"""
from itertools import combinations
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
INF = "inf"


def cross(u, v, q):
    return ((u[1]*v[2]-u[2]*v[1]) % q,
            (u[2]*v[0]-u[0]*v[2]) % q,
            (u[0]*v[1]-u[1]*v[0]) % q)


def dot(u, v, q):
    return sum(x*y for x, y in zip(u, v)) % q


def normalize(v, q):
    z = next(x for x in v if x % q)
    return tuple(x * pow(z, -1, q) % q for x in v)


def conic(t, q):
    return (1, 0, 0) if t == INF else (t*t % q, t, 1)


def chord(pair, q):
    return cross(conic(pair[0], q), conic(pair[1], q), q)


def pole(pair, q):
    # C: Y^2-XZ=0. Polar of P is (-Pz, 2Py, -Px).
    a, b, c = chord(pair, q)
    return normalize((-c, b * pow(2, -1, q) % q, -a), q)


def character(x, q):
    x %= q
    if not x:
        return 0
    return 1 if pow(x, (q-1)//2, q) == 1 else -1


def line_type(line, q):
    a, b, c = line
    return character(b*b - 4*a*c, q)  # -1 external, 0 tangent, +1 secant


def exterior_compatible(pair1, pair2, q):
    return line_type(cross(pole(pair1, q), pole(pair2, q), q), q) == -1


def collinear(pairs, q):
    a, b, c = [pole(p, q) for p in pairs]
    return dot(cross(a, b, q), c, q) == 0


def matchings(items):
    if not items:
        yield ()
        return
    a = items[0]
    for i, b in enumerate(items[1:], 1):
        for tail in matchings(items[1:i] + items[i+1:]):
            yield ((a, b),) + tail


def exterior_arc(matching, q):
    return (all(exterior_compatible(a, b, q) for a, b in combinations(matching, 2))
            and not any(collinear(t, q) for t in combinations(matching, 3)))


def projective_points(q):
    return [(1, a, b) for a in range(q) for b in range(q)] + [(0, 1, a) for a in range(q)] + [(0, 0, 1)]


def stopping_set_audit(matching, q):
    """Exhaust all projective lines: no 1-secant, but 3-secants exist.

    Thus the union is an LDPC stopping set, NOT a binary even codeword.
    """
    points = {conic(t, q) for t in [INF] + list(range(q))}
    points = {normalize(p, q) for p in points} | {pole(p, q) for p in matching}
    counts = {}
    for line in projective_points(q):
        n = sum(dot(line, p, q) == 0 for p in points)
        counts[str(n)] = counts.get(str(n), 0) + 1
    n2 = 3*(q+1)*(q+3)//8
    n3 = (q*q-1)//4
    expected = {"0": q*q+q+1-n2-n3, "2": n2, "3": n3}
    assert counts == expected, (q, counts, expected)
    assert len(points) == 3*(q+1)//2
    return {"size": len(points), "line_intersection_histogram": counts,
            "stopping_set": True, "binary_even_codeword": False}


def audit(q):
    # Import the existing independent cross-ratio/Moebius implementation.
    sys.path.insert(0, str(ROOT / "analysis/search_drivers_12466"))
    from chord_condition import cr, good, involutions, mob
    pts = [INF] + list(range(q))
    squares = {x*x % q for x in range(1, q)}
    invs = involutions(q)
    pair_checks = triple_checks = 0
    for four in combinations(pts, 4):
        for a, b in matchings(four):
            assert exterior_compatible(a, b, q) == (cr(*a, *b, q) not in squares)
            pair_checks += 1
    # Independent projective determinant versus the repo's involution criterion.
    # Testing every involution per triple at q=13 would be wasteful; derive each
    # involution's swapped pairs once and compare sets of concurrent triples.
    involution_triples = set()
    for M in invs:
        swapped = [tuple(sorted((x, mob(x, M, q)), key=str)) for x in pts
                   if mob(x, M, q) != x]
        swapped = set(swapped)
        for t in combinations(sorted(swapped, key=str), 3):
            involution_triples.add(frozenset(t))
    for six in combinations(pts, 6):
        for m in matchings(six):
            key = frozenset(tuple(sorted(p, key=str)) for p in m)
            assert collinear(m, q) == (key in involution_triples)
            triple_checks += 1
    # Enumerate geometrically; cross-check the surviving matchings with old code.
    survivors = [m for m in matchings(tuple(pts)) if exterior_arc(m, q)]
    assert all(good(m, q, squares, invs) for m in survivors)
    controls = {3: 3, 5: 0, 7: 14, 11: 22, 13: 0}
    assert len(survivors) == controls[q]
    return {"q": q, "pair_predicate_checks": pair_checks,
            "triple_predicate_checks": triple_checks,
            "exterior_arc_matchings": len(survivors),
            "example_matching": survivors[0] if survivors else None,
            "conic_union": stopping_set_audit(survivors[0], q) if survivors else None}


def main():
    result = {"status": "exact finite verification; literature classification credited",
              "scope": "computations over prime fields 3,5,7,11,13; theorem over odd prime powers",
              "sources": ["https://doi.org/10.1007/BF01204717", "https://arxiv.org/abs/1201.0484"],
              "prior_repo": ["analysis/PASS12482_12489_EVEN_LINE_SETS_PAIR_STRUCTURE.md",
                             "analysis/PASS12490_12497_MOORE_FAMILY_HS_EXCLUSION.md"],
              "cases": []}
    for q in (3, 5, 7, 11, 13):
        row = audit(q)
        result["cases"].append(row)
        print(json.dumps(row), flush=True)
    path = ROOT / "data/w33_20261031_conic_exterior_arc_bridge.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
