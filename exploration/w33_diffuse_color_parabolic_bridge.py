"""Diffuse color-support algebra for the W(3,3) Higgs Yukawa packet.

This script identifies the exact color-support algebra seen by the two diffuse
Higgs combinations

    D_plus  = H_1 + Hbar_1
    D_minus = H_1 - Hbar_1.

The main result is sharper than the earlier residual-only obstruction:

  - both diffuse lines are exact for the full weak Pauli triple;
  - neither line is exact for the tested nontrivial Gell-Mann generators;
  - nevertheless, each line carries a 7-dimensional exact color-support
    algebra;
  - that exact algebra is precisely the parabolic line stabilizer
        { M in M_3(C) : M s in <s> }
    of the sign vector s = (1,-1,1).

So the surviving diffuse obstruction is not "no color structure at all" but
"not the full SU(3) packet in the current canonical basis".
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_fermionic_connes_sector import higgs_yukawa_slices_8x8


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_diffuse_color_parabolic_bridge_summary.json"


def _left_pauli_generators() -> dict[str, np.ndarray]:
    pauli_2 = {
        "sigma_x": np.array([[0, 1], [1, 0]], dtype=complex),
        "sigma_y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "sigma_z": np.array([[1, 0], [0, -1]], dtype=complex),
    }
    generators = {}
    for name, block in pauli_2.items():
        operator = np.zeros((8, 8), dtype=complex)
        for start in (0, 2, 4, 6):
            operator[np.ix_((start, start + 1), (start, start + 1))] = block
        generators[name] = operator
    return generators


def _left_color_operator(matrix_3: np.ndarray) -> np.ndarray:
    operator = np.zeros((8, 8), dtype=complex)
    operator[:6, :6] = np.kron(np.asarray(matrix_3, dtype=complex), np.eye(2, dtype=complex))
    return operator


def _color_gell_mann_generators() -> dict[str, np.ndarray]:
    return {
        "lambda_1": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_2": np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_3": np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        "lambda_8": np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
    }


def _best_right_intertwiner(left_operator: np.ndarray, yukawa: np.ndarray) -> tuple[np.ndarray, float]:
    rows = []
    rhs = []
    for left_index in range(8):
        for right_index in range(8):
            coeff = np.zeros(64, dtype=complex)
            for inner in range(8):
                coeff[inner * 8 + right_index] = -yukawa[left_index, inner]
            rows.append(coeff)
            rhs.append(-(left_operator @ yukawa)[left_index, right_index])
    matrix = np.stack(rows, axis=0)
    target = np.array(rhs, dtype=complex)
    solution, _, _, _ = np.linalg.lstsq(matrix, target, rcond=None)
    right_operator = solution.reshape(8, 8)
    residual = float(np.linalg.norm(left_operator @ yukawa - yukawa @ right_operator))
    return right_operator, residual


def _diffuse_lines() -> dict[str, np.ndarray]:
    slices = higgs_yukawa_slices_8x8()
    return {
        "diffuse_plus": slices["H_1"].astype(complex) + slices["Hbar_1"].astype(complex),
        "diffuse_minus": slices["H_1"].astype(complex) - slices["Hbar_1"].astype(complex),
    }


def _sign_vector_from_diffuse_line(yukawa: np.ndarray) -> np.ndarray:
    # On both diffuse lines, the quark-to-lepton block is controlled by the same
    # color sign vector read from the e_c column on Q_{*,1}.
    vector = np.array(
        [
            yukawa[0, 6].real,
            yukawa[2, 6].real,
            yukawa[4, 6].real,
        ],
        dtype=float,
    )
    if np.linalg.norm(vector) == 0.0:
        raise ValueError("Diffuse sign vector unexpectedly vanished")
    return vector


def _exact_color_left_subspace_dimension(yukawa: np.ndarray) -> int:
    basis = []
    for a in range(3):
        for b in range(3):
            matrix_3 = np.zeros((3, 3), dtype=complex)
            matrix_3[a, b] = 1.0
            basis.append(_left_color_operator(matrix_3))

    equations = []
    for left_index in range(8):
        for right_index in range(8):
            row = np.zeros(len(basis) + 64, dtype=complex)
            for basis_index, left_operator in enumerate(basis):
                row[basis_index] = (left_operator @ yukawa)[left_index, right_index]
            for inner in range(8):
                row[len(basis) + inner * 8 + right_index] -= yukawa[left_index, inner]
            equations.append(row)

    matrix = np.stack(equations, axis=0)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(singular_values > 1e-9))
    nullspace = vh[rank:].conj().T
    left_projection = nullspace[: len(basis), :]
    _, left_singular_values, _ = np.linalg.svd(left_projection, full_matrices=False)
    return int(np.sum(left_singular_values > 1e-9))


def _line_stabilizer_basis(sign_vector: np.ndarray) -> dict[str, np.ndarray]:
    e1 = np.array([1.0, 0.0, 0.0])
    e2 = np.array([0.0, 1.0, 0.0])
    e3 = np.array([0.0, 0.0, 1.0])
    columns = {
        "lambda_s": np.column_stack([np.zeros(3), np.zeros(3), sign_vector]),
        "c1_e1": np.column_stack([e1, np.zeros(3), -e1]),
        "c1_e2": np.column_stack([e2, np.zeros(3), -e2]),
        "c1_e3": np.column_stack([e3, np.zeros(3), -e3]),
        "c2_e1": np.column_stack([np.zeros(3), e1, e1]),
        "c2_e2": np.column_stack([np.zeros(3), e2, e2]),
        "c2_e3": np.column_stack([np.zeros(3), e3, e3]),
    }
    return columns


def _random_stabilizer_samples(sign_vector: np.ndarray, count: int = 8) -> list[np.ndarray]:
    rng = np.random.default_rng(0)
    samples = []
    for _ in range(count):
        column_1 = rng.normal(size=3)
        column_2 = rng.normal(size=3)
        lam = float(rng.normal())
        column_3 = lam * sign_vector - column_1 + column_2
        samples.append(np.column_stack([column_1, column_2, column_3]))
    return samples


def build_summary() -> dict[str, Any]:
    diffuse = _diffuse_lines()
    sign_vector = _sign_vector_from_diffuse_line(diffuse["diffuse_plus"])
    stabilizer_basis = _line_stabilizer_basis(sign_vector)

    weak_residuals: dict[str, Any] = {}
    for line_name, yukawa in diffuse.items():
        weak_residuals[line_name] = {}
        for generator_name, generator in _left_pauli_generators().items():
            _, residual = _best_right_intertwiner(generator, yukawa)
            weak_residuals[line_name][generator_name] = residual

    tested_color_residuals: dict[str, Any] = {}
    for line_name, yukawa in diffuse.items():
        tested_color_residuals[line_name] = {}
        for generator_name, matrix_3 in _color_gell_mann_generators().items():
            _, residual = _best_right_intertwiner(_left_color_operator(matrix_3), yukawa)
            tested_color_residuals[line_name][generator_name] = residual

    stabilizer_basis_residuals: dict[str, Any] = {}
    for line_name, yukawa in diffuse.items():
        stabilizer_basis_residuals[line_name] = {}
        for basis_name, matrix_3 in stabilizer_basis.items():
            _, residual = _best_right_intertwiner(_left_color_operator(matrix_3), yukawa)
            stabilizer_basis_residuals[line_name][basis_name] = residual

    random_stabilizer_residuals: dict[str, list[float]] = {}
    for line_name, yukawa in diffuse.items():
        random_stabilizer_residuals[line_name] = []
        for matrix_3 in _random_stabilizer_samples(sign_vector):
            _, residual = _best_right_intertwiner(_left_color_operator(matrix_3), yukawa)
            random_stabilizer_residuals[line_name].append(residual)

    color_subspace_dimensions = {
        line_name: _exact_color_left_subspace_dimension(yukawa)
        for line_name, yukawa in diffuse.items()
    }

    return {
        "status": "ok",
        "sign_vector": sign_vector.tolist(),
        "weak_residuals": weak_residuals,
        "tested_color_residuals": tested_color_residuals,
        "exact_color_left_subspace_dimensions": color_subspace_dimensions,
        "stabilizer_basis": {
            name: matrix.tolist() for name, matrix in stabilizer_basis.items()
        },
        "stabilizer_basis_residuals": stabilizer_basis_residuals,
        "random_stabilizer_residuals": random_stabilizer_residuals,
        "diffuse_color_parabolic_theorem": {
            "diffuse_plus_is_weak_exact_for_all_three_pauli_generators": all(
                residual < 1e-12 for residual in weak_residuals["diffuse_plus"].values()
            ),
            "diffuse_minus_is_weak_exact_for_all_three_pauli_generators": all(
                residual < 1e-12 for residual in weak_residuals["diffuse_minus"].values()
            ),
            "tested_nontrivial_gell_mann_generators_are_not_exact": all(
                residual > 1.0
                for line_data in tested_color_residuals.values()
                for residual in line_data.values()
            ),
            "each_diffuse_line_has_exact_color_support_dimension_seven": all(
                dimension == 7 for dimension in color_subspace_dimensions.values()
            ),
            "the_line_stabilizer_basis_is_exact_for_both_diffuse_lines": all(
                residual < 1e-12
                for line_data in stabilizer_basis_residuals.values()
                for residual in line_data.values()
            ),
            "random_line_stabilizer_samples_are_exact_for_both_diffuse_lines": all(
                residual < 1e-10
                for line_data in random_stabilizer_residuals.values()
                for residual in line_data
            ),
            "the_exact_diffuse_color_algebra_equals_the_parabolic_line_stabilizer": all(
                dimension == 7 for dimension in color_subspace_dimensions.values()
            )
            and all(
                residual < 1e-12
                for line_data in stabilizer_basis_residuals.values()
                for residual in line_data.values()
            ),
        },
        "interpretive_read": (
            "The diffuse Higgs lines do not lose color completely. They lose the "
            "full SU(3) packet and retain exactly the 7-dimensional parabolic "
            "stabilizer of the sign line s = (1,-1,1). Equivalently, the current "
            "canonical diffuse color algebra is the line-preserving subalgebra "
            "{M : M s in <s>}. This explains why the standard nontrivial Gell-Mann "
            "generators fail while many structured color operators remain exact."
        ),
        "source_files": [
            "exploration/w33_fermionic_connes_sector.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
