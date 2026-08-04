#!/usr/bin/env python3
"""Passes 3250-3251: explicit local-system cohomology on the collapsed port complex.

Pass 3240 supplies a canonical elementary collapse of the 45-vertex, 720-edge,
240-face port complex: one non-tree edge is paired with each triangular face,
leaving a connected 45-vertex, 480-edge graph of free rank 436.  This module
places finite-field representations on the surviving free generators and
computes cellular cohomology directly from the twisted coboundary matrix.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "data" / "PART_BT3250_BT3251_TWISTED_PORT_LOCAL_SYSTEMS.json"


def load_base():
    path = ROOT / "analysis" / "bt3187_3192_chromatic_defect_block_filter.py"
    spec = importlib.util.spec_from_file_location("bt3250_base", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def rank_mod(matrix: np.ndarray, p: int) -> int:
    a = np.array(matrix, dtype=np.int64) % p
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r, col] % p), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        inv = pow(int(a[rank, col]), -1, p)
        a[rank] = (a[rank] * inv) % p
        for r in range(rows):
            if r != rank and a[r, col] % p:
                a[r] = (a[r] - a[r, col] * a[rank]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def nullity_mod(matrix: np.ndarray, p: int) -> int:
    return matrix.shape[1] - rank_mod(matrix, p)


def collapsed_graph() -> dict:
    base = load_base()
    from bt3240_3241_port_gauge import block_complex

    points, form, lines, supports, frames, incidence, frame_graph = base.build_geometry()
    _, blocks, _ = base.canonical_blocks(points, form, lines, frames)
    result = block_complex(incidence, frame_graph, blocks)
    manifest = result["manifest"]
    tree = [tuple(map(int, edge)) for edge in manifest["tree_edges"]]
    free = [tuple(map(int, edge)) for edge in manifest["free_chord_edges"]]
    surviving = sorted(tree + free)
    assert len(points) == 40 and len(frames) == 540
    assert result["cell_counts"] == {"V": 45, "E": 720, "F": 240}
    assert len(tree) == 44 and len(free) == 436 and len(surviving) == 480
    assert len(set(surviving)) == 480
    return {
        "vertices": 45,
        "original_edges": 720,
        "faces": 240,
        "tree_edges": tree,
        "free_edges": free,
        "surviving_edges": surviving,
        "collapse_manifest_sha256": result["manifest_sha256"],
    }


def invariant_dimension(generators: list[np.ndarray], rank: int, p: int) -> int:
    identity = np.eye(rank, dtype=np.int64)
    if not generators:
        return rank
    stacked = np.vstack([(g - identity) % p for g in generators])
    return nullity_mod(stacked, p)


def twisted_coboundary(
    graph: dict,
    rank: int,
    p: int,
    generator_matrices: list[np.ndarray],
) -> tuple[np.ndarray, list[np.ndarray]]:
    identity = np.eye(rank, dtype=np.int64)
    free = graph["free_edges"]
    assignment = {edge: identity.copy() for edge in graph["surviving_edges"]}
    for edge, matrix in zip(free, generator_matrices):
        m = np.array(matrix, dtype=np.int64) % p
        assert m.shape == (rank, rank)
        assert rank_mod(m, p) == rank
        assignment[edge] = m

    edges = graph["surviving_edges"]
    d0 = np.zeros((len(edges) * rank, graph["vertices"] * rank), dtype=np.int64)
    for edge_index, (u, v) in enumerate(edges):
        transport = assignment[(u, v)]
        row = slice(edge_index * rank, (edge_index + 1) * rank)
        cu = slice(u * rank, (u + 1) * rank)
        cv = slice(v * rank, (v + 1) * rank)
        d0[row, cu] = (-transport) % p
        d0[row, cv] = identity
    used = [assignment[edge] for edge in free if not np.array_equal(assignment[edge] % p, identity % p)]
    return d0 % p, used


def local_systems() -> list[dict]:
    return [
        {
            "name": "constant_F3_rank1",
            "field": 3,
            "rank": 1,
            "generators": [],
            "interpretation": "constant coefficient shadow",
        },
        {
            "name": "sign_F3_rank1",
            "field": 3,
            "rank": 1,
            "generators": [[[2]]],
            "interpretation": "one free generator acts by the nontrivial C2 character",
        },
        {
            "name": "phase_F5_rank1",
            "field": 5,
            "rank": 1,
            "generators": [[[2]]],
            "interpretation": "one free generator carries a primitive order-four scalar phase",
        },
        {
            "name": "unipotent_F3_rank2",
            "field": 3,
            "rank": 2,
            "generators": [[[1, 1], [0, 1]]],
            "interpretation": "one Jordan transport with a one-dimensional fixed line",
        },
        {
            "name": "D4_standard_F3_rank2",
            "field": 3,
            "rank": 2,
            "generators": [
                [[0, 2], [1, 0]],
                [[1, 0], [0, 2]],
            ],
            "interpretation": "quarter-turn and reflection on the two-dimensional D4 module",
        },
        {
            "name": "S3_standard_F5_rank2",
            "field": 5,
            "rank": 2,
            "generators": [
                [[0, 1], [1, 0]],
                [[0, 4], [1, 4]],
            ],
            "interpretation": "transposition and three-cycle on the irreducible S3 plane",
        },
    ]


def compute() -> dict:
    graph = collapsed_graph()
    rows = []
    for spec in local_systems():
        p = int(spec["field"])
        r = int(spec["rank"])
        matrices = [np.array(m, dtype=np.int64) % p for m in spec["generators"]]
        d0, used = twisted_coboundary(graph, r, p, matrices)
        direct_rank = rank_mod(d0, p)
        h0 = graph["vertices"] * r - direct_rank
        h1 = len(graph["surviving_edges"]) * r - direct_rank
        common_fixed = invariant_dimension(used, r, p)
        theorem_h1 = 435 * r + common_fixed
        constant_h1 = 436 * r
        assert h0 == common_fixed
        assert h1 == theorem_h1
        assert constant_h1 - h1 == r - h0
        rows.append(
            {
                "name": spec["name"],
                "field": p,
                "fiber_rank": r,
                "nontrivial_generator_count": len(used),
                "common_invariant_dimension": h0,
                "rank_delta0": direct_rank,
                "twisted_H0_dimension": h0,
                "twisted_H1_dimension": h1,
                "same_rank_constant_H1_dimension": constant_h1,
                "reduction_from_constant": constant_h1 - h1,
                "interpretation": spec["interpretation"],
            }
        )

    expected = {
        "constant_F3_rank1": (1, 436),
        "sign_F3_rank1": (0, 435),
        "phase_F5_rank1": (0, 435),
        "unipotent_F3_rank2": (1, 871),
        "D4_standard_F3_rank2": (0, 870),
        "S3_standard_F5_rank2": (0, 870),
    }
    assert {row["name"]: (row["twisted_H0_dimension"], row["twisted_H1_dimension"]) for row in rows} == expected

    payload = {
        "schema": "w33.pass3250_3251.twisted_port_local_systems.v1",
        "status": "PASS_EXACT_COLLAPSE_AND_TWISTED_COHOMOLOGY",
        "collapsed_complex": {
            "vertices": 45,
            "edges": 480,
            "free_rank": 436,
            "elementary_face_edge_pairs_removed": 240,
            "collapse_manifest_sha256": graph["collapse_manifest_sha256"],
        },
        "theorem": {
            "statement": "For any rank-r local system rho:F_436->GL(r,F_p), with common invariant subspace dimension h0, dim H^0=h0 and dim H^1=435*r+h0.",
            "proof_shape": "The Pass-3240 elementary collapse gives a connected graph with 45 vertices and 480 edges. Its twisted C0-to-C1 coboundary has kernel equal to the common invariant subspace, hence rank 45*r-h0 and H1 dimension 480*r-(45*r-h0).",
            "maximum_reduction_from_same_rank_constant_system": "r-h0 <= r",
            "consequence": "Finite-dimensional twisting can remove at most one cohomology dimension per fiber dimension; it cannot collapse the 436-generator ambiguity to a small finite controller state by itself.",
        },
        "local_systems": rows,
        "boundary": "These are exact finite-field cellular local systems on the explicitly collapsed port complex. They are not laboratory phase measurements, a complete contextuality invariant, or evidence that one particular transport is physically realized.",
    }
    semantic = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["semantic_sha256"] = hashlib.sha256(semantic.encode()).hexdigest()
    return payload


def main() -> None:
    payload = compute()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "free_rank": payload["collapsed_complex"]["free_rank"],
                "systems": {row["name"]: row["twisted_H1_dimension"] for row in payload["local_systems"]},
                "sha256": payload["semantic_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
