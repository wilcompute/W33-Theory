#!/usr/bin/env python3
"""Contextual decryption = local-section gluing obstruction on W(q).

A local "key" chooses exactly one point on every line/context.  A global
noncontextual key is one point-value assignment whose restriction to every line
makes exactly one choice.  For a generalized quadrangle this is precisely an
ovoid.

This finite certificate compares W(2) and W(3):
  * W(2) has six global one-click keys (ovoids).
  * W(3,3) has none.

This is a selection-contextuality/gluing statement.  It is not by itself a
proof of every operator-sign contextuality statement one can formulate on W33.
"""
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CONTEXTUAL_DECRYPTION_OBSTRUCTION.json"


def canon(v, q):
    row = tuple(int(x) % q for x in v)
    for x in row:
        if x:
            inv = pow(x, -1, q)
            return tuple((inv * y) % q for y in row)
    raise ValueError("zero vector")


def symplectic(a, b, q):
    return (a[0]*b[1] - a[1]*b[0] + a[2]*b[3] - a[3]*b[2]) % q


def build_w(q):
    if q not in (2, 3):
        raise ValueError("this exact certificate uses prime q=2,3")
    points = tuple(sorted({
        canon(v, q) for v in product(range(q), repeat=4) if any(v)
    }))
    index = {p: i for i, p in enumerate(points)}
    lines = set()
    for i, j in combinations(range(len(points)), 2):
        a, b = points[i], points[j]
        if symplectic(a, b, q):
            continue
        span = {
            canon(tuple((s*a[k] + t*b[k]) % q for k in range(4)), q)
            for s, t in product(range(q), repeat=2) if (s, t) != (0, 0)
        }
        if len(span) == q + 1:
            lines.add(tuple(sorted(index[p] for p in span)))
    lines = tuple(sorted(lines))
    expected = (q + 1) * (q*q + 1)
    assert len(points) == expected
    assert len(lines) == expected
    assert {len(line) for line in lines} == {q + 1}
    incidences = [set() for _ in points]
    for li, line in enumerate(lines):
        for p in line:
            incidences[p].add(li)
    assert {len(x) for x in incidences} == {q + 1}
    return points, lines, tuple(frozenset(x) for x in incidences)


def enumerate_global_keys(q):
    points, lines, point_lines = build_w(q)
    all_lines = frozenset(range(len(lines)))
    nodes = 0
    solutions = []

    def rec(covered, chosen):
        nonlocal nodes
        nodes += 1
        if covered == all_lines:
            solutions.append(tuple(chosen))
            return
        best = None
        for li in all_lines - covered:
            candidates = [
                p for p in lines[li]
                if point_lines[p].isdisjoint(covered)
            ]
            if not candidates:
                return
            if best is None or len(candidates) < len(best):
                best = candidates
                if len(best) == 1:
                    break
        for p in best:
            rec(covered | point_lines[p], chosen + [p])

    rec(frozenset(), [])
    return {
        "q": q,
        "points": len(points),
        "contexts": len(lines),
        "choices_per_context": q + 1,
        "local_key_space": f"{q+1}^{len(lines)}",
        "required_global_selected_points": len(lines) // (q + 1),
        "global_keys": len(solutions),
        "search_nodes": nodes,
        "example_global_key": list(solutions[0]) if solutions else None,
    }


def verify():
    even = enumerate_global_keys(2)
    odd = enumerate_global_keys(3)
    assert even["global_keys"] == 6
    assert even["required_global_selected_points"] == 5
    assert odd["global_keys"] == 0
    assert odd["required_global_selected_points"] == 10
    return {
        "schema": "w33.contextual-decryption-obstruction.v1",
        "status": "PASS",
        "definition": (
            "A local key picks one point per commuting context. A global classical "
            "key is one context-independent 0/1 valuation whose line sums all equal 1."
        ),
        "control_W2": even,
        "W33": odd,
        "theorem": (
            "The W33 local one-click keys do not glue to a global context-independent "
            "key: the exact-cover set is empty. W(2) is a control where gluing succeeds."
        ),
        "cryptographic_reading": (
            "Classical missing-key randomness can be modeled by one hidden global key. "
            "This W33 selection model exhibits a stronger obstruction: under the one-click "
            "context semantics there is no such global key to reveal."
        ),
        "boundary": (
            "This certificate concerns selection/ovoid contextuality only. It does not "
            "identify all quantum randomness with contextuality, and it does not prove "
            "metaphysical indeterminism."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
