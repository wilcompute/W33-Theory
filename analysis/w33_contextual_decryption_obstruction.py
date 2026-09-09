#!/usr/bin/env python3
"""Contextual decryption = local-section gluing obstruction on W(q).

A local "key" chooses exactly one point on every line/context. A global
noncontextual key is one point-value assignment whose restriction to every line
makes exactly one choice. For a generalized quadrangle this is precisely an
ovoid.

This certificate now joins four layers which must not be conflated:
  * W(2) has six Boolean global keys (positive control).
  * W(3,3) has no Boolean global key at all.
  * therefore the Abramsky-Barbosa contextual fraction for the W33 KS support
    is 1 (strong contextuality).
  * nevertheless the best *near*-global marking satisfies 36/40 contexts, so
    the KS satisfiability defect is 4/40 = 1/10.

It additionally probes a naive Cech-style linear relaxation Mx=1. The
relaxation is soluble over F2 and F3 even though Boolean gluing fails. That
negative result is important: the simple linearized probe does NOT supply a
cohomological witness for W33. Cohomological obstructions are sufficient but
not complete detectors of contextuality.

"Decryption key" is an information-theoretic reading of observer side
information, not a composable cryptographic-security theorem.
"""

from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CONTEXTUAL_DECRYPTION_OBSTRUCTION.json"


def load(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


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


def incidence_matrix(lines, npoints):
    matrix = [[0] * npoints for _ in lines]
    for i, line in enumerate(lines):
        for p in line:
            matrix[i][p] = 1
    return matrix


def solve_mod_p(matrix, rhs, p):
    """Gauss-Jordan solve A x = b over the prime field F_p."""
    aug = [[x % p for x in row] + [b % p] for row, b in zip(matrix, rhs)]
    rows, cols = len(aug), len(aug[0]) - 1
    pivots = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if aug[i][c] % p), None)
        if pivot is None:
            continue
        aug[r], aug[pivot] = aug[pivot], aug[r]
        inv = pow(aug[r][c] % p, -1, p)
        aug[r] = [(x * inv) % p for x in aug[r]]
        for i in range(rows):
            if i != r and aug[i][c] % p:
                factor = aug[i][c] % p
                aug[i] = [(x - factor*y) % p for x, y in zip(aug[i], aug[r])]
        pivots.append(c)
        r += 1
    inconsistent = any(
        all(aug[i][c] % p == 0 for c in range(cols)) and aug[i][-1] % p
        for i in range(rows)
    )
    solution = [0] * cols
    if not inconsistent:
        for row, c in enumerate(pivots):
            solution[c] = aug[row][-1] % p
    return {
        "field": f"F_{p}",
        "rank": r,
        "solvable": not inconsistent,
        "solution_support": sum(bool(x) for x in solution) if not inconsistent else None,
        "solution": solution if not inconsistent else None,
    }


def context_pair_profile(lines):
    intersecting = sum(
        1 for a, b in combinations(lines, 2) if set(a).intersection(b)
    )
    total = len(lines) * (len(lines) - 1) // 2
    return {"intersecting": intersecting, "skew": total - intersecting}


def verify():
    even = enumerate_global_keys(2)
    odd = enumerate_global_keys(3)
    points3, lines3, _ = build_w(3)
    pair_profile = context_pair_profile(lines3)
    matrix = incidence_matrix(lines3, len(points3))
    linear_f2 = solve_mod_p(matrix, [1] * len(lines3), 2)
    linear_f3 = solve_mod_p(matrix, [1] * len(lines3), 3)

    p1080 = load("data/w33_pass1080_contextual_fraction_audit.json")
    p1099 = load("data/w33_pass1099_exact_ks_maximum.json")
    cf = p1080["contextual_fraction"]["W33"]
    exact_max = p1099["exact_maximum_satisfiable_contexts"]
    total_contexts = p1099["total_contexts"]

    assert even["global_keys"] == 6
    assert even["required_global_selected_points"] == 5
    assert odd["global_keys"] == 0
    assert odd["required_global_selected_points"] == 10
    assert cf["ovoids"] == 0 and cf["value"] == 1.0
    assert exact_max == 36 and total_contexts == 40
    assert p1099["defect"] == "1/10"
    assert pair_profile == {"intersecting": 240, "skew": 540}
    assert linear_f2["solvable"] and linear_f3["solvable"]

    return {
        "schema": "w33.contextual-decryption-obstruction.v2",
        "status": "PASS",
        "definition": (
            "A local key picks one point per commuting context. A global classical "
            "key is one context-independent 0/1 valuation whose line sums all equal 1."
        ),
        "measurement_cover": {
            "measurements": 40,
            "contexts": 40,
            "local_one_hot_sections_per_context": 4,
            "total_local_sections": 160,
            "context_pair_profile": pair_profile,
        },
        "control_W2": even,
        "W33": odd,
        "global_section_theorem": (
            "The W33 local one-click keys do not glue to a global context-independent "
            "key: the exact-cover set is empty. W(2) is a control where gluing succeeds."
        ),
        "contextuality_quantities": {
            "abramsky_barbosa_contextual_fraction": cf["value"],
            "global_sections_ovoids": cf["ovoids"],
            "near_global_max_satisfied_contexts": exact_max,
            "total_contexts": total_contexts,
            "ks_satisfiability_defect": p1099["defect"],
            "distinction": (
                "CF=1 and defect=1/10 are different observables. Strong contextuality "
                "means no exact global section; the 1/10 defect measures how close the "
                "best Boolean marking gets, namely 36/40."
            ),
        },
        "linearized_cohomology_probe": {
            "construction": (
                "Use the 40x40 context-ray incidence matrix M and solve Mx=1 over "
                "finite fields. This is a deliberately weak linear relaxation of "
                "one-hot Boolean gluing, not the full event-sheaf obstruction."
            ),
            "F2": linear_f2,
            "F3": linear_f3,
            "verdict": (
                "Both linear systems are soluble. Therefore this naive linearized "
                "probe does not witness the contextuality even though the exact Boolean "
                "global-section obstruction is absolute. Do not report a nonzero "
                "cohomology class from this relaxation."
            ),
        },
        "cryptographic_reading": (
            "Classical missing-key randomness can be modeled by one hidden global key. "
            "This W33 selection model exhibits a stronger obstruction: under the one-click "
            "context semantics there is no such global key to reveal."
        ),
        "boundary": (
            "This certificate concerns selection/ovoid contextuality. The decryption "
            "language is an observer-information interpretation, not a proof of QKD "
            "secrecy, composability, computational hardness, or metaphysical indeterminism."
        ),
        "sources": {
            "strong_contextuality": "data/w33_pass1080_contextual_fraction_audit.json",
            "near_global_optimum": "data/w33_pass1099_exact_ks_maximum.json",
            "cohomology_literature_boundary": (
                "Abramsky-Mansfield-Barbosa: cohomological obstruction is sufficient "
                "but not necessary; later work gives explicit incompleteness results."
            ),
        },
    }


if __name__ == "__main__":
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
