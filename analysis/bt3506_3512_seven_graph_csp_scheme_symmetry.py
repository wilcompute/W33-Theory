#!/usr/bin/env python3
"""Passes 3506-3512: seven-graph descendants, Moore CSP, schemes and symmetry.

All promoted claims in this module are finite, exact, and reproducible with the
Python standard library.  Recent literature statuses are recorded as explicit
boundaries rather than re-proved here.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any, Hashable

Vertex = Hashable
Graph = dict[Vertex, set[Vertex]]


def add_edge(g: Graph, u: Vertex, v: Vertex) -> None:
    g[u].add(v)
    g[v].add(u)


def graph_parameters(g: Graph) -> list[Any]:
    vertices = list(g)
    degrees = {len(g[v]) for v in vertices}
    adjacent_common: set[int] = set()
    nonadjacent_common: set[int] = set()
    for index, u in enumerate(vertices):
        for v in vertices[index + 1 :]:
            common = len(g[u] & g[v])
            if v in g[u]:
                adjacent_common.add(common)
            else:
                nonadjacent_common.add(common)
    return [
        len(vertices),
        sorted(degrees),
        sorted(adjacent_common),
        sorted(nonadjacent_common),
        sum(len(g[v]) for v in vertices) // 2,
    ]


def induced(g: Graph, vertices: set[Vertex]) -> Graph:
    return {v: g[v] & vertices for v in vertices}


def clebsch_graph() -> Graph:
    vertices = [x for x in range(32) if x.bit_count() % 2 == 0]
    g = {x: set() for x in vertices}
    for u, v in combinations(vertices, 2):
        if (u ^ v).bit_count() == 4:
            add_edge(g, u, v)
    return g


def clebsch_petersen_descendant() -> dict[str, Any]:
    g = clebsch_graph()
    assert graph_parameters(g)[:4] == [16, [5], [0], [2]]
    base = 0
    shell2 = set(g) - {base} - g[base]
    petersen = induced(g, shell2)
    assert graph_parameters(petersen)[:4] == [10, [3], [0], [1]]
    weights = sorted(v.bit_count() for v in shell2)
    assert weights == [2] * 10
    return {
        "parent": "Clebsch",
        "parent_parameters": [16, 5, 0, 2],
        "operation": "second_subconstituent_at_00000",
        "child": "Petersen",
        "child_parameters": [10, 3, 0, 1],
        "literal_model": "even_weight_F2^5; adjacency_at_Hamming_distance_4",
        "child_model": "weight_2_words; adjacency_iff_disjoint_supports",
    }


def extended_binary_golay_words() -> list[int]:
    """Generate the extended binary Golay code from a standard cyclic generator."""
    generator_positions = [11, 9, 7, 6, 5, 1, 0]
    words: list[int] = []
    for message in range(1 << 12):
        word23 = 0
        for shift in range(12):
            if (message >> shift) & 1:
                for pos in generator_positions:
                    word23 ^= 1 << (pos + shift)
        parity = word23.bit_count() & 1
        words.append(word23 | (parity << 23))
    assert len(set(words)) == 4096
    distribution = Counter(word.bit_count() for word in words)
    assert distribution == Counter({12: 2576, 8: 759, 16: 759, 0: 1, 24: 1})
    return words


def witt_hexads() -> list[frozenset[int]]:
    """Derive S(3,6,22) by fixing two coordinates in Golay octads."""
    words = extended_binary_golay_words()
    hexads = set()
    fixed = (22, 23)
    for word in words:
        if word.bit_count() == 8 and all((word >> c) & 1 for c in fixed):
            hexads.add(frozenset(i for i in range(22) if (word >> i) & 1))
    assert len(hexads) == 77
    triple_counts: Counter[tuple[int, int, int]] = Counter()
    for block in hexads:
        for triple in combinations(sorted(block), 3):
            triple_counts[triple] += 1
    assert len(triple_counts) == 1540
    assert set(triple_counts.values()) == {1}
    return sorted(hexads, key=lambda x: tuple(sorted(x)))


def witt_descendant_atlas() -> dict[str, Any]:
    hexads = witt_hexads()
    m22: Graph = {block: set() for block in hexads}
    for u, v in combinations(hexads, 2):
        if u.isdisjoint(v):
            add_edge(m22, u, v)
    assert graph_parameters(m22)[:4] == [77, [16], [0], [4]]

    point = 0
    avoid = {block for block in hexads if point not in block}
    gewirtz = induced(m22, avoid)
    assert graph_parameters(gewirtz)[:4] == [56, [10], [0], [2]]

    infinity: Vertex = ("infinity",)
    points: list[Vertex] = [("point", i) for i in range(22)]
    block_vertices: list[Vertex] = [("hexad", i) for i in range(77)]
    hs: Graph = {infinity: set()}
    hs.update({v: set() for v in points})
    hs.update({v: set() for v in block_vertices})
    for p in points:
        add_edge(hs, infinity, p)
    for index, block in enumerate(hexads):
        bv = ("hexad", index)
        for p in block:
            add_edge(hs, ("point", p), bv)
    for i, j in combinations(range(77), 2):
        if hexads[i].isdisjoint(hexads[j]):
            add_edge(hs, ("hexad", i), ("hexad", j))
    assert graph_parameters(hs)[:4] == [100, [22], [0], [6]]

    second_shell = set(hs) - {infinity} - hs[infinity]
    hs_second = induced(hs, second_shell)
    assert graph_parameters(hs_second)[:4] == [77, [16], [0], [4]]
    assert sorted(len(hs_second[("hexad", i)]) for i in range(77)) == [16] * 77

    return {
        "Golay_weight_distribution": {"0": 1, "8": 759, "12": 2576, "16": 759, "24": 1},
        "Witt_design": {"points": 22, "blocks": 77, "block_size": 6, "lambda_3": 1},
        "Higman_Sims": [100, 22, 0, 6],
        "HS_second_subconstituent": {"child": "M22", "parameters": [77, 16, 0, 4]},
        "M22_point_avoidance": {"child": "Gewirtz", "parameters": [56, 10, 0, 2]},
        "construction_boundary": "literal_Golay_Witt_construction_not_only_parameter_matching",
    }


def mu4_r2_parameters(lam: int) -> tuple[int, int, int, int, int, int, int, int]:
    mu, r = 4, 2
    s = lam - 6
    k = 16 - 2 * lam
    v = (lam - 7) * (3 * lam - 22) // 2
    fr = (lam - 5) * (3 * lam - 22) // 2
    fs = -3 * (lam - 7)
    return v, k, lam, mu, r, s, fr, fs


def krein_parameters(v: int, k: int, lam: int, mu: int, r: int, s: int, fr: int, fs: int) -> dict[str, list[str]]:
    """Exact q_ij^h for the rank-three Bose-Mesner algebra."""
    P = [
        [Fraction(1), Fraction(k), Fraction(v - k - 1)],
        [Fraction(1), Fraction(r), Fraction(-r - 1)],
        [Fraction(1), Fraction(s), Fraction(-s - 1)],
    ]
    multiplicities = [1, fr, fs]
    valencies = [1, k, v - k - 1]
    Q = [
        [Fraction(multiplicities[i]) * P[i][ell] / valencies[ell] for i in range(3)]
        for ell in range(3)
    ]
    out: dict[str, list[str]] = {}
    for i, j in [(1, 1), (1, 2), (2, 2)]:
        values = []
        for h in range(3):
            q = sum(Q[ell][i] * Q[ell][j] * P[h][ell] for ell in range(3)) / v
            values.append(str(q))
            assert q >= 0
        out[f"q{i}{j}"] = values
    return out


def scheme_blindness_ladder() -> dict[str, Any]:
    labels = ["M22", "57_vertex_hole", "W33_class", "Paulus_class", "T6"]
    rows = []
    for lam, label in enumerate(labels):
        v, k, la, mu, r, s, fr, fs = mu4_r2_parameters(lam)
        assert (v - k - 1) * mu == k * (k - la - 1)
        absolute = {
            "r_embedding_bound": fr * (fr + 3) // 2,
            "s_embedding_bound": fs * (fs + 3) // 2,
        }
        assert v <= absolute["r_embedding_bound"]
        assert v <= absolute["s_embedding_bound"]
        rows.append(
            {
                "lambda": lam,
                "name": label,
                "parameters": [v, k, la, mu],
                "spectrum": {"eigenvalues": [k, r, s], "multiplicities": [1, fr, fs]},
                "absolute_bounds": absolute,
                "krein": krein_parameters(v, k, la, mu, r, s, fr, fs),
            }
        )
    assert rows[1]["parameters"] == [57, 14, 1, 4]
    return {
        "rows": rows,
        "all_parameter_spectral_absolute_krein_tests_pass": True,
        "obstruction_location": (
            "The nonexistent lambda=1 rung is invisible to the rank-three "
            "Bose-Mesner/Krein/absolute-bound layer; published proofs require "
            "finer local or star-complement compatibility."
        ),
    }


def reduce_polynomial(coefficients: list[int]) -> tuple[int, int]:
    """Reduce sum c_n x^n modulo x^2+2x-8, returning a*x+b."""
    a, b = 0, 0
    for c in reversed(coefficients):
        a, b = b - 2 * a, 8 * a
        b += c
    return a, b


def spectral_transplant_compiler() -> dict[str, Any]:
    examples = {}
    for coefficients in ([0, 1], [0, 0, 1], [1, -3, 2, 1], [7, 0, 0, 0, 1]):
        a, b = reduce_polynomial(list(coefficients))
        examples[str(list(coefficients))] = [a, b]
        for x in (2, -4):
            lhs = sum(c * x**n for n, c in enumerate(coefficients))
            assert lhs == a * x + b
    for x in (2, -4):
        u = Fraction(-1 - x, 3)
        assert u * u == 1
    return {
        "quotient_ring": "Q[x]/(x^2+2*x-8)",
        "normal_form": "a*A+b*I",
        "examples_coefficients_low_to_high": examples,
        "shared_by": {
            "W33": {"multiplicities": [24, 15]},
            "Gewirtz": {"multiplicities": [35, 20]},
        },
        "universal_reflection": "U=(-I-A)/3_on_augmentation; U^2=I",
        "universal_projectors": ["(I+U)/2", "(I-U)/2"],
        "classification": {
            "polynomial_only": [
                "adjacency_polynomial_identities",
                "two_channel_functional_calculus",
                "centered_complement_reflection",
            ],
            "multiplicity_sensitive": ["trace", "determinant", "projector_ranks"],
            "geometry_sensitive": [
                "cliques_and_lines",
                "incidence_factorizations",
                "automorphism_group",
                "codes_and_descendant_maps",
            ],
        },
    }


def hoffman_singleton_graph() -> Graph:
    """Classical 5 pentagons + 5 pentagrams construction."""
    g: Graph = {("p", i, j): set() for i in range(5) for j in range(5)}
    g.update({("q", i, j): set() for i in range(5) for j in range(5)})
    for i in range(5):
        for j in range(5):
            add_edge(g, ("p", i, j), ("p", i, (j + 1) % 5))
            add_edge(g, ("q", i, j), ("q", i, (j + 2) % 5))
    for i in range(5):
        for j in range(5):
            for k in range(5):
                add_edge(g, ("p", i, j), ("q", k, (i * k + j) % 5))
    assert graph_parameters(g)[:4] == [50, [7], [0], [1]]
    return g


def inverse_permutation(p: tuple[int, ...]) -> tuple[int, ...]:
    q = [0] * len(p)
    for i, value in enumerate(p):
        q[value] = i
    return tuple(q)


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths: list[int] = []
    for start in range(len(p)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            current = p[current]
            length += 1
        lengths.append(length)
    return tuple(sorted(lengths))


def edge_rooted_permutations(g: Graph, a: Vertex, b: Vertex) -> dict[tuple[int, int], tuple[int, ...]]:
    assert b in g[a]
    left = sorted(g[a] - {b}, key=repr)
    right = sorted(g[b] - {a}, key=repr)
    residual = set(g) - {a, b} - set(left) - set(right)
    assert len(left) == len(right)
    n = len(left)
    cell: dict[tuple[int, int], Vertex] = {}
    inverse_cell: dict[Vertex, tuple[int, int]] = {}
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            common = (g[x] & g[y]) & residual
            assert len(common) == 1
            vertex = next(iter(common))
            cell[(i, j)] = vertex
            inverse_cell[vertex] = (i, j)
    assert len(cell) == n * n

    sigma: dict[tuple[int, int], tuple[int, ...]] = {}
    row_sets = [{cell[(i, col)] for col in range(n)} for i in range(n)]
    for i, j in combinations(range(n), 2):
        image = []
        for col in range(n):
            neighbors = g[cell[(i, col)]] & row_sets[j]
            assert len(neighbors) == 1
            image.append(inverse_cell[next(iter(neighbors))][1])
        assert len(set(image)) == n
        assert all(image[col] != col for col in range(n))
        sigma[(i, j)] = tuple(image)
    return sigma


def oriented_sigma(sigma: dict[tuple[int, int], tuple[int, ...]], i: int, j: int) -> tuple[int, ...]:
    return sigma[(i, j)] if i < j else inverse_permutation(sigma[(j, i)])


def moore_holonomy_atlas() -> dict[str, Any]:
    hs = hoffman_singleton_graph()
    a = ("p", 0, 0)
    b = sorted(hs[a], key=repr)[0]
    sigma = edge_rooted_permutations(hs, a, b)
    matching_types = Counter(cycle_type(p) for p in sigma.values())
    holonomy_types: Counter[tuple[int, ...]] = Counter()
    for i, j, k in combinations(range(6), 3):
        holonomy = compose(
            oriented_sigma(sigma, k, i),
            compose(oriented_sigma(sigma, j, k), oriented_sigma(sigma, i, j)),
        )
        assert all(holonomy[x] != x for x in range(6))
        holonomy_types[cycle_type(holonomy)] += 1
    assert matching_types == Counter({(2, 2, 2): 15})
    assert holonomy_types == Counter({(2, 2, 2): 20})
    return {
        "known_witness": "Hoffman_Singleton_edge_chart",
        "fibre_size": 6,
        "pair_matchings": {"count": 15, "cycle_type": "2^3"},
        "triangle_holonomies": {"count": 20, "cycle_type": "2^3"},
        "gauge_invariant": "holonomy_cycle_type_is_conjugacy_invariant",
        "bonkers_M57_branch": (
            "Search first inside the non-necessary ansatz where all 1540 "
            "row-pair matchings and all 27720 triangle holonomies are "
            "fixed-point-free involutions of cycle type 2^28."
        ),
        "boundary": "The involutive-curvature ansatz is inspired by HS, not necessary for M57.",
    }


def math_comb(n: int, r: int) -> int:
    from math import comb
    return comb(n, r)


def m57_csp_blueprint() -> dict[str, Any]:
    n = 56
    unordered_pairs = n * (n - 1) // 2
    independent_entries = unordered_pairs * n
    directed_entries = n * (n - 1) * n
    one_hot_nonfixed = unordered_pairs * n * (n - 1)
    row_permutation_constraints = unordered_pairs
    vertex_star_constraints = n * n
    inverse_channel_constraints = unordered_pairs
    gauge_equalities = n - 1
    triangle_row_triples = math_comb(n, 3)
    return {
        "fibre_size": n,
        "independent_permutation_entries": independent_entries,
        "CP_SAT_directed_integer_variables_with_explicit_inverses": directed_entries,
        "one_hot_boolean_baseline": one_hot_nonfixed,
        "constraints_before_lazy_cuts": {
            "row_pair_AllDifferent": row_permutation_constraints,
            "inverse_channels": inverse_channel_constraints,
            "vertex_star_AllDifferent": vertex_star_constraints,
            "base_vertex_gauge_equalities": gauge_equalities,
            "total_structural_constraints": (
                row_permutation_constraints
                + inverse_channel_constraints
                + vertex_star_constraints
                + gauge_equalities
            ),
        },
        "row_triples_for_curvature_separation": triangle_row_triples,
        "lazy_cut_families": [
            "triangle_holonomy_fixed_point_nogoods",
            "nonadjacent_residual_pair_common_neighbor_nogoods",
        ],
        "gauge": "sigma_0j(0)=j_for_j=1..55",
        "exporter": "analysis/bt3506_m57_permutation_csp.py",
        "boundary": "source-complete_model; no 56-fibre solution or unsat certificate claimed",
    }


def symmetry_firewall() -> dict[str, Any]:
    psl = 19 * (19 * 19 - 1) // 2
    assert psl == 3420
    borel = 19 * 9
    assert borel == 171 and psl % borel == 0
    return {
        "PSL2_19_order": psl,
        "Borel_19_semidirect_9_order": borel,
        "M57_automorphism_bounds_peer_reviewed": {
            "odd_order_case_at_most": 375,
            "even_order_case_at_most": 110,
        },
        "recent_preprint_boundary": "no_involutions_would_force_Aut_M57_to_have_odd_order",
        "conditional_consequences": [
            "Aut_M57_would_be_solvable_by_the_odd_order_theorem",
            "no_A5_or_PSL2_19_subgroup",
            "the_existing_A5_20_plane_comparison_cannot_be_an_actual_common_A5_automorphism_action",
        ],
        "surviving_symmetry_shadow": (
            "Parity alone does not exclude the odd Borel subgroup 19:9 of "
            "order 171, which lies below the peer-reviewed odd-order bound 375."
        ),
        "next_exact_test": "restrict_Perkl_minus3_module_to_the_19:9_Borel_shadow",
    }


def build_certificate() -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "PASS_7_FRONTS",
        "passes": list(range(3506, 3513)),
        "front_3506_m57_csp": m57_csp_blueprint(),
        "front_3507_descendant_atlas": {
            "Clebsch_to_Petersen": clebsch_petersen_descendant(),
            "Golay_Witt_chain": witt_descendant_atlas(),
        },
        "front_3508_scheme_blindness": scheme_blindness_ladder(),
        "front_3509_spectral_transplant": spectral_transplant_compiler(),
        "front_3510_symmetry_firewall": symmetry_firewall(),
        "front_3511_bonkers_nonabelian_curvature": moore_holonomy_atlas(),
        "front_3512_bonkers_Golay_puncture_functor": {
            "operations": [
                "extend_cyclic_Golay_23_to_24_by_parity",
                "fix_two_coordinates_in_octads_to_obtain_77_hexads",
                "take_disjointness_graph_to_obtain_M22",
                "avoid_one_point_to_obtain_Gewirtz",
                "adjoin_22_points_and_infinity_to_reconstruct_Higman_Sims",
            ],
            "interpretation": (
                "The HS-M22-Gewirtz chain is an executable puncture/avoidance "
                "functor on one Golay-Witt incidence object, not three isolated graphs."
            ),
            "boundary": "combinatorial_functor_language_not_a_category_equivalence_with_W33",
        },
        "evidence_boundary": [
            "No existence or nonexistence result for M57 is claimed.",
            "The full M57 CP-SAT instance is emitted but not solved.",
            "The involutive-holonomy branch is a high-risk ansatz, not a theorem about M57.",
            "Ordinary Krein feasibility does not prove graph existence.",
            "The 2026 no-involution result remains a recent preprint.",
            "No canonical W33-Gewirtz objectwise intertwiner is asserted.",
        ],
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


def main() -> None:
    result = build_certificate()
    output = Path("data/PART_BT3506_BT3512_SEVEN_GRAPH_CSP_SCHEME_SYMMETRY_results.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"], result["semantic_sha256"])


if __name__ == "__main__":
    main()
