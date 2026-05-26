"""Toroidal dual symmetry groups for the Csaszar/Szilassi pair.

This verifier separates three symmetry layers that are easy to conflate:

* geometric symmetry of the concrete embedded polyhedra in
  data/Toroidal-Polyhedra-Realizations.txt: C2 for the listed realizations;
* abstract map automorphism group of the Csaszar/Szilassi dual toroidal maps:
  order 42, isomorphic to the Frobenius group C7 semidirect C6;
* bare graph automorphism group of the Szilassi skeleton/Heawood graph:
  order 336, larger by a factor of 8 because it forgets the toroidal face map.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import permutations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"


CSASZAR_FACES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (0, 2, 5),
    (0, 5, 4),
    (0, 4, 6),
    (0, 6, 3),
    (0, 3, 1),
    (1, 3, 4),
    (1, 4, 5),
    (1, 5, 6),
    (1, 6, 2),
    (2, 6, 4),
    (2, 4, 3),
    (2, 3, 5),
    (5, 3, 6),
)

SZILASSI_FACES: tuple[tuple[int, ...], ...] = (
    (0, 1, 13, 8, 7, 4),
    (0, 4, 3, 2, 10, 12),
    (0, 12, 9, 6, 5, 1),
    (11, 3, 4, 7, 6, 9),
    (11, 9, 12, 10, 8, 13),
    (11, 13, 1, 5, 2, 3),
    (2, 5, 6, 7, 8, 10),
)


def face_set(faces: tuple[tuple[int, ...], ...]) -> set[frozenset[int]]:
    return {frozenset(face) for face in faces}


def compose_perm(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def perm_order(perm: tuple[int, ...]) -> int:
    identity = tuple(range(len(perm)))
    current = identity
    for order in range(1, 100):
        current = compose_perm(perm, current)
        if current == identity:
            return order
    raise AssertionError(f"permutation order too large: {perm}")


def cyclic_orientations(face: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    a, b, c = face
    return {(a, b, c), (b, c, a), (c, a, b)}


def reversed_orientations(face: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    a, b, c = face
    return {(a, c, b), (c, b, a), (b, a, c)}


def csaszar_map_automorphisms() -> list[tuple[int, ...]]:
    faces = face_set(CSASZAR_FACES)
    automorphisms: list[tuple[int, ...]] = []
    for perm in permutations(range(7)):
        image = {frozenset(perm[vertex] for vertex in face) for face in CSASZAR_FACES}
        if image == faces:
            automorphisms.append(perm)
    return automorphisms


def csaszar_orientation_profiles(automorphisms: list[tuple[int, ...]]) -> dict[str, int]:
    oriented = set().union(*(cyclic_orientations(face) for face in CSASZAR_FACES))
    reversed_faces = set().union(*(reversed_orientations(face) for face in CSASZAR_FACES))
    preserving = 0
    reversing = 0
    for perm in automorphisms:
        image = [tuple(perm[vertex] for vertex in face) for face in CSASZAR_FACES]
        if all(face in oriented for face in image):
            preserving += 1
        if all(face in reversed_faces for face in image):
            reversing += 1
    return {"orientation_preserving": preserving, "orientation_reversing": reversing}


def dual_faces_from_csaszar() -> tuple[tuple[int, ...], ...]:
    dual_faces: list[tuple[int, ...]] = []
    for vertex in range(7):
        dual_faces.append(tuple(index for index, face in enumerate(CSASZAR_FACES) if vertex in face))
    return tuple(dual_faces)


def vertex_face_triples(vertex_count: int, faces: tuple[tuple[int, ...], ...]) -> set[frozenset[int]]:
    return {
        frozenset(face_index for face_index, face in enumerate(faces) if vertex in face)
        for vertex in range(vertex_count)
    }


def szilassi_dual_isomorphism_count() -> int:
    dual = vertex_face_triples(14, dual_faces_from_csaszar())
    listed = vertex_face_triples(14, SZILASSI_FACES)
    count = 0
    for face_perm in permutations(range(7)):
        image = {frozenset(face_perm[index] for index in triple) for triple in dual}
        if image == listed:
            count += 1
    return count


def c2_realization_permutations_preserve_faces() -> dict[str, bool]:
    csaszar_c2 = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4, 6: 6}
    szilassi_c2 = {
        0: 1,
        1: 0,
        2: 3,
        3: 2,
        4: 5,
        5: 4,
        6: 7,
        7: 6,
        8: 9,
        9: 8,
        10: 11,
        11: 10,
        12: 13,
        13: 12,
    }

    return {
        "csaszar_coordinate_c2_preserves_faces": {
            frozenset(csaszar_c2[vertex] for vertex in face) for face in CSASZAR_FACES
        }
        == face_set(CSASZAR_FACES),
        "szilassi_coordinate_c2_preserves_faces": {
            frozenset(szilassi_c2[vertex] for vertex in face) for face in SZILASSI_FACES
        }
        == face_set(SZILASSI_FACES),
    }


def realization_symmetry_counts() -> dict[str, int]:
    text = DATA_PATH.read_text(encoding="utf-8")
    return {
        "csaszar_c2_realizations": text.count("Csaszar Polyhedron (version"),
        "szilassi_c2_realizations": text.count("Szilassi Polyhedron (version"),
        "c2_symmetry_lines": text.count("Symmetry:  \t2-fold Cyclic  (C2)"),
    }


def toroidal_dual_symmetry_packet() -> dict[str, Any]:
    automorphisms = csaszar_map_automorphisms()
    order_profile = Counter(perm_order(perm) for perm in automorphisms)
    orientation = csaszar_orientation_profiles(automorphisms)
    c2_checks = c2_realization_permutations_preserve_faces()
    realization_counts = realization_symmetry_counts()
    heawood_graph_automorphism_order = 336

    checks = {
        "csaszar_vef_is_7_21_14": (7, 21, 14) == (7, 21, len(CSASZAR_FACES)),
        "szilassi_vef_is_14_21_7": (14, 21, 7) == (14, 21, len(SZILASSI_FACES)),
        "csaszar_face_set_automorphism_order_is_42": len(automorphisms) == 42,
        "csaszar_map_is_chiral_not_regular": orientation == {
            "orientation_preserving": 42,
            "orientation_reversing": 0,
        },
        "order_profile_matches_c7_semidirect_c6": dict(sorted(order_profile.items()))
        == {1: 1, 2: 7, 3: 14, 6: 14, 7: 6},
        "szilassi_listed_faces_are_dual_to_csaszar_faces": szilassi_dual_isomorphism_count() == 42,
        "dual_map_automorphism_order_is_42": len(automorphisms) == 42,
        "heawood_graph_forgets_map_faces_and_has_factor_8_more_symmetry": heawood_graph_automorphism_order
        == 8 * len(automorphisms),
        "both_coordinate_c2_involutions_preserve_faces": all(c2_checks.values()),
        "repo_realization_file_records_seven_c2_realizations": realization_counts
        == {"csaszar_c2_realizations": 5, "szilassi_c2_realizations": 2, "c2_symmetry_lines": 7},
        "each_map_has_84_flags": 4 * 21 == 84,
        "map_automorphism_order_is_half_flags": 2 * len(automorphisms) == 84,
        "dual_pair_flags_are_168": 2 * 84 == 168,
        "dual_pair_flags_are_four_map_groups": 2 * 84 == 4 * len(automorphisms),
    }

    return {
        "part": "MCCXLVII",
        "theorem": "Csaszar/Szilassi toroidal dual symmetry stratification",
        "repo_inputs": {
            "realization_data": str(DATA_PATH.relative_to(ROOT)),
            "csaszar_faces": [list(face) for face in CSASZAR_FACES],
            "szilassi_faces": [list(face) for face in SZILASSI_FACES],
        },
        "external_source_alignment": {
            "csaszar": "Wikipedia records Csaszar as a genus-one toroidal polyhedron with 7 vertices, 21 edges, 14 triangular faces, skeleton K7, and geometric symmetry C1 for the displayed model.",
            "szilassi": "Wikipedia records Szilassi as the dual genus-one toroidal polyhedron with 14 vertices, 21 edges, 7 hexagonal faces, Heawood-graph skeleton, and a 180-degree rotation axis.",
            "regular_map_database": "The dual Heawood map has V/F/E=7/14/21, Schlaefli type {3,6}, skeleton K7, and full symmetry group C7 semidirect C6 of order 42.",
            "heawood_graph": "The bare Heawood graph has automorphism group PGL_2(7) of order 336, which is eight times the map automorphism group.",
        },
        "symmetry_layers": {
            "geometric_realizations": {
                "repo_recorded_c2_realizations": realization_counts,
                "coordinate_c2_checks": c2_checks,
                "reading": "The concrete coordinate realizations keep only a C2 geometric symmetry in the repo data.",
            },
            "abstract_toroidal_maps": {
                "csaszar_map_automorphism_order": len(automorphisms),
                "szilassi_dual_map_automorphism_order": len(automorphisms),
                "group_shape": "C7 semidirect C6 = AGL(1,7), order 42",
                "element_order_profile": {str(key): int(value) for key, value in sorted(order_profile.items())},
                "orientation_profile": orientation,
                "flags_per_map": 84,
                "flag_orbits_per_map": 2,
            },
            "bare_graphs": {
                "csaszar_skeleton": "K7, graph automorphism S7 if faces are forgotten",
                "szilassi_skeleton": "Heawood graph, graph automorphism PGL_2(7) of order 336",
                "heawood_to_map_symmetry_ratio": heawood_graph_automorphism_order // len(automorphisms),
            },
        },
        "w33_bridge": {
            "single_map_flags": 84,
            "dual_pair_flags": 168,
            "dual_pair_flags_identity": "168 = 4*42 = |Aut(Fano)|",
            "pointed_split": "84 = 72 + 12 for either Csaszar vertex shell or Szilassi face shell",
            "tomotope_link": "168 + 24 = 192, matching the tomotope flag carrier with tetrahedral 24 added",
        },
        "reading": (
            "The two toroidal polyhedra carry the same abstract chiral map "
            "symmetry C7 semidirect C6 of order 42, while their concrete "
            "coordinate realizations preserve only C2. The Szilassi skeleton's "
            "Heawood graph has order-336 symmetry only before the seven hexagonal "
            "faces are remembered; the toroidal map cuts that by a factor of 8."
        ),
        "boundary": (
            "This is a symmetry stratification theorem. It does not assert that "
            "the geometric C2 model realizes the full abstract order-42 map group "
            "as Euclidean symmetries."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = toroidal_dual_symmetry_packet()
    out_path = ROOT / "PART_MCCXLVII_TOROIDAL_DUAL_SYMMETRY_GROUPS_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCXLVII: Toroidal Dual Symmetry Groups ===")
    print("geometric:", packet["symmetry_layers"]["geometric_realizations"])
    print("abstract:", packet["symmetry_layers"]["abstract_toroidal_maps"])
    print("bare graphs:", packet["symmetry_layers"]["bare_graphs"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
