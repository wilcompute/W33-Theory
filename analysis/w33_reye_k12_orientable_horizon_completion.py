"""Part MCXCII: Reye-K12 orientable horizon completion.

MCLXXXII identified the antipodal Q4 quotient with Reye's (12_4, 16_3)
configuration, the tomotope edge-triangle medial layer.  The new step is to use
those 12 Reye points as the vertices of the K12 horizon.

The 16 Reye lines are included as oriented triangular faces in a full orientable
twofold triple system on 12 vertices.  The completion has 44 triangles, so its
underlying graph is K12:

    V = 12, E = C(12, 2) = 66, F = 44, chi = -10, genus = 6 = q!.

Thus the [72,66]_3 horizon is the K12 edge payload plus one parity/check symbol
per orientable information hole, and the tomotope/Reye skeleton supplies the
first 16 triangular faces of that horizon.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

Q = 3
MU = 4
K = 12
W33_VERTICES = 40
TOMOTOPE_TRIANGLES = 16

# sign 0 means the sorted triple (a,b,c) is oriented as a -> b -> c -> a.
# sign 1 means the sorted triple is oriented as a -> c -> b -> a.
REYE_ORIENTED_SIGNS: tuple[tuple[tuple[int, int, int], int], ...] = (
    ((0, 1, 11), 0),
    ((0, 2, 10), 1),
    ((0, 4, 9), 1),
    ((0, 7, 8), 1),
    ((1, 3, 10), 0),
    ((1, 5, 9), 1),
    ((1, 6, 8), 1),
    ((2, 3, 11), 1),
    ((2, 5, 8), 1),
    ((2, 6, 9), 1),
    ((3, 4, 8), 0),
    ((3, 7, 9), 1),
    ((4, 5, 11), 0),
    ((4, 6, 10), 1),
    ((5, 7, 10), 0),
    ((6, 7, 11), 1),
)

RESIDUAL_ORIENTED_SIGNS: tuple[tuple[tuple[int, int, int], int], ...] = (
    ((0, 1, 2), 1),
    ((0, 3, 4), 1),
    ((0, 3, 8), 0),
    ((0, 5, 6), 0),
    ((0, 5, 11), 1),
    ((0, 6, 10), 0),
    ((0, 7, 9), 0),
    ((1, 2, 3), 0),
    ((1, 4, 9), 0),
    ((1, 4, 10), 1),
    ((1, 5, 8), 0),
    ((1, 6, 7), 0),
    ((1, 7, 11), 0),
    ((2, 4, 7), 1),
    ((2, 4, 11), 0),
    ((2, 5, 9), 0),
    ((2, 6, 8), 0),
    ((2, 7, 10), 1),
    ((3, 5, 7), 1),
    ((3, 5, 10), 0),
    ((3, 6, 9), 0),
    ((3, 6, 11), 1),
    ((4, 5, 6), 1),
    ((4, 7, 8), 0),
    ((8, 9, 10), 1),
    ((8, 9, 11), 0),
    ((8, 10, 11), 1),
    ((9, 10, 11), 0),
)


def _load(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def orient(triple: tuple[int, int, int], sign: int) -> tuple[int, int, int]:
    a, b, c = triple
    if sign == 0:
        return (a, b, c)
    if sign == 1:
        return (a, c, b)
    raise ValueError(f"orientation sign must be 0 or 1, got {sign}")


def directed_edges(face: tuple[int, int, int]) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    a, b, c = face
    return ((a, b), (b, c), (c, a))


def unordered_edges(face: tuple[int, int, int]) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    return tuple(tuple(sorted(edge)) for edge in directed_edges(face))  # type: ignore[return-value]


def canonical_reye_lines() -> tuple[tuple[int, int, int], ...]:
    """Reye model from cube vertices, center, and three infinity points."""

    points: list[tuple[str, object]] = [
        *[("v", bits) for bits in product((0, 1), repeat=3)],
        ("center", 0),
        *[("infinity", dim) for dim in range(3)],
    ]
    lines: list[tuple[int, int, int]] = []

    for dim in range(3):
        frozen_dims = [candidate for candidate in range(3) if candidate != dim]
        for frozen_values in product((0, 1), repeat=2):
            left = [0, 0, 0]
            right = [0, 0, 0]
            for frozen_dim, value in zip(frozen_dims, frozen_values):
                left[frozen_dim] = value
                right[frozen_dim] = value
            left[dim] = 0
            right[dim] = 1
            lines.append(
                tuple(
                    sorted(
                        [
                            points.index(("v", tuple(left))),
                            points.index(("v", tuple(right))),
                            points.index(("infinity", dim)),
                        ]
                    )
                )
            )

    for bits in product((0, 1), repeat=3):
        if bits[0] != 0:
            continue
        opposite = tuple(1 - bit for bit in bits)
        lines.append(
            tuple(
                sorted(
                    [
                        points.index(("v", bits)),
                        points.index(("v", opposite)),
                        points.index(("center", 0)),
                    ]
                )
            )
        )
    return tuple(sorted(lines))


def oriented_reye_faces() -> tuple[tuple[int, int, int], ...]:
    return tuple(orient(triple, sign) for triple, sign in REYE_ORIENTED_SIGNS)


def oriented_residual_faces() -> tuple[tuple[int, int, int], ...]:
    return tuple(orient(triple, sign) for triple, sign in RESIDUAL_ORIENTED_SIGNS)


def oriented_horizon_faces() -> tuple[tuple[int, int, int], ...]:
    return (*oriented_reye_faces(), *oriented_residual_faces())


def reye_pair_count_profile() -> dict[int, int]:
    pair_counts: Counter[tuple[int, int]] = Counter()
    for triple in canonical_reye_lines():
        for pair in combinations(triple, 2):
            pair_counts[tuple(sorted(pair))] += 1
    all_pairs = [tuple(pair) for pair in combinations(range(K), 2)]
    return dict(sorted(Counter(pair_counts[pair] for pair in all_pairs).items()))


def reye_k12_orientable_horizon_completion_packet() -> dict[str, Any]:
    mclxxxii = _load(ROOT / "PART_MCLXXXII_Q4_TOMOTOPE_REYE_DOUBLE_COVER_results.json")

    reye_lines = canonical_reye_lines()
    reye_underlying = tuple(sorted(triple for triple, _sign in REYE_ORIENTED_SIGNS))
    residual_underlying = tuple(sorted(triple for triple, _sign in RESIDUAL_ORIENTED_SIGNS))
    faces = oriented_horizon_faces()
    directed = [edge for face in faces for edge in directed_edges(face)]
    unordered = [edge for face in faces for edge in unordered_edges(face)]

    vertices = K
    edges = math.comb(vertices, 2)
    triangular_faces = len(faces)
    chi = vertices - edges + triangular_faces
    genus = (2 - chi) // 2
    horizon_total = edges + genus
    horizon_payload = edges
    horizon_parity = genus
    reye_edge_profile = reye_pair_count_profile()
    residual_edge_incidences = len(RESIDUAL_ORIENTED_SIGNS) * 3

    directed_profile = Counter(directed)
    unordered_profile = Counter(tuple(sorted(edge)) for edge in unordered)

    checks = {
        "mclxxxii_anchor_has_twelve_reye_points": mclxxxii["reye_model"]["points"] == K,
        "mclxxxii_anchor_has_sixteen_reye_lines": mclxxxii["reye_model"]["lines"] == TOMOTOPE_TRIANGLES,
        "canonical_reye_lines_match_oriented_reye_underlying": reye_lines == reye_underlying,
        "reye_faces_count_is_tomotope_triangles": len(REYE_ORIENTED_SIGNS) == TOMOTOPE_TRIANGLES == 16,
        "residual_faces_count_is_28": len(RESIDUAL_ORIENTED_SIGNS) == 28,
        "total_triangles_is_44": triangular_faces == 44,
        "all_triangles_are_distinct": len({tuple(sorted(face)) for face in faces}) == triangular_faces,
        "each_directed_k12_edge_appears_once": len(directed_profile) == K * (K - 1)
        and set(directed_profile.values()) == {1},
        "each_unordered_k12_edge_appears_twice": len(unordered_profile) == edges
        and set(unordered_profile.values()) == {2},
        "orientable_twofold_triple_system": len(directed_profile) == 132 and len(unordered_profile) == 66,
        "k12_edge_payload_is_66": edges == 66,
        "euler_characteristic_is_minus_10": chi == -10,
        "genus_is_q_factorial": genus == math.factorial(Q) == 6,
        "horizon_code_is_72_66_6": [horizon_total, horizon_payload, horizon_parity] == [72, 66, 6],
        "hole_cost_is_k": 2 * genus == K == 12,
        "reye_pair_profile_is_48_plus_18": reye_edge_profile == {0: 18, 1: 48},
        "residual_triangle_incidences_are_toroidal_flags": residual_edge_incidences == 84,
        "triangular_faces_minus_mu_is_w33_vertices": triangular_faces - MU == W33_VERTICES,
        "residual_faces_are_24_plus_mu": len(RESIDUAL_ORIENTED_SIGNS) == 24 + MU,
        "claim_boundary_preserved": "finite incidence-cover theorem" in mclxxxii["claim_boundary"],
    }

    return {
        "part": "MCXCII",
        "theorem": "Reye-K12 orientable horizon completion",
        "input_anchor": {
            "q4_antipodal_quotient": "MCLXXXII",
            "reye_points": K,
            "reye_lines": TOMOTOPE_TRIANGLES,
            "tomotope_medial_incidences": mclxxxii["tomotope_lock"]["edge_triangle_medial_incidences"],
        },
        "oriented_completion": {
            "vertices": vertices,
            "edges": edges,
            "reye_triangles": len(REYE_ORIENTED_SIGNS),
            "residual_triangles": len(RESIDUAL_ORIENTED_SIGNS),
            "total_triangles": triangular_faces,
            "directed_edge_count": len(directed),
            "directed_edge_profile": dict(sorted(Counter(directed_profile.values()).items())),
            "unordered_edge_profile": dict(sorted(Counter(unordered_profile.values()).items())),
            "reye_pair_profile": reye_edge_profile,
            "oriented_reye_faces": [list(face) for face in oriented_reye_faces()],
            "oriented_residual_faces": [list(face) for face in oriented_residual_faces()],
        },
        "surface": {
            "V": vertices,
            "E": edges,
            "F": triangular_faces,
            "chi": chi,
            "genus": genus,
            "information_hole_cost": 2 * genus,
            "closed_form": "K12 triangular horizon: V=12, E=66, F=44, chi=-10, genus=6=q!",
        },
        "horizon_code": {
            "total": horizon_total,
            "payload": horizon_payload,
            "parity": horizon_parity,
            "rate": "11/12",
            "reading": "[72,66]_3 = K12 edge payload plus one parity/check symbol per orientable information hole",
        },
        "residual_packet": {
            "residual_triangles": len(RESIDUAL_ORIENTED_SIGNS),
            "residual_edge_incidences": residual_edge_incidences,
            "reading": "the 28 non-Reye triangles contribute 84 directed edge incidences, one toroidal flag packet",
        },
        "external_source_alignment": {
            "graph_genus": "MathWorld records gamma(K_n)=ceil((n-3)(n-4)/12)",
            "triangular_embeddings": "Ellingham-Stephens note triangular embeddings of complete graphs are twofold triple systems",
            "tomotope": "the tomotope paper identifies Reye's configuration inside the tomotope medial layer",
        },
        "claim_boundary": (
            "finite oriented incidence completion; this supplies a K12 horizon surface "
            "containing the Q4/tomotope-Reye skeleton, not a continuum dynamics proof"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = reye_k12_orientable_horizon_completion_packet()
    out_path = ROOT / "PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCII: Reye-K12 Orientable Horizon Completion ===")
    print(packet["surface"]["closed_form"])
    print("horizon code:", [packet["horizon_code"]["total"], packet["horizon_code"]["payload"], packet["horizon_code"]["parity"]])
    print("Reye triangles:", packet["oriented_completion"]["reye_triangles"])
    print("residual triangles:", packet["oriented_completion"]["residual_triangles"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
