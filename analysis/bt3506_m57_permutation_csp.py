#!/usr/bin/env python3
"""CP-SAT exporter for the edge-rooted Moore(57,2) permutation system.

The base model is exact for the double-fibration constraints. Triangle and
unique-common-neighbor violations are separated iteratively as no-good cuts.
No claim is made that the base model plus a finite unexecuted cut set solves
the missing-Moore problem.
"""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from typing import Any


def model_statistics(n: int = 56) -> dict[str, int]:
    pairs = n * (n - 1) // 2
    return {
        "fibre_size": n,
        "unordered_row_pairs": pairs,
        "independent_permutation_entries": pairs * n,
        "directed_integer_variables": n * (n - 1) * n,
        "one_hot_nonfixed_boolean_baseline": pairs * n * (n - 1),
        "row_pair_all_different": pairs,
        "inverse_channels": pairs,
        "vertex_star_all_different": n * n,
        "gauge_equalities": n - 1,
        "row_triples": n * (n - 1) * (n - 2) // 6,
        "residual_vertex_pairs": n * n * (n * n - 1) // 2,
    }


def build_cp_sat_model(n: int = 56):
    """Return `(model, p)` with `p[i,j,a]` the column reached in row `j`.

    The optional runtime dependency is OR-Tools. Directed arrays let AddInverse
    channel every unordered row pair. Excluding `a` from the domain of
    `p[i,j,a]` forbids residual edges within one column.
    """
    try:
        from ortools.sat.python import cp_model
    except ImportError as exc:
        raise RuntimeError("Install ortools to materialize the CP-SAT model") from exc

    model = cp_model.CpModel()
    p: dict[tuple[int, int, int], Any] = {}
    domains = {
        a: cp_model.Domain.FromValues([value for value in range(n) if value != a])
        for a in range(n)
    }
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            for a in range(n):
                p[i, j, a] = model.NewIntVarFromDomain(domains[a], f"p_{i}_{j}_{a}")

    for i, j in combinations(range(n), 2):
        forward = [p[i, j, a] for a in range(n)]
        reverse = [p[j, i, a] for a in range(n)]
        model.AddAllDifferent(forward)
        model.AddInverse(forward, reverse)

    for i in range(n):
        for a in range(n):
            model.AddAllDifferent([p[i, j, a] for j in range(n) if j != i])

    for j in range(1, n):
        model.Add(p[0, j, 0] == j)

    return model, p


def candidate_from_solver(
    solver: Any,
    p: dict[tuple[int, int, int], Any],
    n: int,
) -> dict[tuple[int, int], tuple[int, ...]]:
    return {
        (i, j): tuple(solver.Value(p[i, j, a]) for a in range(n))
        for i in range(n)
        for j in range(n)
        if i != j
    }


def triangle_violations(
    candidate: dict[tuple[int, int], tuple[int, ...]],
    n: int,
) -> list[tuple[int, int, int, int, int, int]]:
    """Return fixed points of row-triangle holonomy.

    `(i,j,k,a,b,c)` records `i:a -> j:b -> k:c -> i:a`.
    """
    violations = []
    for i, j, k in combinations(range(n), 3):
        for a in range(n):
            b = candidate[i, j][a]
            c = candidate[j, k][b]
            if candidate[k, i][c] == a:
                violations.append((i, j, k, a, b, c))
    return violations


def add_triangle_nogoods(
    model: Any,
    p: dict[tuple[int, int, int], Any],
    violations: list[tuple[int, int, int, int, int, int]],
) -> None:
    """Forbid every concrete three-edge triangle found in a candidate."""
    for i, j, k, a, b, c in violations:
        model.AddForbiddenAssignments(
            [p[i, j, a], p[j, k, b], p[k, i, c]],
            [(b, c, a)],
        )


def residual_neighbors(
    candidate: dict[tuple[int, int], tuple[int, ...]],
    vertex: tuple[int, int],
    n: int,
) -> set[tuple[int, int]]:
    row, column = vertex
    return {
        (other_row, candidate[row, other_row][column])
        for other_row in range(n)
        if other_row != row
    }


def residual_mu_violations(
    candidate: dict[tuple[int, int], tuple[int, ...]],
    n: int,
    *,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    """Check the complete residual lambda=0/mu=1 law.

    A same-row or same-column residual pair already shares one branch vertex,
    so it must have zero common residual neighbors. A pair in different rows
    and columns must have zero residual common neighbors when adjacent and
    exactly one when nonadjacent.
    """
    vertices = [(i, a) for i in range(n) for a in range(n)]
    neighborhoods = {v: residual_neighbors(candidate, v, n) for v in vertices}
    violations: list[dict[str, Any]] = []
    for index, u in enumerate(vertices):
        i, a = u
        for v in vertices[index + 1 :]:
            k, b = v
            adjacent = k != i and candidate[i, k][a] == b
            common = neighborhoods[u] & neighborhoods[v]
            if i == k or a == b or adjacent:
                expected = 0
            else:
                expected = 1
            if len(common) != expected:
                violations.append(
                    {
                        "u": u,
                        "v": v,
                        "adjacent": adjacent,
                        "expected_residual_common": expected,
                        "actual_residual_common": len(common),
                        "common_vertices": sorted(common),
                    }
                )
                if limit is not None and len(violations) >= limit:
                    return violations
    return violations


def pair_star_assignment(
    candidate: dict[tuple[int, int], tuple[int, ...]],
    p: dict[tuple[int, int, int], Any],
    u: tuple[int, int],
    v: tuple[int, int],
    n: int,
) -> tuple[list[Any], tuple[int, ...]]:
    """Return the local variable/value signature determining one mu violation."""
    i, a = u
    k, b = v
    variables: list[Any] = []
    values: list[int] = []

    if i != k:
        variables.append(p[i, k, a])
        values.append(candidate[i, k][a])

    for row in range(n):
        if row == i or row == k:
            continue
        variables.extend([p[i, row, a], p[k, row, b]])
        values.extend([candidate[i, row][a], candidate[k, row][b]])

    if i == k:
        for row in range(n):
            if row == i:
                continue
            variables.extend([p[i, row, a], p[i, row, b]])
            values.extend([candidate[i, row][a], candidate[i, row][b]])

    return variables, tuple(values)


def add_residual_mu_nogoods(
    model: Any,
    p: dict[tuple[int, int, int], Any],
    candidate: dict[tuple[int, int], tuple[int, ...]],
    violations: list[dict[str, Any]],
    n: int,
) -> None:
    """Forbid each concrete local pair-star that violates lambda=0/mu=1.

    These cuts are exact but intentionally lazy. A violation with no common
    neighbor depends on the full pair-star, so a short static clause would be
    unsound; the local signature has at most `2(n-2)+1` directed entries for
    different-row pairs.
    """
    for violation in violations:
        variables, values = pair_star_assignment(
            candidate,
            p,
            tuple(violation["u"]),
            tuple(violation["v"]),
            n,
        )
        if not variables:
            raise AssertionError("empty pair-star no-good")
        model.AddForbiddenAssignments(variables, [values])


def validate_double_fibration(
    candidate: dict[tuple[int, int], tuple[int, ...]],
    n: int,
) -> None:
    expected = set(range(n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            perm = candidate[i, j]
            assert set(perm) == expected
            assert all(perm[a] != a for a in range(n))
            for a, b in enumerate(perm):
                assert candidate[j, i][b] == a
    for i in range(n):
        for a in range(n):
            assert {candidate[i, j][a] for j in range(n) if j != i} == expected - {a}


def solve_base(
    n: int,
    time_limit: float,
    output: Path | None,
    *,
    separate_once: bool = False,
) -> dict[str, Any]:
    from ortools.sat.python import cp_model

    model, p = build_cp_sat_model(n)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    result: dict[str, Any] = {
        "statistics": model_statistics(n),
        "status": solver.StatusName(status),
        "triangle_cuts_added": 0,
        "mu_cuts_added": 0,
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        candidate = candidate_from_solver(solver, p, n)
        validate_double_fibration(candidate, n)
        triangles = triangle_violations(candidate, n)
        mu_violations = residual_mu_violations(candidate, n)
        result["triangle_violations"] = len(triangles)
        result["residual_mu_violations"] = len(mu_violations)

        if separate_once and (triangles or mu_violations):
            add_triangle_nogoods(model, p, triangles)
            add_residual_mu_nogoods(model, p, candidate, mu_violations, n)
            result["triangle_cuts_added"] = len(triangles)
            result["mu_cuts_added"] = len(mu_violations)

        if output:
            serial = {
                f"{i},{j}": list(values)
                for (i, j), values in sorted(candidate.items())
            }
            output.write_text(json.dumps(serial, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=56)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--stats-only", action="store_true")
    parser.add_argument("--separate-once", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.stats_only:
        print(json.dumps(model_statistics(args.n), indent=2, sort_keys=True))
        return
    result = solve_base(
        args.n,
        args.time_limit,
        args.output,
        separate_once=args.separate_once,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
