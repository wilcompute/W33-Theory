"""Pin the weight-12 Delta fourfold bridge.

Tests cover:
    (1) dim S_12 = 1;
    (2) Delta is the cusp line in the 12/455/691 triad;
    (3) the tau packet agrees with the L-function Delta layer;
    (4) the completed L-function satisfies the weight-12 functional equation;
    (5) Delta is the denominator of the Leech moonshine quotient;
    (6) the combined algebraic/arithmetic/analytic/moonshine spine closes.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "exploration"))


from w33_modular_dimension_formula import dim_S  # noqa: E402
from w33_weight12_delta_fourfold_bridge import build_summary  # noqa: E402


def test_dim_S_12_is_1():
    assert dim_S(12) == 1


def test_delta_is_the_cusp_line_in_the_weight12_triad():
    summary = build_summary()
    theorem = summary["weight12_delta_fourfold_theorem"]
    assert theorem["delta_is_the_cusp_line_in_the_12_455_691_weight_12_triad"] is True


def test_tau_packet_matches_lfunction_delta_on_first_twelve_terms():
    summary = build_summary()
    matches = summary["weight12_delta_fourfold_dictionary"]["tau_first_twelve_cross_match"]
    assert all(row["match"] for row in matches.values()) is True


def test_completed_lfunction_has_weight12_functional_equation():
    summary = build_summary()
    theorem = summary["weight12_delta_fourfold_theorem"]
    assert theorem["the_completed_lfunction_satisfies_Lambda_s_equals_Lambda_12_minus_s"] is True
    assert theorem["the_central_value_Lambda_6_is_real_and_positive"] is True


def test_delta_is_the_denominator_of_the_leech_moonshine_quotient():
    summary = build_summary()
    theorem = summary["weight12_delta_fourfold_theorem"]
    assert theorem["delta_is_the_denominator_of_the_leech_moonshine_quotient"] is True


def test_fourfold_bridge_summary_chain_is_all_true():
    summary = build_summary()
    theorem = summary["weight12_delta_fourfold_theorem"]
    assert theorem["the_weight_12_delta_line_closes_algebraic_arithmetic_analytic_and_moonshine_data"] is True
    assert all(theorem.values()) is True
