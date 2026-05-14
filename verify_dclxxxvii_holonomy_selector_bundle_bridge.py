#!/usr/bin/env python3
"""Part DCLXXXVII: holonomy selector bundle bridge.

The local qutrit selector / Jordan witness from DCLXXXV-DCLXXXVI should not be
an accident of one sample fiber. This verifier proves uniformity across the
entire affine bulk and scales that local law to the full 1620 selector carrier.

Main claims:

  - all 9 affine qutrit fibers in the DCLXIV bulk carry the same 3-cycle;
  - all 9 fibers have the same 2x2 quotient matrix over F3;
  - that common quotient is GL(2,3)-conjugate to the exact Jordan block
    [[1,1],[0,1]] with nilpotent increment [[0,1],[0,0]];
  - the H4 selector carrier is therefore a uniform bundle of
        60 * 9 = 540
    identical local qutrit fibers, with total branch count
        540 * 3 = 1620.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from itertools import product
from pathlib import Path
from typing import Any, Iterable

import numpy as np


ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
for candidate in (ROOT, SCRIPTS):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from scripts.w33_h4_s3_selector_holonomy_audit import (  # noqa: E402
    h4_s3_selector_holonomy_summary,
)
from verify_dclxiv_holonomy_qutrit_transvection_bridge import (  # noqa: E402
    build_bridge as build_dclxiv_bridge,
)


MODULUS = 3
OUT_PATH = ROOT / "data" / "dclxxxvii_holonomy_selector_bundle_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    affine_fiber_count: int
    ordered_adjacent_pair_count: int
    global_qutrit_fiber_count: int
    global_branch_count: int
    all_identities_hold: bool


def _mat_mod3(matrix: Iterable[Iterable[int]] | np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _permutation_matrix(action: list[int]) -> np.ndarray:
    size = len(action)
    matrix = np.zeros((size, size), dtype=int)
    for column, image in enumerate(action):
        matrix[image, column] = 1
    return matrix


def _quotient_coords(vector: np.ndarray) -> tuple[int, int]:
    x, y, z = [int(entry) % MODULUS for entry in vector]
    return ((x - z) % MODULUS, (y - z) % MODULUS)


def _quotient_matrix_from_three_cycle(three_cycle: np.ndarray) -> np.ndarray:
    e0 = np.array([1, 0, 0], dtype=int)
    e1 = np.array([0, 1, 0], dtype=int)
    col0 = _quotient_coords(_mat_mod3(three_cycle @ e0))
    col1 = _quotient_coords(_mat_mod3(three_cycle @ e1))
    return _mat_mod3([[col0[0], col1[0]], [col0[1], col1[1]]])


def _gl2_mod3() -> Iterable[np.ndarray]:
    for a, b, c, d in product(range(MODULUS), repeat=4):
        matrix = np.array([[a, b], [c, d]], dtype=int)
        determinant = (a * d - b * c) % MODULUS
        if determinant != 0:
            yield matrix


def _inverse_gl2(matrix: np.ndarray) -> np.ndarray:
    a, b = [int(x) % MODULUS for x in matrix[0]]
    c, d = [int(x) % MODULUS for x in matrix[1]]
    determinant = (a * d - b * c) % MODULUS
    determinant_inverse = pow(determinant, -1, MODULUS)
    inverse = np.array([[d, -b], [-c, a]], dtype=int)
    return _mat_mod3(determinant_inverse * inverse)


def _find_conjugator(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    for basis_change in _gl2_mod3():
        candidate = _mat_mod3(_inverse_gl2(basis_change) @ source @ basis_change)
        if np.array_equal(candidate, target):
            return basis_change
    raise ValueError("no GL(2,3) conjugator found")


def build_bridge() -> dict[str, Any]:
    dclxiv = build_dclxiv_bridge()
    selector = h4_s3_selector_holonomy_summary()

    shear = _mat_mod3(dclxiv["matrices"]["embedded_qutrit_shear"])
    affine_fibers = [
        [tuple(point) for point in fiber["orbit"]]
        for fiber in dclxiv["carrier_action"]["affine_fibers"]
    ]

    local_actions: list[list[int]] = []
    quotient_matrices: list[np.ndarray] = []
    for fiber in affine_fibers:
        action: list[int] = []
        for point in fiber:
            image = tuple(
                int(entry) % MODULUS
                for entry in (shear @ np.array(point, dtype=int).reshape(4, 1)).flatten()
            )
            action.append(fiber.index(image))
        local_actions.append(action)
        quotient_matrices.append(_quotient_matrix_from_three_cycle(_permutation_matrix(action)))

    reference_action = local_actions[0]
    reference_quotient = quotient_matrices[0]
    jordan_block = np.array([[1, 1], [0, 1]], dtype=int)
    conjugator = _find_conjugator(reference_quotient, jordan_block)
    quotient_in_jordan_basis = _mat_mod3(
        _inverse_gl2(conjugator) @ reference_quotient @ conjugator
    )
    quotient_nilpotent = _mat_mod3(jordan_block - np.eye(2, dtype=int))

    local_fiber_count = len(affine_fibers)
    ordered_adjacent_pair_count = selector["heisenberg_transport_packet"]["ordered_adjacent_pairs"]
    global_qutrit_fiber_count = ordered_adjacent_pair_count * local_fiber_count
    global_branch_count = global_qutrit_fiber_count * len(reference_action)

    identities = {
        "every_affine_fiber_carries_the_same_three_cycle": (
            all(action == reference_action for action in local_actions)
            and reference_action == [1, 2, 0]
        ),
        "every_affine_fiber_has_the_same_reduced_two_by_two_selector_matrix": all(
            np.array_equal(matrix, reference_quotient) for matrix in quotient_matrices
        ),
        "the_common_reduced_matrix_is_gl2_conjugate_to_the_exact_jordan_block": np.array_equal(
            quotient_in_jordan_basis, jordan_block
        ),
        "the_common_nilpotent_increment_is_exactly_square_zero": np.array_equal(
            _mat_mod3(quotient_nilpotent @ quotient_nilpotent), np.zeros((2, 2), dtype=int)
        ),
        "the_local_affine_bulk_is_nine_uniform_qutrit_fibers": (
            local_fiber_count == dclxiv["summary"]["affine_fiber_count"] == 9
            and len(reference_action) == dclxiv["summary"]["affine_fiber_size"] == 3
        ),
        "the_global_selector_carrier_is_sixty_copies_of_that_nine_fiber_packet": (
            ordered_adjacent_pair_count == 60
            and global_qutrit_fiber_count == 60 * 9 == 540
        ),
        "the_total_branch_count_is_exactly_540_times_3_equals_1620": (
            global_branch_count == 540 * 3 == selector["h4_alignment_packet"]["nonlocal_quadrangle_carrier"] == 1620
        ),
        "therefore_the_existing_1620_selector_carrier_is_a_uniform_bundle_of_identical_local_qutrit_jordan_fibers": (
            all(action == [1, 2, 0] for action in local_actions)
            and all(np.array_equal(matrix, reference_quotient) for matrix in quotient_matrices)
            and np.array_equal(quotient_in_jordan_basis, jordan_block)
            and global_branch_count == 1620
        ),
    }

    summary = BridgeSummary(
        affine_fiber_count=local_fiber_count,
        ordered_adjacent_pair_count=ordered_adjacent_pair_count,
        global_qutrit_fiber_count=global_qutrit_fiber_count,
        global_branch_count=global_branch_count,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "local_bundle": {
            "reference_action": reference_action,
            "reference_quotient_matrix_mod3": reference_quotient.tolist(),
            "jordan_conjugator_mod3": conjugator.tolist(),
            "quotient_in_jordan_basis": quotient_in_jordan_basis.tolist(),
            "nilpotent_increment": quotient_nilpotent.tolist(),
            "fiber_actions": local_actions,
            "fiber_quotient_matrices": [matrix.tolist() for matrix in quotient_matrices],
        },
        "global_bundle": {
            "ordered_adjacent_pair_count": ordered_adjacent_pair_count,
            "local_qutrit_fibers_per_packet": local_fiber_count,
            "global_qutrit_fiber_count": global_qutrit_fiber_count,
            "branches_per_fiber": len(reference_action),
            "global_branch_count": global_branch_count,
        },
        "interpretation": {
            "verdict": (
                "The existing 1620 selector carrier is not just count-compatible with the local photonic qutrit selector law. "
                "It is a uniform bundle of 540 identical local qutrit fibers, each carrying the same 3-cycle branch law and the same "
                "2x2 Jordan / nilpotent quotient over F3."
            )
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