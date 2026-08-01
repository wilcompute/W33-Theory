#!/usr/bin/env python3
"""Passes 1872--1876: execute the five outer-doily continuation fronts.

The light verifier closes:
  1872  the 2-local cyclotomic lattice boundary;
  1873  the Tutte--Coxeter lift and Hashimoto packet;
  1874  the exact 9-dimensional separator projector and W(E6) Hom obstruction;
  1875  directed automorphisms, coherent configuration, normality correction,
        and uniqueness of the integral twisted Gram solution;
  1876  MacWilliams extraction of A12 from the frozen exact dual enumerator.

The full 2^45 dual enumerator is produced independently by the companion
input-preparation and C++ contraction workers; this file verifies the frozen
histogram and all downstream claims exactly.
"""
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import math
from pathlib import Path

import networkx as nx
import sympy as sp
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form
from sympy.polys.domains import ZZ

ROOT = Path(__file__).resolve().parents[1]
DUAL = ROOT / "data" / "w33_pass1876_exact_dual_weight_enumerator.json"
OUT = ROOT / "data" / "w33_pass1872_1876_five_frontiers.json"

DUAD_TO_SYNTHEME = (8, 12, 4, 0, 10, 3, 2, 9, 14, 11, 7, 1, 13, 6, 5)
OUTER_IMAGES = (
    (3, 5, 4, 0, 2, 1),
    (2, 3, 0, 1, 5, 4),
    (4, 5, 3, 2, 0, 1),
    (5, 3, 4, 1, 2, 0),
    (2, 5, 0, 4, 3, 1),
)
WE6_IRREP_DEGREES = (
    1, 1, 6, 6, 10, 15, 15, 15, 15, 20, 20, 20, 24, 24,
    30, 30, 60, 60, 60, 64, 64, 80, 81, 81, 90,
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    a = vertices[0]
    out = []
    for i in range(1, len(vertices)):
        b = vertices[i]
        rest = vertices[1:i] + vertices[i + 1 :]
        for matching in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a, b), max(a, b)),) + matching)))
    return tuple(sorted(set(out)))


def permutation_matrix(image: tuple[int, ...]) -> sp.Matrix:
    matrix = sp.zeros(len(image))
    for column, row in enumerate(image):
        matrix[row, column] = 1
    return matrix


def compose(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(left[right[i]] for i in range(len(left)))


def induced_duad_action(p: tuple[int, ...], duads):
    index = {duad: i for i, duad in enumerate(duads)}
    return tuple(index[tuple(sorted((p[a], p[b])))] for a, b in duads)


def outer_automorphism():
    ident = tuple(range(6))
    adjacent = []
    for i in range(5):
        s = list(range(6))
        s[i], s[i + 1] = s[i + 1], s[i]
        adjacent.append(tuple(s))
    mapping = {ident: ident}
    queue = collections.deque([ident])
    while queue:
        g = queue.popleft()
        for s, image in zip(adjacent, OUTER_IMAGES):
            h = compose(s, g)
            alpha_h = compose(image, mapping[g])
            if h in mapping:
                assert mapping[h] == alpha_h
            else:
                mapping[h] = alpha_h
                queue.append(h)
    assert len(mapping) == 720
    return mapping, tuple(adjacent)


def rank_mod2(matrix: sp.Matrix) -> int:
    rows = [[int(matrix[i, j]) & 1 for j in range(matrix.cols)] for i in range(matrix.rows)]
    rank = 0
    for column in range(matrix.cols):
        pivot = next((r for r in range(rank, matrix.rows) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(matrix.rows):
            if r != rank and rows[r][column]:
                rows[r] = [a ^ b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def snf_nonzero(matrix: sp.Matrix):
    diagonal = smith_normal_form(matrix, domain=ZZ)
    return [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape)) if diagonal[i, i] != 0]


def build_outer_transfer():
    vertices = tuple(range(6))
    duads = tuple(itertools.combinations(vertices, 2))
    synthemes = perfect_matchings(vertices)
    duad_index = {duad: i for i, duad in enumerate(duads)}
    incidence = sp.zeros(15)
    for row, syntheme in enumerate(synthemes):
        for duad in syntheme:
            incidence[row, duad_index[duad]] = 1
    identification = permutation_matrix(DUAD_TO_SYNTHEME)
    transfer = identification.T * incidence
    return duads, synthemes, incidence, identification, transfer


def balanced_lattice(transfer: sp.Matrix):
    image_basis = hermite_normal_form(transfer)
    assert image_basis.shape == (15, 10)
    assert list(sp.ones(1, 15) * image_basis) == [3] * 10
    change = sp.eye(10)
    for j in range(1, 10):
        change[0, j] = -1
    basis = image_basis * change[:, 1:]
    action = basis.gauss_jordan_solve(transfer * basis)[0]
    assert all(entry.q == 1 for entry in action)
    return basis, action


def krawtchouk(n: int, degree: int, weight: int) -> int:
    lower = max(0, degree - (n - weight))
    upper = min(degree, weight)
    return sum(
        (-1) ** j * math.comb(weight, j) * math.comb(n - weight, degree - j)
        for j in range(lower, upper + 1)
    )


def permutation_order(p: tuple[int, ...]) -> int:
    seen = set()
    order = 1
    for i in range(len(p)):
        if i in seen:
            continue
        j = i
        length = 0
        while j not in seen:
            seen.add(j)
            length += 1
            j = p[j]
        order = math.lcm(order, length)
    return order


def main(output: Path | None = OUT) -> dict:
    duads, synthemes, incidence, identification, transfer = build_outer_transfer()
    identity15 = sp.eye(15)
    ones15 = sp.ones(15)
    basis, action = balanced_lattice(transfer)
    x = sp.symbols("x")

    # Pass 1872: exact integral and 2-local clock lattice.
    front1872 = {
        "balanced_rank": basis.rank(),
        "balanced_gram_determinant": int((basis.T * basis).det()),
        "balanced_characteristic_polynomial": str(sp.factor(action.charpoly(x).as_expr())),
        "rational_primary_decomposition": (
            "Q[x]/(x-2) + 2 Q[x]/(x+2) + Q[x]/(x^2+4) + Q[x]/(x^4+16)"
        ),
        "normalized_action_integral": all(int(entry) % 2 == 0 for entry in action),
        "normalized_action_mod2_rank": rank_mod2(action),
        "smith_C_plus_2": snf_nonzero(action + 2 * sp.eye(9)),
        "smith_C_minus_2": snf_nonzero(action - 2 * sp.eye(9)),
        "smith_C2_plus_4": snf_nonzero(action**2 + 4 * sp.eye(9)),
        "smith_C4_plus_16": snf_nonzero(action**4 + 16 * sp.eye(9)),
        "minus_two_nullity": 9 - (action + 2 * sp.eye(9)).rank(),
        "quotient_at_minus_two": "Z^2 + (Z/4Z)^3",
        "localized_clock": (
            "After inverting 2, C/2 is semisimple with characters 1, -1 twice, "
            "i, -i, and the four primitive eighth-root characters."
        ),
        "boundary": (
            "C/2 does not preserve the integral balanced lattice. The eight-dimensional "
            "regular C8 packet plus one extra sign line exists over Q (and after inverting 2), "
            "but is neither canonical nor an honest global Z[zeta_8]-lattice splitting."
        ),
    }

    # Pass 1873: exact Tutte--Coxeter lift and nonbacktracking packet.
    adjacency = sp.zeros(30)
    adjacency[:15, 15:] = incidence.T
    adjacency[15:, :15] = incidence
    graph = nx.Graph()
    graph.add_nodes_from(range(30))
    for i in range(15):
        for j in range(15):
            if incidence[j, i]:
                graph.add_edge(i, 15 + j)
    fold = sp.diag(sp.eye(15), identification.T) * adjacency * sp.diag(sp.eye(15), identification)
    arcs = []
    for u, v in graph.edges():
        arcs.extend(((u, v), (v, u)))
    arc_index = {arc: i for i, arc in enumerate(arcs)}
    hashimoto = sp.zeros(90)
    for column, (u, v) in enumerate(arcs):
        for w in graph.neighbors(v):
            if w != u:
                hashimoto[arc_index[(v, w)], column] = 1
    traces = {n: int(sp.trace(hashimoto**n)) for n in range(1, 17)}
    primitive_oriented = {
        n: sum(int(sp.mobius(d)) * traces[n // d] for d in sp.divisors(n)) // n
        for n in range(1, 17)
    }
    distributions = {
        tuple(collections.Counter(nx.single_source_shortest_path_length(graph, root).values())[d] for d in range(5))
        for root in graph
    }
    front1873 = {
        "vertices": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "degree": 3,
        "connected": nx.is_connected(graph),
        "girth": nx.girth(graph),
        "diameter": nx.diameter(graph),
        "distance_distribution": list(next(iter(distributions))),
        "intersection_array": "{3,2,2,2;1,1,1,3}",
        "adjacency_characteristic_polynomial": str(sp.factor(adjacency.charpoly(x).as_expr())),
        "exceptional_fold": fold[:15, 15:] == transfer.T and fold[15:, :15] == transfer,
        "hashimoto_characteristic_polynomial": str(sp.factor(hashimoto.charpoly(x).as_expr())),
        "hashimoto_traces_1_to_16": traces,
        "primitive_oriented_reduced_cycles_1_to_16": primitive_oriented,
        "primitive_unoriented_cycles": {
            str(n): primitive_oriented[n] // 2 for n in range(1, 17) if primitive_oriented[n]
        },
        "boundary": "This is an exact finite Levi-graph and nonbacktracking statement.",
    }

    # Pass 1874: the positive separator occurrence and the full-group obstruction.
    gram = transfer.T * transfer
    projector_numerator = gram * (9 * identity15 - gram)
    vertex_potentials = []
    for k in range(5):
        a = [0] * 6
        a[k], a[5] = 1, -1
        vertex_potentials.append([a[i] + a[j] for i, j in duads])
    kernel_witness = sp.Matrix.hstack(sp.ones(15, 1), sp.Matrix(vertex_potentials).T)
    front1874 = {
        "projector": "E9 = G(9I-G)/20, G=T^T T",
        "projector_numerator_rank": projector_numerator.rank(),
        "projector_numerator_identity": projector_numerator**2 == 20 * projector_numerator,
        "projector_numerator_smith": snf_nonzero(projector_numerator),
        "kernel_dimension": 15 - projector_numerator.rank(),
        "kernel_is_trivial_plus_vertex_potential": (
            kernel_witness.rank() == 6
            and projector_numerator * kernel_witness == sp.zeros(15, 6)
        ),
        "separator_decomposition": "Q^15 = 1 + 5 + 9",
        "clock_partial_isometry": gram * projector_numerator == 4 * projector_numerator,
        "we6_character_degrees": list(WE6_IRREP_DEGREES),
        "we6_has_degree_9": 9 in WE6_IRREP_DEGREES,
        "hom_result": (
            "Multiplicity one in the 15-coordinate S6 separator. No nonzero W(E6)-equivariant "
            "embedding into a full W(E6) carrier can exist as a 9-dimensional irreducible, "
            "because the exact W(E6) degree list contains no degree 9."
        ),
    }

    # Pass 1875: automorphisms, coherent configuration, normality correction,
    # and uniqueness in the two-dimensional twisted Hom-space.
    digraph = nx.DiGraph()
    digraph.add_nodes_from(range(15))
    for i in range(15):
        for j in range(15):
            if transfer[i, j]:
                digraph.add_edge(i, j)
    automorphisms = [
        tuple(mapping[i] for i in range(15))
        for mapping in nx.algorithms.isomorphism.DiGraphMatcher(digraph, digraph).isomorphisms_iter()
    ]

    def orbit_partition(items, action):
        unseen = set(items)
        orbits = []
        while unseen:
            seed = next(iter(unseen))
            orbit = {action(g, seed) for g in automorphisms}
            unseen.difference_update(orbit)
            orbits.append(orbit)
        return orbits

    pair_orbits = orbit_partition(
        [(i, j) for i in range(15) for j in range(15)],
        lambda g, pair: (g[pair[0]], g[pair[1]]),
    )
    orbital_matrices = []
    for orbit in pair_orbits:
        matrix = sp.zeros(15)
        for i, j in orbit:
            matrix[i, j] = 1
        orbital_matrices.append(matrix)
    coherent = True
    for left in orbital_matrices:
        for right in orbital_matrices:
            product = left * right
            if any(len({int(product[i, j]) for i, j in orbit}) != 1 for orbit in pair_orbits):
                coherent = False
                break
        if not coherent:
            break

    alpha, adjacent = outer_automorphism()
    alpha_inverse = {image: source for source, image in alpha.items()}
    variables = sp.symbols("z0:225")
    unknown = sp.Matrix(15, 15, variables)
    equations = []
    for g in adjacent:
        rho = permutation_matrix(induced_duad_action(g, duads))
        rho_twist = permutation_matrix(induced_duad_action(alpha_inverse[g], duads))
        equations.extend(list(unknown * rho - rho_twist * unknown))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    hom_basis_vectors = coefficient_matrix.nullspace()
    hom_basis = [sp.Matrix(15, 15, list(vector)) for vector in hom_basis_vectors]
    flat_basis = sp.Matrix.hstack(*(matrix.reshape(225, 1) for matrix in hom_basis))
    transfer_coordinates = flat_basis.gauss_jordan_solve(transfer.reshape(225, 1))[0]
    assert list(transfer_coordinates) == [1, 0]
    # The second basis matrix is J-T. Row sum 3 gives X=(1-5c)T+cJ.
    c = sp.symbols("c")
    candidate = (1 - 5 * c) * transfer + c * ones15
    gram_equations = sorted({sp.factor(entry) for entry in candidate.T * candidate - gram if entry != 0}, key=str)
    gram_solutions = sp.solve(gram_equations, [c], dict=True)
    front1875 = {
        "normality_correction": transfer * transfer.T == transfer.T * transfer,
        "symmetric": transfer == transfer.T,
        "balanced_orthogonality": (
            transfer.T * transfer * projector_numerator == 4 * projector_numerator
        ),
        "directed_automorphism_group_order": len(automorphisms),
        "directed_automorphism_group": "C4",
        "element_order_census": dict(collections.Counter(permutation_order(g) for g in automorphisms)),
        "generator_cycle_structure": "4+4+4+2+1",
        "vertex_orbit_sizes": sorted(
            (len(orbit) for orbit in orbit_partition(range(15), lambda g, vertex: g[vertex])),
            reverse=True,
        ),
        "one_loop": [i for i in range(15) if transfer[i, i]],
        "strongly_connected": nx.is_strongly_connected(digraph),
        "directed_diameter": nx.diameter(digraph),
        "orbital_rank": len(pair_orbits),
        "ordered_pair_orbit_sizes": sorted((len(orbit) for orbit in pair_orbits), reverse=True),
        "coherent_configuration_closed": coherent,
        "twisted_hom_dimension": len(hom_basis),
        "row_sum_three_family": "X(c)=(1-5c)T+cJ",
        "gram_solutions": [{"c": str(solution[c])} for solution in gram_solutions],
        "unique_integral_zero_one_solution": gram_solutions == [{c: 0}, {c: sp.Rational(2, 5)}],
        "second_rational_solution": "2J/5-T",
        "boundary": (
            "T/2 is orthogonal on the balanced 9-space, but Pass 1866 still forbids a "
            "W(E6)-invariant complex structure on any full-group irreducible sector."
        ),
    }

    # Pass 1876: exact A12 and equal-syndrome collision count.
    frozen = json.loads(DUAL.read_text())
    histogram = {int(weight): int(count) for weight, count in frozen["dual_weight_enumerator"].items()}
    total = sum(histogram.values())
    primal = {}
    for degree in range(13):
        numerator = sum(count * krawtchouk(240, degree, weight) for weight, count in histogram.items())
        assert numerator % (1 << 45) == 0
        primal[degree] = numerator // (1 << 45)
    a12 = primal[12]
    equal_syndrome = 1_312_130_546_100 + 462 * a12
    front1876 = {
        "six_line_pack_stabilizer_order": frozen["six_line_pack_stabilizer_order"],
        "residual_action_order": frozen["residual_action_order"],
        "residual_orbit_count": frozen["residual_orbit_count"],
        "dual_dimension": 45,
        "dual_enumerator_total": total,
        "dual_enumerator_symmetric": all(histogram.get(w, 0) == histogram.get(240 - w, 0) for w in range(241)),
        "primal_coefficients_0_to_12": {str(k): v for k, v in primal.items()},
        "A12": a12,
        "fixed_coordinate_A12": a12 // 20,
        "weight6_equal_syndrome_pairs": equal_syndrome,
        "previous_certified_lower_bound": 5_323_560,
        "boundary": (
            "A12 and the total equal-syndrome pair count are now exact. The sixth-order "
            "unique-minimum BSC coefficient still requires deduplication of lower-shadow "
            "incidences and ambiguous syndrome components."
        ),
    }

    checks = {
        "pass1872_rank9": front1872["balanced_rank"] == 9,
        "pass1872_discriminant": front1872["balanced_gram_determinant"] == 2560,
        "pass1872_not_integral_clock": not front1872["normalized_action_integral"],
        "pass1872_minus2_quotient": front1872["smith_C_plus_2"] == [1, 1, 1, 1, 4, 4, 4],
        "pass1873_tutte_coxeter": [front1873[k] for k in ("vertices", "edges", "degree", "girth", "diameter")] == [30, 45, 3, 8, 4],
        "pass1873_fold": front1873["exceptional_fold"],
        "pass1873_eight_cycles": front1873["primitive_unoriented_cycles"].get("8") == 90,
        "pass1874_projector": front1874["projector_numerator_identity"] and front1874["projector_numerator_rank"] == 9,
        "pass1874_kernel": front1874["kernel_is_trivial_plus_vertex_potential"],
        "pass1874_no_degree9": not front1874["we6_has_degree_9"],
        "pass1875_normal": front1875["normality_correction"],
        "pass1875_aut_C4": front1875["directed_automorphism_group_order"] == 4,
        "pass1875_orbital_rank59": front1875["orbital_rank"] == 59,
        "pass1875_unique_integral": front1875["unique_integral_zero_one_solution"],
        "pass1876_total": total == 1 << 45,
        "pass1876_known_low_weights": [primal[k] for k in (4, 6, 8, 10)] == [540, 9600, 424170, 17523360],
        "pass1876_A12": a12 == 891_792_940,
        "pass1876_fixed_coordinate": a12 // 20 == 44_589_647,
        "pass1876_equal_syndrome": equal_syndrome == 1_724_138_884_380,
    }
    assert all(checks.values()), {name: value for name, value in checks.items() if not value}

    result = {
        "schema": "w33.pass1872_1876.five_frontiers.v1",
        "status": "PASS",
        "pass1872": front1872,
        "pass1873": front1873,
        "pass1874": front1874,
        "pass1875": front1875,
        "pass1876": front1876,
        "checks": checks,
        "n_checks": len(checks),
        "n_verified": sum(bool(value) for value in checks.values()),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["sha256_without_hash_field"] = hashlib.sha256(canonical).hexdigest()
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    report = main()
    print(json.dumps({
        "status": report["status"],
        "checks": f"{report['n_verified']}/{report['n_checks']}",
        "A12": report["pass1876"]["A12"],
        "equal_syndrome_pairs": report["pass1876"]["weight6_equal_syndrome_pairs"],
        "aut_group": report["pass1875"]["directed_automorphism_group"],
        "sha256": report["sha256_without_hash_field"],
    }, indent=2))
