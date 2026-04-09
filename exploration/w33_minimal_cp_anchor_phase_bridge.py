"""Minimal CP activation on the anchored parity bridge.

The parity-odd anchor theorem reduced the quark frontier to a real anchored
shell plus a rank-2 parity-odd bridge between the ``U2`` anchor and the outer
pair. The next exact question is whether simply phasing that bridge can turn on
CP violation.

This module studies the smallest phase deformations of the real vertex-scan
candidate:

1. a common phase on both odd bridge legs;
2. a phase on the outer->middle leg only;
3. a phase on the middle->outer leg only; and
4. opposite phases on the two legs.

For each deformation, we project to the nearest unitary matrix via the polar
factor and measure the resulting Jarlskog invariant.

The outcome is sharp:

- opposite phases are CP-silent;
- a common phase or a one-leg phase produces a nonzero but small unitary
  Jarlskog invariant, with maximal response about ``2.345e-4`` in this minimal
  ansatz.

So the first CP-capable mechanism already present in the repo is not a generic
complex Yukawa cloud. It is a phase on the parity-odd ``U2`` anchor bridge.
"""

from __future__ import annotations

from functools import lru_cache
import json
from math import pi
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_minimal_cp_anchor_phase_bridge_summary.json"
GRID_SIZE = 721
TOL = 1e-10


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _anchor_metrics(matrix: np.ndarray, parity: np.ndarray) -> dict[str, float]:
    outer = np.diag([1, 0, 1]).astype(complex)
    middle = np.diag([0, 1, 0]).astype(complex)
    outer_block = (outer @ matrix @ outer)[np.ix_([0, 2], [0, 2])]
    return {
        "parity_commutator_norm": float(np.linalg.norm(matrix @ parity - parity @ matrix)),
        "outer_middle_coupling_norm": float(
            np.linalg.norm(outer @ matrix @ middle) + np.linalg.norm(middle @ matrix @ outer)
        ),
        "middle_entry_abs": float(abs((middle @ matrix @ middle)[1, 1])),
        "outer_block_det_abs": float(abs(np.linalg.det(outer_block))),
    }


def _phase_modes(even: np.ndarray, leg_a: np.ndarray, leg_b: np.ndarray) -> dict[str, Any]:
    modes: dict[str, Any] = {}
    grid = np.linspace(0.0, 2.0 * pi, GRID_SIZE)

    def build_matrix(mode: str, phi: float) -> np.ndarray:
        if mode == "common":
            return even + np.exp(1j * phi) * (leg_a + leg_b)
        if mode == "left_only":
            return even + np.exp(1j * phi) * leg_a + leg_b
        if mode == "right_only":
            return even + leg_a + np.exp(1j * phi) * leg_b
        if mode == "opposite":
            return even + np.exp(1j * phi) * leg_a + np.exp(-1j * phi) * leg_b
        raise ValueError(f"unknown mode {mode}")

    for mode in ("common", "left_only", "right_only", "opposite"):
        best_phi = 0.0
        best_j = 0.0
        best_abs_j = -1.0
        best_unitary: np.ndarray | None = None

        for phi in grid:
            unitary = _polar_unitary(build_matrix(mode, float(phi)))
            j_value = _jarlskog(unitary)
            if abs(j_value) > best_abs_j:
                best_abs_j = abs(j_value)
                best_phi = float(phi)
                best_j = float(j_value)
                best_unitary = unitary

        if best_unitary is None:
            raise AssertionError("expected a best unitary representative")

        modes[mode] = {
            "best_phase_radians": best_phi,
            "best_phase_over_pi": best_phi / pi,
            "max_abs_unitary_jarlskog": best_abs_j,
            "best_unitary_jarlskog": best_j,
            "best_unitary_abs_matrix": [
                [float(value) for value in row] for row in np.abs(best_unitary).tolist()
            ],
        }
    return modes


@lru_cache(maxsize=1)
def build_minimal_cp_anchor_phase_bridge_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    parity_bridge = _load_json("w33_parity_odd_anchor_bridge_summary.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    vertex = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (vertex + parity @ vertex @ parity)
    odd = 0.5 * (vertex - parity @ vertex @ parity)

    outer = np.diag([1, 0, 1]).astype(complex)
    middle = np.diag([0, 1, 0]).astype(complex)
    leg_a = outer @ odd @ middle
    leg_b = middle @ odd @ outer

    phase_modes = _phase_modes(even, leg_a, leg_b)

    common_best = phase_modes["common"]
    left_best = phase_modes["left_only"]
    right_best = phase_modes["right_only"]
    opposite_best = phase_modes["opposite"]

    common_best_matrix = _polar_unitary(even + np.exp(1j * common_best["best_phase_radians"]) * (leg_a + leg_b))
    opposite_best_matrix = _polar_unitary(
        even
        + np.exp(1j * opposite_best["best_phase_radians"]) * leg_a
        + np.exp(-1j * opposite_best["best_phase_radians"]) * leg_b
    )

    return {
        "status": "ok",
        "anchored_family_label": parity_bridge["anchored_family_label"],
        "real_vertex_scan_baseline": {
            "jarlskog": float(blocks["vertex_scan_best"]["Jarlskog"]),
            "parity_commutator_norm": float(parity_bridge["best_vertex_scan_candidate"]["commutator_norm"]),
            "odd_rank": int(parity_bridge["best_vertex_scan_candidate"]["odd_rank"]),
        },
        "phase_modes": phase_modes,
        "common_phase_best_metrics": _anchor_metrics(common_best_matrix, parity),
        "opposite_phase_best_metrics": _anchor_metrics(opposite_best_matrix, parity),
        "minimal_cp_anchor_phase_theorem": {
            "real_vertex_scan_baseline_is_cp_silent": (
                abs(float(blocks["vertex_scan_best"]["Jarlskog"])) < TOL
            ),
            "common_phase_on_full_odd_bridge_generates_nonzero_unitary_jarlskog": (
                common_best["max_abs_unitary_jarlskog"] > 1e-6
            ),
            "one_leg_phase_generates_the_same_cp_scale_as_common_phase": (
                abs(left_best["max_abs_unitary_jarlskog"] - common_best["max_abs_unitary_jarlskog"]) < 1e-7
                and abs(right_best["max_abs_unitary_jarlskog"] - common_best["max_abs_unitary_jarlskog"]) < 1e-7
            ),
            "opposite_leg_phases_cancel_cp_response": opposite_best["max_abs_unitary_jarlskog"] < 1e-12,
            "maximal_minimal_ansatz_cp_response_is_order_2e_minus_4": (
                2.0e-4 < common_best["max_abs_unitary_jarlskog"] < 3.0e-4
            ),
            "minimal_cp_activation_comes_from_phasing_the_parity_odd_u2_anchor_bridge": (
                common_best["max_abs_unitary_jarlskog"] > 1e-6
                and opposite_best["max_abs_unitary_jarlskog"] < 1e-12
            ),
        },
        "interpretive_read": (
            "Inference from the exact anchored parity decomposition: once the "
            "real quark candidate is reduced to an even shell plus odd anchor "
            "bridge, the first CP-capable deformation is a phase on that odd "
            "bridge. A common phase or a one-leg phase survives unitary "
            "projection and produces a small nonzero Jarlskog invariant, while "
            "opposite phases cancel almost exactly."
        ),
        "bridge_verdict": (
            "The current CP frontier is now minimal. The real anchored vertex "
            "scan is CP-silent. The first nonzero CP response comes from a phase "
            "on the parity-odd bridge connecting the U2 anchor to the outer "
            "pair, with maximal unitary response about 2.345e-4 in this minimal "
            "ansatz. Opposite phases on the two odd legs kill the response. So "
            "the remaining wall is not finding where CP can live. It can live on "
            "the anchored odd bridge already. The wall is explaining the correct "
            "relative phase pattern and amplitude."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_parity_odd_anchor_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_minimal_cp_anchor_phase_bridge_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
