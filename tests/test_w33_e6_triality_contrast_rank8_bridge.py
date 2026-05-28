from __future__ import annotations

from analysis.w33_e6_triality_contrast_rank8_bridge import (
    e6_triality_contrast_rank8_packet,
)


PACKET = e6_triality_contrast_rank8_packet()


def test_mccclxxxvi_representative_raw_and_contrast_ranks() -> None:
    representative = PACKET["representative_point"]

    assert representative["raw_adjacent_triplet_sum_packet"]["rows"] == 24
    assert representative["raw_adjacent_triplet_sum_packet"]["rank"] == 12

    modes = representative["contrast_modes"]
    assert modes["through"]["rank"] == 8
    assert modes["away"]["rank"] == 8
    assert modes["pair_sum"]["rank"] == 8
    assert modes["pair_diff"]["rank"] == 8


def test_mccclxxxvi_clean_gram_spectra() -> None:
    modes = PACKET["representative_point"]["contrast_modes"]

    assert modes["pair_sum"]["gram_spectrum"] == {"1.5": 4, "4.5": 4}
    assert modes["pair_diff"]["gram_spectrum"] == {"0.3": 4, "0.9": 4}
    assert modes["pair_sum"]["gram_diagonal_profile"] == {"3": 8}
    assert modes["pair_diff"]["gram_diagonal_profile"] == {"0.6": 8}


def test_mccclxxxvi_relation_locks() -> None:
    relations = PACKET["representative_point"]["contrast_modes"]["relations"]

    assert relations["pair_sum_gram_equals_5_pair_diff_gram_max_error"] < 1e-10
    assert relations["away_gram_equals_phi4_through_gram_max_error"] < 1e-8
    assert PACKET["max_relation_error"] < 1e-8


def test_mccclxxxvi_all_points_have_same_rank_profiles() -> None:
    profiles = PACKET["all_point_rank_profiles"]

    assert profiles["raw_e6_triplet_sum_rank"] == {"12": 40}
    assert profiles["through_contrast_rank"] == {"8": 40}
    assert profiles["away_contrast_rank"] == {"8": 40}
    assert profiles["pair_sum_contrast_rank"] == {"8": 40}
    assert profiles["pair_diff_contrast_rank"] == {"8": 40}


def test_mccclxxxvi_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())
    assert "not the naive A2-triplet collapse" in PACKET["reading"]
