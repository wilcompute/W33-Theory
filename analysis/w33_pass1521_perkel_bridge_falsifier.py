from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable

import networkx as nx
import numpy as np

import _selector_five_frontiers_impl as ff
from pass1500_1504 import bridge_classification as bc


MASKS = bc.MASKS
GOOD = bc.GOOD


def perkel_graph() -> nx.Graph:
    """Construct the standard Z_3 x Z_19 model of the Perkel graph."""
    graph = nx.Graph()
    graph.add_nodes_from((layer, residue) for layer in range(3) for residue in range(19))
    for layer in range(3):
        rhs = pow(2, 6 * layer, 19)
        next_layer = (layer + 1) % 3
        roots = [delta for delta in range(19) if pow(delta, 3, 19) == rhs]
        assert len(roots) == 3
        for residue in range(19):
            for delta in roots:
                graph.add_edge((layer, residue), (next_layer, (residue + delta) % 19))
    assert graph.number_of_nodes() == 57
    assert graph.number_of_edges() == 171
    assert set(dict(graph.degree()).values()) == {6}
    assert nx.is_connected(graph)
    return graph


def intersection_array(graph: nx.Graph) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    if not nx.is_connected(graph):
        return None
    diameter = nx.diameter(graph)
    b_values: list[int] = []
    c_values: list[int] = []
    for distance in range(diameter + 1):
        bs: set[int] = set()
        cs: set[int] = set()
        for root in graph:
            levels = nx.single_source_shortest_path_length(graph, root)
            for vertex, level in levels.items():
                if level != distance:
                    continue
                bs.add(sum(levels[neighbor] == distance + 1 for neighbor in graph[vertex]))
                cs.add(sum(levels[neighbor] == distance - 1 for neighbor in graph[vertex]))
        if len(bs) != 1 or len(cs) != 1:
            return None
        if distance < diameter:
            b_values.append(next(iter(bs)))
        if distance > 0:
            c_values.append(next(iter(cs)))
    return tuple(b_values), tuple(c_values)


def dense_bridge_family() -> list[dict[str, Any]]:
    """Recompute the 76 rank-complete bridges and retain their exact matrices."""
    _public, captured = bc.capture()
    group_data = captured["g"]
    sheet_rows, rectangles, flag_index = bc.build_all_sheets()
    boundary = ff.levi_boundary(flag_index)
    projectors = [
        (item, ff.orbital_matrix_mod(group_data, item["projector"], GOOD))
        for item in sorted(captured["character_projectors"], key=lambda item: item["block_index"])
    ]

    output: list[dict[str, Any]] = []
    for mask in MASKS:
        mask_label = "".join(map(str, mask))
        for residual in range(3):
            sheet = bc.dense_sheet(sheet_rows[(mask, residual)])
            sheet_rank = bc.rank_mod(sheet)
            if sheet_rank != 81:
                continue
            assert not np.any(boundary @ sheet.T)
            for side_character, edge_character in itertools.product((0, 1), repeat=2):
                matrix = bc.bridge(sheet, rectangles, side_character, edge_character)
                bridge_rank = bc.rank_mod(matrix)
                assert bridge_rank == 81
                sector_ranks = [
                    bc.rank_mod(projector @ (matrix % GOOD) % GOOD)
                    for _item, projector in projectors
                ]
                assert sector_ranks[-1] in (4, 5)
                output.append(
                    {
                        "sheet": f"{mask_label}_r{residual}",
                        "mask": mask_label,
                        "residual": residual,
                        "side_character": side_character,
                        "edge_character": edge_character,
                        "terminal_rank": sector_ranks[-1],
                        "robust": sector_ranks[-1] == 5,
                        "matrix": matrix,
                        "sha256": hashlib.sha256(matrix.astype(np.int64).tobytes()).hexdigest(),
                    }
                )

    assert len(output) == 76
    assert sum(item["robust"] for item in output) == 57
    assert sum(not item["robust"] for item in output) == 19
    return output


def pair_metrics(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    a = left["matrix"]
    b = right["matrix"]
    a_support = a != 0
    b_support = b != 0
    a_rows = np.any(a_support, axis=1)
    b_rows = np.any(b_support, axis=1)
    a_cols = np.any(a_support, axis=0)
    b_cols = np.any(b_support, axis=0)
    mask_hamming = sum(x != y for x, y in zip(left["mask"], right["mask"]))
    sign_hamming = (left["side_character"] != right["side_character"]) + (
        left["edge_character"] != right["edge_character"]
    )
    return {
        "frobenius": int(np.sum(a * b)),
        "support_overlap": int(np.count_nonzero(a_support & b_support)),
        "row_support_overlap": int(np.count_nonzero(a_rows & b_rows)),
        "column_support_overlap": int(np.count_nonzero(a_cols & b_cols)),
        "same_sheet": int(left["sheet"] == right["sheet"]),
        "same_mask": int(left["mask"] == right["mask"]),
        "same_residual": int(left["residual"] == right["residual"]),
        "mask_hamming": mask_hamming,
        "sign_hamming": int(sign_hamming),
    }


def relation_classes(items: list[dict[str, Any]]) -> dict[str, dict[Any, list[tuple[int, int]]]]:
    classes: dict[str, dict[Any, list[tuple[int, int]]]] = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    for i, j in itertools.combinations(range(len(items)), 2):
        metrics = pair_metrics(items[i], items[j])
        for name, value in metrics.items():
            classes[name][value].append((i, j))
        full_key = tuple(metrics[name] for name in sorted(metrics))
        classes["full_signature"][full_key].append((i, j))
    return {name: dict(values) for name, values in classes.items()}


def graph_from_edges(order: int, edges: Iterable[tuple[int, int]]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(order))
    graph.add_edges_from(edges)
    return graph


def is_perkel_candidate(graph: nx.Graph, reference: nx.Graph) -> bool:
    if graph.number_of_nodes() != 57 or graph.number_of_edges() != 171:
        return False
    if set(dict(graph.degree()).values()) != {6}:
        return False
    if not nx.is_connected(graph) or nx.diameter(graph) != 3:
        return False
    if intersection_array(graph) != ((6, 5, 2), (1, 1, 3)):
        return False
    return nx.is_isomorphic(graph, reference)


def is_cycle19_candidate(graph: nx.Graph) -> bool:
    return (
        graph.number_of_nodes() == 19
        and graph.number_of_edges() == 19
        and set(dict(graph.degree()).values()) == {2}
        and nx.is_connected(graph)
    )


def search_relation_unions(
    classes: dict[str, dict[Any, list[tuple[int, int]]]],
    order: int,
    target_edges: int,
    predicate,
    max_union_size: int = 3,
    union_class_cap: int = 64,
) -> list[dict[str, Any]]:
    """Search relation classes exactly, while avoiding cubic explosion in huge signatures.

    Every individual relation class is tested. Unions of two or three classes are
    tested only when the family has at most ``union_class_cap`` values. Scalar
    invariant families are small; the cap primarily protects the full-signature
    refinement from an accidental near-discrete partition.
    """
    hits: list[dict[str, Any]] = []
    for family_name, family in sorted(classes.items()):
        candidates = [(value, edges) for value, edges in family.items() if len(edges) <= target_edges]
        candidates.sort(key=lambda item: (len(item[1]), repr(item[0])))
        effective_max = 1 if len(candidates) > union_class_cap else max_union_size
        for size in range(1, min(effective_max, len(candidates)) + 1):
            for chosen in itertools.combinations(candidates, size):
                if sum(len(edges) for _value, edges in chosen) != target_edges:
                    continue
                union_edges: set[tuple[int, int]] = set()
                for _value, edges in chosen:
                    union_edges.update(edges)
                if len(union_edges) != target_edges:
                    continue
                graph = graph_from_edges(order, union_edges)
                if predicate(graph):
                    hits.append(
                        {
                            "family": family_name,
                            "values": [repr(value) for value, _edges in chosen],
                            "union_size": size,
                        }
                    )
    return hits


def analyze() -> dict[str, Any]:
    bridges = dense_bridge_family()
    robust = [item for item in bridges if item["robust"]]
    defective = [item for item in bridges if not item["robust"]]

    by_sheet: dict[str, dict[str, Any]] = {}
    grouped = itertools.groupby(
        sorted(bridges, key=lambda item: item["sheet"]), key=lambda item: item["sheet"]
    )
    for sheet, members in grouped:
        group = list(members)
        by_sheet[sheet] = {
            "robust": sum(item["robust"] for item in group),
            "defective": sum(not item["robust"] for item in group),
            "defect_characters": [
                [item["side_character"], item["edge_character"]]
                for item in group
                if not item["robust"]
            ],
        }

    uniform_three_plus_one = all(
        record["robust"] == 3 and record["defective"] == 1 for record in by_sheet.values()
    )
    defect_character_census = collections.Counter(
        (item["side_character"], item["edge_character"]) for item in defective
    )

    reference = perkel_graph()
    robust_classes = relation_classes(robust)
    defective_classes = relation_classes(defective)
    perkel_hits = search_relation_unions(
        robust_classes,
        57,
        171,
        lambda graph: is_perkel_candidate(graph, reference),
    )
    cycle19_hits = search_relation_unions(
        defective_classes,
        19,
        19,
        is_cycle19_candidate,
    )

    psl219_order = 19 * (19 * 19 - 1) // 2
    result = {
        "theorem": "Pass 1521 Perkel-Shadow Bridge Falsifier",
        "external_perkel_reference": {
            "vertices": reference.number_of_nodes(),
            "edges": reference.number_of_edges(),
            "degree": 6,
            "diameter": nx.diameter(reference),
            "intersection_array": [[6, 5, 2], [1, 1, 3]],
            "psl_2_19_order": psl219_order,
            "z3_times_z19_model_verified": True,
        },
        "inherited_action_obstruction": {
            "p_sp_4_3_order": 25920,
            "pg_sp_4_3_order": 51840,
            "19_divides_p_sp_4_3": 25920 % 19 == 0,
            "19_divides_pg_sp_4_3": 51840 % 19 == 0,
            "literal_psl_2_19_subgroup_or_inherited_orbit_action_possible": False,
        },
        "bridge_census": {
            "rank81_sheets": len(by_sheet),
            "sign_characters_per_sheet": 4,
            "rank81_bridges": len(bridges),
            "robust_bridges": len(robust),
            "terminal_defect_bridges": len(defective),
            "factorization": "76 = 19*4 and 57+19 = 19*(3+1)",
            "uniform_three_robust_one_defect_per_sheet": uniform_three_plus_one,
            "defect_character_census": {
                f"{side}{edge}": count
                for (side, edge), count in sorted(defect_character_census.items())
            },
            "sheet_records": by_sheet,
        },
        "intrinsic_relation_search": {
            "pair_invariant_families": sorted(robust_classes),
            "relation_class_counts": {
                name: len(values) for name, values in sorted(robust_classes.items())
            },
            "tested_unions_up_to_size": 3,
            "large_family_union_class_cap": 64,
            "perkel_hits_on_57_robust_bridges": perkel_hits,
            "cycle19_hits_on_19_defective_bridges": cycle19_hits,
            "perkel_found": bool(perkel_hits),
            "defect_cycle19_found": bool(cycle19_hits),
        },
        "conclusion": (
            "A Perkel graph was found among the tested exact pair-invariant relations. "
            "Its PSL(2,19) symmetry is emergent and does not lift to the W33 acting group."
            if perkel_hits
            else "No Perkel graph occurs among the tested exact pair-invariant relation classes or permitted small unions. "
            "The equality 57=3*19 remains a cardinality shadow unless a different intrinsic relation is supplied."
        ),
        "boundary": (
            "The divisibility argument excludes inherited PSL(2,19) symmetry but not accidental automorphisms of a derived 57-object graph. "
            "Every individual value class is tested. Unions of up to three classes are tested for families with at most 64 values; larger refinements are tested only classwise. "
            "This is not exhaustive over all conceivable relations on the 57 robust bridges."
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    result["sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = analyze()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
