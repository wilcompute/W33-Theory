#!/usr/bin/env python3
"""Search a literal Hamming/Fano functor for the 72-coordinate horizon code.

The earlier parameter bridge was:

    binary Hamming [7,4,3]_2 has 2^3 = 8 syndrome/coset labels,
    horizon length is 72 = 9 * 8.

This file tries the next concrete thing: label every coordinate in the
explicit 72-coordinate F3 horizon model by one of those 8 binary labels.

The useful model is the tetrahedral Fano plane:

    seven nonzero Fano labels = 4 vertices of K4 + 3 parallel directions.

The six F3 parity checks are the six K4 edges.  A distinct-column horizon
coordinate lives on one K4 edge; a same-column coordinate lives on the K4
star through that column.  The construction below is a gauge-fixed balanced
lift: each of the eight Hamming labels receives exactly nine coordinates.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_hamming_horizon_functor_search.json"

Q = 3
ROWS = range(Q)
COLUMNS = range(4)
COL_BITS = {
    0: (0, 0),
    1: (1, 0),
    2: (0, 1),
    3: (1, 1),
}
BITS_COL = {bits: col for col, bits in COL_BITS.items()}
COL_PAIRS = list(combinations(COLUMNS, 2))
DIRECTIONS = [(1, 0), (0, 1), (1, 1)]


def xor2(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def col_direction(a: int, b: int) -> tuple[int, int]:
    return xor2(COL_BITS[a], COL_BITS[b])


def pair_name(pair: tuple[int, int]) -> str:
    return f"P{pair[0]}{pair[1]}"


def vertex_label(col: int) -> str:
    a, b = COL_BITS[col]
    return f"V{a}{b}"


def direction_label(direction: tuple[int, int]) -> str:
    return f"D{direction[0]}{direction[1]}"


def hamming_bits(label: str) -> tuple[int, int, int]:
    if label == "Z":
        return (0, 0, 0)
    if label.startswith("V"):
        return (1, int(label[1]), int(label[2]))
    if label.startswith("D"):
        return (0, int(label[1]), int(label[2]))
    raise ValueError(label)


def fano_line(pair: tuple[int, int]) -> tuple[str, str, str]:
    a, b = pair
    return (
        vertex_label(a),
        vertex_label(b),
        direction_label(col_direction(a, b)),
    )


def star_support(col: int) -> tuple[str, ...]:
    return tuple(pair_name(tuple(sorted((col, other)))) for other in COLUMNS if other != col)


def direction_pairs(direction: tuple[int, int]) -> list[tuple[int, int]]:
    pairs = [pair for pair in COL_PAIRS if col_direction(*pair) == direction]
    assert len(pairs) == 2
    return pairs


def canonical_special_pairs(column_origin: int = 0) -> dict[tuple[int, int], tuple[int, int]]:
    """Pick one parallel K4 edge per direction through a column-origin gauge."""
    out = {}
    for direction in DIRECTIONS:
        mate = BITS_COL[xor2(COL_BITS[column_origin], direction)]
        out[direction] = tuple(sorted((column_origin, mate)))
    return out


def mixed_label(
    pair: tuple[int, int],
    row_at_left_col: int,
    row_at_right_col: int,
    *,
    row_origin: int,
    residual_delta: int,
    special_pairs: dict[tuple[int, int], tuple[int, int]],
) -> str:
    """Label a mixed edge using a balanced row-origin residual rule.

    With columns ordered as the K4 pair (left, right), the four mixed edges
    not starting at the row-origin split two/two to the endpoint vertices.
    The two residual row-origin edges become the zero sheet, except one
    selected residual on the special parallel pair for the direction, which
    goes to the direction label.
    """
    left, right = pair
    delta = (row_at_right_col - row_at_left_col) % Q
    if delta == 0:
        raise ValueError("mixed edges must have different rows")

    if row_at_left_col != row_origin:
        if delta == 1:
            return vertex_label(left)
        return vertex_label(right)

    direction = col_direction(left, right)
    if pair == special_pairs[direction] and delta == residual_delta:
        return direction_label(direction)
    return "Z"


def build_assignment(
    *,
    row_origin: int = 0,
    column_origin: int = 0,
    residual_delta: int = 1,
) -> list[dict[str, Any]]:
    special_pairs = canonical_special_pairs(column_origin)
    coords: list[dict[str, Any]] = []

    def append_coord(**item: Any) -> None:
        item["hamming_bits"] = hamming_bits(item["label"])
        coords.append(item)

    for row in ROWS:
        for pair in COL_PAIRS:
            direction = col_direction(*pair)
            append_coord(
                kind="row_edge",
                row=row,
                columns=list(pair),
                pair=pair_name(pair),
                support=[pair_name(pair)],
                fano_line=list(fano_line(pair)),
                label=direction_label(direction),
                incidence_ok=True,
            )

    for col in COLUMNS:
        for r0, r1 in combinations(ROWS, 2):
            label = vertex_label(col)
            append_coord(
                kind="column_edge",
                column=col,
                rows=[r0, r1],
                support=list(star_support(col)),
                fano_line=[label],
                label=label,
                incidence_ok=True,
            )

    for pair in COL_PAIRS:
        line = set(fano_line(pair))
        for left_row, right_row in product(ROWS, ROWS):
            if left_row == right_row:
                continue
            label = mixed_label(
                pair,
                left_row,
                right_row,
                row_origin=row_origin,
                residual_delta=residual_delta,
                special_pairs=special_pairs,
            )
            append_coord(
                kind="mixed_edge",
                rows=[left_row, right_row],
                columns=list(pair),
                pair=pair_name(pair),
                support=[pair_name(pair)],
                fano_line=list(fano_line(pair)),
                label=label,
                incidence_ok=(label == "Z" or label in line),
            )

    for pair in COL_PAIRS:
        direction = col_direction(*pair)
        append_coord(
            kind="parity_symbol",
            columns=list(pair),
            pair=pair_name(pair),
            support=[pair_name(pair)],
            fano_line=list(fano_line(pair)),
            label=direction_label(direction),
            incidence_ok=True,
        )

    return coords


def summarize_assignment(coords: list[dict[str, Any]]) -> dict[str, Any]:
    label_counts = Counter(c["label"] for c in coords)
    kind_counts = Counter(c["kind"] for c in coords)
    type_by_label: dict[str, dict[str, int]] = {}
    support_profile: dict[str, dict[str, int]] = {}
    for label in sorted(label_counts, key=lambda s: hamming_bits(s)):
        type_by_label[label] = dict(sorted(Counter(c["kind"] for c in coords if c["label"] == label).items()))

    for pair in COL_PAIRS:
        name = pair_name(pair)
        active = [c for c in coords if name in c["support"]]
        support_profile[name] = {
            "active_coordinates": len(active),
            "label_counts": dict(sorted(Counter(c["label"] for c in active).items())),
            "fano_line": list(fano_line(pair)),
        }

    zero_records = [c for c in coords if c["label"] == "Z"]
    nonzero_records = [c for c in coords if c["label"] != "Z"]
    direction_label_counts = {
        direction_label(d): label_counts[direction_label(d)]
        for d in DIRECTIONS
    }
    vertex_label_counts = {
        vertex_label(col): label_counts[vertex_label(col)]
        for col in COLUMNS
    }

    return {
        "total_coordinates": len(coords),
        "label_counts": dict(sorted(label_counts.items(), key=lambda kv: hamming_bits(kv[0]))),
        "kind_counts": dict(sorted(kind_counts.items())),
        "type_by_label": type_by_label,
        "support_profile": support_profile,
        "zero_sheet_kinds": dict(sorted(Counter(c["kind"] for c in zero_records).items())),
        "direction_label_counts": direction_label_counts,
        "vertex_label_counts": vertex_label_counts,
        "all_labels_have_size_9": all(count == 9 for count in label_counts.values()) and len(label_counts) == 8,
        "all_nonzero_labels_are_fano_incident": all(c["incidence_ok"] for c in nonzero_records),
        "zero_sheet_is_mixed_only": all(c["kind"] == "mixed_edge" for c in zero_records),
    }


def horizon_vertex_name(vertex: tuple[int, int]) -> str:
    row, col = vertex
    return f"r{row}c{col}"


def simple_cycle_basis_summary(edges: list[tuple[tuple[int, int], tuple[int, int]]]) -> dict[str, Any]:
    adjacency: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    vertices = sorted(adjacency)
    seen: set[tuple[int, int]] = set()
    components: list[list[tuple[int, int]]] = []
    for start in vertices:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            cur = stack.pop()
            component.append(cur)
            for nxt in adjacency[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        components.append(sorted(component))

    indexed_edges = []
    edge_adjacency: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = defaultdict(list)
    for edge_index, (u, v) in enumerate(edges):
        indexed_edges.append((u, v, edge_index))
        edge_adjacency[u].append((v, edge_index))
        edge_adjacency[v].append((u, edge_index))

    cycles: set[tuple[tuple[int, int], ...]] = set()

    def canon(path: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
        rotations = []
        for seq in (path, list(reversed(path))):
            for idx in range(len(seq)):
                rotations.append(tuple(seq[idx:] + seq[:idx]))
        return min(rotations)

    def dfs(
        start: tuple[int, int],
        cur: tuple[int, int],
        path: list[tuple[int, int]],
        used_edges: set[int],
    ) -> None:
        for nxt, edge_index in edge_adjacency[cur]:
            if edge_index in used_edges:
                continue
            if nxt == start and len(path) >= 3:
                cycles.add(canon(path[:]))
            elif nxt not in path and len(path) < len(vertices):
                dfs(start, nxt, path + [nxt], used_edges | {edge_index})

    for vertex in vertices:
        dfs(vertex, vertex, [vertex], set())

    return {
        "vertices": [horizon_vertex_name(v) for v in vertices],
        "edges": [
            [horizon_vertex_name(u), horizon_vertex_name(v)]
            for u, v, _edge_index in indexed_edges
        ],
        "vertex_count": len(vertices),
        "edge_count": len(edges),
        "component_sizes": [len(component) for component in components],
        "degree_histogram": dict(
            sorted(Counter(len(adjacency[v]) for v in vertices).items())
        ),
        "degrees": {
            horizon_vertex_name(vertex): len(adjacency[vertex])
            for vertex in vertices
        },
        "cycle_rank": len(edges) - len(vertices) + len(components),
        "simple_cycles": [
            [horizon_vertex_name(vertex) for vertex in cycle]
            for cycle in sorted(cycles, key=lambda item: (len(item), item))
        ],
        "simple_cycle_lengths": sorted(len(cycle) for cycle in cycles),
        "triangle_free": all(len(cycle) != 3 for cycle in cycles),
    }


def zero_sheet_subgraph(coords: list[dict[str, Any]]) -> dict[str, Any]:
    zero_records = [coord for coord in coords if coord["label"] == "Z"]
    edges = [
        (
            (coord["rows"][0], coord["columns"][0]),
            (coord["rows"][1], coord["columns"][1]),
        )
        for coord in zero_records
    ]
    graph = simple_cycle_basis_summary(edges)
    graph["row_incidence"] = dict(
        sorted(Counter(row for edge in edges for row, _col in edge).items())
    )
    graph["column_incidence"] = dict(
        sorted(Counter(col for edge in edges for _row, col in edge).items())
    )
    graph["reading"] = (
        "The zero Hamming sheet is connected and triangle-free with cycle rank 2. "
        "Its two 4-cycles have a 6-cycle as their symmetric-difference shadow."
    )
    return graph


def search_balanced_gauges() -> list[dict[str, Any]]:
    hits = []
    for row_origin in ROWS:
        for column_origin in COLUMNS:
            for residual_delta in (1, 2):
                coords = build_assignment(
                    row_origin=row_origin,
                    column_origin=column_origin,
                    residual_delta=residual_delta,
                )
                summary = summarize_assignment(coords)
                if (
                    summary["all_labels_have_size_9"]
                    and summary["all_nonzero_labels_are_fano_incident"]
                    and summary["zero_sheet_is_mixed_only"]
                ):
                    hits.append(
                        {
                            "row_origin": row_origin,
                            "column_origin": column_origin,
                            "residual_delta": residual_delta,
                            "special_pairs": {
                                direction_label(d): list(p)
                                for d, p in canonical_special_pairs(column_origin).items()
                            },
                        }
                    )
    return hits


def build_payload() -> dict[str, Any]:
    row_origin = 0
    column_origin = 0
    residual_delta = 1
    coords = build_assignment(
        row_origin=row_origin,
        column_origin=column_origin,
        residual_delta=residual_delta,
    )
    summary = summarize_assignment(coords)
    zero_graph = zero_sheet_subgraph(coords)
    hits = search_balanced_gauges()
    identities = {
        "coordinates_are_72": summary["total_coordinates"] == 72,
        "eight_hamming_sheets": len(summary["label_counts"]) == 8,
        "balanced_9_per_sheet": summary["all_labels_have_size_9"],
        "nonzero_labels_are_fano_incident": summary["all_nonzero_labels_are_fano_incident"],
        "zero_sheet_is_exactly_9_mixed_edges": (
            summary["label_counts"].get("Z") == 9
            and summary["zero_sheet_kinds"] == {"mixed_edge": 9}
        ),
        "gauge_search_finds_24_balanced_lifts": len(hits) == 24,
        "row_edges_are_direction_sheets": all(
            c["label"].startswith("D") for c in coords if c["kind"] == "row_edge"
        ),
        "column_edges_are_vertex_sheets": all(
            c["label"].startswith("V") for c in coords if c["kind"] == "column_edge"
        ),
        "zero_sheet_graph_is_connected_8v_9e_rank2": (
            zero_graph["vertex_count"] == 8
            and zero_graph["edge_count"] == 9
            and zero_graph["component_sizes"] == [8]
            and zero_graph["cycle_rank"] == 2
        ),
        "zero_sheet_graph_is_triangle_free_with_two_4_cycles_and_one_6_cycle": (
            zero_graph["triangle_free"]
            and zero_graph["simple_cycle_lengths"] == [4, 4, 6]
        ),
    }
    return {
        "summary": {
            "construction": "gauge-fixed tetrahedral Fano/Hamming labeling of the 72-coordinate horizon model",
            "coordinates": summary["total_coordinates"],
            "hamming_sheets": len(summary["label_counts"]),
            "sheet_size": 9,
            "balanced_gauge_lifts_found": len(hits),
            "all_identities_hold": all(identities.values()),
        },
        "gauge": {
            "row_origin": row_origin,
            "column_origin": column_origin,
            "residual_delta": residual_delta,
            "special_pairs": {
                direction_label(d): list(p)
                for d, p in canonical_special_pairs(column_origin).items()
            },
        },
        "fano_model": {
            "nonzero_labels": {
                label: hamming_bits(label)
                for label in ["Z"]
                + [vertex_label(c) for c in COLUMNS]
                + [direction_label(d) for d in DIRECTIONS]
            },
            "k4_pairs_as_fano_lines": {
                pair_name(pair): list(fano_line(pair)) for pair in COL_PAIRS
            },
            "reading": (
                "The six horizon parity checks are K4 edges.  Each K4 edge is a "
                "Fano line containing its two endpoint vertex labels and the "
                "parallel-direction label."
            ),
        },
        "assignment_summary": summary,
        "zero_sheet_subgraph": zero_graph,
        "balanced_gauge_lifts": hits,
        "identities": identities,
        "coordinates": coords,
        "interpretation": (
            "This fills the missing literal functor at coordinate level: the 72 "
            "F3 horizon coordinates split as eight Hamming/Fano sheets of size 9, "
            "and every nonzero label is incident with its actual parity-check "
            "line.  The zero Hamming sheet is not empty; it is exactly the nine "
            "row-origin residual mixed edges.  Thus the functor is gauge-fixed "
            "by a row origin and a column-origin choice."
        ),
        "honesty_boundary": (
            "This is a coordinate-level labeling and incidence lift.  It is not "
            "yet a proof that the ternary horizon code is equivalent to a known "
            "Hamming, Golay, or quantum code, and it does not upgrade the known "
            "distance boundary."
        ),
    }


def main() -> None:
    payload = build_payload()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
