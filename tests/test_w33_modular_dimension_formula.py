from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_modular_dimension_formula import (  # noqa: E402
    derive_all,
    dim_M,
    dim_M_via_RR,
    dim_S,
    verify_12_periodicity,
    verify_delta_isomorphism,
    verify_hilbert_series,
    verify_low_weight_matches_known,
)


def test_dim_M_matches_rr_closed_form():
    summary = derive_all()
    assert summary["riemann_roch_check"]["all_match"] is True


def test_dim_M_low_weight_values():
    assert [dim_M(k) for k in range(0, 29, 2)] == [1, 0, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 3, 2, 3]


def test_dim_S_low_weight_values():
    assert [dim_S(k) for k in range(0, 29, 2)] == [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 2, 1, 2]


def test_riemann_roch_formula_samples():
    for k in (0, 2, 4, 12, 14, 24, 36, 60):
        assert dim_M(k) == dim_M_via_RR(k)


def test_12_periodicity():
    assert verify_12_periodicity(120)["all_match"] is True


def test_delta_isomorphism():
    assert verify_delta_isomorphism(120)["all_match"] is True


def test_known_low_weight_table():
    known = verify_low_weight_matches_known()
    assert known["M_matches"] is True
    assert known["S_matches"] is True


def test_hilbert_series():
    assert verify_hilbert_series(60)["all_match"] is True


def test_driver_summary_chain():
    summary = derive_all()
    for key, value in summary["summary_chain"].items():
        assert value is True, f"{key} = {value}"
