#!/usr/bin/env python3
"""Promote the 36 W(3,3) spread frames to an executable clock graph.

Two spread frames are adjacent when they overlap in four W(3,3) line clocks.
The resulting graph is SRG(36,15,6,6), so every non-adjacent transition can be
bridged by one connector frame.  This script tests how the coarse OS replay and
strict line-context microkernel embed as walks on that frame-clock graph.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any

import numpy as np
from w33_defect_spread_tensor import spectrum_counts
from w33_uor_runtime_model import ROOT, all_lines, find_spreads

DEFAULT_COMPILER = ROOT / "data" / "w33_line_context_compiler.json"
DEFAULT_OS = ROOT / "data" / "holonet_os_scheduler_trace.json"
DEFAULT_OUTPUT = ROOT / "data" / "w33_spread_clock_graph.json"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def build_overlap_matrix(spreads: list[list[int]]) -> np.ndarray:
    sets = [set(spread) for spread in spreads]
    matrix = np.zeros((len(spreads), len(spreads)), dtype=int)
    for left in range(len(spreads)):
        for right in range(left + 1, len(spreads)):
            overlap = len(sets[left] & sets[right])
            matrix[left, right] = matrix[right, left] = overlap
    return matrix


def adjacency_from_overlap(overlap: np.ndarray) -> dict[int, set[int]]:
    return {
        idx: {other for other, value in enumerate(row) if value == 4}
        for idx, row in enumerate(overlap)
    }


def shortest_path(graph: dict[int, set[int]], start: int, end: int) -> list[int]:
    if start == end:
        return [start]
    queue = deque([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        for nxt in sorted(graph[current]):
            if nxt in parent:
                continue
            parent[nxt] = current
            if nxt == end:
                path = [end]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                return list(reversed(path))
            queue.append(nxt)
    raise AssertionError(f"clock graph disconnected between {start} and {end}")


def all_pair_distance_histogram(
    graph: dict[int, set[int]]
) -> tuple[dict[str, int], int]:
    hist: Counter[int] = Counter()
    diameter = 0
    for start in graph:
        distances = {start: 0}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for nxt in graph[current]:
                if nxt not in distances:
                    distances[nxt] = distances[current] + 1
                    queue.append(nxt)
        if len(distances) != len(graph):
            raise AssertionError("clock graph is disconnected")
        for end, distance in distances.items():
            if end > start:
                hist[distance] += 1
                diameter = max(diameter, distance)
    return {str(key): hist[key] for key in sorted(hist)}, diameter


def common_neighbor_profiles(
    graph: dict[int, set[int]]
) -> tuple[dict[str, int], dict[str, int]]:
    adjacent = Counter()
    nonadjacent = Counter()
    vertices = sorted(graph)
    for i, left in enumerate(vertices):
        for right in vertices[i + 1 :]:
            common = len(graph[left] & graph[right])
            if right in graph[left]:
                adjacent[common] += 1
            else:
                nonadjacent[common] += 1
    return (
        {str(key): adjacent[key] for key in sorted(adjacent)},
        {str(key): nonadjacent[key] for key in sorted(nonadjacent)},
    )


def embed_sequence_on_clock_graph(
    label: str,
    ticks: list[dict[str, Any]],
    graph: dict[int, set[int]],
) -> dict[str, Any]:
    spreads = [int(tick["spread_epoch"]) for tick in ticks]
    transitions = []
    expanded = []
    if spreads:
        expanded.append(
            {"kind": "active", "source_tick": 0, "spread_epoch": spreads[0]}
        )
    for idx, (left, right) in enumerate(zip(spreads, spreads[1:]), start=1):
        path = shortest_path(graph, left, right)
        distance = len(path) - 1
        transitions.append(
            {
                "from_tick": idx - 1,
                "to_tick": idx,
                "from_spread": left,
                "to_spread": right,
                "clock_distance": distance,
                "path": path,
            }
        )
        for connector in path[1:-1]:
            expanded.append(
                {
                    "kind": "connector",
                    "between_ticks": [idx - 1, idx],
                    "spread_epoch": connector,
                }
            )
        if idx < len(ticks):
            expanded.append(
                {"kind": "active", "source_tick": idx, "spread_epoch": right}
            )
    distance_hist = Counter(transition["clock_distance"] for transition in transitions)
    return {
        "label": label,
        "active_tick_count": len(ticks),
        "active_spread_sequence": spreads,
        "transition_distance_histogram": {
            str(key): distance_hist[key] for key in sorted(distance_hist)
        },
        "connector_slot_count": sum(
            1 for slot in expanded if slot["kind"] == "connector"
        ),
        "clock_slot_count": len(expanded),
        "expanded_clock_walk": expanded,
        "transitions": transitions,
    }


def build_report(compiler: dict[str, Any], os_trace: dict[str, Any]) -> dict[str, Any]:
    spreads = find_spreads(all_lines(), limit=10000)
    overlap = build_overlap_matrix(spreads)
    graph = adjacency_from_overlap(overlap)
    adjacency = np.zeros((len(spreads), len(spreads)), dtype=int)
    for left, neighbours in graph.items():
        for right in neighbours:
            adjacency[left, right] = 1
    degree_hist = Counter(len(neighbours) for neighbours in graph.values())
    distance_hist, diameter = all_pair_distance_histogram(graph)
    lambda_hist, mu_hist = common_neighbor_profiles(graph)
    micro = embed_sequence_on_clock_graph(
        "active_line_context_microkernel", compiler["active_schedule"]["ticks"], graph
    )
    clock_native = None
    if "clock_native_schedule" in compiler:
        clock_native = embed_sequence_on_clock_graph(
            "clock_native_line_context_microkernel",
            compiler["clock_native_schedule"]["ticks"],
            graph,
        )
    coarse = embed_sequence_on_clock_graph("coarse_site_os", os_trace["ticks"], graph)
    theorem_checks = {
        "thirty_six_clock_frames": len(spreads) == 36,
        "clock_graph_degree_fifteen": degree_hist == Counter({15: 36}),
        "clock_graph_spectrum": spectrum_counts(adjacency)
        == {"-3": 20, "3": 15, "15": 1},
        "clock_graph_is_srg_36_15_6_6": lambda_hist == {"6": 270}
        and mu_hist == {"6": 360},
        "clock_graph_diameter_two": diameter == 2
        and distance_hist == {"1": 270, "2": 360},
        "microkernel_embeds_as_clock_walk": micro["clock_slot_count"]
        == micro["active_tick_count"] + micro["connector_slot_count"],
        "coarse_os_embeds_as_clock_walk": coarse["clock_slot_count"]
        == coarse["active_tick_count"] + coarse["connector_slot_count"],
        "coarse_os_needs_two_connectors_for_current_demo": coarse[
            "connector_slot_count"
        ]
        == 2,
        "clock_native_schedule_present": clock_native is not None,
        "clock_native_embeds_as_clock_walk": bool(clock_native)
        and clock_native["clock_slot_count"]
        == clock_native["active_tick_count"] + clock_native["connector_slot_count"],
        "clock_native_needs_no_connectors": bool(clock_native)
        and clock_native["connector_slot_count"] == 0,
        "clock_native_uses_fewer_clock_slots_than_active_optimal": bool(clock_native)
        and clock_native["clock_slot_count"] < micro["clock_slot_count"],
    }
    return {
        "schema": "w33.spread_clock_graph.v1",
        "status": "PASS" if all(theorem_checks.values()) else "FAIL",
        "clock_graph": {
            "vertices": len(spreads),
            "edge_rule": "two spread frames adjacent iff they share four W(3,3) line clocks",
            "edge_count": int(adjacency.sum() // 2),
            "degree_histogram": {
                str(key): degree_hist[key] for key in sorted(degree_hist)
            },
            "spectrum": spectrum_counts(adjacency),
            "distance_histogram": distance_hist,
            "diameter": diameter,
            "adjacent_common_neighbor_histogram": lambda_hist,
            "nonadjacent_common_neighbor_histogram": mu_hist,
            "srg_parameters": [36, 15, 6, 6],
            "reading": (
                "The 36 spread frames form an SRG(36,15,6,6) clock graph under 4-line overlap. "
                "Because the diameter is 2, any spread-to-spread jump needs at most one connector frame."
            ),
        },
        "schedule_embeddings": {
            "coarse_site_os": coarse,
            "active_line_context_microkernel": micro,
            "clock_native_line_context_microkernel": clock_native,
        },
        "theorem_checks": theorem_checks,
        "interpretation": (
            "The 4-overlap relation is the finite frame clock for the Holonet scheduler. The site-level OS "
            f"trace embeds in {coarse['clock_slot_count']} clock slots. The active-optimal line microkernel "
            f"embeds in {micro['clock_slot_count']} slots after connector insertion, while the clock-native "
            f"line microkernel embeds in {clock_native['clock_slot_count'] if clock_native else 'unknown'} slots."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--compiler", default=str(DEFAULT_COMPILER), help="line compiler JSON"
    )
    parser.add_argument(
        "--os-trace", default=str(DEFAULT_OS), help="coarse OS trace JSON"
    )
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="output JSON")
    args = parser.parse_args(argv)

    report = build_report(
        load(normalize(args.compiler)), load(normalize(args.os_trace))
    )
    output = normalize(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"status: {report['status']}")
    print(f"clock graph: SRG{tuple(report['clock_graph']['srg_parameters'])}")
    print(
        f"coarse slots: {report['schedule_embeddings']['coarse_site_os']['clock_slot_count']}"
    )
    print(
        f"active micro slots: {report['schedule_embeddings']['active_line_context_microkernel']['clock_slot_count']}"
    )
    native = report["schedule_embeddings"].get("clock_native_line_context_microkernel")
    print(f"clock-native slots: {native['clock_slot_count'] if native else 'missing'}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
