from __future__ import annotations

"""Explicit branch-selection search on the ordered-path S3 carrier.

Supplement M isolates the first exact S3 completion fibres on the 4320 ordered
nonlocal 2-paths of the self-dual 40-line graph. A natural global model for a
coherent branch choice is:

1. choose one of the three nonlocal quadrangle completions above each ordered
   path;
2. require quadrangle-consistency, meaning that if a quadrangle is selected for
   one of its ordered paths then it is selected for all eight ordered paths it
   contains.

Under that consistency rule the selector becomes an exact-cover problem:

    4320 ordered paths = 540 quadrangles x 8 paths per quadrangle.

This module builds that exact-cover search explicitly and proves that no such
540-quadrangle packet exists. So the missing selector cannot be a bare global
choice of quadrangles; extra cocycle/holonomy data is genuinely required.
"""

from collections import Counter, defaultdict
from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from scripts.w33_h4_orbital_no_go import _canonical_cycle, _line_intersection_graph, _simple_line_graph_cycles


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "w33_h4_branch_selection_search_summary.json"


def _ordered_nonlocal_paths(
    lines: list[tuple[int, int, int, int]],
    line_adjacency: dict[int, set[int]],
) -> list[tuple[int, int, int]]:
    paths: set[tuple[int, int, int]] = set()
    for middle in range(len(lines)):
        for left in sorted(line_adjacency[middle]):
            for right in sorted(line_adjacency[middle]):
                if left == right:
                    continue
                if set(lines[left]) & set(lines[right]):
                    continue
                left_anchor = next(iter(set(lines[left]) & set(lines[middle])))
                right_anchor = next(iter(set(lines[middle]) & set(lines[right])))
                if left_anchor != right_anchor:
                    paths.add((left, middle, right))
    return sorted(paths)


def _nonlocal_quadrangles(
    lines: list[tuple[int, int, int, int]],
) -> list[tuple[int, int, int, int]]:
    quadrangles: set[tuple[int, int, int, int]] = set()
    for cycle in _simple_line_graph_cycles(4):
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        if set(lines[cycle[0]]) & set(lines[cycle[1]]) & set(lines[cycle[2]]) & set(lines[cycle[3]]):
            continue
        if any((set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])) for index in range(2)):
            continue
        quadrangles.add(_canonical_cycle(cycle))
    return sorted(quadrangles)


def _quadrangle_to_paths(
    quadrangle: tuple[int, int, int, int],
) -> tuple[tuple[int, int, int], ...]:
    paths = []
    for index in range(4):
        paths.append((quadrangle[index], quadrangle[(index + 1) % 4], quadrangle[(index + 2) % 4]))
        paths.append((quadrangle[index], quadrangle[(index - 1) % 4], quadrangle[(index - 2) % 4]))
    return tuple(sorted(paths))


def _search_exact_cover(
    rows: list[tuple[int, ...]],
    column_rows: dict[int, set[int]],
    column_count: int,
) -> dict[str, Any]:
    all_columns = frozenset(range(column_count))
    all_rows = frozenset(range(len(rows)))

    visited_nodes = 0

    def search(active_columns: frozenset[int], active_rows: frozenset[int]) -> list[int] | None:
        nonlocal visited_nodes
        visited_nodes += 1
        if not active_columns:
            return []

        min_column = None
        min_options: tuple[int, ...] | None = None
        for column in sorted(active_columns):
            options = tuple(sorted(column_rows[column] & active_rows))
            if not options:
                return None
            if min_options is None or len(options) < len(min_options):
                min_column = column
                min_options = options
                if len(min_options) == 1:
                    break
        assert min_column is not None and min_options is not None

        def row_key(row_id: int) -> tuple[int, int]:
            incidence_sum = sum(len(column_rows[column] & active_rows) for column in rows[row_id])
            return incidence_sum, row_id

        for row_id in sorted(min_options, key=row_key):
            covered_columns = set(rows[row_id])
            conflicting_rows: set[int] = set()
            for column in covered_columns:
                conflicting_rows.update(column_rows[column] & active_rows)
            new_rows = active_rows - conflicting_rows
            new_columns = active_columns - covered_columns
            result = search(frozenset(new_columns), frozenset(new_rows))
            if result is not None:
                return [row_id] + result
        return None

    solution_row_ids = search(all_columns, all_rows)
    return {
        "solution_row_ids": solution_row_ids,
        "visited_nodes": visited_nodes,
        "found_exact_cover": solution_row_ids is not None,
        "selected_row_count": None if solution_row_ids is None else len(solution_row_ids),
    }


@lru_cache(maxsize=1)
def build_branch_selection_search_summary() -> dict[str, Any]:
    lines, line_adjacency = _line_intersection_graph()
    ordered_paths = _ordered_nonlocal_paths(lines, line_adjacency)
    quadrangles = _nonlocal_quadrangles(lines)

    path_index = {path: index for index, path in enumerate(ordered_paths)}
    rows: list[tuple[int, ...]] = []
    column_rows: dict[int, set[int]] = defaultdict(set)
    for quadrangle in quadrangles:
        row = tuple(sorted(path_index[path] for path in _quadrangle_to_paths(quadrangle)))
        row_id = len(rows)
        rows.append(row)
        for column in row:
            column_rows[column].add(row_id)

    target_cover_size = len(ordered_paths) // 8
    search = _search_exact_cover(rows, column_rows, len(ordered_paths))

    path_degree_distribution = Counter(len(column_rows[column]) for column in range(len(ordered_paths)))
    quadrangle_path_count_distribution = Counter(len(row) for row in rows)

    checks = {
        "ordered_path_count_is_4320": len(ordered_paths) == 4_320,
        "nonlocal_quadrangle_count_is_1620": len(quadrangles) == 1_620,
        "every_ordered_path_lies_on_exactly_three_nonlocal_quadrangles": path_degree_distribution == {3: 4_320},
        "every_nonlocal_quadrangle_contains_exactly_eight_ordered_paths": quadrangle_path_count_distribution == {8: 1_620},
        "exact_cover_target_size_is_540_quadrangles": target_cover_size == 540,
        "quadrangle_consistent_exact_cover_search_has_no_solution": search["found_exact_cover"] is False,
    }

    theorem = {
        "the_strongest_quadrangle_consistent_global_branch_model_is_an_exact_cover_problem": (
            checks["ordered_path_count_is_4320"]
            and checks["nonlocal_quadrangle_count_is_1620"]
            and checks["every_ordered_path_lies_on_exactly_three_nonlocal_quadrangles"]
            and checks["every_nonlocal_quadrangle_contains_exactly_eight_ordered_paths"]
            and checks["exact_cover_target_size_is_540_quadrangles"]
        ),
        "that_exact_cover_model_has_no_solution": checks[
            "quadrangle_consistent_exact_cover_search_has_no_solution"
        ],
        "therefore_the_missing_selector_is_not_just_a_global_choice_of_540_nonlocal_quadrangles": (
            checks["exact_cover_target_size_is_540_quadrangles"]
            and checks["quadrangle_consistent_exact_cover_search_has_no_solution"]
        ),
        "interpretation": (
            "A coherent branch law cannot be realized as a bare exact packet of 540 "
            "nonlocal quadrangles covering the 4320 ordered paths once each. The "
            "ordered-path S3 carrier needs additional cocycle/holonomy data beyond "
            "a raw quadrangle subset."
        ),
    }

    return {
        "status": "ok",
        "branch_model": {
            "base_carrier": "ordered_nonlocal_2_paths",
            "consistency_rule": "quadrangle_consistent_branch_choice",
            "ordered_path_count": len(ordered_paths),
            "nonlocal_quadrangle_count": len(quadrangles),
            "target_cover_size": target_cover_size,
        },
        "incidence": {
            "ordered_path_completion_degree_distribution": dict(sorted(path_degree_distribution.items())),
            "quadrangle_ordered_path_degree_distribution": dict(sorted(quadrangle_path_count_distribution.items())),
        },
        "search": {
            "found_exact_cover": search["found_exact_cover"],
            "selected_quadrangle_count": search["selected_row_count"],
            "visited_search_nodes": search["visited_nodes"],
        },
        "checks": checks,
        "theorem": theorem,
    }


def write_summary(path: Path = DEFAULT_OUTPUT) -> Path:
    summary = build_branch_selection_search_summary()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path


def main() -> None:
    print(json.dumps(build_branch_selection_search_summary(), indent=2))


if __name__ == "__main__":
    main()