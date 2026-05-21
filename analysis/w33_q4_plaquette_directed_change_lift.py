"""Part MCLXXXI: Q4 plaquette directed-change lift.

MCLXXX identifies the 4x4 toroidal knight board with Q4 and uses it as the
binary router around the four-ray qutrit "now" context.  The next invariant is
the square-face/plaquette structure of Q4.

For Q4:

    square faces = C(4,2) * 2^(4-2) = 6 * 4 = 24.

The factors are exactly the temporal qutrit split:

    6 = directed past/future changes,
    4 = four rays in the Bell now-context.

Thus each router vertex sees the six directed qutrit changes as its six incident
plaquette directions, and the global 24 plaquettes match the W33 positive
gap/gauge multiplicity.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_self_entangled_qutrit_q4_router import q4_edges, q4_vertices  # noqa: E402


Bits = tuple[int, int, int, int]
Face = tuple[Bits, Bits, Bits, Bits]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _canonical_face(vertices: set[Bits]) -> Face:
    if len(vertices) != 4:
        raise ValueError("a Q4 square face must have four vertices")
    return tuple(sorted(vertices))  # type: ignore[return-value]


def directed_changes(q: int = 3) -> list[tuple[int, int]]:
    return [(past, future) for past in range(q) for future in range(q) if past != future]


def q4_square_faces() -> list[dict[str, object]]:
    faces: list[dict[str, object]] = []
    for varying_dims in combinations(range(4), 2):
        frozen_dims = tuple(dim for dim in range(4) if dim not in varying_dims)
        for frozen_values in product((0, 1), repeat=2):
            vertices: set[Bits] = set()
            for free_values in product((0, 1), repeat=2):
                bits = [0, 0, 0, 0]
                for dim, value in zip(frozen_dims, frozen_values):
                    bits[dim] = value
                for dim, value in zip(varying_dims, free_values):
                    bits[dim] = value
                vertices.add(tuple(bits))  # type: ignore[arg-type]
            faces.append(
                {
                    "varying_dims": varying_dims,
                    "frozen_dims": frozen_dims,
                    "frozen_values": frozen_values,
                    "vertices": _canonical_face(vertices),
                }
            )
    return sorted(faces, key=lambda face: (face["varying_dims"], face["frozen_dims"], face["frozen_values"]))  # type: ignore[index]


def face_edges(face: Face) -> set[tuple[Bits, Bits]]:
    q_edges = q4_edges()
    return {edge for edge in q_edges if edge[0] in face and edge[1] in face}


def face_edge_incidence_counts(faces: list[dict[str, object]]) -> Counter[tuple[Bits, Bits]]:
    counts: Counter[tuple[Bits, Bits]] = Counter()
    for face in faces:
        for edge in face_edges(face["vertices"]):  # type: ignore[arg-type]
            counts[edge] += 1
    return counts


def vertex_face_incidence_counts(faces: list[dict[str, object]]) -> Counter[Bits]:
    counts: Counter[Bits] = Counter()
    for face in faces:
        for vertex in face["vertices"]:  # type: ignore[union-attr]
            counts[vertex] += 1
    return counts


def face_by_direction_packet(faces: list[dict[str, object]]) -> dict[str, object]:
    changes = directed_changes()
    direction_pairs = list(combinations(range(4), 2))
    now_slots = list(product((0, 1), repeat=2))

    rows = []
    for index, change in enumerate(changes):
        varying_dims = direction_pairs[index]
        matched = [face for face in faces if face["varying_dims"] == varying_dims]
        matched = sorted(matched, key=lambda face: face["frozen_values"])  # type: ignore[index]
        rows.append(
            {
                "directed_change": change,
                "varying_dims": varying_dims,
                "now_slots": now_slots,
                "face_count": len(matched),
                "faces": [
                    {
                        "frozen_values": face["frozen_values"],
                        "vertices": face["vertices"],
                    }
                    for face in matched
                ],
            }
        )
    return {
        "directed_changes": changes,
        "direction_pairs": direction_pairs,
        "now_slots": now_slots,
        "rows": rows,
    }


def q4_plaquette_directed_change_packet() -> dict[str, object]:
    mclxiii = _load(ROOT / "PART_MCLXIII_TEMPORAL_SELF_ENTANGLED_QUTRIT_results.json")
    mclxxx = _load(ROOT / "PART_MCLXXX_SELF_ENTANGLED_QUTRIT_Q4_ROUTER_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")

    now_context_rays = int(mclxiii["bell_stabilizer_line"]["line_size"])
    directed = int(mclxiii["temporal_qutrit"]["directed_change_histories"])
    history_cells = int(mclxiii["temporal_qutrit"]["past_future_basis_pairs"])
    q4_vertices_count = int(mclxxx["q4_router"]["vertices"])
    q4_edges_count = int(mclxxx["q4_router"]["edges"])
    gap_multiplicity = int(mclxii["gap_shell_lock"]["gap_multiplicity"])
    su5_adjoint = int(mclxii["gap_shell_lock"]["dim_su5_adjoint"])

    faces = q4_square_faces()
    face_count = len(faces)
    face_edge_counts = face_edge_incidence_counts(faces)
    vertex_face_counts = vertex_face_incidence_counts(faces)
    direction_packet = face_by_direction_packet(faces)
    face_count_by_direction = {
        str(row["directed_change"]): row["face_count"] for row in direction_packet["rows"]  # type: ignore[index]
    }

    checks = {
        "q4_face_count_is_24": face_count == 24,
        "q4_face_count_factors_as_directed_changes_times_now_rays": face_count == directed * now_context_rays == 6 * 4,
        "directed_changes_are_q_factorial": directed == 6,
        "now_context_has_four_rays": now_context_rays == 4,
        "history_square_splits_as_now_plus_directed": history_cells == 9 == 3 + directed,
        "face_count_matches_w33_gap_multiplicity": face_count == gap_multiplicity == su5_adjoint == 24,
        "six_direction_pairs_match_directed_changes": len(list(combinations(range(4), 2))) == directed,
        "four_frozen_slots_match_now_context_rays": 2 ** (4 - 2) == now_context_rays,
        "each_directed_change_owns_four_faces": set(face_count_by_direction.values()) == {now_context_rays},
        "each_face_is_a_square_cycle": all(len(face_edges(face["vertices"])) == 4 for face in faces),  # type: ignore[arg-type]
        "each_edge_lies_in_three_faces": set(face_edge_counts.values()) == {3} and len(face_edge_counts) == q4_edges_count,
        "each_vertex_lies_in_six_faces": set(vertex_face_counts.values()) == {directed}
        and len(vertex_face_counts) == q4_vertices_count,
        "face_edge_incidence_identity": face_count * 4 == q4_edges_count * 3 == 96,
        "vertex_face_incidence_identity": face_count * 4 == q4_vertices_count * directed == 96,
        "router_payload_boundary_preserved": "not a replacement for W33" in mclxxx["ternary_binary_bridge"]["boundary"],
    }

    return {
        "part": "MCLXXXI",
        "theorem": "Q4 plaquette directed-change lift",
        "input_context": {
            "q": 3,
            "history_cells": history_cells,
            "directed_change_histories": directed,
            "now_context_rays": now_context_rays,
            "q4_vertices": q4_vertices_count,
            "q4_edges": q4_edges_count,
            "w33_gap_multiplicity": gap_multiplicity,
        },
        "plaquette_formula": {
            "identity": "faces(Q4) = C(4,2)*2^(4-2) = 6*4 = 24",
            "face_count": face_count,
            "direction_pairs": len(list(combinations(range(4), 2))),
            "frozen_now_slots": 2 ** (4 - 2),
            "directed_change_factor": directed,
            "now_context_factor": now_context_rays,
        },
        "incidence_laws": {
            "face_edge_incidence": "24 faces * 4 edges = 32 edges * 3 faces = 96",
            "vertex_face_incidence": "24 faces * 4 vertices = 16 vertices * 6 directed changes = 96",
            "edge_face_counts": dict(Counter(face_edge_counts.values())),
            "vertex_face_counts": dict(Counter(vertex_face_counts.values())),
        },
        "directed_change_face_packet": direction_packet,
        "w33_lock": {
            "q4_plaquettes": face_count,
            "w33_gap_multiplicity": gap_multiplicity,
            "su5_adjoint_dimension": su5_adjoint,
            "reading": "the Q4 router plaquettes supply a finite square-face model for the 24-dimensional W33 positive gap/gauge shell",
        },
        "claim_boundary": (
            "finite Q4 plaquette/router identity; this is not a continuum gauge-field curvature proof "
            "and does not upgrade Q4 beyond its local routing role"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = q4_plaquette_directed_change_packet()
    out_path = ROOT / "PART_MCLXXXI_Q4_PLAQUETTE_DIRECTED_CHANGE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXI: Q4 Plaquette Directed-Change Lift ===")
    print(packet["plaquette_formula"]["identity"])
    print(packet["incidence_laws"]["face_edge_incidence"])
    print(packet["incidence_laws"]["vertex_face_incidence"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
