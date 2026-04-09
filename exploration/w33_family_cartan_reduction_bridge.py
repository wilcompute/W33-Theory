"""Exact Cartan reduction of the remaining family-hierarchy problem.

This module packages the cleanest current reduction of the family side.

Earlier bridges established:
  - the family packet is the complete rank-one qutrit resolution
        I_3 = Q_0 + Q_1 + Q_2;
  - factorized packets Q_i ⊗ B are spectrally family-blind;
  - the first exact hierarchy-generating class is the non-factorized packet
        Q_0 ⊗ B_0 + Q_1 ⊗ B_1 + Q_2 ⊗ B_2.

If one now takes the minimal 3U-hyperbolic model

    B_i = mu_i * H,   H = [[0,1],[1,0]],

then the full bridge spectrum is exactly

    {|mu_0|, |mu_0|, |mu_1|, |mu_1|, |mu_2|, |mu_2|}.

So the remaining family-hierarchy problem has collapsed to an exact
three-scalar Cartan problem.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_family_cartan_reduction_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _complex_matrix(serialized: list[list[list[float]]]) -> np.ndarray:
    return np.array(
        [[complex(entry[0], entry[1]) for entry in row] for row in serialized],
        dtype=complex,
    )


def _operator(projectors: list[np.ndarray], mus: list[complex], hyperbolic: np.ndarray) -> np.ndarray:
    total = np.zeros((6, 6), dtype=complex)
    for projector, mu in zip(projectors, mus):
        total += np.kron(projector, mu * hyperbolic)
    return total


def _packet(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return {
        "rank": int(np.linalg.matrix_rank(matrix)),
        "singular_values": [float(value) for value in singular_values],
    }


def _mus_text(mus: list[complex]) -> list[list[float]]:
    return [[float(value.real), float(value.imag)] for value in mus]


@lru_cache(maxsize=1)
def build_family_cartan_reduction_summary() -> dict[str, Any]:
    rank_one = _read_json("w33_a4_rank_one_qutrit_bridge_summary.json")
    projectors = [
        _complex_matrix(packet["matrix"])
        for packet in rank_one["qutrit_projector_orbit"]["projectors"]
    ]
    hyperbolic = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    samples = {
        "democratic": [1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j],
        "two_plus_one": [1.0 + 0.0j, 1.0 + 0.0j, 3.0 + 0.0j],
        "three_level_real": [1.0 + 0.0j, 2.0 + 0.0j, 5.0 + 0.0j],
        "three_level_phase": [1.0 + 0.0j, 2.0 * np.exp(2j * np.pi / 7), 4.0 * np.exp(-2j * np.pi / 9)],
    }

    reports: dict[str, Any] = {}
    for name, mus in samples.items():
        matrix = _operator(projectors, mus, hyperbolic)
        packet = _packet(matrix)
        expected = sorted([abs(mu) for mu in mus for _ in range(2)], reverse=True)
        reports[name] = {
            "mus": _mus_text(mus),
            "packet": packet,
            "expected_duplicated_weight_spectrum": expected,
            "spectrum_matches_duplicated_weight_rule": bool(
                np.allclose(
                    np.array(packet["singular_values"]),
                    np.array(expected),
                    atol=FLOAT_TOL,
                )
            ),
        }

    return {
        "status": "ok",
        "sample_cartan_packets": reports,
        "family_cartan_reduction_theorem": {
            "every_sample_matches_the_exact_duplicated_weight_rule": all(
                report["spectrum_matches_duplicated_weight_rule"]
                for report in reports.values()
            ),
            "democratic_weights_give_no_family_hierarchy": (
                len(set(round(value, 8) for value in reports["democratic"]["packet"]["singular_values"] if value > FLOAT_TOL)) == 1
            ),
            "two_plus_one_weights_give_partial_hierarchy": (
                len(set(round(value, 8) for value in reports["two_plus_one"]["packet"]["singular_values"] if value > FLOAT_TOL)) == 2
            ),
            "three_level_weights_give_genuine_three_family_hierarchy": (
                len(set(round(value, 8) for value in reports["three_level_real"]["packet"]["singular_values"] if value > FLOAT_TOL)) == 3
                and len(set(round(value, 8) for value in reports["three_level_phase"]["packet"]["singular_values"] if value > FLOAT_TOL)) == 3
            ),
            "remaining_family_problem_is_exact_three_scalar_problem": all(
                report["spectrum_matches_duplicated_weight_rule"] for report in reports.values()
            ),
        },
        "interpretive_read": (
            "Inference from the exact qutrit projector algebra and the minimal "
            "3U hyperbolic model: the unresolved family-hierarchy data are "
            "three scalar magnitudes, modulo permutation of family labels."
        ),
        "bridge_verdict": (
            "The remaining family problem is now reduced as far as the present "
            "exact bridges allow. In the minimal non-factorized 3U model, the "
            "full family spectrum is exactly the duplicated absolute-value "
            "spectrum of three scalars mu_0, mu_1, mu_2. Democratic weights "
            "give no hierarchy, two-plus-one weights give a partial split, and "
            "three distinct weights give a genuine three-family hierarchy. So "
            "the only missing data at this layer are the three orbit weights "
            "themselves."
        ),
        "source_files": [
            "data/w33_a4_rank_one_qutrit_bridge_summary.json",
            "data/w33_nonfactorized_three_u_block_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_family_cartan_reduction_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
