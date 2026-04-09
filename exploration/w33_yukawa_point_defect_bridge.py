"""Point-defect form of the distinguished-generation Yukawa packet.

This module sharpens the relation between the Delta(27)-style generation
envelope and the mod-3 qutrit collapse of the reduced Yukawa algebra.

What is established here:
  - in the cycle basis of the regular C3 generation module, the finite-family
    basis vector (1,-1,0) becomes a single generation point;
  - the canonical distinguished-generation envelope

        [[d, o, o],
         [o, e, o],
         [o, o, e]]

    is exactly

        (e-o) I + o J + (d-e) E_ii

    for one coordinate projector E_ii;
  - the 3-element orbit of distinguished-generation textures is therefore
    exactly the cyclic orbit of one point defect under generation translation;
  - in the complex Fourier/qutrit basis that point defect is democratic across
    the 1, omega, omega^2 packet.

So the distinguished-generation texture is not an extra family mystery. It is
one local point defect riding on top of an isotropic shell in the same cyclic
generation carrier already isolated by the mod-3 bridge.
"""

from __future__ import annotations

from functools import lru_cache
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_yukawa_point_defect_bridge_summary.json"
FLOAT_TOL = 1e-12

PERMUTATION_CYCLE = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=float,
)
FLAG_BASIS = {
    "symmetric_doublet_line": np.array([1, 1, 0], dtype=int),
    "distinguished_generation_axis": np.array([0, 0, 1], dtype=int),
    "doublet_difference_axis": np.array([1, -1, 0], dtype=int),
}


def _read_json(filename: str) -> dict[str, Any]:
    return load_json_from_repo_data(ROOT, Path("data") / filename)


def _mod3(vector_or_matrix: np.ndarray) -> np.ndarray:
    return np.mod(vector_or_matrix, 3).astype(int)


def _cycle_power(power: int) -> np.ndarray:
    result = np.eye(3, dtype=float)
    if power >= 0:
        for _ in range(power):
            result = result @ PERMUTATION_CYCLE
        return result

    inverse = PERMUTATION_CYCLE.T
    for _ in range(-power):
        result = result @ inverse
    return result


def _point_projector(index: int) -> np.ndarray:
    projector = np.zeros((3, 3), dtype=float)
    projector[index, index] = 1.0
    return projector


def _isotropic_shell(diagonal_degenerate: float, off_diagonal: float) -> np.ndarray:
    return (diagonal_degenerate - off_diagonal) * np.eye(3) + off_diagonal * np.ones((3, 3), dtype=float)


def _dft_matrix() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega * omega, omega],
            [1.0, omega, omega * omega],
        ],
        dtype=complex,
    )


def _fourier_conjugate(matrix: np.ndarray) -> np.ndarray:
    fourier = _dft_matrix()
    inverse = np.conjugate(fourier).T / 3.0
    return inverse @ matrix.astype(complex) @ fourier


def _cycle_basis_intertwiner_mod3() -> np.ndarray:
    summary = _read_json("w33_yukawa_qutrit_collapse_bridge_summary.json")
    return np.array(summary["mod3_generation_packet"]["intertwiner_to_cycle_basis"], dtype=int)


def _family_basis_in_cycle_model() -> dict[str, list[int]]:
    intertwiner = _cycle_basis_intertwiner_mod3()
    return {
        name: _mod3(intertwiner @ vector).tolist()
        for name, vector in FLAG_BASIS.items()
    }


def _envelope_matrix(profile: dict[str, Any]) -> np.ndarray:
    return np.array(profile["envelope"], dtype=float)


def _point_defect_profile(profile: dict[str, Any]) -> dict[str, Any]:
    distinguished = int(profile["distinguished_generation"])
    distinguished_diagonal = float(profile["distinguished_diagonal_norm"])
    degenerate_diagonal = float(profile["degenerate_diagonal_norm"])
    off_diagonal = float(profile["uniform_off_diagonal_norm"])

    shell = _isotropic_shell(degenerate_diagonal, off_diagonal)
    defect_size = distinguished_diagonal - degenerate_diagonal
    defect = defect_size * _point_projector(distinguished)
    reconstructed = shell + defect
    envelope = _envelope_matrix(profile)

    return {
        "distinguished_generation": distinguished,
        "shell_scalar_identity": degenerate_diagonal - off_diagonal,
        "shell_scalar_all_ones": off_diagonal,
        "point_defect_amplitude": defect_size,
        "reconstructs_from_shell_plus_point_defect": bool(
            np.allclose(reconstructed, envelope, atol=FLOAT_TOL)
        ),
        "max_abs_reconstruction_error": float(np.max(np.abs(reconstructed - envelope))),
        "reconstructed_envelope": reconstructed.tolist(),
    }


def _slot_cycle_orbit_report(slot_profile: dict[str, Any]) -> dict[str, Any]:
    canonical = slot_profile["canonical_texture"]
    canonical_report = _point_defect_profile(canonical)
    orbit_reports = []
    for orbit_item in slot_profile["cycle_orbit"]:
        orbit_profile = _point_defect_profile(orbit_item)
        power = int(orbit_item["cycle_power"])
        cycled_projector = (_cycle_power(power) @ _point_projector(0) @ _cycle_power(-power)).tolist()
        orbit_reports.append(
            {
                "cycle_power": power,
                "distinguished_generation": orbit_profile["distinguished_generation"],
                "point_defect_amplitude": orbit_profile["point_defect_amplitude"],
                "cycled_point_projector": cycled_projector,
                "reconstructs_from_shell_plus_point_defect": orbit_profile["reconstructs_from_shell_plus_point_defect"],
                "max_abs_reconstruction_error": orbit_profile["max_abs_reconstruction_error"],
            }
        )

    return {
        "canonical_point_defect_profile": canonical_report,
        "cycle_orbit_profiles": orbit_reports,
        "canonical_cycle_orbit_is_point_projector_orbit": all(
            item["distinguished_generation"] == item["cycle_power"]
            and item["reconstructs_from_shell_plus_point_defect"]
            and np.isclose(
                item["point_defect_amplitude"],
                canonical_report["point_defect_amplitude"],
                atol=FLOAT_TOL,
            )
            for item in orbit_reports
        ),
    }


def _fourier_point_defect_report() -> dict[str, Any]:
    point = _point_projector(0)
    point_fourier = _fourier_conjugate(point)
    democratic = np.ones((3, 3), dtype=complex) / 3.0
    return {
        "point_projector_fourier_image": [
            [[float(value.real), float(value.imag)] for value in row]
            for row in point_fourier
        ],
        "point_projector_is_democratic_in_qutrit_basis": bool(
            np.allclose(point_fourier, democratic, atol=1e-10)
        ),
    }


@lru_cache(maxsize=1)
def build_yukawa_point_defect_summary() -> dict[str, Any]:
    delta27 = _read_json("w33_l6_delta27_texture_bridge_summary.json")
    qutrit = _read_json("w33_yukawa_qutrit_collapse_bridge_summary.json")

    family_basis_cycle = _family_basis_in_cycle_model()
    slot_reports = {
        slot: _slot_cycle_orbit_report(profile)
        for slot, profile in delta27["slot_profiles"].items()
    }
    fourier = _fourier_point_defect_report()

    return {
        "status": "ok",
        "family_basis_in_cycle_model": family_basis_cycle,
        "slot_profiles": slot_reports,
        "qutrit_point_defect_fourier_packet": fourier,
        "generation_point_defect_theorem": {
            "doublet_difference_axis_becomes_single_generation_point_mod3": (
                family_basis_cycle["doublet_difference_axis"] in ([1, 0, 0], [2, 0, 0])
            ),
            "distinguished_generation_axis_lands_in_augmentation_plane": (
                sum(family_basis_cycle["distinguished_generation_axis"]) % 3 == 0
                and family_basis_cycle["distinguished_generation_axis"] != [1, 1, 1]
            ),
            "both_slots_have_exact_shell_plus_point_defect_form": all(
                report["canonical_point_defect_profile"]["reconstructs_from_shell_plus_point_defect"]
                for report in slot_reports.values()
            ),
            "both_slots_have_exact_cyclic_point_defect_orbit": all(
                report["canonical_cycle_orbit_is_point_projector_orbit"]
                for report in slot_reports.values()
            ),
            "point_defect_is_democratic_in_qutrit_fourier_basis": bool(
                fourier["point_projector_is_democratic_in_qutrit_basis"]
            ),
            "distinguished_generation_texture_is_single_point_defect_packet": (
                all(
                    report["canonical_point_defect_profile"]["reconstructs_from_shell_plus_point_defect"]
                    for report in slot_reports.values()
                )
                and all(
                    report["canonical_cycle_orbit_is_point_projector_orbit"]
                    for report in slot_reports.values()
                )
                and fourier["point_projector_is_democratic_in_qutrit_basis"]
            ),
        },
        "interpretive_read": (
            "Inference from the exact finite data: the family-sensitive Yukawa "
            "packet is best read as the amplitude of a generation point defect "
            "and its C3 orbit, sitting on top of a generation-isotropic shell. "
            "This is the finite object that any later continuum A4/U1 carrier "
            "should be coupling to."
        ),
        "bridge_verdict": (
            "The distinguished-generation Yukawa texture is now structurally "
            "simple. In the regular C3 generation model, the finite-family "
            "difference axis is literally a single generation point, the "
            "Delta(27)-style envelope is exactly an isotropic shell plus one "
            "point-projector defect, and the 3-cycle orbit of distinguished "
            "generations is exactly the orbit of that point defect. In the "
            "complex qutrit basis, the same defect is democratic across the "
            "1, omega, omega^2 packet. So the family asymmetry is not a new "
            "carrier: it is one local defect riding on the cyclic qutrit carrier."
        ),
        "source_files": [
            "data/w33_l6_delta27_texture_bridge_summary.json",
            "data/w33_yukawa_qutrit_collapse_bridge_summary.json",
        ],
        "upstream_qutrit_theorem": qutrit["qutrit_collapse_theorem"],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_point_defect_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
