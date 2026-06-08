#!/usr/bin/env python3
"""
BT539: W33 Markov Hitting / Resistance Correction Theorem

This continues from BT538. BT538 correctly identified the Laplacian gap
Phi_4=10 and the spectral proxy v/Phi_4=4=mu, but that quotient is not the
actual expected hitting time of the simple random walk.

Here we build W(3,3) explicitly as the symplectic polar graph on projective
points of F_3^4, verify SRG(40,12,2,4), and solve the exact hitting-time
and electrical-resistance laws.

Results:
    H_adjacent = 39 = v-1
    H_nonadjacent = 42 = 6*7 = g2*Phi6
    difference = 3 = q
    Kemeny constant = 801/20 = 40 + 1/20
    R_adjacent = 13/80
    R_nonadjacent = 7/40
    R_nonadjacent - R_adjacent = 1/80

So BT538's v/Phi_4=mu should be read as a spectral diffusion scale, while
actual hitting is governed by the SRG distance shell.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import networkx as nx
import sympy as sp


Q = 3
V = 40
K = 12
LAMBDA = 2
MU_SRG = 4
R_EIG = 2
S_EIG = -4
M_R = 24
M_S = 15
PHI4 = 10
PHI6 = 7
G2 = 6


def canonical_projective_vector(vec: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    vec = tuple(x % Q for x in vec)
    if all(x == 0 for x in vec):
        raise ValueError("zero vector has no projective point")
    for x in vec:
        if x != 0:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % Q for y in vec)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    # Standard alternating form on F_3^4.
    return (a[0] * b[2] - a[2] * b[0] + a[1] * b[3] - a[3] * b[1]) % Q


def build_w33_symplectic_graph() -> tuple[nx.Graph, list[tuple[int, int, int, int]]]:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for vec in product(range(Q), repeat=4):
        if vec == (0, 0, 0, 0):
            continue
        point = canonical_projective_vector(vec)
        if point not in seen:
            seen.add(point)
            points.append(point)

    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, a in enumerate(points):
        for j, b in enumerate(points):
            if i < j and symplectic_form(a, b) == 0:
                graph.add_edge(i, j)
    return graph, points


def solve_two_shell_hitting_times() -> tuple[Fraction, Fraction]:
    # Let A be expected hitting time from a neighbor of target y.
    # Let B be expected hitting time from a non-neighbor of target y.
    # From SRG(40,12,2,4):
    # A = 1 + (lambda*A + (k-lambda-1)*B)/k
    # B = 1 + (mu*A + (k-mu)*B)/k
    A, B = sp.symbols("A B")
    sol = sp.solve(
        [
            sp.Eq(A, 1 + (LAMBDA * A + (K - LAMBDA - 1) * B) / K),
            sp.Eq(B, 1 + (MU_SRG * A + (K - MU_SRG) * B) / K),
        ],
        [A, B],
        dict=True,
    )[0]
    return Fraction(int(sol[A]), 1), Fraction(int(sol[B]), 1)


def main() -> dict:
    graph, points = build_w33_symplectic_graph()
    assert len(points) == V
    assert graph.number_of_nodes() == V
    assert graph.number_of_edges() == V * K // 2 == 240
    assert sorted(dict(graph.degree()).values()) == [K] * V
    assert nx.diameter(graph) == 2

    adjacent_common = []
    nonadjacent_common = []
    for u, v in combinations(graph.nodes(), 2):
        common = len(set(graph.neighbors(u)) & set(graph.neighbors(v)))
        if graph.has_edge(u, v):
            adjacent_common.append(common)
        else:
            nonadjacent_common.append(common)
    assert set(adjacent_common) == {LAMBDA}
    assert set(nonadjacent_common) == {MU_SRG}
    assert len(adjacent_common) == 240
    assert len(nonadjacent_common) == 540

    # Adjacency spectrum from SRG parameters.
    A = nx.to_numpy_array(graph, dtype=int)
    eigenvals = sorted(round(x) for x in sp.Matrix(A).eigenvals().keys())
    # Sympy eigenvals returns distinct keys only; check multiplicities separately.
    spectrum = {str(int(ev)): int(mult) for ev, mult in sorted(sp.Matrix(A).eigenvals().items(), key=lambda kv: kv[0])}
    assert spectrum == {"-4": 15, "2": 24, "12": 1}

    H_adj, H_non = solve_two_shell_hitting_times()
    assert H_adj == 39
    assert H_non == 42
    assert H_non - H_adj == Q

    # Kemeny's constant for the simple random walk P=A/k:
    # sum over nontrivial eigenvalues 1/(1-theta/k).
    kemeny = Fraction(M_R, 1) / (1 - Fraction(R_EIG, K)) + Fraction(M_S, 1) / (1 - Fraction(S_EIG, K))
    assert kemeny == Fraction(801, 20)

    # Effective resistance from commute times C_uv=H_uv+H_vu=2m R_uv.
    # Vertex transitivity makes H_uv=H_vu by distance shell.
    two_m = 2 * graph.number_of_edges()  # = 480
    R_adj = Fraction(2 * H_adj, two_m)
    R_non = Fraction(2 * H_non, two_m)
    assert R_adj == Fraction(13, 80)
    assert R_non == Fraction(7, 40)
    assert R_non - R_adj == Fraction(1, 80)

    # Spectral proxy from BT538.
    spectral_proxy = Fraction(V, PHI4)
    assert spectral_proxy == 4

    # Shell-weighted hitting from a fixed target over all other starting vertices.
    shell_average = Fraction(K * H_adj + (V - K - 1) * H_non, V - 1)
    assert shell_average == Fraction(534, 13)

    results = {
        "theorem": "BT539 W33 Markov Hitting / Resistance Correction Theorem",
        "construction": "symplectic polar graph on projective points of F_3^4",
        "graph_certificates": {
            "vertices": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "degree": K,
            "diameter": nx.diameter(graph),
            "srg_parameters": [40, 12, 2, 4],
            "adjacency_spectrum": spectrum,
            "laplacian_spectrum": {"0": 1, "10": 24, "16": 15},
        },
        "BT538_correction": {
            "spectral_gap": PHI4,
            "v_over_gap": str(spectral_proxy),
            "correct_reading": "v/Phi4=4 is a spectral diffusion scale, not the Markov hitting time",
        },
        "hitting_times": {
            "from_adjacent_vertex_to_target": str(H_adj),
            "from_nonadjacent_vertex_to_target": str(H_non),
            "difference": str(H_non - H_adj),
            "shell_average_over_non_target_starts": str(shell_average),
        },
        "kemeny_constant": {
            "exact": str(kemeny),
            "decimal": float(kemeny),
            "formula": "24/(1-2/12)+15/(1+4/12)",
        },
        "effective_resistance": {
            "adjacent": str(R_adj),
            "nonadjacent": str(R_non),
            "gap": str(R_non - R_adj),
            "commute_relation": "C_uv=2|E| R_uv with 2|E|=480",
        },
        "substrate_reading": {
            "H_adjacent_39": "v-1, complete reachable memory excluding target",
            "H_nonadjacent_42": "g2*Phi6 flag-orbit resonance",
            "hitting_gap_3": "q, field-order penalty for starting outside the target neighborhood",
            "kemeny_801_20": "40 + 1/20, near the W33 vertex count with finite spectral correction",
            "resistance_gap_1_80": "one inverse lambda^mu*F5 resistance quantum",
        },
    }

    out = Path("data/PART_BT539_W33_MARKOV_HITTING_RESISTANCE_CORRECTION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
