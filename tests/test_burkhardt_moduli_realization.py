"""
Supplement omega -- Burkhardt quartic moduli realization of W(3,3).

External facts used:

1. The Burkhardt quartic has 40 j-planes and 40 Steiner primes.
2. j-planes are in Galois-covariant bijection with cyclic order-3 subgroups
   of J[3] for the associated genus-2 Jacobian.
3. Two such order-3 subgroups pair trivially iff the corresponding j-planes
   lie in a common Steiner prime.
4. Under the classical Klein duality, W(3,3) is isomorphic to Q(4,3)^dual, so
    W-points correspond to lines on the parabolic quadric Q(4,3).

Executable certificate:

- Model J[3] as F_3^4 with its standard nondegenerate alternating form.
- Cyclic order-3 subgroups are projective 1-spaces: there are 40 of them.
- Maximal totally isotropic 2-spaces are projective lines: there are 40 of them.
- Interpreting projective points as j-planes and isotropic projective lines as
  Steiner primes yields exactly the incidence structure GQ(3,3).
"""

import importlib.util
import json
import sys
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path


F3 = (0, 1, 2)
ZERO4 = (0, 0, 0, 0)
ZERO5 = (0, 0, 0, 0, 0)

Q = 3
POINT_COUNT = 40
LINE_COUNT = 40
LINE_SIZE = 4
LINES_PER_POINT = 4
POINT_DEGREE = 12
LAMBDA = 2
MU = 4
ROOT = Path(__file__).resolve().parents[1]
THIRTYSIX_CARRIER_BIJECTION_ARTIFACT = ROOT / "artifacts" / "burkhardt_thirtysix_carrier_bijection.json"
PAYNE_CUBIC_LOCAL_DICTIONARY_ARTIFACT = ROOT / "artifacts" / "payne_cubic_local_dictionary.json"
PAYNE_QUTRIT_LOCAL_DICTIONARY_ARTIFACT = ROOT / "artifacts" / "payne_qutrit_local_dictionary.json"
PAYNE_HESSE_PACKET_DICTIONARY_ARTIFACT = ROOT / "artifacts" / "payne_hesse_packet_dictionary.json"


def inv_mod_3(value: int) -> int:
    if value == 1:
        return 1
    if value == 2:
        return 2
    raise ValueError("0 has no inverse in F_3")


def normalize(vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for entry in vector:
        if entry:
            scale = inv_mod_3(entry)
            return tuple((scale * coord) % 3 for coord in vector)
    raise ValueError("zero vector cannot be normalized")


def add_scaled(
    a: int,
    left: tuple[int, int, int, int],
    b: int,
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple((a * x + b * y) % 3 for x, y in zip(left, right))


def omega(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> int:
    x1, x2, x3, x4 = left
    y1, y2, y3, y4 = right
    return (x1 * y3 - x3 * y1 + x2 * y4 - x4 * y2) % 3


def build_projective_points() -> list[tuple[int, int, int, int]]:
    points = {
        normalize(vector)
        for vector in product(F3, repeat=4)
        if vector != ZERO4
    }
    return sorted(points)


PROJECTIVE_POINTS = build_projective_points()
POINT_INDEX = {point: index for index, point in enumerate(PROJECTIVE_POINTS)}


def cyclic_order_3_subgroup(
    point: tuple[int, int, int, int],
) -> frozenset[tuple[int, int, int, int]]:
    double = tuple((2 * coord) % 3 for coord in point)
    return frozenset((ZERO4, point, double))


def isotropic_projective_line(
    first: tuple[int, int, int, int],
    second: tuple[int, int, int, int],
) -> frozenset[tuple[int, int, int, int]]:
    if first == second or omega(first, second) != 0:
        raise ValueError("need two distinct orthogonal projective points")
    line = {
        normalize(add_scaled(a, first, b, second))
        for a, b in product(F3, repeat=2)
        if (a, b) != (0, 0)
    }
    return frozenset(line)


def build_isotropic_lines() -> list[frozenset[tuple[int, int, int, int]]]:
    lines = {
        isotropic_projective_line(first, second)
        for first, second in combinations(PROJECTIVE_POINTS, 2)
        if omega(first, second) == 0
    }
    return sorted(lines, key=lambda line: tuple(sorted(line)))


ISOTROPIC_LINES = build_isotropic_lines()
LINES_THROUGH_POINT = {point: [] for point in PROJECTIVE_POINTS}
for line in ISOTROPIC_LINES:
    for point in line:
        LINES_THROUGH_POINT[point].append(line)


def build_point_graph() -> list[set[int]]:
    adjacency = [set() for _ in PROJECTIVE_POINTS]
    for i, first in enumerate(PROJECTIVE_POINTS):
        for j in range(i + 1, len(PROJECTIVE_POINTS)):
            second = PROJECTIVE_POINTS[j]
            if omega(first, second) == 0:
                adjacency[i].add(j)
                adjacency[j].add(i)
    return adjacency


def build_line_graph() -> list[set[int]]:
    adjacency = [set() for _ in ISOTROPIC_LINES]
    for i, left in enumerate(ISOTROPIC_LINES):
        for j in range(i + 1, len(ISOTROPIC_LINES)):
            right = ISOTROPIC_LINES[j]
            if left & right:
                adjacency[i].add(j)
                adjacency[j].add(i)
    return adjacency


POINT_GRAPH = build_point_graph()
LINE_GRAPH = build_line_graph()
INDEX_LINES = [frozenset(POINT_INDEX[point] for point in line) for line in ISOTROPIC_LINES]


def common_neighbor_count(graph: list[set[int]], left: int, right: int) -> int:
    return len(graph[left] & graph[right])


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def overlap_graph(objects: list[frozenset], overlap_size: int) -> list[set[int]]:
    graph = [set() for _ in objects]
    for i, left in enumerate(objects):
        for j in range(i + 1, len(objects)):
            right = objects[j]
            if len(left & right) == overlap_size:
                graph[i].add(j)
                graph[j].add(i)
    return graph


def graph_patterns(graph: list[set[int]]) -> set[tuple[int, int]]:
    return {
        (int(right in graph[left]), common_neighbor_count(graph, left, right))
        for left in range(len(graph))
        for right in range(left + 1, len(graph))
    }


def perfect_matchings_on_six() -> list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    def recurse(vertices: tuple[int, ...]) -> list[list[tuple[int, int]]]:
        if not vertices:
            return [[]]
        first = vertices[0]
        out = []
        for index in range(1, len(vertices)):
            second = vertices[index]
            rest = vertices[1:index] + vertices[index + 1 :]
            for tail in recurse(rest):
                out.append([(first, second)] + tail)
        return out

    return sorted(
        {
            tuple(sorted(tuple(sorted(pair)) for pair in matching))
            for matching in recurse((1, 2, 3, 4, 5, 6))
        }
    )


def build_graph_from_adjacency(adjacency: list[set[int]]):
    import networkx as nx

    graph = nx.Graph()
    graph.add_nodes_from(range(len(adjacency)))
    for vertex, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            if vertex < neighbor:
                graph.add_edge(vertex, neighbor)
    return graph


def canonical_graph_bijection(
    left_adjacency: list[set[int]],
    right_adjacency: list[set[int]],
) -> dict[int, int]:
    from networkx.algorithms import isomorphism as iso

    left_graph = build_graph_from_adjacency(left_adjacency)
    right_graph = build_graph_from_adjacency(right_adjacency)

    def can_extend(partial: dict[int, int]) -> bool:
        colored_left = left_graph.copy()
        colored_right = right_graph.copy()
        inverse = {target: source for source, target in partial.items()}

        for node in colored_left.nodes:
            colored_left.nodes[node]["color"] = f"locked:{node}" if node in partial else "free"
        for node in colored_right.nodes:
            colored_right.nodes[node]["color"] = (
                f"locked:{inverse[node]}" if node in inverse else "free"
            )

        matcher = iso.GraphMatcher(
            colored_left,
            colored_right,
            node_match=lambda left_attrs, right_attrs: left_attrs["color"] == right_attrs["color"],
        )
        return matcher.is_isomorphic()

    mapping: dict[int, int] = {}
    used_targets: set[int] = set()
    for source in range(len(left_adjacency)):
        for target in range(len(right_adjacency)):
            if target in used_targets:
                continue
            trial = dict(mapping)
            trial[source] = target
            if can_extend(trial):
                mapping = trial
                used_targets.add(target)
                break
        else:
            raise AssertionError(f"failed to extend graph isomorphism at source {source}")
    return mapping


@lru_cache(maxsize=1)
def explicit_payne_to_cubic_local_dictionary() -> dict[str, object]:
    _, type1_lines, type2_lines, derived_lines, _, payne_graph = payne_derivation(base_point=0)
    record = build_double_six_data()[0]
    tritangent_mixed = record["tritangent_planes"]["mixed_30"]
    tritangent_c_only = record["tritangent_planes"]["c_only_15"]
    all_tritangents = tritangent_mixed + tritangent_c_only

    cubic_graph = [set() for _ in range(27)]
    for plane in all_tritangents:
        first, second, third = plane["lines"]
        cubic_graph[first].update([second, third])
        cubic_graph[second].update([first, third])
        cubic_graph[third].update([first, second])

    point_mapping = canonical_graph_bijection(payne_graph, cubic_graph)

    type1_images = sorted({tuple(sorted(point_mapping[index] for index in line)) for line in type1_lines})
    type2_images = sorted({tuple(sorted(point_mapping[index] for index in line)) for line in type2_lines})
    tritangent_lookup = {
        tuple(sorted(plane["lines"])): plane for plane in all_tritangents
    }

    return {
        "record": record,
        "point_mapping": point_mapping,
        "derived_lines": sorted({tuple(sorted(point_mapping[index] for index in line)) for line in derived_lines}),
        "type1_images": type1_images,
        "type2_images": type2_images,
        "type1_planes": [tritangent_lookup[triangle] for triangle in type1_images],
        "type2_planes": [tritangent_lookup[triangle] for triangle in type2_images],
        "mixed_30": {tuple(sorted(plane["lines"])) for plane in tritangent_mixed},
        "c_only_15": {tuple(sorted(plane["lines"])) for plane in tritangent_c_only},
    }


@lru_cache(maxsize=1)
def build_h27_qutrit_local_shell() -> dict[str, object]:
    e8_embedding = load_module(ROOT / "tests" / "test_e8_embedding.py", "test_e8_embedding_payne_qutrit")
    point_count, _, adjacency, _ = e8_embedding.build_w33()
    adjacency_sets = [set(adjacency[index]) for index in range(point_count)]
    helper = e8_embedding.TestHeisenbergQutrit()
    _, h27_vertices, n12_triangles = helper._local_structure(0, point_count, adjacency_sets)
    fibers, vertex_to_xyz = helper._build_cube(h27_vertices, n12_triangles, adjacency_sets)

    relabel = {vertex: index for index, vertex in enumerate(h27_vertices)}
    h27_graph = [set() for _ in h27_vertices]
    for left_index, left_vertex in enumerate(h27_vertices):
        for right_index in range(left_index + 1, len(h27_vertices)):
            right_vertex = h27_vertices[right_index]
            if right_vertex in adjacency_sets[left_vertex]:
                h27_graph[left_index].add(right_index)
                h27_graph[right_index].add(left_index)

    internal_triangles = sorted(
        {
            (left, middle, right)
            for left, middle, right in combinations(range(len(h27_vertices)), 3)
            if middle in h27_graph[left]
            and right in h27_graph[left]
            and right in h27_graph[middle]
        }
    )
    relabeled_fibers = sorted(
        {tuple(sorted(relabel[vertex] for vertex in fiber)) for fiber in fibers.values()}
    )

    return {
        "h27_vertices": h27_vertices,
        "adjacency": h27_graph,
        "internal_triangles": internal_triangles,
        "fibers": relabeled_fibers,
        "vertex_to_xyz": {relabel[vertex]: xyz for vertex, xyz in vertex_to_xyz.items()},
    }


@lru_cache(maxsize=1)
def explicit_payne_to_qutrit_local_dictionary() -> dict[str, object]:
    derived_points, type1_lines, type2_lines, _, raw_graph, _ = payne_derivation(base_point=0)
    qutrit_shell = build_h27_qutrit_local_shell()
    point_mapping = canonical_graph_bijection(raw_graph, qutrit_shell["adjacency"])

    type1_images = sorted({tuple(sorted(point_mapping[index] for index in line)) for line in type1_lines})
    type2_images = sorted({tuple(sorted(point_mapping[index] for index in line)) for line in type2_lines})

    return {
        "derived_points": derived_points,
        "point_mapping": point_mapping,
        "type1_images": type1_images,
        "type2_images": type2_images,
        "qutrit_shell": qutrit_shell,
    }


def canonical_ag23_line(
    points: list[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int]]:
    unique_points = tuple(sorted(set(points)))
    assert len(unique_points) == 3

    for anchor in unique_points:
        for candidate in unique_points:
            if candidate == anchor:
                continue
            direction = ((candidate[0] - anchor[0]) % 3, (candidate[1] - anchor[1]) % 3)
            third = ((anchor[0] + 2 * direction[0]) % 3, (anchor[1] + 2 * direction[1]) % 3)
            if third in unique_points:
                reverse = ((2 * direction[0]) % 3, (2 * direction[1]) % 3)
                return unique_points, min(direction, reverse)

    raise AssertionError("points do not define an AG(2,3) line")


def ordered_ag23_line(
    points: list[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], ...], tuple[int, int]]:
    ag23_line, direction = canonical_ag23_line(points)
    anchor = min(ag23_line)
    ordered_line = tuple(
        ((anchor[0] + step * direction[0]) % 3, (anchor[1] + step * direction[1]) % 3)
        for step in F3
    )
    assert set(ordered_line) == set(ag23_line)
    return ordered_line, direction


def fit_f3_quadratic(values: tuple[int, int, int]) -> tuple[int, int, int]:
    for a, b, c in product(F3, repeat=3):
        if tuple((a * u * u + b * u + c) % 3 for u in F3) == values:
            return (a, b, c)
    raise AssertionError(f"no quadratic fit found for {values}")


def affine_palette_base_step(
    patterns: list[tuple[int, int, int]] | tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    unique_patterns = sorted(set(patterns))
    assert len(unique_patterns) == 3

    for base in unique_patterns:
        for other in unique_patterns:
            if other == base:
                continue
            step = tuple((other[index] - base[index]) % 3 for index in range(3))
            if step == (0, 0, 0):
                continue
            candidate_patterns = sorted(
                {
                    base,
                    tuple((base[index] + step[index]) % 3 for index in range(3)),
                    tuple((base[index] + 2 * step[index]) % 3 for index in range(3)),
                }
            )
            if candidate_patterns == unique_patterns:
                return base, step

    raise AssertionError(f"patterns do not form an affine F_3-line: {patterns}")


def canonical_reparameterized_phase_palette(
    patterns: list[tuple[int, int, int]] | tuple[tuple[int, int, int], ...],
) -> tuple[tuple[int, int, int], ...]:
    best = None
    for scale in (1, 2):
        for shift in F3:
            parameter_map = tuple((scale * u + shift) % 3 for u in F3)
            candidate = tuple(
                sorted(tuple(pattern[index] for index in parameter_map) for pattern in patterns)
            )
            if best is None or candidate < best:
                best = candidate
    assert best is not None
    return best


def affine_phase_gauge_trivializes_line_packets(line_packets: list[dict[str, object]]) -> bool:
    ag23_points = [(x, y) for x, y in product(F3, F3)]
    point_index = {point: index for index, point in enumerate(ag23_points)}

    for scale in (1, 2):
        for gauge in product(F3, repeat=len(ag23_points)):
            trivializes_all_packets = True
            for line_packet in line_packets:
                ordered_line = [tuple(point) for point in line_packet["ordered_ag23_line"]]
                gauge_values = [gauge[point_index[point]] for point in ordered_line]
                for pattern in line_packet["phase_patterns"]:
                    adjusted = tuple(
                        (scale * pattern[index] + gauge_values[index]) % 3
                        for index in range(3)
                    )
                    if len(set(adjusted)) != 1:
                        trivializes_all_packets = False
                        break
                if not trivializes_all_packets:
                    break
            if trivializes_all_packets:
                return True

    return False


@lru_cache(maxsize=1)
def explicit_payne_to_hesse_packet_dictionary() -> dict[str, object]:
    qutrit = explicit_payne_to_qutrit_local_dictionary()
    cubic = explicit_payne_to_cubic_local_dictionary()
    qutrit_shell = qutrit["qutrit_shell"]

    payne_to_h27 = qutrit["point_mapping"]
    h27_to_payne = {target: source for source, target in payne_to_h27.items()}
    payne_to_cubic = cubic["point_mapping"]
    cubic_label_by_line = {
        line: label for label, line in cubic["record"]["classical_labels"].items()
    }
    payne_to_cubic_label = {
        payne_point: cubic_label_by_line[cubic_line]
        for payne_point, cubic_line in payne_to_cubic.items()
    }
    h27_to_cubic_label = {
        h27_point: payne_to_cubic_label[payne_point]
        for h27_point, payne_point in h27_to_payne.items()
    }

    type1_lookup = {tuple(plane["lines"]): plane for plane in cubic["type1_planes"]}
    type2_lookup = {tuple(plane["lines"]): plane for plane in cubic["type2_planes"]}

    point_packets = []
    point_packet_by_ag23: dict[tuple[int, int], dict[str, object]] = {}
    for fiber in qutrit["type2_images"]:
        coordinates = [qutrit_shell["vertex_to_xyz"][index] for index in fiber]
        ag23_points = {(x, y) for x, y, _ in coordinates}
        assert len(ag23_points) == 1
        ag23_point = next(iter(ag23_points))

        payne_line = tuple(sorted(h27_to_payne[index] for index in fiber))
        cubic_plane_key = tuple(sorted(payne_to_cubic[index] for index in payne_line))
        cubic_tritangent = type2_lookup[cubic_plane_key]

        row = {
            "ag23_point": list(ag23_point),
            "qutrit_fiber": {
                "h27_point_indices": list(fiber),
                "h27_vertices": [qutrit_shell["h27_vertices"][index] for index in fiber],
                "heisenberg_xyz": [list(qutrit_shell["vertex_to_xyz"][index]) for index in fiber],
            },
            "payne_line": list(payne_line),
            "cubic_tritangent": cubic_tritangent,
        }
        point_packets.append(row)
        point_packet_by_ag23[ag23_point] = row

    point_packets.sort(key=lambda row: tuple(row["ag23_point"]))

    grouped_line_packets: dict[
        tuple[tuple[int, int], tuple[tuple[int, int], ...]],
        list[dict[str, object]],
    ] = {}
    for triangle in qutrit["type1_images"]:
        coordinates = [qutrit_shell["vertex_to_xyz"][index] for index in triangle]
        ag23_line, direction = canonical_ag23_line([(x, y) for x, y, _ in coordinates])
        payne_line = tuple(sorted(h27_to_payne[index] for index in triangle))
        cubic_plane_key = tuple(sorted(payne_to_cubic[index] for index in payne_line))
        cubic_tritangent = type1_lookup[cubic_plane_key]

        grouped_line_packets.setdefault((direction, ag23_line), []).append(
            {
                "qutrit_triangle": {
                    "h27_point_indices": list(triangle),
                    "h27_vertices": [qutrit_shell["h27_vertices"][index] for index in triangle],
                    "heisenberg_xyz": [list(qutrit_shell["vertex_to_xyz"][index]) for index in triangle],
                },
                "payne_line": list(payne_line),
                "cubic_tritangent": cubic_tritangent,
            }
        )

    line_packets = []
    for (direction, ag23_line), entries in sorted(grouped_line_packets.items()):
        entries.sort(key=lambda row: tuple(row["payne_line"]))
        ordered_line, _ = ordered_ag23_line(list(ag23_line))
        phase_patterns = sorted(
            tuple(
                {
                    (x, y): z
                    for x, y, z in row["qutrit_triangle"]["heisenberg_xyz"]
                }[point]
                for point in ordered_line
            )
            for row in entries
        )
        phase_affine_base, phase_affine_step = affine_palette_base_step(phase_patterns)
        cubic_label_union = sorted(
            {
                label
                for row in entries
                for label in row["cubic_tritangent"]["labels"]
            }
        )
        line_packets.append(
            {
                "ag23_line": [list(point) for point in ag23_line],
                "direction": list(direction),
                "ordered_ag23_line": [list(point) for point in ordered_line],
                "qutrit_triangles": [row["qutrit_triangle"] for row in entries],
                "phase_patterns": [list(pattern) for pattern in phase_patterns],
                "phase_affine_base": list(phase_affine_base),
                "phase_affine_step": list(phase_affine_step),
                "phase_affine_base_quadratic": list(fit_f3_quadratic(phase_affine_base)),
                "phase_affine_step_quadratic": list(fit_f3_quadratic(phase_affine_step)),
                "payne_lines": [row["payne_line"] for row in entries],
                "cubic_tritangents": [row["cubic_tritangent"] for row in entries],
                "cubic_label_union": cubic_label_union,
                "incident_point_packets": [
                    {
                        "ag23_point": list(point),
                        "cubic_tritangent": point_packet_by_ag23[point]["cubic_tritangent"],
                    }
                    for point in ag23_line
                ],
            }
        )

    phase_palette_orbits: dict[tuple[tuple[int, int, int], ...], dict[str, object]] = {}
    for line_packet in line_packets:
        palette = tuple(tuple(pattern) for pattern in line_packet["phase_patterns"])
        orbit = canonical_reparameterized_phase_palette(palette)
        orbit_row = phase_palette_orbits.setdefault(
            orbit,
            {
                "count": 0,
                "representative_patterns": [list(pattern) for pattern in orbit],
            },
        )
        orbit_row["count"] += 1

    for orbit, orbit_row in phase_palette_orbits.items():
        representative_base, representative_step = affine_palette_base_step(orbit)
        orbit_row["representative_affine_base"] = list(representative_base)
        orbit_row["representative_affine_step"] = list(representative_step)
        orbit_row["representative_affine_base_quadratic"] = list(
            fit_f3_quadratic(representative_base)
        )
        orbit_row["representative_affine_step_quadratic"] = list(
            fit_f3_quadratic(representative_step)
        )

    point_packets_per_line_packet = {
        sum(
            set(point_packet["cubic_tritangent"]["labels"]) <= set(line_packet["cubic_label_union"])
            for point_packet in point_packets
        )
        for line_packet in line_packets
    }
    line_packets_per_point_packet = {
        sum(
            set(point_packet["cubic_tritangent"]["labels"]) <= set(line_packet["cubic_label_union"])
            for line_packet in line_packets
        )
        for point_packet in point_packets
    }

    meeting_pairs = 0
    parallel_pairs = 0
    for left in range(len(line_packets)):
        left_points = {tuple(point) for point in line_packets[left]["ag23_line"]}
        left_labels = set(line_packets[left]["cubic_label_union"])
        for right in range(left + 1, len(line_packets)):
            right_points = {tuple(point) for point in line_packets[right]["ag23_line"]}
            intersection_size = len(left_labels & set(line_packets[right]["cubic_label_union"]))
            if left_points & right_points:
                meeting_pairs += 1
                assert intersection_size == 3
            else:
                parallel_pairs += 1
                assert intersection_size == 0

    ag23_points = [(x, y) for x, y in product(F3, F3)]
    ag23_lines = [tuple(tuple(point) for point in row["ag23_line"]) for row in line_packets]

    def det_ag23(matrix: tuple[tuple[int, int], tuple[int, int]]) -> int:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 3

    def all_gl23() -> list[tuple[tuple[int, int], tuple[int, int]]]:
        matrices = []
        for a, b, c, d in product(F3, repeat=4):
            matrix = ((a, b), (c, d))
            if det_ag23(matrix):
                matrices.append(matrix)
        return matrices

    def apply_ag23(
        matrix: tuple[tuple[int, int], tuple[int, int]],
        shift: tuple[int, int],
        point: tuple[int, int],
    ) -> tuple[int, int]:
        return (
            (matrix[0][0] * point[0] + matrix[0][1] * point[1] + shift[0]) % 3,
            (matrix[1][0] * point[0] + matrix[1][1] * point[1] + shift[1]) % 3,
        )

    packet_actions = set()
    projective_packet_actions = set()
    for matrix in all_gl23():
        determinant = det_ag23(matrix)
        for shift in product(F3, repeat=2):
            point_perm = tuple(
                ag23_points.index(apply_ag23(matrix, shift, point)) for point in ag23_points
            )
            line_perm = tuple(
                ag23_lines.index(tuple(sorted(apply_ag23(matrix, shift, point) for point in line)))
                for line in ag23_lines
            )
            packet_actions.add((point_perm, line_perm))
            if determinant == 1:
                projective_packet_actions.add((point_perm, line_perm))

    xyz_to_h27 = {
        qutrit_shell["vertex_to_xyz"][index]: index for index in qutrit_shell["vertex_to_xyz"]
    }
    central_shift = {}
    for x, y, z in product(F3, F3, F3):
        source = xyz_to_h27[(x, y, z)]
        target = xyz_to_h27[(x, y, (z + 1) % 3)]
        central_shift[h27_to_cubic_label[source]] = h27_to_cubic_label[target]

    central_cycles = []
    seen_labels = set()
    for label in sorted(central_shift):
        if label in seen_labels:
            continue
        cycle = []
        current = label
        while current not in seen_labels:
            seen_labels.add(current)
            cycle.append(current)
            current = central_shift[current]
        central_cycles.append(tuple(sorted(cycle)))

    point_packet_labels = sorted(
        tuple(sorted(packet["cubic_tritangent"]["labels"])) for packet in point_packets
    )

    return {
        "kind": "payne_hesse_packet_dictionary",
        "base_point_index": 0,
        "point_packets": point_packets,
        "line_packets": line_packets,
        "incidence_summary": {
            "point_packet_count": 9,
            "line_packet_count": 12,
            "point_packet_size": 3,
            "line_packet_size": 9,
            "line_packet_tritangent_count": 3,
            "line_packets_per_point_packet": sorted(line_packets_per_point_packet),
            "point_packets_per_line_packet": sorted(point_packets_per_line_packet),
            "meeting_line_packet_pairs": meeting_pairs,
            "parallel_line_packet_pairs": parallel_pairs,
        },
        "symmetry_summary": {
            "full_local_h27_order": 1296,
            "projective_local_h27_order": 648,
            "induced_hesse_packet_order": len(packet_actions),
            "induced_hessian_packet_order": len(projective_packet_actions),
            "central_kernel_order": 1296 // len(packet_actions),
            "central_kernel_cycles_equal_point_packets": sorted(central_cycles)
            == point_packet_labels,
        },
        "phase_law_summary": {
            "each_line_packet_is_affine_f3_line": True,
            "global_affine_phase_gauge_trivializable": affine_phase_gauge_trivializes_line_packets(
                line_packets
            ),
            "palette_orbit_count_up_to_line_reparameterization": len(phase_palette_orbits),
            "palette_orbit_sizes_up_to_line_reparameterization": sorted(
                orbit_row["count"] for orbit_row in phase_palette_orbits.values()
            ),
            "palette_orbits_up_to_line_reparameterization": [
                phase_palette_orbits[orbit] for orbit in sorted(phase_palette_orbits)
            ],
        },
    }


def parse_cubic_duad(label: str) -> tuple[int, int]:
    if not label.startswith("c_"):
        raise ValueError(f"not a cubic c_ij label: {label}")
    left = int(label[2])
    right = int(label[3])
    return (left, right)


@lru_cache(maxsize=1)
def build_double_six_data() -> list[dict[str, object]]:
    cds = load_module(ROOT / "tools" / "compute_double_sixes.py", "compute_double_sixes_carriers")
    roots = cds.construct_e8_roots()
    orbit = next(candidate for candidate in cds.compute_we6_orbits(roots) if len(candidate) == 27)
    gram = roots[orbit] @ roots[orbit].T
    skew = abs(gram - 1.0) < 1e-9
    meet = abs(gram) < 1e-9
    for i in range(27):
        skew[i, i] = False
        meet[i, i] = False
    k6_cliques = [tuple(sorted(clique)) for clique in cds.find_k_cliques(skew, 6)]
    double_sixes = cds.find_double_sixes(skew, k6_cliques)

    data = []
    for left, _, match in double_sixes:
        a_lines = tuple(sorted(left))
        b_lines = tuple(match[line] for line in a_lines)
        carrier = frozenset(a_lines) | frozenset(b_lines)
        remaining = sorted(set(range(27)) - set(carrier))

        classical_labels = {f"a_{index + 1}": line for index, line in enumerate(a_lines)}
        classical_labels.update({f"b_{index + 1}": line for index, line in enumerate(b_lines)})
        for vertex in remaining:
            meets = [index for index, line in enumerate(a_lines) if meet[vertex, line]]
            assert len(meets) == 2
            first, second = sorted(meets)
            classical_labels[f"c_{first + 1}{second + 1}"] = vertex

        assert len(classical_labels) == 27
        assert set(classical_labels.values()) == set(range(27))

        tritangent_mixed = []
        tritangent_c_only = []

        for first in range(1, 7):
            for second in range(1, 7):
                if first == second:
                    continue
                cij = f"c_{min(first, second)}{max(first, second)}"
                labels = [f"a_{first}", f"b_{second}", cij]
                tritangent_mixed.append(
                    {
                        "labels": labels,
                        "lines": sorted(classical_labels[label] for label in labels),
                    }
                )

        for matching in perfect_matchings_on_six():
            labels = [f"c_{first}{second}" for first, second in matching]
            tritangent_c_only.append(
                {
                    "labels": labels,
                    "lines": sorted(classical_labels[label] for label in labels),
                }
            )

        actual_triangles = {
            tuple(sorted((left_vertex, middle_vertex, right_vertex)))
            for left_vertex in range(27)
            for middle_vertex in range(left_vertex + 1, 27)
            if meet[left_vertex, middle_vertex]
            for right_vertex in range(middle_vertex + 1, 27)
            if meet[left_vertex, right_vertex] and meet[middle_vertex, right_vertex]
        }
        predicted_triangles = {
            tuple(plane["lines"])
            for plane in tritangent_mixed + tritangent_c_only
        }
        carrier_triangle_count = {
            tuple(sorted(triangle))
            for triangle in actual_triangles
            if sum(vertex in carrier for vertex in triangle) in {0, 2}
        }

        assert len(tritangent_mixed) == 30
        assert len(tritangent_c_only) == 15
        assert predicted_triangles == carrier_triangle_count

        data.append(
            {
                "a_lines": a_lines,
                "b_lines": b_lines,
                "carrier": carrier,
                "classical_labels": classical_labels,
                "tritangent_planes": {
                    "mixed_30": tritangent_mixed,
                    "c_only_15": tritangent_c_only,
                },
            }
        )
    return data


@lru_cache(maxsize=1)
def build_double_six_carriers() -> list[frozenset[int]]:
    return [record["carrier"] for record in build_double_six_data()]


@lru_cache(maxsize=1)
def explicit_thirtysix_carrier_bijection() -> tuple[
    list[frozenset[tuple[int, int, int, int, int]]],
    list[frozenset[int]],
    dict[int, int],
]:
    import networkx as nx
    from networkx.algorithms import isomorphism as iso

    sections = sorted({POLAR_SECTION_POINTS[point] for point in MINUS_TYPE_POINTS}, key=sorted)
    carriers = build_double_six_carriers()

    section_overlap_graph = overlap_graph(sections, overlap_size=1)
    carrier_overlap_graph = overlap_graph(carriers, overlap_size=6)

    left = nx.Graph()
    left.add_nodes_from(range(36))
    for vertex, neighbors in enumerate(section_overlap_graph):
        for neighbor in neighbors:
            if vertex < neighbor:
                left.add_edge(vertex, neighbor)

    right = nx.Graph()
    right.add_nodes_from(range(36))
    for vertex, neighbors in enumerate(carrier_overlap_graph):
        for neighbor in neighbors:
            if vertex < neighbor:
                right.add_edge(vertex, neighbor)

    matcher = iso.GraphMatcher(left, right)
    if not matcher.is_isomorphic():
        raise AssertionError("36-carrier overlap graphs should be isomorphic")
    return sections, carriers, dict(matcher.mapping)


def payne_derivation(base_point: int) -> tuple[
    list[int],
    list[frozenset[int]],
    list[frozenset[int]],
    list[frozenset[int]],
    list[set[int]],
    list[set[int]],
]:
    p_perp = {base_point} | POINT_GRAPH[base_point]
    derived_points = sorted(set(range(POINT_COUNT)) - p_perp)
    relabel = {point: index for index, point in enumerate(derived_points)}

    lines_through_base = [line for line in INDEX_LINES if base_point in line]
    lines_away_from_base = [line for line in INDEX_LINES if base_point not in line]

    type1_lines = [
        frozenset(relabel[point] for point in line - (line & p_perp))
        for line in lines_away_from_base
    ]

    type2_seen = set()
    type2_lines = []
    for point in derived_points:
        px_perp = POINT_GRAPH[base_point] & POINT_GRAPH[point]
        closed_common = set(range(POINT_COUNT))
        for witness in px_perp:
            closed_common &= ({witness} | POINT_GRAPH[witness])
        line = frozenset(relabel[z] for z in closed_common if z in relabel)
        if line not in type2_seen:
            type2_seen.add(line)
            type2_lines.append(line)

    derived_lines = type1_lines + type2_lines
    raw_graph = [set() for _ in derived_points]
    payne_graph = [set() for _ in derived_points]

    for i, left in enumerate(derived_points):
        for j in range(i + 1, len(derived_points)):
            right = derived_points[j]
            if right in POINT_GRAPH[left]:
                raw_graph[i].add(j)
                raw_graph[j].add(i)

    for line in derived_lines:
        for left, right in combinations(sorted(line), 2):
            payne_graph[left].add(right)
            payne_graph[right].add(left)

    return derived_points, type1_lines, type2_lines, derived_lines, raw_graph, payne_graph


def normalize_q43(
    vector: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    for entry in vector:
        if entry:
            scale = inv_mod_3(entry)
            return tuple((scale * coord) % 3 for coord in vector)
    raise ValueError("zero vector cannot be normalized")


def add_scaled_q43(
    a: int,
    left: tuple[int, int, int, int, int],
    b: int,
    right: tuple[int, int, int, int, int],
) -> tuple[int, int, int, int, int]:
    return tuple((a * x + b * y) % 3 for x, y in zip(left, right))


def q43_form(point: tuple[int, int, int, int, int]) -> int:
    x0, x1, x2, x3, x4 = point
    return (x0 * x0 + x1 * x2 + x3 * x4) % 3


def q43_polar(
    left: tuple[int, int, int, int, int],
    right: tuple[int, int, int, int, int],
) -> int:
    x0, x1, x2, x3, x4 = left
    y0, y1, y2, y3, y4 = right
    return (2 * x0 * y0 + x1 * y2 + x2 * y1 + x3 * y4 + x4 * y3) % 3


def build_projective_points_q43() -> list[tuple[int, int, int, int, int]]:
    points = {
        normalize_q43(vector)
        for vector in product(F3, repeat=5)
        if vector != ZERO5
    }
    return sorted(points)


def projective_line_q43(
    first: tuple[int, int, int, int, int],
    second: tuple[int, int, int, int, int],
) -> frozenset[tuple[int, int, int, int, int]]:
    if first == second:
        raise ValueError("need two distinct projective points")
    line = {
        normalize_q43(add_scaled_q43(a, first, b, second))
        for a, b in product(F3, repeat=2)
        if (a, b) != (0, 0)
    }
    return frozenset(line)


Q43_PROJECTIVE_POINTS = build_projective_points_q43()
Q43_POINTS = [point for point in Q43_PROJECTIVE_POINTS if q43_form(point) == 0]
Q43_OFF_POINTS = [point for point in Q43_PROJECTIVE_POINTS if q43_form(point) != 0]


def build_q43_lines() -> list[frozenset[tuple[int, int, int, int, int]]]:
    lines = {
        line
        for first, second in combinations(Q43_POINTS, 2)
        for line in [projective_line_q43(first, second)]
        if all(q43_form(point) == 0 for point in line)
    }
    return sorted(lines, key=lambda line: tuple(sorted(line)))


Q43_LINES = build_q43_lines()
POLAR_SECTION_POINTS = {
    point: frozenset(qpoint for qpoint in Q43_POINTS if q43_polar(point, qpoint) == 0)
    for point in Q43_OFF_POINTS
}
POLAR_SECTION_LINES = {
    point: [line for line in Q43_LINES if line <= POLAR_SECTION_POINTS[point]]
    for point in Q43_OFF_POINTS
}
PLUS_TYPE_POINTS = [point for point in Q43_OFF_POINTS if len(POLAR_SECTION_POINTS[point]) == 16]
MINUS_TYPE_POINTS = [point for point in Q43_OFF_POINTS if len(POLAR_SECTION_POINTS[point]) == 10]


def line_intersection_graph(
    lines: list[frozenset[tuple[int, int, int, int, int]]],
) -> list[set[int]]:
    graph = [set() for _ in lines]
    for i, left in enumerate(lines):
        for j in range(i + 1, len(lines)):
            right = lines[j]
            if left & right:
                graph[i].add(j)
                graph[j].add(i)
    return graph


def bipartition(graph: list[set[int]]) -> tuple[frozenset[int], frozenset[int]]:
    colors: dict[int, int] = {}
    for start in range(len(graph)):
        if start in colors:
            continue
        stack = [start]
        colors[start] = 0
        while stack:
            left = stack.pop()
            for right in graph[left]:
                if right in colors:
                    if colors[right] == colors[left]:
                        raise ValueError("graph is not bipartite")
                    continue
                colors[right] = 1 - colors[left]
                stack.append(right)
    return (
        frozenset(vertex for vertex, color in colors.items() if color == 0),
        frozenset(vertex for vertex, color in colors.items() if color == 1),
    )


class Test_burkhardt_1_Order3Subgroups:
    def test_projective_point_count(self):
        assert len(PROJECTIVE_POINTS) == POINT_COUNT

    def test_cyclic_order_3_subgroup_count(self):
        subgroups = {cyclic_order_3_subgroup(point) for point in PROJECTIVE_POINTS}
        assert len(subgroups) == POINT_COUNT

    def test_each_point_is_a_cyclic_order_3_subgroup(self):
        for subgroup in map(cyclic_order_3_subgroup, PROJECTIVE_POINTS):
            assert len(subgroup) == 3
            assert ZERO4 in subgroup


class Test_burkhardt_2_SteinerPrimes:
    def test_steiner_prime_count(self):
        assert len(ISOTROPIC_LINES) == LINE_COUNT

    def test_each_steiner_prime_has_four_jplanes(self):
        assert {len(line) for line in ISOTROPIC_LINES} == {LINE_SIZE}

    def test_each_jplane_lies_in_four_steiner_primes(self):
        assert {len(lines) for lines in LINES_THROUGH_POINT.values()} == {LINES_PER_POINT}

    def test_incidence_is_symmetric_40_by_40(self):
        flags = sum(len(lines) for lines in LINES_THROUGH_POINT.values())
        assert flags == POINT_COUNT * LINES_PER_POINT == LINE_COUNT * LINE_SIZE == 160


class Test_burkhardt_3_TrivialPairing:
    def test_common_steiner_prime_equals_trivial_pairing(self):
        for first, second in combinations(PROJECTIVE_POINTS, 2):
            shares_steiner_prime = any(
                first in line and second in line for line in LINES_THROUGH_POINT[first]
            )
            assert shares_steiner_prime == (omega(first, second) == 0)

    def test_local_27_shell(self):
        for point in PROJECTIVE_POINTS:
            orthogonal = sum(omega(point, other) == 0 for other in PROJECTIVE_POINTS if other != point)
            nonorthogonal = sum(omega(point, other) != 0 for other in PROJECTIVE_POINTS if other != point)
            assert orthogonal == POINT_DEGREE
            assert nonorthogonal == 27


class Test_burkhardt_4_GQ33Realization:
    def test_point_graph_degree(self):
        assert {len(neighbors) for neighbors in POINT_GRAPH} == {POINT_DEGREE}

    def test_point_graph_srg_parameters(self):
        patterns = {
            (int(right in POINT_GRAPH[left]), common_neighbor_count(POINT_GRAPH, left, right))
            for left in range(POINT_COUNT)
            for right in range(left + 1, POINT_COUNT)
        }
        assert patterns == {(1, LAMBDA), (0, MU)}

    def test_line_graph_matches_same_srg(self):
        patterns = {
            (int(right in LINE_GRAPH[left]), common_neighbor_count(LINE_GRAPH, left, right))
            for left in range(LINE_COUNT)
            for right in range(left + 1, LINE_COUNT)
        }
        assert {len(neighbors) for neighbors in LINE_GRAPH} == {POINT_DEGREE}
        assert patterns == {(1, LAMBDA), (0, MU)}

    def test_gq_axiom_unique_line_through_collinear_pair(self):
        for first, second in combinations(PROJECTIVE_POINTS, 2):
            multiplicity = sum(first in line and second in line for line in ISOTROPIC_LINES)
            if omega(first, second) == 0:
                assert multiplicity == 1
            else:
                assert multiplicity == 0


class Test_burkhardt_Closure:
    def test_burkhardt_dictionary(self):
        summary = {
            "jplanes": len(PROJECTIVE_POINTS),
            "steiner_primes": len(ISOTROPIC_LINES),
            "jplanes_per_steiner_prime": len(next(iter(ISOTROPIC_LINES))),
            "steiner_primes_per_jplane": len(LINES_THROUGH_POINT[PROJECTIVE_POINTS[0]]),
        }
        assert summary == {
            "jplanes": 40,
            "steiner_primes": 40,
            "jplanes_per_steiner_prime": 4,
            "steiner_primes_per_jplane": 4,
        }

    def test_moduli_realization(self):
        # Burkhardt j-planes / Steiner primes realize the symmetric GQ(3,3).
        assert len(PROJECTIVE_POINTS) == len(ISOTROPIC_LINES) == 40
        assert {len(neighbors) for neighbors in POINT_GRAPH} == {12}
        assert {len(neighbors) for neighbors in LINE_GRAPH} == {12}


class Test_burkhardt_5_FixedJplanePayneDerivation:
    def test_fixed_jplane_has_27_point_shell(self):
        derived_points, _, _, _, raw_graph, _ = payne_derivation(base_point=0)
        assert len(derived_points) == 27
        assert {len(neighbors) for neighbors in raw_graph} == {8}

    def test_payne_derivation_has_36_plus_9_lines(self):
        _, type1_lines, type2_lines, derived_lines, _, _ = payne_derivation(base_point=0)
        assert len(type1_lines) == 36
        assert len(type2_lines) == 9
        assert len(derived_lines) == 45
        assert {len(line) for line in derived_lines} == {3}

    def test_payne_incidence_counts(self):
        derived_points, _, _, derived_lines, _, _ = payne_derivation(base_point=0)
        incidences = [sum(index in line for line in derived_lines) for index in range(len(derived_points))]
        assert set(incidences) == {5}
        assert len(derived_points) * 5 == len(derived_lines) * 3 == 135

    def test_payne_graph_is_gq24_collinearity(self):
        _, _, _, _, _, payne_graph = payne_derivation(base_point=0)
        patterns = {
            (int(right in payne_graph[left]), common_neighbor_count(payne_graph, left, right))
            for left in range(27)
            for right in range(left + 1, 27)
        }
        assert {len(neighbors) for neighbors in payne_graph} == {10}
        assert patterns == {(1, 1), (0, 5)}

    def test_payne_complement_is_schlafli(self):
        _, _, _, _, _, payne_graph = payne_derivation(base_point=0)
        complement_graph = [
            {other for other in range(27) if other != vertex and other not in payne_graph[vertex]}
            for vertex in range(27)
        ]
        patterns = {
            (int(right in complement_graph[left]), common_neighbor_count(complement_graph, left, right))
            for left in range(27)
            for right in range(left + 1, 27)
        }
        assert {len(neighbors) for neighbors in complement_graph} == {16}
        assert patterns == {(1, 10), (0, 8)}

    def test_payne_structure_is_basepoint_independent(self):
        for base_point in range(POINT_COUNT):
            derived_points, _, _, derived_lines, raw_graph, payne_graph = payne_derivation(base_point)
            assert len(derived_points) == 27
            assert len(derived_lines) == 45
            assert {len(neighbors) for neighbors in raw_graph} == {8}
            assert {len(neighbors) for neighbors in payne_graph} == {10}


class Test_burkhardt_6_NodeHyperbolicSections:
    def test_q43_side_has_expected_counts(self):
        assert len(Q43_PROJECTIVE_POINTS) == 121
        assert len(Q43_POINTS) == 40
        assert len(Q43_OFF_POINTS) == 81
        assert len(Q43_LINES) == 40

    def test_off_quadric_points_split_as_45_plus_and_36_minus(self):
        point_section_sizes = sorted(len(POLAR_SECTION_POINTS[point]) for point in Q43_OFF_POINTS)
        line_section_sizes = sorted(len(POLAR_SECTION_LINES[point]) for point in Q43_OFF_POINTS)
        assert len(PLUS_TYPE_POINTS) == 45
        assert len(MINUS_TYPE_POINTS) == 36
        assert point_section_sizes == [10] * 36 + [16] * 45
        assert line_section_sizes == [0] * 36 + [8] * 45

    def test_plus_type_sections_are_hyperbolic_8_line_configs(self):
        for point in PLUS_TYPE_POINTS:
            section_points = POLAR_SECTION_POINTS[point]
            section_lines = POLAR_SECTION_LINES[point]
            incidences = [sum(qpoint in line for line in section_lines) for qpoint in section_points]
            intersection_graph = line_intersection_graph(section_lines)
            left_regulus, right_regulus = bipartition(intersection_graph)

            assert len(section_points) == 16
            assert len(section_lines) == 8
            assert set(incidences) == {2}
            assert {len(neighbors) for neighbors in intersection_graph} == {4}
            assert len(left_regulus) == len(right_regulus) == 4

            for left, right in combinations(left_regulus, 2):
                assert not (section_lines[left] & section_lines[right])
            for left, right in combinations(right_regulus, 2):
                assert not (section_lines[left] & section_lines[right])
            for left in left_regulus:
                for right in right_regulus:
                    assert len(section_lines[left] & section_lines[right]) == 1

    def test_minus_type_sections_have_no_quadric_generators(self):
        for point in MINUS_TYPE_POINTS:
            assert len(POLAR_SECTION_POINTS[point]) == 10
            assert POLAR_SECTION_LINES[point] == []

    def test_minus_type_sections_are_ovoids_of_q43(self):
        for point in MINUS_TYPE_POINTS:
            section = POLAR_SECTION_POINTS[point]
            line_hits = [sum(qpoint in line for qpoint in section) for line in Q43_LINES]
            assert len(section) == 10
            assert set(line_hits) == {1}
            assert sum(line_hits) == len(Q43_LINES) == 40

    def test_minus_type_sections_give_36_distinct_dual_spreads(self):
        dual_spreads = {POLAR_SECTION_POINTS[point] for point in MINUS_TYPE_POINTS}
        assert len(dual_spreads) == 36
        assert all(len(spread) == 10 for spread in dual_spreads)

    def test_each_q43_line_lies_in_nine_plus_sections(self):
        plus_incidence_counts = [
            sum(line in POLAR_SECTION_LINES[point] for point in PLUS_TYPE_POINTS)
            for line in Q43_LINES
        ]
        assert set(plus_incidence_counts) == {9}
        assert len(PLUS_TYPE_POINTS) * 8 == len(Q43_LINES) * 9 == 360


class Test_burkhardt_7_ThirtySixCarrierBridge:
    def test_minus_type_sections_have_spread_overlap_packet(self):
        sections = sorted({POLAR_SECTION_POINTS[point] for point in MINUS_TYPE_POINTS}, key=sorted)
        overlap_counts = {
            len(sections[left] & sections[right])
            for left in range(36)
            for right in range(left + 1, 36)
        }
        overlap_1 = overlap_graph(sections, overlap_size=1)
        overlap_4 = overlap_graph(sections, overlap_size=4)

        assert overlap_counts == {1, 4}
        assert {len(neighbors) for neighbors in overlap_1} == {20}
        assert {len(neighbors) for neighbors in overlap_4} == {15}
        assert graph_patterns(overlap_1) == {(1, 10), (0, 12)}
        assert graph_patterns(overlap_4) == {(1, 6), (0, 6)}

    def test_double_sixes_have_same_overlap_packet(self):
        carriers = build_double_six_carriers()

        overlap_counts = {
            len(carriers[left] & carriers[right])
            for left in range(36)
            for right in range(left + 1, 36)
        }
        overlap_6 = overlap_graph(carriers, overlap_size=6)
        overlap_4 = overlap_graph(carriers, overlap_size=4)

        assert len(carriers) == 36
        assert len(set(carriers)) == 36
        assert overlap_counts == {4, 6}
        assert {len(neighbors) for neighbors in overlap_6} == {20}
        assert {len(neighbors) for neighbors in overlap_4} == {15}
        assert graph_patterns(overlap_6) == {(1, 10), (0, 12)}
        assert graph_patterns(overlap_4) == {(1, 6), (0, 6)}

    def test_thirtysix_carriers_share_same_srg_signature(self):
        sections = sorted({POLAR_SECTION_POINTS[point] for point in MINUS_TYPE_POINTS}, key=sorted)
        section_overlap_1 = overlap_graph(sections, overlap_size=1)

        carriers = build_double_six_carriers()
        doublesix_overlap_6 = overlap_graph(carriers, overlap_size=6)

        assert graph_patterns(section_overlap_1) == graph_patterns(doublesix_overlap_6)
        assert {len(neighbors) for neighbors in section_overlap_1} == {len(neighbors) for neighbors in doublesix_overlap_6} == {20}

    def test_explicit_bijection_between_thirtysix_carriers_exists(self):
        sections, carriers, mapping = explicit_thirtysix_carrier_bijection()
        assert len(sections) == len(carriers) == len(mapping) == 36
        assert set(mapping) == set(range(36))
        assert set(mapping.values()) == set(range(36))

    def test_explicit_bijection_carries_both_overlap_relations(self):
        sections, carriers, mapping = explicit_thirtysix_carrier_bijection()
        for left in range(36):
            for right in range(left + 1, 36):
                section_overlap = len(sections[left] & sections[right])
                carrier_overlap = len(carriers[mapping[left]] & carriers[mapping[right]])
                assert (section_overlap, carrier_overlap) in {(1, 6), (4, 4)}

    def test_committed_bijection_artifact_is_valid(self):
        sections = sorted({POLAR_SECTION_POINTS[point] for point in MINUS_TYPE_POINTS}, key=sorted)
        carriers = build_double_six_carriers()
        double_six_data = build_double_six_data()

        payload = json.loads(THIRTYSIX_CARRIER_BIJECTION_ARTIFACT.read_text(encoding="utf-8"))
        rows = payload["rows"]
        assert payload["elliptic_section_count"] == 36
        assert payload["double_six_carrier_count"] == 36
        assert payload["elliptic_section_overlap_sizes"] == [1, 4]
        assert payload["double_six_carrier_overlap_sizes"] == [4, 6]
        assert len(rows) == 36

        seen_sections = set()
        seen_carriers = set()
        artifact_sections = []
        artifact_carriers = []

        for row in rows:
            assert row["elliptic_section_index"] in range(36)
            assert row["double_six_carrier_index"] in range(36)

            section = frozenset(tuple(point) for point in row["elliptic_section_points"])
            carrier = frozenset(row["double_six_lines"])
            double_six = double_six_data[row["double_six_carrier_index"]]

            assert len(section) == 10
            assert len(carrier) == 12
            assert section == sections[row["elliptic_section_index"]]
            assert carrier == carriers[row["double_six_carrier_index"]]
            assert row["double_six_a_lines"] == list(double_six["a_lines"])
            assert row["double_six_b_lines"] == list(double_six["b_lines"])
            assert row["classical_cubic_labels"] == double_six["classical_labels"]
            assert sorted(row["double_six_a_lines"] + row["double_six_b_lines"]) == row["double_six_lines"]
            assert row["tritangent_planes"] == double_six["tritangent_planes"]
            assert len(row["tritangent_planes"]["mixed_30"]) == 30
            assert len(row["tritangent_planes"]["c_only_15"]) == 15
            mixed_line_sets = {
                tuple(plane["lines"]) for plane in row["tritangent_planes"]["mixed_30"]
            }
            c_only_line_sets = {
                tuple(plane["lines"]) for plane in row["tritangent_planes"]["c_only_15"]
            }
            assert len(mixed_line_sets) == 30
            assert len(c_only_line_sets) == 15
            assert mixed_line_sets.isdisjoint(c_only_line_sets)

            seen_sections.add(row["elliptic_section_index"])
            seen_carriers.add(row["double_six_carrier_index"])
            artifact_sections.append(section)
            artifact_carriers.append(carrier)

        assert seen_sections == set(range(36))
        assert seen_carriers == set(range(36))

        for left in range(36):
            for right in range(left + 1, 36):
                section_overlap = len(artifact_sections[left] & artifact_sections[right])
                carrier_overlap = len(artifact_carriers[left] & artifact_carriers[right])
                assert (section_overlap, carrier_overlap) in {(1, 6), (4, 4)}


class Test_burkhardt_8_PayneCubicLocalDictionary:
    def test_payne_local_model_maps_to_cubic_27_line_model(self):
        witness = explicit_payne_to_cubic_local_dictionary()
        mapping = witness["point_mapping"]
        assert len(mapping) == 27
        assert set(mapping) == set(range(27))
        assert set(mapping.values()) == set(range(27))

    def test_payne_36_plus_9_lines_push_to_cubic_36_plus_9_packet(self):
        witness = explicit_payne_to_cubic_local_dictionary()
        type1_images = set(witness["type1_images"])
        type2_images = set(witness["type2_images"])
        mixed_30 = witness["mixed_30"]
        c_only_15 = witness["c_only_15"]

        assert len(type1_images) == 36
        assert len(type2_images) == 9
        assert type1_images.isdisjoint(type2_images)
        assert len(type1_images | type2_images) == 45
        assert sum(triangle in mixed_30 for triangle in type1_images) == 24
        assert sum(triangle in c_only_15 for triangle in type1_images) == 12
        assert sum(triangle in mixed_30 for triangle in type2_images) == 6
        assert sum(triangle in c_only_15 for triangle in type2_images) == 3

    def test_payne_hyperbolic_nine_packet_has_two_triangles_and_three_matchings(self):
        witness = explicit_payne_to_cubic_local_dictionary()
        type2_planes = witness["type2_planes"]

        mixed_planes = [
            plane
            for plane in type2_planes
            if sum(label.startswith("c_") for label in plane["labels"]) == 1
        ]
        c_only_planes = [
            plane
            for plane in type2_planes
            if all(label.startswith("c_") for label in plane["labels"])
        ]

        assert len(mixed_planes) == 6
        assert len(c_only_planes) == 3

        mixed_edges = set()
        for plane in mixed_planes:
            a_label = next(label for label in plane["labels"] if label.startswith("a_"))
            b_label = next(label for label in plane["labels"] if label.startswith("b_"))
            mixed_edges.add(tuple(sorted((int(a_label[2:]), int(b_label[2:])))))

        local_graph = {vertex: set() for vertex in range(1, 7)}
        for left, right in mixed_edges:
            local_graph[left].add(right)
            local_graph[right].add(left)

        assert {len(neighbors) for neighbors in local_graph.values()} == {2}

        components = []
        seen = set()
        for start in range(1, 7):
            if start in seen:
                continue
            stack = [start]
            component = set()
            seen.add(start)
            while stack:
                vertex = stack.pop()
                component.add(vertex)
                for neighbor in local_graph[vertex]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            components.append(component)

        assert sorted(sorted(component) for component in components) == [[1, 2, 6], [3, 4, 5]]
        left_component, right_component = components

        c_only_edges = [sorted(parse_cubic_duad(label) for label in plane["labels"]) for plane in c_only_planes]
        for matching in c_only_edges:
            touched = set()
            for left, right in matching:
                assert (left in left_component and right in right_component) or (
                    left in right_component and right in left_component
                )
                touched.update([left, right])
            assert touched == set(range(1, 7))

    def test_committed_payne_cubic_artifact_is_valid(self):
        witness = explicit_payne_to_cubic_local_dictionary()
        payload = json.loads(PAYNE_CUBIC_LOCAL_DICTIONARY_ARTIFACT.read_text(encoding="utf-8"))

        assert payload["kind"] == "payne_cubic_local_dictionary"
        assert payload["base_point_index"] == 0
        assert payload["reference_double_six_index"] == 0
        assert len(payload["point_mapping_rows"]) == 27
        assert payload["split_summary"] == {
            "type1_total": 36,
            "type2_total": 9,
            "type1_mixed": 24,
            "type1_c_only": 12,
            "type2_mixed": 6,
            "type2_c_only": 3,
        }

        point_mapping_rows = payload["point_mapping_rows"]
        expected_inverse = {
            line: label for label, line in witness["record"]["classical_labels"].items()
        }
        assert {
            row["payne_point_index"]: row["cubic_line_index"] for row in point_mapping_rows
        } == witness["point_mapping"]
        for row in point_mapping_rows:
            assert row["cubic_label"] == expected_inverse[row["cubic_line_index"]]

        assert payload["type1_tritangents"] == witness["type1_planes"]
        assert payload["type2_tritangents"] == witness["type2_planes"]
        assert payload["hyperbolic_nine_shape"] == {
            "mixed_index_triangles": [[1, 2, 6], [3, 4, 5]],
            "c_only_matchings": [
                [[1, 4], [2, 3], [5, 6]],
                [[1, 3], [2, 5], [4, 6]],
                [[1, 5], [2, 4], [3, 6]],
            ],
        }


class Test_burkhardt_9_PayneQutritLocalDictionary:
    def test_payne_local_model_maps_to_h27_qutrit_shell(self):
        witness = explicit_payne_to_qutrit_local_dictionary()
        mapping = witness["point_mapping"]
        assert len(mapping) == 27
        assert set(mapping) == set(range(27))
        assert set(mapping.values()) == set(range(27))

    def test_payne_ordinary_thirtysix_equal_h27_internal_triangles(self):
        witness = explicit_payne_to_qutrit_local_dictionary()
        qutrit_shell = witness["qutrit_shell"]
        assert witness["type1_images"] == qutrit_shell["internal_triangles"]

    def test_payne_hyperbolic_nine_equal_h27_fibers(self):
        witness = explicit_payne_to_qutrit_local_dictionary()
        qutrit_shell = witness["qutrit_shell"]
        assert witness["type2_images"] == qutrit_shell["fibers"]

    def test_committed_payne_qutrit_artifact_is_valid(self):
        witness = explicit_payne_to_qutrit_local_dictionary()
        qutrit_shell = witness["qutrit_shell"]
        payload = json.loads(PAYNE_QUTRIT_LOCAL_DICTIONARY_ARTIFACT.read_text(encoding="utf-8"))

        assert payload["kind"] == "payne_qutrit_local_dictionary"
        assert payload["base_point_index"] == 0
        assert len(payload["point_mapping_rows"]) == 27
        assert len(payload["ordinary_36_triangles"]) == 36
        assert len(payload["hyperbolic_9_fibers"]) == 9

        mapping_rows = payload["point_mapping_rows"]
        assert {
            row["payne_point_index"]: row["h27_point_index"] for row in mapping_rows
        } == witness["point_mapping"]
        for row in mapping_rows:
            point_index = row["h27_point_index"]
            assert row["h27_vertex"] == qutrit_shell["h27_vertices"][point_index]
            assert row["heisenberg_xyz"] == list(qutrit_shell["vertex_to_xyz"][point_index])

        assert [triangle["indices"] for triangle in payload["ordinary_36_triangles"]] == [
            list(triangle) for triangle in witness["type1_images"]
        ]
        assert [fiber["indices"] for fiber in payload["hyperbolic_9_fibers"]] == [
            list(fiber) for fiber in witness["type2_images"]
        ]


class Test_burkhardt_10_PayneHessePacketDictionary:
    def test_payne_local_packet_has_hesse_point_line_signature(self):
        payload = explicit_payne_to_hesse_packet_dictionary()

        assert payload["kind"] == "payne_hesse_packet_dictionary"
        assert payload["base_point_index"] == 0
        assert len(payload["point_packets"]) == 9
        assert len(payload["line_packets"]) == 12
        assert payload["incidence_summary"] == {
            "point_packet_count": 9,
            "line_packet_count": 12,
            "point_packet_size": 3,
            "line_packet_size": 9,
            "line_packet_tritangent_count": 3,
            "line_packets_per_point_packet": [4],
            "point_packets_per_line_packet": [3],
            "meeting_line_packet_pairs": 54,
            "parallel_line_packet_pairs": 12,
        }
        assert payload["symmetry_summary"] == {
            "full_local_h27_order": 1296,
            "projective_local_h27_order": 648,
            "induced_hesse_packet_order": 432,
            "induced_hessian_packet_order": 216,
            "central_kernel_order": 3,
            "central_kernel_cycles_equal_point_packets": True,
        }
        assert payload["phase_law_summary"] == {
            "each_line_packet_is_affine_f3_line": True,
            "global_affine_phase_gauge_trivializable": False,
            "palette_orbit_count_up_to_line_reparameterization": 3,
            "palette_orbit_sizes_up_to_line_reparameterization": [2, 4, 6],
            "palette_orbits_up_to_line_reparameterization": [
                {
                    "count": 4,
                    "representative_patterns": [[0, 0, 0], [1, 1, 2], [2, 2, 1]],
                    "representative_affine_base": [0, 0, 0],
                    "representative_affine_step": [1, 1, 2],
                    "representative_affine_base_quadratic": [0, 0, 0],
                    "representative_affine_step_quadratic": [2, 1, 1],
                },
                {
                    "count": 6,
                    "representative_patterns": [[0, 1, 1], [1, 0, 2], [2, 2, 0]],
                    "representative_affine_base": [0, 1, 1],
                    "representative_affine_step": [1, 2, 1],
                    "representative_affine_base_quadratic": [1, 0, 0],
                    "representative_affine_step_quadratic": [2, 2, 1],
                },
                {
                    "count": 2,
                    "representative_patterns": [[0, 1, 2], [1, 2, 0], [2, 0, 1]],
                    "representative_affine_base": [0, 1, 2],
                    "representative_affine_step": [1, 1, 1],
                    "representative_affine_base_quadratic": [0, 1, 0],
                    "representative_affine_step_quadratic": [0, 0, 1],
                },
            ],
        }

    def test_hesse_line_packets_carry_affine_phase_laws(self):
        payload = explicit_payne_to_hesse_packet_dictionary()

        for line_packet in payload["line_packets"]:
            patterns = [tuple(pattern) for pattern in line_packet["phase_patterns"]]
            base = tuple(line_packet["phase_affine_base"])
            step = tuple(line_packet["phase_affine_step"])

            assert sorted(patterns) == sorted(
                {
                    base,
                    tuple((base[index] + step[index]) % 3 for index in range(3)),
                    tuple((base[index] + 2 * step[index]) % 3 for index in range(3)),
                }
            )

    def test_hesse_line_packet_intersections_recover_hyperbolic_point_packets(self):
        payload = explicit_payne_to_hesse_packet_dictionary()
        point_packets = {
            tuple(packet["ag23_point"]): tuple(sorted(packet["cubic_tritangent"]["labels"]))
            for packet in payload["point_packets"]
        }

        meeting_pairs = 0
        parallel_pairs = 0
        for left in range(len(payload["line_packets"])):
            left_line = payload["line_packets"][left]
            left_points = {tuple(point) for point in left_line["ag23_line"]}
            left_labels = set(left_line["cubic_label_union"])
            for right in range(left + 1, len(payload["line_packets"])):
                right_line = payload["line_packets"][right]
                right_points = {tuple(point) for point in right_line["ag23_line"]}
                intersection = tuple(sorted(left_labels & set(right_line["cubic_label_union"])))
                common_points = left_points & right_points
                if common_points:
                    meeting_pairs += 1
                    common_point = next(iter(common_points))
                    assert intersection == point_packets[common_point]
                else:
                    parallel_pairs += 1
                    assert intersection == ()

        assert meeting_pairs == 54
        assert parallel_pairs == 12

    def test_committed_payne_hesse_packet_artifact_is_valid(self):
        payload = json.loads(PAYNE_HESSE_PACKET_DICTIONARY_ARTIFACT.read_text(encoding="utf-8"))
        assert payload == explicit_payne_to_hesse_packet_dictionary()