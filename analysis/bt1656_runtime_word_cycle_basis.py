#!/usr/bin/env python3
"""
BT1656 — Runtime word cycle-basis theorem.

BT1654 proved beta_1(Heawood)=8.  BT1656 extracts an explicit deterministic
F_2 cycle basis and compares it to the runtime stack.

The important point is not that the chosen basis is unique.  It is not: cycle
bases depend on the spanning tree / root.  The invariant fact is that every
runtime word has eight independent homology bits because the Fano/Heawood clock
has cycle rank 8.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import networkx as nx


def fano_lines() -> list[tuple[int, int, int]]:
    return [tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]


def heawood_graph() -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(14))
    for line_index, line in enumerate(fano_lines()):
        line_node = 7 + line_index
        for point in line:
            graph.add_edge(point, line_node)
    return graph


def normalized_cycle(path: list[object]) -> tuple[object, ...]:
    n = len(path)
    reps: list[tuple[object, ...]] = []
    for seq in (path, list(reversed(path))):
        for i in range(n):
            reps.append(tuple(seq[i:] + seq[:i]))
    return min(reps, key=repr)


def all_simple_cycles(graph: nx.Graph) -> set[tuple[object, ...]]:
    seen: set[tuple[object, ...]] = set()
    for start in graph.nodes():
        stack: list[tuple[object, list[object]]] = [(start, [start])]
        while stack:
            v, path = stack.pop()
            for nb in graph.neighbors(v):
                if nb == start and len(path) >= 3:
                    seen.add(normalized_cycle(path))
                elif nb not in path and len(path) < graph.number_of_nodes():
                    stack.append((nb, path + [nb]))
    return seen


def cycle_edges(cycle: list[object]) -> list[tuple[object, object]]:
    return [tuple(sorted((cycle[i], cycle[(i + 1) % len(cycle)]), key=repr)) for i in range(len(cycle))]


def gf2_rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    A = [row[:] for row in rows]
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i][c] & 1:
                pivot = i
                break
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        for i in range(m):
            if i != r and (A[i][c] & 1):
                A[i] = [(x ^ y) for x, y in zip(A[i], A[r])]
        r += 1
    return r


def main() -> None:
    H = heawood_graph()
    edges = sorted([tuple(sorted(e)) for e in H.edges()], key=repr)
    edge_index = {edge: idx for idx, edge in enumerate(edges)}

    beta1 = H.number_of_edges() - H.number_of_nodes() + nx.number_connected_components(H)
    basis = nx.cycle_basis(H, root=0)

    rows: list[list[int]] = []
    basis_payload = []
    for slot, cycle in enumerate(basis):
        row = [0] * len(edges)
        ce = cycle_edges(cycle)
        for edge in ce:
            row[edge_index[edge]] = 1
        rows.append(row)
        basis_payload.append(
            {
                "slot": slot,
                "vertices": list(cycle),
                "length": len(cycle),
                "edges": [[a, b] for a, b in ce],
                "edge_vector_weight": sum(row),
            }
        )

    rank = gf2_rank(rows)
    simple_cycles = all_simple_cycles(H)
    cycle_length_distribution = Counter(len(c) for c in simple_cycles)

    result = {
        "theorem": "BT1656 Runtime Word Cycle-Basis Theorem",
        "clock_graph": {
            "vertices": H.number_of_nodes(),
            "edges": H.number_of_edges(),
            "connected_components": nx.number_connected_components(H),
            "beta1": beta1,
            "basis_size": len(basis),
            "basis_rank_over_F2": rank,
        },
        "deterministic_cycle_basis_root_0": basis_payload,
        "basis_length_profile": dict(sorted(Counter(len(c) for c in basis).items())),
        "all_simple_cycles": {
            "total": len(simple_cycles),
            "length_distribution": {str(k): int(v) for k, v in sorted(cycle_length_distribution.items())},
            "nonzero_F2_cycle_space_size": 2**beta1 - 1,
        },
        "runtime_stack_comparison": {
            "runtime_word_bits": beta1,
            "six_phase_lift": beta1 * 6,
            "six_phase_lift_interpretation": "8 independent cycle bits times 6 phase positions = 48 body/frame slots.",
            "q2_lift": beta1 * 9,
            "q2_lift_interpretation": "8 independent cycle bits times q^2=9 gives the 72-tick oscillator frame.",
            "e8_coxeter_lift": beta1 * 9 * 30,
            "e8_coxeter_lift_interpretation": "72 times h(E8)=30 gives the 2160 mirror bus.",
            "full_supercycle": beta1 * 9 * 30 * 24,
            "full_supercycle_interpretation": "2160 times 24 gives 51840=|Sp(4,3)|.",
        },
        "boundary": "The explicit cycle basis is deterministic but not canonical; the invariant runtime object is the 8-dimensional F2 homology/cycle space of the Heawood clock.",
    }

    assert beta1 == 8
    assert len(basis) == 8
    assert rank == 8
    assert result["all_simple_cycles"]["length_distribution"] == {
        "6": 28,
        "8": 21,
        "10": 84,
        "12": 56,
        "14": 24,
    }
    assert result["runtime_stack_comparison"]["six_phase_lift"] == 48
    assert result["runtime_stack_comparison"]["q2_lift"] == 72
    assert result["runtime_stack_comparison"]["e8_coxeter_lift"] == 2160
    assert result["runtime_stack_comparison"]["full_supercycle"] == 51840

    out_path = Path("data/PART_BT1656_RUNTIME_WORD_CYCLE_BASIS_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
