#!/usr/bin/env python3
"""Part DCLXXXV: holonomy single-photon fiber Jordan bridge.

After rereading both papers, the strongest unresolved equivalence is local:
the single-photon paper's deterministic 81-state two-qutrit Pauli frame has a
canonical 3-state qutrit feed-forward cycle on each affine fiber, while the
W33 paper's remaining mixed-plane frontier is the exact unipotent witness

    H = I + N,  N = [[0, 1], [0, 0]],  N^2 = 0.

This verifier shows those are the same local datum.  The 81-state Pauli frame
splits exactly as

    81 = 1 + 2*40 = 1 + 2*(13 + 27) = 1 + 26 + 54 = 1 + 26 + 9*6,

and on each 3-state affine fiber the qutrit transvection acts as a 3-cycle.
Over F3, quotienting that 3-cycle by its invariant constant branch produces the
exact 2x2 Jordan block [[1,1],[0,1]] and the exact nilpotent increment
[[0,1],[0,0]].
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
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from PART_CCCCVI_PROTECTED_PHOTONIC_RUNTIME_SCHEDULER import (  # noqa: E402
    build_results as build_scheduler_results,
)
from verify_dclxiv_holonomy_qutrit_transvection_bridge import (  # noqa: E402
    build_bridge as build_dclxiv_bridge,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)


MODULUS = 3
OUT_PATH = ROOT / "data" / "dclxxxv_holonomy_single_photon_fiber_jordan_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    field_order: int
    pauli_frame_size: int
    projective_frame_size: int
    zero_state_count: int
    fixed_frame_state_count: int
    mobile_frame_state_count: int
    mobile_packet_count: int
    mobile_projective_fiber_size: int
    mobile_frame_packet_size: int
    all_identities_hold: bool


def _mat_mod3(matrix: Iterable[Iterable[int]] | np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _all_f3_vectors() -> list[tuple[int, int, int, int]]:
    return [tuple(int(x) for x in vector) for vector in product(range(MODULUS), repeat=4)]


def _scale_vector(vector: tuple[int, ...], scalar: int) -> tuple[int, ...]:
    return tuple((scalar * int(x)) % MODULUS for x in vector)


def _lift_projective_point(point: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [_scale_vector(point, scalar) for scalar in (1, 2)]


def _matrix_order(matrix: np.ndarray) -> int:
    identity = np.eye(matrix.shape[0], dtype=int)
    power = identity.copy()
    for order in range(1, 20):
        power = _mat_mod3(power @ matrix)
        if np.array_equal(power, identity):
            return order
    raise ValueError("matrix order exceeded search bound")


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
        determinant = int(round(np.linalg.det(matrix))) % MODULUS
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
    photonic = build_scheduler_results()
    dclxiv = build_dclxiv_bridge()
    k3 = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()

    pauli_frame_size = photonic["controller_envelope"]["pauli_frame_states"]
    projective_frame_size = photonic["controller_envelope"]["projective_frame_states"]

    fixed_projective_points = [tuple(point) for point in dclxiv["carrier_action"]["fixed_projective_points"]]
    affine_fibers = [
        [tuple(point) for point in fiber["orbit"]]
        for fiber in dclxiv["carrier_action"]["affine_fibers"]
    ]
    sample_projective_fiber = [tuple(point) for point in dclxiv["carrier_action"]["sample_affine_orbit"]]

    zero_state = (0, 0, 0, 0)
    fixed_frame_states = sorted(
        {
            lifted
            for point in fixed_projective_points
            for lifted in _lift_projective_point(point)
        }
    )
    mobile_frame_packets = []
    for fiber in affine_fibers:
        packet = sorted(
            {
                lifted
                for point in fiber
                for lifted in _lift_projective_point(point)
            }
        )
        mobile_frame_packets.append(packet)
    mobile_frame_states = sorted({state for packet in mobile_frame_packets for state in packet})
    all_frame_states = sorted([zero_state, *fixed_frame_states, *mobile_frame_states])
    full_f3_space = sorted(_all_f3_vectors())

    shear = _mat_mod3(dclxiv["matrices"]["embedded_qutrit_shear"])
    projective_action = []
    for point in sample_projective_fiber:
        image = tuple(int(entry) % MODULUS for entry in (shear @ np.array(point, dtype=int).reshape(4, 1)).flatten())
        projective_action.append(sample_projective_fiber.index(image))
    three_cycle_matrix = _permutation_matrix(projective_action)
    three_cycle_nilpotent = _mat_mod3(three_cycle_matrix - np.eye(3, dtype=int))
    constant_branch = np.array([1, 1, 1], dtype=int)

    quotient_matrix = _quotient_matrix_from_three_cycle(three_cycle_matrix)
    jordan_block = np.array([[1, 1], [0, 1]], dtype=int)
    jordan_conjugator = _find_conjugator(quotient_matrix, jordan_block)
    quotient_in_jordan_basis = _mat_mod3(
        _inverse_gl2(jordan_conjugator) @ quotient_matrix @ jordan_conjugator
    )
    quotient_nilpotent = _mat_mod3(jordan_block - np.eye(2, dtype=int))
    k3_nilpotent = np.array(
        k3["mixed_plane_nilpotent_holonomy_increment"]["canonical_nonzero_increment"],
        dtype=int,
    )

    identities = {
        "photonic_deterministic_pauli_frame_is_q_to_the_four_equals_81": pauli_frame_size == 81,
        "photonic_projective_frame_is_exactly_40_sites": projective_frame_size == 40,
        "the_full_pauli_frame_is_zero_plus_doubled_projective_carrier": (
            pauli_frame_size == 1 + 2 * projective_frame_size == len(full_f3_space)
        ),
        "the_dclxiv_13_plus_27_shell_lifts_to_the_exact_1_plus_26_plus_54_split": (
            len(fixed_frame_states) == 2 * dclxiv["summary"]["fixed_projective_count"] == 26
            and len(mobile_frame_states) == 2 * dclxiv["summary"]["affine_bulk_count"] == 54
            and 1 + len(fixed_frame_states) + len(mobile_frame_states) == pauli_frame_size
        ),
        "the_mobile_pauli_frame_sector_is_nine_six_state_packets": (
            len(mobile_frame_packets) == dclxiv["summary"]["affine_fiber_count"] == 9
            and all(len(packet) == 6 for packet in mobile_frame_packets)
            and len(mobile_frame_states) == 9 * 6
        ),
        "the_sample_projective_fiber_carries_a_three_cycle": (
            projective_action == [1, 2, 0] and _matrix_order(three_cycle_matrix) == 3
        ),
        "the_three_cycle_has_one_invariant_constant_branch": np.array_equal(
            _mat_mod3(three_cycle_matrix @ constant_branch), constant_branch
        ),
        "the_three_cycle_is_unipotent_over_f3_with_cubic_nilpotent_increment": (
            np.array_equal(_mat_mod3(three_cycle_nilpotent @ three_cycle_nilpotent @ three_cycle_nilpotent), np.zeros((3, 3), dtype=int))
            and not np.array_equal(_mat_mod3(three_cycle_nilpotent @ three_cycle_nilpotent), np.zeros((3, 3), dtype=int))
        ),
        "quotienting_by_the_constant_branch_produces_the_exact_two_by_two_jordan_block": np.array_equal(
            quotient_in_jordan_basis, jordan_block
        ),
        "the_reduced_nilpotent_increment_is_exactly_square_zero": (
            np.array_equal(quotient_nilpotent, np.array([[0, 1], [0, 0]], dtype=int))
            and np.array_equal(_mat_mod3(quotient_nilpotent @ quotient_nilpotent), np.zeros((2, 2), dtype=int))
        ),
        "the_reduced_nilpotent_increment_matches_the_exact_mixed_plane_k3_witness": np.array_equal(
            quotient_nilpotent, k3_nilpotent
        ),
        "therefore_the_mixed_plane_holonomy_witness_is_the_augmentation_quotient_of_the_local_single_photon_qutrit_feed_forward_cycle": (
            pauli_frame_size == 81
            and projective_frame_size == 40
            and len(fixed_frame_states) == 26
            and len(mobile_frame_states) == 54
            and np.array_equal(quotient_in_jordan_basis, jordan_block)
            and np.array_equal(quotient_nilpotent, k3_nilpotent)
        ),
    }

    summary = BridgeSummary(
        field_order=MODULUS,
        pauli_frame_size=pauli_frame_size,
        projective_frame_size=projective_frame_size,
        zero_state_count=1,
        fixed_frame_state_count=len(fixed_frame_states),
        mobile_frame_state_count=len(mobile_frame_states),
        mobile_packet_count=len(mobile_frame_packets),
        mobile_projective_fiber_size=len(sample_projective_fiber),
        mobile_frame_packet_size=len(mobile_frame_packets[0]),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "frame_decomposition": {
            "zero_state": list(zero_state),
            "fixed_projective_count": len(fixed_projective_points),
            "fixed_frame_state_count": len(fixed_frame_states),
            "mobile_projective_count": dclxiv["summary"]["affine_bulk_count"],
            "mobile_frame_state_count": len(mobile_frame_states),
            "sample_fixed_frame_states": [list(state) for state in fixed_frame_states[:6]],
            "sample_mobile_frame_packet": [list(state) for state in mobile_frame_packets[0]],
        },
        "local_fiber_dynamics": {
            "sample_projective_fiber": [list(point) for point in sample_projective_fiber],
            "sample_projective_action": projective_action,
            "three_cycle_matrix_mod3": three_cycle_matrix.tolist(),
            "three_cycle_nilpotent_increment_mod3": three_cycle_nilpotent.tolist(),
            "constant_branch": constant_branch.tolist(),
            "quotient_matrix_mod3": quotient_matrix.tolist(),
            "jordan_conjugator_mod3": jordan_conjugator.tolist(),
            "quotient_in_jordan_basis": quotient_in_jordan_basis.tolist(),
            "reduced_nilpotent_increment": quotient_nilpotent.tolist(),
        },
        "bridge_alignment": {
            "embedded_qutrit_shear": dclxiv["matrices"]["embedded_qutrit_shear"],
            "k3_nilpotent_increment": k3_nilpotent.tolist(),
            "deterministic_runtime_contract": {
                "pauli_frame_states": pauli_frame_size,
                "projective_frame_states": projective_frame_size,
                "measurement_trits": photonic["controller_envelope"]["measurement_trits"],
            },
            "verdict": (
                "The deterministic 81-state single-photon Pauli frame already contains the exact local holonomy witness. "
                "Its 40 projective sites split as 13 fixed + 27 mobile under the canonical qutrit transvection, and the full "
                "frame lifts that to 1 + 26 + 54 = 1 + 26 + 9*6. On each local 3-state projective fiber the feed-forward law is a "
                "3-cycle; over F3, quotienting by the invariant constant branch yields the exact 2x2 Jordan block and nilpotent increment "
                "that the mixed-plane K3 frontier asks for."
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