from __future__ import annotations

from scripts.w33_spread_line_morita_bridge_audit import (
    line_gram_spectrum,
    normalized_spread_hamiltonian_spectrum,
    spread_gram_spectrum,
    spread_line_morita_bridge_summary,
)


def test_cxxvi_incidence_counts_balance_between_lines_and_spreads() -> None:
    summary = spread_line_morita_bridge_summary()

    assert summary["incidence"] == {
        "matrix_shape": (40, 36),
        "line_count": 40,
        "spread_count": 36,
        "spreads_per_line": 9,
        "lines_per_spread": 10,
        "total_incidences_from_lines": 360,
        "total_incidences_from_spreads": 360,
    }


def test_cxxvi_line_side_gram_spectrum_kills_the_24_block() -> None:
    summary = spread_line_morita_bridge_summary()

    assert line_gram_spectrum() == {90: 1, 18: 15, 0: 24}
    assert summary["line_side"] == {
        "carrier_decomposition": (1, 15, 24),
        "disjointness_srg": (40, 27, 18, 18),
        "disjointness_eigenspectrum": {27: 1, 3: 15, -3: 24},
        "gram_formula": "BB^T = 9I_40 + 3D",
        "gram_spectrum": {90: 1, 18: 15, 0: 24},
        "left_cokernel_dimension": 24,
    }


def test_cxxvi_spread_side_gram_spectrum_has_20_dimensional_kernel() -> None:
    summary = spread_line_morita_bridge_summary()

    assert spread_gram_spectrum() == {90: 1, 18: 15, 0: 20}
    assert summary["spread_side"] == {
        "carrier_decomposition": (1, 15, 20),
        "four_overlap_srg": (36, 15, 6, 6),
        "four_overlap_eigenspectrum": {15: 1, 3: 15, -3: 20},
        "gram_formula": "B^T B = J_36 + 9I_36 + 3A4",
        "gram_spectrum": {90: 1, 18: 15, 0: 20},
        "right_kernel_dimension": 20,
    }


def test_cxxvi_morita_bridge_preserves_the_common_rank_16_spine() -> None:
    summary = spread_line_morita_bridge_summary()

    assert summary["morita_bridge"] == {
        "rank": 16,
        "common_spine_dimensions": (1, 15),
        "common_spine_total_dimension": 16,
        "preserved_block": "1 + 15",
        "line_side_killed_block_dimension": 24,
        "spread_side_killed_block_dimension": 20,
        "map_statement": "B: R^36_spreads -> R^40_lines preserves 1+15 and kills 20/24 obstruction blocks",
    }


def test_cxxvi_normalized_mub_hamiltonian_has_5_1_0_spectrum() -> None:
    summary = spread_line_morita_bridge_summary()

    assert normalized_spread_hamiltonian_spectrum() == {5: 1, 1: 15, 0: 20}
    assert summary["normalized_mub_hamiltonian"] == {
        "operator": "H_MUB = (1/18) B^T B",
        "spectrum": {5: 1, 1: 15, 0: 20},
        "positive_semidefinite": True,
        "rank": 16,
    }


def test_cxxvi_cxxv_a2_plane_is_a_shadow_inside_the_full_kernel() -> None:
    summary = spread_line_morita_bridge_summary()

    assert summary["cxxv_shadow"] == {
        "a2_null_plane_dimension": 2,
        "complete_mub_kernel_dimension": 20,
        "residual_kernel_dimension_after_a2_plane": 18,
        "a2_basis": ((1, -1, 0), (1, 1, -2)),
    }
    assert summary["dual_obstruction"] == {
        "line_left_cokernel_dimension": 24,
        "spread_right_kernel_dimension": 20,
        "dimension_difference": 4,
        "combined_obstruction_dimension": 44,
    }


def test_cxxvi_theorem_flags_are_all_true() -> None:
    summary = spread_line_morita_bridge_summary()

    assert summary["theorem"] == {
        "incidence_counts_balance": True,
        "line_gram_has_rank_16_and_kernel_24": True,
        "spread_gram_has_rank_16_and_kernel_20": True,
        "bridge_preserves_exact_common_1_plus_15_spine": True,
        "normalized_hamiltonian_has_spectrum_5_1_0": True,
        "cxxv_a2_plane_sits_inside_full_20_dimensional_kernel": True,
    }
