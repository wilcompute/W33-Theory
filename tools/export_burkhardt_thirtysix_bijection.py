#!/usr/bin/env python3
"""Export a deterministic 36-to-36 Burkhardt/cubic witness table."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import networkx as nx
from networkx.algorithms import isomorphism as iso

ROOT = Path(__file__).resolve().parents[1]
TEST_FILE = ROOT / "tests" / "test_burkhardt_moduli_realization.py"
OUTPUT_FILE = ROOT / "artifacts" / "burkhardt_thirtysix_carrier_bijection.json"


def load_burkhardt_module():
    spec = importlib.util.spec_from_file_location("burkhardt_test_module", TEST_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_graph(graph_data: list[set[int]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(graph_data)))
    for vertex, neighbors in enumerate(graph_data):
        for neighbor in neighbors:
            if vertex < neighbor:
                graph.add_edge(vertex, neighbor)
    return graph


def can_extend(left_graph: nx.Graph, right_graph: nx.Graph, partial: dict[int, int]) -> bool:
    colored_left = left_graph.copy()
    colored_right = right_graph.copy()
    inverse = {target: source for source, target in partial.items()}

    for node in colored_left.nodes:
        colored_left.nodes[node]["color"] = f"locked:{node}" if node in partial else "free"
    for node in colored_right.nodes:
        colored_right.nodes[node]["color"] = f"locked:{inverse[node]}" if node in inverse else "free"

    matcher = iso.GraphMatcher(
        colored_left,
        colored_right,
        node_match=lambda left_attrs, right_attrs: left_attrs["color"] == right_attrs["color"],
    )
    return matcher.is_isomorphic()


def canonical_bijection(left_graph: nx.Graph, right_graph: nx.Graph) -> dict[int, int]:
    mapping: dict[int, int] = {}
    used_targets: set[int] = set()
    for source in range(left_graph.number_of_nodes()):
        for target in range(right_graph.number_of_nodes()):
            if target in used_targets:
                continue
            trial = dict(mapping)
            trial[source] = target
            if can_extend(left_graph, right_graph, trial):
                mapping = trial
                used_targets.add(target)
                break
        else:
            raise RuntimeError(f"No extension target found for source vertex {source}")
    return mapping


def build_payload() -> dict[str, object]:
    mod = load_burkhardt_module()
    sections = sorted({mod.POLAR_SECTION_POINTS[point] for point in mod.MINUS_TYPE_POINTS}, key=sorted)
    double_six_data = mod.build_double_six_data()
    carriers = [record["carrier"] for record in double_six_data]

    left_graph = make_graph(mod.overlap_graph(sections, overlap_size=1))
    right_graph = make_graph(mod.overlap_graph(carriers, overlap_size=6))
    mapping = canonical_bijection(left_graph, right_graph)

    rows = []
    for section_index in range(36):
        carrier_index = mapping[section_index]
        double_six = double_six_data[carrier_index]
        rows.append(
            {
                "elliptic_section_index": section_index,
                "elliptic_section_points": [list(point) for point in sorted(sections[section_index])],
                "double_six_carrier_index": carrier_index,
                "double_six_lines": sorted(carriers[carrier_index]),
                "double_six_a_lines": list(double_six["a_lines"]),
                "double_six_b_lines": list(double_six["b_lines"]),
                "classical_cubic_labels": double_six["classical_labels"],
                "tritangent_planes": double_six["tritangent_planes"],
            }
        )

    return {
        "kind": "burkhardt_thirtysix_carrier_bijection",
        "elliptic_section_count": 36,
        "double_six_carrier_count": 36,
        "elliptic_section_overlap_sizes": [1, 4],
        "double_six_carrier_overlap_sizes": [4, 6],
        "rows": rows,
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()