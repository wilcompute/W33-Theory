#!/usr/bin/env python3
"""Pass 1536: binary frame code and intrinsic K4,4 minimum words.

Rebuild W(3,3), the 540x240 canonical frame/edge incidence matrix M,
and the 45 intrinsic induced K4,4 octets.  Over F2 the octet incidence
matrix K is the complete parity-check matrix of the frame code.

The minimum-distance and minimum-word census are independently certified
by a mixed-integer parity model.  All returned claims are finite and exact;
no physical interpretation is asserted.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix, hstack, vstack

Q = 3
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1536_frame_dual_k44_code.json"
OMEGA = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=np.int64,
) % Q


def norm(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(int(x) % Q for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % Q for y in v)
    raise ValueError("zero vector")


def symp(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return int(np.array(a, dtype=np.int64) @ OMEGA @ np.array(b, dtype=np.int64) % Q)


def rank_mod(matrix: np.ndarray, prime: int) -> int:
    a = np.array(matrix, dtype=np.int64) % prime
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivots = np.flatnonzero(a[rank:, col])
        if not len(pivots):
            continue
        pivot = rank + int(pivots[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank] * pow(int(a[rank, col]), -1, prime) % prime
        active = np.flatnonzero(a[:, col])
        active = active[active != rank]
        if len(active):
            a[active] = (a[active] - a[active, col, None] * a[rank]) % prime
        rank += 1
        if rank == rows:
            break
    return rank


def srg_parameters(graph: nx.Graph) -> tuple[int, int, int, int] | None:
    degrees = set(dict(graph.degree()).values())
    if len(degrees) != 1:
        return None
    adjacent = set()
    nonadjacent = set()
    for left, right in itertools.combinations(graph.nodes(), 2):
        common = len(set(graph[left]) & set(graph[right]))
        (adjacent if graph.has_edge(left, right) else nonadjacent).add(common)
    if len(adjacent) != 1 or len(nonadjacent) != 1:
        return None
    return graph.number_of_nodes(), next(iter(degrees)), next(iter(adjacent)), next(iter(nonadjacent))


def build_geometry() -> dict[str, Any]:
    points = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    point_index = {point: index for index, point in enumerate(points)}

    graph = nx.Graph()
    graph.add_nodes_from(range(40))
    for left, right in itertools.combinations(range(40), 2):
        if symp(points[left], points[right]) == 0:
            graph.add_edge(left, right)
    edges = sorted(tuple(sorted(edge)) for edge in graph.edges())
    edge_index = {edge: index for index, edge in enumerate(edges)}

    lines: set[tuple[int, ...]] = set()
    for left, right in edges:
        a = np.array(points[left], dtype=np.int64)
        b = np.array(points[right], dtype=np.int64)
        span = {
            norm(tuple((u * a + v * b) % Q))
            for u, v in itertools.product(range(Q), repeat=2)
            if u or v
        }
        lines.add(tuple(sorted(point_index[point] for point in span)))
    ordered_lines = sorted(lines)

    frames: list[tuple[int, int]] = []
    matchings: list[tuple[int, ...]] = []
    for left, right in itertools.combinations(range(40), 2):
        line_left = ordered_lines[left]
        line_right = ordered_lines[right]
        if set(line_left) & set(line_right):
            continue
        matching = []
        for point in line_left:
            partners = [candidate for candidate in line_right if graph.has_edge(point, candidate)]
            if len(partners) != 1:
                raise AssertionError("generalized-quadrangle matching is not unique")
            matching.append(edge_index[tuple(sorted((point, partners[0])))])
        frames.append((left, right))
        matchings.append(tuple(sorted(matching)))

    frame_matrix = np.zeros((len(frames), len(edges)), dtype=np.int8)
    for row, matching in enumerate(matchings):
        frame_matrix[row, list(matching)] = 1

    independent_fours = [
        subset
        for subset in itertools.combinations(range(40), 4)
        if graph.subgraph(subset).number_of_edges() == 0
    ]
    octets: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for left in independent_fours:
        common = set(range(40)) - set(left)
        for point in left:
            common &= set(graph[point])
        if len(common) != 4:
            continue
        right = tuple(sorted(common))
        if graph.subgraph(right).number_of_edges() != 0:
            continue
        octets.add(tuple(sorted((tuple(left), right))))
    ordered_octets = sorted(octets)

    octet_matrix = np.zeros((len(ordered_octets), len(edges)), dtype=np.int8)
    for row, (left, right) in enumerate(ordered_octets):
        for a in left:
            for b in right:
                edge = tuple(sorted((a, b)))
                if edge not in edge_index:
                    raise AssertionError("octet is not an induced K4,4")
                octet_matrix[row, edge_index[edge]] = 1

    return {
        "points": points,
        "graph": graph,
        "edges": edges,
        "lines": ordered_lines,
        "frames": frames,
        "matchings": matchings,
        "M": frame_matrix,
        "octets": ordered_octets,
        "K": octet_matrix,
    }


def minimum_word_certificate(frame_matrix: np.ndarray) -> dict[str, Any]:
    """Prove d=16 and enumerate every weight-16 word of ker(M) over F2."""
    checks, variables = frame_matrix.shape
    parity_aux = checks
    parity_block = hstack(
        [csr_matrix(frame_matrix, dtype=float), -2 * csr_matrix(np.eye(parity_aux))],
        format="csr",
    )
    nonzero_row = hstack(
        [csr_matrix(np.ones((1, variables))), csr_matrix((1, parity_aux))], format="csr"
    )
    objective = np.r_[np.ones(variables), np.zeros(parity_aux)]
    integrality = np.ones(variables + parity_aux)
    bounds = Bounds(
        np.zeros(variables + parity_aux),
        np.r_[np.ones(variables), 2 * np.ones(parity_aux)],
    )

    minimum_model = vstack([parity_block, nonzero_row], format="csr")
    minimum = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(
            minimum_model,
            np.r_[np.zeros(checks), 1],
            np.r_[np.zeros(checks), variables],
        ),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    if minimum.status != 0 or minimum.fun is None:
        raise AssertionError(f"minimum-distance MILP failed: {minimum.message}")
    distance = int(round(float(minimum.fun)))

    weight_row = hstack(
        [csr_matrix(np.ones((1, variables))), csr_matrix((1, parity_aux))], format="csr"
    )
    base = vstack([parity_block, weight_row], format="csr")
    base_lower = np.r_[np.zeros(checks), distance]
    base_upper = np.r_[np.zeros(checks), distance]
    exclusions: list[tuple[int, ...]] = []
    solutions: list[tuple[int, ...]] = []

    while True:
        if exclusions:
            cuts = np.zeros((len(exclusions), variables + parity_aux), dtype=float)
            for row, support in enumerate(exclusions):
                cuts[row, list(support)] = 1
            model = vstack([base, csr_matrix(cuts)], format="csr")
            lower = np.r_[base_lower, np.zeros(len(exclusions))]
            upper = np.r_[base_upper, (distance - 1) * np.ones(len(exclusions))]
        else:
            model = base
            lower = base_lower
            upper = base_upper
        result = milp(
            np.zeros(variables + parity_aux),
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(model, lower, upper),
            options={"presolve": True, "mip_rel_gap": 0.0},
        )
        if result.status == 2:
            break
        if result.status != 0 or result.x is None:
            raise AssertionError(f"minimum-word enumeration failed: {result.message}")
        support = tuple(np.flatnonzero(np.rint(result.x[:variables]).astype(np.int8)))
        if len(support) != distance or support in solutions:
            raise AssertionError("invalid or duplicate minimum word")
        if np.any(frame_matrix[:, support].sum(axis=1) % 2):
            raise AssertionError("enumerated word violates parity checks")
        solutions.append(support)
        exclusions.append(support)

    return {
        "distance": distance,
        "supports": sorted(solutions),
        "count": len(solutions),
    }


def certificate(run_milp: bool = True) -> dict[str, Any]:
    data = build_geometry()
    graph: nx.Graph = data["graph"]
    M: np.ndarray = data["M"]
    K: np.ndarray = data["K"]

    overlap = K @ K.T
    overlap_graph = nx.Graph()
    overlap_graph.add_nodes_from(range(len(K)))
    for left, right in itertools.combinations(range(len(K)), 2):
        if overlap[left, right] == 1:
            overlap_graph.add_edge(left, right)
        elif overlap[left, right] != 0:
            raise AssertionError("two intrinsic octets share more than one W33 edge")
    disjointness_graph = nx.complement(overlap_graph)

    tanner = nx.Graph()
    tanner.add_nodes_from(("check", row) for row in range(K.shape[0]))
    tanner.add_nodes_from(("edge", column) for column in range(K.shape[1]))
    for row, column in zip(*np.nonzero(K)):
        tanner.add_edge(("check", int(row)), ("edge", int(column)))

    minimum = minimum_word_certificate(M) if run_milp else None
    octet_supports = sorted(tuple(map(int, np.flatnonzero(row))) for row in K)

    column_signatures = [tuple(map(int, np.flatnonzero(K[:, column]))) for column in range(K.shape[1])]
    checks = {
        "W33_SRG_40_12_2_4": srg_parameters(graph) == (40, 12, 2, 4),
        "counts_40_lines_240_edges_540_frames": (
            len(data["points"]), len(data["lines"]), len(data["edges"]), len(data["frames"])
        ) == (40, 40, 240, 540),
        "frame_rows_weight_4_columns_weight_9": set(map(int, M.sum(axis=1))) == {4}
        and set(map(int, M.sum(axis=0))) == {9},
        "frame_code_rank_195": rank_mod(M, 2) == 195,
        "exactly_45_induced_K44_octets": len(data["octets"]) == 45,
        "octet_rows_weight_16_columns_weight_3": set(map(int, K.sum(axis=1))) == {16}
        and set(map(int, K.sum(axis=0))) == {3},
        "octets_are_frame_dual": not np.any((M @ K.T) % 2),
        "octets_span_complete_45_dimensional_dual": rank_mod(K, 2) == 45
        and rank_mod(M, 2) + rank_mod(K, 2) == 240,
        "octet_overlap_SRG_45_32_22_24": srg_parameters(overlap_graph) == (45, 32, 22, 24),
        "octet_disjointness_SRG_45_12_3_3": srg_parameters(disjointness_graph) == (45, 12, 3, 3),
        "octet_Gram_spectrum_48_12_18": collections.Counter(
            int(round(value)) for value in np.linalg.eigvalsh(overlap)
        ) == collections.Counter({48: 1, 12: 20, 18: 24}),
        "octet_Gram_ranks_mod_2_3": rank_mod(overlap, 2) == 14 and rank_mod(overlap, 3) == 15,
        "all_240_edge_signatures_are_distinct_triples": len(set(column_signatures)) == 240
        and {len(signature) for signature in column_signatures} == {3},
        "frame_code_parameters_240_195_4": len(set(column_signatures)) == 240,
        "Tanner_is_3_16_regular_girth_6": set(
            tanner.degree(("check", row)) for row in range(45)
        ) == {16}
        and set(tanner.degree(("edge", column)) for column in range(240)) == {3}
        and nx.girth(tanner) == 6,
    }
    if minimum is not None:
        checks.update(
            {
                "dual_minimum_distance_16": minimum["distance"] == 16,
                "exactly_45_minimum_words": minimum["count"] == 45,
                "minimum_words_are_exactly_K44_octets": minimum["supports"] == octet_supports,
            }
        )

    hashes = {
        "frame_matrix_sha256": hashlib.sha256(M.tobytes()).hexdigest(),
        "octet_matrix_sha256": hashlib.sha256(K.tobytes()).hexdigest(),
        "minimum_supports_sha256": hashlib.sha256(
            json.dumps(octet_supports, separators=(",", ":")).encode()
        ).hexdigest(),
    }
    payload = {
        "schema": "w33.pass1536.frame_dual_k44_code.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "Over F2, the code generated by the 540 canonical four-edge frame matchings is a "
            "[240,195,4] code. Its dual is the [240,45,16] code generated by the 45 intrinsic "
            "induced K4,4 edge sets of W(3,3). Those 45 octets are linearly independent and are "
            "exactly all minimum-weight dual words, hence form the unique minimum-word basis."
        ),
        "parameters": {
            "frame_code": [240, 195, 4],
            "frame_dual_code": [240, 45, 16],
            "frame_checks": 540,
            "intrinsic_K44_checks": 45,
            "check_weight": 16,
            "variable_degree": 3,
            "Tanner_girth": 6,
            "minimum_word_count": 45,
        },
        "overlap_geometry": {
            "intersection_graph": [45, 32, 22, 24],
            "disjointness_graph": [45, 12, 3, 3],
            "integer_Gram_spectrum": {"48": 1, "12": 20, "18": 24},
            "Gram_rank_mod_2": 14,
            "Gram_rank_mod_3": 15,
        },
        "checks": {key: bool(value) for key, value in checks.items()},
        "hashes": hashes,
        "prior_art_boundary": (
            "BT766 owns the intrinsic census and SRG geometry of the 45 K4,4 octets. "
            "Pass 1416 owns rank_F2(M)=195 and the 45-dimensional modular cokernel. "
            "Pass 1536 is the new identification of that entire dual code with the octet span, "
            "including exact minimum distance and exhaustive minimum-word classification."
        ),
        "evidence_boundary": (
            "This is a finite binary-code theorem. The 45-word parity-check realization is an "
            "exact LDPC object, but no detector threshold, quantum-code parameter, or physical "
            "noise claim follows without a separate channel and measurement model."
        ),
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--skip-milp", action="store_true")
    args = parser.parse_args()
    payload = certificate(run_milp=not args.skip_milp)
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 1536 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"]), "hashes": payload["hashes"]}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
