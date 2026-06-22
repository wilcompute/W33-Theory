#!/usr/bin/env python3
"""BT1413: compile Q4 plaquettes into the tomotope/Q6 flag ABI.

BT1412 left the 24 Q4 square plaquettes as a boundary count.  BT1363 already
proved that Q4 face-edge incidence modulo the antipode is the 48-block
tomotope/Reye medial layer, and BT1371 already gave a 192-row tomotope-flag to
Q6-edge table.  This packet composes those maps:

    24 Q4 plaquettes -> 96 lifted face-edge incidences
      -> 48 antipodal middle blocks -> 48 * 4 = 192 tomotope flags
      -> 192 Q6 edge addresses.

It is an ABI compiler.  It does not assert a continuous optical embedding.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
for candidate in (ROOT, ANALYSIS):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from bt1363_q4_clock_tomotope_medial_descent import (  # noqa: E402
    CYCLIC_PERMS,
    antipodal_orbits,
    apply_edge,
    apply_face,
    build_q4,
    face_edges,
    orbit_action,
    permutation_orbits,
    translate_edge,
    translate_face,
)

OUT = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def q6_hamming(endpoint_a: str, endpoint_b: str) -> int:
    return sum(a != b for a, b in zip(endpoint_a, endpoint_b))


def q4_medial_model() -> dict[str, Any]:
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

    lift_counter: Counter[tuple[int, int]] = Counter()
    face_block_lifts: list[list[int]] = [[] for _ in faces]
    for face_id, face in enumerate(faces):
        for edge in face_edges(face):
            incidence = (face_orbit_of[face_id], edge_orbit_of[edge_index[edge]])
            lift_counter[incidence] += 1

    incidences = sorted(lift_counter)
    incidence_index = {incidence: i for i, incidence in enumerate(incidences)}
    for face_id, face in enumerate(faces):
        for edge in face_edges(face):
            incidence = (face_orbit_of[face_id], edge_orbit_of[edge_index[edge]])
            face_block_lifts[face_id].append(incidence_index[incidence])

    stabilizer_elements = [(perm, flip) for perm in CYCLIC_PERMS for flip in range(16)]
    action_pairs = []
    for perm, flip in stabilizer_elements:
        face_perm = orbit_action(faces, face_orbits, apply_face, perm, flip)
        edge_perm = orbit_action(edges, edge_orbits, apply_edge, perm, flip)
        action_pairs.append((face_perm, edge_perm))
    quotient_actions = sorted(set(action_pairs))
    incidence_action_perms = [
        tuple(incidence_index[(face_perm[a], edge_perm[b])] for a, b in incidences)
        for face_perm, edge_perm in quotient_actions
    ]
    sheet_rows = permutation_orbits(len(incidences), incidence_action_perms)
    block_to_sheet = {
        block_id: sheet_id
        for sheet_id, blocks in enumerate(sheet_rows)
        for block_id in blocks
    }

    return {
        "faces": faces,
        "edges": edges,
        "face_orbits": face_orbits,
        "edge_orbits": edge_orbits,
        "incidences": incidences,
        "lift_counter": lift_counter,
        "face_block_lifts": face_block_lifts,
        "sheet_rows": sheet_rows,
        "block_to_sheet": block_to_sheet,
    }


def flag_row(
    block_id: int,
    residue: int,
    sheet_id: int,
    tomotope_edge_label: int,
    tomotope_face_label: int,
    q6_address: dict[str, Any],
) -> dict[str, Any]:
    flag = 4 * block_id + residue
    return {
        "tomotope_flag": flag,
        "tomotope_block": block_id,
        "flag_residue": residue,
        "ternary_sheet": sheet_id,
        "tomotope_edge_label_from_q4_face_pair": tomotope_edge_label,
        "tomotope_face_label_from_q4_edge_pair": tomotope_face_label,
        "q6_edge_index": int(q6_address["q6_edge_index"]),
        "q6_direction": int(q6_address["q6_direction"]),
        "q6_endpoint_a": q6_address["q6_endpoint_a"],
        "q6_endpoint_b": q6_address["q6_endpoint_b"],
    }


def build_result() -> dict[str, Any]:
    bt1363 = load_json("data/bt1363_q4_clock_tomotope_medial_descent.json")
    bt1371 = load_json("data/bt1371_q6_tomotope_explicit_orbit_address_table.json")
    bt1412 = load_json("data/bt1412_toroidal_q4_oscillator_boundary.json")
    model = q4_medial_model()
    q6_by_flag = {row["tomotope_flag"]: row for row in bt1371["address_table"]}

    middle_blocks = []
    flag_rows = []
    for block_id, (tom_edge_label, tom_face_label) in enumerate(model["incidences"]):
        sheet_id = model["block_to_sheet"][block_id]
        flags = []
        for residue in range(4):
            flag = 4 * block_id + residue
            row = flag_row(
                block_id,
                residue,
                sheet_id,
                tom_edge_label,
                tom_face_label,
                q6_by_flag[flag],
            )
            flags.append(flag)
            flag_rows.append(row)
        middle_blocks.append(
            {
                "tomotope_block": block_id,
                "ternary_sheet": sheet_id,
                "tomotope_edge_label_from_q4_face_pair": tom_edge_label,
                "tomotope_face_label_from_q4_edge_pair": tom_face_label,
                "q4_lift_count": model["lift_counter"][
                    (tom_edge_label, tom_face_label)
                ],
                "tomotope_flags": flags,
            }
        )

    plaquette_rows = []
    for face_id, face in enumerate(model["faces"]):
        blocks = sorted(model["face_block_lifts"][face_id])
        plaquette_rows.append(
            {
                "q4_plaquette": face_id,
                "q4_vertices": [list(vertex) for vertex in face],
                "middle_blocks": blocks,
                "tomotope_flags": [
                    4 * block + residue for block in blocks for residue in range(4)
                ],
            }
        )

    sheet_summaries = []
    for sheet_id, blocks in enumerate(model["sheet_rows"]):
        edge_labels = Counter(
            middle_blocks[block]["tomotope_edge_label_from_q4_face_pair"]
            for block in blocks
        )
        face_labels = Counter(
            middle_blocks[block]["tomotope_face_label_from_q4_edge_pair"]
            for block in blocks
        )
        sheet_summaries.append(
            {
                "ternary_sheet": sheet_id,
                "middle_blocks": len(blocks),
                "tomotope_flags": len(blocks) * 4,
                "tomotope_edge_labels_hit": len(edge_labels),
                "tomotope_face_labels_hit": len(face_labels),
                "face_projection_multiplicity_profile": dict(
                    sorted(Counter(face_labels.values()).items())
                ),
                "edge_projection_multiplicity_profile": dict(
                    sorted(Counter(edge_labels.values()).items())
                ),
            }
        )

    flag_lift_hist = Counter(
        flag for row in plaquette_rows for flag in row["tomotope_flags"]
    )
    checks = {
        "bt1363_medial_descent_loaded": bt1363["verified"] is True,
        "bt1371_q6_address_table_loaded": bt1371["verified"] is True,
        "bt1412_boundary_loaded": bt1412["verified"] is True,
        "q4_has_24_plaquettes": len(model["faces"]) == 24,
        "q4_face_edge_lift_count_is_96": sum(
            len(row["middle_blocks"]) for row in plaquette_rows
        )
        == 96,
        "antipodal_middle_blocks_are_48": len(middle_blocks) == 48,
        "each_middle_block_has_two_q4_lifts": dict(
            Counter(block["q4_lift_count"] for block in middle_blocks)
        )
        == {2: 48},
        "four_flag_residues_per_middle_block": len(flag_rows) == 4 * len(middle_blocks),
        "flag_table_is_full_192_bijection": sorted(
            row["tomotope_flag"] for row in flag_rows
        )
        == list(range(192)),
        "each_q4_lift_touches_four_blocks": all(
            len(row["middle_blocks"]) == 4 for row in plaquette_rows
        ),
        "each_unique_flag_has_two_q4_plaquette_lifts": dict(
            sorted(Counter(flag_lift_hist.values()).items())
        )
        == {2: 192},
        "ternary_sheets_are_three_64_flag_sheets": [
            row["tomotope_flags"] for row in sheet_summaries
        ]
        == [64, 64, 64],
        "each_sheet_hits_all_16_tomotope_face_labels": all(
            row["tomotope_face_labels_hit"] == 16
            and row["face_projection_multiplicity_profile"] == {1: 16}
            for row in sheet_summaries
        ),
        "q6_addresses_are_one_bit_edges": all(
            q6_hamming(row["q6_endpoint_a"], row["q6_endpoint_b"]) == 1
            for row in flag_rows
        ),
        "q6_edge_addresses_are_bijective": len(
            {row["q6_edge_index"] for row in flag_rows}
        )
        == 192,
        "bt1412_one_sixth_aperture_survives": bt1412["oscillator_boundary"][
            "mark_aperture"
        ]
        == "1/6"
        and bt1412["q4_toroidal_clock"]["square_faces"] == 24,
    }

    return {
        "bt": 1413,
        "title": "Q4 plaquette to tomotope/Q6 flag compiler",
        "verified": all(checks.values()),
        "compiler_summary": {
            "q4_plaquettes": len(model["faces"]),
            "q4_face_edge_lifts": 96,
            "antipodal_middle_blocks": len(middle_blocks),
            "tomotope_flags": len(flag_rows),
            "q6_edges": len({row["q6_edge_index"] for row in flag_rows}),
            "formula": "24 plaquettes * 4 edge incidences / 2 antipodal lifts * 4 residues = 192 flags",
        },
        "sheet_summaries": sheet_summaries,
        "middle_blocks_sample": middle_blocks[:12],
        "plaquette_rows_sample": plaquette_rows[:6],
        "flag_rows_sample": flag_rows[:16],
        "bridge_identities": {
            "bt1363": "24 Q4 faces and 32 Q4 edges give 48 antipodal middle blocks",
            "bt1371": "tomotope_flag is a bijective Q6 edge address",
            "bt1412": "24 plaquettes carry the 1/6 oscillator aperture and 21-edge toroidal boundary",
        },
        "boundary": (
            "BT1413 is a finite address compiler. It proves that every Q4 "
            "plaquette incidence lowers to the existing 192-row tomotope/Q6 "
            "flag ABI. It does not supply waveguide geometry or detector timing."
        ),
        "middle_blocks": middle_blocks,
        "plaquette_rows": plaquette_rows,
        "flag_rows": flag_rows,
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
                "q4_plaquettes": result["compiler_summary"]["q4_plaquettes"],
                "tomotope_flags": result["compiler_summary"]["tomotope_flags"],
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
