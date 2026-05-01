from __future__ import annotations

from scripts.w33_e_sector_tomotope_balance_audit import (
    e_sector_tomotope_balance_summary,
)


def test_cxxvii_pair_counts_reconstruct_the_192_pair_e_sector_layer() -> None:
    summary = e_sector_tomotope_balance_summary()

    assert summary["pair_counts"] == {
        "same_pairs_per_chirality_sector": 48,
        "same_chirality_total_pairs": 96,
        "opposite_chirality_total_pairs": 96,
        "full_e_sector_three_cycle_pairs": 192,
    }


def test_cxxvii_overlap_splits_balance_to_96_and_96() -> None:
    summary = e_sector_tomotope_balance_summary()

    assert summary["overlap_splits"]["same_per_chirality_sector"] == {
        "four_overlap": 18,
        "one_overlap": 30,
    }
    assert summary["overlap_splits"]["same_chirality_total"] == {
        "four_overlap": 36,
        "one_overlap": 60,
    }
    assert summary["overlap_splits"]["opposite_chirality"] == {
        "four_overlap": 60,
        "one_overlap": 36,
    }
    assert summary["overlap_splits"]["full_e_sector_total"] == {
        "four_overlap": 96,
        "one_overlap": 96,
    }


def test_cxxvii_chirality_flip_carries_the_w33_24_block() -> None:
    summary = e_sector_tomotope_balance_summary()

    assert summary["chirality_imbalance"] == {
        "opposite_minus_same_four_overlap": 24,
        "same_minus_opposite_one_overlap": 24,
        "w33_block_size": 24,
    }


def test_cxxvii_mean_overlap_affine_chirality_law() -> None:
    summary = e_sector_tomotope_balance_summary()

    assert summary["mean_overlap"] == {
        "same_chirality": "17/8",
        "opposite_chirality": "23/8",
        "center": "5/2",
        "deviation": "3/8",
    }


def test_cxxvii_theorem_flags_are_all_true() -> None:
    summary = e_sector_tomotope_balance_summary()

    assert summary["theorem"] == {
        "full_three_cycle_layer_has_192_pairs": True,
        "full_layer_balances_96_four_and_96_one": True,
        "chirality_flip_swaps_counts_by_24": True,
        "mean_overlap_affine_chirality_law_holds": True,
    }
