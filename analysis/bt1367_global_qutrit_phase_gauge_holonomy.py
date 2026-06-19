#!/usr/bin/env python3
"""BT1367: global qutrit phase gauge and skew-quadrangle holonomy.

BT361 proves that every skew pair of W(3,3) lines carries a perfect
matching between the three selector/qutrit phase sheets.  This verifier uses
those matchings as an S3-valued connection on the 40-line skew graph, chooses
a spanning-tree gauge, and then computes the gauge-invariant holonomy around
every simple skew-line quadrangle.

The result is intentionally not flat: every S3 conjugacy class appears.  This
turns the old "choose global phase labels" problem into a precise finite
connection with a measured curvature profile.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from typing import Any

from w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle import (
    build_w33,
    generate_projective_symplectic_group,
    selector_failure_edge_supports,
    sheet_anchor_line,
    sheet_orbit,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1367_global_qutrit_phase_gauge_holonomy.json"
ID3 = (0, 1, 2)


def compose_perm(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def invert_perm(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def perm_order(p: tuple[int, ...]) -> int:
    cur = ID3
    for n in range(1, 7):
        cur = compose_perm(p, cur)
        if cur == ID3:
            return n
    raise AssertionError("S3 order bound exceeded")


def perm_key(p: tuple[int, ...]) -> str:
    return "".join(str(x) for x in p)


def canonical_cycle(cycle: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    vals: list[tuple[int, int, int, int]] = []
    raw = list(cycle)
    for seq in (raw, list(reversed(raw))):
        for i in range(4):
            vals.append(tuple(seq[i:] + seq[:i]))  # type: ignore[arg-type]
    return min(vals)


def all_quadrangles(adjacency: list[set[int]]) -> list[tuple[int, int, int, int]]:
    cycles: set[tuple[int, int, int, int]] = set()
    for a, c in combinations(range(len(adjacency)), 2):
        common = sorted(adjacency[a] & adjacency[c])
        for b, d in combinations(common, 2):
            cycles.add(canonical_cycle((a, b, c, d)))
    return sorted(cycles)


def build_phase_transport() -> dict[str, Any]:
    points, edges, edge_index, lines, _adjacency = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)
    sheet_count = len(sheets)

    intersections = [[0] * sheet_count for _ in range(sheet_count)]
    for left in range(sheet_count):
        for right in range(sheet_count):
            intersections[left][right] = len(sheets[left] & sheets[right])

    anchor_line_by_sheet = [sheet_anchor_line(sheet, edges, lines) for sheet in sheets]
    fiber_by_line: dict[int, list[int]] = defaultdict(list)
    for sheet_index, line_index in enumerate(anchor_line_by_sheet):
        fiber_by_line[line_index].append(sheet_index)
    for line_index in fiber_by_line:
        fiber_by_line[line_index].sort()

    local_phase = {
        line_index: {sheet: phase for phase, sheet in enumerate(fiber)}
        for line_index, fiber in fiber_by_line.items()
    }
    line_sets = [set(line) for line in lines]
    skew_edges: list[tuple[int, int]] = []
    skew_adjacency = [set() for _ in lines]
    transport: dict[tuple[int, int], tuple[int, int, int]] = {}
    matching_rows = []

    for left, right in combinations(range(len(lines)), 2):
        if line_sets[left] & line_sets[right]:
            continue
        skew_edges.append((left, right))
        skew_adjacency[left].add(right)
        skew_adjacency[right].add(left)
        perm: list[int | None] = [None, None, None]
        inv: list[int | None] = [None, None, None]
        for left_sheet in fiber_by_line[left]:
            phase_left = local_phase[left][left_sheet]
            matches = [
                right_sheet
                for right_sheet in fiber_by_line[right]
                if intersections[left_sheet][right_sheet] == 4
            ]
            if len(matches) != 1:
                raise AssertionError((left, right, left_sheet, matches))
            phase_right = local_phase[right][matches[0]]
            perm[phase_left] = phase_right
            inv[phase_right] = phase_left
        fwd = tuple(int(x) for x in perm)
        rev = tuple(int(x) for x in inv)
        transport[(left, right)] = fwd
        transport[(right, left)] = rev
        matching_rows.append(
            {
                "left_line": left,
                "right_line": right,
                "transport": list(fwd),
                "transport_key": perm_key(fwd),
            }
        )

    return {
        "line_count": len(lines),
        "sheet_count": sheet_count,
        "fiber_by_line": fiber_by_line,
        "skew_edges": skew_edges,
        "skew_adjacency": skew_adjacency,
        "transport": transport,
        "matching_rows": matching_rows,
    }


def spanning_tree_gauge(
    skew_adjacency: list[set[int]],
    transport: dict[tuple[int, int], tuple[int, int, int]],
) -> tuple[dict[int, tuple[int, int, int]], dict[int, int | None]]:
    gauge = {0: ID3}
    parent: dict[int, int | None] = {0: None}
    queue: deque[int] = deque([0])
    while queue:
        left = queue.popleft()
        for right in sorted(skew_adjacency[left]):
            if right in gauge:
                continue
            gauge[right] = compose_perm(transport[(left, right)], gauge[left])
            parent[right] = left
            queue.append(right)
    if len(gauge) != len(skew_adjacency):
        raise AssertionError("skew graph is disconnected")
    return gauge, parent


def build_result() -> dict[str, object]:
    data = build_phase_transport()
    skew_edges = data["skew_edges"]
    skew_adjacency = data["skew_adjacency"]
    transport = data["transport"]
    gauge, parent = spanning_tree_gauge(skew_adjacency, transport)

    residual_profile: Counter[str] = Counter()
    residual_order_profile: Counter[int] = Counter()
    for left, right in skew_edges:
        residual = compose_perm(
            invert_perm(gauge[right]),
            compose_perm(transport[(left, right)], gauge[left]),
        )
        residual_profile[perm_key(residual)] += 1
        residual_order_profile[perm_order(residual)] += 1

    quadrangles = all_quadrangles(skew_adjacency)
    holonomy_profile: Counter[str] = Counter()
    holonomy_order_profile: Counter[int] = Counter()
    holonomy_examples: dict[str, list[int]] = {}
    for a, b, c, d in quadrangles:
        hol = compose_perm(
            transport[(d, a)],
            compose_perm(
                transport[(c, d)],
                compose_perm(transport[(b, c)], transport[(a, b)]),
            ),
        )
        key = perm_key(hol)
        holonomy_profile[key] += 1
        holonomy_order_profile[perm_order(hol)] += 1
        holonomy_examples.setdefault(key, [a, b, c, d])

    transport_profile = Counter(row["transport_key"] for row in data["matching_rows"])
    tree_edge_count = len(parent) - 1
    non_tree_edge_count = len(skew_edges) - tree_edge_count
    checks = {
        "all_120_selector_sheets_used": data["sheet_count"] == 120,
        "all_540_skew_line_matchings_used": len(skew_edges) == 540,
        "spanning_tree_gauge_reaches_all_40_lines": len(gauge) == 40,
        "tree_edges_have_identity_residual": residual_profile[perm_key(ID3)]
        >= tree_edge_count,
        "non_tree_edges_match_cycle_rank": non_tree_edge_count == 501,
        "all_skew_quadrangles_enumerated": len(quadrangles) == 59670,
        "quadrangle_holonomy_is_not_flat": holonomy_order_profile[1] < len(quadrangles),
        "all_s3_conjugacy_classes_appear": sorted(holonomy_order_profile) == [1, 2, 3],
        "holonomy_profile_sums_to_quadrangles": sum(holonomy_profile.values())
        == len(quadrangles),
    }

    return {
        "bt": 1367,
        "title": "Global qutrit phase gauge and quadrangle holonomy",
        "verified": all(checks.values()),
        "transport": {
            "base": "BT361 overlap-4 skew-line phase perfect matchings",
            "skew_line_matchings": len(skew_edges),
            "transport_permutation_profile": dict(sorted(transport_profile.items())),
        },
        "spanning_tree_gauge": {
            "root_line": 0,
            "tree_edges": tree_edge_count,
            "non_tree_edges": non_tree_edge_count,
            "residual_profile": dict(sorted(residual_profile.items())),
            "residual_order_profile": {
                str(k): v for k, v in sorted(residual_order_profile.items())
            },
        },
        "quadrangle_holonomy": {
            "quadrangles": len(quadrangles),
            "holonomy_profile": dict(sorted(holonomy_profile.items())),
            "holonomy_order_profile": {
                str(k): v for k, v in sorted(holonomy_order_profile.items())
            },
            "examples": holonomy_examples,
        },
        "interpretation": (
            "The BT361 qutrit phase matchings define a genuine S3 connection "
            "on the W33 line-skew graph.  A global spanning-tree gauge exists, "
            "but the connection is curved: skew-line quadrangles realize "
            "identity, transposition, and 3-cycle holonomies."
        ),
        "boundary": (
            "This measures holonomy of the selector phase connection.  It does "
            "not yet choose a correcting cochain or prove that any corrected "
            "selector is flat."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "quadrangles": result["quadrangle_holonomy"]["quadrangles"],
                "holonomy_order_profile": result["quadrangle_holonomy"][
                    "holonomy_order_profile"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
