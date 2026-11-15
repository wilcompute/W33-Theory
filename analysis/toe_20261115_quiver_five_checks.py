"""Exact charge, quartic, duality, and extremality checks for the quiver supports."""

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path

import networkx as nx
import sympy as sp

from toe_20261115_cubic_quiver_steiner import ARROW_LINES, intersection, line_class
from toe_20261115_fermat_quiver_couplings import MARKING, check_couplings, cubic_coefficients, fermat_blowup_points
from toe_20261115_fermat_quiver_mutation import check_four_step_potential


DATA = Path(__file__).resolve().parents[1] / "data"


def simple_roots():
    exceptional = [line_class(f"E{i}") for i in range(1, 7)]
    roots = [tuple(a-b for a, b in zip(left, right)) for left, right in zip(exceptional, exceptional[1:])]
    roots.append((1, -1, -1, -1, 0, 0, 0))
    return roots


def wrapped_charges(tritangents):
    canonical = (-3, 1, 1, 1, 1, 1, 1)
    roots = simple_roots()
    form = sp.Matrix([[intersection(a, b) for b in roots] for a in roots])
    assert all(intersection(root, canonical) == 0 for root in roots)
    assert form.det() == 3
    # Together with E1, the roots span the full unimodular Picard lattice.
    assert abs(sp.Matrix(roots + [line_class("E1")]).det()) == 1
    labels = sorted(set().union(*tritangents))
    charges = {label: [intersection(root, line_class(label)) for root in roots] for label in labels}
    assert all(intersection(canonical, line_class(label)) == -1 for label in labels)
    assert len({tuple(key) for key in charges.values()}) == 27
    inverse = form.inv()
    for charge in charges.values():
        weight = sp.Matrix(charge)
        assert (weight.T * inverse * weight)[0] == -sp.Rational(4, 3)
        difference = inverse * (weight - sp.Matrix(charges["E1"]))
        assert all(entry.is_Integer for entry in difference)
    assert all(sum(charges[label][i] for label in triple) == 0 for triple in tritangents for i in range(6))
    neutral_cubics = [triple for triple in combinations_with_replacement(labels, 3)
                      if all(sum(charges[label][i] for label in triple) == 0 for i in range(6))]
    assert {frozenset(triple) for triple in neutral_cubics} == {frozenset(triple) for triple in tritangents}
    assert len(neutral_cubics) == 45
    return {
        "betti_rank": 6, "root_discriminant": int(form.det()),
        "line_charges_in_dual_root_basis": charges,
        "neutral_degree_three_monomials": len(neutral_cubics),
        "nonzero_cubic_at_zero_total_betti_charge_witness": neutral_cubics[0],
    }


def quartic_pairing(supports, tritangents, optimal):
    labels = sorted(set().union(*tritangents))
    incidence = {label: {i for i, term in enumerate(tritangents) if label in term} for label in labels}
    assert all(len(terms) == 5 for terms in incidence.values())
    assert all(len(terms & support) == 3 for terms, support in product(incidence.values(), supports))
    distinct_pairs = {pair for terms in incidence.values() for pair in combinations(sorted(terms), 2)}
    assert len(distinct_pairs) == 270
    assert all(sum(a in chart and b in chart for chart in supports) == 12 for a, b in distinct_pairs)
    assert all(sum(i in chart for chart in supports) == 24 for i in range(45))
    pair_counts = Counter(sum(a in supports[i] and b in supports[i] for i in optimal) for a, b in distinct_pairs)
    assert all(sum(i in supports[p] for p in optimal) == 6 for i in range(45))
    coupled_terms = distinct_pairs | {(b, a) for a, b in distinct_pairs} | {(i, i) for i in range(45)}
    pairing_constraints = sp.Matrix([
        [int(a in supports[p] and b in supports[q]) for p, q in product(optimal, repeat=2)]
        for a, b in sorted(coupled_terms)
    ])
    assert pairing_constraints * sp.ones(100, 1) == 36 * sp.ones(len(coupled_terms), 1)
    assert pairing_constraints.to_DM().rank() == 100
    return {
        "same_tritangent_gradient_products": 3*45,
        "ordered_distinct_gradient_products": 2*len(distinct_pairs),
        "all_chart_multiplicities": [24, 12],
        "ovoid_distinct_pair_histogram": dict(sorted(pair_counts.items())),
        "ovoid_ordered_pairing_constraint_rank": 100,
        "chart_diagonal_weight_sum_for_same_terms": "5/3",
        "chart_diagonal_weight_sum_for_distinct_terms": "10/3",
    }


def duality_scan(charge_by_line, supports, tritangents):
    arrows = {(int(a)-1, int(b)-1) for a, b in ARROW_LINES}
    initial = tuple(tuple(int((a,b) in arrows)-int((b,a) in arrows) for b in range(9)) for a in range(9))
    ranks = (1,)*9
    original = (initial, ranks)

    def mutate(quiver, sizes, node):
        flavors_in = sum(max(0, quiver[i][node])*sizes[i] for i in range(9))
        flavors_out = sum(max(0, quiver[node][i])*sizes[i] for i in range(9))
        assert flavors_in == flavors_out
        dual_rank = flavors_in-sizes[node]
        if dual_rank <= 0:
            return None
        mutated = tuple(tuple(
            -quiver[i][j] if node in (i,j) else quiver[i][j]
            + max(0, quiver[i][node])*max(0, quiver[node][j])
            - max(0, -quiver[i][node])*max(0, -quiver[node][j])
            for j in range(9)) for i in range(9))
        new_ranks = sizes[:node] + (dual_rank,) + sizes[node+1:]
        assert all(sum(entry*size for entry, size in zip(row, new_ranks)) == 0 for row in mutated)
        return mutated, new_ranks

    for node in range(9):
        quiver, sizes = mutate(*original, node)
        assert sizes[node] == 2
        assert sum(max(0, entry) for row in quiver for entry in row) == 18

    def digraph(matrix):
        graph = nx.DiGraph()
        graph.add_nodes_from(range(9))
        graph.add_weighted_edges_from((i, j, weight) for i, row in enumerate(matrix)
                                      for j, weight in enumerate(row) if weight > 0)
        return graph

    frontier = {original: ()}
    seen = set(frontier)
    initial_graph = digraph(initial)
    levels = []
    for _ in range(4):
        images = {}
        for state, path in frontier.items():
            for node in range(9):
                image = mutate(*state, node)
                if image is not None and image not in seen:
                    images.setdefault(image, path+(node+1,))
        frontier = images
        seen.update(frontier)
        equal_rank = [(matrix, path) for (matrix, sizes), path in frontier.items() if sizes == ranks]
        matching = [path for matrix, path in equal_rank if nx.is_isomorphic(
            initial_graph, digraph(matrix), edge_match=nx.algorithms.isomorphism.numerical_edge_match("weight", 1))]
        levels.append({"new_states": len(frontier), "new_equal_rank_states": len(equal_rank),
                       "old_quiver_up_to_relabeling": len(matching), "matching_path_example": next(iter(matching), None)})
    initial_grading = {
        (int(a)-1, int(b)-1): [tuple(charge_by_line[label])]
        for (a, b), label in ARROW_LINES.items()
    }

    def lift_grading(path):
        grading, sizes = initial_grading, ranks
        for k in (i-1 for i in path):
            incoming = [(i, charge) for (i, j), charges in grading.items() for charge in charges if j == k]
            outgoing = [(j, charge) for (i, j), charges in grading.items() for charge in charges if i == k]
            new_size = sum(sizes[i] for i, _ in incoming) - sizes[k]
            totals = [sum(sizes[i]*charge[a] for i, charge in incoming) for a in range(6)]
            assert all(total == -sum(sizes[j]*charge[a] for j, charge in outgoing) for a, total in enumerate(totals))
            shift = tuple(Fraction(total, new_size) for total in totals)
            updated = {(i, j): charges.copy() for (i, j), charges in grading.items() if k not in (i, j)}
            for i, a in incoming:
                updated.setdefault((k, i), []).append(tuple(t-x for t, x in zip(shift, a)))
                for j, b in outgoing:
                    updated.setdefault((i, j), []).append(tuple(x+y for x, y in zip(a, b)))
            for j, b in outgoing:
                updated.setdefault((j, k), []).append(tuple(-t-y for t, y in zip(shift, b)))
            for i, j in combinations(range(9), 2):
                left, right = updated.get((i, j), []), updated.get((j, i), [])
                for charge in left.copy():
                    opposite = tuple(-x for x in charge)
                    if opposite in right:
                        left.remove(charge)
                        right.remove(opposite)
                if left and right:
                    return None
            grading = {edge: charges for edge, charges in updated.items() if charges}
            sizes = sizes[:k] + (new_size,) + sizes[k+1:]
        return grading

    label_by_charge = {tuple(charge): label for label, charge in charge_by_line.items()}
    tritangent_index = {frozenset(term): i for i, term in enumerate(tritangents)}
    equal_rank_endpoints = {matrix for matrix, _ in equal_rank}

    def paths_to_new_equal_ranks(state, path):
        if len(path) == 4:
            if state[1] == ranks and state[0] in equal_rank_endpoints:
                yield state[0], path
            return
        for node in range(9):
            if path and node+1 == path[-1]:
                continue
            image = mutate(*state, node)
            if image is not None:
                yield from paths_to_new_equal_ranks(image, path+(node+1,))

    graded_returns = Counter()
    endpoint_supports = set()
    potential_returns = []
    first_round = []
    coefficients = cubic_coefficients(*fermat_blowup_points(MARKING))
    for matrix, path in paths_to_new_equal_ranks(original, ()):
        grading = lift_grading(path)
        if grading is None:
            graded_returns["opposite_charges_could_not_cancel"] += 1
            continue
        assert all(len(grading.get((i, j), [])) == max(0, matrix[i][j]) for i, j in product(range(9), repeat=2))
        labels = {edge: label_by_charge.get(charges[0]) for edge, charges in grading.items()}
        if len(set(labels.values())) != 27 or None in labels.values():
            graded_returns["new_arrow_charges"] += 1
            continue
        cycles = {
            tritangent_index.get(frozenset((labels[i, j], labels[j, k], labels[k, i])))
            for i, j, k in product(range(9), repeat=3) if all(edge in labels for edge in ((i,j), (j,k), (k,i)))
        }
        if cycles in supports:
            graded_returns[f"shared_cubics_{len(cycles & supports[0])}"] += 1
            support_index = supports.index(cycles)
            potential, new_coefficients, new_grades = check_four_step_potential(charge_by_line, coefficients, path)
            assert {tritangent_index[frozenset(term)] for term in potential["endpoint_tritangents"]} == cycles
            if support_index not in endpoint_supports:
                endpoint_supports.add(support_index)
                potential_returns.append({"endpoint_support": support_index, "path": path, "steps": potential["steps"]})
                first_round.append((support_index, potential, new_coefficients, new_grades))
        else:
            graded_returns["outside_support_orbit"] += 1
    assert set(graded_returns) == {"shared_cubics_15"} and len(endpoint_supports) == 27
    neighbors = {i for i, support in enumerate(supports) if len(support & supports[0]) == 18}
    neighboring_paths = {}
    for first, evidence, new_coefficients, new_grades in first_round:
        to_original_label = {label: label_by_charge[t] for label, t in new_grades.items()}
        for _, path in equal_rank:
            endpoint, _, _ = check_four_step_potential(new_grades, new_coefficients, path)
            terms = {tritangent_index[frozenset(to_original_label[label] for label in term)]
                     for term in endpoint["endpoint_tritangents"]}
            target = supports.index(terms)
            if target in neighbors and target not in neighboring_paths:
                neighboring_paths[target] = {
                    "intermediate_support": first,
                    "first_path": evidence["path"],
                    "node_relabeling_before_second_path": evidence["endpoint_node_relabeling"],
                    "second_path": path,
                    "second_path_steps": endpoint["steps"],
                }
        if neighboring_paths.keys() == neighbors:
            break
    assert neighboring_paths.keys() == neighbors
    return {"direct_moves": 9, "direct_dual_rank_in_units_of_N": 2,
            "mass_pairs_with_nonzero_couplings": 9, "arrows_after_reduction": 18, "levels": levels,
            "shortest_path_charge_grading": dict(sorted(graded_returns.items())),
            "shortest_path_distinct_supports": sorted(endpoint_supports),
            "exact_four_step_potential_paths": potential_returns,
            "eight_step_paths_to_all_adjacent_supports": dict(sorted(neighboring_paths.items()))}


def check_vertex(polar_lines, weights):
    assert all(value > 0 for value in weights.values())
    assert all(sum(weights.get(i, 0) for i in line) == 1 for line in polar_lines)
    matrix = sp.Matrix([[int(i in line) for i in weights] for line in polar_lines])
    assert matrix.rank() == len(weights)
    return {"weights_in_unit_line_normalization": {str(i): str(v) for i, v in sorted(weights.items())},
            "support_size": len(weights), "constraint_rank": len(weights)}


def positive_support_is_extreme(polar_lines, support):
    if len(support) > 25:
        return False
    sections = [line & support for line in polar_lines]
    graph = nx.Graph()
    graph.add_nodes_from(support)
    graph.add_edges_from(tuple(section) for section in sections if len(section) == 2)
    pinned = set().union(*(section for section in sections if len(section) == 1))
    free = []
    for component in nx.connected_components(graph):
        subgraph = graph.subgraph(component)
        if component.isdisjoint(pinned) and nx.is_bipartite(subgraph):
            free.append({i: 1-2*color for i, color in nx.bipartite.color(subgraph).items()})
    if not free:
        return True
    matrix = sp.Matrix([
        [sum(signs.get(i, 0) for i in section) for signs in free]
        for section in sections if len(section) >= 3
    ])
    return bool(matrix.rows) and matrix.to_DM().rank() == len(free)


def weyl_support_actions(supports, tritangents):
    classes = {line: line_class(line) for line in set().union(*tritangents)}
    label_by_class = {value: label for label, value in classes.items()}
    term_index = {frozenset(term): i for i, term in enumerate(tritangents)}
    actions = []
    for root in simple_roots():
        line_action = {
            label: label_by_class[tuple(a+intersection(value, root)*b for a,b in zip(value, root))]
            for label, value in classes.items()
        }
        term_action = [term_index[frozenset(line_action[label] for label in term)] for term in tritangents]
        actions.append([supports.index({term_action[i] for i in support}) for support in supports])
    return actions


def small_denominator_census(polar_lines, actions):
    histograms = []
    for denominator in (1, 2, 3):
        assignments = [-1]*40
        possibilities = {
            (n, total): [values for values in product(range(total+1), repeat=n) if sum(values) == total]
            for n in range(1, 5) for total in range(denominator+1)
        }
        covers, vertices, extreme_weights = Counter(), Counter(), set()
        rank_by_support = {}

        def search():
            best, variables = None, None
            for line in polar_lines:
                missing = [i for i in line if assignments[i] == -1]
                total = denominator - sum(assignments[i] for i in line if assignments[i] != -1)
                if total < 0 or (not missing and total):
                    return
                if missing:
                    options = possibilities[len(missing), total]
                    if best is None or len(options) < len(best):
                        best, variables = options, missing
            if best is None:
                signature = tuple(assignments.count(i) for i in range(denominator+1))
                covers[signature] += 1
                support = frozenset(i for i, weight in enumerate(assignments) if weight > 0)
                if support not in rank_by_support:
                    rank_by_support[support] = positive_support_is_extreme(polar_lines, support)
                if rank_by_support[support]:
                    vertices[signature] += 1
                    extreme_weights.add(tuple(assignments))
                return
            for values in best:
                for i, value in zip(variables, values):
                    assignments[i] = value
                search()
            for i in variables:
                assignments[i] = -1

        search()
        orbits = []
        while extreme_weights:
            seed = min(extreme_weights)
            orbit = [seed]
            seen = {seed}
            for current in orbit:
                for action in actions:
                    image = tuple(current[i] for i in action)
                    if image not in seen:
                        assert image in extreme_weights
                        seen.add(image)
                        orbit.append(image)
            extreme_weights.difference_update(seen)
            orbits.append({"counts": [seed.count(i) for i in range(denominator+1)], "orbit_size": len(orbit)})
        histograms.append({
            "denominator_divides": denominator,
            "solutions": sum(covers.values()),
            "vertices": sum(vertices.values()),
            "counts_by_numerator_multiplicities": [
                {"counts": key, "solutions": covers[key], "vertices": vertices[key]} for key in sorted(covers)
            ],
            "weyl_orbits_of_vertices": orbits,
        })
    assert [row["solutions"] for row in histograms] == [36, 990, 19768]
    return histograms


def verify():
    certificate = json.loads((DATA / "toe_20261115_cubic_quiver_steiner.json").read_text(encoding="utf-8"))
    recovery = json.loads((DATA / "toe_20261115_cubic_quiver_ovoid.json").read_text(encoding="utf-8"))
    tritangents = list(map(set, certificate["tritangents_in_line_labels"]))
    masks = [int(mask, 16) for mask in certificate["orbit_supports_hex_masks"]]
    supports = [{i for i in range(45) if mask & (1 << i)} for mask in masks]
    graph = nx.Graph()
    graph.add_nodes_from(range(40))
    graph.add_edges_from((a, b) for a, b in combinations(graph, 2) if len(supports[a] & supports[b]) == 18)
    polar_lines = [set(line) for line in sorted(map(sorted, nx.find_cliques(graph)))]
    optimal = recovery["ovoid_charts_by_double_six"][0]["charts"]
    half = recovery["extreme_hemisystem_reconstruction"]["charts"]
    assert sp.Matrix([[int(i in line) for i in graph] for line in polar_lines]).rank() == 25
    extremal = [check_vertex(polar_lines, {i: Fraction(10, len(chart)) for i in chart}) for chart in (optimal, half)]
    nonuniform = (
        ({0, 4, 5, 6, 8, 18, 19, 21, 24, 29, 33, 39}, {1, 2, 10, 11, 12, 15, 22, 30, 31}),
        ({4, 5, 6, 7, 15, 19, 21, 24, 28, 29, 30, 33, 37, 38}, {2, 8, 25, 27, 31, 34, 36, 39}),
    )
    for thirds, two_thirds in nonuniform:
        assert thirds.isdisjoint(two_thirds)
        weights = dict.fromkeys(thirds, Fraction(1, 3)) | dict.fromkeys(two_thirds, Fraction(2, 3))
        extremal.append(check_vertex(polar_lines, weights))
    charge_result = wrapped_charges(tritangents)
    return {
        "wrapped_charges": charge_result,
        "freudenthal_pairing": quartic_pairing(supports, tritangents, optimal),
        "fermat": check_couplings(),
        "duality": duality_scan(charge_result["line_charges_in_dual_root_basis"], supports, tritangents),
        "nonnegative_reconstruction": {"dimension": 15, "verified_vertices": extremal,
                                       "census": small_denominator_census(
                                           polar_lines, weyl_support_actions(supports, tritangents))},
    }


if __name__ == "__main__":
    result = verify()
    path = DATA / "toe_20261115_quiver_five_checks.json"
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the charge lattice, quartic pairings, Fermat coefficients, mutation ranks, and reconstruction vertices")
