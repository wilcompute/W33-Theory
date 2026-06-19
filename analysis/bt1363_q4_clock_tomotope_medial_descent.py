#!/usr/bin/env python3
"""BT1363: descend the BT1362 Q4 clock to the tomotope/Reye middle layer.

BT1362 found a symmetric Q4 gauge quotient whose active stabilizer is
C2^4:C4.  The antipodal translation 1111 lies inside that stabilizer.  Since
MCLXXXII already proved that Q4 face-edge incidence modulo 1111 is the
Reye/tomotope medial layer, the natural question is whether the BT1362 clock
descends to an actual action on that medial layer.

It does.  The quotient action has order 32 = (C2^4 / <1111>) : C4.  On the
48 tomotope middle blocks it has three orbits of size 16, while the pure C4
axis clock has twelve orbits of size 4.  Thus the same middle layer is both
12 binary/cyclic edge clocks and 3 ternary sheets over the 16 face labels.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1363_q4_clock_tomotope_medial_descent.json"

Bits4 = tuple[int, int, int, int]
Edge = tuple[Bits4, Bits4]
Face = tuple[Bits4, Bits4, Bits4, Bits4]

ANTIPODE: Bits4 = (1, 1, 1, 1)
CYCLIC_PERMS: tuple[tuple[int, int, int, int], ...] = (
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
)


def xor4(a: Bits4, b: Bits4 = ANTIPODE) -> Bits4:
    return tuple(x ^ y for x, y in zip(a, b))  # type: ignore[return-value]


def hamming(a: Bits4, b: Bits4) -> int:
    return sum(x != y for x, y in zip(a, b))


def canonical_edge(a: Bits4, b: Bits4) -> Edge:
    return tuple(sorted((a, b)))  # type: ignore[return-value]


def build_q4() -> tuple[list[Bits4], list[Edge], list[Face]]:
    verts = list(itertools.product((0, 1), repeat=4))
    edges: list[Edge] = []
    for v in verts:
        for dim in range(4):
            if v[dim] == 0:
                w = list(v)
                w[dim] = 1
                edges.append(canonical_edge(v, tuple(w)))  # type: ignore[arg-type]
    edges = sorted(edges)

    faces: list[Face] = []
    for i, j in itertools.combinations(range(4), 2):
        for v in verts:
            if v[i] != 0 or v[j] != 0:
                continue
            face_vertices = []
            for ai, aj in ((0, 0), (1, 0), (0, 1), (1, 1)):
                w = list(v)
                w[i] = ai
                w[j] = aj
                face_vertices.append(tuple(w))
            faces.append(tuple(sorted(face_vertices)))  # type: ignore[arg-type]
    faces = sorted(faces)
    return verts, edges, faces


def translate_face(face: Face) -> Face:
    return tuple(sorted(xor4(v) for v in face))  # type: ignore[return-value]


def translate_edge(edge: Edge) -> Edge:
    return canonical_edge(xor4(edge[0]), xor4(edge[1]))


def antipodal_orbits(items: list[object], translate) -> list[tuple[int, int]]:
    index = {item: i for i, item in enumerate(items)}
    seen: set[int] = set()
    out: list[tuple[int, int]] = []
    for i, item in enumerate(items):
        if i in seen:
            continue
        mate = index[translate(item)]
        orbit = tuple(sorted((i, mate)))
        seen.update(orbit)
        out.append(orbit)  # type: ignore[arg-type]
    return out


def face_edges(face: Face) -> list[Edge]:
    return [
        canonical_edge(a, b)
        for a, b in itertools.combinations(face, 2)
        if hamming(a, b) == 1
    ]


def apply_vertex(v: Bits4, perm: tuple[int, int, int, int], flip: int) -> Bits4:
    return tuple(v[perm[i]] ^ ((flip >> i) & 1) for i in range(4))  # type: ignore[return-value]


def apply_face(face: Face, perm: tuple[int, int, int, int], flip: int) -> Face:
    return tuple(sorted(apply_vertex(v, perm, flip) for v in face))  # type: ignore[return-value]


def apply_edge(edge: Edge, perm: tuple[int, int, int, int], flip: int) -> Edge:
    return canonical_edge(
        apply_vertex(edge[0], perm, flip),
        apply_vertex(edge[1], perm, flip),
    )


def orbit_action(
    items: list[object],
    item_orbits: list[tuple[int, int]],
    action,
    perm: tuple[int, int, int, int],
    flip: int,
) -> tuple[int, ...]:
    index = {item: i for i, item in enumerate(items)}
    orbit_of = {
        member: orbit_id
        for orbit_id, orbit in enumerate(item_orbits)
        for member in orbit
    }
    return tuple(
        orbit_of[index[action(items[orbit[0]], perm, flip)]] for orbit in item_orbits
    )


def permutation_orbits(n: int, perms: list[tuple[int, ...]]) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for i in range(n):
        if i in seen:
            continue
        queue = deque([i])
        seen.add(i)
        orbit: list[int] = []
        while queue:
            x = queue.popleft()
            orbit.append(x)
            for perm in perms:
                y = perm[x]
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        out.append(sorted(orbit))
    return sorted(out, key=lambda row: (len(row), row))


def direction_of_edge(edge: Edge) -> int:
    return next(i for i, (a, b) in enumerate(zip(edge[0], edge[1])) if a != b)


def directions_of_face(face: Face) -> tuple[int, int]:
    return tuple(
        i for i, column in enumerate(zip(*face)) if len(set(column)) == 2
    )  # type: ignore[return-value]


def build_result() -> dict[str, object]:
    _verts, edges, faces = build_q4()
    edge_index = {edge: i for i, edge in enumerate(edges)}
    face_orbits = antipodal_orbits(faces, translate_face)
    edge_orbits = antipodal_orbits(edges, translate_edge)
    face_orbit_of = {
        member: orbit_id
        for orbit_id, orbit in enumerate(face_orbits)
        for member in orbit
    }
    edge_orbit_of = {
        member: orbit_id
        for orbit_id, orbit in enumerate(edge_orbits)
        for member in orbit
    }

    incidences: list[tuple[int, int]] = []
    lift_counter: Counter[tuple[int, int]] = Counter()
    for face_id, face in enumerate(faces):
        for edge in face_edges(face):
            incidence = (face_orbit_of[face_id], edge_orbit_of[edge_index[edge]])
            lift_counter[incidence] += 1
    incidences = sorted(lift_counter)
    incidence_index = {incidence: i for i, incidence in enumerate(incidences)}

    stabilizer_elements = [(perm, flip) for perm in CYCLIC_PERMS for flip in range(16)]
    action_pairs = []
    kernel_elements = []
    for perm, flip in stabilizer_elements:
        face_perm = orbit_action(faces, face_orbits, apply_face, perm, flip)
        edge_perm = orbit_action(edges, edge_orbits, apply_edge, perm, flip)
        action_pairs.append((face_perm, edge_perm))
        if face_perm == tuple(range(12)) and edge_perm == tuple(range(16)):
            kernel_elements.append({"perm": list(perm), "flip": flip})

    quotient_actions = sorted(set(action_pairs))
    face_action_perms = sorted({pair[0] for pair in quotient_actions})
    edge_action_perms = sorted({pair[1] for pair in quotient_actions})
    incidence_action_perms = [
        tuple(incidence_index[(face_perm[a], edge_perm[b])] for a, b in incidences)
        for face_perm, edge_perm in quotient_actions
    ]

    pure_c4_actions = []
    for perm in CYCLIC_PERMS:
        face_perm = orbit_action(faces, face_orbits, apply_face, perm, 0)
        edge_perm = orbit_action(edges, edge_orbits, apply_edge, perm, 0)
        pure_c4_actions.append((face_perm, edge_perm))
    pure_face_perms = [pair[0] for pair in pure_c4_actions]
    pure_edge_perms = [pair[1] for pair in pure_c4_actions]
    pure_incidence_perms = [
        tuple(incidence_index[(face_perm[a], edge_perm[b])] for a, b in incidences)
        for face_perm, edge_perm in pure_c4_actions
    ]

    face_orbit_rows = permutation_orbits(len(face_orbits), face_action_perms)
    edge_orbit_rows = permutation_orbits(len(edge_orbits), edge_action_perms)
    incidence_orbit_rows = permutation_orbits(len(incidences), incidence_action_perms)
    pure_face_orbit_rows = permutation_orbits(len(face_orbits), pure_face_perms)
    pure_edge_orbit_rows = permutation_orbits(len(edge_orbits), pure_edge_perms)
    pure_incidence_orbit_rows = permutation_orbits(
        len(incidences), pure_incidence_perms
    )

    ternary_sheet_rows = []
    for sheet_id, orbit in enumerate(incidence_orbit_rows):
        projected_edges = Counter(incidences[i][0] for i in orbit)
        projected_faces = Counter(incidences[i][1] for i in orbit)
        ternary_sheet_rows.append(
            {
                "sheet": sheet_id,
                "middle_blocks": len(orbit),
                "tomotope_edge_labels_hit": len(projected_edges),
                "tomotope_face_labels_hit": len(projected_faces),
                "edge_projection_multiplicity_profile": dict(
                    sorted(Counter(projected_edges.values()).items())
                ),
                "face_projection_multiplicity_profile": dict(
                    sorted(Counter(projected_faces.values()).items())
                ),
            }
        )

    c4_clock_rows = []
    for cycle_id, orbit in enumerate(pure_incidence_orbit_rows):
        projected_edges = sorted({incidences[i][0] for i in orbit})
        projected_faces = sorted({incidences[i][1] for i in orbit})
        c4_clock_rows.append(
            {
                "cycle": cycle_id,
                "middle_blocks": len(orbit),
                "tomotope_edge_labels": projected_edges,
                "tomotope_face_labels": projected_faces,
            }
        )

    face_labels = [
        {
            "tomotope_edge_label": orbit_id,
            "q4_face_orbit": list(orbit),
            "q4_axis_pair": list(directions_of_face(faces[orbit[0]])),
        }
        for orbit_id, orbit in enumerate(face_orbits)
    ]
    edge_labels = [
        {
            "tomotope_face_label": orbit_id,
            "q4_edge_orbit": list(orbit),
            "q4_axis": direction_of_edge(edges[orbit[0]]),
        }
        for orbit_id, orbit in enumerate(edge_orbits)
    ]

    checks = {
        "q4_has_24_faces_32_edges_96_incidences": len(faces) == 24
        and len(edges) == 32
        and sum(len(face_edges(face)) for face in faces) == 96,
        "antipodal_quotient_is_12_16_48": len(face_orbits) == 12
        and len(edge_orbits) == 16
        and len(incidences) == 48,
        "each_middle_block_has_two_q4_lifts": dict(Counter(lift_counter.values()))
        == {2: 48},
        "bt1362_clock_stabilizer_order_64": len(stabilizer_elements) == 64,
        "antipodal_kernel_has_order_2": len(kernel_elements) == 2,
        "descended_clock_order_32": len(quotient_actions) == 32,
        "descended_clock_is_64_over_antipode": len(stabilizer_elements)
        // len(kernel_elements)
        == len(quotient_actions),
        "face_label_orbits_are_4_and_8": [len(row) for row in face_orbit_rows]
        == [4, 8],
        "face_labels_have_4_plus_8_total": sum(len(row) for row in face_orbit_rows)
        == 12,
        "face_action_is_transitive_on_16_labels": [len(row) for row in edge_orbit_rows]
        == [16],
        "middle_blocks_split_into_three_16_sheets": [
            len(row) for row in incidence_orbit_rows
        ]
        == [16, 16, 16],
        "each_ternary_sheet_hits_all_16_face_labels_once": all(
            row["tomotope_face_labels_hit"] == 16
            and row["face_projection_multiplicity_profile"] == {1: 16}
            for row in ternary_sheet_rows
        ),
        "ternary_edge_projection_profile_is_8_8_4": sorted(
            row["tomotope_edge_labels_hit"] for row in ternary_sheet_rows
        )
        == [4, 8, 8],
        "pure_c4_has_twelve_four_block_cycles": [
            len(row) for row in pure_incidence_orbit_rows
        ]
        == [4] * 12,
        "pure_c4_face_profile": [len(row) for row in pure_face_orbit_rows]
        == [2, 2, 4, 4],
        "pure_c4_face_label_profile": [len(row) for row in pure_edge_orbit_rows]
        == [4, 4, 4, 4],
        "middle_layer_has_binary_and_ternary_readings": len(pure_incidence_orbit_rows)
        * 4
        == len(incidence_orbit_rows) * 16
        == 48,
    }

    return {
        "bt": 1363,
        "title": "Q4 clock descent to tomotope/Reye medial layer",
        "verified": all(checks.values()),
        "q4_source": {
            "faces": len(faces),
            "edges": len(edges),
            "face_edge_incidences": 96,
        },
        "tomotope_reye_quotient": {
            "tomotope_edge_labels_from_q4_face_pairs": len(face_orbits),
            "tomotope_face_labels_from_q4_edge_pairs": len(edge_orbits),
            "middle_blocks": len(incidences),
            "lift_multiplicity_profile": dict(
                sorted(Counter(lift_counter.values()).items())
            ),
            "face_labels_sample": face_labels[:6],
            "edge_labels_sample": edge_labels[:8],
        },
        "descended_clock": {
            "bt1362_stabilizer_order": len(stabilizer_elements),
            "antipodal_kernel_elements": kernel_elements,
            "quotient_group_order": len(quotient_actions),
            "structure": "(C2^4/<1111>) : C4 = C2^3 : C4",
            "tomotope_edge_orbit_profile": [len(row) for row in face_orbit_rows],
            "tomotope_face_orbit_profile": [len(row) for row in edge_orbit_rows],
            "middle_block_orbit_profile": [len(row) for row in incidence_orbit_rows],
            "ternary_sheets": ternary_sheet_rows,
        },
        "pure_c4_clock": {
            "order": 4,
            "tomotope_edge_orbit_profile": [len(row) for row in pure_face_orbit_rows],
            "tomotope_face_orbit_profile": [len(row) for row in pure_edge_orbit_rows],
            "middle_block_orbit_profile": [
                len(row) for row in pure_incidence_orbit_rows
            ],
            "four_tick_cycles_sample": c4_clock_rows[:6],
        },
        "interpretation": (
            "The BT1362 local Q4 clock descends through the antipodal double cover "
            "to the tomotope/Reye middle layer.  The pure C4 axis clock decomposes "
            "the 48 middle blocks as twelve four-tick cycles, while adding the "
            "translation quotient fuses them into three 16-block sheets.  Each "
            "ternary sheet hits all 16 tomotope face labels exactly once."
        ),
        "boundary": (
            "This proves the clock action on the tomotope medial layer.  It does "
            "not yet identify the full Q6 flag bus or the 2160 D12 global atlas "
            "with this clock; those are the next lift targets."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "descended_clock": result["descended_clock"]["structure"],
                "middle_block_orbit_profile": result["descended_clock"][
                    "middle_block_orbit_profile"
                ],
                "pure_c4_middle_block_orbit_profile": result["pure_c4_clock"][
                    "middle_block_orbit_profile"
                ],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
