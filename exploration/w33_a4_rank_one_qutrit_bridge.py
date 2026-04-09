"""Rank-one qutrit form of the first family-sensitive A4 bridge packet.

This module combines the current finite-family and continuum-side exact bridges.

What is established here:
  - the first family-sensitive contribution is purely A4, with scalar entry
        Delta A4 = 1209 a0 / 9194,
    and the reduced local/global coefficients are already fixed to
        27/(16 pi^2)   and   351/(4 pi^2);
  - the finite family-sensitive packet is exactly a point-defect orbit on the
    regular C3 generation carrier;
  - in the qutrit/Fourier basis, every point projector E_ii becomes a rank-one
    matrix with all entry magnitudes equal to 1/3;
  - the three distinguished-generation choices are therefore a discrete phase
    orbit of the same rank-one qutrit projector, not three independent
    continuum family amplitudes.

So the strongest current conservative read is: the first family-sensitive
continuum packet is one scalar A4 amplitude carried by the canonical primitive
plane and acting internally as a phase-twisted rank-one qutrit projector.
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

from exploration.w33_yukawa_a4_entry_bridge import build_yukawa_a4_entry_summary


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_a4_rank_one_qutrit_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    path = DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


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


def _point_projector(index: int) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=float)
    matrix[index, index] = 1.0
    return matrix


def _point_projector_qutrit_packet(index: int) -> dict[str, Any]:
    image = _fourier_conjugate(_point_projector(index))
    singular_values = np.linalg.svd(image, compute_uv=False)
    abs_entries = np.abs(image)
    return {
        "index": index,
        "matrix": [
            [[float(value.real), float(value.imag)] for value in row]
            for row in image
        ],
        "singular_values": [float(value) for value in singular_values],
        "rank_one": bool(np.linalg.matrix_rank(image) == 1),
        "all_entry_magnitudes_equal_one_third": bool(
            np.allclose(abs_entries, np.ones((3, 3), dtype=float) / 3.0, atol=FLOAT_TOL)
        ),
    }


@lru_cache(maxsize=1)
def build_a4_rank_one_qutrit_summary() -> dict[str, Any]:
    a4 = build_yukawa_a4_entry_summary()
    local = _read_json("w33_bridge_a4_normalization_bridge_summary.json")
    global_a4 = _read_json("w33_k3_primitive_plane_global_a4_bridge_summary.json")
    qutrit = _read_json("w33_yukawa_qutrit_collapse_bridge_summary.json")
    point_defect = _read_json("w33_yukawa_point_defect_bridge_summary.json")

    projectors = [_point_projector_qutrit_packet(index) for index in range(3)]

    return {
        "status": "ok",
        "a4_entry": {
            "delta_A4": a4["product_heat_coefficients"]["delta_A4"],
            "A0_is_family_blind": a4["a4_entry_theorem"]["A0_is_family_blind"],
            "A2_is_family_blind": a4["a4_entry_theorem"]["A2_is_family_blind"],
            "A4_is_first_family_entry_point": a4["a4_entry_theorem"]["A4_is_first_family_entry_point"],
        },
        "continuum_prefactors": {
            "reduced_local_prefactor": local["reduced_local_bridge_prefactor"]["after_universal_rank2_factor_2"],
            "normalized_global_prefactor": global_a4["reduced_prefactors"]["normalized_global"],
            "primitive_plane_seed_form": global_a4["primitive_plane_seed_form"],
        },
        "finite_family_packet": {
            "qutrit_collapse_theorem": qutrit["qutrit_collapse_theorem"],
            "point_defect_theorem": point_defect["generation_point_defect_theorem"],
            "family_basis_in_cycle_model": point_defect["family_basis_in_cycle_model"],
        },
        "qutrit_projector_orbit": {
            "projectors": projectors,
            "all_three_are_rank_one": all(projector["rank_one"] for projector in projectors),
            "all_three_have_equal_entry_magnitude_one_third": all(
                projector["all_entry_magnitudes_equal_one_third"] for projector in projectors
            ),
            "all_three_share_singular_spectrum": all(
                np.allclose(
                    projectors[0]["singular_values"],
                    projector["singular_values"],
                    atol=FLOAT_TOL,
                )
                for projector in projectors[1:]
            ),
        },
        "rank_one_qutrit_bridge_theorem": {
            "first_family_sensitive_continuum_term_is_pure_A4": (
                a4["a4_entry_theorem"]["A0_is_family_blind"]
                and a4["a4_entry_theorem"]["A2_is_family_blind"]
                and a4["a4_entry_theorem"]["A4_is_first_family_entry_point"]
                and local["bridge_theorem"]["local_gauge_packet_is_pure_A4"]
            ),
            "local_and_global_prefactors_are_exactly_locked": (
                local["bridge_theorem"]["reduced_local_prefactor_is_27_over_16_pi_squared"]
                and global_a4["global_a4_coupling_theorem"]["reduced_global_prefactor_is_351_over_4_pi_squared"]
            ),
            "finite_family_side_is_exact_point_defect_orbit": bool(
                point_defect["generation_point_defect_theorem"]["distinguished_generation_texture_is_single_point_defect_packet"]
            ),
            "qutrit_images_of_generation_points_are_rank_one_phase_orbit": (
                all(projector["rank_one"] for projector in projectors)
                and all(projector["all_entry_magnitudes_equal_one_third"] for projector in projectors)
                and all(
                    np.allclose(
                        projectors[0]["singular_values"],
                        projector["singular_values"],
                        atol=FLOAT_TOL,
                    )
                    for projector in projectors[1:]
                )
            ),
            "first_family_sensitive_bridge_has_one_scalar_amplitude_and_discrete_c3_orbit": (
                a4["a4_entry_theorem"]["A4_is_first_family_entry_point"]
                and local["bridge_theorem"]["reduced_local_prefactor_is_27_over_16_pi_squared"]
                and global_a4["global_a4_coupling_theorem"]["reduced_global_prefactor_is_351_over_4_pi_squared"]
                and point_defect["generation_point_defect_theorem"]["distinguished_generation_texture_is_single_point_defect_packet"]
                and all(projector["rank_one"] for projector in projectors)
            ),
        },
        "bridge_verdict": (
            "The first family-sensitive bridge packet has collapsed further. "
            "Continuum-side, the first entry is the scalar A4 term Delta A4 "
            "with exact local/global prefactors 27/(16 pi^2) and 351/(4 pi^2). "
            "Finite-side, the family packet is exactly the C3 orbit of one "
            "generation point defect. In the qutrit basis, each orbit "
            "representative is a rank-one projector with identical singular "
            "spectrum and uniform entry magnitudes 1/3. So the current exact "
            "picture is not three free family amplitudes. It is one scalar A4 "
            "amplitude carried by the canonical primitive plane and acting "
            "internally through a discrete C3 orbit of one rank-one qutrit projector."
        ),
        "source_files": [
            "data/w33_bridge_a4_normalization_bridge_summary.json",
            "data/w33_k3_primitive_plane_global_a4_bridge_summary.json",
            "data/w33_yukawa_qutrit_collapse_bridge_summary.json",
            "data/w33_yukawa_point_defect_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_a4_rank_one_qutrit_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
