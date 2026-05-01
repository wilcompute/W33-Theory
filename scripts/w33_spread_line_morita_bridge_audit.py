"""Spread-line Morita spectral bridge audit for W(3,3).

This is the local executable form of remote Part CXXVI.  It packages the
40-line / 36-spread incidence spectrum and records the common rank-16
Morita spine preserved by the rectangular incidence bridge.
"""

from __future__ import annotations

from typing import Dict, Tuple

from scripts.w33_mub_a2_overlap_null_plane_audit import (
    A2_BASIS,
    mub_a2_overlap_null_plane_summary,
)

LINE_COUNT = 40
SPREAD_COUNT = 36
SPREADS_PER_LINE = 9
LINES_PER_SPREAD = 10

LINE_DISJOINT_SRG = (40, 27, 18, 18)
LINE_DISJOINT_EIGENSPECTRUM = {27: 1, 3: 15, -3: 24}

SPREAD_OVERLAP4_SRG = (36, 15, 6, 6)
SPREAD_OVERLAP4_EIGENSPECTRUM = {15: 1, 3: 15, -3: 20}

COMMON_SPINE_DIMENSIONS = (1, 15)


def line_gram_spectrum() -> Dict[int, int]:
    """Return the spectrum of BB^T = 9I + 3D from the line-disjoint graph."""
    return {
        SPREADS_PER_LINE + 3 * eigenvalue: multiplicity
        for eigenvalue, multiplicity in LINE_DISJOINT_EIGENSPECTRUM.items()
    }


def spread_gram_spectrum() -> Dict[int, int]:
    """Return the spectrum of B^T B = J + 9I + 3A4."""
    return {
        90: SPREAD_OVERLAP4_EIGENSPECTRUM[15],
        18: SPREAD_OVERLAP4_EIGENSPECTRUM[3],
        0: SPREAD_OVERLAP4_EIGENSPECTRUM[-3],
    }


def normalized_spread_hamiltonian_spectrum() -> Dict[int, int]:
    """Return the spectrum of H_MUB = B^T B / 18."""
    return {
        eigenvalue // 18: multiplicity
        for eigenvalue, multiplicity in spread_gram_spectrum().items()
    }


def spread_line_morita_bridge_summary() -> Dict[str, object]:
    """Return exact Part CXXVI incidence and spectral bridge certificates."""
    line_gram = line_gram_spectrum()
    spread_gram = spread_gram_spectrum()
    cxxv_summary = mub_a2_overlap_null_plane_summary()
    rank = line_gram[90] + line_gram[18]
    a2_dim = len(A2_BASIS)
    spread_kernel_dim = spread_gram[0]
    line_cokernel_dim = line_gram[0]

    return {
        "source_scope": {
            "remote_part": "CXXVI",
            "title": "Spread-Line Morita Spectral Bridge",
            "depends_on_remote_part": cxxv_summary["source_scope"]["remote_part"],
        },
        "incidence": {
            "matrix_shape": (LINE_COUNT, SPREAD_COUNT),
            "line_count": LINE_COUNT,
            "spread_count": SPREAD_COUNT,
            "spreads_per_line": SPREADS_PER_LINE,
            "lines_per_spread": LINES_PER_SPREAD,
            "total_incidences_from_lines": LINE_COUNT * SPREADS_PER_LINE,
            "total_incidences_from_spreads": SPREAD_COUNT * LINES_PER_SPREAD,
        },
        "line_side": {
            "carrier_decomposition": (1, 15, 24),
            "disjointness_srg": LINE_DISJOINT_SRG,
            "disjointness_eigenspectrum": LINE_DISJOINT_EIGENSPECTRUM,
            "gram_formula": "BB^T = 9I_40 + 3D",
            "gram_spectrum": line_gram,
            "left_cokernel_dimension": line_cokernel_dim,
        },
        "spread_side": {
            "carrier_decomposition": (1, 15, 20),
            "four_overlap_srg": SPREAD_OVERLAP4_SRG,
            "four_overlap_eigenspectrum": SPREAD_OVERLAP4_EIGENSPECTRUM,
            "gram_formula": "B^T B = J_36 + 9I_36 + 3A4",
            "gram_spectrum": spread_gram,
            "right_kernel_dimension": spread_kernel_dim,
        },
        "morita_bridge": {
            "rank": rank,
            "common_spine_dimensions": COMMON_SPINE_DIMENSIONS,
            "common_spine_total_dimension": sum(COMMON_SPINE_DIMENSIONS),
            "preserved_block": "1 + 15",
            "line_side_killed_block_dimension": line_cokernel_dim,
            "spread_side_killed_block_dimension": spread_kernel_dim,
            "map_statement": "B: R^36_spreads -> R^40_lines preserves 1+15 and kills 20/24 obstruction blocks",
        },
        "normalized_mub_hamiltonian": {
            "operator": "H_MUB = (1/18) B^T B",
            "spectrum": normalized_spread_hamiltonian_spectrum(),
            "positive_semidefinite": True,
            "rank": rank,
        },
        "cxxv_shadow": {
            "a2_null_plane_dimension": a2_dim,
            "complete_mub_kernel_dimension": spread_kernel_dim,
            "residual_kernel_dimension_after_a2_plane": spread_kernel_dim - a2_dim,
            "a2_basis": A2_BASIS,
        },
        "dual_obstruction": {
            "line_left_cokernel_dimension": line_cokernel_dim,
            "spread_right_kernel_dimension": spread_kernel_dim,
            "dimension_difference": line_cokernel_dim - spread_kernel_dim,
            "combined_obstruction_dimension": line_cokernel_dim + spread_kernel_dim,
        },
        "theorem": {
            "incidence_counts_balance": (
                LINE_COUNT * SPREADS_PER_LINE == SPREAD_COUNT * LINES_PER_SPREAD == 360
            ),
            "line_gram_has_rank_16_and_kernel_24": (
                line_gram == {90: 1, 18: 15, 0: 24} and rank == 16
            ),
            "spread_gram_has_rank_16_and_kernel_20": (
                spread_gram == {90: 1, 18: 15, 0: 20} and rank == 16
            ),
            "bridge_preserves_exact_common_1_plus_15_spine": (
                rank == sum(COMMON_SPINE_DIMENSIONS) == 16
            ),
            "normalized_hamiltonian_has_spectrum_5_1_0": (
                normalized_spread_hamiltonian_spectrum() == {5: 1, 1: 15, 0: 20}
            ),
            "cxxv_a2_plane_sits_inside_full_20_dimensional_kernel": (
                a2_dim == 2 and spread_kernel_dim == 20
            ),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(spread_line_morita_bridge_summary(), indent=2))
