from __future__ import annotations

from analysis.w33_affine_tetracode_e8_glue_bridge import (
    affine_tetracode_e8_glue_packet,
    standard_tetracode,
)


PACKET = affine_tetracode_e8_glue_packet()


def test_mccclxxxvii_representative_is_standard_tetracode() -> None:
    representative = PACKET["representative_point"]

    assert len(representative["words_with_multiplicity"]) == 27
    assert len(representative["unique_words"]) == 9
    assert representative["multiplicity_profile"] == {"3": 9}
    assert representative["rank"] == 2
    assert representative["is_linear"] is True
    assert representative["is_self_dual_tetracode"] is True
    assert representative["matches_standard_tetracode_exactly"] is True
    assert {tuple(word) for word in representative["unique_words"]} == standard_tetracode()


def test_mccclxxxvii_tetracode_weight_profile() -> None:
    representative = PACKET["representative_point"]

    assert representative["weight_profile"] == {"0": 1, "3": 8}
    assert representative["basis"] == [[1, 0, 1, 2], [0, 1, 1, 1]]


def test_mccclxxxvii_all_anchor_profiles() -> None:
    profiles = PACKET["all_point_profiles"]

    assert profiles["rank"] == {"2": 40}
    assert profiles["multiplicity_profile"] == {"{'3': 9}": 40}
    assert profiles["self_dual_tetracode"] == {"True": 40}
    assert profiles["weight_profile"] == {"{'0': 1, '3': 8}": 40}


def test_mccclxxxvii_e8_glue_count() -> None:
    glue = PACKET["e8_glue_count"]

    assert glue["a2_four_root_subsystem"] == 24
    assert glue["nonzero_tetracode_words"] == 8
    assert glue["phase_lifts_per_nonzero_word"] == 27
    assert glue["tetracode_glue_roots"] == 216
    assert glue["total"] == 240
    assert glue["identity"] == "240 = 4*6 + 8*27"


def test_mccclxxxvii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())
    assert "A2^4 rank-8 contrast quotient" in PACKET["reading"]
