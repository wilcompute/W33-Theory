"""Pin the exact 3C = affine E8(q^3) moonshine bridge."""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from scripts.w33_leech_monster import (  # noqa: E402
    mckay_thompson_series,
    verify_fricke_prime_replicability,
)
from w33_3c_affine_e8_moonshine_bridge import build_summary  # noqa: E402
from w33_affine_e8 import affine_e8_series  # noqa: E402


def test_3c_matches_affine_e8_on_exp_3n_minus_1_slots():
    affine = affine_e8_series(q_order=12)
    t3c = mckay_thompson_series("3C", max_q_exp=35)
    assert t3c is not None
    for n, coeff in enumerate(affine["series"][:10]):
        assert t3c.get(3 * n - 1, 0) == coeff


def test_3c_has_no_off_grid_nonzero_terms_in_checked_range():
    t3c = mckay_thompson_series("3C", max_q_exp=35)
    assert t3c is not None
    for exp, coeff in t3c.items():
        if exp >= 0 and coeff != 0:
            assert (exp + 1) % 3 == 0


def test_first_three_nontrivial_3c_coefficients():
    t3c = mckay_thompson_series("3C", max_q_exp=10)
    assert t3c is not None
    assert t3c.get(2) == 248
    assert t3c.get(5) == 4124
    assert t3c.get(8) == 34752


def test_3c_prime_replicability_holds_with_x_cubed_minus_744():
    result = verify_fricke_prime_replicability("3C", max_q_exp=20)
    assert result["verified"] is True
    assert [int(c) for c in result["faber_coeffs"]] == [-744, 0, 0]


def test_3c_affine_bridge_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["threeC_affine_e8_theorem"]
    assert all(theorem.values()) is True
