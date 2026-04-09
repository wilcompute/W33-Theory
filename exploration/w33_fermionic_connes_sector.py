"""Spinor-only finite-geometry diagnostics for W(3,3).

This module isolates the fermionic 16 of E6 inside the canonical 27-state
basis, builds the Higgs Yukawa slices from the exact cubic tensor, and applies
an executable Connes-style screen on the left/right chiral split.

The goal here is narrower than a full finite-triple proof:
  - identify the physically relevant 16-spinor sector per generation;
  - construct exact 8x8 left-right Yukawa slices from the cubic tensor;
  - test a concrete weak/color order-zero and order-one diagnostic family;
  - determine which Higgs directions are already compatible with that screen.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from w33_finite_spectral_triple import (
        BasisState,
        GENERATION_COUNT,
        canonical_cubic_tensor_27,
        canonical_generation_basis,
    )
except ModuleNotFoundError:
    from exploration.w33_finite_spectral_triple import (
        BasisState,
        GENERATION_COUNT,
        canonical_cubic_tensor_27,
        canonical_generation_basis,
    )


LEFT_SM_FIELDS = ("Q", "L")
RIGHT_SM_FIELDS = ("u_c", "d_c", "e_c", "nu_c")
HIGGS_SLOT_NAMES = ("H_1", "H_2", "Hbar_1", "Hbar_2")
UPLIKE_HIGGS_SLOT_NAMES = ("H_1", "H_2")
DOWNLIKE_HIGGS_SLOT_NAMES = ("Hbar_1", "Hbar_2")
SPINOR_DIM = 16
LEFT_DIM = 8
RIGHT_DIM = 8
FERMION_MATTER_DIM = GENERATION_COUNT * SPINOR_DIM
FERMION_TOTAL_DIM = 2 * FERMION_MATTER_DIM


@dataclass(frozen=True)
class FermionicConnesSectorCandidate:
    """Packaged spinor-only finite-geometry diagnostic data."""

    generation_spinor_basis: tuple[BasisState, ...]
    left_basis: tuple[BasisState, ...]
    right_basis: tuple[BasisState, ...]
    slot_to_left_right_yukawa: dict[str, np.ndarray]
    clean_higgs_slots: tuple[str, ...]
    weak_generator_names: tuple[str, ...]
    color_generator_names: tuple[str, ...]


def _basis_by_slot() -> dict[str, BasisState]:
    return {state.slot: state for state in canonical_generation_basis()}


@lru_cache(maxsize=1)
def canonical_spinor_basis() -> tuple[BasisState, ...]:
    basis = tuple(
        state
        for state in canonical_generation_basis()
        if state.sector == "spinor"
    )
    if len(basis) != SPINOR_DIM:
        raise ValueError(f"Expected 16 spinor states, found {len(basis)}")
    return basis


@lru_cache(maxsize=1)
def left_spinor_basis() -> tuple[BasisState, ...]:
    basis = tuple(state for state in canonical_spinor_basis() if state.sm in LEFT_SM_FIELDS)
    if len(basis) != LEFT_DIM:
        raise ValueError(f"Expected 8 left-chiral states, found {len(basis)}")
    return basis


@lru_cache(maxsize=1)
def right_spinor_basis() -> tuple[BasisState, ...]:
    basis = tuple(state for state in canonical_spinor_basis() if state.sm in RIGHT_SM_FIELDS)
    if len(basis) != RIGHT_DIM:
        raise ValueError(f"Expected 8 right-chiral states, found {len(basis)}")
    return basis


@lru_cache(maxsize=1)
def spinor_left_indices_27() -> tuple[int, ...]:
    return tuple(state.local_index for state in left_spinor_basis())


@lru_cache(maxsize=1)
def spinor_right_indices_27() -> tuple[int, ...]:
    return tuple(state.local_index for state in right_spinor_basis())


@lru_cache(maxsize=1)
def higgs_indices_27_by_slot() -> dict[str, int]:
    slot_map = _basis_by_slot()
    return {slot: slot_map[slot].local_index for slot in HIGGS_SLOT_NAMES}


@lru_cache(maxsize=1)
def higgs_yukawa_slices_8x8() -> dict[str, np.ndarray]:
    tensor = canonical_cubic_tensor_27()
    left = spinor_left_indices_27()
    right = spinor_right_indices_27()
    slices = {}
    for slot, index in higgs_indices_27_by_slot().items():
        block = tensor[np.ix_(left, right, [index])][:, :, 0]
        slices[slot] = np.rint(block).astype(np.int64)
    return slices


def combined_yukawa_slice_8x8(coefficients: dict[str, complex]) -> np.ndarray:
    """Form a linear combination of the exact Higgs Yukawa slices."""

    total = np.zeros((LEFT_DIM, RIGHT_DIM), dtype=complex)
    for slot, coeff in coefficients.items():
        total += coeff * higgs_yukawa_slices_8x8()[slot]
    return total


def fermionic_dirac_from_yukawa_16(yukawa: np.ndarray) -> np.ndarray:
    """Build the left-right 16x16 Dirac operator from an 8x8 Yukawa block."""

    yukawa = np.asarray(yukawa, dtype=complex)
    if yukawa.shape != (LEFT_DIM, RIGHT_DIM):
        raise ValueError("yukawa must be 8x8")
    zeros = np.zeros((LEFT_DIM, LEFT_DIM), dtype=complex)
    return np.block([[zeros, yukawa], [np.conjugate(yukawa).T, zeros]])


def fermionic_dirac_for_higgs_slot_16(slot: str) -> np.ndarray:
    return fermionic_dirac_from_yukawa_16(higgs_yukawa_slices_8x8()[slot])


def chiral_grading_16() -> np.ndarray:
    return np.diag([1.0] * LEFT_DIM + [-1.0] * RIGHT_DIM)


def weak_generator_16(name: str) -> np.ndarray:
    """Sample weak generator acting on Q and L doublets on the left."""

    generators = {
        "sigma_x": np.array([[0, 1], [1, 0]], dtype=complex),
        "sigma_z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    if name not in generators:
        raise KeyError(f"Unknown weak generator: {name}")

    operator = np.eye(SPINOR_DIM, dtype=complex)
    block = generators[name]
    for start in (0, 2, 4, 6):
        indices = (start, start + 1)
        operator[np.ix_(indices, indices)] = block
    return operator


def color_generator_16(name: str) -> np.ndarray:
    """Sample color generator acting on Q, u_c, and d_c color blocks."""

    generators = {
        "lambda_1": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_3": np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
    }
    if name not in generators:
        raise KeyError(f"Unknown color generator: {name}")

    color = generators[name]
    operator = np.eye(SPINOR_DIM, dtype=complex)
    operator[np.ix_(range(0, 6), range(0, 6))] = np.kron(color, np.eye(2, dtype=complex))
    operator[np.ix_(range(8, 11), range(8, 11))] = np.conjugate(color)
    operator[np.ix_(range(11, 14), range(11, 14))] = np.conjugate(color)
    return operator


def weak_generator_names() -> tuple[str, ...]:
    return ("sigma_x", "sigma_z")


def color_generator_names() -> tuple[str, ...]:
    return ("lambda_1", "lambda_3")


def order_zero_commutator(left_operator: np.ndarray, right_operator: np.ndarray) -> np.ndarray:
    return left_operator @ right_operator - right_operator @ left_operator


def order_one_double_commutator(
    dirac: np.ndarray,
    left_operator: np.ndarray,
    right_operator: np.ndarray,
) -> np.ndarray:
    first = dirac @ left_operator - left_operator @ dirac
    return first @ right_operator - right_operator @ first


def sample_order_zero_residuals() -> dict[tuple[str, str], np.ndarray]:
    residuals = {}
    for weak_name in weak_generator_names():
        for color_name in color_generator_names():
            residuals[(weak_name, color_name)] = order_zero_commutator(
                weak_generator_16(weak_name),
                color_generator_16(color_name),
            )
    return residuals


def sample_order_one_residuals_for_slot(slot: str) -> dict[tuple[str, str], np.ndarray]:
    dirac = fermionic_dirac_for_higgs_slot_16(slot)
    residuals = {}
    for weak_name in weak_generator_names():
        for color_name in color_generator_names():
            residuals[(weak_name, color_name)] = order_one_double_commutator(
                dirac,
                weak_generator_16(weak_name),
                color_generator_16(color_name),
            )
    return residuals


def sample_order_one_residual_norm(slot: str) -> float:
    total = 0.0
    for residual in sample_order_one_residuals_for_slot(slot).values():
        total += float(np.linalg.norm(residual) ** 2)
    return float(np.sqrt(total))


def sample_order_one_residual_map(slot_names: Iterable[str]) -> np.ndarray:
    """Stack sample order-one residual vectors for a family of Higgs slots."""

    columns = []
    for slot in slot_names:
        vectors = []
        for residual in sample_order_one_residuals_for_slot(slot).values():
            vectors.append(residual.reshape(-1))
        columns.append(np.concatenate(vectors))
    return np.stack(columns, axis=1)


def clean_higgs_slots() -> tuple[str, ...]:
    clean = []
    for slot in HIGGS_SLOT_NAMES:
        if np.isclose(sample_order_one_residual_norm(slot), 0.0):
            clean.append(slot)
    return tuple(clean)


@lru_cache(maxsize=1)
def _source_heisenberg_coords() -> dict[int, tuple[tuple[int, int], int]]:
    data = json.loads((ROOT / "artifacts" / "e6_cubic_affine_heisenberg_model.json").read_text(encoding="utf-8"))
    return {
        int(key): (tuple(int(x) for x in value["u"]), int(value["z"]))
        for key, value in data["e6id_to_heisenberg"].items()
    }


def higgs_support_entries(slot: str) -> tuple[dict[str, object], ...]:
    tensor = canonical_cubic_tensor_27()
    left = left_spinor_basis()
    right = right_spinor_basis()
    slot_index = higgs_indices_27_by_slot()[slot]
    coords = _source_heisenberg_coords()

    entries = []
    for i, left_state in enumerate(left):
        for j, right_state in enumerate(right):
            value = int(np.rint(tensor[left_state.local_index, right_state.local_index, slot_index]))
            if value == 0:
                continue
            left_u, left_z = coords[left_state.source_i27]
            right_u, right_z = coords[right_state.source_i27]
            entries.append(
                {
                    "left_slot": left_state.slot,
                    "left_source_i27": left_state.source_i27,
                    "left_u": left_u,
                    "left_z": left_z,
                    "right_slot": right_state.slot,
                    "right_source_i27": right_state.source_i27,
                    "right_u": right_u,
                    "right_z": right_z,
                    "value": value,
                    "same_u": left_u == right_u,
                    "delta_z_mod_3": int((left_z - right_z) % 3),
                }
            )
    return tuple(entries)


def build_clean_higgs_geometry_summary() -> dict[str, object]:
    basis_by_slot = _basis_by_slot()
    coords = _source_heisenberg_coords()
    support = {slot: list(higgs_support_entries(slot)) for slot in HIGGS_SLOT_NAMES}
    clean = clean_higgs_slots()
    clean_support = {slot: support[slot] for slot in clean}

    return {
        "status": "ok",
        "clean_higgs_slots": list(clean),
        "slot_locations": {
            slot: {
                "source_i27": basis_by_slot[slot].source_i27,
                "u": coords[basis_by_slot[slot].source_i27][0],
                "z": coords[basis_by_slot[slot].source_i27][1],
            }
            for slot in HIGGS_SLOT_NAMES
        },
        "yukawa_support_counts": {
            slot: len(entries) for slot, entries in support.items()
        },
        "yukawa_support": support,
        "geometry_theorem": {
            "clean_pair_is_charged_origin_fiber": all(
                coords[basis_by_slot[slot].source_i27][0] == (0, 0)
                and coords[basis_by_slot[slot].source_i27][1] in {1, 2}
                for slot in clean
            ),
            "clean_pair_supports_identical_two_entry_yukawas": (
                len(clean) == 2
                and len(clean_support[clean[0]]) == 2
                and clean_support[clean[0]] == clean_support[clean[1]]
            ),
            "clean_pair_support_is_same_u_and_delta_z_one": all(
                entry["same_u"] and entry["delta_z_mod_3"] == 1
                for slot in clean
                for entry in clean_support[slot]
            ),
            "clean_pair_support_is_exactly_leptonic": (
                {(entry["left_slot"], entry["right_slot"], entry["value"]) for entry in clean_support.get("H_2", [])}
                == {("L_1", "nu_c", -1), ("L_2", "e_c", 1)}
                and {(entry["left_slot"], entry["right_slot"], entry["value"]) for entry in clean_support.get("Hbar_2", [])}
                == {("L_1", "nu_c", -1), ("L_2", "e_c", 1)}
            ),
            "nonclean_pair_is_more_diffuse": all(
                len(support[slot]) > len(clean_support[clean[0]]) for slot in HIGGS_SLOT_NAMES if slot not in clean
            ),
        },
    }


@lru_cache(maxsize=1)
def build_fermionic_connes_sector_candidate() -> FermionicConnesSectorCandidate:
    return FermionicConnesSectorCandidate(
        generation_spinor_basis=canonical_spinor_basis(),
        left_basis=left_spinor_basis(),
        right_basis=right_spinor_basis(),
        slot_to_left_right_yukawa=higgs_yukawa_slices_8x8(),
        clean_higgs_slots=clean_higgs_slots(),
        weak_generator_names=weak_generator_names(),
        color_generator_names=color_generator_names(),
    )


def main() -> None:
    summary = build_clean_higgs_geometry_summary()
    print("W33 FERMIONIC CONNES SECTOR")
    print("=" * 72)
    print(f"clean Higgs slots: {summary['clean_higgs_slots']}")
    for slot, loc in summary["slot_locations"].items():
        print(f"{slot}: source_i27={loc['source_i27']} u={tuple(loc['u'])} z={loc['z']} support={summary['yukawa_support_counts'][slot]}")
    print("geometry theorem:")
    for key, value in summary["geometry_theorem"].items():
        print(f"  {key}: {value}")
    for slot in summary["clean_higgs_slots"]:
        print(f"{slot} support: {summary['yukawa_support'][slot]}")


if __name__ == "__main__":
    main()
