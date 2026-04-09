"""Mod-3 qutrit collapse of the reduced Yukawa generation algebra.

This module packages a sharper identification of the exact Yukawa generation
packet already isolated elsewhere in the repo.

What is established here:
  - the two universal 3x3 generation matrices reduce modulo 3 to nontrivial
    order-3 operators, with C_- = C_+^2, so they generate one cyclic C3;
  - over F3, that cyclic packet is not an arbitrary unipotent algebra: it is
    conjugate to the regular translation action of the 3-cycle permutation on
    the three generation labels;
  - under this conjugacy, the repo's common line/plane flag becomes the
        fixed line <(1,1,1)>  contained in  the augmentation plane
        {x0 + x1 + x2 = 0}
    of the regular F3[C3]-module;
  - over C, the same permutation packet diagonalizes by the discrete Fourier
    transform with eigenvalues 1, omega, omega^2.

So the exact one-versus-two family flag is the characteristic-3 collapse of
the semisimple qutrit packet, not a separate ad hoc family structure.
"""

from __future__ import annotations

from functools import lru_cache
import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from exploration._artifact_paths import load_json_from_repo_data


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_qutrit_collapse_bridge_summary.json"
FIELD_PRIME = 3

PERMUTATION_CYCLE = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=int,
)
ONES_VECTOR = np.array([1, 1, 1], dtype=int)
CANONICAL_AUGMENTATION_BASIS = np.array(
    [
        [2, 0],
        [1, 2],
        [0, 1],
    ],
    dtype=int,
)


def _read_json(filename: str) -> dict[str, Any]:
    return load_json_from_repo_data(ROOT, Path("data") / filename)


def _mod3(matrix: np.ndarray) -> np.ndarray:
    return np.mod(matrix, FIELD_PRIME).astype(int)


def _mod3_eye() -> np.ndarray:
    return np.eye(3, dtype=int) % FIELD_PRIME


def _mat_pow_mod3(matrix: np.ndarray, power: int) -> np.ndarray:
    result = _mod3_eye()
    base = _mod3(matrix)
    for _ in range(power):
        result = _mod3(result @ base)
    return result


def _matrix_rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix.astype(float)))


def _find_intertwiner_to_cycle(
    generator_mod3: np.ndarray,
    line_vector_mod3: np.ndarray,
) -> np.ndarray:
    target = PERMUTATION_CYCLE
    for entries in itertools.product(range(FIELD_PRIME), repeat=9):
        candidate = np.array(entries, dtype=int).reshape(3, 3)
        if round(np.linalg.det(candidate)) % FIELD_PRIME == 0:
            continue
        if not np.array_equal(_mod3(target @ candidate), _mod3(candidate @ generator_mod3)):
            continue
        if not np.array_equal(_mod3(candidate @ line_vector_mod3), ONES_VECTOR):
            continue
        return candidate
    raise RuntimeError("failed to find mod-3 intertwiner to the cyclic permutation model")


def _invert_mod3(matrix: np.ndarray) -> np.ndarray:
    identity = _mod3_eye()
    for entries in itertools.product(range(FIELD_PRIME), repeat=9):
        candidate = np.array(entries, dtype=int).reshape(3, 3)
        if np.array_equal(_mod3(matrix @ candidate), identity) and np.array_equal(
            _mod3(candidate @ matrix), identity
        ):
            return candidate
    raise RuntimeError("failed to invert matrix over F3")


def _span_equals_mod3(left: np.ndarray, right: np.ndarray) -> bool:
    def span_set(columns: np.ndarray) -> set[tuple[int, ...]]:
        output: set[tuple[int, ...]] = set()
        for coeffs in itertools.product(range(FIELD_PRIME), repeat=columns.shape[1]):
            vector = np.zeros(columns.shape[0], dtype=int)
            for coeff, column in zip(coeffs, columns.T):
                vector = _mod3(vector + coeff * column)
            output.add(tuple(int(value) for value in vector))
        return output

    return span_set(left) == span_set(right)


def _dft_qutrit_packet() -> dict[str, Any]:
    omega = np.exp(2j * np.pi / 3)
    fourier = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega * omega, omega],
            [1.0, omega, omega * omega],
        ],
        dtype=complex,
    )
    inverse = np.conjugate(fourier).T / 3.0
    diagonal = inverse @ PERMUTATION_CYCLE.astype(complex) @ fourier
    eigenvalues = np.diag(diagonal)
    expected = np.array([1.0, omega, omega * omega], dtype=complex)
    return {
        "fourier_diagonalization_matches_qutrit_eigenbasis": bool(
            np.allclose(diagonal, np.diag(eigenvalues), atol=1e-10)
            and np.allclose(
                np.sort_complex(eigenvalues),
                np.sort_complex(expected),
                atol=1e-10,
            )
        ),
        "complex_eigenvalues": [
            [float(value.real), float(value.imag)] for value in eigenvalues
        ],
    }


@lru_cache(maxsize=1)
def build_yukawa_qutrit_collapse_summary() -> dict[str, Any]:
    unipotent = _read_json("w33_yukawa_unipotent_reduction_bridge_summary.json")
    flag = _read_json("w33_yukawa_generation_flag_bridge_summary.json")

    algebra = unipotent["universal_generation_algebra"]
    common_flag = flag["common_flag"]

    c_plus = np.array(algebra["plus_minus_generation_matrix"], dtype=int)
    c_minus = np.array(algebra["minus_plus_generation_matrix"], dtype=int)
    line_vector = np.array(common_flag["line_generator"], dtype=int)
    plane_basis = np.array(common_flag["plane_basis"], dtype=int).T

    c_plus_mod3 = _mod3(c_plus)
    c_minus_mod3 = _mod3(c_minus)
    intertwiner = _find_intertwiner_to_cycle(c_plus_mod3, _mod3(line_vector))
    intertwiner_inverse = _invert_mod3(intertwiner)

    plane_in_cycle_basis = _mod3(intertwiner @ plane_basis)
    permutation_nilpotent = _mod3(PERMUTATION_CYCLE - _mod3_eye())

    dft_packet = _dft_qutrit_packet()

    return {
        "status": "ok",
        "field_prime": FIELD_PRIME,
        "mod3_generation_packet": {
            "plus_generator": c_plus_mod3.tolist(),
            "minus_generator": c_minus_mod3.tolist(),
            "cycle_permutation_generator": PERMUTATION_CYCLE.tolist(),
            "intertwiner_to_cycle_basis": intertwiner.tolist(),
            "intertwiner_inverse": intertwiner_inverse.tolist(),
            "plus_generator_order_3": bool(
                np.array_equal(_mat_pow_mod3(c_plus_mod3, 3), _mod3_eye())
                and not np.array_equal(c_plus_mod3, _mod3_eye())
            ),
            "minus_generator_order_3": bool(
                np.array_equal(_mat_pow_mod3(c_minus_mod3, 3), _mod3_eye())
                and not np.array_equal(c_minus_mod3, _mod3_eye())
            ),
            "minus_equals_plus_squared_mod3": bool(
                np.array_equal(_mat_pow_mod3(c_plus_mod3, 2), c_minus_mod3)
            ),
            "plus_and_minus_generate_same_c3": bool(
                np.array_equal(_mod3(c_plus_mod3 @ c_minus_mod3), _mod3_eye())
            ),
            "cycle_conjugacy_is_exact": bool(
                np.array_equal(
                    _mod3(intertwiner_inverse @ PERMUTATION_CYCLE @ intertwiner),
                    c_plus_mod3,
                )
            ),
        },
        "mod3_flag_identification": {
            "repo_line_generator": _mod3(line_vector).tolist(),
            "repo_plane_basis": _mod3(plane_basis).T.tolist(),
            "line_in_cycle_basis": _mod3(intertwiner @ line_vector).tolist(),
            "plane_in_cycle_basis": plane_in_cycle_basis.T.tolist(),
            "cycle_fixed_line_generator": ONES_VECTOR.tolist(),
            "canonical_augmentation_basis": CANONICAL_AUGMENTATION_BASIS.tolist(),
            "permutation_nilpotent": permutation_nilpotent.tolist(),
            "line_maps_to_fixed_line": bool(
                np.array_equal(_mod3(intertwiner @ line_vector), ONES_VECTOR)
            ),
            "plane_maps_to_augmentation_plane": bool(
                _span_equals_mod3(plane_in_cycle_basis, CANONICAL_AUGMENTATION_BASIS)
            ),
            "fixed_line_equals_kernel_of_cycle_minus_identity": bool(
                np.array_equal(_mod3(permutation_nilpotent @ ONES_VECTOR), np.zeros(3, dtype=int))
            ),
            "augmentation_plane_equals_image_of_cycle_minus_identity": bool(
                _span_equals_mod3(
                    _mod3(permutation_nilpotent),
                    CANONICAL_AUGMENTATION_BASIS,
                )
            ),
            "fixed_line_is_contained_in_augmentation_plane": bool(
                _span_equals_mod3(
                    np.column_stack([ONES_VECTOR, plane_in_cycle_basis]),
                    plane_in_cycle_basis,
                )
            ),
        },
        "semisimple_qutrit_packet": dft_packet,
        "qutrit_collapse_theorem": {
            "universal_generation_algebra_reduces_to_one_c3_mod3": bool(
                np.array_equal(_mat_pow_mod3(c_plus_mod3, 2), c_minus_mod3)
                and np.array_equal(_mat_pow_mod3(c_plus_mod3, 3), _mod3_eye())
            ),
            "mod3_generation_module_is_regular_c3_module": bool(
                np.array_equal(
                    _mod3(intertwiner_inverse @ PERMUTATION_CYCLE @ intertwiner),
                    c_plus_mod3,
                )
            ),
            "repo_common_flag_matches_loewy_flag_of_regular_module": bool(
                np.array_equal(_mod3(intertwiner @ line_vector), ONES_VECTOR)
                and _span_equals_mod3(plane_in_cycle_basis, CANONICAL_AUGMENTATION_BASIS)
            ),
            "complex_regular_module_splits_as_qutrit_packet": bool(
                dft_packet["fourier_diagonalization_matches_qutrit_eigenbasis"]
            ),
        },
        "bridge_verdict": (
            "The exact reduced Yukawa generation algebra is not merely an "
            "integer unipotent normal form. Modulo 3 it is the regular C3 "
            "generation-translation module, and the repo's common line/plane "
            "flag is exactly its fixed-line-inside-augmentation-plane Loewy "
            "flag. Over C the same cyclic packet splits into the qutrit "
            "eigencharacters 1, omega, omega^2. So the exact one-versus-two "
            "family structure is the characteristic-3 collapse of the same "
            "qutrit object already visible on the local W33 side."
        ),
        "source_files": [
            "data/w33_yukawa_unipotent_reduction_bridge_summary.json",
            "data/w33_yukawa_generation_flag_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_qutrit_collapse_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
