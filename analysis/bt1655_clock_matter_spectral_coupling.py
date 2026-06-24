#!/usr/bin/env python3
"""
BT1655 — Clock-to-matter spectral coupling theorem.

This continues BT1654.  The clock module is the Heawood/Fano flag-clock
L(H), whose Laplacian has endpoint 6^8.  The matter graph is the complement of
W(3,3), the SRG(40,27,18,18), whose Laplacian has mass gap 24^15 and top shell
30^24.

We form the conservative tensor/cartesian spectral coupling

    L_coupled = L_clock \otimes I_matter + I_clock \otimes L_matter.

This is not asserted to be the physical interaction Hamiltonian.  It is the
canonical graph-product test of whether the verified clock endpoint and matter
mass-gap sectors resonate.

Result:
    clock endpoint 6^8 x matter gap 24^15 lands at 30 with rank 120.
    The same eigenvalue 30 also receives clock-ground x matter-top rank 24.
    Thus the coupled 30-eigenspace has total multiplicity 144 = 120 + 24,
    while the protected resonance subblock has rank 120 = 8*15.
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


def laplacian_spectrum(graph: nx.Graph, nodelist: list[object] | None = None) -> list[float]:
    if nodelist is None:
        nodelist = list(graph.nodes())
    A = nx.to_numpy_array(graph, nodelist=nodelist, dtype=float)
    L = np.diag(A.sum(axis=1)) - A
    return [float(x) for x in np.linalg.eigvalsh(L)]


def counter(vals: list[float], places: int = 6) -> dict[str, int]:
    out = Counter(round(float(x), places) for x in vals)
    return {str(0.0 if abs(k) < 10 ** (-places) else k): int(v) for k, v in sorted(out.items())}


def main() -> None:
    H = heawood_graph()
    clock = nx.line_graph(H)
    clock_nodes = sorted(clock.nodes(), key=repr)

    W = w33_collinearity_graph()
    matter = nx.complement(W)

    # Verify graph parameters.
    assert H.number_of_nodes() == 14 and H.number_of_edges() == 21
    assert clock.number_of_nodes() == 21 and clock.number_of_edges() == 42
    assert sorted(set(dict(clock.degree()).values())) == [4]
    assert W.number_of_nodes() == 40 and W.number_of_edges() == 240
    assert sorted(set(dict(W.degree()).values())) == [12]
    assert matter.number_of_edges() == 540
    assert sorted(set(dict(matter.degree()).values())) == [27]

    clock_spec = counter(laplacian_spectrum(clock, clock_nodes))
    matter_spec = counter(laplacian_spectrum(matter, list(range(40))))

    assert clock_spec == {"0.0": 1, "1.585786": 6, "4.414214": 6, "6.0": 8}
    assert matter_spec == {"0.0": 1, "24.0": 15, "30.0": 24}

    sqrt2 = math.sqrt(2)
    clock_blocks = [
        (0.0, 1, "clock ground"),
        (3 - sqrt2, 6, "clock lower oscillator shell"),
        (3 + sqrt2, 6, "clock upper oscillator shell"),
        (6.0, 8, "clock endpoint/runtime word shell"),
    ]
    matter_blocks = [
        (0.0, 1, "matter ground"),
        (24.0, 15, "matter mass gap"),
        (30.0, 24, "matter top shell"),
    ]

    components = []
    coupled = Counter()
    for ce, cm, cname in clock_blocks:
        for me, mm, mname in matter_blocks:
            eig = round(ce + me, 6)
            mult = cm * mm
            coupled[eig] += mult
            components.append(
                {
                    "clock_block": cname,
                    "clock_eigenvalue": round(ce, 6),
                    "clock_mult": cm,
                    "matter_block": mname,
                    "matter_eigenvalue": round(me, 6),
                    "matter_mult": mm,
                    "coupled_eigenvalue": eig,
                    "product_mult": mult,
                }
            )

    coupled_spectrum = {str(k): int(v) for k, v in sorted(coupled.items())}
    assert sum(coupled.values()) == clock.number_of_nodes() * matter.number_of_nodes() == 840
    assert coupled[30.0] == 144

    resonance_rank = 8 * 15
    resonance_eigenvalue = 6 + 24
    degeneracy_at_30 = coupled[30.0]
    companion_rank_at_30 = 1 * 24
    assert resonance_rank == 120
    assert resonance_eigenvalue == 30
    assert degeneracy_at_30 == resonance_rank + companion_rank_at_30 == 144

    result = {
        "theorem": "BT1655 Clock-to-Matter Spectral Coupling Theorem",
        "construction": "Cartesian/tensor graph-product Laplacian L_clock⊗I + I⊗L_matter, using clock=L(Heawood) and matter=complement(W33).",
        "clock_graph": {
            "name": "line graph of Heawood/Fano incidence clock",
            "vertices": clock.number_of_nodes(),
            "edges": clock.number_of_edges(),
            "regular_degree": [4],
            "laplacian_spectrum": clock_spec,
        },
        "matter_graph": {
            "name": "complement of W(3,3)",
            "vertices": matter.number_of_nodes(),
            "edges": matter.number_of_edges(),
            "regular_degree": [27],
            "laplacian_spectrum": matter_spec,
        },
        "coupled_spectrum": coupled_spectrum,
        "blocks": components,
        "resonance": {
            "clock_endpoint_eigenvalue": 6,
            "clock_endpoint_rank": 8,
            "matter_gap_eigenvalue": 24,
            "matter_gap_rank": 15,
            "coupled_eigenvalue": resonance_eigenvalue,
            "rank": resonance_rank,
            "interpretation": "clock endpoint 6^8 times matter gap 24^15 lands exactly at 30=h(E8), with rank 120.",
        },
        "degeneracy_boundary": {
            "total_30_eigenspace_rank": degeneracy_at_30,
            "resonant_subblock_rank": resonance_rank,
            "clock_ground_times_matter_top_rank": companion_rank_at_30,
            "boundary": "The 30-eigenspace is degenerate: the 120-dimensional clock-endpoint×matter-gap block shares eigenvalue 30 with a 24-dimensional clock-ground×matter-top block. The coupling theorem identifies a canonical tensor subblock, not a unique spectral eigenspace without projectors.",
        },
    }

    out_path = Path("data/PART_BT1655_CLOCK_MATTER_SPECTRAL_COUPLING_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
