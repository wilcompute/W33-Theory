"""No-go theorem for factorized family hierarchy in the current bridge class.

This module upgrades the primitive-plane hierarchy obstruction to a general
factorization obstruction.

Input from earlier exact bridges:
  - the internal family packet is a discrete C3 orbit of three rank-one qutrit
    projectors Q_0, Q_1, Q_2;
  - these projectors are related by internal cyclic permutation conjugacy;
  - the first family-sensitive continuum entry is the scalar A4 packet.

Main point:
  For any fixed external operator B, the family-tagged bridge operators

      M_i = Q_i ⊗ B

  are all unitarily similar through an internal permutation matrix. Hence they
  are exactly isospectral, with identical singular values and identical
  eigenvalue multisets.

So no bridge layer of the current factorized form "family projector times
family-blind external carrier" can generate a genuine three-family spectral
hierarchy. Any real hierarchy must come from a non-factorized coupling,
multiple interfering family packets, or a later symmetry-breaking layer.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_factorized_family_no_go_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _complex_matrix(serialized: list[list[list[float]]]) -> np.ndarray:
    return np.array(
        [[complex(entry[0], entry[1]) for entry in row] for row in serialized],
        dtype=complex,
    )


def _qutrit_phase_cycle(power: int) -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    base = np.diag([1.0, omega, omega * omega]).astype(complex)
    result = np.eye(3, dtype=complex)
    if power >= 0:
        for _ in range(power):
            result = result @ base
        return result
    inverse = np.conjugate(base).T
    for _ in range(-power):
        result = result @ inverse
    return result


def _spectral_packet(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    eigenvalues = np.linalg.eigvals(matrix)
    return {
        "shape": list(matrix.shape),
        "rank": int(np.linalg.matrix_rank(matrix)),
        "singular_values": [float(value) for value in singular_values],
        "eigenvalues": [[float(value.real), float(value.imag)] for value in eigenvalues],
    }


def _sorted_complex_pairs(values: list[list[float]]) -> np.ndarray:
    complex_values = np.array([complex(real, imag) for real, imag in values], dtype=complex)
    return np.sort_complex(complex_values)


@lru_cache(maxsize=1)
def build_factorized_family_no_go_summary() -> dict[str, Any]:
    rank_one = _read_json("w33_a4_rank_one_qutrit_bridge_summary.json")
    global_a4 = _read_json("w33_k3_primitive_plane_global_a4_bridge_summary.json")

    qutrit_projectors = [
        _complex_matrix(packet["matrix"])
        for packet in rank_one["qutrit_projector_orbit"]["projectors"]
    ]

    sample_external_operators = {
        "primitive_plane_seed": np.array(global_a4["primitive_plane_seed_form"], dtype=complex),
        "primitive_plane_first_refinement": np.array(
            global_a4["primitive_plane_first_refinement_form"],
            dtype=complex,
        ),
        "generic_nondiagonal_test": np.array(
            [
                [2.0, 1.0 - 1.0j],
                [3.0 + 2.0j, -1.0],
            ],
            dtype=complex,
        ),
    }

    sample_reports: dict[str, Any] = {}
    for name, external in sample_external_operators.items():
        operators = [np.kron(projector, external) for projector in qutrit_projectors]
        packets = [_spectral_packet(operator) for operator in operators]
        similarities = []
        for index in range(3):
            phase = _qutrit_phase_cycle(index)
            conjugated = np.kron(phase, np.eye(external.shape[0], dtype=complex)) @ operators[0] @ np.kron(
                np.conjugate(phase).T,
                np.eye(external.shape[0], dtype=complex),
            )
            similarities.append(bool(np.allclose(conjugated, operators[index], atol=FLOAT_TOL)))
        sample_reports[name] = {
            "external_operator": [
                [[float(value.real), float(value.imag)] for value in row]
                for row in external
            ],
            "operator_packets": packets,
            "cyclic_similarity_from_first_operator": similarities,
            "all_three_share_singular_spectrum": all(
                np.allclose(
                    np.array(packets[0]["singular_values"]),
                    np.array(packet["singular_values"]),
                    atol=FLOAT_TOL,
                )
                for packet in packets[1:]
            ),
            "all_three_share_eigenvalue_multiset": all(
                np.allclose(
                    _sorted_complex_pairs(packets[0]["eigenvalues"]),
                    _sorted_complex_pairs(packet["eigenvalues"]),
                    atol=FLOAT_TOL,
                )
                for packet in packets[1:]
            ),
        }

    return {
        "status": "ok",
        "inputs": {
            "rank_one_qutrit_bridge_theorem": rank_one["rank_one_qutrit_bridge_theorem"],
            "normalized_global_prefactor": global_a4["reduced_prefactors"]["normalized_global"],
        },
        "sample_factorized_family_packets": sample_reports,
        "factorized_family_no_go_theorem": {
            "qutrit_projectors_are_cyclically_conjugate": True,
            "every_tested_factorized_family_packet_is_cyclically_similar": all(
                all(report["cyclic_similarity_from_first_operator"])
                for report in sample_reports.values()
            ),
            "every_tested_factorized_family_packet_is_singular_isospectral": all(
                report["all_three_share_singular_spectrum"]
                for report in sample_reports.values()
            ),
            "every_tested_factorized_family_packet_is_eigen_isospectral": all(
                report["all_three_share_eigenvalue_multiset"]
                for report in sample_reports.values()
            ),
            "no_factorized_family_blind_external_carrier_can_generate_three_way_hierarchy": all(
                all(report["cyclic_similarity_from_first_operator"])
                and report["all_three_share_singular_spectrum"]
                and report["all_three_share_eigenvalue_multiset"]
                for report in sample_reports.values()
            ),
        },
        "interpretive_read": (
            "Inference from the exact internal packet: once the family side has "
            "collapsed to a cyclic orbit of conjugate rank-one qutrit projectors, "
            "any bridge that still factorizes through a fixed external carrier is "
            "forced to be spectrally family-blind."
        ),
        "bridge_verdict": (
            "The hierarchy obstruction is now general within the current bridge "
            "class. It is not tied to the primitive K3 plane or any one special "
            "external form. For any family-blind external operator B, the three "
            "family-tagged bridge operators Q_i ⊗ B are conjugate by the internal "
            "C3 permutation, so they are exactly isospectral. Therefore no "
            "factorized bridge of the current form can produce a genuine "
            "three-family hierarchy. Breaking through requires a non-factorized "
            "family/external coupling, multiple interfering family packets, or "
            "another later symmetry-breaking layer."
        ),
        "source_files": [
            "data/w33_a4_rank_one_qutrit_bridge_summary.json",
            "data/w33_k3_primitive_plane_global_a4_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_factorized_family_no_go_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
