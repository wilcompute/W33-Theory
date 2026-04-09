"""Exact weak-intertwiner diagnostics for the W(3,3) Higgs Yukawa packet.

This script sharpens the local finite-triple story at the first place where the
exact cubic tensor really bites: the spinor-spinor-vector Yukawa slices.

What is shown here:
  - the four Higgs-labelled Yukawa slices span only a 3-dimensional space;
  - the exact kernel is H_2 - Hbar_2, so the clean pair is duplicated;
  - the clean slice is an exact SU(2) intertwiner between the left lepton
    doublet and a right 2-state packet on (e_c, nu_c);
  - the diffuse slices H_1, Hbar_1 carry only the weak Cartan weight exactly
    and fail the non-Cartan generators with a fixed positive obstruction.

This is a stronger and more honest statement than "the blocks look right":
the clean channel is exact, while the diffuse channel is not yet a full weak
doublet in the current canonical basis.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_clean_weak_intertwiner_bridge_summary.json"
SLOT_ORDER = ("H_1", "H_2", "Hbar_1", "Hbar_2")
LEFT_LEPTON_INDICES = (6, 7)
RIGHT_LEPTON_INDICES = (6, 7)


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


def _left_color_generators() -> dict[str, np.ndarray]:
    gell_mann_3 = {
        "lambda_1": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_2": np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_3": np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        "lambda_8": np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3),
    }
    generators = {}
    for name, block in gell_mann_3.items():
        operator = np.zeros((8, 8), dtype=complex)
        operator[:6, :6] = np.kron(block, np.eye(2, dtype=complex))
        generators[name] = operator
    return generators


def _slice_span_diagnostics() -> dict[str, Any]:
    slices = higgs_yukawa_slices_8x8()
    matrix = np.stack([slices[slot].reshape(-1) for slot in SLOT_ORDER], axis=1)
    _, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(singular_values > 1e-9))
    h2_minus_hbar2 = float(np.linalg.norm(slices["H_2"] - slices["Hbar_2"]))
    gram = matrix.conj().T @ matrix
    return {
        "slot_order": list(SLOT_ORDER),
        "singular_values": [float(value) for value in singular_values],
        "rank": rank,
        "h2_minus_hbar2_norm": h2_minus_hbar2,
        "gram_matrix": [[float(value.real) for value in row] for row in gram],
    }


def _best_right_intertwiner(left_generator: np.ndarray, yukawa: np.ndarray) -> tuple[np.ndarray, float]:
    rows = []
    rhs = []
    for left_index in range(8):
        for right_index in range(8):
            coeff = np.zeros(64, dtype=complex)
            for inner in range(8):
                coeff[inner * 8 + right_index] = -yukawa[left_index, inner]
            rows.append(coeff)
            rhs.append(-(left_generator @ yukawa)[left_index, right_index])
    matrix = np.stack(rows, axis=0)
    target = np.array(rhs, dtype=complex)
    solution, _, _, _ = np.linalg.lstsq(matrix, target, rcond=None)
    right_generator = solution.reshape(8, 8)
    residual = float(np.linalg.norm(left_generator @ yukawa - yukawa @ right_generator))
    return right_generator, residual


def _slot_intertwiner_diagnostics() -> dict[str, Any]:
    slices = {slot: higgs_yukawa_slices_8x8()[slot].astype(complex) for slot in SLOT_ORDER}
    diagnostics: dict[str, Any] = {}
    for generator_name, left_generator in _left_pauli_generators().items():
        diagnostics[generator_name] = {}
        for slot, yukawa in slices.items():
            right_generator, residual = _best_right_intertwiner(left_generator, yukawa)
            diagnostics[generator_name][slot] = {
                "residual_norm": residual,
                "right_leptonic_block": [
                    [complex(value) for value in row]
                    for row in right_generator[np.ix_(RIGHT_LEPTON_INDICES, RIGHT_LEPTON_INDICES)]
                ],
            }
    return diagnostics


def _slot_color_intertwiner_diagnostics() -> dict[str, Any]:
    slices = {slot: higgs_yukawa_slices_8x8()[slot].astype(complex) for slot in SLOT_ORDER}
    diagnostics: dict[str, Any] = {}
    for generator_name, left_generator in _left_color_generators().items():
        diagnostics[generator_name] = {}
        for slot, yukawa in slices.items():
            _, residual = _best_right_intertwiner(left_generator, yukawa)
            diagnostics[generator_name][slot] = {"residual_norm": residual}
    return diagnostics


def _clean_pair_symplectic_bridge() -> dict[str, Any]:
    clean_slice = higgs_yukawa_slices_8x8()["H_2"].astype(complex)
    j_matrix = clean_slice[np.ix_(LEFT_LEPTON_INDICES, RIGHT_LEPTON_INDICES)]
    pauli_2 = {
        "sigma_x": np.array([[0, 1], [1, 0]], dtype=complex),
        "sigma_y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "sigma_z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    right_generators = {}
    intertwiner_errors = {}
    for name, left_generator in pauli_2.items():
        right_generator = np.linalg.inv(j_matrix) @ left_generator @ j_matrix
        right_generators[name] = right_generator
        intertwiner_errors[name] = float(np.linalg.norm(left_generator @ j_matrix - j_matrix @ right_generator))

    lie_error = float(
        np.linalg.norm(
            right_generators["sigma_x"] @ right_generators["sigma_y"]
            - right_generators["sigma_y"] @ right_generators["sigma_x"]
            - 2j * right_generators["sigma_z"]
        )
    )

    return {
        "clean_2x2_core": [[complex(value) for value in row] for row in j_matrix],
        "right_pauli_generators": {
            name: [[complex(value) for value in row] for row in generator]
            for name, generator in right_generators.items()
        },
        "intertwiner_errors": intertwiner_errors,
        "lie_error_norm": lie_error,
    }


def _representative_diffuse_line_diagnostics() -> dict[str, Any]:
    slices = {slot: higgs_yukawa_slices_8x8()[slot].astype(complex) for slot in SLOT_ORDER}
    diffuse_lines = {
        "diffuse_plus": slices["H_1"] + slices["Hbar_1"],
        "diffuse_minus": slices["H_1"] - slices["Hbar_1"],
    }
    diagnostics: dict[str, Any] = {}
    for line_name, matrix in diffuse_lines.items():
        diagnostics[line_name] = {
            "weak_residuals": {},
            "color_residuals": {},
        }
        for generator_name, generator in _left_pauli_generators().items():
            _, residual = _best_right_intertwiner(generator, matrix)
            diagnostics[line_name]["weak_residuals"][generator_name] = residual
        for generator_name, generator in _left_color_generators().items():
            _, residual = _best_right_intertwiner(generator, matrix)
            diagnostics[line_name]["color_residuals"][generator_name] = residual
    return diagnostics


def _gauge_exact_grid_scan() -> dict[str, Any]:
    slices = {slot: higgs_yukawa_slices_8x8()[slot].astype(complex) for slot in SLOT_ORDER}
    generators = {
        **_left_pauli_generators(),
        "lambda_1": _left_color_generators()["lambda_1"],
        "lambda_2": _left_color_generators()["lambda_2"],
        "lambda_3": _left_color_generators()["lambda_3"],
    }

    exact_solutions: list[dict[str, Any]] = []
    for a in (-2, -1, 0, 1, 2):
        for b in (-2, -1, 0, 1, 2):
            for c in (-2, -1, 0, 1, 2):
                if a == 0 and b == 0 and c == 0:
                    continue
                yukawa = a * slices["H_1"] + b * slices["Hbar_1"] + c * slices["H_2"]
                residuals = {}
                for name, generator in generators.items():
                    _, residual = _best_right_intertwiner(generator, yukawa)
                    residuals[name] = residual
                if max(residuals.values()) < 1e-10:
                    exact_solutions.append(
                        {
                            "coefficients": {"H_1": a, "Hbar_1": b, "H_2": c},
                            "residuals": residuals,
                        }
                    )

    return {
        "coefficient_range": [-2, -1, 0, 1, 2],
        "exact_solutions": exact_solutions,
    }


def _serialize_complex_matrix(matrix: list[list[complex]]) -> list[list[dict[str, float]]]:
    return [
        [{"real": float(value.real), "imag": float(value.imag)} for value in row]
        for row in matrix
    ]


def build_summary() -> dict[str, Any]:
    span = _slice_span_diagnostics()
    slots = _slot_intertwiner_diagnostics()
    colors = _slot_color_intertwiner_diagnostics()
    clean = _clean_pair_symplectic_bridge()
    diffuse = _representative_diffuse_line_diagnostics()
    grid = _gauge_exact_grid_scan()

    serialized_slots: dict[str, Any] = {}
    for generator_name, slot_data in slots.items():
        serialized_slots[generator_name] = {}
        for slot, diagnostic in slot_data.items():
            serialized_slots[generator_name][slot] = {
                "residual_norm": diagnostic["residual_norm"],
                "right_leptonic_block": _serialize_complex_matrix(diagnostic["right_leptonic_block"]),
            }

    clean_right = {
        name: _serialize_complex_matrix(matrix)
        for name, matrix in clean["right_pauli_generators"].items()
    }
    clean_core = _serialize_complex_matrix(clean["clean_2x2_core"])

    diffuse_xy_residuals = [
        serialized_slots[generator][slot]["residual_norm"]
        for generator in ("sigma_x", "sigma_y")
        for slot in ("H_1", "Hbar_1")
    ]
    clean_residuals = [
        serialized_slots[generator][slot]["residual_norm"]
        for generator in ("sigma_x", "sigma_y", "sigma_z")
        for slot in ("H_2", "Hbar_2")
    ]
    serialized_colors: dict[str, Any] = {}
    for generator_name, slot_data in colors.items():
        serialized_colors[generator_name] = {
            slot: {"residual_norm": diagnostic["residual_norm"]}
            for slot, diagnostic in slot_data.items()
        }
    diffuse_color_residuals = [
        serialized_colors[generator][slot]["residual_norm"]
        for generator in ("lambda_1", "lambda_2", "lambda_3", "lambda_8")
        for slot in ("H_1", "Hbar_1")
    ]
    clean_color_residuals = [
        serialized_colors[generator][slot]["residual_norm"]
        for generator in ("lambda_1", "lambda_2", "lambda_3", "lambda_8")
        for slot in ("H_2", "Hbar_2")
    ]
    diffuse_lines_serialized = {
        line_name: {
            "weak_residuals": {
                generator: float(value)
                for generator, value in values["weak_residuals"].items()
            },
            "color_residuals": {
                generator: float(value)
                for generator, value in values["color_residuals"].items()
            },
        }
        for line_name, values in diffuse.items()
    }

    return {
        "status": "ok",
        "slice_span": span,
        "weak_slot_intertwiner_residuals": serialized_slots,
        "color_slot_intertwiner_residuals": serialized_colors,
        "representative_diffuse_lines": diffuse_lines_serialized,
        "small_integer_gauge_exact_grid_scan": grid,
        "clean_symplectic_bridge": {
            "clean_2x2_core": clean_core,
            "right_pauli_generators": clean_right,
            "intertwiner_errors": clean["intertwiner_errors"],
            "lie_error_norm": clean["lie_error_norm"],
        },
        "clean_weak_intertwiner_theorem": {
            "higgs_slice_space_has_rank_three": span["rank"] == 3,
            "kernel_is_exactly_h2_minus_hbar2": span["h2_minus_hbar2_norm"] == 0.0,
            "clean_pair_is_exact_for_all_three_pauli_generators": all(value == 0.0 for value in clean_residuals),
            "clean_pair_is_color_exact_for_the_tested_gell_mann_generators": all(value == 0.0 for value in clean_color_residuals),
            "clean_pair_realizes_a_right_su2_action_via_symplectic_j": (
                all(value == 0.0 for value in clean["intertwiner_errors"].values())
                and clean["lie_error_norm"] == 0.0
            ),
            "diffuse_pair_fails_noncartan_generators": all(value > 2.0 for value in diffuse_xy_residuals),
            "diffuse_pair_is_only_cartan_exact_in_current_basis": (
                serialized_slots["sigma_z"]["H_1"]["residual_norm"] < 1e-12
                and serialized_slots["sigma_z"]["Hbar_1"]["residual_norm"] < 1e-12
            ),
            "diffuse_pair_fails_tested_color_generators": all(value >= 1.0 for value in diffuse_color_residuals),
            "diffuse_plus_minus_lines_are_weak_exact": all(
                value < 1e-12
                for line in diffuse_lines_serialized.values()
                for value in line["weak_residuals"].values()
            ),
            "diffuse_plus_minus_lines_remain_color_obstructed": all(
                value > 0.8
                for line in diffuse_lines_serialized.values()
                for value in line["color_residuals"].values()
            ),
            "small_integer_full_gauge_exact_solutions_are_clean_only": all(
                solution["coefficients"]["H_1"] == 0 and solution["coefficients"]["Hbar_1"] == 0
                for solution in grid["exact_solutions"]
            ),
        },
        "interpretive_read": (
            "The spinor-spinor-vector Higgs packet is not a generic four-parameter "
            "cloud. It is a rigid 3-dimensional interaction space with one exact "
            "duplicated clean direction. That clean direction is the unique full "
            "weak SU(2) intertwiner already visible in the current canonical basis: "
            "its 2x2 core is the symplectic matrix J = [[0,-1],[1,0]], which "
            "conjugates the left Pauli action into an exact right Pauli action on "
            "(e_c, nu_c). The same clean pair is also exact for the tested color "
            "generators because it is color-trivial. By contrast, the diffuse pair "
            "H_1, Hbar_1 are singular coordinate axes on a broader diffuse plane: "
            "the weak-adapted lines H_1 + Hbar_1 and H_1 - Hbar_1 are exact for the "
            "full Pauli triple, but they still fail the tested nontrivial color "
            "generators. The small integer scan over the full 3-dimensional Higgs "
            "slice span reinforces the same point: the only fully gauge-exact lines "
            "detected there are the clean multiples. So the current exact frontier "
            "is sharper than 'weak fails': weak exactness can be restored inside the "
            "diffuse plane, while the surviving obstruction is color."
        ),
        "source_files": [
            "exploration/w33_fermionic_connes_sector.py",
            "exploration/w33_finite_spectral_triple.py",
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
