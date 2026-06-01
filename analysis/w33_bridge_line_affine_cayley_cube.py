"""Part MMCCCLXXI: bridge-line affine Cayley cube.

MMCCCLXX decomposes the 108 unique golden-selector failures as four 27-failure
blocks.  This verifier identifies the shared 27-object bridge carrier.

Fix the anchor line used by the draft golden selector.  A bridge line is any
W(3,3) line disjoint from that anchor line.  For each of the four anchor
points, the generalized-quadrangle axiom gives a unique off-anchor line through
that point meeting the bridge line.  Therefore every bridge line has a natural
four-symbol word in F3^4.

The 27 bridge words are exactly the 3-dimensional affine subspace

    x0 + x1 + 2*x2 + x3 = 0  over F3.

Their intersection graph is the corrected 8-regular affine Cayley cube from
Part CDIV: Cay(F3^3, {+/-e1, +/-e2, +/-e3, +/-(1,1,1)}), up to an explicit
GL(3,3) coordinate change.  Hence the bridge carrier has spectrum
{8^1, 2^12, -1^8, -4^6}.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_golden_selector_z20_cochain_lift import load_selector_data  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MMCCCLXXI_BRIDGE_LINE_AFFINE_CAYLEY_CUBE_results.json"

Q = 3

Vector3 = tuple[int, int, int]
Vector4 = tuple[int, int, int, int]
Matrix3 = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def point_line_maps(lines: list[tuple[int, ...]]) -> tuple[list[set[int]], dict[int, list[int]]]:
    line_points = [set(line) for line in lines]
    point_to_lines: dict[int, list[int]] = defaultdict(list)
    for line_index, line in enumerate(lines):
        for point in line:
            point_to_lines[point].append(line_index)
    return line_points, {point: sorted(indices) for point, indices in point_to_lines.items()}


def anchor_geometry(anchor_line: int = 0) -> dict[str, Any]:
    lines, _sigma = load_selector_data()
    line_points, point_to_lines = point_line_maps(lines)
    anchor_points = tuple(lines[anchor_line])
    endpoint_lines = {
        point: sorted(line for line in point_to_lines[point] if line != anchor_line)
        for point in anchor_points
    }
    through_anchor = {anchor_line}
    for point in anchor_points:
        through_anchor.update(endpoint_lines[point])
    bridge_lines = sorted(set(range(len(lines))) - through_anchor)
    return {
        "lines": lines,
        "line_points": line_points,
        "anchor_line": anchor_line,
        "anchor_points": anchor_points,
        "endpoint_lines": endpoint_lines,
        "through_anchor": sorted(through_anchor),
        "bridge_lines": bridge_lines,
    }


def bridge_words(geometry: dict[str, Any]) -> dict[int, Vector4]:
    line_points: list[set[int]] = geometry["line_points"]
    anchor_points: tuple[int, ...] = geometry["anchor_points"]
    endpoint_lines: dict[int, list[int]] = geometry["endpoint_lines"]
    bridge_lines: list[int] = geometry["bridge_lines"]

    words: dict[int, Vector4] = {}
    for bridge_line in bridge_lines:
        word = []
        for anchor_point in anchor_points:
            choices = [
                local_index
                for local_index, endpoint_line in enumerate(endpoint_lines[anchor_point])
                if line_points[endpoint_line] & line_points[bridge_line]
            ]
            if len(choices) != 1:
                raise AssertionError(f"bridge {bridge_line} has choices {choices} at point {anchor_point}")
            word.append(choices[0])
        words[bridge_line] = tuple(word)  # type: ignore[assignment]
    return words


def relation_value(word: Vector4) -> int:
    return (word[0] + word[1] + 2 * word[2] + word[3]) % Q


def standard_generators() -> set[Vector3]:
    base = {(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)}
    return base | {tuple((-entry) % Q for entry in vector) for vector in base}


def bridge_intersection_generators(geometry: dict[str, Any], words: dict[int, Vector4]) -> set[Vector3]:
    line_points: list[set[int]] = geometry["line_points"]
    bridge_lines: list[int] = geometry["bridge_lines"]
    generators: set[Vector3] = set()
    for left, right in combinations(bridge_lines, 2):
        if not (line_points[left] & line_points[right]):
            continue
        diff = tuple((words[right][index] - words[left][index]) % Q for index in range(3))
        generators.add(diff)  # type: ignore[arg-type]
        generators.add(tuple((-entry) % Q for entry in diff))  # type: ignore[arg-type]
    return generators


def det3(matrix: Matrix3) -> int:
    (a, b, c), (d, e, f), (g, h, i) = matrix
    return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % Q


def mat_vec(matrix: Matrix3, vector: Vector3) -> Vector3:
    return tuple(sum(matrix[row][column] * vector[column] for column in range(3)) % Q for row in range(3))  # type: ignore[return-value]


def gl3_matrices() -> list[Matrix3]:
    matrices: list[Matrix3] = []
    for entries in product(range(Q), repeat=9):
        matrix = (entries[0:3], entries[3:6], entries[6:9])  # type: ignore[assignment]
        if det3(matrix) != 0:
            matrices.append(matrix)
    return matrices


def find_standardizing_matrix(generators: set[Vector3]) -> Matrix3 | None:
    target = standard_generators()
    for matrix in gl3_matrices():
        if {mat_vec(matrix, vector) for vector in generators} == target:
            return matrix
    return None


def cayley_adjacency(coords: list[Vector3], generators: set[Vector3]) -> list[set[int]]:
    index = {coord: idx for idx, coord in enumerate(coords)}
    adjacency = [set() for _ in coords]
    for idx, coord in enumerate(coords):
        for generator in generators:
            target = tuple((coord[i] + generator[i]) % Q for i in range(3))
            adjacency[idx].add(index[target])
    return adjacency


def bridge_adjacency(geometry: dict[str, Any], words: dict[int, Vector4]) -> list[set[int]]:
    line_points: list[set[int]] = geometry["line_points"]
    bridge_lines: list[int] = geometry["bridge_lines"]
    bridge_index = {line: idx for idx, line in enumerate(bridge_lines)}
    adjacency = [set() for _line in bridge_lines]
    for left, right in combinations(bridge_lines, 2):
        if line_points[left] & line_points[right]:
            left_index = bridge_index[left]
            right_index = bridge_index[right]
            adjacency[left_index].add(right_index)
            adjacency[right_index].add(left_index)
    return adjacency


def character_spectrum(generators: set[Vector3]) -> dict[str, int]:
    spectrum: Counter[int] = Counter()
    for character in product(range(Q), repeat=3):
        counts = Counter(sum(character[index] * generator[index] for index in range(3)) % Q for generator in generators)
        # omega + omega^2 = -1, and the symmetric generator set makes counts[1] == counts[2].
        eigenvalue = counts[0] - counts[1]
        spectrum[int(eigenvalue)] += 1
    return {str(value): int(count) for value, count in sorted(spectrum.items())}


def common_neighbor_profiles(adjacency: list[set[int]]) -> dict[str, dict[str, int]]:
    adjacent: Counter[int] = Counter()
    nonadjacent: Counter[int] = Counter()
    for left, right in combinations(range(len(adjacency)), 2):
        common = len(adjacency[left] & adjacency[right])
        if right in adjacency[left]:
            adjacent[common] += 1
        else:
            nonadjacent[common] += 1
    return {
        "adjacent": counter_to_json(adjacent),
        "nonadjacent": counter_to_json(nonadjacent),
    }


def bridge_line_affine_cayley_cube_packet() -> dict[str, Any]:
    geometry = anchor_geometry(0)
    words = bridge_words(geometry)
    word_set = set(words.values())
    coords = [words[line][:3] for line in geometry["bridge_lines"]]
    coord_set = set(coords)
    generators = bridge_intersection_generators(geometry, words)
    standardizing_matrix = find_standardizing_matrix(generators)
    bridge_graph = bridge_adjacency(geometry, words)
    cayley_graph = cayley_adjacency(coords, generators)

    projection_profiles = {}
    for omitted in range(4):
        projection_counts = Counter(
            tuple(word[index] for index in range(4) if index != omitted)
            for word in word_set
        )
        projection_profiles[f"omit_{omitted}"] = counter_to_json(Counter(projection_counts.values()))

    generator_images = (
        sorted(mat_vec(standardizing_matrix, vector) for vector in generators)
        if standardizing_matrix is not None
        else []
    )

    checks = {
        "bridge_line_count_is_27": len(geometry["bridge_lines"]) == Q**3,
        "bridge_words_are_unique": len(word_set) == Q**3,
        "bridge_words_satisfy_linear_relation": Counter(relation_value(word) for word in word_set) == {0: Q**3},
        "every_three_coordinate_projection_is_bijection": all(profile == {"1": Q**3} for profile in projection_profiles.values()),
        "first_three_coordinates_are_f3_cubical": coord_set == set(product(range(Q), repeat=3)),
        "intersection_graph_is_8_regular": Counter(len(neighbors) for neighbors in bridge_graph) == {8: Q**3},
        "intersection_graph_has_108_edges": sum(len(neighbors) for neighbors in bridge_graph) // 2 == 108,
        "intersection_generators_have_size_8": len(generators) == 8,
        "cayley_graph_matches_bridge_graph": sorted(sorted(neighbors) for neighbors in bridge_graph)
        == sorted(sorted(neighbors) for neighbors in cayley_graph),
        "generators_gl3_equivalent_to_cdiv_standard": standardizing_matrix is not None
        and set(generator_images) == standard_generators(),
        "character_spectrum_is_corrected_cdiv": character_spectrum(generators)
        == {"-4": 6, "-1": 8, "2": 12, "8": 1},
        "common_neighbor_profile_matches_affine_cube": common_neighbor_profiles(bridge_graph)
        == {"adjacent": {"1": 108}, "nonadjacent": {"2": 162, "4": 81}},
    }

    return {
        "part": "MMCCCLXXI",
        "theorem": "Bridge-line affine Cayley cube",
        "input_packet": "MMCCCLXX golden failure K2,2 x F3^3 carrier",
        "anchor_line": geometry["anchor_line"],
        "anchor_points": list(geometry["anchor_points"]),
        "endpoint_lines_by_anchor_point": {
            str(point): geometry["endpoint_lines"][point]
            for point in geometry["anchor_points"]
        },
        "bridge_line_count": len(geometry["bridge_lines"]),
        "sample_bridge_words": {str(line): list(words[line]) for line in geometry["bridge_lines"][:12]},
        "linear_relation": "x0 + x1 + 2*x2 + x3 = 0 over F3",
        "projection_profiles": projection_profiles,
        "intersection_graph": {
            "degree_profile": counter_to_json(Counter(len(neighbors) for neighbors in bridge_graph)),
            "edge_count": sum(len(neighbors) for neighbors in bridge_graph) // 2,
            "common_neighbor_profiles": common_neighbor_profiles(bridge_graph),
        },
        "cayley_model": {
            "coordinate_choice": "first three bridge-word coordinates",
            "generators": [list(vector) for vector in sorted(generators)],
            "standard_generators": [list(vector) for vector in sorted(standard_generators())],
            "standardizing_gl3_matrix": [list(row) for row in standardizing_matrix] if standardizing_matrix else None,
            "standardized_generator_images": [list(vector) for vector in generator_images],
            "spectrum": character_spectrum(generators),
        },
        "reading": (
            "The 27 bridge lines are the actual affine qutrit cube hidden inside "
            "the golden-selector failure carrier. Each bridge line is coordinatized "
            "by which off-anchor line it meets above each of the four anchor "
            "points. Those four coordinates obey one F3-linear relation, so any "
            "three coordinates give F3^3. Bridge-line intersection is exactly the "
            "corrected CDIV 8-generator Cayley graph after a GL(3,3) change "
            "of basis."
        ),
        "claim_boundary": (
            "This identifies the 27-line bridge carrier and its spectrum. It still "
            "does not identify the four K2,2 cross-pair copies with explicit "
            "O^-(6,2)/A5 cosets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = bridge_line_affine_cayley_cube_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXXI: Bridge-Line Affine Cayley Cube ===")
    print("bridge line count:", packet["bridge_line_count"])
    print("linear relation:", packet["linear_relation"])
    print("cayley spectrum:", packet["cayley_model"]["spectrum"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
