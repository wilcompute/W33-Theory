"""Pin the linear/affine non-Fricke moonshine split."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from scripts.w33_leech_monster import (  # noqa: E402
    mckay_thompson_series,
    verify_rogers_ramanujan_5b_identity,
)
from w33_mckay_thompson_eta_quotients import eta_quotient_laurent  # noqa: E402
from w33_nonfricke_linear_moonshine_bridge import build_summary  # noqa: E402


def test_nonfricke_prime_classes_match_linear_eta_formula():
    for class_name, level, k in [("2B", 2, 24), ("3B", 3, 12), ("5B", 5, 6), ("7B", 7, 4), ("13B", 13, 2)]:
        x = eta_quotient_laurent(level, k, 12)
        t = mckay_thompson_series(class_name, max_q_exp=12)
        assert t is not None
        for exp in range(-1, 13):
            assert int(t.get(exp, 0)) == int(x[exp + 1] + (k if exp == 0 else 0))


def test_4c_matches_linear_eta_formula():
    x = eta_quotient_laurent(4, 8, 15)
    t = mckay_thompson_series("4C", max_q_exp=15)
    assert t is not None
    for exp in range(-1, 16):
        assert int(t.get(exp, 0)) == int(x[exp + 1] + (8 if exp == 0 else 0))


def test_4c_support_is_odd_only():
    t = mckay_thompson_series("4C", max_q_exp=15)
    assert t is not None
    for exp in range(0, 16, 2):
        assert int(t.get(exp, 0)) == 0


def test_5b_rogers_ramanujan_identity_holds():
    rr = verify_rogers_ramanujan_5b_identity(24)
    assert rr["verified"] is True
    assert rr["n_mismatches"] == 0


def test_nonfricke_linear_bridge_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["nonfricke_linear_moonshine_theorem"]
    assert all(theorem.values()) is True
