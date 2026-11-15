"""Check all-support sparsity bounds for the Freudenthal derivative pairing."""

import json
from itertools import combinations, combinations_with_replacement, product
from math import gcd
from pathlib import Path

import networkx as nx
import sympy as sp

from toe_20261115_quiver_five_checks import weyl_support_actions


DATA = Path(__file__).resolve().parents[1] / "data"


def rank_mod_prime(matrix, prime=101):
    """A maximal modular minor gives a lower bound on rational rank."""
    basis = {}
    for values in matrix:
        row = [value % prime for value in values]
        for column, value in enumerate(row):
            if value == 0:
                continue
            if column not in basis:
                inverse = pow(value, -1, prime)
                basis[column] = [x*inverse % prime for x in row[column:]]
                break
            for j, entry in enumerate(basis[column], start=column):
                row[j] = (row[j] - value*entry) % prime
    return len(basis)


def verify():
    quiver = json.loads((DATA / "toe_20261115_cubic_quiver_steiner.json").read_text(encoding="utf-8"))
    recovery = json.loads((DATA / "toe_20261115_cubic_quiver_ovoid.json").read_text(encoding="utf-8"))
    tritangents = list(map(set, quiver["tritangents_in_line_labels"]))
    masks = [int(mask, 16) for mask in quiver["orbit_supports_hex_masks"]]
    supports = [{t for t in range(45) if mask & (1 << t)} for mask in masks]
    s = sp.Matrix([[int(t in support) for t in range(45)] for support in supports])
    ovoids = [frozenset(record["charts"]) for record in recovery["ovoid_charts_by_double_six"]]
    ovoid = sorted(ovoids[0])
    graph = nx.Graph()
    graph.add_nodes_from(range(40))
    graph.add_edges_from((i, j) for i in graph for j in range(i+1, 40)
                         if len(supports[i] & supports[j]) == 18)
    lines = sorted(tuple(sorted(line)) for line in nx.find_cliques(graph))
    b = sp.Matrix([[int(i in line) for line in lines] for i in graph])
    assert len(lines) == 40 and all(len(line) == 4 for line in lines)
    assert s*s.T == 15*sp.ones(40, 40) + 3*b*b.T
    assert b*sp.ones(40, 1) == b.T*sp.ones(40, 1) == 4*sp.ones(40, 1)
    assert s.T*sp.ones(40, 1) == 24*sp.ones(45, 1)
    assert all(
        s[:, [t for t, term in enumerate(tritangents) if label in term]]*sp.ones(5, 1) == 3*sp.ones(40, 1)
        for label in set().union(*tritangents)
    )

    pairs = [(a, b) for a, b in product(range(45), repeat=2) if tritangents[a] & tritangents[b]]
    term_graph = nx.Graph()
    term_graph.add_edges_from(pairs)
    assert len(term_graph) == 45 and nx.is_connected(term_graph)
    assert nx.diameter(term_graph) == 2
    assert len(pairs) == 585
    line_term_counts = b.T*s
    assert all(sorted(line_term_counts.row(i)) == [0]*9 + [3]*36 for i in range(40))
    coefficients = line_term_counts.applyfunc(
        lambda count: sp.Rational(-7, 54) if count == 0 else sp.Rational(1, 27)
    )
    assert s*coefficients.T == b
    assert all(sum(map(abs, coefficients.row(i))) == sp.Rational(5, 2) for i in range(40))

    # A Weyl orbit check transports the one-sided rank witness to all ovoids.
    action_generators = weyl_support_actions(supports, tritangents)
    orbit = [ovoids[0]]
    seen = set(orbit)
    for current in orbit:
        for action in action_generators:
            image = frozenset(action[i] for i in current)
            if image not in seen:
                seen.add(image)
                orbit.append(image)
    assert seen == set(ovoids) and len(seen) == 36
    basis = s.T.rref()[1]
    assert len(basis) == 25
    rectangular_columns = [(p, q) for p in ovoid for q in basis]
    rectangular_rank = rank_mod_prime(
        [int(a in supports[p] and c in supports[q]) for p, q in rectangular_columns]
        for a, c in pairs
    )
    assert rectangular_rank == len(rectangular_columns) == 250
    compressed_ranks = {}
    for name, sign, chart_pairs in (
        ("symmetric", 1, list(combinations_with_replacement(basis, 2))),
        ("alternating", -1, list(combinations(basis, 2))),
    ):
        block = sp.Matrix([
            [int(a in supports[p] and c in supports[q])
             + sign*int(p != q and a in supports[q] and c in supports[p]) for p, q in chart_pairs]
            for a, c in pairs if a < c or (sign == 1 and a == c)
        ])
        compressed_ranks[name] = block.to_DM().rank()
    assert compressed_ranks == {"symmetric": 205, "alternating": 186}

    # Explicit nonnegative coefficients need not give a PSD bilinear form.
    # The perturbation is invisible on all 585 tritangent pairs.
    chart_subset = ovoid + [i for i in graph if i not in ovoid][:8]
    symmetric_columns = list(combinations_with_replacement(chart_subset, 2))
    operator = sp.Matrix([
        [int(a in supports[p] and c in supports[q])
         + int(p != q and a in supports[q] and c in supports[p]) for p, q in symmetric_columns]
        for a, c in pairs if a <= c
    ])
    kernel = operator.to_DM().nullspace().to_Matrix()
    assert kernel.rows == 1
    raw = [int(value) for value in kernel.row(0)]
    divisor = gcd(*raw)
    h = sp.zeros(40, 40)
    for (p, q), value in zip(symmetric_columns, raw):
        h[p, q] = h[q, p] = value // divisor
    invisible = s.T*h*s
    assert all(invisible[a, c] == 0 for a, c in pairs)
    line_residual = b.T*h*b
    i, j = next((i, j) for i, j in product(range(40), repeat=2) if line_residual[i, j])
    divisor = 1152*max(map(abs, h))
    positive_weights = sp.ones(40, 40)/576 + h/divisor
    assert all(value > 0 for value in positive_weights)
    line_pair_weight = (b.T*positive_weights*b)[i, j]
    assert line_pair_weight != sp.Rational(1, 36)

    return {
        "polar_line_pairs": 1600,
        "line_pairs_per_chart_pair": 16,
        "minimum_pairs_for_psd_reconstruction": 100,
        "psd_minimizers": len(ovoids),
        "absolute_coefficient_error_threshold_for_psd_100_pair_bound": "1/2025",
        "polar_line_expansion_l1_norm": "5/2",
        "minimum_pairs_if_either_leg_uses_ten_charts": 100,
        "one_sided_constraint_rank_over_f101": rectangular_rank,
        "all_support_constraint_ranks_over_q": compressed_ranks,
        "all_support_invisible_bilinear_dimension": 25**2 - sum(compressed_ranks.values()),
        "column_basis_chart_indices": list(basis),
        "entrywise_positive_non_psd_example": {
            "uniform_entry": "1/576",
            "perturbation_divisor": int(divisor),
            "integer_symmetric_perturbation_upper_triangle": [
                [p, q, int(h[p, q])] for p in graph for q in range(p, 40) if h[p, q]
            ],
            "line_pair_witness": [lines[i], lines[j]],
            "line_pair_weight": str(line_pair_weight),
        },
    }


if __name__ == "__main__":
    path = DATA / "toe_20261115_freudenthal_support_sparsity.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the all-support PSD bound, one-sided rigidity, and an entrywise-positive counterexample")
