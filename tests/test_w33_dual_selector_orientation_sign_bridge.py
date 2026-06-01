from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from w33_dual_selector_orientation_sign_bridge import (  # noqa: E402
    build_dual_selector_orientation_sign_summary,
)


def test_local_selector_average_and_sign_projector_boundary() -> None:
    summary = build_dual_selector_orientation_sign_summary()
    packet = summary["local_selector_packet"]
    theorem = packet["theorem"]

    assert packet["selector_order"] == 6
    assert packet["average_weight"] == "1/6"
    assert packet["trivial_projector"]["rational_matrix"] == [
        ["1/3", "1/3", "1/3"],
        ["1/3", "1/3", "1/3"],
        ["1/3", "1/3", "1/3"],
    ]
    assert packet["sign_projector"]["rational_matrix"] == [
        ["0", "0", "0"],
        ["0", "0", "0"],
        ["0", "0", "0"],
    ]
    assert theorem["plus_one_sixth_is_exact_local_selector_average"] is True
    assert theorem["sign_projector_vanishes_on_the_local_permutation_rep"] is True


def test_both_variants_tune_to_exact_minus_one_sixth() -> None:
    summary = build_dual_selector_orientation_sign_summary()
    packet = summary["dual_scale_packet"]
    theorem = packet["theorem"]

    assert packet["fixed_scale_sl3"] == 1 / 6
    assert packet["expected_scale_g2g2"] == -1 / 6
    assert packet["artifact_scale_g2g2"] == -1 / 6
    assert theorem["canonical_tunes_to_exact_minus_one_sixth"] is True
    assert theorem["sign_flipped_variant_also_tunes_to_exact_minus_one_sixth"] is True
    assert theorem["artifact_and_tuned_scale_agree"] is True
    assert packet["absolute_errors"]["canonical_to_expected"] < 1e-12
    assert packet["absolute_errors"]["sign_flipped_to_expected"] < 1e-12


def test_naive_sign_flip_breaks_mixed_jacobi_but_not_g1_g1_g2() -> None:
    summary = build_dual_selector_orientation_sign_summary()
    packet = summary["mixed_jacobi_pattern_packet"]
    theorem = packet["theorem"]
    canonical = packet["canonical"]
    sign_flipped = packet["sign_flipped"]

    assert canonical["max_residual"] < 1e-10
    assert canonical["patterns"]["g0_g1_g2"]["max_residual"] < 1e-10
    assert canonical["patterns"]["g1_g1_g2"]["max_residual"] < 1e-10
    assert canonical["patterns"]["g1_g2_g2"]["max_residual"] < 1e-10

    assert sign_flipped["patterns"]["g0_g1_g2"]["max_residual"] > 10.0
    assert sign_flipped["patterns"]["g1_g2_g2"]["max_residual"] > 10.0
    assert sign_flipped["patterns"]["g1_g1_g2"]["max_residual"] < 1e-10

    assert theorem["canonical_closes_all_mixed_patterns_at_exact_rational_scales"] is True
    assert theorem["sign_flipped_breaks_g0_g1_g2_badly"] is True
    assert theorem["sign_flipped_breaks_g1_g2_g2_badly"] is True
    assert theorem["sign_flipped_leaves_g1_g1_g2_small"] is True


def test_bridge_theorem_is_the_exact_no_go() -> None:
    summary = build_dual_selector_orientation_sign_summary()
    theorem = summary["bridge_theorem"]

    assert theorem["plus_one_sixth_is_exact_local_selector_average"] is True
    assert theorem["local_sign_projector_vanishes_exactly"] is True
    assert theorem["canonical_and_sign_flipped_variants_both_tune_to_minus_one_sixth"] is True
    assert theorem["canonical_bracket_closes_mixed_jacobi_at_exact_rational_scales"] is True
    assert theorem["naive_sign_flipped_dual_action_breaks_mixed_jacobi"] is True
    assert theorem["minus_one_sixth_is_not_a_simple_local_sign_or_dual_flip"] is True
