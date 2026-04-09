"""CP capacity curve of the minimal ``U2`` anchor bridge.

The observed-target scan showed that the physical CKM Jarlskog scale is
reachable inside the minimal parity-odd anchor-bridge ansatz, but the matching
amplitude is not unique because phase and amplitude can trade off against each
other.

This module isolates the amplitude-side invariant instead: for each bridge
amplitude ``a in [0,1]`` it maximizes the unitary Jarlskog response over the
common phase family

    E + a * exp(i phi) * O,

where ``E`` is the parity-even anchored shell and ``O`` is the parity-odd
bridge. The resulting capacity curve

    J_max(a)

measures how much CP the bridge can support at strength ``a``.

The outcome is sharp in the current coarse scan:

- ``J_max(a)`` is monotone on ``[0,1]``;
- the observed CKM scale ``3.12e-5`` becomes reachable at amplitude about
  ``0.49``; and
- the closest coarse-grid capacity point is ``a = 0.4875``.

So the physical CP scale requires only about half of the full odd-bridge
capacity. The remaining freedom is phase placement, not whether the bridge is
strong enough in principle.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_cp_capacity_curve_bridge_summary.json"
AMPLITUDE_GRID_SIZE = 401
PHASE_GRID_SIZE = 721
TARGET_J_CKM = 3.12e-5
TOL = 1e-12


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


@lru_cache(maxsize=1)
def build_cp_capacity_curve_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    amplitudes = np.linspace(0.0, 1.0, AMPLITUDE_GRID_SIZE)
    phases = np.linspace(0.0, 2.0 * np.pi, PHASE_GRID_SIZE)

    capacity_curve: list[dict[str, float]] = []
    for amplitude in amplitudes:
        best_abs_j = 0.0
        best_phase = 0.0
        for phase in phases:
            unitary = _polar_unitary(even + amplitude * np.exp(1j * phase) * odd)
            abs_j = abs(_jarlskog(unitary))
            if abs_j > best_abs_j:
                best_abs_j = abs_j
                best_phase = float(phase)
        capacity_curve.append(
            {
                "amplitude": float(amplitude),
                "max_abs_unitary_jarlskog": float(best_abs_j),
                "phase_radians_at_max": best_phase,
            }
        )

    monotone = all(
        capacity_curve[index + 1]["max_abs_unitary_jarlskog"]
        >= capacity_curve[index]["max_abs_unitary_jarlskog"] - TOL
        for index in range(len(capacity_curve) - 1)
    )
    threshold = next(
        (
            point["amplitude"]
            for point in capacity_curve
            if point["max_abs_unitary_jarlskog"] >= TARGET_J_CKM
        ),
        None,
    )
    closest = min(
        capacity_curve,
        key=lambda point: abs(point["max_abs_unitary_jarlskog"] - TARGET_J_CKM),
    )

    sample_points = [
        point
        for index, point in enumerate(capacity_curve)
        if index % 40 == 0 or abs(point["amplitude"] - 0.4875) < TOL or abs(point["amplitude"] - 0.49) < TOL
    ]

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "capacity_curve_samples": sample_points,
        "threshold_amplitude_for_target_reachability": threshold,
        "closest_coarse_grid_point_to_target": closest,
        "cp_capacity_curve_theorem": {
            "common_phase_capacity_curve_is_monotone_in_bridge_amplitude": monotone,
            "observed_ckm_cp_scale_becomes_reachable_at_amplitude_about_0_point_49": (
                threshold is not None and abs(threshold - 0.49) < TOL
            ),
            "closest_coarse_grid_capacity_point_is_amplitude_0_point_4875": (
                abs(float(closest["amplitude"]) - 0.4875) < TOL
            ),
            "physical_cp_scale_uses_only_about_half_of_full_bridge_capacity": (
                threshold is not None and threshold < 0.5
            ),
        },
        "interpretive_read": (
            "Inference from the capacity curve: the odd U2 anchor bridge has a "
            "monotone CP budget as its strength increases. The observed CKM CP "
            "scale turns on well before full bridge strength, at about half of "
            "the available capacity in the current coarse scan."
        ),
        "bridge_verdict": (
            "The minimal anchored parity bridge is not barely sufficient for CP. "
            "Its maximal unitary Jarlskog response grows monotonically with bridge "
            "amplitude, and the observed CKM scale becomes reachable at amplitude "
            "about 0.49. So the physical CP size uses only about half of the full "
            "odd-bridge capacity. The remaining question is phase selection, not "
            "whether the bridge can carry enough CP."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_cp_capacity_curve_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
