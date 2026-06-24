#!/usr/bin/env python3
"""
BT1658 — Resonance projector split theorem.

BT1655 found a degenerate coupled eigenvalue 30:
    6_clock^8 x 24_matter^15  -> 30^120
    0_clock^1 x 30_matter^24  -> 30^24
so the full coupled 30-eigenspace has rank 144.

BT1658 proves that this degeneracy is split by natural commuting projectors.  In
particular, the partial clock Laplacian K = L_clock \otimes I_matter has eigenvalue
6 on the rank-120 resonance block and eigenvalue 0 on the rank-24 companion block.
No arbitrary coordinate selector is needed.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3


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


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...] | None:
    vv = tuple(x % MOD for x in v)
    if all(x == 0 for x in vv):
        return None
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in vv)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % MOD


def w33_collinearity_graph() -> nx.Graph:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            points.append(c)  # type: ignore[arg-type]
    points.sort()
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, j in itertools.combinations(range(len(points)), 2):
        if symplectic_form(points[i], points[j]) == 0:
            graph.add_edge(i, j)
    return graph


def laplacian_matrix(graph: nx.Graph, nodelist: list[object]) -> np.ndarray:
    A = nx.to_numpy_array(graph, nodelist=nodelist, dtype=float)
    return np.diag(A.sum(axis=1)) - A


def spectrum_counter(matrix: np.ndarray) -> dict[str, int]:
    vals = np.linalg.eigvalsh(matrix)
    c = Counter(round(float(x), 6) for x in vals)
    return {str(0.0 if abs(k) < 1e-6 else k): int(v) for k, v in sorted(c.items())}


def trace_rank(P: np.ndarray) -> int:
    return int(round(float(np.trace(P))))


def norm(A: np.ndarray) -> float:
    return float(np.linalg.norm(A))


def main() -> None:
    clock = nx.line_graph(heawood_graph())
    clock_nodes = sorted(clock.nodes(), key=repr)
    Lc = laplacian_matrix(clock, clock_nodes)
    Ic = np.eye(clock.number_of_nodes())

    W = w33_collinearity_graph()
    matter = nx.complement(W)
    Lm = laplacian_matrix(matter, list(range(40)))
    Im = np.eye(matter.number_of_nodes())

    assert spectrum_counter(Lc) == {"0.0": 1, "1.585786": 6, "4.414214": 6, "6.0": 8}
    assert spectrum_counter(Lm) == {"0.0": 1, "24.0": 15, "30.0": 24}

    # Clock projectors.  The middle pair is eliminated by ((L-3I)^2-2I).
    Pc0 = -((Lc - 6 * Ic) @ ((Lc - 3 * Ic) @ (Lc - 3 * Ic) - 2 * Ic)) / 42.0
    Pc6 = (Lc @ ((Lc - 3 * Ic) @ (Lc - 3 * Ic) - 2 * Ic)) / 42.0

    # Matter projectors for eigenvalues 24 and 30.
    Pm24 = (Lm @ (Lm - 30 * Im)) / ((24 - 0) * (24 - 30))
    Pm30 = (Lm @ (Lm - 24 * Im)) / ((30 - 0) * (30 - 24))

    checks = {
        "clock_P0_rank": trace_rank(Pc0),
        "clock_P6_rank": trace_rank(Pc6),
        "matter_P24_rank": trace_rank(Pm24),
        "matter_P30_rank": trace_rank(Pm30),
        "clock_P0_idempotent_norm": norm(Pc0 @ Pc0 - Pc0),
        "clock_P6_idempotent_norm": norm(Pc6 @ Pc6 - Pc6),
        "matter_P24_idempotent_norm": norm(Pm24 @ Pm24 - Pm24),
        "matter_P30_idempotent_norm": norm(Pm30 @ Pm30 - Pm30),
        "clock_P0_P6_orthogonality_norm": norm(Pc0 @ Pc6),
        "matter_P24_P30_orthogonality_norm": norm(Pm24 @ Pm30),
        "clock_L_on_P6_residual_norm": norm(Lc @ Pc6 - 6 * Pc6),
        "clock_L_on_P0_residual_norm": norm(Lc @ Pc0),
        "matter_L_on_P24_residual_norm": norm(Lm @ Pm24 - 24 * Pm24),
        "matter_L_on_P30_residual_norm": norm(Lm @ Pm30 - 30 * Pm30),
    }

    resonance_rank = checks["clock_P6_rank"] * checks["matter_P24_rank"]
    companion_rank = checks["clock_P0_rank"] * checks["matter_P30_rank"]
    total_rank = resonance_rank + companion_rank

    assert resonance_rank == 120
    assert companion_rank == 24
    assert total_rank == 144
    assert max(checks[k] for k in checks if k.endswith("norm")) < 1e-8

    result = {
        "theorem": "BT1658 Resonance Projector Split Theorem",
        "projectors": {
            "clock_ground_P0": "- (Lc-6I)((Lc-3I)^2-2I) / 42",
            "clock_endpoint_P6": "Lc((Lc-3I)^2-2I) / 42",
            "matter_gap_P24": "Lm(Lm-30I)/((24)(24-30))",
            "matter_top_P30": "Lm(Lm-24I)/((30)(30-24))",
        },
        "checks": checks,
        "coupled_30_split": {
            "resonance_block": {
                "formula": "P_clock_6 ⊗ P_matter_24",
                "coupled_eigenvalue": 30,
                "rank": resonance_rank,
                "partial_clock_eigenvalue": 6,
                "partial_matter_eigenvalue": 24,
            },
            "companion_block": {
                "formula": "P_clock_0 ⊗ P_matter_30",
                "coupled_eigenvalue": 30,
                "rank": companion_rank,
                "partial_clock_eigenvalue": 0,
                "partial_matter_eigenvalue": 30,
            },
            "total_30_rank": total_rank,
        },
        "separator": {
            "operator": "K_clock = L_clock ⊗ I_matter",
            "eigenvalue_on_resonance_block": 6,
            "eigenvalue_on_companion_block": 0,
            "normalized_resonance_selector_on_30_space": "(K_clock / 6) restricted to the coupled 30-eigenspace",
        },
        "boundary": "The coupled eigenvalue 30 is degenerate, but the degeneracy is split by commuting graph operators. The split is projector-natural, not coordinate-natural.",
    }

    out_path = Path("data/PART_BT1658_RESONANCE_PROJECTOR_SPLIT_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
