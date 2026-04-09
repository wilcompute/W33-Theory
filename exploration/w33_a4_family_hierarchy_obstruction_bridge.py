"""Hierarchy obstruction at the first family-sensitive A4 bridge level.

This module turns the new rank-one qutrit bridge picture into an exact
spectral obstruction theorem.

What is established here:
  - the first family-sensitive continuum packet is already fixed to the A4
    level, with exact local/global prefactors and the canonical primitive K3
    plane form;
  - the internal family packet is a discrete C3 orbit of rank-one qutrit
    projectors with identical singular spectra;
  - tensoring any one of those projectors with the canonical primitive plane
    seed form or its first refinement form gives a 6x6 bridge operator whose
    singular spectrum is independent of the chosen family point.

So the first family-sensitive bridge term distinguishes a family direction
geometrically, but not spectrally. Any genuine three-family hierarchy must
appear only beyond this exact A4 rank-one bridge layer.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_a4_family_hierarchy_obstruction_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _complex_matrix(serialized: list[list[list[float]]]) -> np.ndarray:
    return np.array(
        [[complex(entry[0], entry[1]) for entry in row] for row in serialized],
        dtype=complex,
    )


def _spectral_packet(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    nonzero = [float(value) for value in singular_values if value > FLOAT_TOL]
    return {
        "shape": list(matrix.shape),
        "rank": int(np.linalg.matrix_rank(matrix)),
        "singular_values": [float(value) for value in singular_values],
        "nonzero_singular_values": nonzero,
        "nonzero_multiplicity": len(nonzero),
    }


def _allclose_packets(left: list[float], right: list[float]) -> bool:
    return np.allclose(np.array(left), np.array(right), atol=FLOAT_TOL)


@lru_cache(maxsize=1)
def build_a4_family_hierarchy_obstruction_summary() -> dict[str, Any]:
    rank_one = _read_json("w33_a4_rank_one_qutrit_bridge_summary.json")
    global_a4 = _read_json("w33_k3_primitive_plane_global_a4_bridge_summary.json")

    projectors = [
        _complex_matrix(packet["matrix"])
        for packet in rank_one["qutrit_projector_orbit"]["projectors"]
    ]
    seed = np.array(global_a4["primitive_plane_seed_form"], dtype=float)
    refined = np.array(global_a4["primitive_plane_first_refinement_form"], dtype=float)

    seed_packets = [_spectral_packet(np.kron(projector, seed)) for projector in projectors]
    refined_packets = [_spectral_packet(np.kron(projector, refined)) for projector in projectors]

    return {
        "status": "ok",
        "continuum_lock": {
            "delta_A4": rank_one["a4_entry"]["delta_A4"],
            "reduced_local_prefactor": rank_one["continuum_prefactors"]["reduced_local_prefactor"],
            "normalized_global_prefactor": rank_one["continuum_prefactors"]["normalized_global_prefactor"],
            "primitive_plane_seed_form": global_a4["primitive_plane_seed_form"],
            "primitive_plane_first_refinement_form": global_a4["primitive_plane_first_refinement_form"],
        },
        "seed_operator_orbit": seed_packets,
        "refined_operator_orbit": refined_packets,
        "hierarchy_obstruction_theorem": {
            "all_three_family_seed_operators_are_isospectral": all(
                _allclose_packets(seed_packets[0]["singular_values"], packet["singular_values"])
                for packet in seed_packets[1:]
            ),
            "all_three_family_refined_operators_are_isospectral": all(
                _allclose_packets(refined_packets[0]["singular_values"], packet["singular_values"])
                for packet in refined_packets[1:]
            ),
            "seed_packet_has_exactly_two_nonzero_singular_values": all(
                packet["nonzero_multiplicity"] == 2 for packet in seed_packets
            ),
            "refined_packet_has_exactly_two_nonzero_singular_values": all(
                packet["nonzero_multiplicity"] == 2 for packet in refined_packets
            ),
            "seed_packet_nonzero_spectrum_is_degenerate": all(
                len(packet["nonzero_singular_values"]) == 2
                and np.isclose(packet["nonzero_singular_values"][0], packet["nonzero_singular_values"][1], atol=FLOAT_TOL)
                for packet in seed_packets
            ),
            "refined_packet_nonzero_spectrum_is_degenerate": all(
                len(packet["nonzero_singular_values"]) == 2
                and np.isclose(packet["nonzero_singular_values"][0], packet["nonzero_singular_values"][1], atol=FLOAT_TOL)
                for packet in refined_packets
            ),
            "first_family_sensitive_bridge_cannot_yield_three_way_spectral_hierarchy": (
                all(
                    _allclose_packets(seed_packets[0]["singular_values"], packet["singular_values"])
                    for packet in seed_packets[1:]
                )
                and all(
                    _allclose_packets(refined_packets[0]["singular_values"], packet["singular_values"])
                    for packet in refined_packets[1:]
                )
                and all(packet["nonzero_multiplicity"] == 2 for packet in seed_packets)
                and all(packet["nonzero_multiplicity"] == 2 for packet in refined_packets)
            ),
        },
        "interpretive_read": (
            "Inference from the exact finite-plus-continuum bridge: the first "
            "family-sensitive term already picks a family direction, but only "
            "through an isospectral discrete orbit. So this layer can orient "
            "family space, but it cannot by itself produce a genuine three-way "
            "mass hierarchy."
        ),
        "bridge_verdict": (
            "The first family-sensitive A4 bridge layer is now boxed in by an "
            "exact obstruction. Because the internal family packet is a C3 orbit "
            "of rank-one qutrit projectors and the external carrier is already "
            "fixed, the resulting 6x6 bridge operators for the three family "
            "choices are exactly isospectral on both the primitive-plane seed "
            "and its first refinement. Each has only two equal nonzero singular "
            "values. So the first A4 bridge can mark a family direction, but it "
            "cannot generate the observed three-family spectral hierarchy. That "
            "hierarchy must come from a later bridge layer: higher heat order, "
            "selector mixing, or another nontrivial coupling beyond this exact "
            "rank-one packet."
        ),
        "source_files": [
            "data/w33_a4_rank_one_qutrit_bridge_summary.json",
            "data/w33_k3_primitive_plane_global_a4_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_a4_family_hierarchy_obstruction_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
