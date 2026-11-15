"""Track and reduce the Fermat quiver potential along a four-mutation path."""

from collections import Counter
from fractions import Fraction
from itertools import product

import networkx as nx

from toe_20261115_cubic_quiver_steiner import ARROW_LINES
from toe_20261115_fermat_quiver_couplings import ZERO, ONE


def add_term(potential, path, coefficient):
    if not coefficient:
        return
    word = min(path[i:] + path[:i] for i in range(len(path)))
    value = potential.get(word, ZERO) + coefficient
    if value:
        potential[word] = value
    else:
        del potential[word]


def reduce_mass_terms(arrows, potential, grades):
    eliminated = 0
    while True:
        mass_terms = [word for word in potential if len(word) == 2]
        if not mass_terms:
            return eliminated
        for mass in mass_terms:
            x, y = mass
            containing = [word for word in potential if x in word or y in word]
            if all(word == mass or word.count(x) + word.count(y) == 1 for word in containing):
                break
        else:
            raise ValueError("The remaining masses need nonlinear elimination")
        x_terms, y_terms = [], []
        for word in containing:
            if word == mass:
                continue
            field = x if x in word else y
            i = word.index(field)
            entry = (word[i+1:] + word[:i], potential.pop(word))
            (x_terms if field == x else y_terms).append(entry)
        coefficient = potential.pop(mass)
        assert all(a+b == 0 for a, b in zip(grades[x], grades[y]))
        for (left, a), (right, b) in product(x_terms, y_terms):
            add_term(potential, left + right, -a*b/coefficient)
        del arrows[x], arrows[y]
        eliminated += 1


def check_four_step_potential(charge_by_line, coefficients, path):
    arrows = {i: (int(a), int(b)) for i, (a, b) in enumerate(ARROW_LINES)}
    grades = {i: tuple(charge_by_line[label]) for i, label in enumerate(ARROW_LINES.values())}
    initial_arrows = {edge: i for i, edge in arrows.items()}
    potential = {}
    for (a, b, c), coefficient in coefficients.items():
        nodes = (a+1, b+4, c+7)
        # Wijnholt's X_ij notation runs oppositely to the arrow convention here.
        add_term(potential, tuple(initial_arrows[i, j] for i, j in zip(nodes, nodes[1:]+nodes[:1])), coefficient)
    sizes = [1]*10
    next_id = len(arrows)
    steps = []
    for node in path:
        incoming = [i for i, (_, b) in arrows.items() if b == node]
        outgoing = [i for i, (a, _) in arrows.items() if a == node]
        flavors = sum(sizes[arrows[i][0]] for i in incoming)
        assert flavors == sum(sizes[arrows[i][1]] for i in outgoing)
        sizes[node] = flavors-sizes[node]
        assert sizes[node] > 0
        shift = tuple(Fraction(sum(sizes[arrows[i][0]]*grades[i][a] for i in incoming), sizes[node])
                      for a in range(6))

        mesons = {}
        for i, j in product(incoming, outgoing):
            mesons[i, j] = next_id
            arrows[next_id] = (arrows[i][0], arrows[j][1])
            grades[next_id] = tuple(a+b for a, b in zip(grades[i], grades[j]))
            next_id += 1

        updated = {}
        for word, coefficient in potential.items():
            start = next(i for i, arrow in enumerate(word) if arrows[arrow][0] != node)
            word = word[start:] + word[:start]
            reduced = []
            cursor = 0
            while cursor < len(word):
                arrow = word[cursor]
                if arrow in incoming:
                    reduced.append(mesons[arrow, word[cursor+1]])
                    cursor += 2
                else:
                    reduced.append(arrow)
                    cursor += 1
            add_term(updated, tuple(reduced), coefficient)
        for i in incoming + outgoing:
            a, b = arrows[i]
            arrows[i] = (b, a)
        for i in incoming:
            grades[i] = tuple(t-a for t, a in zip(shift, grades[i]))
        for i in outgoing:
            grades[i] = tuple(-t-a for t, a in zip(shift, grades[i]))
        for (i, j), meson in mesons.items():
            add_term(updated, (meson, j, i), ONE)
        potential = updated
        count = reduce_mass_terms(arrows, potential, grades)
        assert all(arrows[i][1] == arrows[j][0]
                   for word in potential for i, j in zip(word, word[1:]+word[:1]))
        assert all(sum(grades[i][a] for i in word) == 0 for word in potential for a in range(6))
        for k in range(1, 10):
            incoming_neighbors = [(a, i) for i, (a,b) in arrows.items() if b == k]
            outgoing_neighbors = [(b, i) for i, (a,b) in arrows.items() if a == k]
            assert sum(sizes[j] for j, _ in incoming_neighbors) == sum(sizes[j] for j, _ in outgoing_neighbors)
            assert all(sum(sizes[j]*grades[i][a] for j, i in incoming_neighbors + outgoing_neighbors) == 0
                       for a in range(6))
        edge_set = set(arrows.values())
        assert not any((b,a) in edge_set for a,b in edge_set)
        steps.append({"node": node, "new_rank": sizes[node], "mesons": len(mesons),
                      "eliminated_pairs": count, "arrows": len(arrows),
                      "potential_degrees": dict(sorted(Counter(map(len, potential)).items()))})
    assert sizes[1:] == [1]*9
    assert len(arrows) == len(potential) == 27 and all(len(word) == 3 for word in potential)
    label_by_charge = {tuple(value): label for label, value in charge_by_line.items()}
    endpoint = {i: label_by_charge[grades[i]] for i in arrows}
    assert len(set(endpoint.values())) == 27
    directed = nx.DiGraph()
    directed.add_edges_from(arrows.values())
    reference = nx.DiGraph()
    reference.add_edges_from(initial_arrows)
    node_map = next(nx.algorithms.isomorphism.DiGraphMatcher(reference, directed).isomorphisms_iter())
    arrow_by_edge = {edge: i for i, edge in arrows.items()}
    standardized = {(a,b): arrow_by_edge[node_map[a], node_map[b]] for a,b in initial_arrows}
    new_coefficients = {}
    for a,b,c in product(range(3), repeat=3):
        nodes = a+1, b+4, c+7
        word = tuple(standardized[edge] for edge in zip(nodes, nodes[1:]+nodes[:1]))
        new_coefficients[a,b,c] = potential[min(word[i:] + word[:i] for i in range(3))]
    new_grades = {label: grades[standardized[int(a),int(b)]] for (a,b),label in ARROW_LINES.items()}
    evidence = {
        "path": path, "steps": steps, "endpoint_node_relabeling": node_map,
        "endpoint_tritangents": sorted(tuple(sorted(endpoint[i] for i in word)) for word in potential),
    }
    return evidence, new_coefficients, new_grades
