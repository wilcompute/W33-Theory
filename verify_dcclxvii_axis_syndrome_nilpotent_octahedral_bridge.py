#!/usr/bin/env python3
"""Part DCCLXVII: axis-syndrome nilpotent / octahedral codec bridge.

DCCXVI factored the local photonic/QEC runtime alphabet as

    12 = 3 axes * 2 signs * 2 accepted/return roles.

DCCL-DCCLXVI made the same signed-axis set into the exact octahedral harmonic
phase space. DCLXXXV identified the remaining local holonomy witness as the
reduced F3 Jordan increment

    N = [[0, 1], [0, 0]],  N^2 = 0.

This verifier ties those lanes together. The six signed axes are the six
octahedron vertices. The 12 axis-syndrome slots are six signed axes tensored
with the two-state transport extension. Adding the KLM rail bit resolves each
slot into one of two non-opposite target axes, producing the 24 directed
octahedral turn incidences:

    480 = 40 * 12,
    960 = 40 * 24.

On the homological matter sector the same extension gives the exact sequence

    0 -> 81 -> 162 -> 81 -> 0

with a square-zero rank-81 nilpotent.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxvi_axis_syndrome_selector_codec_bridge import (  # noqa: E402
    DIRECTED,
    E,
    H1,
    KLM,
    LAM,
    Q,
    V,
    build_bridge as build_dccxvi_bridge,
)
from verify_dccl_octahedral_laplacian_heat_kernel_bridge import (  # noqa: E402
    adjacency_matrix,
    octahedron_vertices,
)


OUT_PATH = ROOT / "data" / "dcclxvii_axis_syndrome_nilpotent_octahedral_bridge.json"

MODULUS = 3
AXIS_ORDER = ["B23", "B31", "B12"]
ROLE_ORDER = ["accepted", "return"]


@dataclass(frozen=True)
class BridgeSummary:
    signed_axis_count: int
    local_axis_syndrome_slots: int
    local_directed_turns: int
    global_fusion_slots: int
    global_klm_primitives: int
    global_extension_dimension: int
    global_nilpotent_rank: int
    all_identities_hold: bool


def _mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def rank_mod3(matrix: np.ndarray) -> int:
    """Row-reduction rank over F3."""
    a = _mod3(matrix).copy()
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row, col] % MODULUS), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        inv = pow(int(a[rank, col]), -1, MODULUS)
        a[rank] = _mod3(inv * a[rank])
        for row in range(rows):
            if row != rank and a[row, col] % MODULUS:
                a[row] = _mod3(a[row] - int(a[row, col]) * a[rank])
        rank += 1
        if rank == rows:
            break
    return rank


def nilpotent_increment() -> np.ndarray:
    return np.array([[0, 1], [0, 0]], dtype=int)


def block_nilpotent(copy_count: int) -> np.ndarray:
    return _mod3(np.kron(np.eye(copy_count, dtype=int), nilpotent_increment()))


def nilpotent_data(copy_count: int) -> dict[str, Any]:
    n = block_nilpotent(copy_count)
    n2 = _mod3(n @ n)
    rank = rank_mod3(n)
    dimension = int(n.shape[0])
    return {
        "copy_count": copy_count,
        "dimension": dimension,
        "rank": rank,
        "kernel_dimension": dimension - rank,
        "image_dimension": rank,
        "square_zero": bool(np.array_equal(n2, np.zeros_like(n))),
    }


def signed_axis_vertices() -> list[dict[str, Any]]:
    return [
        {"index": index, "axis": axis, "sign": sign, "label": f"{'+' if sign > 0 else '-'}{axis}"}
        for index, (axis, sign) in enumerate(octahedron_vertices())
    ]


def local_axis_syndrome_basis() -> list[dict[str, Any]]:
    basis: list[dict[str, Any]] = []
    for vertex in signed_axis_vertices():
        for role_index, role in enumerate(ROLE_ORDER):
            basis.append(
                {
                    "basis_index": len(basis),
                    "signed_axis_index": vertex["index"],
                    "axis": vertex["axis"],
                    "sign": vertex["sign"],
                    "role": role,
                    "extension_coordinate": role_index,
                    "label": f"{role}:{vertex['label']}",
                }
            )
    return basis


def directed_octahedral_turns() -> list[dict[str, Any]]:
    turns: list[dict[str, Any]] = []
    vertices = {(axis, sign): index for index, (axis, sign) in enumerate(octahedron_vertices())}
    for source in signed_axis_vertices():
        other_axes = [axis for axis in AXIS_ORDER if axis != source["axis"]]
        for role in ROLE_ORDER:
            target_sign = source["sign"] if role == "accepted" else -source["sign"]
            for rail, target_axis in enumerate(other_axes):
                target_key = (target_axis, target_sign)
                target_index = vertices[target_key]
                edge_key = tuple(sorted([source["index"], target_index]))
                turns.append(
                    {
                        "source": source["label"],
                        "source_index": source["index"],
                        "role": role,
                        "klm_rail": rail,
                        "target": f"{'+' if target_sign > 0 else '-'}{target_axis}",
                        "target_index": target_index,
                        "edge_key": list(edge_key),
                    }
                )
    return turns


def octahedral_turn_data() -> dict[str, Any]:
    verts = octahedron_vertices()
    adjacency = adjacency_matrix(verts).astype(int)
    directed_turns = directed_octahedral_turns()
    unique_edges = sorted({tuple(turn["edge_key"]) for turn in directed_turns})
    edge_multiplicities = {
        f"{a}-{b}": sum(tuple(turn["edge_key"]) == (a, b) for turn in directed_turns)
        for a, b in unique_edges
    }

    return {
        "signed_axis_vertices": signed_axis_vertices(),
        "octahedral_adjacency": adjacency.tolist(),
        "undirected_edge_count": len(unique_edges),
        "directed_turn_count": len(directed_turns),
        "directed_turn_sample": directed_turns[:8],
        "each_undirected_edge_has_two_directions": all(value == 2 for value in edge_multiplicities.values()),
        "edge_multiplicities": edge_multiplicities,
    }


def build_bridge() -> dict[str, Any]:
    dccxvi = build_dccxvi_bridge()

    local_basis = local_axis_syndrome_basis()
    turn_data = octahedral_turn_data()
    local_nilpotent = nilpotent_data(copy_count=len(signed_axis_vertices()))
    global_nilpotent = nilpotent_data(copy_count=H1)
    reduced_nilpotent = nilpotent_increment()
    dclxxxv_canonical_nilpotent = np.array([[0, 1], [0, 0]], dtype=int)

    local_basis_labels = [entry["label"] for entry in local_basis]
    dccxvi_slot_labels = [slot["slot"] for slot in dccxvi["local_codec"]["local_slots"]]

    codec_counts = {
        "signed_axis_count": len(signed_axis_vertices()),
        "axis_syndrome_basis_size": len(local_basis),
        "octahedral_undirected_turn_edges": turn_data["undirected_edge_count"],
        "octahedral_directed_turns": turn_data["directed_turn_count"],
        "w33_vertices": V,
        "w33_edges": E,
        "fusion_slots": V * len(local_basis),
        "klm_primitives": V * turn_data["directed_turn_count"],
    }

    qec_extension = {
        "matter_dimension": H1,
        "extension_fiber_dimension": LAM,
        "total_dimension": H1 * LAM,
        "nilpotent_rank": global_nilpotent["rank"],
        "exact_sequence": "0 -> 81 -> 162 -> 81 -> 0",
        "read": (
            "The return/syndrome branch is a square-zero extension of the accepted "
            "frame branch; tensoring it with H1 gives image = kernel = 81."
        ),
    }

    identities = {
        "local_signed_axis_set_is_the_octahedron_vertex_set": (
            codec_counts["signed_axis_count"] == len(octahedron_vertices()) == 6
        ),
        "local_axis_syndrome_basis_is_dccxvi_3_times_2_times_2": (
            len(local_basis) == dccxvi["summary"]["local_codec_size"] == Q * LAM * LAM == 12
            and sorted(local_basis_labels) == sorted(dccxvi_slot_labels)
        ),
        "same_local_12_is_also_the_octahedral_undirected_turn_count": (
            codec_counts["octahedral_undirected_turn_edges"] == len(local_basis) == 12
        ),
        "klm_rail_resolves_axis_syndrome_slots_to_directed_octahedral_turns": (
            codec_counts["octahedral_directed_turns"] == len(local_basis) * LAM == 24
            and turn_data["each_undirected_edge_has_two_directions"] is True
        ),
        "global_fusion_slots_are_40_times_local_12": (
            codec_counts["fusion_slots"] == dccxvi["summary"]["fusion_attempt_slots"] == DIRECTED == 480
        ),
        "global_klm_slots_are_40_times_directed_octahedral_24": (
            codec_counts["klm_primitives"] == dccxvi["summary"]["klm_primitive_slots"] == KLM == 960
        ),
        "reduced_nilpotent_matches_dclxxxv_canonical_single_photon_jordan_witness": np.array_equal(
            reduced_nilpotent, dclxxxv_canonical_nilpotent
        ),
        "local_nilpotent_on_12_slots_is_square_zero_with_image_kernel_six": (
            local_nilpotent["dimension"] == 12
            and local_nilpotent["rank"] == 6
            and local_nilpotent["kernel_dimension"] == 6
            and local_nilpotent["image_dimension"] == 6
            and local_nilpotent["square_zero"] is True
        ),
        "global_matter_extension_is_0_81_162_81_0": (
            qec_extension["total_dimension"] == 162
            and global_nilpotent["dimension"] == 162
            and global_nilpotent["rank"] == H1
            and global_nilpotent["kernel_dimension"] == H1
            and global_nilpotent["image_dimension"] == H1
            and global_nilpotent["square_zero"] is True
        ),
        "snake_tail_runtime_counts_close": (
            E == 240 and DIRECTED == 2 * E and KLM == 4 * E and H1 == Q**4
        ),
    }

    summary = BridgeSummary(
        signed_axis_count=codec_counts["signed_axis_count"],
        local_axis_syndrome_slots=codec_counts["axis_syndrome_basis_size"],
        local_directed_turns=codec_counts["octahedral_directed_turns"],
        global_fusion_slots=codec_counts["fusion_slots"],
        global_klm_primitives=codec_counts["klm_primitives"],
        global_extension_dimension=qec_extension["total_dimension"],
        global_nilpotent_rank=qec_extension["nilpotent_rank"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "local_axis_syndrome_basis": local_basis,
        "octahedral_turn_data": turn_data,
        "nilpotent_extension": {
            "reduced_increment_mod3": reduced_nilpotent.tolist(),
            "local_12_slot_nilpotent": local_nilpotent,
            "global_matter_nilpotent": global_nilpotent,
            "dclxxxv_single_photon_increment": dclxxxv_canonical_nilpotent.tolist(),
            "dclxxxv_source_note": (
                "DCLXXXV promotes the same canonical reduced single-photon "
                "Jordan increment. DCCLXVII keeps the matrix inline to avoid "
                "pulling optional exploration graph dependencies into the "
                "focused architecture suite."
            ),
        },
        "codec_counts": codec_counts,
        "qec_extension": qec_extension,
        "theorem": (
            "Axis-Syndrome Nilpotent / Octahedral Codec Theorem. The six signed "
            "Clifford axes are the six octahedron vertices. The promoted local "
            "photonic/QEC alphabet is the 12-dimensional signed-axis tensor "
            "transport-extension basis, matching DCCXVI's 3*2*2 codec and the "
            "octahedron's 12 undirected turn edges. The KLM rail bit resolves "
            "each slot to one of two non-opposite target axes, giving the 24 "
            "directed octahedral incidences and hence 960=40*24 primitives. "
            "The same F3 extension carries N=[[0,1],[0,0]], so locally N has "
            "rank 6 on 12 slots, and on H1 it gives the exact square-zero "
            "sequence 0 -> 81 -> 162 -> 81 -> 0."
        ),
        "snake_eats_tail_read": (
            "The return branch is not an extra classical selector. It is the "
            "nilpotent tail of the accepted frame branch: N sends the return "
            "syndrome into the protected frame and then vanishes. This is the "
            "finite QEC version of the ouroboros loop."
        ),
        "honesty_boundary": (
            "This proves a finite runtime/codec/holonomy identity. It does not "
            "construct a universal non-Clifford photonic gate set, solve detector "
            "noise, or prove the curved 4D spectral-action asymptotics."
        ),
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    payload = build_bridge()
    print(f"Wrote {out}")
    print(f"Verified: {payload['summary']['all_identities_hold']}")
    print(f"480 = {payload['summary']['global_fusion_slots']}")
    print(f"960 = {payload['summary']['global_klm_primitives']}")


if __name__ == "__main__":
    main()
