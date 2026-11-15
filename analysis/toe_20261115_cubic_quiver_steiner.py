"""Map the published cubic del Pezzo quiver supports to finite polar geometry."""

import json
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path

import networkx as nx


# X_ab -> line label in Franco–Hanany–Kazakopoulos, eq. (3.34).
ARROW_LINES = dict(item.split(":") for item in (
    "81:E1 82:E2 83:E3 47:E4 57:E5 67:E6 93:L12 92:L13 14:L14 "
    "15:L15 16:L16 91:L23 24:L24 25:L25 26:L26 34:L34 35:L35 36:L36 "
    "69:L45 59:L46 49:L56 71:Q1 72:Q2 73:Q3 48:Q4 58:Q5 68:Q6"
).split())


def line_class(label):
    indices = [int(i) for i in label[1:]]
    if label[0] == "E":
        return (0,) + tuple(int(i in indices) for i in range(1, 7))
    if label[0] == "L":
        return (1,) + tuple(-int(i in indices) for i in range(1, 7))
    return (2,) + tuple(-int(i not in indices) for i in range(1, 7))


def intersection(a, b):
    return a[0]*b[0]-sum(x*y for x, y in zip(a[1:], b[1:]))


def projective_points(dimension):
    return [v for v in product(range(3), repeat=dimension) if next((x for x in v if x), 0) == 1]


def polar_graph(dimension, quadratic, pairing):
    points = [v for v in projective_points(dimension) if quadratic(v) % 3 == 0]
    graph = nx.Graph()
    graph.add_nodes_from(points)
    graph.add_edges_from((a, b) for a, b in combinations(points, 2) if pairing(a, b) % 3 == 0)
    return graph


def independent_triad_census(graph):
    neighbors = {vertex: set(graph[vertex]) for vertex in graph}
    return Counter(
        len(neighbors[a] & neighbors[b] & neighbors[c])
        for a, b, c in combinations(graph, 3)
        if b not in neighbors[a] and c not in neighbors[a] and c not in neighbors[b]
    )


def verify():
    arrows = list(ARROW_LINES)
    labels = list(ARROW_LINES.values())
    lines = [line_class(label) for label in labels]
    lookup = {line: i for i, line in enumerate(lines)}
    tritangents = [triple for triple in combinations(range(27), 3)
                  if all(intersection(lines[a], lines[b]) == 1 for a, b in combinations(triple, 2))]
    tritangent_lookup = {triple: i for i, triple in enumerate(tritangents)}

    def directed_triangle(triple):
        for a, b, c in permutations(arrows[i] for i in triple):
            if a[1] == b[0] and b[1] == c[0] and c[1] == a[0]:
                return True
        return False

    paths = [triple for triple in combinations(range(27), 3) if directed_triangle(triple)]
    assert len(tritangents) == 45 and len(paths) == 27
    support = frozenset(tritangent_lookup[triple] for triple in paths)
    blocks = ["123", "456", "789"]
    determinants = set()
    for first, second in zip(blocks, blocks[1:]+blocks[:1]):
        for matching in permutations(second):
            determinants.add(tuple(sorted(arrows.index(a+b) for a, b in zip(first, matching))))
    assert len(determinants) == 18
    assert determinants == set(tritangents)-set(paths)

    roots = [(0,) + tuple(int(j == i)-int(j == i+1) for j in range(1, 7)) for i in range(1, 6)]
    roots.append((1, -1, -1, -1, 0, 0, 0))
    generators = []
    for root in roots:
        action = [lookup[tuple(v+intersection(line, root)*w for v, w in zip(line, root))] for line in lines]
        generators.append([tritangent_lookup[tuple(sorted(action[i] for i in triple))] for triple in tritangents])
    orbit = [support]
    visited = {support}
    for member in orbit:
        for action in generators:
            image = frozenset(action[i] for i in member)
            if image not in visited:
                orbit.append(image)
                visited.add(image)
    assert len(orbit) == 40
    intersections = Counter(len(support & member) for member in orbit[1:])
    assert intersections == {15: 27, 18: 12}

    overlap_graph = nx.Graph()
    overlap_graph.add_nodes_from(range(40))
    overlap_graph.add_edges_from((i, j) for i, j in combinations(range(40), 2) if len(orbit[i] & orbit[j]) == 18)
    symplectic = polar_graph(4, lambda _: 0, lambda a, b: a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])
    parabolic = polar_graph(5, lambda a: a[0]*a[1]+a[2]*a[3]+a[4]**2,
                            lambda a, b: a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2]+2*a[4]*b[4])
    candidates = {"W(3,3)": symplectic, "Q(4,3)": parabolic}
    census = {name: independent_triad_census(graph) for name, graph in candidates.items()}
    census["quiver overlaps"] = independent_triad_census(overlap_graph)
    assert census["quiver overlaps"] == census["Q(4,3)"] == {0: 1080, 2: 2160}
    assert census["W(3,3)"] == {1: 2880, 4: 360}
    matcher = nx.algorithms.isomorphism.GraphMatcher(overlap_graph, parabolic)
    assert matcher.is_isomorphic()

    # Recover the tritangents and cubic-surface lines from quadric coordinates.
    points = [matcher.mapping[i] for i in range(len(orbit))]
    sections = [
        (frozenset(i for i, point in enumerate(points) if sum(a*b for a, b in zip(normal, point)) % 3 == 0), normal)
        for normal in projective_points(5)
    ]
    section_sizes = Counter(len(section) for section, _ in sections)
    assert section_sizes == {10: 36, 13: 40, 16: 45}
    hyperbolic = {section: normal for section, normal in sections if len(section) == 16}
    omitted = [frozenset(i for i, member in enumerate(orbit) if j not in member) for j in range(len(tritangents))]
    assert len(omitted) == len(set(omitted)) == len(hyperbolic)
    assert set(omitted) == set(hyperbolic)

    tritangent_graph = nx.Graph()
    tritangent_graph.add_nodes_from(range(len(tritangents)))
    for i, j in combinations(range(len(tritangents)), 2):
        shares_line = bool(set(tritangents[i]) & set(tritangents[j]))
        assert len(omitted[i] & omitted[j]) == (4 if shares_line else 7)
        if shares_line:
            tritangent_graph.add_edge(i, j)
    line_stars = {
        frozenset(i for i, triple in enumerate(tritangents) if line in triple): label
        for line, label in enumerate(labels)
    }
    assert len(line_stars) == 27 and all(len(star) == 5 for star in line_stars)
    assert {frozenset(clique) for clique in nx.find_cliques(tritangent_graph)} == set(line_stars)

    # Cyclic block permutations preserve the arrow orientation. The other
    # block permutations act on line labels after reversing every arrow.
    orientation_actions = Counter()
    for block_images in permutations(range(3)):
        preserves_direction = block_images[1] == (block_images[0] + 1) % 3
        for images in product(*(permutations(blocks[i]) for i in block_images)):
            node_map = dict(zip("123456789", sum(images, ())))
            pairs = arrows if preserves_direction else [arrow[::-1] for arrow in arrows]
            action = [arrows.index(node_map[a] + node_map[b]) for a, b in pairs]
            assert all(intersection(lines[i], lines[j]) == intersection(lines[action[i]], lines[action[j]])
                       for i, j in combinations(range(27), 2))
            image = {tritangent_lookup[tuple(sorted(action[i] for i in triple))] for triple in paths}
            assert image == support
            orientation_actions["preserving" if preserves_direction else "reversing"] += 1
    assert orientation_actions == {"preserving": 648, "reversing": 648}
    assert sum(orientation_actions.values()) == 51840 // len(orbit)

    return {
        "arrows_to_lines": ARROW_LINES,
        "tritangents": len(tritangents),
        "quiver_cubic_loops": len(paths),
        "determinant_triples": len(determinants),
        "support_orbit_size": len(orbit),
        "support_intersections": dict(sorted(intersections.items())),
        "weyl_support_stabilizer_order": sum(orientation_actions.values()),
        "orientation_actions": orientation_actions,
        "overlap_graph_model": "Q(4,3)",
        "independent_triad_census": census,
        "quadric_hyperplane_section_sizes": section_sizes,
        "omission_hyperplane_covectors": [hyperbolic[section] for section in omitted],
        "line_stars_in_tritangent_indices": {label: sorted(star) for star, label in line_stars.items()},
        "orbit_supports_hex_masks": [hex(sum(1 << i for i in member)) for member in orbit],
        "tritangents_in_line_labels": [[labels[i] for i in triple] for triple in tritangents],
        "overlap_isomorphism": dict(sorted(matcher.mapping.items())),
    }


if __name__ == "__main__":
    result = verify()
    report = json.dumps(result, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261115_cubic_quiver_steiner.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(f"Verified {result['support_orbit_size']} supports on {result['overlap_graph_model']}")
