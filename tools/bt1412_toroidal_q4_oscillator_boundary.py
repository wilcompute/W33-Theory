#!/usr/bin/env python3
"""BT1412: toroidal Q4 oscillator boundary.

This packet joins three already-verified layers:

* the 4x4 toroidal knight graph is Q4;
* the tetrahedral oscillator admits the mod-12 marks {0,3,4,7} and forbids
  genus h=q=3 on the neighborly ladder;
* the Csaszar/Szilassi toroidal pair preserves the 21-edge dual boundary.

The new certificate is the exact arithmetic splice:

    Q4 square faces = C(4,2) * 2^2 = 24
    oscillator aperture = 4 marks / 24 faces = 1/6
    24 faces - forbidden genus q=3 = 21 toroidal edges

It is an ABI/boundary theorem, not a physical waveguide layout.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_self_entangled_qutrit_q4_router import (  # noqa: E402
    KNIGHT_TO_Q4,
    KNIGHT_TOUR,
    hamming,
    knight_edges,
    q4_edges,
    q4_square_face_count,
    tour_bits,
    tour_flip_sequence,
)

OUT = ROOT / "data" / "bt1412_toroidal_q4_oscillator_boundary.json"
Q = 3
MU = 4


Bits = tuple[int, int, int, int]
Vertex = tuple[int, int]
BitEdge = tuple[Bits, Bits]


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def sorted_bit_edge(left: Bits, right: Bits) -> BitEdge:
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def bits_to_int(bits: Bits) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | bit
    return value


def board_parity(vertex: Vertex) -> int:
    row, col = vertex
    return (row + col) % 2


def bit_parity(bits: Bits) -> int:
    return sum(bits) % 2


def q4_square_faces() -> list[dict[str, Any]]:
    faces = []
    for dims in combinations(range(MU), 2):
        fixed_dims = [dim for dim in range(MU) if dim not in dims]
        for fixed_values in product((0, 1), repeat=len(fixed_dims)):
            base = [0, 0, 0, 0]
            for dim, value in zip(fixed_dims, fixed_values):
                base[dim] = value

            vertices = []
            for toggles in product((0, 1), repeat=2):
                bits = base[:]
                bits[dims[0]] = toggles[0]
                bits[dims[1]] = toggles[1]
                vertices.append(tuple(bits))  # type: ignore[arg-type]

            cycle_edges = {
                sorted_bit_edge(vertices[0], vertices[1]),
                sorted_bit_edge(vertices[0], vertices[2]),
                sorted_bit_edge(vertices[3], vertices[1]),
                sorted_bit_edge(vertices[3], vertices[2]),
            }
            faces.append(
                {
                    "dimensions": list(dims),
                    "fixed": dict(zip((str(dim) for dim in fixed_dims), fixed_values)),
                    "vertices": [list(vertex) for vertex in vertices],
                    "cycle_edges": [
                        [list(edge[0]), list(edge[1])] for edge in sorted(cycle_edges)
                    ],
                    "parities": [bit_parity(vertex) for vertex in vertices],
                }
            )
    return faces


def cycle_edges_from_tour(bits: list[Bits]) -> set[BitEdge]:
    return {
        sorted_bit_edge(bits[index], bits[(index + 1) % len(bits)])
        for index in range(len(bits))
    }


def projection_profile(bits: list[Bits]) -> dict[str, Any]:
    even_ticks = bits[::2]
    cyclic_distances = [
        hamming(even_ticks[index], even_ticks[(index + 1) % len(even_ticks)])
        for index in range(len(even_ticks))
    ]
    pairwise_distances = [
        hamming(left, right) for left, right in combinations(even_ticks, 2)
    ]
    return {
        "ticks": [bits_to_int(vertex) for vertex in even_ticks],
        "vertices": [list(vertex) for vertex in even_ticks],
        "cyclic_hamming_distances": cyclic_distances,
        "min_pairwise_hamming_distance": min(pairwise_distances),
        "max_pairwise_hamming_distance": max(pairwise_distances),
        "parity": sorted(set(bit_parity(vertex) for vertex in even_ticks)),
    }


def build_result() -> dict[str, Any]:
    bt802 = load_json("data/bt802_oscillator_atlas_verification.json")
    bt1316 = load_json("data/bt1316_toroidal_authoritative_data_lock.json")
    bt1319 = load_json("data/bt1319_toroidal_q4_hypercube_holonet_bridge.json")

    faces = q4_square_faces()
    face_count = len(faces)
    oscillator_marks = bt802["T2"]["marks"]
    mark_fraction = Fraction(len(oscillator_marks), face_count)
    forbidden_genus = Q
    toroidal_edge_boundary = face_count - forbidden_genus

    csaszar = bt1316["authoritative_values"]["csaszar"]
    szilassi = bt1316["authoritative_values"]["szilassi"]

    bits = tour_bits()
    cycle_edges = cycle_edges_from_tour(bits)
    all_q4_edges = q4_edges()
    extra_q4_chords = all_q4_edges - cycle_edges
    parity_trace = [
        {
            "tick": index,
            "board_vertex": list(vertex),
            "q4_word": list(KNIGHT_TO_Q4[vertex]),
            "board_parity": board_parity(vertex),
            "q4_parity": bit_parity(KNIGHT_TO_Q4[vertex]),
        }
        for index, vertex in enumerate(KNIGHT_TOUR)
    ]
    even_projection = projection_profile(bits)

    checks = {
        "bt802_oscillator_atlas_loaded": bt802["theorem"]
        == "BT802 oscillator atlas verification",
        "bt1316_toroidal_data_loaded": bt1316["verified"] is True,
        "bt1319_q4_bridge_loaded": bt1319["verified"] is True,
        "toroidal_knight_edges_are_q4_edges": len(knight_edges())
        == len(all_q4_edges)
        == 32,
        "tour_is_full_q4_gray_clock": len(bits) == 16
        and len(set(bits)) == 16
        and all(
            hamming(bits[index], bits[(index + 1) % len(bits)]) == 1
            for index in range(16)
        ),
        "tour_flip_sequence_matches_prior_q4_clock": tour_flip_sequence()
        == bt1319["q4_packet"]["gray_flip_sequence"],
        "board_parity_matches_q4_parity": all(
            item["board_parity"] == item["q4_parity"] for item in parity_trace
        ),
        "tour_alternates_parity_each_step": all(
            parity_trace[index]["q4_parity"]
            != parity_trace[(index + 1) % len(parity_trace)]["q4_parity"]
            for index in range(len(parity_trace))
        ),
        "q4_has_24_square_faces": face_count == q4_square_face_count() == 24,
        "every_q4_face_is_balanced_two_even_two_odd": all(
            sorted(face["parities"]) == [0, 0, 1, 1] for face in faces
        ),
        "q4_faces_match_tetrahedral_flag_window": face_count
        == Q * (Q - 1) * (Q + 1)
        == 24,
        "gray_clock_is_not_an_induced_snake": len(extra_q4_chords) == 16,
        "every_other_projection_has_eight_even_words": len(even_projection["ticks"])
        == 8
        and even_projection["parity"] == [0],
        "every_other_projection_is_distance_two_code": even_projection[
            "min_pairwise_hamming_distance"
        ]
        == 2
        and set(even_projection["cyclic_hamming_distances"]) == {2},
        "oscillator_marks_are_bt802_mod12_marks": oscillator_marks == [0, 3, 4, 7],
        "oscillator_mark_aperture_is_one_sixth": mark_fraction == Fraction(1, 6),
        "forbidden_genus_gap_is_q": forbidden_genus == Q
        and Q not in bt802["T3"]["attainable_start"]
        and bt802["T3"]["discriminant"] == 145,
        "q4_faces_minus_forbidden_q_is_21": toroidal_edge_boundary == 21,
        "csaszar_szilassi_share_21_edges": csaszar["edges"] == szilassi["edges"] == 21,
        "duality_preserves_edges_and_swaps_vertices_faces": (
            csaszar["vertices"],
            csaszar["faces"],
        )
        == (szilassi["faces"], szilassi["vertices"]),
        "dual_toroidal_boundary_has_e_equals_v_plus_f": csaszar["vertices"]
        + csaszar["faces"]
        == szilassi["vertices"] + szilassi["faces"]
        == csaszar["edges"]
        == szilassi["edges"],
        "q4_local_codecs_match_toroidal_codec_sum": bt1319["tomotope_codec"][
            "total_codecs"
        ]
        == 16
        and bt1319["tomotope_codec"]["reading"] == "(2+7+7)*12 = 16*12 = 192",
    }

    return {
        "bt": 1412,
        "title": "Toroidal Q4 oscillator boundary",
        "verified": all(checks.values()),
        "q4_toroidal_clock": {
            "vertices": 16,
            "edges": 32,
            "square_faces": face_count,
            "gray_flip_sequence": tour_flip_sequence(),
            "parity_trace": parity_trace,
            "extra_q4_chords_outside_gray_cycle": len(extra_q4_chords),
            "snake_boundary": (
                "The full 16-tick Gray clock is Hamiltonian but not an induced "
                "snake/coil: Q4 has 16 non-cycle chords.  The every-other "
                "projection is the distance-2 even-parity error-detecting layer."
            ),
            "even_projection": even_projection,
        },
        "oscillator_boundary": {
            "mod12_marks": oscillator_marks,
            "mark_count": len(oscillator_marks),
            "mark_aperture": f"{mark_fraction.numerator}/{mark_fraction.denominator}",
            "forbidden_genus": forbidden_genus,
            "forbidden_genus_discriminant": bt802["T3"]["discriminant"],
            "carrier_level": bt802["T6"]["carrier"],
        },
        "toroidal_dual_boundary": {
            "csaszar": csaszar,
            "szilassi": szilassi,
            "shared_edge_invariant": 21,
            "dual_edge_reading": (
                "Csaszar maximizes vertex adjacency and Szilassi maximizes face "
                "adjacency; duality swaps V and F while preserving the 21-edge "
                "channel."
            ),
        },
        "bridge_identities": {
            "q4_square_faces": face_count,
            "q4_face_formula": "C(4,2)*2^2 = 24 = q*(q-1)*(q+1)",
            "one_sixth_aperture": f"{len(oscillator_marks)}/{face_count} = 1/6",
            "edge_boundary_from_forbidden_genus": (
                f"{face_count} - {forbidden_genus} = {toroidal_edge_boundary}"
            ),
            "dual_polyhedron_e_equals_v_plus_f": "7+14=14+7=21",
            "codec_sum": bt1319["tomotope_codec"]["reading"],
        },
        "physical_reading": (
            "The local packet clock is a 16-state toroidal Q4 Gray clock.  Its "
            "24 square faces are the plaquette shell on which the tetrahedral "
            "oscillator's four admissible mod-12 marks occupy exactly a 1/6 "
            "aperture.  Removing the forbidden neighborly genus h=q=3 leaves "
            "21, the edge channel preserved by the Csaszar/Szilassi dual "
            "toroidal boundaries.  The every-other parity projection is the "
            "distance-2 error-detecting clock layer; the full Hamilton clock is "
            "not claimed to be an induced snake code."
        ),
        "boundary": (
            "BT1412 is a finite arithmetic and routing certificate. It does not "
            "prove a continuous optical embedding of the toroidal polyhedra, a "
            "new optimal snake-in-the-box code, or a calibrated physical "
            "oscillator. It supplies the exact local ABI boundary tying Q4 "
            "plaquettes, mod-12 oscillator marks, and the 21-edge toroidal dual "
            "channel."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "edge_boundary": result["toroidal_dual_boundary"][
                    "shared_edge_invariant"
                ],
                "oscillator_mark_aperture": result["oscillator_boundary"][
                    "mark_aperture"
                ],
                "q4_square_faces": result["q4_toroidal_clock"]["square_faces"],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
