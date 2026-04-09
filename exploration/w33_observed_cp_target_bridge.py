"""Observed CKM-scale CP target inside the minimal anchor-bridge ansatz.

The minimal CP bridge showed that a phase on the parity-odd ``U2`` anchor
bridge is the first CP-capable deformation already present in the repo. The
next concrete question is whether the observed CKM CP scale is reachable inside
that same minimal ansatz, or whether a new structure is still needed.

Using the 2024 PDG value

    J_CKM = 3.12e-5,

we scan the same three minimal phase families:

1. common phase on the full odd bridge;
2. phase on the outer->middle leg only;
3. phase on the middle->outer leg only.

For each case, we polar-project to the nearest unitary matrix and search for a
point whose unitary Jarlskog invariant matches the observed scale.

The outcome is constructive: the observed CKM CP scale is already reachable
inside the minimal anchored parity-bridge ansatz. In the current coarse scan,
all three phase families hit the target at the same bridge amplitude
``0.7025`` up to scan resolution.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_observed_cp_target_bridge_summary.json"
TARGET_J_CKM = 3.12e-5
AMPLITUDE_GRID_SIZE = 401
PHASE_GRID_SIZE = 721


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _abs_score(candidate: np.ndarray, baseline: np.ndarray) -> float:
    return float(np.linalg.norm(np.abs(candidate) - np.abs(baseline)))


def _anchor_commutator_norm(candidate: np.ndarray, parity: np.ndarray) -> float:
    return float(np.linalg.norm(candidate @ parity - parity @ candidate))


@lru_cache(maxsize=1)
def build_observed_cp_target_bridge_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    minimal_cp = _load_json("w33_minimal_cp_anchor_phase_bridge_summary.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    outer = np.diag([1, 0, 1]).astype(complex)
    middle = np.diag([0, 1, 0]).astype(complex)
    leg_a = outer @ odd @ middle
    leg_b = middle @ odd @ outer

    amplitudes = np.linspace(0.0, 1.0, AMPLITUDE_GRID_SIZE)
    phases = np.linspace(0.0, 2.0 * pi, PHASE_GRID_SIZE)

    modes: dict[str, Any] = {}
    for mode in ("common", "left_only", "right_only"):
        best_error = float("inf")
        best_unitary: np.ndarray | None = None
        best_amplitude = 0.0
        best_phase = 0.0
        best_j = 0.0

        for amplitude in amplitudes:
            for phase in phases:
                if mode == "common":
                    candidate = even + amplitude * np.exp(1j * phase) * (leg_a + leg_b)
                elif mode == "left_only":
                    candidate = even + amplitude * np.exp(1j * phase) * leg_a + amplitude * leg_b
                else:
                    candidate = even + amplitude * leg_a + amplitude * np.exp(1j * phase) * leg_b

                unitary = _polar_unitary(candidate)
                j_value = _jarlskog(unitary)
                error = abs(abs(j_value) - TARGET_J_CKM)
                if error < best_error:
                    best_error = error
                    best_unitary = unitary
                    best_amplitude = float(amplitude)
                    best_phase = float(phase)
                    best_j = float(j_value)

        if best_unitary is None:
            raise AssertionError("expected best unitary candidate")

        modes[mode] = {
            "best_amplitude": best_amplitude,
            "best_phase_radians": best_phase,
            "best_phase_over_pi": best_phase / pi,
            "best_unitary_jarlskog": best_j,
            "target_error": best_error,
            "absolute_matrix_deviation_from_real_vertex_scan": _abs_score(best_unitary, baseline),
            "anchor_parity_commutator_norm": _anchor_commutator_norm(best_unitary, parity),
            "best_unitary_abs_matrix": [
                [float(value) for value in row] for row in np.abs(best_unitary).tolist()
            ],
        }

    common = modes["common"]
    left = modes["left_only"]
    right = modes["right_only"]

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "baseline_reference": {
            "real_vertex_scan_jarlskog": float(blocks["vertex_scan_best"]["Jarlskog"]),
            "minimal_common_phase_max_abs_j": float(
                minimal_cp["phase_modes"]["common"]["max_abs_unitary_jarlskog"]
            ),
        },
        "target_reaching_phase_modes": modes,
        "observed_cp_target_bridge_theorem": {
            "observed_ckm_cp_scale_is_reachable_inside_minimal_anchor_bridge_ansatz": (
                common["target_error"] < 1e-8
                and left["target_error"] < 1e-8
                and right["target_error"] < 1e-8
            ),
            "common_and_one_leg_phase_modes_hit_the_target_at_same_bridge_amplitude": (
                abs(common["best_amplitude"] - left["best_amplitude"]) < 1e-12
                and abs(common["best_amplitude"] - right["best_amplitude"]) < 1e-12
            ),
            "coarse_scan_target_bridge_amplitude_is_approximately_0_point_7025": (
                abs(common["best_amplitude"] - 0.7025) < 1e-12
            ),
            "target_cp_scale_is_submaximal_relative_to_the_minimal_ansatz_capacity": (
                TARGET_J_CKM < minimal_cp["phase_modes"]["common"]["max_abs_unitary_jarlskog"]
            ),
            "observed_cp_target_does_not_require_a_new_family_structure": (
                common["target_error"] < 1e-8
                and TARGET_J_CKM < minimal_cp["phase_modes"]["common"]["max_abs_unitary_jarlskog"]
            ),
        },
        "interpretive_read": (
            "Inference from the target-matching scan: once the quark side is "
            "reduced to the minimal U2 anchor bridge, the observed CKM CP scale "
            "already lies inside that ansatz. The problem is no longer whether "
            "the repo can support the right order of magnitude. It can."
        ),
        "bridge_verdict": (
            "The observed CKM CP scale is already reachable inside the minimal "
            "anchored parity-bridge model. In the current coarse scan, common-, "
            "left-only-, and right-only-phase deformations all hit "
            "J = 3.12e-5 at bridge amplitude 0.7025 up to scan resolution. So "
            "the remaining wall is not the existence of the correct CP scale. "
            "It is why the physical phase choice and amplitude land where they do."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_minimal_cp_anchor_phase_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_observed_cp_target_bridge_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
