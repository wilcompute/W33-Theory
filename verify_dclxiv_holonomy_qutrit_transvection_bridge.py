#!/usr/bin/env python3
"""Part DCLXIV: holonomy-qutrit transvection bridge.

The current `w33_paper.tex` frontier localizes the remaining smooth-realization
wall to the first nonzero nilpotent holonomy increment on the canonical mixed
plane host. The single-photon paper identifies the exact finite owner as the
two-qutrit W(3,3) carrier.

This verifier closes the gap between those statements. It shows that the
minimal holonomy witness

    N = [[0, 1], [0, 0]],   H = I + N = [[1, 1], [0, 1]]

is exactly the canonical qutrit symplectic shear/transvection class on one
F_3^2 factor, embedded in the two-qutrit phase space F_3^4. Its projective
action on the 40 W(3,3) points fixes the 13-point perp hyperplane and organizes
the remaining 27 points into 9 affine fibers of size 3.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from w33_h1_decomposition import J_matrix, apply_matrix_projective, transvection_matrix
from w33_homology import build_w33

OUT_PATH = ROOT / "data" / "dclxiv_holonomy_qutrit_transvection_bridge.json"
MODULUS = 3
ANCHOR_VECTOR = (1, 0, 0, 0)


@dataclass(frozen=True)
class BridgeSummary:
    field_order: int
    vertex_count: int
    transvection_order: int
    fixed_projective_count: int
    affine_bulk_count: int
    affine_fiber_count: int
    affine_fiber_size: int
    all_identities_hold: bool


def _mat_mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _symplectic_form(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    a, b, c, d = u
    a2, b2, c2, d2 = v
    return (a * b2 - b * a2 + c * d2 - d * c2) % MODULUS


def _embedded_qutrit_shear() -> np.ndarray:
    return _mat_mod3(
        np.array(
            [
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=int,
        )
    )


def _repo_transvection_generator() -> np.ndarray:
    return transvection_matrix(np.array(ANCHOR_VECTOR, dtype=int), J_matrix())


def _adapted_basis_change() -> np.ndarray:
    return _mat_mod3(np.diag([2, 1, 1, 1]))


def _compute_order(matrix: np.ndarray) -> int:
    identity = np.eye(matrix.shape[0], dtype=int)
    power = identity.copy()
    for order in range(1, 20):
        power = _mat_mod3(power @ matrix)
        if np.array_equal(power, identity):
            return order
    raise ValueError("matrix order exceeded search bound")


def _build_projective_orbits(matrix: np.ndarray) -> dict[str, Any]:
    n, vertices, adj, edges = build_w33()
    permutation = [vertices.index(apply_matrix_projective(matrix, v)) for v in vertices]

    seen: set[int] = set()
    orbit_indices: list[list[int]] = []
    for start in range(n):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = permutation[current]
        orbit_indices.append(orbit)

    orbits = [[vertices[i] for i in orbit] for orbit in orbit_indices]
    orbit_size_counts = Counter(len(orbit) for orbit in orbits)

    adjacency_sets = [set(row) for row in adj]
    adjacency_preserved = all(
        ((j in adjacency_sets[i]) == (permutation[j] in adjacency_sets[permutation[i]]))
        for i in range(n)
        for j in range(n)
        if i != j
    )

    return {
        "vertices": vertices,
        "permutation": permutation,
        "orbits": orbits,
        "orbit_size_counts": dict(sorted(orbit_size_counts.items())),
        "adjacency_preserved": adjacency_preserved,
        "edge_count": len(edges),
    }


def _normalize_affine_point(point: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    a, b, c, d = point
    if b % MODULUS == 0:
        raise ValueError("expected affine point with nonzero second coordinate")
    inverse = pow(int(b), -1, MODULUS)
    return (
        (inverse * a) % MODULUS,
        1,
        (inverse * c) % MODULUS,
        (inverse * d) % MODULUS,
    )


def build_bridge() -> dict[str, Any]:
    shear = _embedded_qutrit_shear()
    identity4 = np.eye(4, dtype=int)
    nilpotent = _mat_mod3(shear - identity4)
    J = J_matrix()

    repo_transvection = _repo_transvection_generator()
    basis_change = _adapted_basis_change()
    adapted_from_repo = _mat_mod3(basis_change @ repo_transvection @ basis_change)

    orbit_data = _build_projective_orbits(shear)
    vertices = orbit_data["vertices"]
    orbits = orbit_data["orbits"]

    fixed_points = sorted(orbit[0] for orbit in orbits if len(orbit) == 1)
    affine_orbits = [orbit for orbit in orbits if len(orbit) == 3]
    affine_points = sorted(point for orbit in affine_orbits for point in orbit)

    perp_hyperplane = sorted(
        point for point in vertices if _symplectic_form(point, ANCHOR_VECTOR) == 0
    )
    normalized_affine_points = sorted(_normalize_affine_point(point) for point in affine_points)

    expected_normalized_affine = sorted(
        (a, 1, c, d)
        for a in range(MODULUS)
        for c in range(MODULUS)
        for d in range(MODULUS)
    )

    affine_fibers = []
    for orbit in affine_orbits:
        normalized_orbit = sorted(_normalize_affine_point(point) for point in orbit)
        _, _, c, d = normalized_orbit[0]
        affine_fibers.append(
            {
                "fiber_key": [c, d],
                "orbit": normalized_orbit,
                "is_translation_fiber": normalized_orbit
                == [(0, 1, c, d), (1, 1, c, d), (2, 1, c, d)],
            }
        )
    affine_fibers = sorted(affine_fibers, key=lambda item: tuple(item["fiber_key"]))

    identities = {
        "embedded_shear_is_symplectic": np.array_equal(_mat_mod3(shear.T @ J @ shear), J),
        "embedded_shear_has_order_3": _compute_order(shear) == 3,
        "nilpotent_increment_is_square_zero": np.array_equal(_mat_mod3(nilpotent @ nilpotent), np.zeros((4, 4), dtype=int)),
        "holonomy_increment_matches_local_jordan_block": nilpotent[:2, :2].tolist() == [[0, 1], [0, 0]],
        "adapted_shear_is_gauge_equivalent_to_repo_transvection_generator": np.array_equal(adapted_from_repo, shear),
        "projective_action_preserves_w33_adjacency": orbit_data["adjacency_preserved"],
        "fixed_points_are_exactly_the_13_point_perp_hyperplane": fixed_points == perp_hyperplane and len(fixed_points) == 13,
        "remaining_points_form_the_27_point_affine_bulk": len(affine_points) == 27 and len(fixed_points) + len(affine_points) == 40,
        "affine_bulk_normalizes_to_all_a1cd_tuples": normalized_affine_points == expected_normalized_affine,
        "nonfixed_orbits_are_nine_3_cycles": orbit_data["orbit_size_counts"] == {1: 13, 3: 9},
        "every_three_cycle_is_one_affine_fiber": all(fiber["is_translation_fiber"] for fiber in affine_fibers),
        "therefore_the_open_holonomy_witness_is_the_canonical_qutrit_transvection_on_the_two_qutrit_carrier": (
            np.array_equal(_mat_mod3(shear.T @ J @ shear), J)
            and _compute_order(shear) == 3
            and fixed_points == perp_hyperplane
            and orbit_data["orbit_size_counts"] == {1: 13, 3: 9}
            and all(fiber["is_translation_fiber"] for fiber in affine_fibers)
        ),
    }

    summary = BridgeSummary(
        field_order=MODULUS,
        vertex_count=len(vertices),
        transvection_order=_compute_order(shear),
        fixed_projective_count=len(fixed_points),
        affine_bulk_count=len(affine_points),
        affine_fiber_count=len(affine_fibers),
        affine_fiber_size=3,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "matrices": {
            "embedded_qutrit_shear": shear.tolist(),
            "nilpotent_increment": nilpotent.tolist(),
            "repo_transvection_generator": repo_transvection.tolist(),
            "adapted_basis_change": basis_change.tolist(),
            "adapted_transvection_from_repo_generator": adapted_from_repo.tolist(),
        },
        "carrier_action": {
            "projective_orbit_size_counts": orbit_data["orbit_size_counts"],
            "fixed_projective_points": fixed_points,
            "perp_hyperplane_points": perp_hyperplane,
            "sample_affine_orbit": affine_fibers[0]["orbit"],
            "affine_fibers": affine_fibers,
        },
        "interpretation": {
            "exact_owner": "W(3,3) as two-qutrit Pauli commutation geometry",
            "fixed_shell": "13-point projective hyperplane PG(2,3)",
            "mobile_shell": "27-point affine bulk AG(3,3)",
            "fiber_packet": "9 affine fibers of size 3",
            "bridge_verdict": (
                "The current mixed-plane nilpotent holonomy increment is not a new external object. "
                "It is the canonical qutrit symplectic shear/transvection class on one F3^2 factor, "
                "embedded in the two-qutrit carrier F3^4. Its projective action is exactly the 13+27 shell: "
                "a fixed PG(2,3) memory screen and a 9x3 affine bulk."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()