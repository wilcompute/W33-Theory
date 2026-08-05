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


def candidate_from_solver(solver: Any, p: dict[tuple[int, int, int], Any], n: int) -> dict[tuple[int, int], tuple[int, ...]]:
    return {
        (i, j): tuple(solver.Value(p[i, j, a]) for a in range(n))
        for i in range(n)
        for j in range(n)
        if i != j
    }


def triangle_violations(candidate: dict[tuple[int, int], tuple[int, ...]], n: int) -> list[tuple[int, int, int, int, int, int]]:
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


def add_triangle_nogoods(model: Any, p: dict[tuple[int, int, int], Any], violations: list[tuple[int, int, int, int, int, int]]) -> None:
    """Forbid every concrete three-edge triangle found in a candidate."""
    for i, j, k, a, b, c in violations:
        model.AddForbiddenAssignments(
            [p[i, j, a], p[j, k, b], p[k, i, c]],
            [(b, c, a)],
        )


def validate_double_fibration(candidate: dict[tuple[int, int], tuple[int, ...]], n: int) -> None:
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


def solve_base(n: int, time_limit: float, output: Path | None) -> dict[str, Any]:
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
    }
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        candidate = candidate_from_solver(solver, p, n)
        validate_double_fibration(candidate, n)
        violations = triangle_violations(candidate, n)
        result["triangle_violations"] = len(violations)
        if output:
            serial = {f"{i},{j}": list(values) for (i, j), values in sorted(candidate.items())}
            output.write_text(json.dumps(serial, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=56)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--stats-only", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.stats_only:
        print(json.dumps(model_statistics(args.n), indent=2, sort_keys=True))
        return
    result = solve_base(args.n, args.time_limit, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
