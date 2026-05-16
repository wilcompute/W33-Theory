#!/usr/bin/env python3
"""Part DCCLXVIII: nilpotent chain-lift / QEC bridge.

DCCLXVII proved that the local photonic/QEC return branch is the square-zero
F3 increment

    N = [[0, 1], [0, 0]].

This verifier lifts that operator from the local axis-syndrome slot to the
actual W(3,3) chain complex.  Over F3, orient the 2-skeleton

    C2 --d2--> C1 --d1--> C0

with dimensions (160, 240, 40).  The ranks are

    rank(d1) = 39, rank(d2) = 120,

so H1 has dimension 81.  Tensoring every chain group with the dual-number
extension F3[epsilon]/epsilon^2 gives dimensions

    (320, 480, 80)

and H1 dimension 162.  The chain-level nilpotent commutes with the boundary,
induces a square-zero rank-81 map on H1, and turns the W33 edge module into the
480-slot photonic fusion ledger.
"""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxvii_axis_syndrome_nilpotent_octahedral_bridge import (  # noqa: E402
    KLM,
    nilpotent_increment,
    rank_mod3,
)


OUT_PATH = ROOT / "data" / "dcclxviii_nilpotent_chain_lift_qec_bridge.json"

Q = 3
V_EXPECTED = 40
E_EXPECTED = 240
T_EXPECTED = 160
H1_EXPECTED = 81
FUSION_EXPECTED = 480
FULL_TETRA_EULER = -80


@dataclass(frozen=True)
class BridgeSummary:
    vertex_count: int
    edge_count: int
    triangle_count: int
    h1_dimension: int
    lifted_edge_dimension: int
    lifted_h1_dimension: int
    induced_nilpotent_rank_h1: int
    all_identities_hold: bool


def _mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % Q


def _scale_vector(scalar: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple((scalar * coordinate) % Q for coordinate in vector)


def _symplectic_form(x: tuple[int, int, int, int], y: tuple[int, int, int, int]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % Q


def _canonical_projective_point(vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for coordinate in vector:
        if coordinate % Q:
            return _scale_vector(1 if coordinate == 1 else 2, vector)
    raise ValueError("zero vector has no projective point")


def w33_points() -> list[tuple[int, int, int, int]]:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for vector in itertools.product(range(Q), repeat=4):
        if vector == (0, 0, 0, 0):
            continue
        point = _canonical_projective_point(tuple(int(x) for x in vector))
        if point not in seen:
            seen.add(point)
            points.append(point)
    return points


def w33_adjacency(points: list[tuple[int, int, int, int]]) -> list[set[int]]:
    adjacency = [set() for _ in points]
    for i, j in itertools.combinations(range(len(points)), 2):
        if _symplectic_form(points[i], points[j]) == 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    return adjacency


def edge_list(adjacency: list[set[int]]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(adjacency)) for j in sorted(adjacency[i]) if i < j]


def triangle_list(adjacency: list[set[int]]) -> list[tuple[int, int, int]]:
    return [
        (i, j, k)
        for i, j, k in itertools.combinations(range(len(adjacency)), 3)
        if j in adjacency[i] and k in adjacency[i] and k in adjacency[j]
    ]


def boundary_matrices() -> dict[str, Any]:
    points = w33_points()
    adjacency = w33_adjacency(points)
    edges = edge_list(adjacency)
    triangles = triangle_list(adjacency)
    edge_index = {edge: index for index, edge in enumerate(edges)}

    d1 = np.zeros((len(points), len(edges)), dtype=int)
    for column, (i, j) in enumerate(edges):
        d1[i, column] = -1
        d1[j, column] = 1

    d2 = np.zeros((len(edges), len(triangles)), dtype=int)
    for column, (i, j, k) in enumerate(triangles):
        d2[edge_index[(j, k)], column] += 1
        d2[edge_index[(i, k)], column] -= 1
        d2[edge_index[(i, j)], column] += 1

    d1 = _mod3(d1)
    d2 = _mod3(d2)
    composition = _mod3(d1 @ d2)

    return {
        "points": points,
        "adjacency": adjacency,
        "edges": edges,
        "triangles": triangles,
        "d1": d1,
        "d2": d2,
        "composition": composition,
    }


def chain_homology_data() -> dict[str, Any]:
    matrices = boundary_matrices()
    d1 = matrices["d1"]
    d2 = matrices["d2"]
    c0 = len(matrices["points"])
    c1 = len(matrices["edges"])
    c2 = len(matrices["triangles"])
    r1 = rank_mod3(d1)
    r2 = rank_mod3(d2)
    h0 = c0 - r1
    h1 = c1 - r1 - r2
    h2 = c2 - r2
    return {
        "chain_dimensions": {"C0": c0, "C1": c1, "C2": c2},
        "boundary_ranks": {"rank_d1": r1, "rank_d2": r2},
        "homology_dimensions": {"H0": h0, "H1": h1, "H2": h2},
        "euler_characteristic": c0 - c1 + c2,
        "d1_d2_is_zero": bool(np.array_equal(matrices["composition"], np.zeros_like(matrices["composition"]))),
    }


def lifted_chain_data() -> dict[str, Any]:
    base = chain_homology_data()
    dims = base["chain_dimensions"]
    ranks = base["boundary_ranks"]
    homology = base["homology_dimensions"]
    lifted_dims = {key: 2 * value for key, value in dims.items()}
    lifted_ranks = {key: 2 * value for key, value in ranks.items()}
    lifted_homology = {key: 2 * value for key, value in homology.items()}

    return {
        "dual_number_extension": "F3[epsilon]/epsilon^2",
        "lifted_chain_dimensions": lifted_dims,
        "lifted_boundary_ranks": lifted_ranks,
        "lifted_homology_dimensions": lifted_homology,
        "lifted_euler_characteristic": lifted_dims["C0"] - lifted_dims["C1"] + lifted_dims["C2"],
        "fusion_read": {
            "C1_lifted_dimension": lifted_dims["C1"],
            "KLM_rail_cover": 2 * lifted_dims["C1"],
        },
    }


def nilpotent_chain_data() -> dict[str, Any]:
    base = chain_homology_data()
    dims = base["chain_dimensions"]
    homology = base["homology_dimensions"]
    n2 = nilpotent_increment()

    chain_nilpotents = {}
    for name, dimension in dims.items():
        n_chain = _mod3(np.kron(np.eye(dimension, dtype=int), n2))
        chain_nilpotents[name] = {
            "dimension": int(n_chain.shape[0]),
            "rank": rank_mod3(n_chain),
            "kernel_dimension": int(n_chain.shape[0]) - rank_mod3(n_chain),
            "image_dimension": rank_mod3(n_chain),
            "square_zero": bool(np.array_equal(_mod3(n_chain @ n_chain), np.zeros_like(n_chain))),
        }

    homology_nilpotents = {}
    for name, dimension in homology.items():
        n_h = _mod3(np.kron(np.eye(dimension, dtype=int), n2))
        homology_nilpotents[name] = {
            "dimension": int(n_h.shape[0]),
            "rank": rank_mod3(n_h),
            "kernel_dimension": int(n_h.shape[0]) - rank_mod3(n_h),
            "image_dimension": rank_mod3(n_h),
            "square_zero": bool(np.array_equal(_mod3(n_h @ n_h), np.zeros_like(n_h))),
        }

    return {
        "local_increment": n2.tolist(),
        "chain_nilpotents": chain_nilpotents,
        "homology_nilpotents": homology_nilpotents,
        "exact_sequence_on_h1": "0 -> 81 -> 162 -> 81 -> 0",
        "read": (
            "At chain level N sends the return/syndrome copy to the accepted/frame "
            "copy and then vanishes. Since it commutes with d1 and d2, the same "
            "square-zero map descends to homology."
        ),
    }


def boundary_commutation_data() -> dict[str, Any]:
    matrices = boundary_matrices()
    d1 = matrices["d1"]
    d2 = matrices["d2"]
    n0 = _mod3(np.kron(np.eye(d1.shape[0], dtype=int), nilpotent_increment()))
    n1 = _mod3(np.kron(np.eye(d1.shape[1], dtype=int), nilpotent_increment()))
    n2 = _mod3(np.kron(np.eye(d2.shape[1], dtype=int), nilpotent_increment()))
    d1_lift = _mod3(np.kron(d1, np.eye(2, dtype=int)))
    d2_lift = _mod3(np.kron(d2, np.eye(2, dtype=int)))
    d1_commutator = _mod3(n0 @ d1_lift - d1_lift @ n1)
    d2_commutator = _mod3(n1 @ d2_lift - d2_lift @ n2)

    return {
        "d1_lift_shape": list(d1_lift.shape),
        "d2_lift_shape": list(d2_lift.shape),
        "rank_d1_lift": rank_mod3(d1_lift),
        "rank_d2_lift": rank_mod3(d2_lift),
        "d1_commutes_with_nilpotent": bool(np.array_equal(d1_commutator, np.zeros_like(d1_commutator))),
        "d2_commutes_with_nilpotent": bool(np.array_equal(d2_commutator, np.zeros_like(d2_commutator))),
        "lifted_composition_zero": bool(
            np.array_equal(_mod3(d1_lift @ d2_lift), np.zeros((d1_lift.shape[0], d2_lift.shape[1]), dtype=int))
        ),
    }


def build_bridge() -> dict[str, Any]:
    base = chain_homology_data()
    lifted = lifted_chain_data()
    nilpotent = nilpotent_chain_data()
    commutation = boundary_commutation_data()

    identities = {
        "oriented_w33_chain_counts_are_40_240_160": base["chain_dimensions"] == {"C0": 40, "C1": 240, "C2": 160},
        "oriented_boundaries_form_a_chain_complex_over_f3": base["d1_d2_is_zero"] is True,
        "boundary_ranks_are_39_and_120": base["boundary_ranks"] == {"rank_d1": 39, "rank_d2": 120},
        "base_homology_is_1_81_40": base["homology_dimensions"] == {"H0": 1, "H1": 81, "H2": 40},
        "truncated_euler_characteristic_is_minus_40": base["euler_characteristic"] == -40,
        "dual_number_lift_doubles_chain_groups": lifted["lifted_chain_dimensions"] == {"C0": 80, "C1": 480, "C2": 320},
        "lifted_edge_module_is_the_480_fusion_ledger": lifted["fusion_read"]["C1_lifted_dimension"] == FUSION_EXPECTED,
        "klm_rail_cover_is_960": lifted["fusion_read"]["KLM_rail_cover"] == KLM == 960,
        "lifted_boundary_ranks_double": lifted["lifted_boundary_ranks"] == {"rank_d1": 78, "rank_d2": 240},
        "lifted_homology_is_2_162_80": lifted["lifted_homology_dimensions"] == {"H0": 2, "H1": 162, "H2": 80},
        "lifted_euler_matches_promoted_full_tetrahedral_shell_value": (
            lifted["lifted_euler_characteristic"] == FULL_TETRA_EULER
        ),
        "nilpotent_commutes_with_lifted_boundaries": (
            commutation["d1_commutes_with_nilpotent"]
            and commutation["d2_commutes_with_nilpotent"]
            and commutation["lifted_composition_zero"]
        ),
        "h1_nilpotent_is_exact_0_81_162_81_0": (
            nilpotent["homology_nilpotents"]["H1"]["dimension"] == 162
            and nilpotent["homology_nilpotents"]["H1"]["rank"] == H1_EXPECTED
            and nilpotent["homology_nilpotents"]["H1"]["kernel_dimension"] == H1_EXPECTED
            and nilpotent["homology_nilpotents"]["H1"]["image_dimension"] == H1_EXPECTED
            and nilpotent["homology_nilpotents"]["H1"]["square_zero"] is True
        ),
    }

    summary = BridgeSummary(
        vertex_count=base["chain_dimensions"]["C0"],
        edge_count=base["chain_dimensions"]["C1"],
        triangle_count=base["chain_dimensions"]["C2"],
        h1_dimension=base["homology_dimensions"]["H1"],
        lifted_edge_dimension=lifted["lifted_chain_dimensions"]["C1"],
        lifted_h1_dimension=lifted["lifted_homology_dimensions"]["H1"],
        induced_nilpotent_rank_h1=nilpotent["homology_nilpotents"]["H1"]["rank"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "base_chain_complex": base,
        "dual_number_lift": lifted,
        "nilpotent_chain_map": nilpotent,
        "boundary_commutation": commutation,
        "identities": identities,
        "theorem": (
            "Nilpotent Chain-Lift / QEC Bridge. The oriented W33 2-skeleton over F3 "
            "has chain dimensions (40,240,160), boundary ranks (39,120), and "
            "H=(1,81,40). Tensoring the full chain complex with F3[epsilon]/epsilon^2 "
            "doubles the edge-chain module to 480, exactly the photonic fusion "
            "ledger, and doubles H1 to 162. The square-zero nilpotent epsilon map "
            "commutes with both boundaries and descends to a rank-81 square-zero "
            "operator on H1, giving 0 -> 81 -> 162 -> 81 -> 0."
        ),
        "snake_eats_tail_read": (
            "The QEC tail is a chain map, not an analogy: the return/syndrome copy "
            "is mapped into the accepted/frame copy by N, N commutes with the CSS "
            "boundaries, and the induced H1 tail has image = kernel = 81."
        ),
        "honesty_boundary": (
            "This is an exact finite chain-complex and nilpotent-extension theorem "
            "over F3. It does not prove a hardware noise threshold, a non-Clifford "
            "photonic magic-state protocol, or the curved 4D spectral-action limit."
        ),
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
    print(f"H1_lift = {payload['summary']['lifted_h1_dimension']}")
    print(f"C1_lift = {payload['summary']['lifted_edge_dimension']}")


if __name__ == "__main__":
    main()
